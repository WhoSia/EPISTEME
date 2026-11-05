# EPISTEME-P77 W22 — Research Data Acquisition Guide (CRI + ISSP, 2026-11-05)

**Purpose:** Manual download instructions for the user; **not** a claim the files were downloaded into Drive. Related [W22 scientific-test observability court](p77_w22_20261105_market_observability_scientific_test_route_countermodel.md).

## A. The first thing to download: original author-analysis data and code

**Source:** https://github.com/nbreznau/CRI

**Easy (Windows/browser):**
1. Visit the exact GitHub repository linked above and select **Code → Download ZIP**. Extract to a stable local folder, e.g. `Documents/EPISTEME_sources/CRI_author_repo/`.
2. If the full repository is too large, individually open and save **Raw** for `data/cri.csv`, `data/cri_team.csv`, `data/cri_str.csv`. Also get `README.md`, `LICENSE.md`, `code/01_CRI_Descriptives.Rmd`, `code/03_CRI_Spec_Analysis.Rmd`, `code/04_CRI_Main_Analyses.Rmd`, and `.binder/runtime.txt` / `.binder/install.R`.
3. Do not treat `data/cri.csv` as empty because the chat connector returned empty text. [Actual GitHub file](https://github.com/nbreznau/CRI/blob/master/data/cri.csv) is ~1.95MB and the website warns it is too large to preview; `data/cri_team.csv` was actually parsed at 89 rows x 464 columns (Git blob SHA `20293f871cdc613903601b3ea3ce089de6d002a5`).
4. The author README states `cri_team.csv` uses **89 team-hypothesis units** because 16 teams gave separate stock/flow conclusions. Its main work omits **Team 0** from estimates; treat 73 teams, 72 submitting teams, 1,261 submitted models, 1,253 converged models as different denominators. Do not accidentally count historical original-study Team 0 as a CRI participant.
5. Save the [2024 official PNAS Fig. 1 correction PDF, already held in Drive](https://drive.google.com/file/d/1NSkJ1yxy8vZ4EUP6SwD5BQa3mbe5_G4z/view). Do not overwrite or silently substitute the earlier article PDF.

**Developer/PowerShell alternative (requires installed Git, no credential needed for this public repository):**
```powershell
git clone https://github.com/nbreznau/CRI.git
Set-Location CRI
git rev-parse HEAD
Get-FileHash .\data\cri.csv -Algorithm SHA256
Get-FileHash .\data\cri_team.csv -Algorithm SHA256
```
Preserve the obtained commit hash alongside the SHA256 digests; do not invent or assume an expected hash. The Git **blob SHA** exposed in the repo and a raw-file **SHA-256** are different hash types.

**Alternate originally cited repository:** Harvard Dataverse https://doi.org/10.7910/DVN/UUP8CX. This dataset is explicitly referenced by the *PNAS* data-availability statement, but its live Dataverse download interface was **not opened successfully** in the W22 web environment. Use it as a cross-check, not a guaranteed one-click file list. The authors' **GitHub** was accessible and independently read.

## B. Required base social-science data — GESIS/ISSP Role of Government waves

**Official entry:** https://issp.org/data-download/ and https://www.gesis.org/en/issp/data-and-documentation/role-of-government

These are *survey microdata* used to build original response variables, NOT the `cri.csv` postanalysis outputs. ISSP/GESIS says downloads are **free but require registration/account login**.

**Follow the topic-year links for these five surveys** (full original CRI design considers *up to* five waves, not necessarily identical variables or countries in all years):

| Survey | GESIS code | Original data portal | Latest version displayed in official ISSP module (as accessed 2026-11-05) |
|---|---|---|---|
| Role of Government I — 1985 | ZA1490 | https://www.gesis.org/en/issp/data-and-documentation/role-of-government/1985 | v1.0.0, DOI https://doi.org/10.4232/1.1490 |
| Role of Government II — 1990 | ZA1950 | https://www.gesis.org/en/issp/data-and-documentation/role-of-government/1990 | v1.0.0, DOI https://doi.org/10.4232/1.1950 |
| Role of Government III — 1996 | ZA2900 | https://www.gesis.org/en/issp/data-and-documentation/role-of-government/1996 | v1.0.0, DOI https://doi.org/10.4232/1.2900 |
| Role of Government IV — 2006 | ZA4700 | https://www.gesis.org/en/issp/data-and-documentation/role-of-government/2006 | v2.0.0, DOI https://doi.org/10.4232/1.13707 |
| Role of Government V — 2016 | ZA6900 | https://www.gesis.org/en/issp/data-and-documentation/role-of-government/2016 | v2.0.0, DOI https://doi.org/10.4232/1.13052 |

**Step-by-step:**
1. Open https://issp.org/data-download/ → **Role of Government** year link.
2. On each official GESIS module page choose **Data Access / Download of data and documents**.
3. Create/sign into the GESIS account if required; comply with its actual terms. Download the original compatible data package and related *codebook/source questionnaire/variable report*. Select common SPSS/Stata formats as available; do not assume CSV automatically exists.
4. Record **ZA study ID, version, DOI, download date and license/conditions** for each wave. Keep original ZIP untouched. If there is a differing dataset version from the original 2022 authors' analysis, record it, and do not call the new output an exact reproduction.
5. A separately prepared *Role of Government cumulation* dataset is available (official cumulative portal https://www.gesis.org/en/issp/data-and-documentation/data-cumulations), but cannot be assumed exactly equivalent to the particular variables/country/year definitions the CRI project used.

The paper also says researchers were provided immigration *stock* and *flow* indicator data from the World Bank, United Nations and OECD. **Downloading only the five ISSP waves is not sufficient for a faithful replication**. First recover the actual CRI prepared files/provenance and sample definitions; only then acquire source immigration indicator vintages and validate their data-use conditions. Source paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC9636921/.

## C. Where the files should go and what the user may share

**Local storage recommendation:**
```
EPISTEME_sources/
  CRI_author_repo/           # GitHub or ZIP extraction, preserve repo version
  ISSP_1985_ZA1490/          # raw study package + codebook, if downloaded
  ISSP_1990_ZA1950/
  ISSP_1996_ZA2900/
  ISSP_2006_ZA4700/
  ISSP_2016_ZA6900/
  acquisition_manifest.txt   # filenames, original SHA256, version, DOI, date, rights
```

Only move datasets to the Google Drive canonical source shelf after confirming license and correct project custody. In particular, **do not assume ISSP third-party microdata can be redistributed in an open/public GitHub repository** even though the authors' own code is CC0. Do not disclose account credentials or private restricted access tokens. A safe low-friction thing to send in chat is a source **filename list and checksum+version manifest** (no credentials or survey respondent data). If uploading is permitted, preserve raw source bytes and provenance, not a modified reconstructed table.

**Minimal manifest contents** (not filled with fake hashes):
```
source=ISSP 2006 Role of Government IV
study_id=ZA4700
version=2.0.0
doi=10.4232/1.13707
local_filename=<your exact downloaded original>
sha256=<actual Get-FileHash output>
date_acquired=<actual date>
license_or_terms=<terms read from GESIS at download>
```

## D. Preflight decision after acquisition

**Pass 1:** Confirm exact original files and versions, team-0 handling, and that the baseline author code can be executed with its declared R dependency stack.

**Pass 2:** Check numeric published outputs against the 2024 Fig.1 correction and archived author results, allowing explicitly specified numerical tolerances; no convenient invented matches.

**Pass 3 (only if justified):** Compare original code, strongest deterministic/manual conversion and a versioned AI translation under matched budget against real inferential validity conditions.

**No AI treatment and no communal adoption outcomes were assigned in the 2022 CRI study**; even perfect reproduction of all 1,253 model results is not direct evidence of the EPISTEME founding causal thesis. P77 ACTIVE / P78 + PAPER HOLD.
