# EPISTEME-P77 W25 — Fatal Rival Court: Significance, Magnitude, Measurement and AI-Translation Causality

**Date:** 2026-11-05 KST
**Mandate:** [P77 director strategy](../STRATEGY_P77_CURRENT.md). **Status:** P77 ACTIVE, P78 HOLD, PAPER HOLD; no independently novel EPISTEME explanation certified.
**Source evidence:** [W24 correction-first source replication](p77_w24_20261105_corrected_fig1_reproduction_and_estimand_court.md) · [W23 authentic ZIP custody](p77_w23_20261105_original_cri_archive_unsealed_data_grain_and_custody.md).

## 1. New original-code audit: magnitude normalization is not evidence of changed 95% CI classification

The user's actual ZIP includes `code/data_prep/002_CRI_Data_Prep.Rmd`. This source clearly states that 1% immigration *flow* change and 1% immigrant *stock* share differ; its `standardizeDV` chunk scales *flow* AME and confidence endpoints by the ratio of stock/flow standard deviation computed from pooled submissions; it also applies documented manual `/10` scale corrections to original `t104m2` and `t104m4`. It is a **published author's own implementation and limitations**, not an EPISTEME new invention.

We independently read the original `cri_str.csv` with cp1252 and compared, for **all 1,252 model records with both raw and standardized interval bounds**, the sign/zero-exclusion categories under the raw `(AME, lower, upper)` versus standardized `(AME_Z, lower_Z, upper_Z)` pairs. **Exactly 0 out of 1,252 changed categories**; group counts 244 significant negative / 806 includes zero / 202 significant positive. This is an actual **negative control against attributing the three-category evidence variation to this particular positive-rescaling step**.

[Executable standalone validation](../analysis/p77_w25_cri_raw_vs_standardized_ci_null_control.py) committed; the same comparison was executed independently on actual original CSV in local Python/Pandas, with 1,252 agreement. A category-only result does **not** mean the standardized magnitude, unit, measurement interpretation or target estimand is unchanged; the latter require domain-relevant reading. No AI converter was involved.

## 2. Published strongest direct rivals: must review this entire debate, not just Breznau 2022 headline

