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

The International Monetary Fund (IMF) has asked us to find out how countries can be grouped by the issues that their information and communications technology (ICT) workers face, and to show that the grouping makes sense from a macroeconomic point of view. The data we are given covers 37 countries and 9 issues.

- dependence on friendship circles (FC)
- job insecurity (JI)
- self-efficacy (SE)
- work satisfaction (WS)
- work overload (WO)
- work-home conflict (WH)
- work exhaustion (WE)
- turnover intention (TI, employer attrition)
- turnaway intention (TA, attrition from the ICT profession altogether). 

Each of the issues mentioned above comes with two scores: a factor score, and a sum score. The IMF has asked that the grouping be done with both and the results compared.

Thus, we set out to answer three questions. How many natural groups of countries can be formed, and which countries belong to each of said groups? Do the factor scores and the sum scores lead to the same groups, and what do the groups have in common economically, so that the IMF can use them in its policy work?

The data is a set of national averages built from 93 to 634 ICT workers per country. Our groups therefore describe countries rather than individual workers, and the interpretation works off economic reasoning rather than on any additional country data.

**Our recommendations, briefly:**

1. Use a two-group classification of countries for ICT labour policy, and not the usual split between advanced and emerging economies which these groups cut across.
2. In the "strained but mobile" group (that includes mostly Europe and the Americas), treat exhaustion and exit from the ICT profession as the main risk, focusing on workload and working-time related policy.
3. In the "insecure but committed" group (that includes mostly Asia, the Middle East and Africa), treat job insecurity as the chief risk, focusing on safety nets, reskilling and deeper tech job markets.
4. Keep two small watchlists: one being Iran, Japan and South Korea, and the other being Bangladesh, Malaysia, Nigeria and Pakistan, whose position depends on which score is used.

# Data preprocessing

The file has one sheet with 37 rows and 21 columns: the country, a country code, the number of respondents and the two scores for each of the nine issues. We checked it in Python with pandas [7]: there are no missing values, no text in numeric columns and no duplicated countries or codes; the codes run from 1 to 46 with nine gaps, so the IMF has kept 37 of the 46 countries in the original study.

The factor scores (FS) are already standardised, with a mean close to zero for every issue. The sum scores (S) are on a different scale for each issue, because each issue is measured with a different number of questionnaire items (friendship circles average 5.8 and work satisfaction 13.4). Any distance-based clustering would let the issues with relatively larger scales dominate, so we standardised every sum score to a mean of 0 and a standard deviation of 1 before clustering them. The two scores agree closely for each issue, with correlations between 0.93 (work satisfaction) and 0.998 (friendship circles) so any difference in the groups will come from the details and not from a different perspective of the countries.

Ten values lie more than 2.5 SDs from the mean, where Iran scores very high on job insecurity as well as self-efficacy in both scores, and Nigeria very low on work overload, work-home conflict and exhaustion, but only in the sum scores. These are not data-entry errors, so we kept them. Because a few extreme countries can pull cluster centres around we re-ran the clustering without Iran and Nigeria as a check.

| Country | Issue | Score | z |
|:-----------|:----------------------|:------------------|------:|
| India | Job insecurity | Factor score | $-2.54$ |
| Iran | Job insecurity | Factor and sum score | $2.66$, $2.67$ |
| Iran | Self-efficacy | Factor and sum score | $3.36$, $3.35$ |
| Italy | Turnover intention | Factor score | $2.56$ |
| Nigeria | Work overload, work-home conflict, exhaustion | Sum score | $-2.75$ to $-3.13$ |
| Pakistan | Work-home conflict | Factor score | $-2.61$ |

Table: Values more than 2.5 standard deviations from the mean (these are still kept in the data)

The number of respondents varies from 93 in Nigeria to 634 in Thailand. We did not weight countries by it since the IMF's question is about countries, but averages from small samples aren't as precise, which particularly matters for Nigeria.

# Data visualization

The issues form two blocks: one constituted by work overload, work-home conflict, exhaustion, satisfaction, turnover and turnaway, that all rise together across countries, with work-home conflict and exhaustion being the most closely linked (correlation 0.84, as seen in Figure 1a). Job insecurity and self-efficacy are the constituents of the second block; that is countries where ICT workers feel insecure but also report high self-efficacy (0.73) with a much lower intention to leave the profession altogether ($-0.72$). Friendship circles sit largely on their own. A single principal component captures 54% of the variation in the nine factor scores, an implication that countries split along one main dimension.

**Countries line up along that dimension.** When the countries are ordered by this first component (Figure 1b), the top of the heatmap is dominated by East and South Asian, Middle Eastern and African countries with high insecurity and self-efficacy, the bottom by European and American countries with high strain and exit intentions. The change is gradual for most issues, which means the clustering has to decide the boundary.

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

