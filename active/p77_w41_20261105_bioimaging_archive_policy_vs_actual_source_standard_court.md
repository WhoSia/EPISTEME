# EPISTEME-P77 W41 — Same Bioimaging Ecosystem, Different Format Policies: BIA, IDR and the Joint Infrastructure

**Date:** 2026-11-05 KST. [P77 current](../STRATEGY_P77_CURRENT.md), [G-001](../GOVERNANCE.md). **Previous:** [W39 three original PDFs](p77_w39_20261105_three_publisher_originals_full_read_and_custody_court.md), [W40 author-measured institutional integration](p77_w40_20261105_new_bioimage_archive_2026_actual_integration_cohorts.md). **Decision:** P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novelty not certified.

## 1. Real, current institutional policies (verified on actual official sites)

**EMBL-EBI BioImage Archive** [Zarr submissions official documentation](https://www.ebi.ac.uk/bioimage-archive/help-zarr/) explicitly calls OME-Zarr support **alpha** (policy can change) and describes zipped `.ome.zarr.zip` submissions, explicit file-size and validation guidance. [BIA official format FAQ](https://www.ebi.ac.uk/bioimage-archive/help-faq/) says multiple microscopy imaging formats can be accepted, preferring formats handled by Bio-Formats. These pages establish format *intake support*, not the distribution of actual archives or scientifically valid converted results.

**EMBL-EBI Image Data Resource (IDR)** [official current IDR landing page](https://idr.openmicroscopy.org/tissue/) states a **transition** to OME-Zarr for improved performance/access; **all new IDR studies must be submitted in OME-Zarr format**, while old images in other formats can still be downloaded for local viewing, thumbnails are served during transition, and all studies are being converted. This is a **documented policy** as observed at W41, not proof of every contributor's actual compliance or completed migration.

**EMBL-EBI BIA+EMPIAR joint infrastructure** [Zulueta-Coarasa et al. 2026 official journal source](https://doi.org/10.1093/nar/gkag1108), published today, reports raw deposited files retained unchanged and deterministic `bioformats2raw` access-format conversion. Unified submission was *under development* during Q3 2026; specific ingestion and streaming coverage counts from 2026-06-30 appear in [W40](p77_w40_20261105_new_bioimage_archive_2026_actual_integration_cohorts.md).

These findings **are not policy contradictions**: BIA, IDR, and future joint systems have different missions and separate submission/curation routes. Do not merge BIA accepting all formats with IDR requiring OME-Zarr for new selected studies into a single nationwide policy or claim time-series replacement occurred uniformly.

## 2. Original code-level baseline exists, without AI intervention

Source code [BioImage-Archive/bia-zarr](https://github.com/BioImage-Archive/bia-zarr) README actually fetched through installed GitHub connector; source blob `8c101d301ed2048ff6b288fef1053fe3cd90aa9d`. Supports Zarr v2/v3 utilities, OME NGFF metadata objects, thumbnail/array manipulation, `open_ome_zarr_image`, version/model checks. This repository is an **existing non-LLM scientific data-processing baseline**. Source README provides API/function descriptions; W41 did **not** run the package against real scientific images or independently certify numerical/epistemic fidelity. No hidden assumption that metadata validation automatically validates an experiment's inferential assumptions.

Other existing strong baselines remain `bioformats2raw` (Moore 2023 and Zulueta-Coarasa 2026), DataDesc/ioProc (Kuckertz 2026), existing Huvila 2026 standard process representation models, and network standards adoption economics.

## 3. Research question identification: declared policy ≠ behavior ≠ scientific testing

We must distinguish at least:
- **P**: a documented institution's format requirement or recommendation (dated archived policy, not immutable).
- **S**: the original raw source format maintained in actual storage (checksum, lineage, persistence).
- **X**: access-format versions served (transient caches vs persistent derived copies).
- **D**: actual experimental processing/analysis input and toolchain (not advertised compatibility).
- **V**: automated standard conformance + independently adjudicated scientific meaning/provenance and valid test interpretation.
- **Z**: an assigned, versioned LLM/AI **conversion treatment**, with strong original deterministic/manual comparator, equal review, cost and expertise.
- **T**: actually available and accepted substantive H0/H1 discriminating tests, including any affordable alternate access route.

**A policy P is not an observation of S or D**, an entry indexed in a new catalogue is not a converted image count, and an image accessible as OME-Zarr is not a guarantee that a hypothesis has become admissibly testable. IDR's OME-Zarr policy and BIA's alpha submission support can simultaneously be true.

## 4. Better actual data project than another illustrative formula

We now have the first real infrastructure cohort counts and identified authoritative institutional metadata. A bounded follow-up could query accession-level BIA/EMPIAR versioned public records to construct dates, original submission format, hashed raw files, converted OME-Zarr availability, converter versions, and user analysis events **if actually exposed**. The raw public API would require data rights/scope review and a reproducible census, not scraping personal information.

To test `Z→A→T` causally, an independently documented AI vs deterministic conversion rollout with time-ordered interacting laboratories and measured test repertoire is still absent. Even complete descriptive accession histories would identify *format infrastructure diffusion*, not an AI-induced lost scientific test. Prospective experiments require appropriate study governance and separate human/organizational ethics if researchers are recruited.

## 5. Decision and source debt

W40 and W41 provide a genuine real-world testbed **for description and source inventory**, but no independent theoretical novelty. Existing original researchers already explain preservation of original deposit bytes + conversion to derived accessible representation. Any user-facing conclusion must include this fatal competitor.

**Original new NAR gkag1108 publisher PDF** is not yet independently held in user's Google Drive (HTML publisher full text and official table figures read). The three requested original publishers' PDFs and the ZIP source are now held in canonical original-science locations; do not ask them again.

**P77 ACTIVE / P78 HOLD / PAPER HOLD / TLP causal effect NOT IDENTIFIED; novelty NOT CERTIFIED.**
