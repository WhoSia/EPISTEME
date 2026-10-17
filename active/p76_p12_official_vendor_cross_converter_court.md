# EPISTEME-P76-P12 — Official Vendor Conversion Disconfirms Converter-Intrinsic Impossibility

2026-10-17 KST. Authentic source comparison. P76 stays OPEN. PAPER HOLD. No new human participants or paid model calls.

## Frozen original bytes and vendor source integrity

- Pinned original HDF Group hdf4 source commit `2c46ad56bea5aab05e996e473a81dcbd9a66b125`.
- `SDSfloat2.hdf` 3116B SHA256 `3ba791239a5874bf9d97e1765a3e2896dbe965680b7fee59f9cc96afefb28b38`; native `hdp` reader verified prior P10.
- `sds_compressed.hdf` 3945B SHA256 `bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb`; native `hdp` reader verified prior P10.
- Original vendor release `h4h5tools 2.2.5` distribution official HDF Group support archive: https://support.hdfgroup.org/ftp/HDF5/releases/h4toh5/h4toh5-2.2.5/bin/ . Exact legacy CentOS7 package `h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz` was fetched on a temporary GitHub runner, checked against publisher .sha256 file and match TRUE. It is a self-extracting `hdf/H4H5-2.2.5-Linux.sh` installer, not a raw executable: earlier attempts wrongly assumed an executable at first unpack.

## Actual read-only CI

- [Official vendor completed Action #39026025935 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39026025935), commit `f9e7386449eadbad37ea0fa9f9cd80da845611ff`. Publisher package SHA match, temporary isolated installer extract, actual vendor binary invocation and HDF5 `h5dump -H` PASS for both inputs. JSON artifact uploaded in that run.
- Actual original `SDSfloat2.hdf` → HDF5 file **6360 bytes**, vendor exit=0, h5dump header exit=0, dataset `SDStemplate`, **H5T_IEEE_F32BE**, **9 × 6**. HDF5 mapped dimension datasets `fakeDim0` and `fakeDim1` and associated reference attributes.
- Actual original `sds_compressed.hdf` → HDF5 file **17003 bytes**, vendor exit=0, h5dump header exit=0, `SDSgzip` **H5T_STD_I32BE**, **16 × 5**, alongside other SDS structures (`SDSskiphuff` identified in header). Original HDF4 was DEFLATE compressed and native reader recovered its elements; HDF5 output did **not** yet receive all-element numeric-oracle test in P12.
- Compare [P11 third-party h5utils v1.13.2 experiment #39024334397](https://github.com/WhoSia/EPISTEME/actions/runs/39024334397): `SDSfloat2` source decoded values preserved across 54 original `hdp`-displayed entries while HDF5 dtype changed from float32 to float64; `sds_compressed` input conversion failed `h5fromh4 error: error reading HDF4 file`.

## Strong negative causal court

**Critical improvement**: P11 compressed-input failure is **NOT** intrinsic non-convertibility. The vendor converter successfully transforms the same checksum-matched archived source. This is an actual paired toolchain comparison, materially damaging any naive claim that migrating this original HDF4 dataset necessarily destroys an old countertest.
**Data model preservation is converter-dependent**: P11 third-party emitted float64 storage while official vendor emitted float32 storage for the same `SDSfloat2` original. These are storage-schema differences, not established world-level epistemic loss. HDF5 dimensions and mapped dimension references visible in official output. Do not claim HDF5 keeps old compression algorithm, all metadata meaning, or all scientific queries solely from headers.

## Failed tries faithfully preserved

- [#39025626779](https://github.com/WhoSia/EPISTEME/actions/runs/39025626779) FAIL: vendor tarball extracted but no direct `h4toh5` executable in first-layer tar.
- [#39025673436](https://github.com/WhoSia/EPISTEME/actions/runs/39025673436) FAIL: case-insensitive tool filename lookup still missed nested shell installer.
- [#39025765977](https://github.com/WhoSia/EPISTEME/actions/runs/39025765977) FAIL but original archive listing established `hdf/H4H5-2.2.5-Linux.sh`.
- [#39025894877](https://github.com/WhoSia/EPISTEME/actions/runs/39025894877) FAIL: wrong noninteractive installer flags and absent extraction, not data conversion.
- [#39025942526](https://github.com/WhoSia/EPISTEME/actions/runs/39025942526) FAIL, printed installer required interactive license acknowledgment.
- [#39026025935](https://github.com/WhoSia/EPISTEME/actions/runs/39026025935) PASS: publisher-checksummed, temporary-dir installed vendor converter ran on both source bytes and produced valid HDF5 headers.

## Next sharply bounded scientific gate

Perform independent **element-level native HDF4/official vendor HDF5** comparisons for each named SDS (including the multi-SDS compressed file) and preserve all original dtype, shape, scientific values and metadata keys. Then compare independent HDF4 reader restoration and installed HDF5 readers, source rights, cost, and alternative routes. A matched real scientific *historical* falsifier case remains absent: both present fixtures are software tests, not natural measurement ecology.

Disposition: `P76_P12_VENDOR_BINARY_SHA_PASS / HDF5_HEADERS_2_OF_2_PASS / COMPRESSED_THIRD_PARTY_FAILURE_DISCONFIRMED_AS_INTRINSIC / ALL_ELEMENT_VENDOR_QUERY_UNTESTED / ADOPTION_CAUSALITY_NOT_SHOWN / PAPER_HOLD`.