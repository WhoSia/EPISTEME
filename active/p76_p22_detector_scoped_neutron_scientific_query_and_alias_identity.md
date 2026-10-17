# EPISTEME-P76-P22 — Detector-Scoped NeXus Measurement Identity, Bin-Aware Scientific Queries, and Shared-Reference Rival Court

**2026-10-17 KST. P76 OPEN / REAL MEASUREMENT QUERY POSITIVE / CAUSAL ADOPTION MECHANISM UNPROVEN / PAPER HOLD / P77 WATCH NOT PROMOTED.**

## Scientific source provenance and actual executions
Original IPNS/LRMECS neutron instrument NeXus HDF4 source `IPNS/LRMECS/hdf4/lrcs3701.nxs` from `nexusformat/exampledata` at upstream commit `eae516807ef7e27d1c45aab3af3a64a679154677`; **115,770 raw bytes**, SHA-256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`, HDF4 magic. This is an actual facility-file example, whose natural observational status beyond source metadata is not independently authenticated by the underlying experimental institution.

Official HDF Group vendor `h4h5tools 2.2.5` archive `h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz` checksum-verified against the publisher SHA-256; fully deployed in an isolated temporary GitHub runner. Native HDF4 group data, SD/SDS and VS/Vdata extracted through `pyhdf.HDF`, `V`, `VS`, `SD`; independent converted HDF5 checked using `h5py`. No permanent machine changes.

**Final actual CI: [#39043333481 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39043333481)**, code [source/converted mixed path comparison](../src/p76_p22_mixed_object_vendor_identity.py) and [read-only workflow](../.github/workflows/p76_p22_mixed_object_vendor.yml). P22 original preflight [#39042649713 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39042649713) initially confirmed 128 HDF4 Vgroups and `Histogram1`/`Histogram2` NXentry but incompletely interpreted internal SDS records. First #39042553333 failed because required `pyhdf.V` module had not been imported lazily. First source-vendor #39042857497 success compared only 12 explicitly visited unique-object dataset paths and *incorrectly seemed* to omit some aliases; direct HDF5 path lookup corrected that to all 20 scoped comparison paths in [#39043145064 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39043145064). Do not erase prior attempts or treat instrumentation bugs as underlying science.

## Actual group/source-object audit
Native old IPNS HDF4 has **128 Vgroups**, four apparent roots: two scientific `NXentry` `Histogram1`, `Histogram2`, plus `CDF0.0` and `RIG0.0` internal HDF roots. Across the walk, **281 linked object occurrences** were visited (118 SDS and 163 Vdata occurrences), not 281 distinct original physical observations. Vendor HDF5 ordinary unique-object walker visited 74 unique datasets, also **not** a total of 74 resolved paths. These counts differ in grain and must NEVER be treated as a 281→74 loss rate.

Original source Vgroup references include shared monitors across `Histogram1` and `Histogram2`. Some reference numbers appear in multiple Vgroups. Default `h5py.visititems()` enumerates a linked dataset object once even if additional HDF5 hard-link paths exist, so it can create a false loss. Independent direct `f[path]` lookup and HDF5 object-address equality showed **all 20 relevant path-qualified source `data`/`time_of_flight`/`polar_angle`/`energy` occurrences** existed as HDF5 dataset paths and had matching numerical arrays (20/20 comparisons, including alias repeats). Ten source-ref identity audits included **eight real multi-path NXentry references**; all their relevant HDF5 paths exist and resolve to the **same HDF5 object**. The remaining two singleton refs are not counted as evidence of multi-path alias preservation. The internal auto-generated `CDF0.0` root paths are **not** required as independent NXentry scientific paths.

## Actually calculated detector-scoped scientific queries
Fix historic NeXus source path `/HistogramX/data/` rather than matching `data` basenames. Original `data` attributes include `units=counts`, `signal=1`, `axes=polar_angle:time_of_flight`. Original `time_of_flight` is in microseconds, `polar_angle` in degrees. Original neutron-count arrays and both axis arrays decode successfully; exact same qualified HDF5 paths have equal element arrays, units and science-axis attributes.

| Query | Histogram1 original AND vendor converted | Histogram2 original AND vendor converted |
|---|---:|---:|
| Source count matrix | 148 × 750 int32 | 148 × 35 int32 |
| Count total (sum over all bins and angles) | **2,666,912** | **2,809,690** |
| Time-of-flight axis edges | **751** float32 | **36** float32 |
| Polar angle positions | **148** float32 | **148** float32 |
| Count-weighted mean time-of-flight, bin midpoint | **2060.0742634177655 µs** | **2186.9438977253717 µs** |
| First nonzero-angle bin counts | 2664 | 3412 |
| Full data+axis elementwise equality | **PASS** | **PASS** |
| Units, `axes`, `signal` attributes equality | **PASS** | **PASS** |
| Row-wise angle-sum SHA256 equality | **PASS** | **PASS** |

Definitions: `time_of_flight` holds **bin edges**, hence count matrix has one fewer time column than time-axis length. Weighted mean uses each bin midpoint and neutron count as weight, with `float64` arithmetic; this is a source-bound descriptive statistic, not an experimentally independent calibration or claim about MgB2 phonon density.

Original and converted row-sum SHA256:
- Histogram1: `b38396791e69ddeb0f39578649bcd1b76da46114d38442dbc825e7fe2922d7b5`
- Histogram2: `f7dbad6c9d91928876e938a26691e66e6ae9e864ef27eaa744ecdc0683acbf1d`

Critically, all described observed scientific results are **positive fidelity controls**, not evidence of adoption-induced, path-history-dependent inability to falsify a theory.

## NeXus rival prior-art and P77 conditional review
The native old file uses field `signal=1` and `axes` colon-separated, typical historical NeXus semantics; current NeXus normative conventions have evolved to group-level `NXdata@signal`, `NXdata@axes`, `AXISNAME_indices` and support multi-dimensional and bin-edge axes. Strong original NeXus sources:
- https://manual.nexusformat.org/classes/base_classes/NXdata.html
- https://www.nexusformat.org/Connecting_NXdata_to_NXdetector.html
- HDF4 Vgroup documentation: https://fhs.github.io/pyhdf/modules/V.html

**Most promising P77 scent**: distinct **evidential-independence accounting under shared-observation aliases**. Two HDF4 paths, including monitor `Histogram1/monitor1/data` and `Histogram2/monitor1/data`, can refer to precisely the same underlying raw observed values. Naive path-counting may falsely treat them as independent readings when building confidence or comparing competing science claims. This is a real potential scientific question distinct from bare numerical file preservation, and a potential empirical *fault mode*; however, standard HDF aliasing, provenance graph identity, correlated observations and pseudoreplication already cover the basic mechanism. **No identified independent novel object or rival-defeating result; P77 NOT OPEN**. The P76 scope already includes path-dependent validation and evidence authority; continue to test within P76.

**Next source-based falsifier (P76-P23)**: compare actual monitor-normalized neutron count estimates under (i) source-reference-correct unique monitor accounting versus (ii) naive duplicated HDF5 path counting. Freeze competing claims and demonstrate whether duplicated evidence paths would materially change a science inference; challenge classic alias-aware software, PROV and statistics before promoting a separate theory. Do not infer experimental measurement independence merely from sharing/differing paths. Include APS separately only when justified, rather than appending many test fixtures.

**Judgment:** `P76_P22_GENUINE_ORIGINAL_DETECTOR_QUERY_PASS_2_OF_2 / 20_OF_20_SCOPED_ORIGINAL_CONVERTED_PATH_NUMERIC_EQUAL / 8_OF_8_MULTI_REFERENCE_ALIAS_GRAPHS_PRESERVED / INSTITUTIONAL_ADOPTION_CAUSAL_MECHANISM_HOLD / P77_SCENT_PSEUDOREPLICATION_EXISTING_PRIOR_ART / P77_NOT_OPEN / PAPER_HOLD`. No recruited humans, paid inference, or CI bot contributions.
