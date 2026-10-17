# EPISTEME-P76-P25 — Original LRMECS Producer-Logic Witness, Acquisition-Unit Nonidentifiability and the Limits of Numerical Normalization

**2026-10-18 KST · P76 open · P77 automatically reviewed, HOLD · PAPER HOLD.**

## Executive scientific judgment

A major evidential improvement over P24 has occurred. The official NeXus project exposes historical Fortran **`NXlrcs.f90`**, which writes `lrcs####.nxs` from an IPNS LRMECS `lrcs####.run`. Its producer-logic pattern exactly explains two seemingly paradoxical attributes of the P24 instrument-source HDF4 sample:

1. For each histogram entry `i`, the producer calls `get_IPNS_item("PLS", int_value)` and creates **a fresh** `proton_pulses` dataset in the per-entry `NXsource` group. Thus equal run pulse values stored in different original objects are an expected serialization design pattern, **not automatically distinct physical accelerator runs**.
2. It creates `monitor1` and `monitor2` groups when `i=1`, saves their link IDs `M1_id` and `M2_id`, then calls `NXmakelink(... M1_id/M2_id)` when `i>1`. Thus multiple histogram paths to the **same** monitor storage group are an intended producer pattern, not independently sampled neutron monitors.

**Careful limit:** The public historical demonstration program is NOT an authenticated copy of the precise compiled binary/commit that produced the specific archived `lrcs3701.nxs`. The NeXus user-guide example displays earlier-version metadata than P21's pinned source file, and the actual `lrcs3701.run` acquisition log is not preserved in this court. We have *historical generative-pattern concordance*, not an exact line-by-line reconstruction of the 2001 experiment or a physical exposure contract.

## Verified source and first-hand toolchain

