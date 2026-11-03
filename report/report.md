```{=latex}
\begin{titlepage}
\centering
\vspace*{6cm}
{\LARGE\bfseries International Monetary Fund\par}
\vspace{0.8cm}
{\Large DOM207 MP3 Report\par}
\vspace{2.5cm}
\begin{tabular}{ll}
\toprule
\textbf{Team member} & \textbf{Roll number} \\
\midrule
Lalit Maurya & 2310110164 \\
Jia Swapnil Khot & 2310110491 \\
Rachit Kumar & 2310110234 \\
\bottomrule
\end{tabular}
\vfill
{\large \today\par}
\end{titlepage}
```

# Introduction

The International Monetary Fund (IMF) asked us to find out how countries can be grouped by the issues that their information and communications technology (ICT) workers face, and to show that the grouping makes sense from a macroeconomic point of view. The data covers 37 countries and nine issues: dependence on friendship circles (FC), job insecurity (JI), self-efficacy (SE), work satisfaction (WS), work overload (WO), work-home conflict (WH), work exhaustion (WE), turnover intention (TI, leaving the employer) and turnaway intention (TA, leaving the ICT profession altogether). Each issue comes with two scores, a factor score and a sum score, and the IMF asked that the grouping be done with both and the results compared.

We set out to answer three questions. How many natural groups of countries are there, and which countries belong to each? Do the factor scores and the sum scores lead to the same groups? And what do the groups have in common economically, so that the IMF can use them in its policy work?

The data is a set of country averages, built from 93 to 634 ICT workers per country. Our groups therefore describe countries, not individual workers, and the interpretation rests on economic reasoning rather than on additional country data.

**Our recommendations in brief:**

1. Use a two-group classification of countries for ICT labour policy, not the usual split between advanced and emerging economies, which these groups cut across.
2. In the "strained but mobile" group (mostly Europe and the Americas), treat exhaustion and exit from the ICT profession as the main risk, and focus on workload and working-time policy.
3. In the "insecure but committed" group (mostly Asia, the Middle East and Africa), treat job insecurity as the main risk, and focus on safety nets, reskilling and deeper tech job markets.
4. Keep two small watch lists, Iran, Japan and South Korea, and Bangladesh, Malaysia, Nigeria and Pakistan, whose position depends on which score is used.

# Data preprocessing

The file has one sheet with 37 rows and 21 columns: the country, a country code, the number of respondents and the two scores for each of the nine issues. We checked it in Python with pandas [7]. There are no missing values, no text in numeric columns and no duplicated countries or codes. The codes run from 1 to 46 with nine gaps, so the IMF has evidently kept 37 of the 46 countries in the original study. Nothing needed correcting.

**Two kinds of score.** The factor scores (FS) are already standardised, with a mean close to zero for every issue. The sum scores (S) are on a different scale for each issue, because each issue is measured with a different number of questionnaire items: friendship circles average 5.8 and work satisfaction 13.4. Distance-based clustering would let the issues with the largest scales dominate, so we standardised every sum score to a mean of 0 and a standard deviation of 1 before clustering. The two scores agree closely for each issue, with correlations between 0.93 (work satisfaction) and 0.998 (friendship circles), so any difference in the groups will come from the details, not from a different picture of the countries.

**Extreme values.** Ten values lie more than 2.5 standard deviations from the mean (Table 1). Iran scores very high on job insecurity and self-efficacy in both scores, and Nigeria very low on work overload, work-home conflict and exhaustion, but only in the sum scores. These are real country averages, not data-entry errors, so we kept them. Because a few extreme countries can pull cluster centres, we re-ran the clustering without Iran and Nigeria as a check (Section 5).

| Country | Issue | Score | z |
|:-----------|:----------------------|:------------------|------:|
| India | Job insecurity | Factor score | $-2.54$ |
| Iran | Job insecurity | Factor and sum score | $2.66$, $2.67$ |
| Iran | Self-efficacy | Factor and sum score | $3.36$, $3.35$ |
| Italy | Turnover intention | Factor score | $2.56$ |
| Nigeria | Work overload, work-home conflict, exhaustion | Sum score | $-2.75$ to $-3.13$ |
| Pakistan | Work-home conflict | Factor score | $-2.61$ |

