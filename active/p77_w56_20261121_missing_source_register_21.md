# P77 W56 — Current missing-source register: 21 evidence lines, audited 2026-11-21

**Current total: 21 ledger lines**; separate *original PDFs absent from Drive* from *specific historical run/manifests unlocated* and *public but not archived*. This supersedes the W55 **active** count of 23; W55's historical 23 is preserved as the state at that date. [Canonical Notion register](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385).

**Later custody readback:** The original PDFs are currently in the Research OS 10_PAPERS literature commons, not in the empty W56 project folder. Original IDs and sizes are unchanged.

**Newly resolved 2026-11-21:** B02 Moore et al. (2021) exact original DOI 10.1038/s41592-021-01326-w, Drive ID `1UoZL8vX1AtcZ55TfKLJHYxZKC_BM8Uvf`; B09 Gonçalves & Musen (2019) DOI 10.1038/sdata.2019.21, Drive ID `1bc3Lw6qJacO6Zgf5hNlWkoNYwhOsk0sH`. Original PDFs, not mere available online pages, confirmed in Research OS 00 and canonicalized into [Research OS 10_PAPERS](https://drive.google.com/drive/folders/1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP). [W56 original full-text verdict](p77_w56_20261121_ome_ngff_metadata_quality_two_original_prior_art_court.md).

## F — Existing Figure 2E technical replay and separate P77 causal reopening (7)
| ID | Missing evidence | Primary route | Direct use |
|---|---|---|---|
| F01 | Figure 2E mapping of all 16 embryos to manuscript arms and files, including exclusions | [S-BIAD602](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD602) | Figure-reproduction denominator |
| F02 | Authoritative embryo-specific t0, frame numbering, missing/excluded frames, measurement time anchor | [TwoPhoton archive](https://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/602/S-BIAD602/Files/DataRepository/TwoPhoton/) | Stop 30 s frame-alignment ambiguity |
| F03 | All embryo-specific origin/quadrant, D-cw/ccw, pixel scale, PIV and averaging settings actually used | [modelTissueFlow code](https://github.com/HiBandan/modelTissueFlow) | Original analysis correspondence |
| F04 | Original per-embryo per-frame velocity and Figure 2E analysis table | [Gehrels et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9963527/) | Independent Figure 2E group test |
| F05 | Exact original publication runtime and intermediate reference traces | [Open methodology comparator](https://doi.org/10.1111/jmi.70125) | Source-run reproduction |
| F06 | Time-stamped per-object ingestion/conversion/index-selection events | [Archive study API](https://www.ebi.ac.uk/biostudies/api/v1/studies/S-BIAD602/info) | Representation policy and access event timeline |
| F07 | Same scientists' observed route choice plus pre/post scientifically justified rival-test results and controls | [W53 decision](p77_w53_20261121_director_decision.md) | **Required** for independent causal P77 re-opening; an object inventory alone cannot fill it |

## A — AI-assisted biomedical harmonization replication/review records (9)
| ID | Missing or not yet held as original bytes | Public route | Specific gate |
|---|---|---|---|
| A02 | GenCDE exact release SHA, models/prompts/thresholds and evaluated 31-dataset snapshot | [Long code cited by authors](https://github.com/datatecnica/GenCDE) (GitHub API previously 404) | Original treatment / denominator |
| A03 | Long expert-edit decisions at sample/field level and adjudication protocol | [Long 2026](https://doi.org/10.1038/s41746-026-02795-z) | Reproduce 94% field-weighted no-edit figure |
| A04 | FAIRkit site use and subsequent community standard choices / independent test results for linked institutions | [CDE browser](https://cde-browser-809832168532.us-central1.run.app/) | True community/outcome link |
| A05 | Zenodo Sundaram v1 **Data.zip** original bytes not yet Drive-held | [Zenodo record 15617183](https://zenodo.org/records/15617183) | Inspect original-published revision |
| A06 | Zenodo Sundaram v2 and v3 **Data.zip** originals not yet Drive-held | [v2](https://zenodo.org/records/17516680) · [v3](https://zenodo.org/records/17555722) | Byte comparison and version drift |
| A08 | Exact accession/study/query/model join and original scripts behind the author workbook | [Sundaram 2026](https://doi.org/10.1093/gigascience/giag019) | True query-level analysis unit |
| A09 | Revision history, original submission, reviewer files and author responses, native bytes | [Publisher supplement](https://academic.oup.com/gigascience/article/doi/10.1093/gigascience/giag019/8504119#supplementary-data) | Investigate table/statistic corrections |
| A10 | Ikeda Table 4 exact MetaSRA evaluated input and runnable code/version | [Ikeda fork](https://github.com/sh-ikeda/MetaSRA-pipeline) | Published .903 vs saved .867 precision discrepancy |
| A12 | Exact MetaSRA ontology dumps, initial source snapshot, execution environment | [Original MetaSRA](https://github.com/deweylab/MetaSRA-pipeline) | Replay 206/422 records and mismatches |

## B — Non-AI literature and data/technical controls (5)
| ID | Missing original bytes / input identification | Source | Significance |
|---|---|---|---|
| B04 | Sheridan EXCHANGE Campaign 1 evaluator CSV, exact source version | [PNNL data](https://doi.org/10.15485/1960313) | Actual non-AI data context |
| B05 | Sheridan Global Soil Virus Atlas evaluator CSV, exact version | [PNNL data](https://doi.org/10.25584/2229733) | Same |
| B06 | Sheridan PNNL DataHub node 33553 evaluator CSV, original direct URL gave HTTP 400 | [Original cited path](https://data.pnnl.gov/group/nodes/dataset/33553) | Locate actual assessment file |
| B10 | Courtot et al. 2022 BioSamples and Davis & Meltzer 2007 GEOquery original PDFs (two separate PDFs under one legacy ID) | [BioSamples](https://doi.org/10.1093/nar/gkab1046) · [GEOquery](https://doi.org/10.1093/bioinformatics/btm254) | Biological specimen / series / sample grain |
| B11 | DataSHaPER 2011, Maelstrom 2017 and Rolland 2015 primary PDFs (3 separate works under one ID) | [DataSHaPER](https://doi.org/10.1093/ije/dyr106) · [Maelstrom](https://doi.org/10.1093/ije/dyw075) · [Rolland](https://pubmed.ncbi.nlm.nih.gov/26589709/) | Non-AI harmonization comparators |

**Never equate number of ledger lines with number of physical papers.** F=7, A=9, B=5, total=21 lines. B10 includes 2 papers, B11 3. The two 2019/2021 originals, seven W55 originals, past original PDFs and full CRI archive are HELD and must not reappear as missing.

## Fresh checks / negative results
- Direct folder enumeration of `00_INTAKE` found the two relevant PDFs plus unrelated assets; the remaining intake objects should not be forcibly classified or moved to EPISTEME.
- Targeted Drive metadata searches for `gkab1046`, `btm254`, `Maelstrom` and `DataSHaPER` did not find their originals in currently accessible results. **Search absence is not a proof of whole-Drive non-possession.**
- Source [Gonçalves & Musen 2019](https://doi.org/10.1038/sdata.2019.21) additionally points to a real [Figshare data release](https://doi.org/10.6084/m9.figshare.6890603) with 2017 validation records; this is an optional background resource for technical replication, **NOT a necessary new ledger line** or the missing 2026 joint causal sample.
- Verified original DOI/title/publication by direct PDF text and publisher/PubMed records. Raw hash comparison for today's metadata-only Drive moves not performed.

## Priority discipline
1. For a bounded **Research OS Figure 2E reproduction**, F01–F05 dominate; W54 shows a one-frame time sensitivity. Do not call four orientation projections four independent samples.
2. For **EPISTEME's founding independent causal identity**, F06–F07 + A04 dominate only if a dated real adoption event, treatment, same-unit hypothesis testing and equal-budget non-AI comparator can be obtained. More TIFF/Zarr visibility counts alone are not a promotion criterion.
3. A05–A06, A08, A10 clarify real metadata-analysis version/cell integrity; these are worthwhile **technical** studies, but even complete success would not identify Z→A→T.
4. B10/B11 are strong non-AI baselines; acquire only with priority after the causal access gate, not to inflate PDF intake. P77 ongoing, P78/PAPER HOLD.