- Original source repository `nexusformat/exampledata`, pinned SHA `eae516807ef7e27d1c45aab3af3a64a679154677`, exact original `IPNS/LRMECS/hdf4/lrcs3701.nxs` 115,770 bytes SHA256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`.
- Original producer candidate: [NeXus `NXlrcs.f90` public source](https://www.nexusformat.org/NXlrcs.f90.html), loop / `PLS` write / per-histogram `NXsource` at source lines ~46–97, monitor creation and `NXmakelink` at ~121–156. These are actual producer-source statements, **not** inferred from path naming.
- [Actual P25 original source+producer check, GitHub Actions #39046664833, SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39046664833). Hosted Ubuntu, `pyhdf`, source SHA verification, full HDF4 original group / SDS traversal; source-generator HTML SHA captured in run artifact. Source: [`src/p76_p25_ipns_generator_original_ref_alignment.py`](../src/p76_p25_ipns_generator_original_ref_alignment.py), workflow [`p76_p25_ipns_producer_ref_court.yml`](../.github/workflows/p76_p25_ipns_producer_ref_court.yml). GitHub CI writes no commits (`contents: read`).
- Earlier diagnostic failures: [#39046363003](https://github.com/WhoSia/EPISTEME/actions/runs/39046363003) (Sphinx syntax nodes were joined with inserted spaces), [#39046469144](https://github.com/WhoSia/EPISTEME/actions/runs/39046469144) (`pyhdf.V` not imported, a code error), [#39046540095](https://github.com/WhoSia/EPISTEME/actions/runs/39046540095) (assumed producer `LRMECS` group name identical in this archived file; actual NeXus group is `instrument`). Corrections retained; successful #39046664833 used source-traversed paths, not basename matching. CI PASS refers to the *specified source checks*, not a full physical inference.

## Actual original HDF4 object evidence

| Field / group | `/Histogram1` | `/Histogram2` | Interpretation |
|---|---|---|---|
| `monitor1` group HDF4 ref | 52 | 52 | Shared **group** object |
| `monitor1/data` SDS ref | 57 | 57 | Shared stored numeric dataset |
| `monitor2` group HDF4 ref | 59 | 59 | Shared **group** object |
| `monitor2/data` SDS ref | 64 | 64 | Shared stored numeric dataset |
| `instrument/source/proton_pulses` SDS ref | 22 | 91 | Two distinct storage objects |
| `proton_pulses` decoded value | 2,268,088 | 2,268,088 | Same stored count value, not independent exposures |
| `run_number` | 3701 | 3701 | Consistent run label, not physical treatment replication |

Generator text names `LRMECS` as the instrument group, but the actual pinned file's path is `/Histogram{1,2}/instrument/source/proton_pulses`. **Treat this mismatch as evidence the historical source code cannot be declared the exact executed binary for these bytes.** It does not weaken the independently checked original ref identity statements.

## What independent physics sources contribute, and what they DO NOT

- [NeXus official NXmonitor base-class definition](https://manual.nexusformat.org/classes/base_classes/NXmonitor.html) explicitly distinguishes monitor time-of-flight arrays, `data`, optional `integral`, `nominal`, `preset`, `efficiency`, `sampled_fraction`, and `count_time`. In particular, calendar interval is not necessarily active counting time, and a histogram of monitor counts is not automatically a facility-approved normalization denominator. This is a **strong existing rival convention**, not a new invention by P76.
- The historical producer `NXlrcs.f90` serializes `sg%counts` into monitor `data` and obtains `PLS` into an integer. That establishes the **writer's emitted fields**, not an effective proton charge, target proton intensity, detector efficiency, gate-specific monitor acceptance, or the unique data-reduction rule. The `PLS` acquisition interpretation beyond its name is not authenticated against the missing native `.run` raw acquisition log.
- [Osborn et al. (2001), `Phonon Density-of-States in MgB2`](https://doi.org/10.1103/PhysRevLett.87.017005) is a genuinely contemporaneous Argonne/IPNS MgB2 neutron-scattering study. Its existence strengthens scientific-context custody **but does not show that their reported published experiment is exactly histogram run 3701**, or authorize its calibration protocol as run 3701's rule. Distinct sample masses/incident energy and file metadata may even prevent naive identity assumptions; a source/run-specific link is required.
- [Hurlbert (1984), pseudoreplication](https://doi.org/10.2307/1942661) already distinguishes stored observations from independent experiment units. The P24 source phenomenon is very well represented in existing database aliasing, observational science and statistical experimental design. No novel theorem established.

### Non-identification result (conditional, classical)

Let the publicly observed file encode two histogram count arrays (Y_1,Y_2), run label (r), pulse counter (P), monitor traces (M_1,M_2), and their source object alias graph (G). Distinct unobserved physical acquisition protocols (A) can produce the same ((Y_1,Y_2,r,P,M_1,M_2,G)), e.g. two re-binnings of one event stream vs two detector selections in a run. Therefore the archive alone need not identify unique independent-exposure count (n_A), source flux, monitor gate, or scientifically correct normalization `N(Y,M,P,A)`. **No constructed model was empirically executed here; this is a caution about the evidential information absent from the identified artifact**. Future explicit countermodels must obey real instrument constraints before theorem/paper promotion.

Prior descriptive count-per-stored-pulse ratios (2,666,912/2,268,088=1.17584...) and (2,809,690/2,268,088=1.23879...) are reproducible arithmetic, **not** neutron cross-sections, independent trials, physical normalization or statistical significance. The equal monitor arrays are one stored object in the original file, not two independent monitor observations.

## Strong rival and P77 court

**Verdict against novelty laundering**: today's positive finding gives actual producer-side explanation of earlier source topology; the same pattern is **already NeXus source-code prior art**. NeXus NXmonitor, HDF4 group hard links, PROV/ETL, instrument-run identification and Hurlbert independently anticipate the relevant distinctions. Hence the P77 candidate `measurement unit as a provenance-labelled relation independent of storage paths` does **not yet survive** its best classical rivals and sits within P76's existing future-source-authorized criticism question.

P77 automatic monitor **ON**. P77 **NOT PROPOSED / NOT OPEN**. P76's broader founding question about endogenous evidence-production and future rival defeat remains open, not disproved by this producer-source concordance.

## High-value P26 object, stop rule against tool proliferation

Before more code, find the original LRMECS `IPNS_module` source defining `PLS`, native `lrcs3701.run` provenance/log and publication-linked reduction method. If unavailable, report `PHYSICAL_ACQUISITION_NORMALIZATION_NOT_IDENTIFIED` and stop searching old paths unboundedly. A higher-value intervention is to **condition a predetermined future scientific query on a known physical exposure contract** and distinguish an archive that preserves exact source data from one that destroys critical generator/monitor reference information; classify any induced break as a **constructed transformation** rather than observed institution adoption.

**Court:** `P76_P25_ORIGINAL_GENERATOR_LOGIC_SOURCE_PASS / HISTOGRAM_MONITOR_SHARED_HDF4_GROUP_IDENTIFIED / PULSE_PER_HISTOGRAM_DISTINCT_SDS_WITH_EQUAL_VALUES / EXACT_GENERATING_BINARY_NOT_AUTHENTICATED / PHYSICAL_NORMALIZATION_UNIDENTIFIED / CLASSICAL_RIVALS_SURVIVE / P77_HOLD / PAPER_HOLD / NO_HUMAN_OR_PAID_CALLS`.