We frame the issues with the job demands-resources model [1]. Demands such as work overload, work-home conflict and job insecurity wear workers down and lead to exhaustion, and exhaustion leads to withdrawal, first from the employer (turnover) and then from the profession (turnaway). Resources such as friendship circles, self-efficacy and satisfaction help buffer this process. At the level of countries, demands, resources and the realistic options for leaving all depend on the economy and the labour market leaving four hypotheses:

| | Hypothesis |
|:-----|:---------------------------------------------------------------------------------|
| H1 | The groups follow the IMF's split between advanced and emerging or developing economies |
| H2 | The groups follow culture and region, separating more collectivist from more individualist societies |
| H3 | Where ICT labour markets are deep and skills are portable, workers feel less insecure but are more willing to leave their employer and the profession |
| H4 | Demands, strain and withdrawal move together, as the job demands-resources model predicts |

Table: Hypotheses

# Analysis

**Method.** We grouped the countries with the two standard methods for this kind of data, using Euclidean distance on the 9 standardised issues. Ward's hierarchical clustering [3] starts with each country on its own and merges at each step the two groups whose merger adds least to the spread within groups. k-means [4] places $k$ cluster centres and moves them until each country sits with its nearest centre. We use 200 random starts and a fixed seed. Both methods were run on the factor scores and on the standardised sum scores, using scikit-learn [6].

**Choosing the number of clusters.** We used the elbow method and the average silhouette [5]. The elbow method plots the within-cluster sum of squares against $k$ and looks for the point where adding a cluster stops adding value. The silhouette measures, for each country, how much closer it is to its own cluster than to the next one, from $-1$ to $1$. Both point the same way for both scores (Table 3, Figure 2). Going from one to two clusters removes 42% of the within-cluster variation for the factor scores and 38% for the sum scores; every later step removes less than 20%. The average silhouette is highest at $k = 2$ (0.35 and 0.32), only slightly lower at $k = 3$, and falls sharply at $k = 4$. The Calinski-Harabasz index also peaks at $k = 2$. We therefore take two clusters as the main solution and examine three as a refinement.

| | Factor scores | | | | Sum scores | | | |
|:--|------:|------:|------:|------:|------:|------:|------:|------:|
| k | WSS | Drop | Silhouette | CH | WSS | Drop | Silhouette | CH |
| 2 | 18.83 | 41.8% | 0.345 | 25.1 | 199.99 | 38.3% | 0.318 | 21.7 |
| 3 | 15.69 | 16.7% | 0.320 | 18.1 | 161.74 | 19.1% | 0.298 | 17.1 |
| 4 | 13.73 | 12.5% | 0.195 | 14.9 | 139.92 | 13.5% | 0.197 | 14.5 |
| 5 | 12.17 | 11.3% | 0.171 | 13.3 | 118.51 | 15.3% | 0.223 | 13.9 |

Table: Choosing the number of clusters (WSS: within-cluster sum of squares; Drop: reduction from $k-1$; CH: Calinski-Harabasz index)

![Elbow plot (within-cluster sum of squares, solid) and average silhouette (dashed) for k-means on both scores.](output/figures/fig4_elbow_silhouette.png){width=88%}

**Ward and k-means agree.** The Ward dendrogram (Figure 3) has one dominant merge: two groups that join only at the very top, far above every other merge. Cutting it into two or three groups gives exactly the same memberships as k-means with both scores (adjusted Rand index 1.00, Table 4). The adjusted Rand index [8] compares two groupings, from ~0 for agreement no better than chance to 1 for identical groups. The two methods only part ways at $k = 4$ (0.65 and 0.55), another sign that four clusters forces splits that the data doesn't support.

![Ward hierarchical clustering of the factor scores. The dashed line cuts the tree into three groups.](output/figures/fig5_dendrogram.png){width=95%}

**Factor scores and sum scores give the same two groups, but not the same three.** With two clusters, the factor scores and the sum scores put every one of the 37 countries in the same group (adjusted Rand index 1.00). With three clusters they agree only partly (0.78), and seven countries move (Table 5). The large European and American group of 20 are identical either way. The difference is in which small group breaks away from the other countries. With the factor scores it is Iran, Japan and South Korea, which stand out on friendship circles, self-efficacy and job insecurity. With the sum scores it is Bangladesh, Malaysia, Nigeria and Pakistan, which stand out on very low overload, work-home conflict and exhaustion. Section 6 explains why the scores behave differently.

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

