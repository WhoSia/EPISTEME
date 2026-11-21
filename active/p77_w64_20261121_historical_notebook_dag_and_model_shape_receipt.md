# EPISTEME-P77 W64 — Historical Author Notebook Path Audit and Release Shape Witness

**2026-11-21 KST. Research meaning and active 19-line missing ledger are in [Notion W64](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385).** This is a bounded technical receipt, not evidence that the audited notebooks were used for the author's published statistics.

## Sources and exact historical provenance

- Original author repository: [musen-lab/FAIRMetadataCuration](https://github.com/musen-lab/FAIRMetadataCuration), [pinned 2025-06-07 commit `fcc91cc321c649fd96895eb435e978fb57d00acc`](https://github.com/musen-lab/FAIRMetadataCuration/tree/fcc91cc321c649fd96895eb435e978fb57d00acc).
- Five original notebook files have Git blob SHA identical at the pinned commit and 2026-11-21 HEAD `248bbc3595a8979aec6d155452421a659245bc8a`, as checked through GitHub's original content API. All distributed code cells have `execution_count:null` and `outputs:[]`. **That does not prove the notebooks were never run**, because saved execution outputs can be cleared before committing.
- Actual held [Zenodo v2/v3 original ZIP](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view), 3,992,768 B, SHA-256 `bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c`, reopened locally and CRC-checked. Work W63 previously verified the ZIP's 33 research payload files byte-match the 2025-06-07 Git Data directory. This does not attach a run ID to statistical outputs.

## Static DAG anomaly #1 — GEO generator selector vs name

`GEODatasetGenerator.ipynb` source contains:
- `if 'liver cancer' in d['title']`
- `random_samples = random.sample(final_data, 800)` without any fixed random seed in the distributed code
- `with open('ovarian_cancer_geo.json', 'w')`

That means the *visible code path* filters liver-titled source records but names its output as ovarian. Actual held ZIP JSON `Data/ovarian_cancer_geo.json` instead has **800/800** titles containing `ovarian cancer` and **0/800** containing `liver cancer`. Its liver and lung original JSONs have 800/800 corresponding title terms (and none of the other two); verified using [original-source title audit](../analysis/p77_w64_geo_title_crosscheck.py) with [five passing tests](../analysis/test_p77_w64_geo_title_crosscheck.py). Titles in the parsed listing and later re-fetched GEO dataset are two steps: no verified GSE-title join exists across them, so this contrast cannot by itself prove what generator was run for the held file. Study-title words are not gold truth.

## Static DAG anomaly #2 — MedLlama authored CEDAR branch not selected for final output

`MetadataCorrection.ipynb` separately calculates `llm_cedar_samples.append(eval(ans))` from an ontology-constrained prompt. The final archived-record assembly uses `dict_sample['LLM+CEDAR'] = cedar_samples[i]`, a *different array* from a simpler prompt-generated branch, instead of `llm_cedar_samples[i]`. Thus the long ontology-constrained branch has no direct edge to final `LLM+CEDAR` export in the visible notebook sequence. This is an exact **static data-flow defect/candidate**, not proof that the authors' actually published CEDAR results were computed with it.

**Independent release shape witness:** all **4,800** released MedLlama dictionary objects (three cancer cohorts × 800 source rows × LLM and LLM+CEDAR layers) have **0 or 1** key. Zero/one-key counts:
- Liver LLM: 309/491; liver CEDAR: 198/602.
- Lung LLM: 299/501; lung CEDAR: 184/616.
- Ovarian LLM: 334/466; ovarian CEDAR: 242/558.
- Contrast: ovarian GPT-4 CEDAR **800/800 have at least two keys**.

These numbers were obtained by re-reading and running [original ZIP shape audit](../analysis/p77_w64_output_shape_fingerprint.py) with [five passing synthetic regression tests](../analysis/test_p77_w64_output_shape_fingerprint.py). They are structurally compatible with the MedLlama simple one-field output construction, but many different programs could produce such dictionaries. **Shape matching is not historical execution identity**, let alone semantic label accuracy.

## Negative control and implementation fix

`MetadataCorrection-gpt.ipynb` has an initial `llm_samples` array of pre-existing responses, **then explicitly resets it with `llm_samples=[]` before appending new LLM outputs**. Therefore it cannot be criticized with the same "old array necessarily exported" mechanism under the actual shown order. Our first static scanner counted an earlier empty-array initialization as an adequate reset, allowing a false positive under deletion of the later reset. [W64 negative-control correction](../analysis/p77_w64_notebook_lineage_court.py) now requires a reset **between the old-response append and the new-response append**. The intentionally mutated synthetic test caught this bug; after correction [10/10 tests](../analysis/test_p77_w64_notebook_lineage_court.py) pass.

Other already-established examples remain bounded: `metadata-refine.ipynb` runs `blood` searches against `ovary` truth in one cell; `Rules.ipynb` lowercases input and later tests uppercase `PBMC`. Those are examples of publicly distributed notebook code, not manuscript run receipts.

## Exact execution scope

- Historical 5/5 author notebook source and blob metadata inspected through GitHub connector; static source assertions checked directly. Standalone [notebook lineage auditor](../analysis/p77_w64_notebook_lineage_court.py) validates pinned Git blob byte hashes when run against an actual local clone; **its full clone-based CLI was not run in this Chat**. Its 10 synthetic tests were run locally and passed after scanner fix.
- Actual Zenodo original ZIP re-opened and both GEO title and output shape scripts executed successfully. Their respective 5+5 regression tests were run. **Total W64 regression tests: 20/20 passed**.
- No LLM calls, independent statistical-run manifest, author Figure 2E PIV or paper t-tests were executed.
- Work W63 candidate cta 20 mask files are only verified as directory listings; scientific panel selection and exact original Tcell anchor remain unverified.

## Adjudication and next evidence

**A08 remains incomplete**: historical code and data can be byte-identified, and distinct source-level hazards exist, but neither directly traces `accession → input → prompt/model version/run ID → row-level predicted tissue → heuristic gold label → query TP/FP/FN → XLSX cell → manuscript statistic`. An actual dated execution/analysis manifest or independently linked raw benchmark table is required. Under missing run provenance, one world in which the released data is *production input* and another where it is a *post hoc archive export* are observationally consistent with what is currently held. No correction of the authors' published numerical values is scientifically justified.

F01/F02/F05 require actual Figure 2E 16-subject membership, biology-to-frame registration, PIV versions and original analyses; do not substitute cta candidate file listings. F06/F07/A04 require true AI-adoption-to-standard-to-test record before independent EPISTEME promotion. **P77 REVIEW ACTIVE / S-BIAD602 standalone causal PAUSED / P78 and PAPER HOLD, missing 19 (F7/A7/B5).**
