# EPISTEME-P77 W44 — An Identifiability Court: API Visibility Selection, Missing Original-Image Denominators and the TLP Stop Rule

**Observed and adjudicated 2026-11-09 KST.** [P77 binding charter](../STRATEGY_P77_CURRENT.md), [W42 real API](p77_w42_20261109_live_bia_openapi_and_original_accession_contract.md), [W43 source snapshot + negative controls](p77_w43_20261109_actual_bia_paired_image_api_negative_controls.md).

## The inferential object and a known censoring mechanism

Original institutional article [Zulueta-Coarasa et al. (2026), BioImage Archive: bringing bioimaging data together](https://doi.org/10.1093/nar/gkag1108), published 2026-11-05, states that **only images converted into OME-Zarr can be searched through the new image API and website**. This author-provided operational limitation makes a 100% conversion share **among API-visible image hits** essentially a consequence of the index's selection rule, not evidence that all physically archived images have been converted.

Definitions for an archived image i in a *fixed independent source inventory*:
- `C_i=1` means an OME-Zarr converted representation actually exists.
- `I_i=1` means the modern image-search endpoint retrieves this image for the query.
- `S_i` is its original deposited, persistent file representation and lineage.
- `T_i(h)` is an independently adjudicated scientifically valid hypothesis-distinguishing test for a fixed substantive question h, given budget, provenance, and an acceptable alternative access path.
Under the documented current image-index design, `I_i=1 ⇒ C_i=1` but not conversely without data. So `Pr(C_i=1 | I_i=1)=1` can be true without `Pr(C_i=1)` being near 1 in the original archive population.

Actual **S-BIAD1410 image API**: 16 distinct visible images, 16 genuine source TIFF and 16 derived OME-Zarr representation links. These yield **16 physical-image mappings in an API-visible selected cohort**, NOT an all-original-image conversion fraction. Three real study-visible but new-image-search empty controls (S-BIAD1, S-BIAD570, EMPIAR-10014) show why API study index and derived image index have different selection rules, but do **not** establish which source image files in those archives are converted.

**Partial-identification statement (hypothetical):** if a complete original archive inventory later reveals `N≥16` distinct source images of the same defined type and all 16 mapped visible source image units remain valid, the known lower bound on the total converted-image count is 16, and the conversion fraction is at least `16/N`. **However N was not recovered**, so there is no scientifically useful numerical lower bound on the total fraction from the new image API alone. A formula involving an unknown `N` is a sensitivity condition, not a reported conversion percentage.

## Bounded direct source-manifest attempt: actually executed

Independently queried old [BioStudies original study JSON for S-BIAD1410](https://www.ebi.ac.uk/biostudies/api/v1/studies/S-BIAD1410), containing 23 immediate subsections; and old [BioStudies S-BIAD1410 TSV](https://www.ebi.ac.uk/biostudies/files/S-BIAD1410/S-BIAD1410.tsv), returned as 136 rendered text lines. A recursive file-manifest scan of the original JSON found no `files` array or exact-source-file inventory in the inspected hierarchy. The newer BIA study record advertised a GitLab `combined_file_list.tsv` URL, but a direct connector request to it returned HTTP 404. **No complete original TIFF/segmentation image file count was independently obtained in W44.** This is a data-availability blocker, not a claim that the original repository has no such inventory.

The actual public image records include `original_file_reference_uuid`, `creation_process_uuid`, model revisions, and some `attributes_from_bioformat2raw_conversion` tags. None of those inspected fields is an independently verified exact converter execution timestamp, converter binary SHA, scientifically calibrated voxel geometry or a validated hypothesis experiment. The study `ReleaseDate=2024-10-30` is a release date, not a converter rollout date.

## A second methodological trap: “AI” is not one intervention

The S-BIAD1410 study includes `associated_ai_models` metadata for **ReSCU-Nets**, a scientific segmentation/model-analysis task, whereas image representation conversion is labelled `bia_image_conversion`, and the original 2026 BIA article specifies deterministic non-LLM `bioformats2raw` for repository conversion. Confusing AI **image-analysis methods** with an assigned AI **file translator** would falsely manufacture the founding treatment variable `Z`.

## Scientific outcome and forward gate

We have now **actually observed** original/derived scientific image representation identities, formats, provenance and an institution's modern search selection rule, with **no** direct measurement of:
(1) source-file corpus denominator N; (2) exact converter execution date and version; (3) longitudinal lab-level standard-choice observations S/X/D; (4) assigned versioned AI converter vs strongest actual deterministic baseline under matched validation budgets; (5) independent scientific H0/H1 testability T, including other affordable access routes. A bigger set of query-visible converted images alone cannot bridge these evidentiary gaps.

**Rival defeats and non-novelty:** This selection-on-observability issue is standard statistical ascertainment/missingness, and the original BIA 2026 authors expressly describe it. Kuckertz et al. 2026 (already held in Drive), Huvila et al. 2026, Moore et al. 2023, PNAS many-analyst debate and converter/network economics remain stronger explanations of generic interoperability and representation effects.

**P77 director ruling:** An original-image file manifest and conversion event log could support a **bounded technical archive-fidelity/descriptive infrastructure audit**; without the full joint AI-treatment/community-adoption/scientific-testing data, the founding `Z→A→T` causal claim is **NOT IDENTIFIED**. Explicit **NO-GO for independent novelty promotion or PAPER/P78**, continue the bounded P77 investigation without pretending the empty endpoints are negative scientific results. No extra dataset download required of user right now; author PDFs already held. New 2026 NAR publisher PDF is not yet confirmed in 10_PAPERS, while publisher full HTML and API are publicly readable.
