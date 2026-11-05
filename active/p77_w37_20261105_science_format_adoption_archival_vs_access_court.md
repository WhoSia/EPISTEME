# EPISTEME-P77 W37 — Actual scientific-format decisions, archive/access distinctions, and causal evidence limits

**Date:** 2026-11-05. **Mandate:** [P77 binding strategy](../STRATEGY_P77_CURRENT.md). **Verdict:** P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novelty NOT CERTIFIED.

## Actual sources inspected

**U.S. Bureau of Reclamation (2023)**, [RISE project 22041 official catalog](https://data.usbr.gov/catalog/8002/item/128581), *Evaluation of file formats for storage and transfer of large datasets in the RISE platform*. The official institutional report summary states netCDF and Zarr were both viable scientific data formats; netCDF was **prioritized** because of greater maturity, while dual support would give flexibility. This is an observed institutional format-prioritization decision, **not** an experimental AI-translation treatment or proof of a general lock-in law.

**Moore et al. (2023)**, *OME-Zarr: a cloud-optimized bioimaging file format with international community support*, Histochemistry and Cell Biology 160:223-251, DOI [10.1007/s00418-023-02209-1](https://doi.org/10.1007/s00418-023-02209-1). [Full original publisher article](https://link.springer.com/article/10.1007/s00418-023-02209-1), especially “Growth of a compatible solution” and “BIA and IDR” and subsequent institutional adoption sections, read as original full HTML.

The original source describes distinct institutional paths: selected bioimages are converted into OME-Zarr to provide cloud access; some converted copies are **transient** and coexist with long-term archival material. Wellcome Sanger adopted OME-Zarr as default representation for some imaging data. RIKEN SSBD describes existing **bioformats2raw** conversion for selected microscopy records. A separate scientific repository describes **on-demand OME-Zarr access to material kept in an alternative storage format**, rather than necessarily replacing its original archival format; parts of this plan were prospective in 2023, so do not characterize as an already-completed longitudinal migration. Source also describes an existing OME-NGFF schema validator for basic format conformance, not a scientific truth oracle.

## Critical correction to founding TLP variables

An institution's preferred **archival/source format** `S`, its emitted **access/adapter interface** `X`, and the format in which a **scientific test was actually performed** `D` need separate measurements. A rise in OME-Zarr *access* support need not imply a decline in alternative primary storage; nor is a format's use proof that the scientific hypothesis remains correctly testable.

Formal target: a documented, versioned AI-conversion change `Z` under matched resources versus the strongest existing deterministic/manual converter, a time-ordered community adoption outcome on `S/X/D`, and an independently adjudicated fixed-H0/H1 feasible-test outcome `T`. These sources show real format-related institutional choices and compatibility technology but **do not** report this joint causal experiment.

## Strong existing alternatives

RISE reports maturity and technical performance; Moore et al. discuss ecosystem/tool growth, institutional needs, cloud I/O, temporary transformed copies, and validator conformance. The already published scientific data-model adapter work of Kuckertz et al. (2026), Huvila et al. (2026) on standards' process-documentation affordances, prior converter economics and measurement/provenance models supply additional competitors. A claim “new representations necessarily entrench the old standard” does **not** follow, nor do these unmatched different-domain cases estimate a causal opposite effect.

## Evidence conclusion

**Actually performed:** verified report catalog, original publisher full-text sections and the difference between existing and planned practices. **Not performed:** full federal PDF raw benchmark rerun, numeric longitudinal institutional migration panel, treatment assignment, AI-vs-nonAI testing and testability-oracle measurement. Never invent institutional switch counts or times.

**Original PDF holding debt (not an immediate data blocker):** Moore et al. 2023 [MIT published PDF](https://dspace.mit.edu/entities/publication/ae784a29-4bbb-4157-b6f7-1164e2801b72); Kuckertz et al. 2026 DOI 10.1016/j.patter.2026.101493; Huvila et al. 2026 DOI 10.1108/JD-10-2025-0324. None was found in Drive by author/title search in W36.

**Director decision:** the source cases materially strengthen *measurement* of the founding research question but **do not certify a new mechanism**. **P77 ACTIVE / P78 HOLD / PAPER HOLD / originality not demonstrated.**
