# P77 W62 — Repeated Source Rows, Model Response Instability and cta Candidate Timing

**2026-11-21 KST. Source-authenticated Research OS quality work; not certified EPISTEME independent causality.** Notion remains authoritative for scientific judgments and the active [19-line missing-evidence ledger](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385). No new manuscript-level author execution was obtained.

## Source identity and execution checks

- [Sundaram et al. (2026) original source ZIP](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view): Zenodo 17516680 / 17555722, original 3,992,768 B, SHA-256 `bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c`, archive CRC verified. Actual held ZIP was read directly for [10 archived BioSample model-result files](../analysis/p77_w62_repeated_response_audit.py). Three cohorts, 800 rows per model output, including two separate liver Llama3 DD/CEDAR files. [W61 Work original lineage receipt](https://drive.google.com/file/d/1bpZ02RY5X-AVxntmNvA_hk6OyyKeHD2b/view) and [W60 original content audit](../analysis/p77_w60_zenodo_cohort_court.py) were compared.
- [S-BIAD602 210929 RTF](https://drive.google.com/file/d/1NJLsRKkScl2safAl-wTn_y-pc_BtSnAl/view), 697 B SHA-256 `f276dbc5caa9b42de87ac98310d9f5b0fa3fec275b4800341c8005df8c2915f9`.
- [S-BIAD602 211005 RTF](https://drive.google.com/file/d/1f2xl3sNrRjVg4Tcbr0zZraELpiNHt10O/view), 660 B SHA-256 `378f5fe961a668b28d443e44944899c9cfd81ebbf09b6aa250229ff6b537cbc2`.
- [S-BIAD602 211007 RTF](https://drive.google.com/file/d/1JFQ7gAY6PRNw4iZKYpwHAFofOTCN5cIp/view), 682 B SHA-256 `7af88904395e0d381ab797431b7a99c9b9444a733c64c8c39473151019f39522`.

All 3 RTF original bytes were independently downloaded from Drive and hashes, sizes, and explicit 30 sec/frame cadence verified against W61 Work receipts.

## 1. Duplicate input-source groups: raw source fields vs sample identifiers

Source signature = exact JSON of `BioSample` after removing only the field `biosample_accession`, sorting object keys; no semantic normalization of values. This is *not an asserted globally unique identity*.

| Cohort | Rows | Distinct source signatures | Repeated signature groups | All rows in those groups | Excess rows under one-per-signature hypothetical |
|---|---:|---:|---:|---:|---:|
| liver | 800 | **752** | **24** | **72** | **48** |
| lung | 800 | 780 | 18 | 38 | 20 |
| ovarian | 800 | 777 | 6 | 29 | 23 |

In the **liver GPT-4** file all 800 records carry an explicit accession: 752 unique accessions, each repeated source-signature group has the **same accession** and each accession maps to only one source signature. The 24 repeated groups have sizes 2 (11 groups), 3 (9), 4 (3), and 11 (1). The 48 excess rows constitute 6% of the released 800-row table. Source-content repetition cannot be promoted to accession-level or specimen-level duplication for lung or ovary, where output source dictionaries lack the accession field.

## 2. Same input signature, different prediction artifacts

Two separate metrics on each repeated group:
- FULL: at least two distinct whole JSON dictionary prediction outputs.
- TISSUE: at least two different case-folded/trimmed values under `tissue` or fallback `tissue_type`; **missing field counts as an explicit structural token**; not a tissue correctness label.

| Liver model/condition | Repeated groups with distinct FULL outputs /24 | Distinct TISSUE tokens /24 | Rows with `tissue` or `tissue_type` among all 800 |
|---|---:|---:|---:|
| GPT-4 DD (LLM) | 22 | 9 | 614 |
| GPT-4 CEDAR | 21 | 8 | 800 |
| Llama3 DD | 24 | 24 | 633 |
| Llama3 CEDAR | 24 | 14 | 315 |
| MedLlama DD | 23 | 0 | 13 |
| MedLlama CEDAR | 24 | 2 | 6 |

Extremely low `tissue`-key presence for MedLlama reflects large amounts of arbitrary freeform dictionary-key text in original released outputs; **a TISSUE difference count of zero cannot establish prediction consistency**. A differing whole dictionary can reflect field-name variation or ancillary formatting rather than a change in the biological tissue label. GPT-4 CEDAR has full `tissue` presence and still eight repeated groups with different normalized tissue tokens.

**Mechanism uncertainty:** the original per-row invocation prompt, random seed, model snapshot, temperature, and execution order are missing. The within-source divergence **does not prove** stochastic LLM instability across identical invocation conditions. Do not infer causality, real-world error rate, or automatically falsify published aggregate metrics.

## 3. Counterfactual weighting sensitivity (strict mathematical caveat)

In the liver GPT-4 raw release, let `n_i` be the number of occurrences of accession `i`; `N=800` rows and `U=752` unique accessions. For a *single fixed bounded score* `f(i) ∈ [0,1]` that is truly the same on every duplicate, the row-weight distribution `p_i=n_i/N` and unique-accession weight `q_i=1/U` have total-variation distance

`TV(p,q) = (1/2)Σ_i|n_i/800 − 1/752| = 273/4700 = 0.05808510638.`

Consequently, the largest **possible difference in a mean of such hypothetical accession-level bounded scores** is 5.8085 percentage points. The 11-row repeated accession has relative weight `(11/800)/(1/752)=10.34` times that of any one accession under uniform accession weighting. This is a mathematical *counterfactual bound*, **not** a measured estimate of performance error and **not** a bound on the actual precision, recall, F1 or p-values. It cannot be transported to row-dependent model predictions that differ within the same accession, nor to a different gold-standard or unit-of-analysis scheme. See [code](../analysis/p77_w62_accession_weighting_bound.py) and [five tests](../analysis/test_p77_w62_accession_weighting_bound.py).

## 4. Five cta embryo *candidates*, 9-minute and 17-minute possible frame pairs

All three original dated RTF notes report 30 seconds/frame and 0.49 µm/pixel. Conditional on `t0` being the zero-based frame of actual author biological `Tcell=0`, no dropped frames, and the embryo being in Figure 2E, the pair at minute `m` is `[t0+2m,t0+2m+1]`.

| cta candidate folder | t0 | 9 min frames | 17 min frames |
|---|---:|---|---|
| `embryo1_210929_1_1` | 23 | 41–42 | 57–58 |
| `embryo2_210929_1_3` | 17 | 35–36 | 51–52 |
| `embryo3_211005_1_2` | 33 | 51–52 | 67–68 |
| `embryo4_211007_1_1` | 17 | 35–36 | 51–52 |
| `embryo5_211007_1_2` | 7 | 25–26 | 41–42 |

RTF `210929` additionally notes `#1_2 t0=22`; this annotation was not assigned to one of the five named candidate folders. The table is NOT verification of deposited marker file existence, original author's selected five biological embryos, actual Tcell temporal registration, PIV conditions, or published t-test input. Original Figure 2E reported WT n=5, toll vl n=6 and cta n=5; coincidence of counts alone does not prove panel identity.

[Reproducible candidate-frame code](../analysis/p77_w62_cta_candidate_frame_map.py) · [six tests](../analysis/test_p77_w62_cta_candidate_frame_map.py).

## 5. Independent scientific critique

The [2026 Sundaram GigaScience published paper](https://doi.org/10.1093/gigascience/giag019) says 4,800 source records across 3 cancers×2 repositories, reports 6 independent runs in statistical analysis, and states that tissue gold truth was heuristic plus 5% manual checking. The actual raw manifests and independent run IDs have not been linked to the published summaries; **six query task rows, six reruns, and six independent cohort-level units cannot be assumed equivalent.** W55 overview Precision/F1 row permutations, W60 GEO Llama3 three-output cohort mismatch, W61 BioSample repetitions and W62 tissue-key discrepancies are distinct defects/constraints on source audit. They cannot be stacked into a causal narrative without a versioned graph: `accession → original metadata → query → model/version/prompt/run → output → heuristic true label → model retrieval → TP/FP/FN → workbook cell/published figure`.

Reproducibility reviewer: source values and code pass checksum and falsification checks, but author execution not recreated.
Causal reviewer: neither metadata artifact inconsistency nor frame registration yields a measured AI-mediated standards-adoption pathway or loss of independently warranted H0/H1 options.
Originality reviewer: practical data lineage audit is worth preserving; independent EPISTEME mechanism remains defeated by strong existing standards economics/metadata quality explanations unless a new empirical residual is found.

**Research-go/no-go:** A08 gets first priority for authors' true execution manifest and independent unit/run identities; F01/F02/F05 receive the second priority for manuscript cohort selection and original Tcell/PIV settings. Keep paper and P78 on HOLD, S-BIAD602 independent causal case PAUSED, 19 active missing-evidence lines (F7/A7/B5) unchanged. Do not ask Work to redownload already acquired original ZIPs or TIFF gigabytes.