A. **Mathur, Covington & VanderWeele (2023)**, *Variation across analysts in statistical significance, yet consistently small effect sizes*, PNAS 120(3):e2218957120, DOI [10.1073/pnas.2218957120](https://doi.org/10.1073/pnas.2218957120), [official open text](https://pmc.ncbi.nlm.nih.gov/articles/PMC9933094/). Their critique: headline 25%/58%/17% significance categories do not establish large **substantive effect-size heterogeneity**. Original-data reanalysis W24 **independently counted 1,126/1,253 = 89.864%** of standardized point estimates within ±0.037, agreeing with their ~90% observation. Their further random-effects/meta-analytic argument about underlying effects lying within ±0.014 in 90% of cases is **not independently replicated here**. Do not conflate statistical vs scientific/practical significance.

B. **Engzell (2023)**, *A Universe of Uncertainty Hiding in Plain Sight*, PNAS 120(2):e2218530120, DOI [10.1073/pnas.2218530120](https://doi.org/10.1073/pnas.2218530120), [full open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC9926231/). Argues that large variation also occurs **within a single earlier analyst study**, so within- and between-team variability and measurement/theory/causal inference matter. This challenges simplistic 'many teams discovered surprising unpredictability' readings, not the existence of analytical flexibility itself.

C. **Auspurg & Brüderl (2024)**, *Toward a More Credible Assessment of the Credibility of Science by Many-Analyst Studies*, PNAS 121(38):e2404035121, DOI [10.1073/pnas.2404035121](https://doi.org/10.1073/pnas.2404035121), [official open text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11420151/). Their THREE methodological gates: (1) prespecified **meta-estimand** and separate sources of variation; (2) participant/process/incentive comparability with standard scientific practice; (3) defensible meta-analysis rather than naive categorical/significance aggregation. Crucial point: marginal differences of P=.049 vs .051 or sign around zero are not automatically different scientific explanations. A separate AI translator intervention must also specify an **epistemic estimand** as opposed to significance ratio.

D. **Breznau et al. (2022)** underlying PNAS paper and the actual **June 20, 2024 Figure 1 correction** remain valid source of multi-analyst descriptive data. The official corrected Figure 1 contains **25.4%, 57.7%, 16.9%**, verified by PDF page-2 visual inspection and W24 reconstruction. But corrected caption `n=1253` counts nonmissing point estimates; published R code's CI-based significance grouping uses 1252 complete-CI records because `t75m14` lacks CI. Neither count licenses a causal interpretation of modern LLM conversion.

E. Existing EPISTEME prior rivals still binding: Farrell–Saloner/Arthur/Liu/Heinrich/Rosero standard-choice economics, Reijula–Blanco Sequeiros 2024/Blanco Sequeiros 2026 evidential discordance, Janssen 2026 scientific knowledge graphs/AI-workflow interoperation, Pritchard–Wicenec 2025 workflow reproducibility, MQR measurement/calibration. A new label for any one component is **not novelty**.

## 3. Chain decomposition and explicit failed identification

Let `Z` be a versioned, assigned AI converter; `A` be adoption of a common standard; `T` be the set of **independently justified, scientifically discriminating** admissible tests of a prespecified H0/H1 under equal resources. For identification of a translation-induced *scientific* consequence, one must distinguish

- `Z → A`: developer/market/coordination effects (the economic competitors already predict migration and lock-in).
- `Z → T` at fixed `A`: semantic fidelity, provenance and alternative methods (the workflow/provenance competitors already model these).
- `A → T` at fixed `Z`: social/institutional infrastructure dependence (historical science and measurement competitors already address it).
- the full mediated path `Z → A → T` with interference across researchers and **real observed tasks**.

The original 2022 CRI data have no allocated modern AI `Z`, no observed community standard response `A`, and no independently verified feasible-test-set `T`. Its three evidence-significance categories and AME values cannot recover an effect on the full causal chain, regardless of how accurately Fig.1 is reproduced.

**New challenge to theorist:** Even when a prospective AI converter changes output report, what is the falsifiable residual after a strong no-AI deterministic converter with the same data, provenance proof, budget, adoption conditions and expert validation? Without a specified difference in competitor predictions, no independent EPISTEME theory exists.

## 4. Outcome and bounded decision

**Passes:** actual corrected weighted Fig1 category reproduction; exact 1252 paired raw-vs-standardized CI category null; ~90% near-zero estimate check; three scholarly direct critiques source-grounded and directly applied. These are **methodological safeguards**, not new empirical AI intervention data.

**Fails/pending:** no raw original R model full replication; no AI-vs-classic converter paired study, measured laboratory standard adoption, independent scientiﬁc-test warrant or hypothesis-specific causal identification. This cannot be cured by repeatedly generating synthetic worlds or reading more rows from the same CRI table.

**W26 gate:** Verify that bundled raw upstream ISSP files match official original versions/rights if one wants full data regeneration; separately decide feasibility of an *authentic paired scientific-test conversion benchmark* with prespecified H0/H1 and equal-budget human/deterministic comparison. If the required assignment/adoption log does not exist, record the full founding chain as **NOT EMPIRICALLY IDENTIFIED** and do not manufacture it.

## 5. Original PDF debt only (original articles NOT verified held on user's Drive as of W25)

1. Mathur, Covington & VanderWeele (2023), *Variation across analysts in statistical significance, yet consistently small effect sizes*, PNAS 120(3):e2218957120, DOI [10.1073/pnas.2218957120](https://doi.org/10.1073/pnas.2218957120). Web full text verified; Drive PDF not found.
2. Per Engzell (2023), *A universe of uncertainty hiding in plain sight*, PNAS 120(2):e2218530120, DOI [10.1073/pnas.2218530120](https://doi.org/10.1073/pnas.2218530120). Web full text verified; Drive PDF not found.
3. Katrin Auspurg & Josef Brüderl (2024), *Toward a more credible assessment of the credibility of science by many-analyst studies*, PNAS 121(38):e2404035121, DOI [10.1073/pnas.2404035121](https://doi.org/10.1073/pnas.2404035121). Web full text verified; Drive PDF not found.

Not a source to re-request: original CRI 117MB ZIP, author result tables, PNAS 2024 Fig1 correction, Janssen 2026, Rosero 2026 — **already held**. Original GESIS upstream survey files physically present bundled, but independent version-rights authenticity NOT certified.
