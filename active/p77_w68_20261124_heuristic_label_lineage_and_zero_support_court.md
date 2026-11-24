# EPISTEME-P77 W68 — Heuristic Label Rule Reconstruction and Zero-Support Retrieval Audit

2026-11-24 KST. [Canonical Notion research ledger](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385). P77 identity review active; P78/PAPER HOLD. This round reuses authenticated source artifacts and narrows A08; it does not identify the authors' production run or establish independent biological ground truth.

## 1. Pinned inputs and rule reconstruction

- [Held original Zenodo Data.zip v2/v3](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view), 3,992,768 B, SHA256 bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c; actual local SHA and ZIP CRC verified.
- [Original author workbook](https://drive.google.com/file/d/1iT7YVcGanPuxbjjHgiOlYxONe-KMusDw/view), 29,533 B, SHA256 3c95456d42326dba210c0943489988895ffeba2ac09eb3d0e84124e54fcfb935; actual local bytes verified.
- [Pinned author Rules.ipynb, 2025-06-07](https://github.com/musen-lab/FAIRMetadataCuration/blob/fcc91cc321c649fd96895eb435e978fb57d00acc/Rules.ipynb), fetched via GitHub. Its executable lung branch lowercases tissue, tests uppercase PBMC literally, and prioritizes lymph over plasma. The commented ovarian branch prioritizes plasma over blood. Its commented liver condition tests uppercase HCC against the lowercased value.
- [R2 original](https://drive.google.com/file/d/1vQg-1h7cL65CpAt2UPi3VZRto7FAFFAE/view), Table 2: stated keyword order lung, liver/HCC, ovary/ovarian, PBMC/blood, plasma, lymph. "Contains the word" does not unambiguously specify substring vs word-boundary behavior, so both interpretations were evaluated without claiming a production implementation.

| Cohort | Case-insensitive substring interpretation | Whole-word interpretation | Historically motivated candidate |
| --- | ---: | ---: | ---: |
| BioSample liver | 700/800 | 762/800 | 800/800 |
| BioSample lung | 800/800 | 792/800 | 800/800 |
| BioSample ovarian | 794/800 | 794/800 | 800/800 |
| GEO lung | 800/800 | 800/800 | 800/800 |
| GEO ovarian | 800/800 | 800/800 | 800/800 |
| GEO liver | expected named label file absent | not evaluated | not evaluated |

In BioSample liver the case-insensitive substring interpretation differs in 100 rows: 62 predicted blood and 38 predicted liver that the release labels call unknown. The historically motivated reconstruction matches all 800; this does not prove that the case-sensitive acronyms were the sole production cause. In BioSample ovarian 6 predicted blood rows are labeled plasma; the candidate using the commented ovarian precedence matches all 800. Only lung has a directly attested executable historical branch; liver and ovarian are reconstructions, chosen after inspecting source and labels. The two GEO cohorts use the stated rule itself, not an attested historical GEO rule. All comparisons assume positional pairing. These are 4,000/4,000 in-sample released-label reproductions, not independent biological validation. The corresponding named liver GEO label member is absent from the archive; other possible representations are not ruled out.

The rule-derived comparator therefore attains 1.0 on all nine supported organ/blood tasks against these same labels. This is a circular reference replay, not a fair scientific predictive benchmark or proof that a non-AI system is superior. It is a diagnostic of the reference's dependence on the source tissue field. Independent accession-keyed tissue labels remain necessary.

## 2. Zero-positive GEO ovarian blood query

In the held GEO ovarian label file, blood positives=0. The original, LLM and LLM+CEDAR output layers each have 0 exact blood retrievals. Recall is mathematically undefined, not a measured zero. The workbook geo-gpt4!G5:G7 contains three literal zeros. The sheet title says GPT-4 but its rows say Llama3+DD / Llama3+CEDAR; do not silently resolve that ambiguity. The published provenance link remains missing. A zero-fill convention can be explicit, but changes the estimand and deserves disclosure.

Read the exact XLSX with artifact_tool and extract recall columns C/G from rows (5,6,7), (18,19,20), (26,27,28). Compute a one-factor subject-blocked RM-ANOVA and tie-corrected Friedman test, then omit the ovarian blood all-zero row as a support-aware sensitivity, not a paper correction:

| Quantity | Six displayed task triples | Five supported triples (conditional omission) |
| --- | ---: | ---: |
| Raw/source mean recall | .1490460 | .1788552 |
| DD mean recall | .0204678 | .0245614 |
| CEDAR mean recall | .4400472 | .5280566 |
| F | 2.7402473 | 2.9544773 |
| df | 2,10 | 2,8 |
| p | .11248014 | .10944149 |
| Friedman statistic | 4.5882353 | 4.5882353 |
| Friedman p | .10085034 | .10085034 |

The unchanged Friedman value agrees to rounding with the reported GEO statistic 4.59, whereas the RM-ANOVA still does not recover the reported F≈1.08. This is a partial numerical correspondence, not proof of the same source matrix. Omitting a completely tied zero-support block leaves the Friedman statistic unchanged here and changes macro means and degrees of freedom. Neither ANOVA result is significant at .05. The five retained workbook rows are not independently verified as the manuscript's statistical subjects, nor are all five confirmed to have positive ground-truth counts: the liver GEO label is missing.

## 3. Technical reproducibility and scope

[Rule replay](../analysis/p77_w68_label_rule_replay.py), [seven tests](../analysis/test_p77_w68_label_rule_replay.py), [zero-support audit](../analysis/p77_w68_zero_support_statistics.py), [three tests](../analysis/test_p77_w68_zero_support_statistics.py), [aggregate receipt](../analysis/p77_w68_rule_and_zero_support_receipt.json). Actual source inputs verified and both scripts executed locally; 10 local mirror tests passed. No GitHub Actions run or original author model execution performed.

## 4. Research director decision and next stage

The result narrows A08 to three specific evidence requests: (a) the original exact label generator, including liver/ovarian precedence and acronym handling and missing liver GEO labels; (b) per-query TP/FP/FN and explicit zero-support metric convention; (c) the original 6x3 statistical inputs and model/run/cell identities. A09 remains closed; B10/B11 remain partial. Current ledger last checked: 18 open categories F7/A6/B5. No further general file collection is justified merely to inflate source counts.

Scientific bridge: an evaluation reference constructed from source metadata cannot independently establish that a transformation improves scientific correctness. Equally, discovering correct tissue labels does not establish community standard adoption or a newly permissible scientific test. Separate (i) representation fidelity, (ii) query support, (iii) actual adoption, and (iv) feasibility of a pre-specified scientific contrast. For the next independent case, require a pair of standard representations over the same source material, a pre-registered scientific test that is executable in one representation and not in the other, and an observed community choice with AI exposure distinguished from deterministic conversion. The proposed separation is a design criterion, not an original theorem or discovered effect. P77 identity REVIEW ACTIVE, S-BIAD602 standalone causal case PAUSED, P78/PAPER HOLD.
