# EPISTEME-P76-P20 — Real Scientific Instrument HDF4 Original Byte Custody

2026-10-17 KST. **P76 source contact POSITIVE; scientific inference / causal migration question untested; PAPER HOLD.** P77 default scent checked, no independent P77 question yet.

## Authenticated actual upstream source

GitHub `nexusformat/exampledata`, master pinned commit `eae516807ef7e27d1c45aab3af3a64a679154677` (2022-12-16). This project explicitly describes a mix of mostly real instrument-generated NeXus files (some deliberately broken or synthetic, so **do not claim all source files are verified natural measurements merely from repository classification**).

Read-only [real original science-file hosted CI #39041562983 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39041562983). Downloaded original repository bytes directly from exact SHA, checked file length and magic and executed independent old native `hdp list`.

| Upstream path | Length | SHA256 | Magic | Native `hdp list` |
|---|---:|---|---|---|
| `IPNS/LRMECS/hdf4/lrcs3701.nxs` | 115770 | `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39` | `0e031301` HDF4 | exit 0; NCSA HDF4 v4.1 release 3, scientific data groups |
| `APS/CCDImageServer/hdf4/Smither400.3_apr0300051.hdf` | 568977 | `f67d40f0cef33c6d0336fcc012d8940d2dc8b58767f36d7468faf4b5a11c34c7` | `0e031301` HDF4 | exit 0; HDF4 science group and Vdata records |
| `ANSTO/hdf4/PLP0006018.nx.hdf` | 572682 | `f922c79ea1c081354d230f91d3e13143cb86c4227ea1a071ea4a65c7d0def898` | `89484446` HDF5, NOT HDF4 | intentionally excluded |

First CI #39041502443 failed its 3/3 original-HDF4 assertion; the failure correctly detected mislabeled folder contents (ANSTO HDF5 under `hdf4` path). Revised CI #39041562983 PASSED exact required 2 authentic independent instrument-source HDF4 files while **retaining the ANSTO exception**. Misclassification is not evidence of historical archive conversion; repo naming is weaker than file magic.

## New independent feasible physical-science query gate

The original IPNS/LRMECS and APS CCD instrument files contain source-specific scientific data records; native physical-variable names, units, measurement axes and operational provenance must be extracted and declared **before** interpreting any numerical agreement. Suitable questions are e.g. time-of-flight count spectra and CCD image pixel intensities **only if actual source fields verify these semantics**. Do not label those variables as measured until original metadata readback.

Next bounded empirical task: choose the smaller IPNS original and extract `hdp dumpsds` named axes, scalar dataset values, instrument metadata and sample context. Then run SHA-verified official HDF Group h4h5tools 2.2.5, compare the SAME named original science variable across both representations (and the old-source rescue baseline). These NeXus source files may contain Vgroup/Vdata peculiarities, so failed conversion is route-specific unless strong competitors are exhausted.

This is **real scientific facility source custody**, more probative than HDF4 test fixtures, but **not** observed migration adoption, scientific falsifier loss, or a P76-specific new theorem. Existing Duerr layout readers, provenance, science calibration, source rights and Forand option stocks still viable.

## Automatic P77 court

Potential topic: scientific instrument archive *mislabeling and source trust* independent of format conversion. This is standard data integrity/provenance quality, reducible to P76 source-evidence custody and classic data quality; NO P77 independent program. Genuine falsifiable independent new question not yet observed.

`P76_P20_TRUE_SCIENCE_SOURCE_HDF4_2_OF_2_NATIVE_PASS / UPSTREAM_SHA_PIN / MISFILED_ANSTO_HDF5_DISCOVERED / SCIENTIFIC_VARIABLE_QUERY_NOT_RUN / P77_NOT_OPEN / PAPER_HOLD`.
