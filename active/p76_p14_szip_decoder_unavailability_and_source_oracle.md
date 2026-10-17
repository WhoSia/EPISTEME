# EPISTEME-P76-P14 — SZIP Native-Decoder Unavailability as a Route-Specific Oracle Gap

2026-10-17 KST. CI SUCCESS https://github.com/WhoSia/EPISTEME/actions/runs/39026619238 ; not a completed SZIP value-preservation verdict.

## Direct diagnostic result
Original bytes source SHA `2c46ad56bea5aab05e996e473a81dcbd9a66b125`, `sds_compressed.hdf` SHA-256 `bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb`.
Native `hdp dumpsds` independently decodes GZIP SDSgzip 80 entries and SKPHUFF SDSskiphuff 80 entries, but prints exactly `<SZIP library is not available>` and `<Unable to read SZIP compressed data>` instead of SDSszip 80 values. Header still discloses `SZIP`, `Bits per pixel = 32`, `Pixels = 80`, rank2 dims 16x5.
Official HDFGroup h4h5tools 2.2.5 conversion produced an HDF5 dataset `SDSszip` 16x5 int32; the P13 output confirms its presence and type, NOT equivalence to original values.
Therefore P13's 214/214 compared entries remain legitimate, while SZIP original-vs-converted 80-value oracle remains UNKNOWN. This is a **missing codec in one original reader**, not demonstrated source loss, failure of publisher conversion, or a P76 causal irreversibility result.

## Next discriminating check
Use an independently version-pinned HDF4 reader built with working SZIP decoding (e.g. an actual HDF4+libaec/libsz runtime validated on SZIP dataset) on the same original SHA-pinned 3945-byte source and compare all 80 native decoded int32 values against vendor HDF5 values. Validate actual codec loading and the `hdp` error disappears; do not declare success based only on package installation. If independent HDF4 SZIP path unavailable, mark source-dependent oracle censored, not scientific loss.

## Historical-method link
PEA-Scope M22–M30 composition / outcome-dependent censoring: excluding unreadable SZIP from denominator is wrong for a global fidelity estimate; interpreting it as numeric mismatch is also wrong. R/A/G/I/X remains diagnostic tags, and a route-specific missing codec cannot stand for global defeat-capacity extinction. No human recruitment, paid calls, paper promotion, new theorem or P77. P76-P14 DIAGNOSIS PASS / ORIGINAL SZIP VALUE EQUALITY HOLD / PAPER HOLD.