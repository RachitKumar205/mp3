"""Step 2: descriptive statistics and the exploratory figures.

Each figure supports a decision: the heatmap shows that countries differ in a structured
way, the correlation matrix shows two blocks of issues, and the PCA map shows how many
groups to expect before any clustering is run.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA

from config import CLEAN_CSV, FIG_DIR, FS, ISSUES, NAMES, save_values, write_table

sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)


def save(fig, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.png", dpi=200)
    plt.close(fig)


def describe(x: pd.Series) -> dict:
    return {"Mean": x.mean(), "Median": x.median(), "Variance": x.var(), "SD": x.std(),
            "Min": x.min(), "Max": x.max(), "Range": x.max() - x.min(), "Skewness": x.skew(),
            "Kurtosis": x.kurt(), "Q1": x.quantile(.25), "Q3": x.quantile(.75)}


def main() -> None:
    df = pd.read_csv(CLEAN_CSV).set_index("Country")

    # Descriptive statistics of both scores (sum scores on their original scale).
    rows = []
    for i in ISSUES:
        rows.append({"Issue": f"{NAMES[i]} (FS)", **describe(df[f"{i}_FS"])})
        rows.append({"Issue": f"{NAMES[i]} (S)", **describe(df[f"{i}_Sraw"])})
    rows.append({"Issue": "Respondents per country", **describe(df["Num"])})
    write_table("descriptives", pd.DataFrame(rows), floatfmt=".2f")

    corr = df[FS].corr()
    corr.index = corr.columns = ISSUES
    write_table("issue_correlations", corr.map(lambda v: f"{v:.2f}"), index=True, numparse=False)

    # Fig 1: correlations between the issues (two blocks).
    fig, ax = plt.subplots(figsize=(6.2, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, ax=ax,
                cbar_kws={"shrink": .8})
    ax.set_title("Correlations between the nine issues (factor scores)")
    save(fig, "fig1_issue_correlations")

    # PCA of the factor scores, used for the map and to order the heatmap.
    pca = PCA(n_components=2).fit(df[FS])
    pcs = pd.DataFrame(pca.transform(df[FS]), index=df.index, columns=["PC1", "PC2"])
    if pca.components_[0][ISSUES.index("TA")] < 0:  # orient PC1 so strain points right
        pcs["PC1"] *= -1
        pca.components_[0] *= -1
    pcs.to_csv(FIG_DIR.parent / "tables" / "pca_scores.csv")
    loadings = pd.DataFrame(pca.components_.T, index=ISSUES, columns=["PC1", "PC2"])
    write_table("pca_loadings", loadings.rename_axis("Issue"), index=True)

    # Fig 2: country x issue heatmap, countries ordered along PC1.
    order = pcs["PC1"].sort_values().index
    heat = df.loc[order, FS]
    heat.columns = ISSUES
    fig, ax = plt.subplots(figsize=(6.5, 9))
    sns.heatmap(heat, cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax, cbar_kws={"shrink": .5})
    ax.set(title="Factor scores by country (ordered by the first principal component)",
           xlabel="", ylabel="")
    save(fig, "fig2_country_heatmap")

    # Fig 3: PCA map of the countries with issue directions.
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(pcs["PC1"], pcs["PC2"], s=18, color="#2a6f97")
    for c, (x, y) in pcs.iterrows():
        ax.annotate(c, (x, y), fontsize=7, xytext=(3, 2), textcoords="offset points")
    scale = 1.6
    for i, (lx, ly) in loadings.iterrows():
        ax.arrow(0, 0, lx * scale, ly * scale, color="#d1495b", alpha=.6, head_width=.03)
        ax.text(lx * scale * 1.12, ly * scale * 1.12, i, color="#d1495b", fontsize=9, ha="center")
    ev = pca.explained_variance_ratio_
    ax.axhline(0, color="grey", lw=.5)
    ax.axvline(0, color="grey", lw=.5)
    ax.set(xlabel=f"PC1 ({ev[0]:.0%} of variance)", ylabel=f"PC2 ({ev[1]:.0%} of variance)",
           title="Countries on the first two principal components (factor scores)")
    save(fig, "fig3_pca_map")

    save_values({"pca_ev1": round(float(ev[0]), 3), "pca_ev2": round(float(ev[1]), 3),
                 "corr_wh_we": round(float(corr.loc["WH", "WE"]), 2),
                 "corr_ji_se": round(float(corr.loc["JI", "SE"]), 2),
                 "corr_ji_ta": round(float(corr.loc["JI", "TA"]), 2)})
    print(f"eda: PC1 {ev[0]:.0%}, PC2 {ev[1]:.0%}; 3 figures written")


if __name__ == "__main__":
    main()