Table: Values more than 2.5 standard deviations from the mean (kept in the data)

The number of respondents varies from 93 (Nigeria) to 634 (Thailand). We did not weight countries by it, since the IMF's question is about countries, but averages from small samples are less precise, which matters for Nigeria in particular.

# Data visualization

**The issues form two blocks.** Work overload, work-home conflict, exhaustion, satisfaction, turnover and turnaway all rise together across countries, and work-home conflict and exhaustion are the most closely linked (correlation 0.84, Figure 1a). Job insecurity and self-efficacy form a second block that moves the other way: countries where ICT workers feel insecure also report high self-efficacy (0.73) and much lower intention to leave the profession ($-0.72$). Friendship circles sit largely on their own. A single principal component captures 54% of the variation in the nine factor scores, a strong hint that countries split along one main dimension.

**Countries line up along that dimension.** When the countries are ordered by this first component (Figure 1b), the top of the heatmap is dominated by East and South Asian, Middle Eastern and African countries with high insecurity and self-efficacy, and the bottom by European and American countries with high strain and exit intentions. The change is gradual for most issues, so the clustering has to decide where the boundary lies.

```{=latex}
\begin{figure}[htbp]
\centering
\begin{subfigure}[t]{0.49\textwidth}\centering
\includegraphics[width=\textwidth]{output/figures/fig1_issue_correlations.png}
\caption{Correlations between the issues}
\end{subfigure}\hfill
\begin{subfigure}[t]{0.42\textwidth}\centering
\includegraphics[width=\textwidth]{output/figures/fig2_country_heatmap.png}
\caption{Factor scores by country}
\end{subfigure}
\caption{The nine issues across the 37 countries (factor scores).}
\end{figure}
```

# Hypotheses and theory building

We frame the issues with the job demands-resources model [1]. Demands such as work overload, work-home conflict and job insecurity wear workers down and lead to exhaustion, and exhaustion leads to withdrawal, first from the employer (turnover) and then from the profession (turnaway). Resources such as friendship circles, self-efficacy and satisfaction buffer this process. At the level of countries, demands, resources and the realistic options for leaving all depend on the economy and the labour market. That gives four macroeconomic hypotheses, stated before any clustering was done:

| | Hypothesis |
|:-----|:---------------------------------------------------------------------------------|
| H1 | The groups follow the IMF's split between advanced and emerging or developing economies |
| H2 | The groups follow culture and region, separating more collectivist from more individualist societies [2] |
| H3 | Where ICT labour markets are deep and skills are portable, workers feel less insecure but are more willing to leave their employer and the profession |
| H4 | Demands, strain and withdrawal move together, as the job demands-resources model predicts |

Table: Hypotheses

# Analysis

**Method.** We grouped the countries with the two standard methods for this kind of data, using Euclidean distance on the nine standardised issues. Ward's hierarchical clustering [3] starts with each country on its own and merges at each step the two groups whose merger adds least to the spread within groups. k-means [4] places $k$ cluster centres and moves them until each country sits with its nearest centre; we used 200 random starts and a fixed seed, so the result can be reproduced. Both methods were run on the factor scores and on the standardised sum scores, with scikit-learn [6].

**Choosing the number of clusters.** We used the elbow method and the average silhouette [5]. The elbow method plots the within-cluster sum of squares against $k$ and looks for the point where adding a cluster stops paying off. The silhouette measures, for each country, how much closer it is to its own cluster than to the next one, from $-1$ to $1$. Both point the same way for both scores (Table 3, Figure 2). Going from one to two clusters removes 42% of the within-cluster variation for the factor scores and 38% for the sum scores; every later step removes less than 20%. The average silhouette is highest at $k = 2$ (0.35 and 0.32), only slightly lower at $k = 3$, and falls sharply at $k = 4$. The Calinski–Harabasz index also peaks at $k = 2$. We therefore take two clusters as the main solution and examine three as a refinement.

