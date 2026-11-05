# EPISTEME-P77 W34 — Real BLADE Fishing Data, Scientific Estimand Alignment, and a Strong Deterministic Baseline

**Date:** 2026-11-05 KST. **Binding:** [P77 current charter](../STRATEGY_P77_CURRENT.md) and [governance](../GOVERNANCE.md). **Status:** P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novelty not certified.
**Previous:** [W32 version-sensitive benchmark court](p77_w32_20261105_bixbench_v15_revision_and_grader_schema_court.md) and [W33 real expert annotation grain](p77_w33_20261105_blade_expert_annotation_grain_and_scientific_task_preflight.md).

## 1. Original source acquired and executed, with precise evidence boundary

We selected a **small actual BLADE scientific dataset** rather than requiring the user to download BixBench's 5.91GB capsules. Sources were fetched through the installed GitHub connector at original commit `6118fa8d5007b91aa8c91c518182db82446a4547`:
- [fish/data.csv](https://github.com/behavioral-data/BLADE/blob/6118fa8d5007b91aa8c91c518182db82446a4547/blade_bench/datasets/fish/data.csv), blob `a590e5b1a92029adc2db4915e48295ed60833430`. **All 250 rows were actually parsed and aggregations executed in the connected JavaScript runtime.**
- [fish/info.json](https://github.com/behavioral-data/BLADE/blob/6118fa8d5007b91aa8c91c518182db82446a4547/blade_bench/datasets/fish/info.json), blob `d3db2dde4439638dc08aa31a7fa8ec2d2a3f02e3`. Metadata says each row is a **group visit**; `persons` are **adults**, `child` are children, and `hours` are **hours spent in the park**, not independently measured *actual fishing hours*.
- [fish/annotations.csv](https://github.com/behavioral-data/BLADE/blob/6118fa8d5007b91aa8c91c518182db82446a4547/blade_bench/datasets/fish/annotations.csv), blob `4e903985f7ceef01d3ebb9f4453a5cd13d55d0c7`. Actual source expert graph, 65 specification records (6 conceptual, 13 transformations, 10 model, 4 conceptual annotation, 31 transform annotation, 1 dependency graph), not 65 independent test results.

No individual original data rows were republished to this public repository or the separate receipt. The author's BLADE repo mentions ODC attribution for data, but per-file rights should still be verified before rehosting original records. **Original full data were processed through connector JavaScript**, while the separate standalone Python auditors were only **self-tested with synthetic inputs locally**. Do not state those Python source auditors were separately run against the exact upstream 250-row file.

## 2. A real source-derived estimand discrepancy, not a new theory

Actual counts: **250 complete group-visit records**, six numeric columns; total caught fish **824**, total park-group-hours **1381.495**, total park-person-hours (adults + children multiplied by park-visit duration) **3258.2**; **142 visits with zero catch**, zero visits with duration zero, 34 visits with duration under 0.1 park-hour.

| Distinct measurable target on same authentic records | Direct calculation |
|---|---:|
| All fish / all group park-hours, `sum(fish)/sum(hours)` | **0.5964552893785353** |
| Average of individual visit park-hour rates, `mean(fish/hours)` | **1.1073814569241494** |
| All fish / all person-park-hours, `sum(fish)/sum(hours*(persons+child))` | **0.2529003744398747** |
| Average of individual visit person-park-hour rates | **0.3042787803287378** |

These are four **different descriptive estimands**, not four numerical representations of the same estimand. In particular, **the denominator is park time**, and this dataset alone cannot justify literal fish-per-**fishing**-hour estimates. People need not fish through their entire park visit.

Visit-level resampling (3000 IID-visit-with-replacement draws using explicitly seeded 32-bit LCG, `seed=20261105`, executed in connector JS) gave exploratory percentile intervals pooled-rate 0.378–0.890, mean-visit-rate 0.650–1.721, and paired difference 0.087–1.078. **These are not validated coverage CIs for a real sampling frame**, because visit IID/external validity assumptions were not independently verified. This is a sensitivity calculation, NOT an AI effect. The independently published Python replay code uses a **different seeded random generator**, so it should not be expected to give bit-identical bootstrap limits; compare methods and point estimates, not bit strings.

## 3. Strong non-AI scientific checking, including falsification of naive count-likelihood

An intercept-only Poisson **exposure-offset model** `Y_i ~ Poisson(lambda * hours_i)` has MLE `lambda=sum(Y_i)/sum(hours_i)` under independent equal-rate Poisson assumptions. Running its **actual source-row diagnostic** produces Pearson chi-square/(250-1) = **31.583022820268265**, observed zero catches **142**, model-expected zero catches **105.97174972494899**. Strong overdispersion and zero mismatch warn that naive constant-rate Poisson error bars and standard inference are indefensible; they do **not** prove a specific zero-inflated generating process or causal fishing effect.

Duration-threshold sensitivity, source counts and rates:
- All 250 rows: pooled 0.596455, mean-visit 1.107381.
- Exclude park-hours below 0.01: 245 records; pooled 0.596469, mean-visit 1.129981.
- Below 0.1: 216 records; pooled 0.597111, mean-visit 1.281692.
- Below 0.5: 173 records; pooled 0.583622, mean-visit 1.096902.
- Below 1: 148 records; pooled 0.570554, mean-visit 1.044733.

**Outcome:** a defensible future benchmark **must fix** the visit versus exposure-weighted estimand, grouping, units, observation duration and model assumptions before comparing any AI versus original analysis.

## 4. Source-linked strong prior art and what *cannot* be claimed

The original BLADE expert annotations already include `fish_per_hour`, `group_size`, `fish_per_hour_person`, linear regression on rates, and Poisson regression on counts. One original Poisson regression formula uses `fish_caught ~ livebait + camper + persons + child + hours` with hours as a **predictor**, rather than an explicitly specified `offset=log(hours)` — different statistical rate assumption. These are original author **candidate analyst choices**, not automatically a universally correct inference oracle.

[Engzell 2023 original PDF](https://drive.google.com/file/d/1VpL2sCk2gRSlKVlrGwzoTm5UWW-DgIxp/view) and [Auspurg–Brüderl 2024 original PDF](https://drive.google.com/file/d/1s95yC7Rkxp52GK1BpiQzdL_00a4FWlFE/view) have already explained the scientific hazards of different estimands and invalid measurement conversions. MQR and existing statistical rate/offset and provenance literature are direct conventional competitors. An actual discrepancy between four source-valid *targets* does not constitute an independently novel EPISTEME TLP mechanism.

[Python replay auditor](../analysis/p77_w34_fish_source_estimand_audit.py) uses an original Git **blob SHA-1** source seal and fails closed on wrong bytes. Its small synthetic selftest was run successfully; real source calculations were executed independently in connector JS, not by local Python. [Aggregate source receipts preserved in actual EPISTEME Drive](https://drive.google.com/file/d/1pUb4n89xQ-CiOaouQhyBCdOQrautwB60/view) once upload confirmed.

## 5. Disposition

Technical real-source pilot: **PASS** for original author data contact, estimand unit/audit and deterministic comparator diagnostics. **FAIL** for naive constant-rate Poisson inference; **NO-GO** for assigning the difference to AI, suppressing valid H0/H1 or community standard retention. No randomized AI adapter Z, no collective adoption A, no independently measured T feasible-test outcome. Existing source-based analysis and metascience theories explain these distinctions.

**Next W35:** test if two superficially different original expert transform expressions are mathematically the same, to avoid counting code-style variation as meaningful scientific diversity. **P77 ACTIVE / P78 HOLD / PAPER HOLD.**
