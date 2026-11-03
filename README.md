# MP3: Grouping countries by the issues of ICT workers

Our DOM207 MP3 project. The IMF gave us country averages for 37 countries on nine issues
that ICT workers face (`ICTIndiv.xlsx`), each measured two ways, and asked how the countries
group together. The write-up is in [`report/MP3_Report.pdf`](report/MP3_Report.pdf).

## Running it

You need Python 3.14, [uv](https://docs.astral.sh/uv/), and pandoc with pdflatex for the PDF.

```bash
uv sync
```

Then open `mp3.ipynb` in Jupyter or VS Code with the project's environment and run all
cells from the project folder. The notebook holds all the code: it reads the raw file,
writes every table to `output/tables/` and every figure to `output/figures/`, and builds
`report/MP3_Report.pdf` from `report/report.md` at the end.

| Section of the notebook | What it does |
|---|---|
| Setup | Paths, issue names and table helpers |
| 1. Data preprocessing | Data checks, extreme values, standardising the sum scores |
| 2. Data visualization | Descriptive statistics, issue correlations, heatmap, PCA |
| 3. Clustering | Elbow and silhouette, Ward and k-means on both scores, adjusted Rand index |
| 4. Do the clusters differ? | ANOVA with Shapiro–Wilk and Levene checks, Kruskal–Wallis, Tukey HSD, profiles |
| 5. Build the PDF report | Turns `report/report.md` into the PDF |

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