| | Factor scores | | | | Sum scores | | | |
|:--|------:|------:|------:|------:|------:|------:|------:|------:|
| k | WSS | Drop | Silhouette | CH | WSS | Drop | Silhouette | CH |
| 2 | 18.83 | 41.8% | 0.345 | 25.1 | 199.99 | 38.3% | 0.318 | 21.7 |
| 3 | 15.69 | 16.7% | 0.320 | 18.1 | 161.74 | 19.1% | 0.298 | 17.1 |
| 4 | 13.73 | 12.5% | 0.195 | 14.9 | 139.92 | 13.5% | 0.197 | 14.5 |
| 5 | 12.17 | 11.3% | 0.171 | 13.3 | 118.51 | 15.3% | 0.223 | 13.9 |

Table: Choosing the number of clusters (WSS: within-cluster sum of squares; Drop: reduction from $k-1$; CH: Calinski–Harabasz index)

![Elbow plot (within-cluster sum of squares, solid) and average silhouette (dashed) for k-means on both scores.](output/figures/fig4_elbow_silhouette.png){width=88%}

**Ward and k-means agree.** The Ward dendrogram (Figure 3) has one dominant merge: two groups that join only at the very top, far above every other merge. Cutting it into two or three groups gives exactly the same memberships as k-means with both scores (adjusted Rand index 1.00, Table 4). The adjusted Rand index [8] compares two groupings, from about 0 for agreement no better than chance to 1 for identical groups. The two methods only part ways at $k = 4$ (0.65 and 0.55), another sign that four clusters force splits the data does not support.

![Ward hierarchical clustering of the factor scores. The dashed line cuts the tree into three groups.](output/figures/fig5_dendrogram.png){width=95%}

**Factor scores and sum scores give the same two groups, but not the same three.** With two clusters, the factor scores and the sum scores put every one of the 37 countries in the same group (adjusted Rand index 1.00). With three clusters they agree only partly (0.78), and seven countries move (Table 5). The large European and American group of 20 is identical either way. The difference lies in which small group breaks away from the other 17 countries. With the factor scores it is Iran, Japan and South Korea, which stand out on friendship circles, self-efficacy and job insecurity. With the sum scores it is Bangladesh, Malaysia, Nigeria and Pakistan, which stand out on very low overload, work-home conflict and exhaustion. Section 6 explains why the scores behave differently.

| k | FS vs S (k-means) | FS vs S (Ward) | k-means vs Ward (FS) | k-means vs Ward (S) |
|:--|------:|------:|------:|------:|
| 2 | 1.00 | 1.00 | 1.00 | 1.00 |
| 3 | 0.78 | 0.78 | 1.00 | 1.00 |
| 4 | 0.67 | 0.62 | 0.65 | 0.55 |

Table: Agreement between scores and methods (adjusted Rand index)

| | S cluster 1 (4) | S cluster 2 (13) | S cluster 3 (20) |
|:-----------------------------|------:|------:|------:|
| FS cluster 1: Iran, Japan, South Korea | 0 | 3 | 0 |
| FS cluster 2 (14) | 4 | 10 | 0 |
| FS cluster 3 (20) | 0 | 0 | 20 |

Table: Three-cluster memberships with factor scores (rows) and sum scores (columns)

**The two-cluster solution is stable.** Without Iran and Nigeria, the two-cluster memberships of the remaining 35 countries are unchanged with both scores (adjusted Rand index 1.00). The three-cluster solution is less stable (0.72 for factor scores and 0.52 for sum scores), because its small groups are built around exactly these extreme countries. The per-country silhouettes show where the boundary is soft. Russia sits on the border between the two clusters (silhouette $-0.01$), with Poland (0.15) and Canada (0.18) close to it, and every other country fits its cluster better than the alternative.

