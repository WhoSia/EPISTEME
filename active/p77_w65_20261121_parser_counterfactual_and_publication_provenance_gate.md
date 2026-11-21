# EPISTEME-P77 W65 — Query Parser Sensitivity and Source-Ranking Reversal Court

2026-11-21. **This is a conditional source-artifact analysis, not an author manuscript-run reproduction or an independent EPISTEME standard-adoption causal estimate.** [Notion W65 evidence and latest 19-item missing register](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385) is the scientific semantic authority.

## Sources and calculations

Original [Sundaram Zenodo v2/v3 Data.zip](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view), 3,992,768 B, SHA256 bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c; actual ZIP CRC and original 800-row cohort/model JSON plus annotated_800_simple_liver/lung/ovary.txt lines verified. The author [historical metadata-refine.ipynb](https://github.com/musen-lab/FAIRMetadataCuration/blob/fcc91cc321c649fd96895eb435e978fb57d00acc/metadata-refine.ipynb) performs exact equality on dictionary key tissue against the query lowercased, without a tissue_type alias or normalization of stored values. It is **an example notebook**, not the confirmed program that generated manuscript statistics. We assume row position links all 800 released predictions to their heuristic text labels; that binding has not been validated against accession-level provenance or independent gold truth.

Three candidate parsers were applied to each exact query: original exact tissue key/value; exact value with tissue_type fallback; and fallback plus trimming/casefold of stored values. We **did not** add ontology synonyms, inferred correct tissue, new LLM responses or optimally chosen query strings. Queries were fixed to the named organ and blood in each original cohort.

## Key original-data results

| Ovarian 800-row retrieval | Original exact F1 | Case-folded/trimmed F1 |
| --- | ---: | ---: |
| BioSample organ=ovary | 0.0798 | 0.4376 |
| GPT4 LLM organ=ovary | 0.0875 | 0.4444 |
| GPT4 CEDAR organ=ovary | 0.7618 | 0.8815 |
| BioSample blood | 0.3958 | 0.9967 |
| GPT4 CEDAR blood | 0.6473 | 0.7744 |

Released heuristic ovarian labels: 457 ovary / 154 blood / 30 plasma / 159 unknown. For original BioSample blood: exact equality 38 TP, 38 retrieved; normalized 153 TP, 153 retrieved. For GPT4 CEDAR blood: exact 78 TP / 87 retrieved; normalized 103 TP / 112 retrieved. Thus **the direction of the apparent retrieval advantage reverses under a deterministic non-AI parser change**. This is a conditional replay result, not a claim that such normalization was absent from the authors' actual statistical implementation.

Over all 3 cohorts, available model/layer combinations, two predeclared queries, three metrics (precision, recall, F1), and source-vs-model comparisons, **108 metric comparisons yielded 2 strict sign reversals**: both ovarian GPT4 CEDAR vs original BioSample for blood, in recall and F1. Ties do not count as reversal.

## Reproducible technical assets

- [Three-parser original-input replay](https://github.com/WhoSia/EPISTEME/blob/main/analysis/p77_w65_query_parser_sensitivity.py) and [9 fail-closed synthetic tests](https://github.com/WhoSia/EPISTEME/blob/main/analysis/test_p77_w65_query_parser_sensitivity.py)
- [Strict pairwise reversal detector](https://github.com/WhoSia/EPISTEME/blob/main/analysis/p77_w65_rank_reversal_court.py) and [4 tests](https://github.com/WhoSia/EPISTEME/blob/main/analysis/test_p77_w65_rank_reversal_court.py)
- [Seven-edge paper provenance admission gate](https://github.com/WhoSia/EPISTEME/blob/main/analysis/p77_w65_provenance_gate.py) and [7 tests](https://github.com/WhoSia/EPISTEME/blob/main/analysis/test_p77_w65_provenance_gate.py). An original ZIP hash or static notebook source does not satisfy missing input-to-invocation-to-output-to-query-to-confusion-to-workbook-to-paper edges. This is a schema gate only; successful claims still need independent artifact/run checks.

The exact archived ZIP was processed locally and passed original-source hash and CRC checks. Local equivalent implementation tests for parser and reversal calculations plus provenance gate passed (19 tests); repository version includes an additional missing-query synthetic test and clean-clone execution should be verified before describing the checked-in test files as independently CI-passed. No model calls or actual published statistical replication occurred.

## Scientific decision

**Primary strong rival:** non-AI string/field preprocessing substantially changes what is retrievable under fixed metadata and heuristic labels; apparent improvement from rewritten metadata cannot be attributed to AI semantic translation alone unless the author production evaluator's normalization and independent labels are fixed. The actual statistical run, 6 independent run IDs, input accession-to-row-to-label map, TP/FP/FN provenance and paper cell mapping remain unidentified (A08 OPEN). Evidence could falsify this rival if the real publication evaluator already normalized these values or independent labels do not agree with released text.

Preserve as Research OS evaluation-method evidence; **do not** conclude corrected paper F1, biological ground truth, scientific-standards adoption, or independent philosophical novelty. P77 identity REVIEW ACTIVE, S-BIAD602 standalone causal case PAUSED, P78/PAPER HOLD, active missing **19 categories (F7,A7,B5)**.

Procurement is split into truly downloadable official papers/review packets (A09, B10, B11), candidate PNNL CSV data (B04-B06), and author-only execution/cohort/epistemic records (F01-F07, A02-A04,A08,A10,A12). A similarly named generic PDF must not be used to falsely close an exact original execution artifact.
