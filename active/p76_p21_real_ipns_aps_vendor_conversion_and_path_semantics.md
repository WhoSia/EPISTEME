# EPISTEME-P76-P21 — Real IPNS/APS Instrument-Source HDF4→HDF5 Vendor Conversion and Scientific Variable Identification

**2026-10-17 KST | P76 OPEN | P77 promotion watch ON, NOT OPEN | PAPER HOLD.**

## Real source and executable receipt

[Authentic upstream source-byte and conversion court, GitHub Actions #39041975405 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39041975405). Code: [src/p76_p21_real_neXus_hdf4_instrument_vendor_court.py](../src/p76_p21_real_neXus_hdf4_instrument_vendor_court.py); [workflow](../.github/workflows/p76_p21_real_instrument_vendor.yml). No GitHub Actions bot commits, workflow contents read permission.

- Original source repository `nexusformat/exampledata` fixed commit `eae516807ef7e27d1c45aab3af3a64a679154677`.
- IPNS `IPNS/LRMECS/hdf4/lrcs3701.nxs` 115770 bytes original SHA256 `8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39`; native `hdp dumpsds` exit 0, official HDF Group h4h5tools 2.2.5 vendor converter exit 0, HDF5 `h5dump -H` exit 0.
- APS `APS/CCDImageServer/hdf4/Smither400.3_apr0300051.hdf` 568977 bytes original SHA256 `f67d40f0cef33c6d0336fcc012d8940d2dc8b58767f36d7468faf4b5a11c34c7`; native `hdp dumpsds` exit 0, vendor converter exit 0, converted HDF5 `h5dump -H` exit 0.
- Vendor archive `h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz` from HDF Group official distribution verified against publisher .sha256 before temporary self-extractor invocation; no permanent system changes.
- The ANSTO path found HDF5 (despite /hdf4 folder) at P20 remains excluded from HDF4→HDF5 denominator, never presented as third original HDF4 conversion.

## Original instrument science fields (actual hdp output)

IPNS `lrcs3701.nxs` has native attrs: `NeXus_version=2.0.0`, `HDF_version=NCSA HDF Version 4.1 Release 3, May 1999`, `file_time=2002-10-08 23:25:42-0600`, user `EAG/RO`. Its `title` value reads `MgB2 PDOS 43.37g 8K 120meV E0@240Hz T0@120Hz`. Original named SDS include `time_of_flight`, `polar_angle`, `distance`, `gas_pressure`, `energy`, `proton_pulses`, `frequency`, `target_material`, `moderator`, and multiple identically named `data` entries and `time_of_flight` entries. Vendor HDF5 hierarchy visibly contains matching names at multiple paths plus generated `fakeDim*` dimension-scale data sets. Names repeat across distinct scientific group paths: **must never match `data` merely by basename** or infer that all duplicates have a shared physical meaning.

APS `Smither400.3_apr0300051.hdf` native attrs `NeXus_version=1.3.2`, `file_time=2003-04-15 16:39:47-0600`, `facility_name=APS`, `program_name=CCD Image Server`, program version `V1.7.3`. Source SDS include `data`, `A2_thc`, `A2_thf`, `PI_500_PZT2`, program author and start_time. Converted vendor HDF5 lists these names in its actual paths; physical meanings of specific motor channels must not be guessed beyond what original metadata demonstrates.

## Scientific question that is now nontrivial

The P20 science records have multiple homonymous SDS names and layered NeXus group context. **The scientific object is not basename-preserving conversion**: it is a *group-scoped, semantically typed path*, preserving original measurement value plus coordinate/units and instrument relationship. For an IPNS time-of-flight spectrum, scientific equivalence demands that original time-of-flight axis and a particular detector-scoped data group, including units and original sample/environment context, continue to denote the same observation. For APS CCD image it requires detector intensity pixels, sample or acquisition time and instrument metadata. These are hypotheses/prospective comparisons; no numerical semantic equivalence verified yet.

Strong prior-art rivals include NeXus scientific file conventions, standard HDF4→HDF5 conversion and HDF5 dimension scales, established HDF provenance, Duerr layout reader, Forand verification options, and conventional namespacing/type checking. Without different predictions from these prior models, P76 and especially P77 novelty remains unproven.

## Evidence hierarchy and next fatal test

1. **Now observed:** real source bytes hashed; native original fields and contents partly inspected; official vendor conversion succeeded 2/2; produced hierarchical HDF5 dataset names; HDF5 headers valid.
2. **NOT YET observed:** 1-to-1 correspondence of original and new *path-qualified* scientific values; full units, uncertainty, event metadata, instrument transformations; scientific inference result after migration; historical institutional *adoption* of representation; endogenous future challenge loss.
3. Freeze just one IPNS primary detector `data` + its matching `time_of_flight` axis with group path and units taken directly from original NeXus metadata; compare old and new arrays and scientific query. If ambiguous, pick APS instrument CCD `data` path with actual source path IDs.
4. A negative new-format result must be opposed by archived native-read path; if native original works, global irreversible scientific defeat loss fails for the tested query.

**P77 auto-court:** Scientifically important identity collision across same-named data groups may reveal an audit of group-dependent observational reference. But source hierarchies and NeXus path-typed scientific identities are conventional prior art, and P76 already includes representation-dependent query executability. `P77_SCENT / REDUCIBLE_TO_P76 / NOT_OPEN`.

**Final status:** `P76_P21_REAL_IPNS_APS_VENDOR_CONVERSION_2_2_PASS / NATIVE_FIELDS_RETRIEVED / NUMERICAL_QUERY_HOLD / EXPERIMENTAL_ADOPTION_CAUSALITY_UNSHOWN / PAPER_HOLD / NO_HUMANS_OR_PAID_MODELS`.