**Do the clusters differ, and on which issues?** We compared the clusters on each issue with a one-way ANOVA (Table 9), and checked its two assumptions. The Shapiro–Wilk test checks that scores are roughly normal within each cluster, and Levene's test checks that the spread is similar across clusters. With two clusters on the factor scores, only one Shapiro–Wilk test (job insecurity) and one Levene test (work overload) reject at 5%; on the sum scores, two Shapiro–Wilk tests and no Levene test reject. Because the clusters are small, we repeated every comparison with the Kruskal–Wallis test, which assumes neither. It gives the same verdict as ANOVA on every issue, for both scores and both numbers of clusters. One caution: the clusters were formed from these same scores, so significant differences are expected and the p-values overstate the evidence. What the ANOVA adds is the size of each difference (eta squared, the share of variation explained by the clusters), which shows which issues drive the split. For the three-cluster solutions, Tukey's test identifies which pairs of clusters differ (Table 6).

{{float:tukey_k3_wide|Tukey HSD p-values for each pair of clusters in the three-cluster solutions (* p < 0.10, ** p < 0.05, *** p < 0.01)}}

# Results

**Descriptive statistics.** Table 7 summarises both scores for every issue. The factor scores are centred near zero by construction; the sum scores show the different scales that made standardisation necessary. Self-efficacy is the most skewed issue (skewness 1.1 for both scores), because of Iran.

{{float:descriptives|Descriptive statistics of the 37 country averages (S on its original scale; kurtosis is excess kurtosis)}}

**Two groups of countries.** The robust solution divides the countries into two clusters of 17 and 20 (Table 8). Their profiles are close to mirror images (Figure 4). Eight of the nine issues differ significantly between them with both scores (Table 9); only friendship circles do not. The largest differences are in work satisfaction, turnaway intention and job insecurity, each of which the clusters explain more than half the variation in. Figure 5 places the two clusters on the first two principal components, where they fall on either side of the vertical axis.

| Cluster | n | Countries |
|:--------------------------------|---:|:------------------------------------------------------------|
| 1. Insecure but committed | 17 | Bangladesh, Canada, China, France, Ghana, Iran, Japan, Jordan, Malaysia, Nigeria, Pakistan, Russia, South Korea, Taiwan, Thailand, Turkey, Vietnam |
| 2. Strained but mobile | 20 | Argentina, Brazil, Egypt, Finland, Germany, Greece, Hungary, India, Italy, Lithuania, Macedonia, Mexico, New Zealand, Peru, Poland, Portugal, Romania, South Africa, UK, USA |

Table: The two clusters (identical with factor scores and sum scores, and with Ward and k-means)

![Mean factor score of each cluster on the nine issues, for two and three clusters.](output/figures/fig6_profiles.png){width=92%}

| | Factor scores | | | | | Sum scores (standardised) | | |
|:-------------------|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| Issue | C1 | C2 | F | Eta² | p (KW) | C1 | C2 | Eta² |
| Friendship circles | 0.06 | $-0.06$ | 1.3 | 0.04 | 0.411 | 0.17 | $-0.15$ | 0.03 |
| Job insecurity | 0.21 | $-0.20$ | 47.3\*\*\* | 0.57 | <0.001 | 0.79 | $-0.67$ | 0.55\*\*\* |
| Self-efficacy | 0.22 | $-0.22$ | 18.5\*\*\* | 0.35 | <0.001 | 0.60 | $-0.51$ | 0.31\*\*\* |
| Work satisfaction | $-0.27$ | 0.28 | 59.3\*\*\* | 0.63 | <0.001 | $-0.78$ | 0.66 | 0.53\*\*\* |
| Work overload | $-0.17$ | 0.13 | 17.7\*\*\* | 0.34 | 0.001 | $-0.60$ | 0.51 | 0.31\*\*\* |
| Work-home conflict | $-0.21$ | 0.15 | 28.6\*\*\* | 0.45 | <0.001 | $-0.69$ | 0.58 | 0.41\*\*\* |
| Work exhaustion | $-0.19$ | 0.16 | 23.8\*\*\* | 0.40 | <0.001 | $-0.66$ | 0.56 | 0.37\*\*\* |
| Turnover intention | $-0.13$ | 0.13 | 10.8\*\*\* | 0.24 | 0.005 | $-0.54$ | 0.46 | 0.25\*\*\* |
| Turnaway intention | $-0.31$ | 0.31 | 48.3\*\*\* | 0.58 | <0.001 | $-0.88$ | 0.75 | 0.68\*\*\* |