**The two-cluster solution is stable.** The results remain the same even after removing Iran and Nigeria. The remaining 35 countries are assigned to exactly the same two clusters using both factor scores and sum scores, with an adjusted Rand index of 1.00. The three-cluster solution is less consistent, with values of 0.72 for factor scores and 0.52 for sum scores. This difference seems to be mainly due to the smaller groups being influenced by countries with particularly extreme scores.

The silhouette scores also give an idea of how well each country fits into its assigned cluster. Russia is almost equally positioned between the two groups, with a silhouette score of -0.01. Poland (0.15) and Canada (0.18) are also relatively close to the boundary. Most of the remaining countries have higher silhouette scores, suggesting that they fit their assigned clusters more clearly.

**Do the clusters differ, and on which issues?** To examine the differences between the clusters, we used a one-way ANOVA for each of the nine issues (Table 9). We also checked the assumptions required for this test. The Shapiro-Wilk test was used to examine whether the scores were approximately normally distributed within each cluster, while Levene's test checked whether the variation in scores was similar across the groups.

For the two-cluster solution using factor scores, only job insecurity failed the Shapiro-Wilk test, while work overload failed Levene's test at the 5% significance level. With sum scores, two Shapiro-Wilk tests were significant, while none of the Levene tests showed a significant result. Since the number of countries in each cluster is relatively small, we also repeated the comparisons using the Kruskal-Wallis test, which does not require the same assumptions as ANOVA. The results were consistent across both tests for every issue, using both scoring methods and both cluster solutions.

One point worth considering is that the clusters were created using the same scores that were later compared. Therefore, some differences between the groups are expected, and the p-values may overstate the strength of the evidence. We also considered eta squared, which measures how much of the variation in each issue can be explained by cluster membership. This helps identify which issues contribute most to the differences between the groups. For the three-cluster solutions, Tukey's test was used to identify the specific pairs of clusters that differ (Table 6).

{{float:tukey_k3_wide|Tukey HSD p-values for each pair of clusters in the three-cluster solutions (* p < 0.10, ** p < 0.05, *** p < 0.01)}}

# Results

**Descriptive statistics.** Table 7 presents the descriptive statistics for both factor scores and sum scores across all nine issues. The factor scores are centred around zero, which is expected given how they are calculated. The sum scores have different scales across the issues, making standardisation necessary before comparing them. Self-efficacy has the highest skewness, at 1.1 for both scoring methods. This is largely influenced by Iran, which has an unusually high score on this issue.

{{float:descriptives|Descriptive statistics of the 37 country averages (S on its original scale; kurtosis is excess kurtosis)}}

**Two groups of countries.** The two-cluster solution divides the 37 countries into two groups of 17 and 20 countries respectively (Table 8). The same grouping is obtained using factor scores and sum scores, as well as with Ward's method and k-means clustering. This consistency makes the two-cluster solution a useful basis for interpreting the results.

The profiles of the two groups are quite different, as shown in Figure 4. Eight of the nine issues show statistically significant differences between the clusters using both scoring methods. Friendship circles are the only issue where the difference is not significant. The largest differences appear in work satisfaction, turnaway intention and job insecurity. For each of these issues, cluster membership explains more than half of the variation in scores.

Figure 5 shows the two groups using the first two principal components. Most countries appear on opposite sides of the vertical axis, although a few are positioned closer to the boundary between the clusters.

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

Table: Cluster means and one-way ANOVA for the two-cluster solution (KW: Kruskal-Wallis; *** p < 0.01)

![The two clusters on the first two principal components, with the countries that split off at k = 3 marked.](output/figures/fig7_cluster_map.png){width=80%}

**Cluster 1: Insecure but committed.** This cluster contains 17 countries. On average, ICT workers in these countries report greater job insecurity and lower work satisfaction. At the same time, they tend to have higher confidence in their own abilities and report less work overload, less conflict between work and home, and lower exhaustion. They are also less likely to consider leaving their current employer or moving out of the ICT profession.

Fifteen of the 17 countries are located in East, Southeast or South Asia, the Middle East, Africa or Russia. A few economic and social factors could help explain this pattern.

First, ICT jobs in many of these economies offer relatively high salaries and social status compared with other professions. Leaving the sector could therefore involve a considerable financial or professional loss. This may help explain why workers are less likely to consider leaving, even when they feel uncertain about their job security.

Second, the technology job markets in some of these countries may offer fewer employers and less movement between companies. Finding another job after losing the current one could be difficult, which may contribute to higher job insecurity. Workers may consequently prefer to remain in their existing positions despite these concerns.

