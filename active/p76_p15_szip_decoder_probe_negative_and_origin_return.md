# EPISTEME-P76-P15 — SZIP Independent Decoder Probe: Negative Result

Date: 2026-10-17 (KST). Original SHA-pinned public HDF4 test fixture, NO natural scientific case. Paper HOLD.

## Authentic read-only execution
[GitHub Actions run 39033254338 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39033254338). The workflow installed `hdf4-tools` and `libaec0` on a temporary Ubuntu runner, then executed the original SHA256-verified `sds_compressed.hdf` through `hdp dumpsds` in baseline and alternative library search-path configurations. In both, `hdp` printed `<SZIP library is not available>` and `<Unable to read SZIP compressed data>`. The run receipt recorded `NO_INDEPENDENT_SZIP_DECODE`, `native_szip_values_verified=false`. This tool outcome is a FAIL of the proposed recovery hypothesis, despite Actions SUCCESS.

The experiment **does not** show `libaec` is intrinsically inadequate or that SZIP cannot be decoded anywhere. It only shows this particular packaged HDF4 executable did not gain working SZIP decoding from installing `libaec0` or changing the search path. The decoder feature may be controlled by build options or library ABI compatibility; untested. Do not call this an independent SZIP-capable reader, because no such capability was demonstrated.

## Previous established results
P13 official `h4h5tools 2.2.5` output was decoded by `h5py`; original `hdp` yielded comparable values for SDStemplate 54/54, SDSgzip 80/80, SDSskiphuff 80/80 (**214/214 eligible decimal-rendered entries equal**). Native original SZIP 16x5 int32 values remain unreadable: 80 **CENSORED**, not unequal or known equal. P12 official vendor converter had a successful compressed fixture conversion; its output SDSszip data existence/type does not itself certify original numeric equivalence.

## Origin-first decision
This is now a narrow library-build compatibility limitation on a software test fixture. PEA-Scope's tool-growth warning applies: avoid arbitrary additional support matrices unless an independently checkable SZIP reader is immediately available. More valuable P76 investment is a **genuine versioned observational-science migration** with an old reader, converted reader, and a preselected rival-discriminating scientific query. Keep a full original input denominator and independent oracle, challenge standard PROV/Forand/ETL, and consider the SZIP issue a bounded pending technical test rather than a fundamental theory result.

P76-P15: `ENVIRONMENTAL_SZIP_RECOVERY_FAIL / ORIGINAL_SOURCE_ORACLE_80_VALUES_HOLD / CONVERTER_TOOLCHAIN_ALTERNATIVES_SURVIVE / PAPER_HOLD / HUMAN_FREE`. No recruited people or paid inference, no P77.
