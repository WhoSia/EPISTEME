# EPISTEME-P77 W45 — Actual BIA Conversion Implementation, a Non-AI Baseline and a Synthetic Cache-Reuse Control

**Audit date:** 2026-11-11 KST. **Research authority:** [P77 binding strategy](../STRATEGY_P77_CURRENT.md), [G-001 provenance](../GOVERNANCE.md), [W44 missing-denominator and selection gate](p77_w44_20261109_api_selection_partial_identification_and_tlp_stop_rule.md). **P77 ACTIVE / P78 HOLD / PAPER HOLD; independent TLP originality NOT CERTIFIED**.

## 1. Exact primary-source code, actually fetched via connected GitHub

The [BioImage Archive 2026 original institutional article](https://doi.org/10.1093/nar/gkag1108) says the new infrastructure converts into OME-Zarr using **bioformats2raw**, preserving originally submitted files. We found and read additional genuine public original implementation, NOT merely a paper's architectural claim:

| Source | Observed Git blob | Actual relevant behavior |
|---|---|---|
| [BioImage-Archive/bia-converter/bia_converter/conversion.py](https://github.com/BioImage-Archive/bia-converter/blob/main/bia_converter/conversion.py) | `6d7097387990c639fab5189bc69a40a7532a5b8f` | `run_zarr_conversion` invokes an executable from configured `bioformats2raw_bin`, checks subprocess exit code; `cached_convert_to_zarr_and_get_fpath` tests whether `<image.uuid>.zarr` already exists before rerunning |
| [BioImage-Archive/bia-converter/bia_converter/convert.py](https://github.com/BioImage-Archive/bia-converter/blob/main/bia_converter/convert.py) | `a147a25e6d40c366373dc505b623fd81ff064b4d` | Original file references, multi-file T/C/Z template assembly, local Zarr cache and S3 representation objects. `convert_with_bioformats2raw_single_fileref` and multi-file conversion condition on output path `.exists()`. An additional ZIP handling branch includes an upstream TODO: verify an already cached unpacked directory matches the source archive |
| [BioImage-Archive/bia-converter/bia_converter/config.py](https://github.com/BioImage-Archive/bia-converter/blob/main/bia_converter/config.py) | `e8a436bf7a344fbdbaf4df28d3810ff72cb6c646` | Runtime executable path and output store configured separately; this is **not** a version-pinned published execution receipt |
| [BioImage-Archive/bia-converter/bia_converter/bia_api_client.py](https://github.com/BioImage-Archive/bia-converter/blob/main/bia_converter/bia_api_client.py) | `55bf4923a573372f60d98cc7b096190faab9d72c` | `store_object_in_api_idempotent` fetches object by UUID and posts only when not found, without establishing what specific original-byte or scientific-data validation was performed in the upstream call |
| [glencoesoftware/bioformats2raw README.md](https://github.com/glencoesoftware/bioformats2raw/blob/master/README.md) | `6f5e076ee83d22aaf23172cdb0ded23473a1da41` | Documented conversion flags, metadata export, format-spec version transitions and already existing scientific convertibility limits |
| [glencoesoftware/bioformats2raw Converter.java](https://github.com/glencoesoftware/bioformats2raw/blob/master/src/main/java/com/glencoesoftware/bioformats2raw/Converter.java) | `a5ed7cd5476a9654c369e29405999453616d5b83` | Original Java option definitions for `--no-ome-meta-export`, `--no-original-metadata`, deprecated `--dimension-order`, and rendering option `--no-minmax` |

**Scope limit:** These are exact public *repository blob snapshots*, not proof they equal every live production deployed container/version on 2026-11-11. No access to the institution's production job logs, conversion database or binary digest; private endpoints were not queried. Repository content alone cannot demonstrate an actual production corruption.

## 2. Provenance and idempotence are different invariants

The observed local cache path existence check is a valid *technical optimization*, but **scientific reuse of exactly the same transformation** should additionally bind:
`(input raw SHA256, converter binary SHA256, ordered effective CLI flags/configuration, OME-NGFF specification, complete output manifest/hash, independent scientific-validation receipt)`.

An unchanged output directory can coexist with a changed input file, executable, conversion flags, or specification if a cache identity only checks a directory's existence. We constructed [a read-only synthetic exact-input selftest](../analysis/p77_w45_bia_conversion_cache_contract.py), executing 4 counterfactual request variants:
- Original raw input bytes changed.
- Converter binary changed.
- Effective conversion CLI options changed.
- Target specification changed.

A *synthetic* path-exists-only classifier reuses old output in each of these four states, whereas the fail-closed bound source/converter/options/spec classifier rejects all four; the known-good request passes only when output validation passes. **Local Python selftest PASS**; this is elementary cache identity logic, **NOT** an executed trial of bia-converter against a raw microscopy sample and NOT proof the actual BIA pipeline ever used stale cached output. The public code itself includes an explicit cache-validation TODO for the ZIP source case. Therefore the risk is *documented implementation audit opportunity*, not an observed outcome.

Actual tested source-only local Python console:
```
PASS synthetic: 4 source/binary/args/spec changes blocked by sealed cache
PASS synthetic: valid unchanged output reused; invalid or absent rejected
LIMIT: did NOT run or inspect the production cache state
```

## 3. Strong negative control: already configurable metadata omission

The original [bioformats2raw README](https://github.com/glencoesoftware/bioformats2raw/blob/master/README.md) and Java code explicitly document:
- `--no-ome-meta-export` omits exported OME-XML metadata and warns it breaks `raw2ometiff` compatibility.
- `--no-original-metadata` omits source-vendor `OriginalMetadata` pairs, **expressly offered to reduce accidental exposure of unwanted experimental metadata**. This can serve a valid privacy purpose rather than constituting an error.
- `--no-minmax` omits precomputed min/max rendering information, which can affect display convenience/performance but is NOT by itself demonstrated loss of original scientific measurements.
- `--dimension-order` is deprecated and documented as potentially producing an invalid OME-NGFF layout; defaults changed across upstream releases.

The upstream [Bio-Formats original project metadata reference](https://bio-formats.readthedocs.io/en/stable/about/) distinguishes **core structural metadata**, **original format/vendor metadata**, and **OME-mapped metadata**; the mappings are explicitly imperfect. If a hypothesis needs a vendor field deliberately excluded for privacy, separate protected access to the original source may provide a permissible route while the exported public representation omits it. **Whether a particular H0/H1 becomes infeasible is a scientific/ethical/permission judgment requiring authentic data, not a consequence of detecting a CLI option.**

These controls and epistemic tradeoffs are **prior published engineering** and directly constrain any broad EPISTEME claim that an AI translation system first discovered representation-dependent science.

## 4. Research-director result / stop condition

**Strong non-AI reference demonstrated:** Actual code-based BIA conversion is implemented and uses standard scientific-image conversion rather than an assigned LLM. **Reproduction gap remains:** exact executed production binary/flag/asset manifests, processing timestamps and independent substantive image correctness not published in the reviewed public code/API, as confirmed by prior [W43](p77_w43_20261109_actual_bia_paired_image_api_negative_controls.md). **No observation of** AI translation treatment Z, time-ordered collective adoption S/X/D, or independently adjudicated feasible H0/H1 test T. An original source-visible conversion pathway and a synthetic cache counterexample do not establish independent TLP novelty.

**DO NOT** spend the P77 residency repeatedly relitigating simple BIA cache behaviour: absent an actual raw image/formats oracle, matching converter binary and production event log, the engineering audit cannot answer founding TLP. Strongest next question: can any documented research institution supply a joint converter transition + observable lab decisions + independently verified scientific test repertoire? If not, source evidence supports an explicit **NO-GO for empirical founding-mechanism claim** while P77 remains active under the binding charter.

**P77 ACTIVE / P78 HOLD / PAPER HOLD / independent originality NOT CERTIFIED.**
