# EPISTEME-P77 W40 — First Measured Institutional Format-Access Integration Cohorts: BIA/EMPIAR 2026, Correct Denominators and Temporal Status

**Date:** 2026-11-05 KST. [P77 binding charter](../STRATEGY_P77_CURRENT.md) · [G-001](../GOVERNANCE.md). **Decision:** P77 ACTIVE, P78 HOLD, PAPER HOLD; founding causal TLP **NOT IDENTIFIED**, independent novelty NOT CERTIFIED. **Parent source court:** [W39 actual original PDFs](p77_w39_20261105_three_publisher_originals_full_read_and_custody_court.md), [W37 observed vs planned standard adoption](p77_w37_20261105_science_format_adoption_archival_vs_access_court.md).

## 1. A genuinely new source published TODAY, verified exact publication and historical as-of dates

**Teresa Zulueta-Coarasa et al. (2026),** *BioImage Archive: bringing bioimaging data together*, *Nucleic Acids Research*, database issue advance article **gkag1108**, published **2026-11-05**, DOI [10.1093/nar/gkag1108](https://doi.org/10.1093/nar/gkag1108). [Original Oxford published article and methodological details](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkag1108/9013049), [official date in journal advance articles](https://academic.oup.com/nar/advance-articles).

**DO NOT confuse paper publication on 2026-11-05 with its snapshot AS OF 2026-06-30.** The original author article measures BIA and EMPIAR holdings and upgraded infrastructure adoption as of June 30; future milestones are plans (not yet fulfilled even when paper is published).

## 2. Real measured numbers, with observation grain

As of **2026-06-30**, authors report:
- **BioImage Archive/BioStudies:** 1,477 total released accession **entries**, **1,396 entries** available in upgraded image-centered infrastructure. Exact denominator share **1396/1477 = 94.5159%**. These are **entries indexed in a unified infrastructure**, not 94.5% of stored raw image files rewritten to a new canonical archival format. Authors note those covered are released before May 2026.
- **EMPIAR:** 3,019 released accession **entries**, **508 entries** in upgraded infrastructure, **508/3019 = 16.8268%**. Different deposit/submission/curation route.
- **Converted image objects:** **more than 25,000 distinct images** transformed for OME-Zarr visualization/streaming by the new infrastructure (different unit, not 25,000 accessions or laboratories).
- **Source total volumes:** 1.19PB BIA and 9.92PB EMPIAR in the author snapshot; the abstract describes >11PB combined historical scientific data. Do not treat those volumes as converted OME-Zarr volumes or as counts of experiments.
- Actual conversion pipeline is **Bio-Formats' deterministic bioformats2raw**, RO-Crate package metadata, MongoDB and existing source files. The source explicitly says originally deposited data files are **not altered**; derived OME-Zarr stored on public S3 with metadata returned to the database. **No assigned LLM/AI scientific-format converter treatment** is described.

**Independent source-record audit executable:** [analysis/p77_w40_bia_actual_integration_denominator_audit.py](../analysis/p77_w40_bia_actual_integration_denominator_audit.py). A locally run independent implementation checked the source numbers; it does **not** fetch the BIA live API or prove a causal explanation.

Actual local printed source check:
```
SOURCE_ENTRY_FRACTION 2026-06-30 BioImage Archive / BioStudies: 1396/1477 = 94.516%
SOURCE_ENTRY_FRACTION 2026-06-30 EMPIAR: 508/3019 = 16.827%
SOURCE_IMAGE_COUNT: >25,000 converted scientific images (not entries)
SOURCE_AUTHOR_FUTURE_TARGETS (not observed outcomes): {'all_legacy_entries_ingested': '2026-12', '70_percent_images_converted': '2027-03', 'unified_submission_target': '2027-mid'}
NO-GO: these counts identify ingestion and conversion operations, not AI-treated laboratory choices or H0/H1 test feasibility
```

## 3. Documented vs forthcoming source architecture

**Actually described:** BioStudies and EMPIAR separate deposition routes coexist; archive retains original submitted data; RO-Crate metadata, existing bioformats2raw conversion and OME-Zarr access transformation support the new cross-resource image-centric representation. This is the actual published institutional operation, not EPISTEME's future proposal.

**Author FUTURE milestones (do not present as achieved):**
- Bring all old published entries into new infrastructure, **target December 2026**.
- Convert **70% of images** into streaming-compatible OME-Zarr, **target March 2027**.
- Unified submission replacement, **target middle of 2027**; testing programmatic submission during 2026.
These are stated author targets from current November 2026 article and may change.

**Epistemic caveat:** the same scientific image may be archived unchanged yet served as OME-Zarr. Thus repository-level *entries indexed* and *images converted* indicate increasing access interoperability, not migration of source storage format. This directly supports the S (archive) / X (access) / D (actual analysis) separation already stated in W37 and **already addressed by original BIA scientists**, not a newly discovered principle.

## 4. True scientific-evidence limitation and rivals

The authors describe reanalysis/reuse cases and methodological reproducibility work but **do not report independent blinded correctness of all converted scientific measurements, AI conversion treatment assignment, or a panel of scientific laboratories adopting standards with time-varying test capabilities**. Publication/reuse counts and increased downloads cannot be equated with a growing set of scientifically justified H0/H1 hypothesis tests. Deep-learning demand for images is not evidence of an *AI translator* treatment.

Strong already established rivals: **source Kuckertz 2026** machine-readable deterministic DataDesc/ioProc workflow mapping, **Huvila 2026** standards' paradata affordances, **Moore 2023** temporary OME-Zarr access copies, conventional format maturity and cloud I/O, existing OME bioformats2raw, network effects standards economics. A full future claim must withstand these.

## 5. New observational data opportunity: bounded, not yet obtained

Institutional accession IDs, deposit date, original format hash/types, validated derived-format availability and conversion processing dates could support a **descriptive time-series uptake audit**. The actual publication mentions a public API and planned expansion. But authors' cumulative entry counts are currently only one historical aggregate snapshot with mention of growth charts, **not a downloaded panel**. A properly controlled test requires actual per-entry event timestamps, versioned converter deployment and independent hypothesis-specific inference; a scientific-community adoption causal effect will **not** emerge from the 1396/508 ratios alone.

**No original publisher NAR 2026 PDF was located in user's Drive at this W40 audit**; source published full HTML and DOI are already accessible. Add this newly published PDF to the missing-source ledger only if full original PDF custody desired. The three user-supplied W39 publisher PDFs are all now safely in `10_PAPERS`; do NOT ask for them again.

**Decision:** measured real **institutional infrastructure ingestions**, not AI-caused standards entrenchment nor scientific H0/H1 testability. **P77 ACTIVE / P78 HOLD / PAPER HOLD**.
