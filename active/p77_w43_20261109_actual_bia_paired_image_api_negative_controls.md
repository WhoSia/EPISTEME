# EPISTEME-P77 W43 — Actual Original/Derived Image Pairings and Three Visibility Negative Controls

**Evidence observed 2026-11-09 KST. Charter:** [P77](../STRATEGY_P77_CURRENT.md). **Verdict:** source provenance verified, no population conversion-rate estimate, founding TLP causality **NOT IDENTIFIED**; P77 ACTIVE, P78/PAPER HOLD.

## Actual image-source census

A real live [BIA image API request for S-BIAD1410, page_size=25](https://beta.bioimagearchive.org/search/v1/search/fts/image?query=S-BIAD1410&pagination.page_size=25) returned **16 total hits and all 16 rows** on one page. Every image row carried its own genuine image UUID, `original_file_reference_uuid`, `creation_process_uuid`, original TIFF representation with `object_creator=bia_image_assignment` and linked `https://www.ebi.ac.uk/biostudies/files/...` file URI, plus one `.ome.zarr` representation with `object_creator=bia_image_conversion` and a distinct derived-object UUID/OME-Zarr path. **16 image records, 16 TIFF representations, 16 OME-Zarr representations — not 32 separately acquired images.**

Some metadata elements name `attributes_from_bioformat2raw_conversion` (2 of 16 derived records); presence of that marker is NOT proof that the other 14 used a different converter. The image-level `study_release_date` is 2024-10-30 on all returned rows, but **no explicit conversion-event timestamp was present in the saved source/image/representation metadata**. Revision integers 0/1/3 are NOT dates.

**Actual real evidence snapshot**, committed directly from read-only source API connector results, without inventing IDs: [four-accession API metadata JSON](../evidence/p77_w43_bia_20261109_four_accessions_metadata_census.json) (16 per-image genuine public UUID/URI/format/provenance records plus three control accession counts). The exact committed source snapshot was **independently read back from GitHub and re-audited in connector-side JavaScript**, confirming 16 unique image UUIDs, 16 original and 16 derived representations, 16 original file-reference UUIDs, 16 creation-process UUIDs, and associated file URI patterns. [Stand-alone Node source checker](../analysis/p77_w43_bia_api_visibility_census.mjs) is reproducible given this fixture; the **connector-side equivalent logic was actually executed**, the local Node test on the full GitHub fixture was not separately executed.

## Three negative controls from genuine API

Each accession returned exactly **one study hit** in `facet.accession_id.eq` study search, but **zero image search hits** in the corresponding new image endpoint:

| Official accession | Original study release date | Study hits | New image API hits |
| --- | --- | ---: | ---: |
| `S-BIAD570` | 2022-10-24 | 1 | 0 |
| `S-BIAD1` | 2018-11-22 | 1 | 0 |
| `EMPIAR-10014` | 2014-09-17 | 1 | 0 |

Actual queries: [S-BIAD570 image](https://beta.bioimagearchive.org/search/v1/search/fts/image?query=S-BIAD570&pagination.page_size=1), [S-BIAD1 image](https://beta.bioimagearchive.org/search/v1/search/fts/image?query=S-BIAD1&pagination.page_size=1), [EMPIAR-10014 image](https://beta.bioimagearchive.org/search/v1/search/fts/image?query=EMPIAR-10014&pagination.page_size=1). These are deliberately **chosen case studies, not a representative random sampling frame**. A zero in converted-image search **does not prove zero original images, no conversion or no institutional adoption**; it merely establishes that the specific new API search gave no result for the string at the observed time.

## Selection mechanism: conditional rather than population conversion

The authors' [actual NAR 2026 published source](https://doi.org/10.1093/nar/gkag1108) explicitly states **only images already converted to OME-Zarr are searchable through the new image API**. Set `C_i=1` if the source image has a converted representation, `I_i=1` if the new search exposes it; this implies `I_i=1 → C_i=1` *under documented current architecture*. Therefore observing 16/16 converted **conditional on being API visible** provides **no unbiased estimate** of the source archive's fraction converted; that would require independently enumerating all original image/acquisition units. Nor do the three 0-hit cases give reliable unconverted-image denominators.

The original BioStudies S-BIAD1410 JSON and S-BIAD1410 TSV actually fetched in W42 carry project/study metadata. They **do not independently reveal an exhaustive raw image-file manifest from the fields we inspected**. The indexed study points to a GitLab `combined_file_list.tsv/raw` link, but an actual direct fetch of that URL returned 404 from a rendering connector; no original-file denominator was recovered. Do NOT invent `N=16` for source images. Difference between file, image, time series, segmentation mask and accession remains critical.

## Observationally meaningful conclusion vs novelty

**PASS:** Actual per-image original `.tiff` ↔ access `.ome.zarr` provenance linkage, source UUIDs, 16-case full query census, API visibility negative controls, metadata version caveats. **HOLD:** source archive image corpus, time/order of conversion, precise converter binary provenance, lab's actual analysis standard and scientifically legitimate H0/H1 comparisons. **NO-GO:** claim that AI translation caused standard entrenchment or loss of scientific testability. **Not a newly discovered principle:** original BIA authors state the derived-only image-index rule, and classic sampling-selection theory covers the inferential defect.

**P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novelty NOT CERTIFIED.**
