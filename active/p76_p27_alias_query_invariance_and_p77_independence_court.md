# EPISTEME-P76-P27 — Task-Conditioned Scientific Query Invariance under Archive Alias Fracture: Source-Object Identity, NeXus Link Contracts, Provenance-Aware Aggregation & the Limits of Evidence-Unit Promotion

**2026-10-18 KST. P76 OPEN. P77 watch ON but HOLD. PAPER HOLD.**

## 1. Source custody and a genuinely new controlled comparison

Direct original source repository `nexusformat/exampledata`, pinned revision `eae516807ef7e27d1c45aab3af3a64a679154677`. Downloaded and SHA-verified both:
- `IPNS/LRMECS/hdf4/lrcs3701.nxs`: 115,770 bytes, HDF4 magic, SHA256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`;
- `IPNS/LRMECS/hdf5/lrcs3701.nx5`: 541,008 bytes, HDF5 magic, SHA256 `20a65f41ddf61afd53126847c3204f069b0f5ae69880af4777e1863a2ac66ea2`.

[P27 robust completed Actions #39052443988 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39052443988), plus earlier first-pass [#39052224360 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39052224360). [Original Python](../src/p76_p27_source_pair_alias_query_intervention.py); [read-only workflow](../.github/workflows/p76_p27_alias_query_intervention.yml). P27 R1 replaced an insufficient first-five-values source-content key with SHA256 of the *full canonicalized int32 data array*, then independently reran. Both original files verified against exact frozen SHA; no converters run in this new court. `contents: read` prevents bot commits.

Both files existed side by side in the upstream repository by at least [2020-01-22 relocation commit](https://github.com/nexusformat/exampledata/commit/976130be074a056efb5f03d6ca3b16b0aaaee07a). The commit is **only evidence of directory relocation, NOT provenance of original NeXus HDF5 creation or adoption by IPNS.** The original archive README states most but not all examples came from real instruments and some are deliberately unsuitable test inputs. Its [2022 critique.md](https://github.com/nexusformat/exampledata/blob/eae516807ef7e27d1c45aab3af3a64a679154677/critique.md) categorizes this HDF4 as `unrecognised` by a cursory checker but does not disprove the SHA/native HDF4 reader evidence; the archived HDF5 has two NXentries and no recognized application definition in that report. Those tool reports are not a physics authority.

## 2. Distinguish queries **before** interpreting a representation shift

**Q0 — Named path/entry/monitor values:** for each `Histogram1` and `Histogram2`, ask the recorded sums of `monitor1/data` and `monitor2/data` and the `run_number`. Answers are invariant: monitor 1 = **146,389**, monitor 2 = **31,732**, and `run_number=3701` at both entries in both files. This is an actual source-verified query, but not a validated neutron normalization.

**Q1 — Sum all four monitor-data paths:** both file formats return **356,242**. Invariant because the path-accessible array values remain equal.

**Q2 — Sum each storage object once:** original HDF4 has monitor SDS refs 57 and 64, total **178,121**; publicly distributed HDF5 has FOUR distinct dataset object addresses and total **356,242**. 2× result is truly source verified, but Q2 is an *intentionally fragile storage-address-based statistic*, **NOT** a justified physical exposure estimator.

**Q3 — Deduplicate by (run number, monitor role, full canonical int32 array SHA):** both formats return **178,121**. This is a controlled, purpose-specific content-key equivalence; it does NOT prove physical acquisition identity, since independent acquisitions may coincidentally agree and shared acquisitions might differ after transformation. Do not conflate Q3 with scientifically authorized inference. The use of historical role-and-run identity is an externally selected rule; the HDF5 byte structure alone does not magically certify its authority.

Four source HDF4 monitor data paths and four HDF5 paths passed all elementwise values (as part of the source-pair court), and exact 20 historical science paths and 16 numeric arrays remain confirmed from P26 R1, 4 timestamp strings semantically equal and normalized `units` values matched. **No new measurement performed.**

## 3. New specific factual test: NeXus `target` and group identity

NeXus [design hard link/target rules](https://manual.nexusformat.org/design.html), [FAQ](https://manual.nexusformat.org/faq.html), and [HDF5 model](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_d_m__u_g.html) already explain the exact distinction between two names for one stored object and two copies. They are very strong, directly relevant prior art, not merely loose conceptual analogues.

In the **pre-existing** HDF5, the four tested `monitor1/data` or `monitor2/data` datasets have object addresses `25224`, `4180`, `505364`, `511764` respectively, corresponding HDF5 `NXmonitor` group addresses also distinct. Each of the four inspected monitor group and data paths has **NO NeXus `target` attribute**; each monitor group has `NX_class=NXmonitor` and each data field `units=counts`. This means the inspected HDF5 metadata does **not** explicitly restore original cross-histogram alias identity. This finding is bounded to these exact objects; **absence of a target on non-linked copies does not on its own establish invalid NeXus compliance** or an invalid physical archive.

Earlier P23 source-matched **official** HDF Group `h4toh5 2.2.5` conversion retained the shared monitor aliases. Thus HDF5 as a format is not responsible for intrinsic source-alias fracture; the *producer path* for the independent pre-existing HDF5 companion remains unknown.

## 4. Adversarial verdict for the scientific claim

What the actual science files establish:
1. stored scalar arrays, named paths, date meanings and units can be identical while physical *storage linkage* is different;
2. one particular, openly specified storage-identity-based statistic is representation-sensitive;
3. per-entry measurement-value queries, all-path counting and context-conditioned content grouping are invariant in this same source pair;
4. no tested `target` attribute on the copied HDF5 monitor group/datasets supplies the historical cross-entry alias relation.

What they absolutely DO NOT establish:
- which monitor readings were statistically independent or how true beam normalization should be performed;
- source run 3701 raw `lrcs3701.run`, `PLS` acquisition physics or calibration semantics; the public `NXlrcs.f90` demonstration source is not the authenticated producer executable;
- that any actual scientist produced an erroneous inference from object deduplication;
- which institution historically adopted the HDF5 example as a source of authority or which exact converter created it;
- that a path/units preservation policy is globally insufficient for every future question;
- that NeXus/HDF hardlink behavior, content collisions, or pseudoreplication are novel discoveries.

Strong ordinary rivals win on this bounded result: NeXus/HDF link semantics, standard relational object identity and data provenance/ETL, source experiment log requirements, sample pseudoreplication and Forand option-maintenance. The case is a meaningful nontrivial *source-backed adversarial example* and methodology demonstration, not evidence for P76-specific adoption-induced irreversible loss.

## 5. Automatic P77 independent-problem scent court

Candidate label: **Evidence-Unit Identity and Query-Relative Sufficiency across Scientific Serialization**. Admissible as a *potentially interesting separate problem*, but in the present data reducible to P76's source-preserving verification options and classic provenance/schema/experimental-unit theories.

Promotion requires a genuinely independently source-authorized experimental/acquisition-unit witness (not just storage addresses) that changes an actual rival-discriminating scientific verdict across two historically adopted representations, beyond existing provenance/NeXus/ETL and pseudo-replication. Or a rigorous bounded theorem that adds a distinctive result beyond elementary graph quotient/strong bisimulation. **No such P77-discriminating world observation yet. P77 NOT OPEN.**

**P76-P27 verdict**: `ORIGINAL_PAIR_SHA_PASS / FULL_ARRAY_CONTENT_SHA_RERUN_PASS / PER_HISTOGRAM_VALUE_QUERY_INVARIANT / PATH_SUM_INVARIANT / STORAGE_IDENTITY_QUERY_2X / RUN_ROLE_FULL_CONTENT_POLICY_INVARIANT / ALL_FOUR_H5_MONITOR_TARGET_ATTRS_ABSENT / NO_SCIENTIFIC_NORMALIZATION_CERT / CAUSAL_ADOPTION_HOLD / P77_SCENT_STRONG_HOLD / PAPER_HOLD`.

No human recruitment, no paid models, no bot commits. P76 lives; no premature closing or novelty laundering.
