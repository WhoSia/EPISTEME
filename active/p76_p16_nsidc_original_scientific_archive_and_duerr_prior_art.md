# EPISTEME-P76-P16 — Original Observation Migration Ecology: NSIDC-0397, MODIS and Direct Prior-Art Threat

2026-10-17 KST. **SCIENTIFIC ARCHIVE IDENTIFIED / HTTP SOURCE INDEX FETCHED / RAW SCIENCE HDF4 BYTES NOT DOWNLOADED / SCIENCE-QUERY EXPERIMENT NOT DONE / PAPER HOLD**.

## 1. Strongest unexpected primary archive and prior art

**Duerr & Crider (2010), NSIDC-0397: HDF4 Data Used to Assess Long-Term Access to Remote Sensing Data with Layout Maps, v1**. Official https://nsidc.org/data/nsidc-0397/versions/1 ; DOI https://doi.org/10.5067/P1B2VYBCJ95O . This is authentic historical scientific HDF4 observational data *samples from NASA eight data centers*, archived for a study of complex internal bytes, layout mapping, and alternate direct readers. The NSIDC description says maps permit reading without the original HDF API. Original external source archive https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0397_HDF4_Sampler_v01/ . Official freely accessible source background PDF https://nsidc.org/sites/default/files/nsidc0397_duerr_longterm_access.pdf .

**Direct very strong existing original publication** Duerr, Cao, Crider, Folk, Lynnes & Yang (2009), *Ensuring Long-Term Access to Remotely Sensed Data With Layout Maps*, IEEE Trans Geoscience and Remote Sensing 47(1), 123–129, DOI https://doi.org/10.1109/TGRS.2008.2004626 . The original study describes *two independent reader tools* built from an HDF4 layout map instead of relying on the standard HDF API. This is directly fatal prior art to any would-be P76 claim that mapping science file layout to recover independent old-format read routes is a new idea. The HDF4map schema and independent Python map reader also documented by US Library of Congress https://www.loc.gov/preservation/digital/formats/fdd/fdd000327.shtml .

**Drive search**: keywords `NSIDC-0397`, `Duerr`, `Ensuring Long-Term Access` returned no matching exact original research/source items (unrelated homonyms appeared). Search-based not complete inventory proof. IEEE publisher OA fulltext not verified: user should receive DOI/publisher page, NOT made-up free PDF. NASA NSIDC background PDF is officially downloadable free.

## 2. Reproducible direct original source access attempt

[Read-only GitHub CI #39033612833 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39033612833), run on GitHub-hosted Ubuntu for [P76-P16 source directory script](../src/p76_p16_nsidc_scientific_original_inventory.py). NSIDC source directory HTTP=200, response HTML=10959 bytes SHA256 `403829810d3f05dbc467e46e8899feddebc1911fb1ca16b08b623811b12b9a13`, but our static same-host anchor parser found **zero candidate file links**. Zero parseable links ≠ evidence archive contains zero files; the response may be client-side UI, access landing page or other HTML. We did **not** download a scientific source HDF file or SHA-pin it, and did not carry out HDF4/HDF5 observable scientific question comparison. CI success is only successful completion of bounded source-index probe.

Additional real scientific remote-sensing candidate: NASA MODIS/Terra `MOD021KM` Earth-observation calibrated radiance HDF-EOS granules, official https://data.nasa.gov/dataset/modis-terra-calibrated-radiances-5-min-l1b-swath-1km-0e7cd and LAADS directory https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/61/MOD021KM/2016/182/ . The LAADS directory lists many original `.hdf` granules 60–170 MB and provides explicit Earthdata bearer token instructions. **Authentication required to download the granules**; no user credentials or tokens have been requested, scraped or used. For security and source custody, do NOT fake original download evidence or ask user to paste secret credentials into chat. A future user-initiated Earthdata token connection should use a safe approved workflow, or find existing legal public mirror.

Another original publicly registered observational dataset: NASA MASTER airborne L1B original HDF4 and L2 HDF5 for certain field studies e.g. https://github.com/awslabs/open-data-registry/blob/main/datasets/nasa-master.yaml . However HDF4 L1B and HDF5 L2 are **different processing levels**, not direct file-format conversions. They cannot be used as interchangeable old/new representations of the same scientific value without verifying the real transformation and its uncertainty calibration.

## 3. New research decision: prior-art shock and origin return

NSIDC-0397 is both a potentially ideal real-data archive **and extremely strong classical rival**: the very strategy 'independently restore a past scientific verification route by layout mapping' was already designed and tested by Duerr et al. Thus a new P76 result must show something beyond data recoverability of HDF4 layouts: a genuinely source-authorized future rival-discriminating scientific question, with historical representation adoption and feasible-cost counterfactuals, that strong full existing mapping+PROV+option-retention theory cannot explain. No general claim of intrinsic irreversible epistemic lock-in survives just from unavailable modern reader/format conversion.

For next experiment, first get one NSIDC-0397 actual source archive file with publisher provenance and SHA (if index accessible, do not fabricate). Freeze an original scientific query grounded in original instrument metadata and calibration, compare native old API, independent layout-map reader, official h4toh5+HDF5, and archived original-source rerun. Test preservation and loss conditional on feasible reader/tool paths, not product deprecation alone. If NSIDC listing remains unavailable, choose another authentic low-friction NASA/HDF observational source rather than building endless index parsing machinery.

## 4. Full status

`P76_P16_SCIENCE_SOURCE_PRIOR_ART_DISCOVERED / OFFICIAL_INDEX_HTTP_200 / INDEX_FILES_ZERO_PARSEABLE / SCIENCE_BYTES_SHA_NONE / NO_SCIENCE_TEST / NEW_CAUSAL_MECHANISM_NONE / NO_HUMAN_RATERS / NO_PAID_CALLS / PAPER_HOLD`.

This stage justifies continuing EPISTEME while rigorously demoting naive 'independent fallback decoding' novelty; PEA-Scope-style premature Lab shutdown or endless CI pipeline growth are both unacceptable.
