# EPISTEME-P76-P23 — Shared-Monitor Source Identity, Naive Path Aggregation and Evidence-Unit Rival Court

**Date: 2026-10-18 KST. P76 ACTIVE; P23 actual science-file experiment POSITIVE BOUNDED; no P77 and no paper promotion.**

## Source and executing receipt

Official publisher-converter and original IPNS HDF4 experiment reused exactly:
- Original `nexusformat/exampledata` IPNS/LRMECS `lrcs3701.nxs` at commit `eae516807ef7e27d1c45aab3af3a64a679154677`, original SHA-256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`.
- HDF Group `h4h5tools 2.2.5`, vendor package verified against publisher SHA-256, temporary hosted Ubuntu reader, native `pyhdf` old Vgroup/SDS refs and `h5py` converted HDF5 objects. No simulated monitor values.
- [Actual read-only CI P76-P23 #39044145184 — SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39044145184), independent rerun of entire P22 original/converted comparison plus new path-identity audit; receipt artifact `p76-p23-ipns-monitor-source-object-identity`.
- [Exact P23 Python source](../src/p76_p23_shared_monitor_object_identity.py), [workflow](../.github/workflows/p76_p23_shared_monitor_identity.yml). CI has `contents: read`, no bot commit.

## Original-source observation, not a synthetic example

| Source | HDF4 ref | Two actual paths | HDF5 object address | Native sum | Shape and units | Original to HDF5 |
|---|---:|---|---:|---:|---|---|
| Monitor1 | 57 | `/Histogram1/monitor1/data`, `/Histogram2/monitor1/data` | 32141 | **146,389** | 1000 int32 count bins | All source elements agree |
| Monitor2 | 64 | `/Histogram1/monitor2/data`, `/Histogram2/monitor2/data` | 39925 | **31,732** | 500 int32 count bins | All source elements agree |

All four paths resolve in both representations, each monitor's two HDF4 paths share exactly the same source SDS ref and have equal original raw decoded value arrays; the two HDF5 paths resolve to the exact **same HDF5 dataset object address**. Original and converted values and `units=counts`, `signal=1`, `axes=time_of_flight` preserved for each path. `time_of_flight` itself is shared across Histogram1 and Histogram2 via refs 55/62, as verified in P22. No new measurement is created merely by adding another filesystem/HDF path.

**Measured raw-data counting collision**:
- Four apparent `monitor*/data` path occurrences: 2 per Histogram.
- Exactly **2 unique SDS source objects**, refs 57/64.
- Sum of one copy per SDS reference: `146389 + 31732 = 178121` stored counter events (mixed monitor channels; this is an illustrative total of integers, not a physically justified estimator).
- Sum of all four paths as if observations distinct: `2*146389 + 2*31732 = 356242`.
- **Ratio 2** between *these two bookkeeping aggregation rules*.

This is actual file-grounded **storage-identity overcounting** when counting identical monitors once per path rather than once per source object.

## Scientific inference hold: pseudoreplication is NOT identified simply by hard-link duplication

A shared stored object certifies repeated access to *one recorded array*, not the number of independent physical trials or whether an NXmonitor's readings should be reused as a denominator for two different Histogram `NXentry` analyses.

Two source objects do **not** imply two statistically independent experiments; conversely a shared count monitor used correctly across two distinct histograms is not automatically a statistical error.

A naive combined quantity `(Histogram1_count_total+Histogram2_count_total)/(unique_ref_monitor_sum)` vs denominator over four path occurrences can be made to differ by factor 2, but **neither is an endorsed neutron-scattering physical normalization** unless measurement exposure/monitor sampling semantics, the compatibility of two data-bin grids (750 versus 35 time bins), and actual analysis protocol are established. We intentionally do **not** present this made-up formula as scientific discovery, effect size, p-value, posterior shift or a documented user mistake.

No measured real analyst downstream error; no observed changed scientific conclusion, no statistical independence inference, and **no migration-caused source alias loss**. Indeed the official converter preserved object identities exactly.

## Strongest existing rivals: earlier science already has this

1. [NeXus Design — NeXus hard links and `target` attribute](https://manual.nexusformat.org/design.html) and [NeXus FAQ — aliases point to one actual dataset](https://manual.nexusformat.org/faq.html): explicit official source identity preservation, including migration utility. This is *direct anticipatory prior art*, not merely partial overlap.
2. [NeXus NXmonitor base class](https://manual.nexusformat.org/classes/base_classes/NXmonitor.html): beam monitor data, integrals, and optional normalization fields are already formalized. No permission to infer correct normalization from `data` array alone.
3. [NeXus NXdata](https://manual.nexusformat.org/classes/base_classes/NXdata.html): signal/axes and source semantic context, preventing basename-only matches.
4. [Hurlbert (1984), *Pseudoreplication and the Design of Ecological Field Experiments*, DOI 10.2307/1942661](https://doi.org/10.2307/1942661): non-independent replication/inappropriate experimental unit has foundational prior art; path aliasing supplies a trivial modern implementation hazard, not a novel statistical theory.
5. Standard PROV/graph-identity/source deduplication and Forand option maintenance can already describe representation paths and available correction interventions.

## P77 standing automatic promotion court

Candidate: **Evidence-Unit Identity under Representation-Dependent Scientific Measurement**, distinct in prose from P76's migration defeat-capacity, but currently no independent cause, no real changed downstream scientific inference, no evidence of special dependence not encoded by known hard link + experimental design + provenance, and all observed effects appeared in original HDF4 *and* official HDF5. Thus **P77_NOVELTY_HOLD**. This result is valuable as a *mandatory negative control* in P76: a naïve name/path-counting inference is wrong irrespective of version, and can be repaired using retained source object identity. A new project title is unwarranted.

## Next highest-value scientific discriminator (P76-P24 candidate, no blind implementation)

From the same real IPNS original source: recover experimental exposure and normalization contract (`proton_pulses`, beam monitor `integral`, measurement start/end, detector data assignment) using native NXentry/Vdata, test whether two histogram entries legitimately share the same monitor, and only then freeze one source-authorized physical normalized statistic. Evaluate *actual readers' inference*, not assume migration creates a downstream statistical defect. If the missing context cannot be recovered, classify an estimand as **not identified**, not effect=0 or irreversible loss.

**P23 final judgment:** `ORIGINAL_REAL_MONITOR_ALIAS_MATCH_2_OF_2 / HDF5_HARD_LINK_IDENTITY_PRESERVED_2_OF_2 / PATH_COUNT_DOUBLE_SUM_OBSERVED / EXPERIMENTAL_INDEPENDENCE_NOT_IDENTIFIED / CAUSAL_MIGRATION_EFFECT_NOT_OBSERVED / P77_NOT_PROMOTED / PAPER_HOLD / HUMAN_FREE`.
