# EPISTEME-P76-P24 — Exposure-Conditioned Evidence Identity & Scientific Normalization: Shared Neutron Monitors, Acquisition-Unit Reconstruction, Correlated Measurement Controls & Rival-Sensitive Inference

**2026-10-18 KST · P76 active · P77 automatic watch ON but not promoted · scientific inference / manuscript PAPER HOLD.**

## 1. Source-level authentication and actual P24 execution

- Source: `nexusformat/exampledata`, source repository revision `eae516807ef7e27d1c45aab3af3a64a679154677`, `IPNS/LRMECS/hdf4/lrcs3701.nxs`, 115,770 B, original SHA256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`.
- HDF Group official `h4h5tools 2.2.5` source bundle passed publisher SHA256; archived old HDF4 read uses pyhdf HDF/V/VS/SD, HDF5 h5py direct paths and true object addresses.
- First original-acquisition inventory [GitHub Actions #39045141893 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39045141893); strengthened actual acquisition-time/value-certificate and source-to-vendor rerun [#39045333477 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39045333477). Both `contents: read`; no bot authored repository commits. Code: [exact full replay](../src/p76_p24_original_acquisition_exposure_audit.py) · [workflow](../.github/workflows/p76_p24_acquisition_exposure.yml).
- This is a public example distributed by NeXus rather than a newly obtained instrument-authenticated run log. Both `Histogram1` and `Histogram2` exist in the canonical NeXus manual's *same* `lrcs3701.nxs` walkthrough [original format documentation](https://fairmat-nfdi.github.io/nexus_definitions/mpes-liquid/introduction-napi.html). The example's existence and semantics are **prior art**: never call the mere demonstration of this file's basic NeXus structure a novel experimental discovery.

## 2. Precise original-source and vendor observations

| Distinction | Histogram1 | Histogram2 | Evidence interpretation |
|---|---|---|---|
| `run_number` | **3701** (old HDF ref 11) | **3701** (old HDF ref 80) | Equal run numbers, distinct stored SDS objects |
| `start_time` | **2001-02-07T08:54:21-0600** (ref 7) | same timestamp (ref 76) | Both source and HDF5 preserve the decoded ASCII timestamp despite storage representation as character array vs int8 bytes |
| `end_time` | **2001-02-09T14:12:53-0600** (ref 9) | same timestamp (ref 78) | Same temporal metadata, distinct SDS refs |
| `proton_pulses` | **2,268,088** (ref 22) | **2,268,088** (ref 91) | **Equal value, different stored original objects** |
| HDF5 `proton_pulses` object address | 13036 | 118449 | Vendor retains their **distinct storage identity** |
| `monitor1/data` | ref **57** | ref **57** | Two paths genuinely share ONE old object; vendor HDF5 addresses both **32141** |
| `monitor2/data` | ref **64** | ref **64** | Two paths genuinely share ONE old object; vendor HDF5 addresses both **39925** |
| Histogram `/data/data` total | 2,666,912 | 2,809,690 | Original and vendor matched P22; differing 148x750 and 148x35 bin systems |

Source `proton_pulses` SDS fields had **no `units` attribute** on the exact source paths inspected. The official vendor output preserved its int32 numeric scalar values and distinct HDF5 object addresses. Run number and dates preserved after *semantic* decoding; do not demand bytewise identical storage dtype for old source char arrays vs HDF5 int8 arrays.

The P24 NXentry traversal located **no recorded per-monitor `integral`, `nominal`, or `preset` fields** among examined acquisition candidates. NeXus NXmonitor formally permits these optional fields; their absence is not proof there is no valid external experiment normalization protocol ([official NXmonitor definition](https://manual.nexusformat.org/classes/base_classes/NXmonitor.html)). Nor do equal start/end, run number and proton count certify a unique physical experimental exposure, statistical independence, beam monitor calibration or the correct denominator for an estimator. HDF *object identity*, content equality and physical *acquisition identity* are separate.

## 3. Actual numerical comparison, explicitly NOT a physical estimator

For a frozen storage-level arithmetic check, calculate the uncalibrated scalar `stored histogram total / source-stored proton_pulses`:

| Bookkeeping quotient | HDF4 | HDF5 official vendor |
|---|---:|---:|
| Histogram1: 2,666,912 / 2,268,088 | **1.1758415017406731** | same (both source values preserved) |
| Histogram2: 2,809,690 / 2,268,088 | **1.238792321991034** | same |

This numerical equality is a **source-to-vendor descriptive positive control**, not an approved monitor normalization or a scientifically meaningful comparison of different histogram binning. No error bars, physical units of monitor efficiency, assumption of independent pulses/trials, group allocation policy, statistical significance or MgB2 phonon conclusion have been established. Neither a ratio of path-sums 356,242/178,121=2 (P23) nor a quotient by equal proton counts identifies an experiment's physical inferential scale by itself.

## 4. The genuinely useful three-grain identity counterexample

This ONE authentic source exhibits two distinct situations simultaneously:

- **Repeated paths to one stored measurement:** two original HDF4 monitor paths per monitor share refs 57 and 64. HDF5 vendor creates/preserves hard-link equivalences. Path incidence is not an independent raw-observation count.
- **Different stored objects with identical numeric values:** `proton_pulses` stored twice as *different* refs 22 and 91, and two distinct HDF5 object addresses. A content-value/hash-only deduper would collapse them as if they were the same source storage object, but *equal numbers alone do not determine object identity*. This does **not** prove they represent distinct physical accelerator exposures either.
- **Acquisition unit remains an independent question:** equal run/time/pulses plus shared monitors strongly suggest a common measurement context; reconstructing whether one physical run was reprocessed into two histogram views needs original acquisition documentation, beam logs, exact monitor gate, pulse/frame integration, and analysis design. P76 must **not** substitute object-graph connectivity for authorization to count independent experimental replications.

Thus `path_count`, `unique_source_object_count`, `content_distinct_count` and `independent_experiment_count` are **four different quantities**. Their distinctness is established by classical object identity/database/provenance and Hurlbert's statistical pseudoreplication literature, not a new EPISTEME axiom.

## 5. Historical genealogy / strongest rival / P77 adjudication

- P9 original fixed dispute-set quotient retained ranking sufficiency, but no universal future-task guarantee. P10 original endogenizes future criticism questions under retention `D(q)`; neither allows labeling a source path duplicate as a newly produced independent future falsifier. Original P9 and P10 native Notion pages were actually reread.
- PEA-Scope M22–M30 original exported history: independent operations can compose non-additively; outcome-censoring/selective audits are separate from original-world evidence. The exported spine alone is weaker authority than original independently checked execution receipts; original PEA closure M66 had provider fatal test unexecuted, therefore STOP/GO determined by independent research jurisdiction, not failed model scores. This original archive was actually reread in P24.
- NeXus `NXmonitor`, `NXdata`, design hard links, and the same exact original LRMECS example already define detector vs monitor semantics. P23's source-alias 2x count is a storage-arithmetic sanity check, not a physics claim. Hurlbert (1984) pseudoreplication is a direct historical theoretical competitor (DOI 10.2307/1942661).
- Full-source PROV, HDF4→HDF5 alias-preserving converter, classical statistical experiment-unit identity, versioned source+rights and Forand verification-option retention explain all currently observed outcomes. Vendor **preserves** original monitor aliases and separate proton-pulse objects; no migration-induced inferential error or actual changed scientific belief observed.

**P77 automatic scent:** `evidence-unit identity under hierarchical representation` is an intuitively distinct wording but presently collapses to standard NeXus provenance + experimental-unit identification and P76's source-authorized criticism paths. New fact that distinct original SDS refs contain equal proton counts **raises a useful *measurement-unit identifiability* question** but provides **no independent mechanism, no historical competing world adoption test, no changed rival-verdict**. `P77_WATCH_ON / P77_NOT_PROMOTED`.

## 6. What next is worth the cost (P76, not endless tools)

Ask what specific original IPNS experimental logs, beam monitor intensity/pulse integration and histogram gating contract distinguish one physical acquisition interpreted twice from independently gathered exposures. Use **one independent dated source document or acquisition log** before adding another self-contained source-file parser. If unavailable, set `PHYSICAL_NORMALIZATION_NOT_IDENTIFIED` with bounded descriptive positive results; optional next high-value future-falsifier experiment could deliberately drop/reassign preserved hard links while freezing raw values, showing how a **specified lossy** migration changes auditability, but it is a constructed intervention on this public source, not evidence of historical adoption. Strong classical alternatives remain the null.

**P24 final court:** `ACTUAL_ORIGINAL_AND_HDF5_ACQUISITION_FIELDS_PASS / SAME_RUN_TIMESTAMPS_PULSE_COUNTS / PROTON_VALUE_EQUAL_BUT_SOURCE_OBJECT_DISTINCT / MONITOR_OBJECT_SHARED / DESCRIPTIVE_PULSE_QUOTIENT_EQUAL / SCIENTIFIC_NORMALIZATION_HOLD / PHYSICAL_INDEPENDENCE_UNIDENTIFIED / P77_NOT_PROMOTED / PAPER_HOLD / NO_HUMAN_RATERS_OR_PAID_CALLS`.
