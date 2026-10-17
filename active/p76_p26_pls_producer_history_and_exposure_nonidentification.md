# EPISTEME-P76-P26 — LRMECS PLS Source Contract, Hard-Coded Frequency and Historical Exposure Nonidentification

**2026-10-18 KST | P76 OPEN | P77 automatic promotion watch ON, NOT PROMOTED | PAPER HOLD**

## Actual source and reproducible execution

- Pinned NeXus original scientific instrument HDF4 source: `nexusformat/exampledata`, commit `eae516807ef7e27d1c45aab3af3a64a679154677`, `IPNS/LRMECS/hdf4/lrcs3701.nxs`, 115,770 bytes, SHA-256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`. Originally validated P20–P25, downloaded and rehashed this P26 run.
- **Primary producer source**: NeXus wiki raw file [`source/content/NXlrcs.f90.md`](https://github.com/nexusformat/wiki/blob/ca703eda4dd2ca7fe3460011206fe90eef752179/source/content/NXlrcs.f90.md), commit `ca703eda4dd2ca7fe3460011206fe90eef752179`; downloaded bytes SHA-256 `36504eb5a68b241050d42f87f2e6917ac6ced82dc634d2df2e9dc6bf3a09dc6a`. Separate rendered page https://www.nexusformat.org/NXlrcs.f90.html inserts anomalous whitespace into literal `30.0` (`3 0.0`), while raw primary Markdown has valid `30.0`. Text rendering is NOT a byte-true transcription.
- [CI successful source-specific replay #39049351127](https://github.com/WhoSia/EPISTEME/actions/runs/39049351127) with [exact code](../src/p76_p26_ipns_pls_producer_contract_court.py) and [read-only workflow](../.github/workflows/p76_p26_ipns_pls_contract.yml). An earlier [run #39049086744](https://github.com/WhoSia/EPISTEME/actions/runs/39049086744) FAILED because the first audit's string filter excluded the exact root path `/Histogram1`, `/Histogram2`, which contain start and end date fields. Those dates are **HDF4 SDS**, as previously proved by P24. An initial intermediate conjecture that they were Vdata was wrong; the corrected program includes both root group and descendant groups. Do not misclassify source semantics based on parser bugs.
- GitHub workflow `permissions: contents: read` and produces receipt artifact; no bot commits. This new source-only court does not run the HDF4→HDF5 conversion again: P22–P24 already did matched source and vendor semantics.

## PLS acquisition-source authority: the missing definition

Verbatim original producer call sites:
```fortran
call get_IPNS_item ("PLS", int_value)
if (NXUwritedata (file_id, "proton_pulses", int_value) /= NX_OK) stop
if (NXUwritedata (file_id, "frequency", 30.0, "Hz") /= NX_OK) stop
```

This **proves** the described public producer code emits an integer from an external IPNS `PLS` key and records a literal 30.0 Hz source field. It does **NOT** define which accelerator pulses `PLS` includes or whether it is accepted monitor gates, beam-on delivered pulses, logged commanded pulses, effective proton charge, fluence or physical normalization. The *source* frequency in this public code is a hard-coded number, **not** a measured time series. The current original HDF4 file matches this metadata setting; that concordance does not authenticate the exact producer executable run that wrote archived bytes. The raw `IPNS_module` implementation (and original `lrcs3701.run` source log) was **not recovered** by this targeted original NeXus/GitHub search, and was not proven permanently nonexistent.

Original source and old reader P26 exactly:
- Histogram1 and Histogram2 start: `2001-02-07T08:54:21-0600`; end: `2001-02-09T14:12:53-0600`; elapsed wall clock **191,912 seconds = 53 h 18 min 32 s**.
- Each has original `proton_pulses` **2,268,088**, stored in two distinct HDF4 SDS refs 22 and 91, with no local `units` attribute.
- Each has `frequency` **30.0 Hz**, original SDS refs 28 and 97, local `units="Hz"`; this field is consistent with **producer fixed metadata**, and with NeXus [NXsource schema](https://manual.nexusformat.org/classes/base_classes/NXsource.html) describing the radiation-source frequency, not a guarantee of continuously delivered good pulses for all wall time.
- `30.0 Hz × 191,912 s = 5,757,360` is a **hypothetical continuous source-pulse count**, not a measured observation.
- `2,268,088 / 191,912 = 11.818375088582266` stored pulses / wall-second.
- `2,268,088 / 5,757,360 = 0.39394583628607555`. **This is NOT an empirically identified 39.4% beam duty factor, delivered-neutron fluence, or a valid normalization efficiency**. Unknown timestamp semantics, source field meaning, pulse selection, accelerator operation and sample/detector live-gating admit many rival explanations. The numerator's dependence on `PLS` and physics calibration is unidentified.

## P9/P10 and PEA-Scope method transfer

The *same* file can carry raw counts, times, a seemingly descriptive source-frequency scalar, and measured monitoring object links yet **not suffice to identify a future physical interpretation**. A later independent acquisition log could license a formerly unresolved query. This is a source-specific instance of P9's fixed-task sufficiency versus P10's endogenous future question set, not an independent EPISTEME theorem.

PEA-Scope M37/M66 taught that another workflow, extra model, or missingness pseudo-score is not a research result. Here one original-source cross-check and a minimal read-only court are sufficient to establish:
- **Identified:** source semantics of the serialization key `PLS` as opaque fetched integer; fixed NeXus `frequency=30.0 Hz`, archived values/times, shared monitor source-object references P25.
- **Not identified:** meaning of physical good beam pulses, active exposure duration, accelerator proton charge/current, accepted counts normalization, exact original input `.run` data and exact compiler binary.
- **Not permitted:** assign counts-per-pulse rates as neutron cross-sections, statistically independent experimental replications, or interpret the 0.394 ratio as a measured duty factor.

## Scientific rival and automatic P77 promotion

Classical NeXus NXsource/NXmonitor metadata, HDF producer code, instrument operational logs, missing/latent measurement calibration, observational pseudoreplication (Hurlbert), provenance and Duerr's independent reader all explain this boundary; P76 itself already studies missing evidence-generating options.

**P77 scent:** “nominal metadata masquerading as observed exposure” might be an appealing label. But P26's primary producer proves the original field is a **hard-coded source descriptor**, while the file stores a separate counter. The difference is existing scientific data provenance and measurement-model identification, reducible to P76's authority-conditioned future verification question. `P77_SCENT=OBSERVED_BUT_REDUNDANT / P77_PROPOSED=FALSE / NO_P77`.

A future genuinely new candidate would require a source-specific *experiment* showing that two retention/producer-history regimes with equivalent conventional provenance-and-option state diverge on a legitimate future rival-defeating physics query, with alternative standard models actually failing. Neither the current original file nor converter tests establish that.

## Disposition and next bounded action

**P76-P26** `PRIMARY_PRODUCER_MARKDOWN_SHA_PASS / TRUE_SOURCE_30HZ_AND_PLS_PASS / WALL_TIME_CONDITIONAL_DISCORDANCE_OBSERVED / PLS_PHYSICAL_DEFINITION_NOT_FOUND / EXACT_GENERATOR_BUILD_NOT_AUTHENTICATED / P77_HOLD / PAPER_HOLD`.

Next narrow gate: seek the IPNS native run-file header semantics / `IPNS_module` `PLS` definition and an actual LRMECS run-specific beam gate, then precommit a scientifically legitimate normalization formula. If unavailable under bounded search, retain honest nonidentification and investigate a different source-qualified real scientific challenge rather than endless producer code chasing. No new humans or paid provider calls.
