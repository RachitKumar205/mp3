"""Step 4: do the clusters really differ, and how?

One-way ANOVA on each issue across clusters, with Shapiro-Wilk (normality within each
cluster) and Levene (equal variances) as assumption checks and Kruskal-Wallis as the
non-parametric fallback. Tukey HSD shows which pairs of the three-cluster solution
differ. Cluster profiles (mean score per issue) give each group its character.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from config import CLEAN_CSV, FIG_DIR, ISSUES, NAMES, SCORES, TAB_DIR, save_values, write_table

COLOURS = {1: "#2a6f97", 2: "#d1495b", 3: "#edae49"}


def stars(p):
    return "***" if p < .01 else "**" if p < .05 else "*" if p < .10 else ""


def anova_table(df, labels, score):
    rows = []
    for i in ISSUES:
        col = f"{i}_{score}"
        groups = [df.loc[labels == c, col] for c in sorted(labels.unique())]
        f, p = stats.f_oneway(*groups)
        lev_p = stats.levene(*groups, center="median").pvalue
        sw = [stats.shapiro(g).pvalue for g in groups if len(g) >= 3]
        kw_p = stats.kruskal(*groups).pvalue
        means = {f"Mean C{c}": g.mean() for c, g in zip(sorted(labels.unique()), groups)}
        ss_b = sum(len(g) * (g.mean() - df[col].mean()) ** 2 for g in groups)
        ss_t = ((df[col] - df[col].mean()) ** 2).sum()
        rows.append({"Issue": NAMES[i], **means, "F": f, "p (ANOVA)": p, "Eta²": ss_b / ss_t,
                     "Levene p": lev_p, "Min Shapiro p": min(sw), "p (Kruskal)": kw_p,
                     "Sig.": stars(p)})
    return pd.DataFrame(rows)


def main() -> None:
    df = pd.read_csv(CLEAN_CSV).set_index("Country")
    m = pd.read_csv(TAB_DIR / "memberships.csv", index_col=0).loc[df.index]
    vals = {}

    for score in SCORES:
        for k in (2, 3):
            t = anova_table(df, m[f"{score}_km{k}"], score)
            write_table(f"anova_{score}_k{k}", t, floatfmt=".3f")
            vals[f"anova_{score}_k{k}_nsig"] = int((t["p (ANOVA)"] < .05).sum())
            vals[f"anova_{score}_k{k}_nsig_kw"] = int((t["p (Kruskal)"] < .05).sum())
            vals[f"anova_{score}_k{k}_levene_fail"] = int((t["Levene p"] < .05).sum())
            vals[f"anova_{score}_k{k}_shapiro_fail"] = int((t["Min Shapiro p"] < .05).sum())
            for _, r in t.iterrows():
                key = [i for i in ISSUES if NAMES[i] == r["Issue"]][0]
                vals[f"eta_{score}_k{k}_{key}"] = round(float(r["Eta²"]), 2)
                vals[f"p_{score}_k{k}_{key}"] = float(r["p (ANOVA)"])

    # Tukey HSD for the three-cluster solution of each score.
    tk = []
    for score in SCORES:
        lab = m[f"{score}_km3"]
        for i in ISSUES:
            res = pairwise_tukeyhsd(df[f"{i}_{score}"], lab)
            for row in res.summary().data[1:]:
                g1, g2, diff, p = row[0], row[1], row[2], row[3]
                tk.append({"Score": score, "Issue": NAMES[i], "Pair": f"C{g1} vs C{g2}",
                           "Mean difference": diff, "p (Tukey)": p, "Sig.": stars(p)})
    tk = pd.DataFrame(tk)
    write_table("tukey_k3", tk)
    wide = tk.pivot_table(index="Issue", columns=["Score", "Pair"], values="p (Tukey)").loc[
        [NAMES[i] for i in ISSUES]]
    wide.columns = [f"{s}: {p}" for s, p in wide.columns]
    write_table("tukey_k3_wide", wide.map(lambda p: f"{p:.3f}{stars(p)}"), index=True, numparse=False)

    # Cluster profiles on the factor scores (k = 2 and k = 3).
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.9), sharey=True)
    x = np.arange(len(ISSUES))
    for a, k in zip(ax, (2, 3)):
        lab = m[f"FS_km{k}"]
        for c in sorted(lab.unique()):
            means = df.loc[lab == c, [f"{i}_FS" for i in ISSUES]].mean()
            a.plot(x, means.values, "o-", color=COLOURS[c], label=f"Cluster {c} (n = {(lab == c).sum()})")
        a.axhline(0, color="grey", lw=.6)
        a.set_xticks(x, ISSUES)
        a.set(title=f"{k} clusters (factor scores)", ylabel="Mean factor score" if k == 2 else "")
        a.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig6_profiles.png", dpi=200)
    plt.close(fig)

    # PCA map coloured by the two-cluster solution, three-cluster subgroups marked.
    pcs = pd.read_csv(TAB_DIR / "pca_scores.csv", index_col=0).loc[df.index]
    fig, ax = plt.subplots(figsize=(8, 5.6))
    for c in (1, 2):
        sel = m["FS_km2"] == c
        ax.scatter(pcs.loc[sel, "PC1"], pcs.loc[sel, "PC2"], s=28, color=COLOURS[c],
                   label=f"Cluster {c}")
    for name, marker, label in [("FS_km3", "o", "Split off at k = 3 (factor scores)"),
                                ("S_km3", "s", "Split off at k = 3 (sum scores)")]:
        sel = m[name] == 1
        ax.scatter(pcs.loc[sel, "PC1"], pcs.loc[sel, "PC2"], s=130, facecolors="none",
                   edgecolors="black", marker=marker, lw=1, label=label)
    for cn, (px, py) in pcs.iterrows():
        ax.annotate(cn, (px, py), fontsize=7, xytext=(4, 2), textcoords="offset points")
    ax.axhline(0, color="grey", lw=.5)
    ax.axvline(0, color="grey", lw=.5)
    ax.set(xlabel="PC1: strain and exit intentions (right) vs insecurity and self-efficacy (left)",
           ylabel="PC2: friendship circles and self-efficacy",
           title="The two clusters on the first two principal components")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig7_cluster_map.png", dpi=200)
    plt.close(fig)

    save_values(vals)
    print("profile:", {k: v for k, v in vals.items() if "nsig" in k or "fail" in k})


if __name__ == "__main__":
    main()