Table: Cluster means and one-way ANOVA for the two-cluster solution (KW: Kruskal–Wallis; *** p < 0.01)

![The two clusters on the first two principal components, with the countries that split off at k = 3 marked.](output/figures/fig7_cluster_map.png){width=80%}

**Cluster 1: insecure but committed.** ICT workers in these 17 countries feel less secure in their jobs and less satisfied, but they are confident in their own abilities, report less overload, work-home conflict and exhaustion, and are much less inclined to leave their employer or the profession. Fifteen of the 17 lie in East, Southeast and South Asia, the Middle East, Africa or Russia. Three economic features help explain the pattern. First, in most of these economies ICT jobs pay far above the national median wage and carry high social status, so leaving the profession would mean a large loss; the low turnaway intention reflects that cost. Second, tech job markets are thinner, with fewer employers and less mobility between them, so a lost job is harder to replace. That explains why insecurity is higher and why workers stay put instead of searching: insecurity and commitment are two sides of the same limited outside options. Third, most of these societies are more collectivist [2], with stronger norms of loyalty to the employer and long careers inside one firm, especially in Japan, South Korea and Taiwan, and with family networks that absorb home demands and lower work-home conflict. High self-efficacy fits a profession that is selective and prestigious in these economies.

**Cluster 2: strained but mobile.** In these 20 countries ICT workers feel more secure and more satisfied, but they also report more overload, work-home conflict and exhaustion, and they are much more willing to leave both their employer and the profession. Sixteen of the 20 are in Europe or the Americas. These are mostly deep, open ICT labour markets in which skills are portable. A lost job is easy to replace, so insecurity is low, and the same ease of movement makes turnover and turnaway realistic choices rather than risky ones. The Central and Eastern European members, Hungary, Lithuania, Macedonia, Poland and Romania, are nearshoring hubs inside or next to the European labour market, where moving abroad is also an option; Mexico, Peru, Brazil and Argentina play a similar role for North America. India belongs here for a related reason: its large outsourcing industry is known for some of the highest attrition rates among IT workers anywhere, which matches the cluster's high turnaway and very low insecurity. In more individualist cultures [2], conflicts between work and home are also felt and reported more strongly.

**Countries at the edges.** Two members of Cluster 1, Canada and France, are advanced Western economies. France's strong employment protection and short legal working week fit the low overload and turnover of Cluster 1, and Canada sits close to the boundary (silhouette 0.18). Russia lies exactly on the boundary between the two clusters and should be treated as belonging to neither.

**The three-cluster refinements depend on the score.** With the factor scores, Iran, Japan and South Korea form their own group, with very high self-efficacy, friendship circles and job insecurity (Figure 4, right). Japan and South Korea combine company-centred social lives with intense workplace pressure, and Iran's sanctions-affected economy adds insecurity to a highly educated, tightly networked tech workforce. With the sum scores, Bangladesh, Malaysia, Nigeria and Pakistan form a group instead, defined by extremely low overload, work-home conflict and exhaustion, at about 1.7 standard deviations below the mean. The difference comes from how the scores are built. A sum score adds up the raw answers to every item, so a country that answers some items at the extreme of the scale moves a long way. A factor score weights the items by how well they measure the issue and filters out item-specific noise, which damps these extremes. Nigeria's very low strain appears only in the sum scores, and Nigeria has the smallest sample (93 workers). The factor scores are therefore the more reliable basis for the refinement. Neither refinement survives the removal of the extreme countries well, so we treat them as watch lists rather than as separate groups.

