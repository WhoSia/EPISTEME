# EPISTEME-P77 W24 — Actual Corrected PNAS Figure 1 Replication and Estimand/Denominator Court

**Date:** 2026-11-05 KST. **Authority:** [P77 mandate](../STRATEGY_P77_CURRENT.md). **Status:** source-table replication PASS; raw ISSP regression rerun NOT DONE; TLP novelty NOT CERTIFIED; P78/PAPER HOLD.  
**Raw-byte parent:** [User-supplied original CRI-master.zip](https://drive.google.com/file/d/1qRL9_P6mV4nJaBMgxq3p60ShDa5p-NJY/view), SHA256 `64756bfe62b25cdd7dbea57d2b063cb0f564225751d1f0251b4879f426894098`. **Historical audit:** [W23](p77_w23_20261105_original_cri_archive_unsealed_data_grain_and_custody.md).

## Executed independent numerical check

We read actual `CRI-master/data/cri_str.csv` (cp1252) and `CRI-master/data/cri.csv` and audited `CRI-master/code/03_CRI_Spec_Analysis.Rmd` source commands. The author script first filters `u_teamid != 0`, `AME_Z` and `lower_Z` missing values, adjusts near-zero lower/upper interval bounds, applies symmetric plot clipping/rounding, derives `sig_group2` using the sign and 95% CI crossing zero, and calculates **per-team inverse-model-count weighted** proportions. We implemented an independent Python read-only reconstruction, locally executed it successfully against the original byte-sealed ZIP, and checked all assertions.

| Cohort / inferential object | Observed |
|---|---:|
| All models including historical Team0 | 1,309 |
| CRI cohort model submissions excluding Team0 | 1,261 |
| AME_Z nonmissing | 1,253 |
| Both 95% CI bounds nonmissing and admitted by the plotting code | **1,252** |
| 95% CI significant negative | **244 rows** |
| 95% CI includes zero (nonsignificant) | **806 rows** |
| 95% CI significant positive | **202 rows** |
| Unweighted category percentages | **19.489% / 64.377% / 16.134%** |
| Inverse-team-model-count weighted category percentages | **25.4% / 57.7% / 16.9%** |
| Sum of retained team weights (original team contributions were 72 prior to missing-CI filtering) | **70.944444444444** |

The weighted percentages exactly reproduce both (i) the figure bundled in the 2022 original ZIP `results/Fig1.pdf` and (ii) the **actual rendered original [PNAS June 20, 2024 published Correction PDF](https://drive.google.com/file/d/1NSkJ1yxy8vZ4EUP6SwD5BQa3mbe5_G4z/view), page 2**. The correction explicitly says the old Figure 1 appeared incorrectly. Its corrected figure labels show **25.4, 57.7, 16.9** and caption `n=1,253` converged models. Yet publicly posted plotting code filters one more record missing CI, `t75m14`, after retaining its nonmissing AME. This is a **granularity/figure-code denominator caveat**; no allegation of fraud or retraction.

**Weight interpretation:** the 72 teams each contribute aggregate inverse-weight 1 before omission; the failed eight AME rows from team1 remove weight 1, and model `t75m14` missing CI removes weight 1/18. Of 72 originally model-submitting team IDs, only 71 have retained models with complete CI. **The 2022 headline participant teams (73) are a different count from model-sending team IDs.** Do not report weighted shares as independent team proportions or unweighted model proportions.

## Independent adversarial challenge from actual CRI data

Mathur, Covington & VanderWeele (2023), *Variation across analysts in statistical significance, yet consistently small effect sizes*, PNAS 120(3):e2218957120, DOI [10.1073/pnas.2218957120](https://doi.org/10.1073/pnas.2218957120), stress that 90% of standardized point estimates lie within ±0.037. Our direct source recheck found **1,126 of 1,253 = 89.864%** with `|AME_Z| <= 0.037` (including the one missing CI but valid point estimate). The difference between **three-color significance dispersion** and **small observed effect sizes** is real and cannot be suppressed when inferring epistemic disagreement. Mathur's `[-.014,.014]` meta-analysis range for **estimated underlying population effects** is a different model-based statistical inference, **NOT reproduced** by this descriptive recheck. Their paper is a direct **existing rival**, not our discovery.

The 2024 review by Auspurg & Brüderl, DOI [10.1073/pnas.2404035121](https://doi.org/10.1073/pnas.2404035121), additionally warns that many-analyst inference requires a prespecified **meta-estimand**, research incentive/process comparability and appropriate meta-analysis. Engzell (2023), DOI [10.1073/pnas.2218530120](https://doi.org/10.1073/pnas.2218530120), points to differences between within-team and between-team variation and to measurement, theory and causal inference as competing explanations. Do not present these scholars as unanimous against all many-analyst results; each diagnoses distinct interpretation hazards.

## Code/source reproducibility receipts

[Exact standalone GitHub Python audit](../analysis/p77_w24_original_fig1_weighted_replay.py) operates on the original ZIP without changing data or running R. The local source replay passed its exact 25.4/57.7/16.9 and 1,126/1,253 assertions. The archived original and official corrected PDF figures were separately **rendered and visually checked**, rather than relying on text extracted from the PDF. No newly sourced GESIS file or R 1,261-model regression rerun.

## EPISTEME founding-problem implications

Evidence that (1) significance decisions differ, (2) estimates are often small, or (3) data conversion can alter workflow reports **does not identify** the founding causal chain AI translation -> endogenous standard choice -> collective scientific hypothesis-test availability or admissibility. Basic statistics, conventional network economics, scientific measurement/validity and data provenance already explain much of this. This W24 positive result is a **faithful independent postprocessing replication** and a **negative epistemic caution**, not novel philosophy.

**W25 priority:** confront all three direct many-analyst critiques, hold original H0/H1 and unit of inference fixed, then decide where evidence stops; do not replace TLP with an endless CRI research agenda. **P77 ACTIVE / P78 HOLD / PAPER HOLD.**

## Missing source table at W24

The original PDF of three direct critic texts is **not verified held in Drive** although open official full text and DOI are available: Mathur/Covington/VanderWeele (2023) 10.1073/pnas.2218957120; Engzell (2023) 10.1073/pnas.2218530120; Auspurg/Brüderl (2024) 10.1073/pnas.2404035121. Separate GESIS version/terms and historic CERN signed 2000 minutes remain pending. **CRI original ZIP and PNAS 2024 correction are already held.**
