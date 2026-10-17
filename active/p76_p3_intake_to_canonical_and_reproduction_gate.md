# EPISTEME-P76-P3 — Actual Drive 00→10 Source Normalization & HDF Reproduction Gate

**2026-10-17 · P76 OPEN · Source custody PASS for four originals, HDF actual query experiment HOLD.**
No human recruitment, no paid API, no new generation proposed solely to increase version number.

## Native Google Drive original intake recovery and verified changes
Four PDFs were **actually found in 00_INTAKE** folder `1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16`, individually fetched for text content, metadata read (exact original size, mimeType, parent), and **renamed and moved** into `10_PAPERS — Canonical Literature Commons` folder `1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP` using Drive file metadata update, with the **same file IDs** (not new duplicate copies). The source version and author names are taken from actual original PDF content, not inferred from website title alone:

1. `1iDVCRrRYc7GOa52ozJt58O70ZnLxVlE7`, old `H4toH5Mapping.pdf` (1,091,376 B), now `Folk, McGrath & Yang (2017 rev.) — Mapping HDF4 Objects to HDF5 Objects — Version 4 — HDF Group.pdf`. Actual first page: v4, revised October 2000, July 2002, August 2003, September 2017. https://drive.google.com/file/d/1iDVCRrRYc7GOa52ozJt58O70ZnLxVlE7/view .
2. `1OM1tjsyaDgW0lv0diPMXtG4IKqohp9FA`, old `h4toh5lib_UG.pdf` (85,466 B), now `The HDF Group — H4toH5 Conversion Library User's Guide — v2.2.5 — OFFICIAL.pdf`. Exact PDF text describes SDS, image GR/RI8/RI24, Vdata, Vgroup, palette, annotation, mapping of attributes and scales, not a guarantee of global semantics. https://drive.google.com/file/d/1OM1tjsyaDgW0lv0diPMXtG4IKqohp9FA/view .
3. `1lxBHdARPJE5FlrWLocOgAyxO1rT2RCJl`, old `TransitionIssues.pdf` (41,444 B), now `McGrath & NCSA HDF Group (2000) — Transition from HDF4 to HDF5 — Compatibility Conversion Interoperability.pdf`. Actual PDF header dates September 12, 2000 and defines compatibility *relative to intended user tasks*. https://drive.google.com/file/d/1lxBHdARPJE5FlrWLocOgAyxO1rT2RCJl/view .
4. `1fMd0p8wdRL38OZ2G6Bi2yjsJRSroeY6d`, old `KCI_FI003031337.pdf` (584,311 B), now `Lee & Yang (2023) — A Study on Significant Properties for Dataset Type Preservation Format — DOI 10.14699-kbiblia.2023.34.4.259.pdf`. Actual original abstract reports **9 database-type** and **7 structured-data-type** significant properties, with NARA/Korean national archive comparison. https://drive.google.com/file/d/1fMd0p8wdRL38OZ2G6Bi2yjsJRSroeY6d/view .

Metadata update responses all returned `success:true` and `parent_ids=[10_PAPERS]`. Independent final readback of the exact parent IDs is a separate gate; if missing, do not state readback verified. Google Drive PDF raw byte SHA and check against actual publisher file bytes NOT performed; stable file IDs+sizes and parsed text ≠ checksum certification. The four original input records must not remain misclassified as still missing. Duplicate title-keyword search found these exact four, not additional confirmed duplicates.

## Strong original primary mapping rival (new insight from full original PDFs)

Folk/McGrath/Yang v4 explicitly provides application-side interpretation of HDF5 objects as HDF4 concepts, hence original readers' operational availability and exact object mappings are a **classical sufficient alternative** to any hasty 'irreversible epistemic migration' inference. McGrath 2000 directly emphasizes compatibility is relative to *what a user needs to keep doing*; this is essentially a prior task-indexed semantic-preservation approach. Lee/Yang 2023 independently decomposes dataset long-term properties (9+7), so merely asserting that preservation must include semantics is already existing research.

The proposed P76 novelty target should be sharpened to:
**Versioned Scientific Query Preservation under Representation-Dependent Verification-Option Depletion** — but this is **a P76 INTERNAL TEST NAME ONLY**, not a P77 new generation or a formal novel theorem. Benchmark an exact science-query `q` and its admissible source+software+rights paths; distinguish `q(original,legacy)`, `q(converted,new)` and `q(original,recovered-legacy)`, with full migration cost and old-tool availability. Test the conditional quantity `available_defeating_queries(source, toolchain, proof_role, budget)` against fully informative Forand-option and competent ETL/PROV rivals. Do NOT call simple conversion noninjectivity or lost endpoint novel.

## Concrete official experiment materials and honest current execution ceiling
- HDF Group original NASA HDF4→HDF5 sample catalogue: https://hdfdap.hdfgroup.org/zoo/h4toh5/h4toh5-def-demo.php .
- HDF Group official downloadable CentOS7 h4toh5 version 2.2.5 binary, built using HDF5 1.14.2 and HDF4 4.2.16-2 patch (site version wording): https://www.hdfeos.org/software/h4toh5-def-download.php . The publisher includes SHA256 and legacy v2.2.5 static builds. **Actual binary retrieval and checksum verification not yet achieved**.
- Official HDF4 library source: https://github.com/HDFGroup/hdf4 .
- Official converter original user guide and source mapping are stored canonical in Drive above.
- This assistant's local sandbox has `h5py 3.15.1` and numpy 2.3.5, but **no HDF4 reader (`pyhdf`, `hdp`) and no `h4toh5` executable**, and HTTP DNS resolution to the sample provider failed in the local sandbox. **Do not promote environment preflight to an executed HDF4→HDF5 actual conversion**. A safe followup is a READ-ONLY GitHub Actions runner acquisition of primary fixture, publisher SHA, converter binary and dependencies in temporary storage, plus bounded original/converted data query; do not misreport historical different build versions.
- Web official source confirms HDF Group already makes HDF4/HDF5 example pairs and metadata representations available, so successful conversion is a necessary positive control. Mere existence of the demo webpage is not equivalent to downloading/checking its exact bytes.

**P76-P3 verdict:** `4_CANONICAL_DRIVE_FILES_NORMALIZED_PASS / HDF_EXACT_SOURCE_AND_ORACLE_SPEC_DEFINED / REAL_CONVERTER_RUN_HOLD / PAPER_HOLD`.