Cultural factors could also be relevant. Many of these countries are generally considered more collectivist [2], where loyalty to an organisation and long-term employment relationships may carry greater importance. This is particularly relevant when considering Japan, South Korea and Taiwan. Family and social networks may also help workers manage responsibilities outside the workplace, potentially contributing to the lower levels of reported work-home conflict. The higher self-efficacy scores could also be related to the relatively selective nature and professional status of ICT jobs in some of these countries.

**Cluster 2: Strained but mobile.** The second cluster contains 20 countries. Workers in these countries generally report lower job insecurity and higher work satisfaction. However, they also report more work overload, greater conflict between work and home, and higher levels of exhaustion. Their intentions to leave their current employer or move out of the ICT profession are also higher.

Sixteen of these 20 countries are located in Europe or the Americas. One possible explanation is the structure of their ICT labour markets. Many of these countries have relatively open technology sectors, where workers can move between employers more easily. As a result, losing a job may be less concerning because alternative opportunities are more accessible. This could explain why job insecurity is lower, while intentions to change employers or leave the profession are higher.

The Central and Eastern European countries in this group, including Hungary, Lithuania, Macedonia, Poland and Romania, are also connected to the wider European labour market. Moving abroad for better employment opportunities may be a realistic option for ICT workers in these countries. A similar situation may apply to Mexico, Peru, Brazil and Argentina because of their links with the North American technology market.

India is also part of this cluster. Its large IT outsourcing industry has experienced relatively high employee attrition, which is consistent with the higher turnover and turnaway intentions observed in this group.

Cultural differences may also contribute to these patterns. Countries with more individualistic cultures can have different expectations regarding work, personal responsibilities and work-life balance. These differences may influence how workers experience and report conflicts between work and home.

**Countries at the edges.** Some countries do not fit entirely into the general patterns of either cluster. Canada and France, for example, are both advanced Western economies but are included in Cluster 1. France's employment protection policies and relatively shorter legal working week may help explain its lower work overload and turnover scores. Canada, on the other hand, has a silhouette score of 0.18, which suggests that its position within Cluster 1 is not particularly clear.

Russia is even closer to the boundary between the two groups, with a silhouette score of -0.01. This means that it could reasonably be associated with either cluster, so its classification should be treated with caution.

**The three-cluster results depend on the scoring method.** When factor scores are used, Iran, Japan and South Korea form a separate third group. These countries have particularly high scores for self-efficacy, friendship circles and job insecurity (Figure 4, right). Japan and South Korea share relatively strong company-based social networks, alongside demanding workplace conditions. Iran may show a similar pattern for different reasons, including the economic uncertainty associated with international sanctions and the professional networks within its educated ICT workforce.

The results are different when sum scores are used. In this case, Bangladesh, Malaysia, Nigeria and Pakistan form the third group. These countries are mainly characterised by unusually low scores for work overload, work-home conflict and exhaustion, at approximately 1.7 standard deviations below the average.

This difference is related to how the two scoring methods work. Sum scores combine the raw responses across all items, meaning that particularly high or low answers can have a larger influence on the final score. Factor scores assign different weights to items depending on how well they measure the underlying issue. They also reduce some item-specific variation, which can make extreme scores less influential.

Nigeria's unusually low strain scores appear mainly when using sum scores. It is also important to consider that Nigeria has the smallest sample, with only 93 workers. For this reason, factor scores appear to provide a more reliable basis for interpreting the three-cluster results.

Overall, the three-cluster solutions are less consistent, particularly when countries with extreme scores are removed. We therefore consider these smaller groups as countries that may deserve further attention rather than treating them as clearly established clusters.

**Hypotheses.** Table 10 summarises the findings for the four hypotheses.

| | Result | Finding |
|:-----|:--------------------------------------------------------------|:----------------|
| H1 | Advanced economies fall in both clusters (about 9 of 20 in Cluster 2 and 5 of 17 in Cluster 1) | Not supported |
| H2 | 15 of 17 in Cluster 1 lie in Asia, the Middle East, Africa or Russia; 16 of 20 in Cluster 2 in Europe or the Americas | Largely supported |
| H3 | Cluster 2 combines low insecurity with high turnover and turnaway; Cluster 1 the reverse | Supported |
| H4 | Overload, work-home conflict, exhaustion, turnover and turnaway rise together; satisfaction rises with them, not against them | Partly supported |

Table: Verdicts on the hypotheses

The results for H4 are worth discussing further. At the individual level, workers who are more satisfied with their jobs are generally less exhausted. However, the country-level results show that satisfaction increases alongside work-related strain and intentions to leave.

One possible explanation is that workers in more developed and mobile labour markets have access to jobs that they find satisfying, even if those jobs involve longer working hours and greater pressure. They may also have more opportunities to move to another employer or leave the profession altogether.

