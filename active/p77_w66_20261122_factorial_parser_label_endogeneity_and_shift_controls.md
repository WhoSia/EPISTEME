# EPISTEME-P77 W66 — Four-Policy Parser Court, Label-Endogeneity Diagnostics, and Deliberately Broken-Join Controls

**2026-11-22 KST.** [Notion scientific ledger](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385) is canonical. This audit tests an **already held original** [Sundaram et al. Zenodo v2/v3 Data.zip](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view) (3,992,768 bytes; SHA-256 `bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c`; ZIP CRC passed). No new source specimen, author run ID, model call, publication statistic or AI standard-adoption trajectory was acquired. [Machine-readable aggregate receipt](../analysis/p77_w66_aggregate_receipt.json) records all reported counts without raw participant records.

## Problem in W65 and W66 design

W65's strongest non-AI baseline changed **two factors simultaneously**: adding an alias lookup for `tissue_type` and trimming/case-folding the stored value. The W65 source exact selector was a public *example notebook*, **not** an authenticated original manuscript evaluation program. W66 resolves factor attribution without pretending the labels are independently grounded.

The factorial parameters are: (1) only original key `tissue` versus fallback `tissue_type` *when the original key is absent*; (2) original exact lowercased-query equality versus casefold+strip of stored text. This is a 2×2 deterministic comparison on unchanged original JSON. No ontological synonyms, inferred organs, new LLM calls or re-labeling.

For all three cohorts, available GPT4/Llama3/MedLlama layers, and two predetermined organ/blood queries, the released ZIP yields **56 layer/query evaluation cells**. Some are the repeated original BioSample object within multiple model files: **56 is not 56 independent tests or samples**. Alias alone changes a confusion table in **1/56 cells**, while value normalization alone changes **34/56**. Under 108 model-vs-source metric contrasts (precision/recall/F1), the original-vs-casefold branch has 2 strict relative-rank reversals (ovarian GPT4+CEDAR blood recall and F1); alias alone has 0 and combining alias with casefold still has 2.

| Ovarian blood query, positional 800-row heuristic labels | Original source F1 | GPT4+CEDAR F1 |
| --- | ---: | ---: |
| Exact `tissue` | 0.395833 | **0.647303** |
| Alias only | 0.395833 | **0.647303** |
| Casefold+strip on `tissue` only | **0.996743** | 0.774436 |
| Alias and casefold+strip | **0.996743** | 0.774436 |

The source has 154 released blood labels. The unchanged source records yield **38 exact true positives/38 retrieved** and **153 casefold true positives/153 retrieved** under that positional label pairing. GPT4+CEDAR yields **78 TP/87 retrieved** (exact) versus **103 TP/112 retrieved** (casefold). No assertion about authors' actual published F1, model quality, or biological correctness follows.

## New source-label *endogeneity* warning

All three released labels are **functionally consistent in-sample** with the original BioSample `tissue` value after trimming and casefolding: every repeated normalized value maps to exactly one released label.

| Cohort | Distinct normalized original tissue values | Values with conflicting released label | Rows having at least one other row with the same tissue value |
| --- | ---: | ---: | ---: |
| Liver | 89 | **0** | 725/800 |
| Lung | 73 | **0** | 766/800 |
| Ovarian | 49 | **0** | 780/800 |

This verifies a *within-released-artifact* relationship, **not** an identified causal label-generation procedure or gold-standard correctness. The original author `Rules.ipynb` already demonstrates deterministic `tissue`-based rule labeling for lung (W63: 800/800 rule recreation), making independent biological verification especially important. Same-value group consistency cannot infer accuracy on new tissue strings or person/subject independence.

## Bounded negative control — circularly break the original row joins

Shift the 800 released heuristic labels by each possible 0..799 cyclic offset while keeping original tissue values and model outputs fixed. This is **deliberately an invalid source-label join**, serving as a counterexample diagnostic, **not 800 independent replicates, a randomization-based p-value, or a confidence interval**.

- At the unshifted position, all three cohorts have **zero** conflicting labels among repeated normalized tissue values.
- Of the 799 other shifts, **none** reaches zero conflicts. The *minimum* number of minority-label rows within same-tissue groups is 172 (liver), 164 (lung) and 319 (ovarian).
- Yet the ovarian blood apparent rank reversal occurs under **794/800 shifts for recall** and **721/800 shifts for F1**, even when the real row–label correspondence has been intentionally destroyed.

