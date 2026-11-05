# EPISTEME-P77 W29 — Authentic CRI Within/Between Analyst, Outcome and Immigration-Exposure Variance Decomposition

**Date:** 2026-11-05 KST. **Source authority:** [P77 mandate](../STRATEGY_P77_CURRENT.md), original [CRI-master.zip](https://drive.google.com/file/d/1qRL9_P6mV4nJaBMgxq3p60ShDa5p-NJY/view), source [W28 three original rival court](p77_w28_20261105_three_original_pnas_rivals_and_metric_translation_prior_art.md).
**Status:** descriptive source decomposition VERIFIED / causal attribution NOT POSSIBLE / P78 + PAPER HOLD.
**Reproducible code:** [analysis/p77_w29_cri_variance_hierarchy.py](../analysis/p77_w29_cri_variance_hierarchy.py).

## 1. Actually executed calculations from the genuine original CSV

The genuine CRI master ZIP remains in the container unmodified and CRC-audited, source `CRI-master/data/cri_str.csv`, cp1252 text, 1,309 total model records, including original baseline Team0. We exclude Team0 and rows with missing standardized point estimate `AME_Z`, leaving **1,253 model records / 71 distinct model-producing team IDs** (the submitted data originally had 72 team IDs including one with no numeric estimates; do not quietly conflate denominators).

Define `y_ij` as the *recorded standardized estimate* for model j contributed by team i, not the independently known true treatment effect. For a finite observational table with equal model-record weight, the mathematical identity is:

`Var_records(y) = Var_between_teams(weighted by team record counts) + E_records[Var(y|team)]`.

Direct independent Python/Pandas execution on that actual source produced:

| Component | Actual finite-record variance | Proportion |
|---|---:|---:|
| Total model-level `AME_Z` variance | 0.005410404127146502 | 100% |
| Variance between team means, weighted by their record counts | 0.0007358588099630939 | **13.6008%** |
| Variance within teams, weighted by their record counts | 0.004674545317183408 | **86.3992%** |

This **is not** the statistical intraclass correlation of a common random-effects distribution, does **not** remove sampling error, and does **not** show 86.4% "hidden epistemic uncertainty." Teams submitted different numbers of models (min 1, max 112). Equal-weighting **teams** instead of **models** changes the descriptive within-team fraction to **79.5103%** (different target population/aggregation).

## 2. Nested estimand-family decomposition: original materials reveal why 'within team' misleads

Original `cri_str.csv` has `dv_type` and `Stock` / `Flow` fields. The latter encode distinct immigration stock vs flow exposures, with 43 other records that cannot be silently forced into either category. For data-record-weighted orthogonal nested mean decomposition, grouping model outcomes by

`team → team × dv_type → team × dv_type × immigration_type → model`

yields:

| Descriptive layer | Share of total observed model variance |
|---|---:|
| Between team means | **13.6008%** |
| Between policy-support outcome classes within team | **19.9151%** |
| Between immigration stock/flow/other classes within same team/outcome | **51.1259%** |
| Remaining within identical recorded team/outcome/exposure class | **15.3582%** |
| TOTAL | **100.0000%** |

Actual source composition: **621 Stock / 589 Flow / 43 Other** model records, seven values of `dv_type`; **275 team×outcome groups, 532 team×outcome×exposure groups**, 46 of the 71 teams reported more than one outcome class. Every step sums to observed total variance to numerical rounding precision.

**Careful meaning:** Only 15.36% remains within this *coarse* grouping. However, this is **NOT** demonstrated "remaining research-choice error"; countries, time, covariates, models, inferential estimand, sample selection and measurement method can still differ. Conversely, the 51.13% exposure-class component is **not** a causal contribution of 'stock/flow' to the actual effect, because variation in other analyst choices is not randomized or equalized and groups have nonuniform representations. This is an **orthogonal descriptive projection on uneven observed categories**, not a valid ANOVA causal attribution. It directly supports Engzell/Auspurg's warning that the 2022 pooled work bundles different scientific questions.

## 3. Sensitivity and nonlinear weighting

The data contain two extreme original standardized entries: `t13m23 = +1.30` (housing outcome) and `t13m24 = +1.21` (health outcome). These are **original source table values**, not newly diagnosed conversion errors. The original Figure 1 code clips plot values near 0.75 for display, while source variance over un-clipped values is outlier-sensitive. Source-specified sensitivity tests:

| Analysis choice | Model records | Within-team share of observed variance (model weighted) |
|---|---:|---:|
| All original `AME_Z` nonmissing | 1,253 | **86.40%** |
| Remove `|AME_Z| > 0.75` (two records) | 1,251 | **88.27%** |
| Remove `|AME_Z| > 0.20` | 1,231 | **79.03%** |
| Winsorize `AME_Z` to ±0.10 (all records kept) | 1,253 | **82.43%** |

These arbitrary cutoffs are **sensitivity diagnostics**, not evidence-based rules for invalidating genuine observations. Model-weighting and team-weighting produce different descriptive estimands; observe rather than conceal that distinction.

Actual local Python execution completed exact 1,253/71 and 1,251/1,231 controls and the original two-level accounting identity; separate local Pandas execution also verified four-level proportions **13.6008, 19.9151, 51.1259, 15.3582**, including group sizes. GitHub code exposes both techniques for future rerun.

## 4. Interpretation under the now-held 2023/2024 source critiques

- [Engzell 2023 original](https://drive.google.com/file/d/1VpL2sCk2gRSlKVlrGwzoTm5UWW-DgIxp/view) predicts that same-hypothesis label can hide multiple combinations of immigration treatment/outcome, and that within-team model variation can be substantial. W29 is consistent with this **already articulated** concern, not novel EPISTEME evidence.
- [Auspurg & Brüderl 2024 original](https://drive.google.com/file/d/1s95yC7Rkxp52GK1BpiQzdL_00a4FWlFE/view) insists on a fixed meta-estimand and distinguishes productive heterogeneity across populations/estimands, research errors, and inability to choose a correct estimator. Raw category projections cannot distinguish those.
- [Mathur et al. 2023 original](https://drive.google.com/file/d/1_f5TrM-tonVpl9k7kDswgCHlQ23VBgrA/view) separately highlights that 90% of individual standardized effects are small; within-record variance need not imply large practically important effects or epistemic collapse. Its underlying-effect heterogeneity estimation is different from W29's simple descriptive decomposition.

None of the above estimates AI-conversion treatment or a scientific community's actual standard-retention choices, so neither the full TLP nor a new independent epistemological residual is established.

## 5. Next W30

Treat **absence of common estimand** as a serious source validity problem before claiming translation suppresses hypothesis tests; apply a **source-matched task contract** with known original H0/H1, outcome/exposure/site/time, reference inference, strong non-AI conversion and adoption/choice data. If no credible observed joint chain exists, record this as **IDENTIFICATION HOLD**, not an empirical TLP effect.

**No additional CRI ZIP or ISSP download needed for this check.** Official ISSP variant-rights custody still unresolved for external publication, not for derived-record internal analysis. **P77 ACTIVE, P78/PAPER HOLD.**
