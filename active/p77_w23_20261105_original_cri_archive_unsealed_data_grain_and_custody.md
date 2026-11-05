# EPISTEME-P77 W23 — Original 117-MB CRI Archive Acquired, Full Model Table Unsealed, and Scientific-Test Causal Gate

**Date:** 2026-11-05 KST  
**Director authority:** [P77 binding strategy](../STRATEGY_P77_CURRENT.md) · [official P77 Notion](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53).  
**Research status:** P77 ACTIVE, P78 HOLD, PAPER HOLD, independent EPISTEME innovation NOT CERTIFIED.  
**Previous:** [W22 scientific-test route countermodel](p77_w22_20261105_market_observability_scientific_test_route_countermodel.md).

## 1. Actual user-supplied ZIP discovered and placed in correct scientific project

**Source:** [CRI-master.zip, original user's Drive file](https://drive.google.com/file/d/1qRL9_P6mV4nJaBMgxq3p60ShDa5p-NJY/view). It was found by direct child listing of `RESEARCH_OS_LITERATURE/00_INTAKE`, **not by generic Google Drive search** (which missed it). Original Drive ID: `1qRL9_P6mV4nJaBMgxq3p60ShDa5p-NJY`. Original 117,386,632 bytes, MIME `application/zip`.

**Move actually completed:** `RESEARCH_OS_LITERATURE/00_INTAKE` → [My Drive/EPISTEME](https://drive.google.com/drive/folders/1X7veUdKK1PIbnUM2wN5SOzaDbuE_QWJm). **NOT** `RESEARCH_OS_CHAT_ARCHIVE/EPISTEME` (different folder ID `1JhOpcXKE-ACs04KEVN64Io53BivQOrOg`). Metadata readback confirmed original ID and size, new parent `1X7veUdKK1PIbnUM2wN5SOzaDbuE_QWJm`.

## 2. Actually unpacked ZIP, validated integrity and identified source rights risk

A 117,386,632-byte raw ZIP was mounted at `/mnt/data/CRI-master.zip`. Python `zipfile` inspected all member paths, rejected any absolute or `..` traversal and symlinks, checked **every member CRC** with `testzip() → None`, then extracted the full **439 files (461 entries including directories), 859,647,748 uncompressed bytes** to a working local directory. The archive SHA-256 calculated from the genuine bytes was:

`64756bfe62b25cdd7dbea57d2b063cb0f564225751d1f0251b4879f426894098`.

Source ZIP contains a lot more than derived author results. Among others: `data/ZA4700.csv`, `data/ZA6900_v2-0-0.csv`, `data/ZA2900.csv`, `data/issp1985_2016.dta`, `data/MIG_13112018215624915.csv`, and the corresponding `Provided Materials` folders. The original author repository's CC0 license alone **does not guarantee unrestricted republication of each third-party ISSP microdata file**. We did **not** upload those individually to GitHub or a separate globally shared Drive folder.

### Drive extraction destinations: precisely what succeeded

A new actual Drive folder was created: [My Drive/EPISTEME/CRI-master — Verified Extraction 20261105](https://drive.google.com/drive/folders/17piNryz_eTmhFgOKyHtzEmhM1Ok5YBZk), with subfolders `code`, `data_derived`, `metadata`, `results`, `binder`.

**Uploaded and verified:**
- [Selected source/data/core ZIP](https://drive.google.com/file/d/1CgxFRHi47xP3Mb6l2f7bolRG0NgnVugz/view), 330,005 bytes. Contains 18 selected public code/derived data/license/runtime and existing author tables, plus exact-path SHA-256 manifest — NOT a substitute for the full 859MB uncompressed source.
- [Extracted original README.md](https://drive.google.com/file/d/1CYnXVPlps5stgtPPnoGx1jBE5fuUiu74/view).
- [Extracted LICENSE.md](https://drive.google.com/file/d/1kmOWUAzPxLD-wtZbeRL8xdnSwvvdSoLk/view).
- [Actual derived model table `data/cri.csv`](https://drive.google.com/file/d/1wxu79Nipz7noHPprQIKXUyZbwvmuGfpK/view) — 2,046,600 bytes.
- [Actual `data/cri_team.csv`](https://drive.google.com/file/d/1Kc1iUM5kDOkGdfigAgBu8PMIhq5ke9m4/view) — 140,694 bytes.
- [Actual `data/cri_str.csv`](https://drive.google.com/file/d/16gsb5iwvwGw1PGnG72ecrEReeE_g8-cm/view) — 1,429,653 bytes.

A broader **individual-file Drive upload** was attempted but returned `container_session_expired` for several source paths. **Do NOT label the entire decompressed 439-file tree as uploaded into Drive.** Its full bytes are still preserved inside the original Drive ZIP, and local decompression was successful. The small selected research core ZIP contains readable source scripts. Do not claim additional successful uploads without file IDs/readback.

## 3. Actual model-level CRI data acquired and parsed — genuine major progress since W21–W22

Previous W20/W21 connectors returned empty text for the large `data/cri.csv`, but it was in the 117MB actual ZIP. Python extracted it and read it with `encoding='cp1252'`: **UTF-8 fails with UnicodeDecodeError** on this original. `data/cri_str.csv` also required `cp1252`, while `data/cri_team.csv` parsed with UTF-8.

| Original author source | Records incl Team0 | Columns | Baseline Team0 rows | After excluding Team0 |
|---|---:|---:|---:|---:|
| `data/cri.csv` | **1309** | **479** | **48** | **1261 submitted model records**, 72 distinct team IDs |
| `data/cri_team.csv` | **89** | **464** | **1** | **88 team-hypothesis records**, 72 distinct IDs |
| `data/cri_str.csv` | **1309** | **219** | **48** | **1261 source-model string records** |

For `data/cri.csv`, after excluding Team 0:
- **1,261** submitted model records (actual direct table count, not borrowed from paper).
- **1,253** records with nonmissing numeric `AME`, exactly the corrected PNAS Fig. 1 estimate denominator.
- **8** records with missing AME; all are original submission rows `t1m1` through `t1m8`, with `u_teamid=1` (`package=brm`). Missingness alone does not establish the exact cause.
- **1,252** records with nonmissing *both* numeric CI bounds `lower` and `upper` and also 1,252 nonmissing p-values. **Exactly one additional model `t75m14` has nonmissing AME `-0.07332` but missing lower, upper, and p**. This distinction matters when using *corrected* Fig. 1's caption 1,253 converged AMEs vs CI-based significance categories.
- `AME` signs among the 1,253 records: 687 negative, 2 zero, 564 positive — **not** counts of teams and **not** publication-weighted percentages. CI labeling and team inverse weighting are separate; do not reinterpret these raw sign counts as the final Fig.1 distribution.

These are **real source table computations** and improve data custody/reproducibility. **NOT** a rerun of all original regression models or an AI-adapter effect estimate.

### Explicit executable quality gate

[analysis/p77_w23_cri_archive_replay.py](../analysis/p77_w23_cri_archive_replay.py) contains standard-library ZIP CRC+SHA-256, `cp1252` model-table parsing and preregistered 1,261/1,253/1,252/8/1 checks, plus team-summary 89×464/11–55–23 counts. A locally executed separate Python/Pandas source analysis verified the displayed counts and exceptions; the committed standalone exact validator itself is still **awaiting an independent local replay receipt** (do not falsely mark the committed program separately executed).

## 4. What this validates—and what it does not

**Validates:** repository author data actually available under the ZIP; the 1,261 models / 1,253 nonmissing AMEs published denominator, Team0 subtraction, ID/judgment grain, discrepancy between AME and CI-complete rows, container metadata and clear mapping to the 2024 PNAS Fig.1 correction.

**Cannot validate yet:** (i) whether the 1,253 estimates reappear after re-running 1,261 original model scripts on original survey/immigration versions; (ii) whether any author model uses a wrong data transformation or disputed method; (iii) why `t75m14` lacks interval/p, beyond recorded missingness; (iv) whether a particular official or manual vs AI conversion changes **scientifically justified** discrimination under the same budget; (v) any community scientific standard adoption response to AI converters. No human subject work or field conversion experiment was performed.

This is crucial for the founder's TLP. The existence of real model-level data alone is **not an identified AI translator treatment**. Strong prior art (Farrell–Saloner/Arthur/Liu, Rosero, Janssen, Breznau, Reijula–Blanco Sequeiros, Pritchard–Wicenec) remains a serious obstacle; simple workflow portability/variance is not original theory.

## 5. Next W24 challenge, not a paper escape

The strongest next research unit is **actual result-level validity and source-route replication**:
1. Preserve the 117 MB raw original ZIP and snapshot hash; inspect original author `data_prep`, `team_code`, R environment and the 2024 corrected Fig. 1.
2. Try a *bounded* reproducibility cross-check of source table to original author output with explicit Team0 filter, NA handling, CI significance, model/team weighting and versioned code. Do not hand-correct away `t75m14` or misrepresent missing CI.
3. Separately ask whether the founding chain AI conversion -> community standards -> scientific test availability has any **genuine intervention data**, not merely the CRI team's rich analysis choices. If none, record a **negative novelty/evidence verdict** rather than expand archival chores without causal leverage.
4. Preserve original-data license caveats and genuine non-AI baseline; no manufactured measurements.

**Decision:** Original data acquisition and direct model-table audit **PASS**; original statistical model reproduction **PENDING**; AI-adapter treatment identification **NO-GO**. **P77 ACTIVE; P78/PAPER HOLD.**

## 6. Source debt ledger (holdings vs missing)

- **Acquired from actual user ZIP:** CRI author code, derived model-level CSV/strings/team summary, and bundled ISSP/immigration input *candidates*; provenance/version/legal reuse **not yet independently authenticated**. Do not send user to redownload the whole CRI GitHub ZIP.
- **Not fully validated:** External ISSP survey microdata (ZA2900/ZA4700/ZA6900 etc) versions and GESIS terms (files **physically bundled**, version/authorization unknown). Authenticated GESIS separate download is necessary only if checking against official originals, not just source-table reproduction.
- **Historic low priority:** CERN Management Board/LEPC/Research Board 2000 original signed minutes not authenticated in Drive.
- **Held:** Breznau PNAS 2024 correction, Janssen 2026, Rosero Abad 2026 PDF — do not list missing.
