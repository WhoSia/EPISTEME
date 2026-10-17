# EPISTEME-P76-P11 — Real HDF4→HDF5 Conversion, Numeric Preservation vs Type Drift, and Converter-Specific Censoring

**Date:** 2026-10-17 KST. **Scientific status:** AUTHENTIC_SOURCE_CONVERSION_COMPARISON_PASS_BOUNDED / OFFICIAL_H4TOH5_REPLAY_PENDING / PAPER_HOLD.

## Frozen actual original and exact trial

Original repository HDFGroup/hdf4 SHA `2c46ad56bea5aab05e996e473a81dcbd9a66b125`. Original HDF4 files and SHA-256 exact:
- `mfhdf/hdfimport/SDSfloat2.hdf` 3116 bytes, SHA256 `3ba791239a5874bf9d97e1765a3e2896dbe965680b7fee59f9cc96afefb28b38`. Original native `hdp dumpsds` **PASS**, SDS float32 9×6. Converted by **third-party h5utils h5fromh4 v1.13.2** to HDF5; `h5py` new-reader shape 9×6, **54 numeric values exactly match** the original `hdp` printout, old/new double-precision sums both 15700.0; new HDF5 dtype **float64**, original HDF4 semantic dtype **float32**. Numeric equality therefore does NOT guarantee storage type/schema equality; investigate conversion policy/typing and whether values shown by hdp have been rounded.
- `mfhdf/hdp/testfiles/sds_compressed.hdf` 3945 bytes, SHA256 `bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb`. Original `hdp dumpsds` PASS and displayed SDSgzip int32 16×5 DEFLATE level 6. **h5fromh4 conversion EXIT 1** with `h5fromh4 error: error reading HDF4 file`. No converted HDF5 query result for this input. NOT proven source data loss because original reader works.
- `pyhdf` original reader also failed on the simple SDS dataset with `SDreaddata failure` in first attempt #39024097223; the validated native `hdp` was used as the original-value oracle in later court. Differences between reader implementations should not be misclassified as irreversible data loss. `hdp` emits finite decimal representations, so equality of printed decimal values to new float64 is not bitwise original-float proof; investigate original bits before a full exact-precision assertion.

**Actual conclusive Actions:** [P76-P11 #39024334397 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39024334397), commit `0782f9c7aeb2bfe2879f88cfd0785863f2fad308`. [Source](../src/p76_p11_h5utils_original_converted_query.py), [workflow](../.github/workflows/p76_p11_h5utils_numeric_query.yml). Results JSON saved as the run's named artifact. Earlier P11 job failures are source investigation history, not erased: first pyhdf error, then parser regex error, then repeated SDS metadata, then converter-specific compression read error. The successful final job explicitly retains **1 preservation and 1 converter failure**, not 2/2 conversion success.

## Strong scientific interpretation
(a) Retained raw HDF4 source with working hdp provides an **actual positive control against 'global irreversible epistemic route loss'** for these bounded queries. (b) h5utils third-party converter has an actual dataset-specific failure; this is `toolchain-bound route failure`, **not** evidence of P76's distinctive representation-adoption-caused inability to test scientific rivals. (c) Observed dtype float32→float64 makes 'same number' weaker than scientific-type/metadata preservation, but does not alone prove any scientific inference changed. (d) Fraction of observed numeric preservation among ALL selected inputs **1/2 succeeded, 1/2 source-specific failure**, not '100%' by dropping failed item.

**This is not NASA observational data**; both are actual publicly distributed HDF Group *software test fixtures*. The scientific program's empirical real-infrastructure lock-in distinction remains unresolved and paper HOLD.

## Next fatal-rival execution
1. Obtain official HDF Group **h4h5tools 2.2.5** source/binary from https://support.hdfgroup.org/ftp/HDF5/releases/tools/h4toh5/h4toh5-2.2.5/src/ and verify publisher sha256 before build. Official library can have different result on the same original HDF4 fixture, which would indicate toolchain-dependent compatibility not source-intrinsic impossibility.
2. Compare native HDF4 datatype/bytes with official h4toh5 and h5utils transformed float data, especially original 32-bit type versus output 64-bit type and metadata.
3. Include unsupported/converted/untested samples as separate denominator types and **never** infer cross-version scientific falsification incapacity from input converter exceptions.
4. Competent ETL/PROV, Forand options and installed-base standard transformation rivals must be defeated with original source-specific falsifiable test, else P76 new-mechanism HOLD.