**Important inference correction:** preservation of the observed rank reversal does not validate the row join; most invalid alignments also show it, because marginal retrieval set sizes and differing string-case policies can create the direction change. This weakens any W65 interpretation that would treat the reversal itself as evidence of successful semantic/biological information recovery. Conversely, unique zero-conflict original alignment supports a strong *recorded association*, not author manuscript-level provenance.

## Code, verification and falsifiers

- [W66 four-policy parser, label association and 800-shift control](../analysis/p77_w66_parser_factorial_and_label_court.py): loads actual pinned original ZIP with SHA+CRC, reuses W65's original file manifest/JSON stream parser, runs 4× evaluation controls and records aggregate TP/FP/FN without raw sample contents.
- [12 synthetic regression and mutation tests](../analysis/test_p77_w66_parser_factorial_and_label_court.py): case sensitivity, alias effect, missing keys, exact and normalized confusion, label collision, circular-shift marginal invariance, and fail-closed malformed data.
- [Aggregate result receipt](../analysis/p77_w66_aggregate_receipt.json): 56 cells, 108 contrasts, 2 strict value-only rank reversals, 3× circular-shift consistency, 794/800 and 721/800 negative-control reversal counts.
- The original held ZIP audit and **all 12 W66 local tests passed**; this is a direct local Python run against the true Google Drive byte copy, not a claimed GitHub Actions CI acceptance. The local W66 run used a mirror of the confirmed W65 manifest/parser source; the checked-in import path points to the original committed W65 module, and clean-clone test execution should be conducted as a further check.

## What would change the scientific verdict?

1. A08 original producer/annotation/evaluation run manifest with accession/row ID, exact actual heuristic or independent reference label origin, model version+prompt+run ID, original query parser and TP/FP/FN→workbook cell linkage. Without it, W65/W66 are deliberately conditional release-artifact diagnostics.
2. Independently verified biological tissue labels on a pre-registered sample, not labels derived from the same `BioSample.tissue` field against which preprocessing is scored. Explicitly test deterministic string/casing rules before attributing any result to AI semantic mediation.
3. For a truly novel EPISTEME mechanism, independently observed time-indexed collective standard choices and feasible rival H0/H1 scientific tests under comparable non-AI conversion; neither source-data auditing nor source-label functional consistency supplies these units.
4. Keep Figure 2E F01/F02/F05 subject and author production registration separate. More large TIFFs or an index listing alone do not identify group membership or time origins.

**Director decision (synchronized after Work's A09 admission):** Technical Research OS replay strengthened and W65 overinterpretation constrained. Work independently admitted A09's nine original review/manuscript PDFs, leaving **18 active missing evidence categories (F7/A6/B5)**. B10 1/2 and B11 2/3 are partial and remain open. P77 identity review ACTIVE, S-BIAD602 independent causal case PAUSED, P78 and PAPER HOLD; no independent philosophical novelty certified.

## W66 independent historical peer-review cross-check: baseline critique already existed

The now-held [Reviewer 2 original-submission report](https://drive.google.com/file/d/1ZWG3gxk8HaoynLhd3ZaLrEF793xbe-5L/view) explicitly raised, on page 1, whether the raw-metadata baseline was disadvantaged by lacking even basic stemming/linguistic normalization and asked how much of the approximate gold standard was manually reviewed. This was not a research concern newly invented in W65/W66. [Original manuscript page 7](https://drive.google.com/file/d/1HExlxx5ZZzBE4hAUDJPnefJYMQxrOLSY/view) gives a deterministic tissue keyword/precedence table to construct the approximate reference labels, and openly states that its search used exact string matching without substring, stemming, or synonym expansion. The [revised second submission](https://drive.google.com/file/d/1vQg-1h7cL65CpAt2UPi3VZRto7FAFFAE/view) retains the exact-match rule. The [author's original reviewer response](https://drive.google.com/file/d/1WwZnihkaUR4VaqO8m7s1adtyVcF1VrbC/view) thanks reviewer 2 generally, but does not provide a distinct new deterministic-normalization baseline table in that response; it separately describes added Figure/ANOVA and explanatory material for other reviewers.

**Historical interpretation:** The authors deliberately measured exact-match retrieval as one target task. Therefore W66's casefold comparator is a **sensitivity to evaluation-policy choice**, not proof that the paper's stated exact-match method was accidentally implemented incorrectly. The peer review raised this rival before publication and the source reference labels were themselves designed from source tissue strings; independent biological correctness and publication-run provenance remain separate gates. The only defensible novelty of W66 is the precise factorial/negative-control quantification on the public artifact, not discovering the general preprocessing objection itself.
