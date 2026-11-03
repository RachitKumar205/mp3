"""Step 1: check the IMF file and prepare both score sets for clustering.

The factor scores (FSMean) are already standardised. The sum scores (Smean) sit on a
different scale for each issue, because each issue has a different number of items, so
they are z-scored before clustering. Nothing is imputed or dropped.
"""

import pandas as pd

from config import CLEAN_CSV, ISSUES, RAW_XLSX, save_values, write_table


def main() -> None:
    raw = pd.read_excel(RAW_XLSX, sheet_name="ClusterData")
    raw.columns = [c.strip() for c in raw.columns]

    checks = {
        "Countries": len(raw),
        "Columns": raw.shape[1],
        "Missing cells": int(raw.isna().sum().sum()),
        "Duplicate countries": int(raw["Country"].duplicated().sum()),
        "Duplicate codes": int(raw["Code"].duplicated().sum()),
        "Non-numeric score cells": int(sum(pd.to_numeric(raw[c], errors="coerce").isna().sum()
                                           for c in raw.columns if "mean" in c.lower())),
        "Codes missing from 1-46": ", ".join(str(c) for c in sorted(set(range(1, 47)) - set(raw["Code"]))),
    }
    write_table("data_checks", pd.DataFrame(checks.items(), columns=["Check", "Result"]),
                numparse=False)

    df = raw[["Country", "Code", "Num"]].copy()
    for i in ISSUES:
        df[f"{i}_FS"] = raw[f"{i}_FSMean"]
        s = raw[f"{i}_Smean"]
        df[f"{i}_Sraw"] = s
        df[f"{i}_S"] = (s - s.mean()) / s.std()

    # Countries more than 2.5 standard deviations from the mean on any issue.
    rows = []
    for score, suffix in [("Factor score", "_FS"), ("Sum score", "_S")]:
        for i in ISSUES:
            col = df[f"{i}{suffix}"]
            z = (col - col.mean()) / col.std()
            for country, v in z[z.abs() > 2.5].items():
                rows.append({"Country": df.at[country, "Country"], "Issue": i, "Score": score,
                             "z": round(float(v), 2)})
    extremes = pd.DataFrame(rows).sort_values(["Country", "Issue", "Score"])
    write_table("extremes", extremes, floatfmt=".2f")

    agreement = pd.DataFrame({"Issue": ISSUES,
                              "r(FS, S)": [df[f"{i}_FS"].corr(df[f"{i}_S"]) for i in ISSUES]})
    write_table("score_agreement", agreement)

    df.to_csv(CLEAN_CSV, index=False)
    save_values({
        "n_countries": len(df), "n_resp_total": int(df["Num"].sum()),
        "n_resp_min": int(df["Num"].min()), "n_resp_max": int(df["Num"].max()),
        "resp_min_country": df.loc[df["Num"].idxmin(), "Country"],
        "resp_max_country": df.loc[df["Num"].idxmax(), "Country"],
        "r_fs_s_min": round(float(agreement["r(FS, S)"].min()), 3),
        "r_fs_s_max": round(float(agreement["r(FS, S)"].max()), 3),
    })
    print(f"prepared {len(df)} countries; {len(extremes)} extreme values flagged, none removed")


if __name__ == "__main__":
    main()
