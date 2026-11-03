"""Step 3: cluster the 37 countries on both score sets.

Standard workflow: the elbow method and the average silhouette choose k; Ward
hierarchical clustering and k-means are run at each candidate k on the factor scores
(FS) and on the standardised sum scores (S); the adjusted Rand index (ARI) and
cross-tabulations show whether the two scores, and the two methods, give the same groups.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score, silhouette_samples,
                             silhouette_score)

from config import CLEAN_CSV, FIG_DIR, SCORES, SEED, save_values, write_table

BLUE, RED = "#2a6f97", "#d1495b"
CANDIDATES = [2, 3, 4]


def kmeans(X, k):
    return KMeans(k, n_init=200, random_state=SEED).fit(X)


def ward(X, k):
    return AgglomerativeClustering(k, linkage="ward").fit_predict(X)


def relabel(labels, reference):
    """Renumber clusters 1..k by the mean of a reference score, so labels read the same
    across methods and score sets (cluster 1 = lowest strain)."""
    order = pd.Series(reference).groupby(labels).mean().sort_values().index
    mapping = {old: new + 1 for new, old in enumerate(order)}
    return np.array([mapping[l] for l in labels])


def main() -> None:
    df = pd.read_csv(CLEAN_CSV).set_index("Country")
    strain = df[["WS_FS", "WO_FS", "WH_FS", "WE_FS", "TI_FS", "TA_FS"]].mean(axis=1).to_numpy()

    # 1. Choosing k: elbow (within-cluster sum of squares), silhouette, Calinski-Harabasz.
    rows = []
    for name, cols in SCORES.items():
        X = df[cols].to_numpy()
        for k in range(1, 11):
            km = kmeans(X, k)
            row = {"Score": name, "k": k, "WSS": km.inertia_}
            if k > 1:
                w = ward(X, k)
                row.update({"Silhouette (k-means)": silhouette_score(X, km.labels_),
                            "Silhouette (Ward)": silhouette_score(X, w),
                            "Calinski-Harabasz": calinski_harabasz_score(X, km.labels_),
                            "ARI k-means vs Ward": adjusted_rand_score(km.labels_, w)})
            rows.append(row)
    choose = pd.DataFrame(rows)
    choose["WSS drop %"] = (choose.groupby("Score")["WSS"].pct_change() * -100)
    write_table("choose_k", choose.astype({"k": str}))

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    for a, (name, col) in zip(ax, [("FS", "Factor scores"), ("S", "Sum scores (standardised)")]):
        c = choose[choose.Score == name]
        a.plot(c["k"], c["WSS"], "o-", color=BLUE, label="Within-cluster SS")
        a.set(xlabel="Number of clusters k", ylabel="Within-cluster sum of squares", title=col)
        b = a.twinx()
        b.plot(c["k"], c["Silhouette (k-means)"], "s--", color=RED, label="Average silhouette")
        b.set_ylabel("Average silhouette", color=RED)
        b.grid(False)
        for k in (2, 3):
            a.axvline(k, color="grey", lw=.6, ls=":")
    fig.legend(*[sum(x, []) for x in zip(*(a.get_legend_handles_labels() for a in
                                              [ax[0], ax[0].figure.axes[2]]))],
               loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=(0, .07, 1, 1))
    fig.savefig(FIG_DIR / "fig4_elbow_silhouette.png", dpi=200)
    plt.close(fig)

    # 2. Memberships at each candidate k, for both methods and both scores.
    labels = pd.DataFrame(index=df.index)
    for name, cols in SCORES.items():
        X = df[cols].to_numpy()
        for k in CANDIDATES:
            labels[f"{name}_km{k}"] = relabel(kmeans(X, k).labels_, strain)
            labels[f"{name}_ward{k}"] = relabel(ward(X, k), strain)
        labels[f"{name}_sil3"] = silhouette_samples(X, labels[f"{name}_km3"])
        labels[f"{name}_sil2"] = silhouette_samples(X, labels[f"{name}_km2"])
    labels.to_csv(FIG_DIR.parent / "tables" / "memberships.csv")

    # 3. Agreement: FS vs S and k-means vs Ward (adjusted Rand index).
    ari = []
    for k in CANDIDATES:
        ari.append({"k": k,
                    "FS vs S (k-means)": adjusted_rand_score(labels[f"FS_km{k}"], labels[f"S_km{k}"]),
                    "FS vs S (Ward)": adjusted_rand_score(labels[f"FS_ward{k}"], labels[f"S_ward{k}"]),
                    "k-means vs Ward (FS)": adjusted_rand_score(labels[f"FS_km{k}"], labels[f"FS_ward{k}"]),
                    "k-means vs Ward (S)": adjusted_rand_score(labels[f"S_km{k}"], labels[f"S_ward{k}"])})
    write_table("ari", pd.DataFrame(ari).astype({"k": str}))

    cross = pd.crosstab(labels["FS_km3"], labels["S_km3"], rownames=["FS cluster"], colnames=["S cluster"])
    cross.columns = [f"S{c}" for c in cross.columns]
    cross.index = [f"FS{c}" for c in cross.index]
    write_table("crosstab_k3", cross.rename_axis("k = 3"), index=True, floatfmt=".0f")

    members = []
    for name in SCORES:
        for k in (2, 3):
            for c in sorted(labels[f"{name}_km{k}"].unique()):
                who = labels.index[labels[f"{name}_km{k}"] == c]
                members.append({"Score": name, "k": k, "Cluster": c, "n": len(who),
                                "Countries": ", ".join(who)})
    write_table("members", pd.DataFrame(members), numparse=False)

    # 4. Sensitivity: k-means without the two most extreme countries (Iran, Nigeria).
    sens = []
    keep = ~df.index.isin(["Iran", "Nigeria"])
    for name, cols in SCORES.items():
        X = df.loc[keep, cols].to_numpy()
        for k in (2, 3):
            lab = relabel(kmeans(X, k).labels_, strain[keep])
            sens.append({"Score": name, "k": k,
                         "ARI with full-sample clusters": adjusted_rand_score(
                             labels.loc[keep, f"{name}_km{k}"], lab),
                         "Silhouette": silhouette_score(X, lab)})
    write_table("sensitivity", pd.DataFrame(sens).astype({"k": str}))

    # 5. Ward dendrogram on the factor scores.
    Z = linkage(df[SCORES["FS"]].to_numpy(), method="ward")
    fig, ax = plt.subplots(figsize=(10, 4.2))
    cut = (Z[-2, 2] + Z[-3, 2]) / 2
    dendrogram(Z, labels=df.index.tolist(), leaf_rotation=90, leaf_font_size=8,
               color_threshold=cut, above_threshold_color="grey", ax=ax)
    ax.axhline(cut, color=RED, ls="--", lw=1)
    ax.set(ylabel="Ward linkage distance", title="Ward hierarchical clustering of the factor scores")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig5_dendrogram.png", dpi=200)
    plt.close(fig)

    c2 = choose.set_index(["Score", "k"])
    save_values({
        **{f"wss_drop_{s}_{k}": round(float(c2.loc[(s, k), "WSS drop %"]), 1)
           for s in SCORES for k in range(2, 6)},
        **{f"sil_{s}_{k}": round(float(c2.loc[(s, k), "Silhouette (k-means)"]), 3)
           for s in SCORES for k in range(2, 6)},
        **{f"ari_k{r['k']}_fs_s": round(float(r["FS vs S (k-means)"]), 2) for r in ari},
        **{f"ari_k{r['k']}_km_ward_fs": round(float(r["k-means vs Ward (FS)"]), 2) for r in ari},
        "n_switch_k3": int((labels["FS_km3"] != labels["S_km3"]).sum()),
        "switch_k3": ", ".join(labels.index[labels["FS_km3"] != labels["S_km3"]]),
        "neg_sil_fs3": ", ".join(labels.index[labels["FS_sil3"] < 0]) or "none",
    })
    print("cluster:", pd.DataFrame(ari).round(2).to_dict("records"))


if __name__ == "__main__":
    main()
