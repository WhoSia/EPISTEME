# EPISTEME-P77 W28 — Three Newly Acquired PNAS Originals, Direct Reading, and Fatal Translation/Pooled-Estimand Prior Art

**Date:** 2026-11-05 KST. **Strategy:** [P77 CURRENT](../STRATEGY_P77_CURRENT.md), [governance](../GOVERNANCE.md). **Research status:** P77 ACTIVE / P78 HOLD / PAPER HOLD / independent mechanism NOT CERTIFIED.
**Parent:** [W27 six-gate director review](p77_w27_20261105_founder_identity_six_gates_and_actual_data_entry_contract.md), actual original [CRI-master.zip](https://drive.google.com/file/d/1qRL9_P6mV4nJaBMgxq3p60ShDa5p-NJY/view), SHA256 64756bfe62b25cdd7dbea57d2b063cb0f564225751d1f0251b4879f426894098.

## 1. Actual Drive intake, bibliographic reading, and relocation: all 3 VERIFIED

The three PDFs were confirmed by *direct folder listing* of `RESEARCH_OS_LITERATURE/00_INTAKE` (unlike sometimes incomplete global search), then **actually fetched and original full extracted text read**, metadata-normalized and moved **using their original Google Drive file IDs** into canonical `RESEARCH_OS_LITERATURE/10_PAPERS`. All post-move IDs/parent/byte counts were independently read back.

| Work and exact type | Genuine Drive file | bytes, page count, DOI |
|---|---|---|
| Maya B. Mathur, Christian Covington & Tyler J. VanderWeele (2023), *Variation across analysts in statistical significance, yet consistently small effect sizes*, PNAS 120(3):e2218957120, **LETTER** | [actual source PDF](https://drive.google.com/file/d/1_f5TrM-tonVpl9k7kDswgCHlQ23VBgrA/view) | 118,179 B; 1 page; DOI 10.1073/pnas.2218957120 |
| Per Engzell (2023), *A universe of uncertainty hiding in plain sight*, PNAS 120(2):e2218530120, **LETTER** | [actual source PDF](https://drive.google.com/file/d/1VpL2sCk2gRSlKVlrGwzoTm5UWW-DgIxp/view) | 111,962 B; 2 pages; DOI 10.1073/pnas.2218530120 |
| Katrin Auspurg & Josef Brüderl (2024), *Toward a more credible assessment of the credibility of science by many-analyst studies*, PNAS 121(38):e2404035121, **PERSPECTIVE** | [actual source PDF](https://drive.google.com/file/d/1s95yC7Rkxp52GK1BpiQzdL_00a4FWlFE/view) | 341,123 B; 8 pages; DOI 10.1073/pnas.2404035121 |

Do not describe these as a randomized empirical AI translation study; genres are a 1-page Letter, a 2-page Letter, and an 8-page Perspective. Metadata-only rename/move preserved file IDs and byte counts. No independent fresh raw-file SHA256 was computed for the three uploaded PDFs.

## 2. Direct primary-source arguments, separately not blended

**Mathur et al. 2023** oppose the inference from 25/58/17 significance categories to "massive substantive variation". They state **90% of standardized point estimates in [-.037,+.037]**, and calculate that **90% of inferred underlying population effects** lie within about [-.014,+.014] under their meta-analytical model, a separate inferential claim. Their article links *actual public reproducibility code* at [ctcovington/MCV_BRWN-22_comment](https://github.com/ctcovington/MCV_BRWN-22_comment). W24 independently checked **1126/1253 = 89.864%** within ±.037 in the true original CRI derived file, supporting the **first descriptive** claim only, not their modeled population interval. Scientific versus statistical significance must be distinguished.

**Engzell 2023** argues that supposedly "same hypothesis" BRW work is a *bundle*: **2 immigration measures (4 including source variants) × 6 social-policy outcomes**, multiple countries/years and within/between-country analyses. Variation can be due to **different estimands**, not analyst unreliability. Engzell directly compares **174 models** of original Brady–Finnigan 2014 (using log odds ratios, **NOT directly comparable** in numerical scale to BRW AMEs) and notes that the original study itself had wide within-study variation, while broadly acknowledging BRW's contribution to open science. This is **strong prior art** for separating intended scientific questions from byte-level format issues.

**Auspurg & Brüderl 2024** delineate THREE stringent validity gates: (1) predefine meta-estimand and separate sources of variability; (2) ensure researcher participation/incentive/review resembles normal scientific research for external validity; (3) use suitable second-stage meta-analysis and measurement conversions. On pages 3–6, authors classify sources as (a) uncertainty over correct approach to an estimand, (b) sloppy/opaque research mistakes, and (c) **productive genuine heterogeneity in phenomena, populations or estimands**. Only (a)/(b) should automatically count as problematic uncertainty. Their §2.3.1 titled **'Do not get lost in translation: Effects must be on the same metric before they are pooled'** directly treats the danger of arbitrary or invalid metric conversion. They argue several BRW rescaling decisions produced artificial variance (including up to factor 10) and explain how wrong rescaling can attenuate meta-regressions. Their paper reports that a separate weighted least squares meta-regression with extra explanatory features increased visible variation explained from BRW's 5% to ~64%, citing their own earlier reanalysis. **W28 did NOT reproduce the 64% WLS-MRA or independently establish alleged factor-ten processing errors**: both are *attributed authored claims*, not proven by our W24 0/1252 CI category changes.

Crucial correction to previous EPISTEME reading: W25's result that standardized/raw 95% CI **categories** show 0/1252 flips **does NOT falsify** Auspurg–Brüderl's claim that the *magnitude and pooling metric* may be wrong. A positive scale factor preserves CI sign even when the scale and cross-estimand comparison are invalid. Their **Do not get lost in translation** framing is explicit near-verbatim fatal prior art for EPISTEME's broad "scientific conversion changes evidential warrant" rhetoric. Distinguish **metric** translation from the founding proposed **AI conversion intervention**; the shared word does not establish identical causal estimands or exact priority on the full TLP chain.

## 3. Specific research-director source verdict

- The independent field already contains a precise source-defined theory of correct/incorrect effects conversion, estimand heterogeneity, artificial meta-analytical variance and standards of evidential credibility.
- W24 source figures 25.4/57.7/16.9 are reproduced but **do not vindicate a large substantive effect** and **do not show that the many-analyst outputs measure one identical target question**.
- W25 CI category null merely limits one proposed error mechanism; it **cannot** dismiss worries about wrong effect-size normalization.
- The CRI data include no randomized AI translator assignment, no scientific community adoption intervention/time-series, and no independent feasible H0/H1 hypothesis-testing set. Consequently, all three are **fatal competitors** to broad EPISTEME claims but none proves or disproves a future well-defined AI-adapter causal effect.

**Next W29:** quantitative within-/between-team variance decomposition as a *descriptive test* of Engzell/Auspurg issues, nested by outcomes and immigration exposure types and with sensitivity, explicitly without claiming a new meta-estimand or epistemic law.
**Next W30:** return full founding Z→A→T and test whether any empirical causal residual beyond these competitors remains.

## 4. Current missing source ledger

The previously missing **Mathur 2023, Engzell 2023 and Auspurg–Brüderl 2024 original PDFs are now HELD in 10_PAPERS**, not missing. Their independently linked supplemental reproduction original (Mathur et al. GitHub; Auspurg–Brüderl OSF `https://osf.io/dtv2p/files/osfstorage/647cf174bf3d0f09d9d872be`) is **not locally cloned/run/archived by W28**. No need to download the three PDFs again.

Legacy CERN 2000 signed Management Board/LEPC/Research Board minutes and official third-party GESIS survey version/rights are unverified; neither blocks current author-derived numerical audit.
