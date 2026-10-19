# Paper 2 — What Does Scientific Serialization Preserve? A Source-Verified NeXus Case of Query-Relative Equivalence

**EPISTEME Writing Loop 2 — Draft v0.1, 2026-10-20. NOT SUBMISSION READY.**  
**Type:** methods and reproducibility case study.  
**Status:** P27 source-backed result / P28 three-way prospective verification pending / PAPER HOLD.

## Abstract

Whether a scientific data conversion preserves evidence depends on the question posed to the data. We examine an archival LRMECS NeXus example that exists both as original HDF4 data and as a separately distributed HDF5 companion. Source-authenticated byte hashes and native readers establish equality of the observed numeric arrays and scientific paths examined in the previous P27 court, including semantically equal timestamps and units. Yet the original HDF4 uses two shared stored monitor arrays across four named paths, whereas the archival HDF5 copy uses four distinct HDF5 objects. Summation over all named paths produces the same 356,242 integer counts in both files; summation once per native storage object produces 178,121 in HDF4 but 356,242 in the historical HDF5. Neither rule is an authorized neutron-flux estimator. An earlier independently sourced official HDF4-to-HDF5 conversion preserved the sharing relation, so the divergence is not a necessary property of HDF5. We use the case to specify preservation claims relative to query languages, equivalence relations and required provenance. The results are anticipated by mature NeXus link semantics, database provenance and experimental-unit theory, and do not yet support a novel physical or historical causal conclusion.

## 1. A false sense of completeness

Data migration audits often privilege checks that can be automated across a large directory: were the expected paths created, did values match, did units survive? These checks matter. They may still leave open whether two path names refer to one object or to separate copies. Conversely, the presence or loss of object sharing need not matter for every scientific question. Query choice must come before claims of equivalence.

This paper begins with a controlled but publicly distributed source pair, not a hypothetical converter bug. The original HDF4 data and the companion HDF5 appear at a pinned revision of the NeXus exampledata archive. The companion's original generator and institutional adoption history are not authenticated. We do not assume that its creation involved the official modern converter.

## 2. Source custody and controlled facts

Pinned upstream revision: eae516807ef7e27d1c45aab3af3a64a679154677. HDF4 original lrcs3701.nxs SHA-256 8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39. Existing companion lrcs3701.nx5 SHA-256 20a65f41ddf61afd53126847c3204f069b0f5ae69880af4777e1863a2ac66ea2.

P27's original pair audit established 20 exact scientific paths, 16 elementwise numeric-array comparisons, four semantically equal time values and semantically equal decoded units. Two original monitor SDS references, 57 and 64, are each reachable from Histogram1 and Histogram2. The companion HDF5 instead has four distinct addresses for those four paths.

Across each histogram, monitor1 sums to 146389 and monitor2 to 31732. These integers are real file contents. No new physical measurement is claimed.

## 3. Four queries and their answers

Q0 asks for the value of a named monitor at a named histogram. Both formats agree.

Q1 sums every monitor data path, independent of source-storage aliasing. Both formats yield 356242.

Q2 uses the native file's stored-object identity as a deduplication key. HDF4 yields 178121 and the historical HDF5 companion 356242. This is intentionally an address-sensitive bookkeeping diagnostic, not a physical exposure estimate.

Q3 groups by run number, monitor role and the SHA-256 of every canonical int32 value. Both formats yield 178121. This operational signature is useful for finding matching recorded arrays but does not demonstrate equal physical acquisition episodes. Two independent acquisitions could yield equal arrays; a shared acquisition could be represented by different transformed arrays.

Thus neither unconditional 'preserved' nor unconditional 'not preserved' is a complete description. We must say which question, normalization, interpretation and equivalence relation are intended.

## 4. The third representation as a negative control

The official HDF Group h4toh5 v2.2.5 conversion examined previously in P23 retained the original monitor aliases. This refutes the overbroad claim that the HDF5 format necessarily breaks the source relation. P28 now predeclares a new three-way court among (A) pinned original HDF4, (B) separately distributed historical HDF5 and (C) a freshly vendor-generated HDF5 copy. Its code and read-only CI are installed, including a fresh native-HDF4 P27 receipt gate. However the P28 CI run, execution logs and artifacts are not yet independently authenticated. Therefore this manuscript does **not** report its predicted three-way outcome as completed P28 evidence.

## 5. Equivalence is relative to admissible queries

Let R and R' be two representations and let Q be a frozen set of admissible queries. Define R equivalent-to R' relative to Q if every q in Q has the same semantically interpreted answer on R and R', under the chosen observation contract. Q0 and Q1 cannot distinguish these two files; Q2 can. The stronger equivalence thus requires an explicit query language and an authoritative interpretation of object identity.

This is a basic relational idea, not a claim to have discovered a new theorem. NeXus documents hard links and source targets. Ordinary database provenance explains why values and lineage are different invariants. Experimental design warns that a stored object cannot be equated with an independent physical observation. The technical contribution, if any, must lie in a more rigorous and inspectable scientific migration audit with genuine source-side evidence, not novelty claims about aliasing.

## 6. The scientific authority gap

A physical normalization requires an acquisition definition and calibrated observational unit. We do not have the original DAQ definition of the archived PLS pulse counter, monitor gates or creator provenance of the companion HDF5. Dividing proton pulses by nominal 30 Hz and elapsed wall time would not establish accelerator uptime. Likewise, replacing native link equivalence with content hashes does not recover physical independence.

The ability to execute Q2 establishes that a *storage-sensitive* query can change across archived representations. It does not show that a real researcher made a wrong inference, that a true rival was rejected, or that an institution lost its capacity to test a theory. Those are separate, unsatisfied evidence burdens.

## 7. Discussion

The preservation contract useful for one task may be uninformative for another. Scientific archives should be able to explain both the operations under which they are equivalent and the questions for which a conversion has not been verified. An apparently complete path-and-value comparison can coexist with a broken storage-identity relation; a successful official converter can, in turn, defeat claims of inevitability.

The next step is to observe, not assume: verify P28's fresh official conversion, authenticate its execution and identify one physically legitimate LRMECS question with acquisition provenance. If none can be grounded, this remains a bounded reproducibility case.

## References and materials

- NeXus design and hard-link semantics: https://manual.nexusformat.org/design.html
- NeXus exampledata pinned source: https://github.com/nexusformat/exampledata/tree/eae516807ef7e27d1c45aab3af3a64a679154677
- EPISTEME P27 court: ../active/p76_p27_alias_query_invariance_and_p77_independence_court.md
- EPISTEME P28 preregistration: ../active/p76_p28_acquisition_unit_identifiability_and_three_representation_court.md
- NeXus NXmonitor class: https://manual.nexusformat.org/classes/base_classes/NXmonitor.html
- Hurlbert (1984), Pseudoreplication. https://doi.org/10.2307/1942661

## Next writing loop

Insert **actual P28 CI artifact** only after authenticated run; add a formal finite query-algebra table and independent validator; retrieve historical generator and physical acquisition source before any scientific-meaning claims. **Paper hold.**
