# EPISTEME-P77 W20 — CRI Reproducibility Preflight, Correction Custody, and AI-Adapter Identification NO-GO

**Date:** 2026-11-05 KST  
**Director status:** P77 ACTIVE, P78 HOLD, PAPER HOLD, no EPISTEME novelty established.  
**Authority:** [Binding P77 strategy](../STRATEGY_P77_CURRENT.md) and [official Notion page](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53).  
**Preceding:** [W19 science-discrimination court](p77_w19_20261105_scientific_discrimination_case_adjudication_and_fatal_rivals.md).

## 1. New original paper custody (now VERIFIED HELD, not missing)

Two actual user-uploaded original PDFs were found in `00_INTAKE`, text-read, bibliographically verified, then metadata-renamed and moved to `10_PAPERS`. Parent folder and file byte lengths were read back; original Drive file IDs are unchanged. **No SHA-256 comparison or independent byte-level corruption test in W20.**

| File | Canonical Drive file ID / URL | Byte length | Original identification |
|---|---|---:|---|
| Breznau et al. (2024) — *Correction for Observing Many Researchers Using the Same Data and Hypothesis Reveals a Hidden Universe of Uncertainty* | [1NSkJ1yxy8vZ4EUP6SwD5BQa3mbe5_G4z](https://drive.google.com/file/d/1NSkJ1yxy8vZ4EUP6SwD5BQa3mbe5_G4z/view) | 282,123 | PNAS 121(26), e2410677121, DOI 10.1073/pnas.2410677121; two pages, published 2024-06-20. Correction states Fig. 1 appeared incorrectly, supplies corrected Fig.1/legend. It does not instruct that original regression data or the overall published theory was withdrawn. |
| Janssen et al. (2026) — *Toward Full Interoperability in Materials Science: Integrating Workflows With Knowledge Graphs* | [1WTPIdhhpn5l1xOB-K3D6iIOh9erpZCzo](https://drive.google.com/file/d/1WTPIdhhpn5l1xOB-K3D6iIOh9erpZCzo/view) | 1,150,308 | *Advanced Engineering Materials* 28:e71258, DOI 10.1002/adem.71258, 19 pages; explicitly a **PERSPECTIVE**, not new randomized experimental data. |

W19 [Rosero Abad et al.](https://drive.google.com/file/d/1ylQS-SgEpLzolGGq2x89nSryGEfmJSMt/view) already moved to `10_PAPERS`; no duplicate migration here.

### Janssen 2026 direct novelty challenge

The full original **abstract and introduction** explicitly mention workflow management systems, interoperable Python Workflow Definition abstraction, *atomRDF*, Abstract Workflow Language, semantikon, RDF knowledge graphs, provenance, large language models, AI-assisted workflow orchestration, and computational/experimental workflow linking. Thus the generic claim *"semantic workflow adapters, provenance and LLMs enable science interoperability"* is directly anticipated. As a **perspective/review**, it does not establish a field causal effect of a particular AI translator on actual scientific hypotheses; still, it is fatal prior art to merely combining those component names into a proposed novel theory.

## 2. Read actual CRI repository files instead of only reading its paper

User's previous W19 selected [Breznau et al. 2022](https://drive.google.com/file/d/1lsyHjglet1NaXlOf2EYfNPtW92jU5aYK/view) as a candidate starting case. In W20 the following **live public GitHub original repository paths** were directly fetched:

- [nbreznau/CRI README](https://github.com/nbreznau/CRI/blob/master/README.md) at content SHA `ea69197fc15af820e0e9f008e9461259ce3f760b`. Reports 73 teams, R Markdown `.Rmd` notebooks and HTML outputs, workflow starting in `team_code` then `data_prep`, optional Binder and Shiny visualizations.
- [code/01_CRI_Descriptives.Rmd](https://github.com/nbreznau/CRI/blob/master/code/01_CRI_Descriptives.Rmd) at SHA `f770e0e4743118fd8a83b00303b3a903da12efed`, actual source and model-level/team-level data readers.
- [code/07_CRI_DVspecific_Analyses.Rmd](https://github.com/nbreznau/CRI/blob/master/code/07_CRI_DVspecific_Analyses.Rmd) at SHA `07c7f3afac2c7e7c0e08d8393059d0a4c7cdda5e`, real R code depending on many packages.
- [LICENSE.md](https://github.com/nbreznau/CRI/blob/master/LICENSE.md), CC0 1.0 license text; *do not infer from this alone that third-party ISSP source survey/raw data carry the same rights*.
- [Binder runtime](https://github.com/nbreznau/CRI/blob/master/.binder/runtime.txt) contains `r-4.1-2021-05-18`. [Binder install script](https://github.com/nbreznau/CRI/blob/master/.binder/install.R) installs numerous R dependencies and explicitly resorts to a CRAN archive URL for `lavaanPlot` 0.6.0. It is **not** evidence Binder launches successfully today; the archived dependency's live reachability is unverified.
- [data/cri.csv](https://github.com/nbreznau/CRI/blob/master/data/cri.csv) content interface returned **empty text but reported file SHA `bf783b4897c7e69d021271ca1854b6de9d53b09d`**. This is a **read limitation or ambiguous empty result**, **not** proof that the historical dataset lacks rows. No CSV bytes were actually parsed or used to compute results.

**Serious paper/reproduction traps directly attested in README:**
1. Data include **Team 0** (Brady–Finnigan 2014 baseline), which the paper's main 73-team analyses *exclude*. The real `01_CRI_Descriptives.Rmd` explicitly filters `u_teamid != 0` for `cri.csv`, `cri_team.csv` and `cri_str.csv`. Reproductions must also filter.
2. README warns a belief-in-hypothesis field is mistakenly reverse-recoded in the workflow, while asserting this does not affect the published results. Do not use that field as an unverified ground-truth baseline or silently "fix" it without a matched analysis/version audit.
3. PNAS correction of original Figure 1 is now **actually held**. Its legend explicitly specifies **n=1,253 converged models** and distinguishes the signs of AMEs and significance from labels. Do not conflate **1,261 submitted models**, **1,253 converged models**, **72 submitting teams**, and **73 starting teams**. Corrected article does not constitute new AI experiment.

**Execution evidence boundary:** W20 read original R notebook sources, license, runtime and paper correction. **No full clone, dependency installation, Binder session, survey/CSV parse, original R rerun, model-level result reproduction, or AI adapter execution** was conducted.

## 3. Scientific H0/H1 and precise proposed estimand

**Existing substantive hypothesis:** greater immigration decreases support for welfare/social policies vs lack of that predicted association, with the actual original model/ISSP measurement choices preserved as described in CRI. This substantive question is *not* invented by EPISTEME.

A *different* **future engineering/intervention question** could be: on a prespecified set of documented CRI analytical tasks and permitted data, does **agentic AI-assisted translation** versus **human-validated deterministic manual/schema-based translation** change which prespecified inferential checks can be completed correctly and reproducibly **under equal compute/time/error-validation budgets**?

For task j and assigned treatment z, define `Y_j(z)` = preregistered binary successful execution of a specific inferential test, **including comparison with the original faithful method and independent provenance/assumption checks**, rather than the mere presence of a numerical p-value. One possible target is `ATE = mean_j [Y_j(1)-Y_j(0)]` over a specified task population and a defined random-assignment scheme. For a single observed run, both potential outcomes are not simultaneously observed; repeated randomized assignments or matched careful comparison needed. The task population, intervention version, data license, verifier, tolerance, alternative route, costs, and preregistration have **not** been fixed or executed.

- **Baseline 0:** original faithfully executed R code with proper version/Team-0 exclusion (positive control).
- **Baseline 1:** non-AI explicit schema mapping plus validation with equal time/compute (strong converter control).
- **Treatment 2:** a precisely versioned AI-assisted transformation, subject to equivalent tests and error control. LLM output that merely reproduces a headline AME is not proof of correct scientific hypothesis testing.
- **Outcome extension (requires distinct cohort evidence):** community standard adoption/retention. The public CRI record does **not** have AI translation assignment or a matched adoption cohort, so it **cannot** identify the full TLP chain.

**Strong established rivals:** compatibility/converter economics (Farrell–Saloner, Arthur, Liu, Heinrich, Rosero Abad), workflow equivalence/provenance (Pritchard–Wicenec, PROV-IDEA, Workflow RO-Crate, Janssen), evidence discordance (Breznau, Reijula & Blanco Sequeiros, Blanco Sequeiros). Do not call reduced workload, improved portability or changed analytical answer a new epistemic law absent specific adversarial evidence.

## 4. W20 decision — identify GO/NO-GO boundaries now

| Gate | Finding | Status |
|---|---|---|
| Published substantive H0/H1 | Breznau PNAS paper read, correction acquired | PASS for *source definition*, not inference verification |
| Existing reproducible original scripts | Real CRI RMarkdown files readable | PASS for *code inventory* |
| Corrected result labels and Team-0 handling | PNAS 2024 correction and GitHub code/README cross-checked | PASS for documentation |
| Data bytes and reuse/rights | `cri.csv` returned no readable text in connector; separate ISSP source-data rights not evaluated | **HOLD** |
| Environment and baseline executable | R runtime and install script read; no actual installation or baseline tests | **HOLD** |
| AI adapter intervention and strong alternative | No versioned intervention, matched non-AI baseline, or assigned tasks | **HOLD** |
| Community-level standard lock-in measurement | CRI 2022 data have no original assigned AI adapter or standard adoption treatment | **NOT IDENTIFIED** |
| Existing theory residual | Multiple direct economics, computational workflow and HPS rivals already cover broad mechanisms | **NO NOVELTY CERTIFIED** |

**Decision:** `W20 PRE-FLIGHT COMPLETE / REAL AI INTERVENTION NO-GO / P77 ACTIVE`. It would be methodologically unsound to infer a TLP causal effect from the old data or the synthetic W18 market-choice model. A future narrow **technical** experiment might be possible upon clearing source rights, baseline reproducibility and matched comparator gates, but even then its successful engineering outcome alone would not establish an independent EPISTEME theory.

## 5. Cross-project Drive EPUB inventory side-question

The user also asked for *presently problematic EPUB* in Google Drive. Independent Drive metadata searches `mimeType='application/epub+zip'`, `application/x-epub+zip`, `name contains '.epub'`, and `name contains 'EPUB'` returned **no current EPUB file identities** in the accessible search scope. Broad `epub` full-text search returns PDF/Google Doc/chat-log mentions, not actual EPUB mime items. The canonical `11_BOOKS` folder shows PDF book files in direct listing. Therefore no current `broken EPUB` **bytes** can be certified.

[Historical 2026-10-24 chat archive](https://drive.google.com/file/d/1B9iOLpaHszWAAVgL_nVaV2A6XX8a_V1J/view) mentions:
- **Arrow (1951), *Social Choice and Individual Values* EPUB** initially acquired but then marked **physical/full-text collation pending**, with **no present EPUB Drive ID recovered**. A [PDF substitute](https://drive.google.com/file/d/1pyOmat3nskLH4kC8xsHjjXwTH_qwIJnw/view) remains `TEXT EXTRACTION HOLD`; it is a PDF, not a currently identified EPUB.
- **Joyner, *Adventures in Group Theory* (2nd ed.) EPUB** historically marked imported/metadata-tested and moved to `11_BOOKS`, but currently no EPUB file found by filename/format or author search; do not call it broken or deleted without identifier/version/custody evidence.
- **Tollefsbol *Handbook of Epigenetics*** historically suffered **edition mismatch**: intended 3rd vs [actual 2nd-edition PDF](https://drive.google.com/file/d/1CKqaMAuziNiGDhZuYAs2MXEWuD9IRFS1/view). The defect is bibliographic, **NOT a verified EPUB corruption**.

Do not destroy, rename or quarantine anything based only on historic chat references. The EPUB issue is now a **historical custody conflict**, not a confirmed damaged EPUB file. No EPUB files were moved/deleted by this audit.

## 6. Next action and missing source table

**W21:** Seek legitimate read access to CRI model-data CSV and its provenance, compare original R code prerequisites and corrected figure, only then decide whether a secondary-data-only reproducibility preflight is possible. Do **not** recruit people, claim randomized experimental results or elevate P78.

Missing/conditional files:
- **ISSP source survey data + license/version for CRI**: independently held raw survey bytes and reuse permissions not verified (the GitHub project's CC0 license does not settle third-party rights).
- Historical **original 2000 CERN Management Board/LEPC/Research Board minutes** remain nonpriority, not verified held.
- **No missing Rosero 2026 / Janssen 2026 / PNAS 2024 correction**: all three verified in `10_PAPERS`.

**P77 ACTIVE / P78 PAPER HOLD / 12-week program is a bounded research residency, not a promised innovation.**