Differences in survey response styles could also influence these findings. Previous research suggests that respondents in East Asian countries may be less likely to choose the highest points on rating scales. This could partly explain the lower satisfaction scores observed in Cluster 1.

# Recommendations

**1. Use the two country groups when comparing ICT labour markets.** The results suggest that grouping countries according to the characteristics of their ICT workforce could be more useful than relying only on income classifications. The two clusters remain the same across both scoring methods and clustering techniques, and they include countries from different economic categories.

For example, Japan and Ghana fall into the same group, while the USA and Peru are also grouped together. This shows that countries with different economic backgrounds can still have similar patterns in job security, satisfaction and turnover intentions. Future comparisons and policy discussions could take these similarities into account.

**2. Focus on exhaustion and employee retention in the strained-but-mobile group.** Countries in Cluster 2 report higher levels of work overload, work-home conflict and exhaustion, along with stronger intentions to leave the ICT profession. Turnaway intention also shows one of the largest differences between the two clusters.

This could become a concern for countries that depend heavily on their ICT workforce, particularly those in Central and Eastern Europe and Latin America. Policies encouraging reasonable working hours, flexible arrangements and remote work could help address some of these issues. It would also be useful to monitor how many ICT workers leave the profession over time, rather than focusing only on employee turnover within individual companies.

**3. Give more attention to job insecurity in the insecure-but-committed group.** Workers in Cluster 1 appear less likely to leave their employers or the ICT profession, but they report higher job insecurity and lower work satisfaction. Over time, this could affect their willingness to take risks, develop new ideas or invest in their professional growth.

Possible policy measures include improving unemployment protection, making benefits more portable between employers, supporting reskilling programmes and encouraging more technology companies to establish operations in these countries. These measures could help provide workers with greater security while improving their opportunities within the ICT sector.

**4. Keep track of the smaller groups and countries near the cluster boundaries.** The three-cluster results identify a few countries with unusual patterns. Iran, Japan and South Korea stand out because of their combination of high job insecurity, self-efficacy and friendship circles. Bangladesh, Malaysia, Nigeria and Pakistan report particularly low levels of work-related strain.

These patterns may reflect genuine differences, but they could also be influenced by sample sizes or cultural differences in survey responses. Russia, Poland and Canada are also worth monitoring because their positions are relatively close to the boundary between the two main clusters.

**5. Improve the data used for future analysis.** The current analysis covers 37 countries, with sample sizes ranging from 93 to 634 workers. Nine of the original 46 countries are not in the file we received.

Future research would benefit from larger and more balanced samples across countries. Repeating the survey over several years would also help show whether countries move between clusters as their ICT industries develop. This would make it easier to understand whether the patterns identified in this analysis remain consistent over time.

**Limitations.** There are several limitations that should be considered when interpreting these findings.

First, the analysis is based on country averages. Therefore, it describes differences between countries rather than differences between individual workers. Workers within the same country may have very different experiences that are not reflected in the average scores.

Second, the analysis includes only 37 countries. The smaller groups in the three-cluster solutions contain just three or four countries, so their results should be interpreted carefully.

Another limitation concerns the statistical tests. Since the same scores were used to create the clusters and then compare them, the ANOVA p-values may overstate the strength of the differences. Although the Kruskal-Wallis tests produced similar results, this issue still needs to be considered.

The explanations provided for the differences between clusters are also based mainly on general knowledge about national economies and labour markets. Additional country-level data would be needed to examine whether factors such as employment protection, labour market mobility and cultural differences actually explain the observed patterns.

Finally, survey responses may not be directly comparable across cultures. People in different countries may interpret questions or use rating scales differently, which could influence the country averages and, in turn, the clustering results.

# References

```{=latex}
\begingroup\small\setlength{\parskip}{0.25em}
```

[1] Bakker, A. B. and Demerouti, E. (2007). The job demands-resources model: State of the art. *Journal of Managerial Psychology*, 22(3), 309-328.

[2] Hofstede, G. (2001). *Culture's Consequences* (2nd ed.). Thousand Oaks, CA: Sage.

[3] Ward, J. H. (1963). Hierarchical grouping to optimize an objective function. *Journal of the American Statistical Association*, 58(301), 236-244.

[4] MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the 5th Berkeley Symposium on Mathematical Statistics and Probability*, 1, 281-297.

[5] Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65.

[6] Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.

[7] McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61.

[8] Hubert, L. and Arabie, P. (1985). Comparing partitions. *Journal of Classification*, 2(1), 193-218.

```{=latex}
\endgroup
```