**Hypotheses.** Table 10 summarises the verdicts.

| | Result | Finding |
|:-----|:--------------------------------------------------------------|:----------------|
| H1 | Advanced economies fall in both clusters (about 9 of 20 in Cluster 2 and 5 of 17 in Cluster 1) | Not supported |
| H2 | 15 of 17 in Cluster 1 lie in Asia, the Middle East, Africa or Russia; 16 of 20 in Cluster 2 in Europe or the Americas | Largely supported |
| H3 | Cluster 2 combines low insecurity with high turnover and turnaway; Cluster 1 the reverse | Supported |
| H4 | Overload, work-home conflict, exhaustion, turnover and turnaway rise together; satisfaction rises with them, not against them | Partly supported |

Table: Verdicts on the hypotheses

The partial result for H4 is worth a comment. Within a country, satisfied workers are usually less exhausted. Across countries, however, satisfaction rises with strain and exit intentions. This is consistent with mobile markets, where workers choose jobs they like but work hard and leave readily. It may also reflect known differences in how people answer surveys across cultures: respondents in East Asia tend to avoid the top of rating scales, which lowers reported satisfaction in Cluster 1.

# Recommendations

**1. Classify countries for ICT labour policy by these two groups, not by income level.** The two clusters are the same whichever score, method or subset of countries is used, and they cut across the IMF's split between advanced and emerging economies. Japan and Ghana share a profile, and so do the USA and Peru. Peer comparisons and policy advice on the ICT workforce should therefore be organised by cluster.

**2. In the strained-but-mobile cluster, address exhaustion and exit from the profession.** These countries combine the highest overload, work-home conflict and exhaustion with the highest turnaway intention, and turnaway separates the clusters more than any other issue. The risk is a loss of ICT skills to other sectors or abroad, especially for the Central and Eastern European and Latin American hubs. Policy should focus on working-time regulation, flexible and remote work, and tracking how many workers leave the sector.

**3. In the insecure-but-committed cluster, address job insecurity.** Workers here stay, but they feel insecure and less satisfied, which can hold back risk-taking and innovation. Unemployment insurance, portable benefits, publicly supported reskilling and policies that bring more tech employers into the country would lower insecurity without making workers leave the profession.

**4. Monitor the two watch lists and the boundary countries.** Iran, Japan and South Korea stand out for high insecurity alongside strong self-efficacy and social networks. Bangladesh, Malaysia, Nigeria and Pakistan report unusually low strain, which may be real or may reflect small samples and response styles. Russia, Poland and Canada sit near the boundary and could change group as their economies change.

**5. Strengthen the data.** Country samples range from 93 to 634 workers, and nine of the original 46 countries are missing. Larger and more even samples, repeated over time, would allow the IMF to see whether countries move between clusters as their ICT sectors mature.

**Limitations.** The analysis uses country averages, so it describes countries, not individual workers. With 37 countries, clusters of three or four countries rest on very few observations. The ANOVA p-values are inflated because the clusters were built from the same scores. The interpretation relies on general economic knowledge rather than on additional country data, and survey answers may not be fully comparable across cultures.

# References

```{=latex}
\begingroup\small\setlength{\parskip}{0.25em}
```

[1] Bakker, A. B. and Demerouti, E. (2007). The job demands-resources model: State of the art. *Journal of Managerial Psychology*, 22(3), 309–328.

[2] Hofstede, G. (2001). *Culture's Consequences* (2nd ed.). Thousand Oaks, CA: Sage.

[3] Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. *Journal of the American Statistical Association*, 58(301), 236–244.

[4] MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the 5th Berkeley Symposium on Mathematical Statistics and Probability*, 1, 281–297.

[5] Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53–65.

[6] Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

[7] McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61.

[8] Hubert, L. and Arabie, P. (1985). Comparing partitions. *Journal of Classification*, 2(1), 193–218.

```{=latex}
\endgroup
```
