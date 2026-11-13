# EPISTEME-P77 W51 — Accession-Level Cellosaurus Replay, Comparator Code, and Literature Census

**2026-11-13 KST.** [P77 charter](../STRATEGY_P77_CURRENT.md) · [W50](p77_w50_20261113_author_workbook_reanalysis_and_matched_non_llm_control.md) · [Founding archive](https://drive.google.com/file/d/1kkTnpLUMpVgSdoW-IeTvQFVw-G5d9EPL/view). P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novelty uncertified.

## 1. Actual primary data and replay scope

[Ikeda et al. 2025, giaf070](https://doi.org/10.1093/gigascience/giaf070) · [Ikeda, Ohta, Oki & Zou, Zenodo v1](https://zenodo.org/records/14881142) · [raw files plus derived JSON in Drive](https://drive.google.com/drive/folders/1NucHNWKsfY2ZJyDTnQgpaofqnj36suA4). Zenodo labels the gold standard CC BY 4.0 and the other files CC0. All four publisher MD5 hashes matched independently materialized local bytes before upload. Drive file IDs, byte counts and parent were read back; the provider did not return a Drive-side checksum. No gene-extraction artifacts were pulled.

| Zenodo file role | Bytes | Local SHA-256 | Drive object |
|---|---:|---|---|
| Gold standard | 22,233 | 28b8fe71db19f71b4e769693336d46b806ee7cf266dd2a226da3148c120a8489 | [TSV](https://drive.google.com/file/d/1Q0lUt7rQENMWUa1dAYrMntFecLCO1B3e/view) |
| Direct MetaSRA output | 47,781 | cb2807b3fb461fa28c0afef60a9287360e5527c97f8aae049937a73540eb1540 | [TSV](https://drive.google.com/file/d/1svU0bQdurin4bd4FI5gnxSsxmXhxFklV/view) |
| LLM-assisted output | 577,624 | c397b39863521d82adec9d553149457a78bc25d7d1d0073650f3d8410ddbc63f | [TSV](https://drive.google.com/file/d/1NFvLqhIKmx00TZvCnoEiq0kS1Dg0zq_f/view) |
| Test metadata | 1,812,140 | 5610f429a669ee948e16559a5d8d8f75b89765b90d8a5c19209589a7d9298949 | [JSON](https://drive.google.com/file/d/1j_W06yP6ZkekkHTGucJrRViut4_XfZ2l/view) |

[Standard-library Python replay](../analysis/p77_w51_replay_cellosaurus.py). The four files contain the same 600 unique BioSample accessions and the result files repeat identical reference IDs for all 600. Table joins use accession keys. Reverse order gave identical output; duplicate and missing accessions were rejected. No explicit BioProject token was present in the test JSON, so the paper's within-assay study separation was not independently reconstructed. No models or full mapper were rerun. The metrics below are scores on saved authors' output. An independent execution of the authors' calc_test_values.awk after a column-only projection produced the same count and score vectors.

## 2. What the saved outputs demonstrate

| Saved-output policy | Exact accuracy | CVCL ID precision | CVCL ID recall |
|---|---:|---:|---:|
| Direct MetaSRA | 82.50% | 86.69% | 72.15% |
| LLM-assisted | 93.17% | 92.33% | 92.95% |
| MetaSRA first, use LLM output on blank | 91.83% | 88.35% | 91.61% |
| LLM first, use MetaSRA output on blank | 92.83% | 90.29% | 93.62% |
| Accept an ID only when the two agree | 83.50% | 93.81% | 71.14% |

Exact accuracy includes blank on blank. ID precision uses all emitted IDs; ID recall uses the 298 nonblank reference IDs. An incorrect ID is both a false positive prediction and a missed reference ID for these two rates, but counts once in exact accuracy. Of the 600, both matched the exact reference in 490, LLM-assisted alone in 69, MetaSRA alone in five and neither in 36. Direct MetaSRA missed 72 IDs and assigned 11 wrong IDs on records with a target; LLM-assisted missed 18 and assigned three wrong IDs. LLM-assisted alone remains the highest exact accuracy of the five tested policies. On this same archive, choosing strict agreement raises precision by 1.47 points against LLM-assisted alone at the cost of 21.81 recall points. The three post-hoc policies have no held-out deployment estimate; a fallback based on a saved blank is not a live cost/time measurement.

**Published vs archived metrics.** For direct MetaSRA, the published Table 4 gives .903 cell-line accuracy, .721 coverage, .782 blank precision and .937 blank recall. Applying its written metric definitions to the archived TSV yields .867, .721, .795 and .927 respectively. All four LLM-assisted quantities reproduce to published display precision (.923, .930, .940, .934). The difference may come from a different processing or output version; original table-generation inputs are required. The release’s TSV has a reference name with blank ID in 29 cases, and both methods emitted an ID on six of those cases each. Those are unmapped reference cases, rather than a trustworthy indication of no biological cell line. The gold TSV has 168 nonblank CVCL IDs on ChIP-Seq and 130 on ATAC-Seq, versus the article's prose arithmetic of 183−17=166 and 139−12=127. These are version/definition questions, not silent corrections to the published table.

## 3. Public implementations reviewed and transferred design choices

| Implementation / code inspected | What it contributes here |
|---|---|
| [Original MetaSRA](https://github.com/deweylab/MetaSRA-pipeline), run_pipeline.py, all_pipelines/pipeline_v53.py, pipeline_components.py, text_reasoning_graph.py | Filter fields, preserve source key/value and mapping paths, prioritize exact over fuzzy, distinguish explicit from inferred terms. The repo exposes two annotated JSONs. The public paper dataset has 422 accessions (209 records with explicit UBERON, 108 with consequent UBERON, groups can overlap). The 206 entries under analysis_data all match attribute payloads present in the public 422. Explicitly mapped term dictionaries matched on all 206, but consequent dictionaries differed in 62 and real-value properties in one. Treat the two as different annotation versions with overlapping observations. Never train on the 206 and report a test against all 422 as held-out. |
| [Ikeda MetaSRA fork](https://github.com/sh-ikeda/MetaSRA-pipeline), run_pipeline.py, and [bsllmner](https://github.com/sh-ikeda/bsllmner), main entry and evaluation scripts | Separate extraction, candidate generation and final selection; use explicit multiple-candidate outcomes. Author AWK independently reproduced archived ID precision/recall. The fork emits accession, original attribute, match type and consequent/full/exact flags. |
| [Musen Lab notebooks](https://github.com/musen-lab/FAIRMetadataCuration), metadata-refine.ipynb | The published example uses row-index linkage and an exact match in the target field. Replace positional joins with accession keys for our replay, report removed/duplicate IDs and retain source ordering only to audit authors' original alignment. |
| [EBI BioSamples](https://github.com/EBIBioSamples/biosamples-v4), CurationApplicationService and ZoomaService | Provider stores curation separately; application applies removal/addition deltas. Public original route is documented as `.json?curationdomain=`. The inspected ZoomaService is scoped to NCBI taxonomy, so a same-task UBERON alternative needs a verified different route and version. |
| [SSSOM schema](https://github.com/mapping-commons/sssom/blob/main/src/sssom_schema/schema/sssom_schema.yaml), [GEOquery getGEO](https://github.com/seandavi/GEOquery/blob/master/R/getGEO.R) | Keep mapping predicate, justification and version; do not merge exact with broad match. Keep GSM sample and GSE study identities distinct, plus platform where applicable. |
| [DataDesc/ioProc companion](https://github.com/dlr-ve-esy/modelcouplingworkflows), [OAEI Bio-ML](https://github.com/KRR-Oxford/OAEI-Bio-ML) | Specify input/output contracts and transformations; Bio-ML's distinction of equivalence and subsumption is a useful analogy. Ontology-to-ontology benchmarks cannot substitute for the same-record extraction task. |

Code fingerprints: original MetaSRA run `66e6e1bd63717486033fc6d6dce2e84f978484dc`, v53 `d3a7025cc66db8be10bb11c4a68770e17a169321`, graph `0ef5a56269765e3c87af1a92ce5c99ca10310300`; Ikeda fork run `cfc64ca6325cc3bfe2ff3f57b85a623591537a13`, author metrics AWK `bd87e3a2e0901e079456f054ffc095b7866896d6`; EBI application `4742a09067e823d974e24f62498ea596663493a8`; SSSOM `1eae923021ccca279be88e766d8892d97eda39cf`; GEOquery `f948626aa322e9f48283fb1072552e72ba390f6c`.

## 4. Reconnection to the research question

Held originals revisited: [Leonelli (2016), especially chapter 1](https://drive.google.com/file/d/1qPm83qmzIATx-n_uBxr1hf02vMIoMlb5/view) treats packaging, classification and curation as part of recontextualizing data; [Huvila et al. (2026)](https://drive.google.com/file/d/14_ZZAAvjK9puYcxbQsOUPPeB7GW_BFWj/view) compares which aspects of processes nine standards make representable and hence reusable; [Kuckertz et al. (2026)](https://drive.google.com/file/d/1ar_ViOI7pRjJbr8OsxCYPVwmOhqnA6Ba/view) documents reproducible shared transformations; [Bakeev (2026)](https://drive.google.com/file/d/1cV3Q42I9uE5Ek1LpFkNtJuqB9gXc4Tqy/view) explains why transfer can fail when epistemic standards differ. [Maelstrom guidelines](https://doi.org/10.1093/ije/dyw075) already tie valid harmonization to the research question before processing. More recall, representational loss, or domain acceptance alone therefore cannot be counted as an independent EPISTEME explanation.

First reproduce tissue retrieval with archived output and verified study/accession membership; then hold vocabulary release, mapping predicate, raw access, analyst time and reviewer rules fixed when comparing exact, scoped non-LLM, and LLM-assisted outputs. Use held-out study splits rather than sample-row randomization and distinguish no term, conflicting candidates, broad relation and confirmed match. For the founding question independently test whether conversion into the incumbent representation lowers local friction while changing which standard a community uses and which valid, pre-specified scientific test is actually feasible. A metadata failure that the available source-aware route repairs at the same budget is a negative control; a quality-equivalent mapping comparison must still observe standard choice and downstream test access. W51 adds evidence only to the measurement of translation.

## 5. Literature and material acquisition queue

[Notion W51 record](https://app.notion.com/p/417ef561cf92818299d5e9fb8f62190b). The [public MetaSRA 422-sample JSON](https://github.com/deweylab/MetaSRA-pipeline/blob/master/website/static/publication_datasets/test_set_ontology_mapping.json) and the [206-sample analysis JSON](https://drive.google.com/file/d/11KwBQeKNG7v2op4GhO5LiBfxvqRfNuKx/view) were copied byte-for-byte after matching their Git blob IDs. [Drive copy of the 422-sample file](https://drive.google.com/file/d/1M2-Cuf1LkrkGPuI4_MClI5y43duB1E3-/view). Official executable dependencies and a version-locked mapping replay are still outstanding.

| Priority | Source | Pending acquisition and use |
|---|---|---|
| 1 | [Sundaram Zenodo v1/v3](https://zenodo.org/records/17555722) | Original ZIPs, v3 workbook, accession/study-to-query mapping, GEO model/ANOVA inputs and output provenance. Archive listing still available; ZIP bytes not materialized. |
| 1 | [Long 2026](https://doi.org/10.1038/s41746-026-02795-z) | Supplementary PDF binary, original GenCDE release/run IDs, audit row counts, reviewer decisions and denominators. |
| 1 | [Ikeda 2025](https://doi.org/10.1093/gigascience/giaf070) | Main PDF, paper Table 4's original MetaSRA metric input and exact run configuration (incl. ontology versions), ChIP-Atlas study-to-accession manifest. Four original evaluation files are held. |
| 1 | [Bernstein, Doan & Dewey 2017](https://doi.org/10.1093/bioinformatics/btx334) | Original PDF and matched release/resources for executable MetaSRA; code and both annotation JSONs inspected; Git blob for public 422 set 80980e712328aeaf590fcefb688b8562872c846c. |
| 2 | [Bairoch 2018](https://doi.org/10.7171/jbt.18-2902-002); [Matentzoglu et al. 2022](https://doi.org/10.1093/database/baac035) | Cellosaurus identity/derivative and SSSOM relation/provenance papers; exact Cellosaurus release for replay. |
| 2 | [Gonçalves & Musen 2019](https://doi.org/10.1038/sdata.2019.21); [Courtot et al. 2022](https://doi.org/10.1093/nar/gkab1046); [Davis & Meltzer 2007](https://doi.org/10.1093/bioinformatics/btm254) | Metadata validity, raw/curated access and sample/study structure originals. |
| 2 | [Fortier et al. 2011](https://doi.org/10.1093/ije/dyr106); [Fortier et al. 2017](https://doi.org/10.1093/ije/dyw075); [Rolland et al. 2015](https://pubmed.ncbi.nlm.nih.gov/26589709/) | Existing harmonization feasibility, actual 53-study application and research-question-first selection. |
| 2 | [He et al. 2022](https://doi.org/10.1007/978-3-031-19433-7_33) | Bio-ML ontology matching resource paper and versioned benchmark as method reference. |
| 3 | [Ostropolets 2026](https://doi.org/10.2196/92727), [Sundaram 2026](https://doi.org/10.1093/gigascience/giag019), [PNNL report](https://doi.org/10.2172/3020608) | Publisher appendix, peer review packet and three exact CSV input versions, respectively. |

The September archive and held Leonelli, Leonelli–Tempini, Huvila, Kuckertz, Bakeev are excluded from the missing-original queue. Public links and targeted Drive search results cannot prove library-wide absence.
