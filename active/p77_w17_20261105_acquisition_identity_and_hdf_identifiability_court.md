# EPISTEME-P77 W17 — Acquisition Identity Is Not Array Equality: A Non-identification Court

**Date:** 2026-11-05 KST  
**Generation:** [official P77](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53) / [binding director strategy](../STRATEGY_P77_CURRENT.md)  
**Status:** P77 Phase 1 ACTIVE / P78 HOLD / PAPER HOLD / no novelty certified.  
**Predecessor:** [W16](p77_w16_20261105_interoperability_layer_relocation_and_p76_competitor_court.md).

## 1. Specific question and archival source status

W16 asked whether a converter changes the **actual possibility of discriminating two scientific hypotheses**, as opposed to merely changing data format. P76's archived NeXus HDF4/HDF5 result is a useful **counterexample to overclaiming**:
- [2026-10-18 EPISTEME chat archive 6 (Drive)](https://drive.google.com/file/d/1J9HYhuEEJXyLWIQicgHDbHnAWb5OzVQf/view) records direct previous-work comparisons of `lrcs3701.nxs` and `lrcs3701.nx5`: an HDF4 source has shared storage references for two histogram monitor paths (monitor1 ref 57, monitor2 ref 64); the separately distributed HDF5 counterpart has different object addresses for those paths, though the compared arrays match.
- The earlier recorded audit tested **20 paths; 16 numeric arrays matched** and four time-string representations differ. The archive also reports that the **official `h4toh5` conversion preserved object sharing** in a separate test. Therefore inability of the HDF5 format to represent shared storage is **not** established.
- An earlier provenance receipt listed `lrcs3701.nx5` size **541,008 bytes**, SHA-256 `20a65f41ddf61afd53126847c3204f069b0f5ae69880af4777e1863a2ac66ea2`; this is an **archived prior-turn receipt**, NOT a fresh download or current independent hash validation.
- Previously recorded P76 `proton_pulses = 2,268,088`, 30 Hz setting and 191,912 s interval cannot be naively converted to an accelerator duty fraction; original IPNS `PLS` counting/gating/normalization procedure is not obtained. This is distinct from logical storage-object sharing.
- [McGrath & NCSA HDF Group (2000), *Transition from HDF4 to HDF5*](https://drive.google.com/file/d/1lxBHdARPJE5FlrWLocOgAyxO1rT2RCJl/view) expressly states compatibility is relative to user goals. [Bakeev (2026)](https://drive.google.com/file/d/1cV3Q42I9uE5Ek1LpFkNtJuqB9gXc4Tqy/view) independently explains disciplinary tractability and methodological embedding.

**Evidence-grade restriction:** The direct W17 reads are the Drive chat archive and two published/original methodological papers, plus the existing W15/W16 GitHub court. The original binary NeXus datasets and prior CI job's full artifacts were **not reacquired or rerun here**. A prior-recorded real result is not a new W17 physical measurement.

## 2. Separate three identities

For two histogram monitor paths, distinguish:

1. **Numeric equality**: `x1 == x2`, which says the saved counts are equal.
2. **Storage-object aliasing**: `object(path1) is object(path2)`, which may be determined from the data container's reference/address/links.
3. **Physical acquisition identity**: did the same particular detector/acquisition event yield both count streams (or were two independent measurements later stored or coalesced)?

None is definitionally equal to the other. Numeric equality need not prove shared storage or acquisition. Shared storage does not by itself establish the physical measurement history without data-generation provenance. Separate storage does not by itself establish independent acquisitions.

## 3. Explicit H0/H1 and falsifiability

- `H0`: histogram paths reuse **the same physical measurement**.
- `H1`: histogram paths originate from **independent physical measurements**, which happen to have the same saved count vector.

**Observed input `O`:** identical numeric arrays for both paths, with separate HDF5 dataset objects. `O` does **not** distinguish `H0` from `H1` unless an external acquisition-linked identifier, measurement-time record, source-file map, event provenance or sufficient statistical independence evidence is supplied. Exact equality could be unlikely under a suitable independent-count model, but without the model and original event records one must not call it physically impossible.

**Additional point:** Even knowing that the earlier HDF4 container had an aliased storage object would not logically exclude a producer that coalesced two equal independent measurements before writing. The historical `NXlrcs.f90` and `PLS` provenance, not storage format alone, is needed.

## 4. Constructive non-identification example (SYNTHETIC, not physical data)

[Source code — two-world observational-equivalence fixture](../analysis/p77_w17_synthetic_observational_equivalence.py) has two worlds: `shared` with numeric vector (3,5,2) reused, and `independent` with independently acquired but equal vector (3,5,2). A hypothetical converter duplicates the output as two storage objects without acquisition provenance. Both worlds produce **exactly the same observable record**. A data-only classifier returns the same label for both.

**Actual local execution:** `python /tmp/episteme_w17_identity_fixture.py` completed all assertions:
- `PASS: 2 distinct acquisition histories -> 1 identical exported record`
- `PASS: equal-prior identification accuracy bound = 1/2`
- explicit warning that no original NeXus dataset or real format converter was executed.

Formal statement under *this constructed deterministic equal-prior two-world model*: with `f(H0)=f(H1)=o`, any estimator `delta(o)` cannot correctly classify both worlds. Under prior probabilities 1/2, the best achievable classification accuracy from `o` is exactly 1/2 (equivalent error >= 1/2). This is **elementary identifiability/observational equivalence** and cannot be promoted as a novel theorem. For arbitrary real data distributions, Bayes error depends on distributional overlaps and priors; W17 makes no universal 1/2 claim.

This illustrates why the well-established information-loss and provenance framework defeats the generic EPISTEME sentence 'the converter preserved the values so the scientific test survived.' It is not a demonstration that the historical NeXus conversion caused a lost scientific test.

## 5. Direct competitors, negative controls, and falsification criteria

| Candidate explanatory statement | Strong rival / control | W17 assessment |
|---|---|---|
| Format preserves counts | Original P76 16-array numeric equality, HDF format documentation | **Archive-supported** within recorded scope |
| Format preserves original storage aliases | Original distributed HDF5 differs; official h4toh5 preserves | **Not universal; path-dependent** |
| Storage aliases prove shared physical measurement | Distinct measurement/source provenance; storage coalescence counterexample | **Not identified** |
| Format conversion caused a specific inability to test H0 against H1 in real physics | Need original acquisition log, test hypothesis, detector model, alternate pipeline | **Not established** |
| EPISTEME offers a new account beyond ordinary information loss/traceability, Bakeev, McGrath and MQR | Need independently predicted effect that these theories cannot explain | **No novelty certified** |

**Negative control:** The previously archived official `h4toh5` conversion preserved aliases. This rules out any careless claim that migration to HDF5 is *necessarily* destructive of alias topology. It does not show that the separately published HDF5 file was generated by that same exact conversion procedure.

## 6. Genuine future test requirements — no fictional experimental success

To advance beyond textbook non-identifiability and implementation audit, obtain at minimum:
- an original acquisition-level indicator/log explaining `PLS`, monitor reuse and gating, plus actual producer code/version or authenticated converter lineage;
- a concrete physics hypothesis pair and **test statistic or downstream inferential decision** that makes different predictions under those source histories;
- benchmark against **official alias-preserving h4toh5 conversion** and source HDF4 readers, not a deliberately lossy format-only strawman;
- error/reliability controls, alternate retained paths, and a source-backed result that **established competitors fail to explain**.

**Next W18:** Given the 12-week director mandate, do **not** spend the whole stage chasing this one HDF case. Return to the founding AI-conversion/standard adoption path and test an *equal-constraint rival model* where conversion makes some outcomes more likely, rather than manufacturing a new epistemic term. Keep W17 as an adverse negative witness in the source matrix.

## 7. Missing literature and decision

Unverified-as-held: Rosero Abad et al. (2026) DOI 10.59490/jos.2026.8038; Janssen et al. (2026) DOI 10.1002/adem.71258. Nonpriority LEP history debt: CERN Management Board 2000-12-07; LEPC 2000-11-03 and Research Board 2000-11-07 original decision minutes. Marro & Torr 2026 is **held in Drive 10_PAPERS** and is not missing.

**Decision:** P77 active, no P78, no paper. W17 is a **formal and source-backed negative control, not an independent discovered mechanism.**
