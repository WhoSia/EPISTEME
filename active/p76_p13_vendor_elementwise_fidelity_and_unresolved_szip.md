# EPISTEME-P76-P13 — Official Vendor Elementwise Query Preservation Court

Date 2026-10-17 KST. Stage BOUNDED_PASS, open SDSszip source numeric oracle, PAPER HOLD.

## Genuine execution

CI SUCCESS https://github.com/WhoSia/EPISTEME/actions/runs/39026406568 commit 0085d84ab8fb25bd27dc43710e037819193c36d6. Run executed Python https://github.com/WhoSia/EPISTEME/blob/main/src/p76_p13_vendor_elementwise_semantics.py . Original HDF Group hdf4 commit 2c46ad56bea5aab05e996e473a81dcbd9a66b125; publisher SHA-matched official h4h5tools 2.2.5 binary. Original raw SHA-256 checks matched both presealed HDF4 source files.

Actual original native hdp dumpsds text vs converted official vendor HDF5 decoded by h5py. The comparison uses hdp *decimal rendering*, not a bit-identical old-file raw-value extraction; this is a bounded numeric-result comparison, not proof of every original float bit's fidelity or scientific meaning.

| Source SDS | Original scalar type | New HDF5 type | Dimension | Element-wise numeric result |
|---|---|---|---|---|
| SDStemplate | float32 | >f4 | 9x6 | 54/54 equal, sum 15700 both |
| SDSgzip | int32 | >i4 | 16x5 | 80/80 equal, sum 840 both |
| SDSskiphuff | int32 | >i4 | 16x5 | 80/80 equal, sum 840 both |
| SDSszip | original text reader did not emit complete array | >i4 | converted 16x5 | UNTESTED old-vs-new values |

Observed element-equality denominator is 214/214 eligible decoded samples; the source contains 4 SDS datasets totaling 294 elements (if source SDSszip shape 16x5 confirmed by HDF native metadata) and 80 source bytes' decoded values remain unsupported by current oracle. Hence NEVER claim 294/294 or four-of-four semantic preservation. Converted dimension-scale datasets and DIMENSION_LIST attrs exist, but full semantic fidelity of old-scale metadata not independently established.

Failed CI attempts #39026278615 (vendor binary basename case), #39026339764 (tool lookup selected header file instead of executable) are implementation problems, preserved rather than erased. First successful #39026406568 uses same selection predicate known successful at P12.

## Scientific boundary

This is strong evidence against attributing the h5utils compressed-input failure to inherent source format nonconvertibility; official vendor converter preserved measured scalar values/dtype of all three testable SDS, and retains an original HDF4 read route. No actual physical measurement or scientific falsification source/authority is evaluated; no identified representation-dependent irreversible loss; no novel theorem. Next execute genuine independent native-reader audit for SDSszip rather than increasing formal theory. PAPER HOLD, no new human recruitment, no paid API.