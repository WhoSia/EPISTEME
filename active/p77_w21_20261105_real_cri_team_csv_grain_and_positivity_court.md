# EPISTEME-P77 W21 — Actual CRI Team-Data Read, Unit-of-Analysis Correction and Causal Identification Barrier

**Timestamp:** 2026-11-05 KST
**Research director:** [binding P77 charter](../STRATEGY_P77_CURRENT.md) · [official Notion](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53)
**State:** P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novel mechanism NOT CERTIFIED
**Earlier:** [W20 original-code reproducibility preflight](p77_w20_20261105_cri_preflight_corrections_epub_custody_and_intervention_nogo.md).

## 1. Concrete new result: access to an actual original analysis dataset

The GitHub connector returns an empty text body when reading public [nbreznau/CRI/data/cri.csv](https://github.com/nbreznau/CRI/blob/master/data/cri.csv), with blob SHA `bf783b4897c7e69d021271ca1854b6de9d53b09d`. Inspection of the original GitHub file page independently explains why it may be difficult to present: `cri.csv` is ~1.95 MB and is not previewable as searchable text in GitHub; this is a transport/representation issue, NOT evidence the file is empty. We did NOT read, hash, or parse its entire model-level contents.

However the GitHub connector successfully returned an actual 140,694-character CSV text for [nbreznau/CRI/data/cri_team.csv](https://github.com/nbreznau/CRI/blob/master/data/cri_team.csv), Git blob SHA `20293f871cdc613903601b3ea3ce089de6d002a5`. It was **actually parsed as CSV, including quoted fields, in memory** in W21; values were not invented from article text.

**Observed team-level file structure:**

| Check | Direct parsing result |
|---|---:|
| CSV data records excluding header | **89** |
| CSV columns | **464** |
| Unique `u_teamid` values, including original-study team 0 | **73** |
| Rows after removing `u_teamid==0` | **88** |
| Unique team IDs after removing team 0 | **72** |
| `AME` numeric (parseable) | **88** |
| `AME` missing/NA | **1** |
| `Hresult=No test` | **11 rows** |
| `Hresult=Reject` | **55 rows** |
| `Hresult=Support` | **23 rows** |

The actual CSV has consistent 464-field records. **Exactly 16 distinct team IDs each appear twice** in this source; remaining team IDs appear once. The 89 rows are therefore **team–hypothesis/judgment records, not 89 independent teams**.

The original README discusses an 89-unit team-conclusion table and the source notebooks exclude team 0 with `subset(u_teamid != 0)`. The **2022 paper study participants** are 73 teams in the broader original study, 72 teams submitting models, 71 teams yielding numerical model results. The **73 unique IDs including Team 0 in this particular released table are NOT the same set as the original 73 participant teams**; do not silently map or assume equal denominators. At least one original participant team is not present as an independently numbered ID in this compiled team-level table. This is an *apparent cohort coverage discrepancy*, not a claim of data misconduct or source error; exact historical team-ID mapping still needs author/README validation.

**Further interpretation controls:** `Hresult=No test` does **not** imply the 11 rows never attempted a statistical analysis; only one of the 89 records has missing `AME` in this table. `Hresult` encodes subjective judgment, not necessarily numerical statistical significance. Never claim "11 teams did not analyze anything". In the 2024 [PNAS Fig. 1 correction](https://drive.google.com/file/d/1NSkJ1yxy8vZ4EUP6SwD5BQa3mbe5_G4z/view), the figure caption is explicitly about **1,253 converged model estimates**; it cannot be regenerated from the 89 aggregated rows without more data and methods.

### New reproducibility asset

[analysis/p77_w21_cri_team_grain_validator.py](../analysis/p77_w21_cri_team_grain_validator.py): standalone Python standard-library, read-only CSV parser and expected-grain drift detector for an authentic local copy of `cri_team.csv`. Its **synthetic quoted-field, duplicate-team, NA fixture self-test** ran locally and passed; separately the **actual 140,694-character CRI source** was parsed in the in-tool JavaScript runtime, yielding the 89×464 source matrix and counts above. We did NOT run Python against a locally acquired real CSV file; retain this split execution receipt and do not claim the Python validator itself has executed the real source.

## 2. Original-code lineage, nontrivial caveats

Inspected original [nbreznau/CRI/code/01_CRI_Descriptives.Rmd](https://github.com/nbreznau/CRI/blob/master/code/01_CRI_Descriptives.Rmd), [code/02_CRI_Common_Specifications.Rmd](https://github.com/nbreznau/CRI/blob/master/code/02_CRI_Common_Specifications.Rmd), [code/03_CRI_Spec_Analysis.Rmd](https://github.com/nbreznau/CRI/blob/master/code/03_CRI_Spec_Analysis.Rmd), and [code/04_CRI_Main_Analyses.Rmd](https://github.com/nbreznau/CRI/blob/master/code/04_CRI_Main_Analyses.Rmd) as original R notebook source. The public [README](https://github.com/nbreznau/CRI) warns Team 0 original-study baseline inclusion in released data (exclusion in main results), a miscoded belief variable, and the need to account for split subjective conclusions. Prior W20 fetched the CC0 repository license and Binder environment. **We have not installed R packages or rerun original statistical models.**

[Results TblS4](https://github.com/nbreznau/CRI/blob/master/results/TblS4.csv), [TblS8](https://github.com/nbreznau/CRI/blob/master/results/TblS8.csv), [TblS11](https://github.com/nbreznau/CRI/blob/master/results/TblS11.csv) were actually readable, with Git blobs `5f7681097f04598e05109a984cb8c242687c471d`, `ac8ac03f8c5c8241ee0a4e8a9364f01f99e3939c`, `cc0527c2e05f92bc7dd49a3e2e61826a52cb3177` respectively. The output files are not independent reproductions.

**Licensing:** the repository CC0 text is present, but that does not automatically establish the reuse terms of separately sourced ISSP survey microdata, independent datasets used by teams, or personally identifying participant information. Do not copy or publish raw participant files on the presumption that a repository license settles upstream rights.

## 3. Causal identification: why the original CRI dataset cannot establish the founder thesis

Define `Z` as a well-defined, versioned AI translation intervention applied to a prespecified analytic conversion task; `Y` as completion of a *scientifically valid and reproducible* discriminating test under a matched budget. If all observations in the historic CRI data lack an actual assigned `Z=1`, then positivity/overlap fails:

`P(Z=1 | X=x)=0` for the observed sample, so the average causal contrast `E[Y(1)-Y(0)]` is not nonparametrically identified from those observational records alone.

A model that regresses Hresult or AME on team choice variation cannot repair this: researcher design choices, software practices, statistical thresholds and acceptance criteria are **not** the treatment of interest. Neither the set of computationally possible tasks nor collective standard adoption is observed as a separate outcome. Alternative routes (manual conversions and existing workflow standards) remain essential.

This is a familiar causal-inference fact, not a novel theorem. Existing social-science multiverse analysis, philosophy of evidential discordance, workflow provenance and network compatibility economics all already explain major components. The source data simply make the missing-treatment problem particularly clear.

**Independent EPISTEME explanatory residual:** NOT FOUND in the available CRI observational dataset. The practical acquisition of 89 real rows is a data-validation improvement, not proof of a new physics or epistemology claim.

## 4. Conditional next gate W22

Keep P77's original question; do NOT turn it into a perpetual CRI reproduction project. W22 should conduct a sharp comparison:

**Candidate test:** take a fixed science hypothesis and small set of authentic source-code translation tasks that have independent reference answers. Assign (A) original environment, (B) equally resourced explicit non-AI schema/code translation, (C) versioned AI translation. Prespecify outcomes in three separate dimensions: semantic output fidelity, admissible inferential tasks and group selection/adoption. An engineering win on (A)→(C) is not automatically a network lock-in or epistemic novelty result. If no independent (C) intervention is actionable, do not claim causal effects.

**Required entry:** authentic source/permission and executable base pipeline; versioned converter and strong manual alternative; preregistered task units, fixed randomization/negative controls; independently checkable output and validity; explicit outcome for any communal standard selection claim; safety/ethics approvals if human participants are sought.

No study participants recruited and no field experimental intervention implemented in W21. **P77 ACTIVE / P78 HOLD / PAPER HOLD; director adjudication remains bounded.**

## 5. Current pending original/byte table

- **ISSP survey raw-data version and external usage terms:** not independently acquired/verified, despite project CC0 code being present.
- **`cri.csv` model-level (~1.95 MB) raw bytes/complete text and actual R statistical reproduction:** GitHub page confirms file is present but connector text empty and no local raw-file replay.
- **CERN Management Board 2000-12-07 / LEPC and Research Board Nov 2000 signed original minutes:** not in verified Drive custody (nonpriority heritage).
- **Rosero Abad 2026, Breznau 2024 corrigendum, Janssen 2026:** verified already-held in Drive 10_PAPERS; do NOT add as missing.
- EPISTEME-only Github authorship policy no `github-actions[bot]`; Notion = decision authority; Drive = bytes.
