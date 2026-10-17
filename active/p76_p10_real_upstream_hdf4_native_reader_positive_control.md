# EPISTEME-P76-P10 — Real Official HDF4 Source-Byte & Native-Reader Pass, No Conversion Claim

Date 2026-10-17 KST.

## Direct original upstream custody
Original source repository HDFGroup/hdf4 at pinned commit `2c46ad56bea5aab05e996e473a81dcbd9a66b125` (the upstream `master` revision inspected 2026-10-17). GitHub source tree enumerated actual HDF4 bytes. The following publicly distributed HDF4 **test fixtures** are used; **NOT NASA observational data**.

| Fixture | Byte count | SHA-256 from actual downloaded raw original | Native result |
|---|---:|---|---|
| `mfhdf/hdfimport/SDSfloat2.hdf` | 3,116 | `3ba791239a5874bf9d97e1765a3e2896dbe965680b7fee59f9cc96afefb28b38` | `hdp dumpsds` exit 0; `SDStemplate` float32, dimensions **9×6**, no compression |
| `mfhdf/hdp/testfiles/sds_compressed.hdf` | 3,945 | `bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb` | `hdp dumpsds` exit 0; `SDSgzip` int32, dimensions **16×5**, DEFLATE level 6, reported compression ratio 5.42:1 |

First dataset displayed row of `100,100,200,200,300,400`. Second displayed early rows `1..5`, `2..6` etc. These are original tests, not claimed scientific evidence for migration hysteresis.

## Actual checked read-only CI
[GitHub Action #39023692816](https://github.com/WhoSia/EPISTEME/actions/runs/39023692816) **SUCCESS**; specific native `hdp dumpsds` commands PASS x2. Receipt `p76_p10_official_hdf4_native_reader_receipt.json` archived as Actions artifact under that run; no bot commits or user server writes.
[Exact source code](../src/p76_p10_official_hdf4_native_reader_preflight.py) · [GitHub native-reader workflow](../.github/workflows/p76_p10_official_hdf4_reader.yml).

[Earlier independent first attempt #39023497124](https://github.com/WhoSia/EPISTEME/actions/runs/39023497124) FAIL because official NASA/HDF demo webpage did not supply immediately parseable direct `.hdf`/ `.h5` HTML URLs in frozen parser. [HTML inventory rerun #39023583725](https://github.com/WhoSia/EPISTEME/actions/runs/39023583725) SUCCESS after fixing real `all_links` initialization error in failed intermediate #39023545476. The successful HTML link-index **does not demonstrate source data download**, and must not be confused with native fixture reading.

## Scientific boundaries and next falsifier
**P76-P10 direct-world contact is genuinely stronger than all previous P76 original-data proposals:** first observed native original HDF4 file bytes and an operating HDF4 reader. Nevertheless this is a software-source positive control, NOT a real scientific migration, HDF5 versioned converter or future challenge generation.

Prospective next `P76-P11` work inside P76:
1. Acquire and version-pin **official** h4toh5 conversion binary; verify publisher SHA/source and executable compatibility.
2. Convert the two verified original HDF4 datasets, compare numerical arrays, shapes, dtype, compression semantics and dimension scale fields by fresh HDF5 reader; allow functional equivalence even where storage layout/compression differ.
3. Preserve native original+reader recovery baseline, and include unsupported-source and failed-conversion denominators.
4. Challenge strongest classical software format migration/PROV/Forand option-capital before declaring representation-induced loss of falsifiability.
5. If no mechanism survives, record a null comparative benchmark without generating new theories solely to keep P76 alive.

**Verdict:** `P76_P10_REAL_ORIGINAL_HDF4_READER_PASS_2_OF_2 / ORIGINAL_BYTES_SHA_PINNED / CONVERTER_NOT_RUN / HDF5_QUERY_EQUALITY_UNTESTED / SCIENTIFIC_MECHANISM_HOLD / PAPER_HOLD / NO_HUMANS_OR_PAID_CALLS`.
