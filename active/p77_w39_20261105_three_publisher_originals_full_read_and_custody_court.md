# EPISTEME-P77 W39 — Three Publisher Originals Acquired: Custody, Whole-Text Threat Analysis and Claim Correction

**Date:** 2026-11-05 KST. **Authority:** [binding P77 strategy](../STRATEGY_P77_CURRENT.md), [G-001](../GOVERNANCE.md). **Decision:** P77 ACTIVE / P78 HOLD / PAPER HOLD, independent TLP novelty not certified. **Previous:** [W36 prior-art screen](p77_w36_20261105_datadesc_ioproc_paradata_2026_fatal_prior_art.md), [W37 scientific standards](p77_w37_20261105_science_format_adoption_archival_vs_access_court.md), [W38 evidence gate](p77_w38_20261105_seven_source_evidence_grain_and_causal_gate.md).

## 1. User's three real original articles: metadata/byte custody and actual reading

The user put the materials in Research OS `00_INTAKE`; direct folder listing confirmed **two publisher PDFs and one original-source ZIP**, not a third PDF at the root.

| Original study | Verified original file | Size, precise custody |
|---|---|---|
| Kuckertz et al. (2026), *A framework for reproducibly managing coupled research software and data assets based on shared transformation functions*, *Patterns* 7:101493, DOI 10.1016/j.patter.2026.101493 | [Actual publisher PDF](https://drive.google.com/file/d/1ar_ViOI7pRjJbr8OsxCYPVwmOhqnA6Ba/view) | **3,060,606 B**, was already bibliographically renamed/moved to `10_PAPERS` when metadata was read again; same original file ID. Full extracted text ~89k chars read. |
| Huvila, Sköld, Zengenene & Andersson (2026), *What a standard makes out of a process? Data-documentation standards and their consequences to process documentation*, *Journal of Documentation* 82(7):289–314, DOI 10.1108/JD-10-2025-0324 | [Publisher PDF original](https://drive.google.com/file/d/14_ZZAAvjK9puYcxbQsOUPPeB7GW_BFWj/view) | **710,412 B**, already inside `10_PAPERS` when checked; this W39 completed full author/issue/pages/DOI filename normalization **without changing ID or bytes**. Full extracted text ~100k chars read. |
| Moore et al. (2023), *OME-Zarr: a cloud-optimized bioimaging file format with international community support*, *Histochemistry and Cell Biology* 160:223–251, DOI 10.1007/s00418-023-02209-1 | [Actual Springer 29-page PDF](https://drive.google.com/file/d/1RH6K2XEptsxEd4zu-kHVIdRy7rFV6GKa/view) | **4,866,691 B**. Derived from [original ZIP + METS](https://drive.google.com/file/d/1Rsnu4fmQc5HTQFAPfEjXV6Hh0bIssmdI/view) (**4,013,596 B**) provided by user. Local Python ZIP member CRC ALL PASS; extracted original file `418_2023_Article_2209.pdf` SHA256 **8aab2d20e75ac8fbe094a7ba2fb601b47a08819a37177f9106f2ee3a9b762c43**. Original ZIP SHA256 **778111ea3abd77f7910226b23546095c4ae2adcd4adde8b5a11dafc8c7b2938f**. Original ZIP was renamed/moved into **My Drive/EPISTEME/P77_W39 — 20261105 Original Standards Papers and Archive**, NOT Chat Archive. Extracted PDF was uploaded to project Drive and then moved to `10_PAPERS` with final ID/size/parent readback verification. |

**No unsupported custody claim:** Fresh SHA256 for the two existing Drive PDFs was **not** computed; original metadata size and file ID were checked. The third Moore PDF's SHA256 was computed from the actual ZIP-extracted bytes; upload file ID and size were read back, but the Drive-side raw bytes were not independently downloaded for another SHA. The third original source ZIP is preserved, not silently deleted.

## 2. Original full-text Kuckertz 2026: serious direct technical prior art, with a meaningful limitation

Publisher PDF explicitly defines three **already published** engineering contributions: (i) DataDesc extended from software interface models to dataset structure annotations; (ii) automated comparison to identify transformation **requirements**; (iii) ioProc modular, auditable shared transformation workflows. Two energy-system examples, FINE and REMix, demonstrate actual construction; public implementations [DataDesc](https://github.com/FZJ-IEK3-VSA/DataDesc) and [modelcouplingworkflows](https://github.com/dlr-ve-esy/modelcouplingworkflows) READMEs were actually inspected in W36.

**Original-paper qualification in “Limitations” (read in full):** the approach is initially limited by scarcity of available **well-annotated software/data components**, reusable published workflows/transformation functions and registries. It depends upon future publication/adoption of this infrastructure. Also, the author describes automated *identification of transformation needs* separately from building and evaluating every transformation; do not exaggerate it to universal automated scientifically valid conversion. In the original work, “AI-assisted technologies” are reported for writing/grammar polish, **not as proof that the scientific converters themselves were LLM treatment**.

**Implication:** the broad claim that metadata-based adapter design preserves process reproducibility has direct, working 2026 prior art. User's TLP AI-vs-strong-nonAI experiment must actually run/reproduce this alternative rather than use a token CSV rename as its “non-AI baseline.” No such experimental comparison was carried out in W39.

## 3. Original full-text Huvila 2026: direct philosophy-of-data rival, bounded method

Actual 26-page journal source surveys **nine** standards (Data Package, DataCite, Dublin Core, OAI-ORE, PREMIS, CERIF, DDI, PROV, NetCDF), using **close reading** and a table of process types, representation, scope, purpose and granularity. The Methods and material section states that this is a **convenience/purposive sample**, not all scientific metadata standards. The article directly demonstrates that differing standards emphasize curatorial life histories and different parts of research processes. Particularly, PROV models entities/activities/agents; DDI describes survey conceptualization, collection and processing; NetCDF offers computational process history/provenance attributes.

**Key inferential limit:** content analysis of standards identifies representation *affordances*, **not** empirical laboratory converter adoption and **not** an experiment quantifying actual lost scientific hypothesis tests. Their conclusion cautions that documentation practices also depend on the individual data producers’ intentions and actual degrees of choice. Therefore neither the paper nor EPISTEME may infer realized laboratory causal outcomes simply from feature availability.

**Fatal competing explanation:** the capacity of a standard to describe process information through selected ontological/epistemic lenses was already explicitly articulated in this paper. This general claim cannot be sold as a new EPISTEME mechanism. Potential novel work would need genuinely different testable, matched predictions beyond it.

## 4. Original full-text Moore 2023: documented and planned conversions distinct

Original Springer PDF 29 pages extracted. Pages around 243–247 report **BIA/IDR** converting selected bioimages to OME-Zarr and keeping converted representations transient for fast access and visualization, while archival data are stored on a different storage tier. SSBD reports known non-AI `bioformats2raw` conversion. The **Brain Image Library “In-progress” subsection** explicitly describes further tools as early development, while figure 15 illustrates a ~6TB archive example with dynamic OME-Zarr access. Do NOT infer the prospective large-scale service was deployed to all holdings at paper publication merely from a demonstrator figure.

**Interpretive correction:** `S` archival original, `X` access representation and `D` actual scientific-analysis format are separate variables. This distinction is **already in Moore's source**, so it can inform measurement without certifying novelty.

## 5. Actual state and next science gate

- **Original three PDF custody/whole-text:** PASS; correction to W36/W37 original-PDF debt: **these three original PDFs now HELD**, not missing.
- **Independent scientific hypothesis testing from whole underlying scientific images or energy models:** NOT RUN.
- **Assigned versioned AI converter Z, equal-budget strong non-AI baseline, community standards choice history, independently validated H0/H1 testing outcome:** NOT OBSERVED.
- **New independent explanatory residual beyond economic compatibility, DataDesc, Huvila, Moore and MQR:** NOT CERTIFIED.

**W40:** newly published 2026 institutional BioImage Archive article with real adoption/ingestion and converted-image counts must be assessed at its **correct observational grain**. Do not label a longitudinal image-conversion processing rate as causal AI adoption of a research standard.

**P77 ACTIVE / P78 & PAPER HOLD.**
