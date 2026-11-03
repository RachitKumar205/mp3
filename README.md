# MP3: Grouping countries by the issues of ICT workers

Our DOM207 MP3 project. The IMF gave us country averages for 37 countries on nine issues
that ICT workers face (`ICTIndiv.xlsx`), each measured two ways, and asked how the countries
group together. The write-up is in [`report/MP3_Report.pdf`](report/MP3_Report.pdf).

## Running it

You need Python 3.14 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

```bash
uv run python src/run_all.py
```

This rebuilds every table and figure from the raw file. To rebuild the PDF too (needs
pandoc and pdflatex):

```bash
uv run python src/build_report.py
```

## What's where

| Path | What it is |
|---|---|
| `src/01_prepare.py` | Data checks, extreme values, standardising the sum scores |
| `src/02_eda.py` | Descriptive statistics, issue correlations, heatmap, PCA |
| `src/03_cluster.py` | Elbow and silhouette, Ward and k-means on both scores, adjusted Rand index |
| `src/04_profile.py` | ANOVA with Shapiro–Wilk and Levene checks, Kruskal–Wallis, Tukey HSD, profiles |
| `src/config.py` | Paths, issue names and table helpers |
| `report/report.md` | The report text, built into the PDF |
| `output/tables/`, `output/figures/` | Everything the scripts produce |

## What we found

- The elbow and silhouette both point to **two clusters**. Ward and k-means, and the
  factor and sum scores, all give exactly the same two groups, even without the two most
  extreme countries.
- **Insecure but committed** (17 countries, mostly Asia, the Middle East and Africa):
  more job insecurity and self-efficacy, less strain, and much less intention to leave
  the employer or the profession.
- **Strained but mobile** (20 countries, mostly Europe and the Americas): more
  satisfaction, but also more overload, exhaustion and willingness to leave ICT.
- With three clusters the two scores disagree on which small group breaks off: Iran,
  Japan and South Korea with factor scores, and Bangladesh, Malaysia, Nigeria and
  Pakistan with sum scores. We treat these as watch lists.
- The groups cut across the usual split between advanced and emerging economies, and
  line up more with region, culture and how mobile the ICT labour market is.
