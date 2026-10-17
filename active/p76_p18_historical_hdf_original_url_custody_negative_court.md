# EPISTEME-P76-P18 — Historical MODIS Download Boundary: Embedded FTP Source URLs, Negative Byte-Custody Court

2026-10-17 KST. P76 research continues; PAPER HOLD.

## Actual evidence
Read original public HDF-EOS LAADS MOD publisher science source summary PDF https://hdfeos.org/zoo/Data_Collection/LAADS_MOD.pdf, SHA256 `42b175fea5ab5b23ce725d45aed70180716ec410654a59a8b335b4b02794822c`; its embedded clickable links genuinely identify publisher historical FTP paths and original NASA FTP paths. GitHub CI [#39038744551 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39038744551) recovered **34 embedded PDF target hyperlinks**, including named MOD021KM Level 1 original radiance file 42 MB, geolocation MOD03, and smaller MODASRVN grid observation 553 KB; not all those are valid/live HTTP links. PDF target recovery is discovery of historical references, not proof original scientific bytes remain fetchable.

Small-file original source candidate was `MODASRVN.Arica.A2000055.1525.005.2008161234032.hdf` (historical Terra MODIS auxiliary data, 553 KB, science fields `SolarZenith` and `Albedo`, NOT the P17 MOD021KM calibrated radiance product). We deliberately selected a smaller **different physical query** for source-acquisition feasibility; must not promote MODASRVN result to radiance-equivalence experiment.

GitHub hosted independent read-only [source access probe #39038824678 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39038824678) attempted four explicit http(s) adaptations to original publisher FTP link, with strict HDF4 magic bytes `0e031301` and 2.2 MB cap:
- Historical `ftp.hdfgroup.uiuc.edu` over HTTPS: DNS name lookup failed.
- Official support.hdfgroup.org `/ftp/pub/outgoing/NASAHDFPOOL/LAADS/MOD/...`: HTTP 404.
- HDF-EOS `/zoo/LAADS/MOD/...`: HTTP 404.
- Modern NASA LAADS adapted URL: HTTP 200 but returned text/html (10833B SHA256 `3235e0e499422c9ed4d2bfed9fe001238ca5b3bae5b437c5d2ae64721222a5bc`), **not original HDF4**; login/directory HTML cannot be mistaken for data.

Result: `raw_observation_custody=false`, `radiance_query_executed=false`. NOT an observation that scientific information is irreversibly unavailable; four historic URL probes are not all feasible tools, all mirrors, institution archive paths, or download authorizations. Actual NASA Earthdata authorization may be necessary, and no user tokens or accounts handled.

## Research consequence
The P76-specific loss-of-future-falsifier claim cannot be supported by two GitHub workflow successes that returned zero science data. Duerr 2009 independent layout-map HDF4 recovery, ordinary preservation/ETL, instrument calibration, and Forand path-option theory remain strong rivals. No fabricated original bytes or study-level empirical proof; no new human recruitment, no paid inference, no P77. The next **single meaningful** observation is verified SHA raw public Earth science granule with a documented science variable and original physical-data interpretation. Do not spend unbounded work on archival HTTP wrappers. If MODIS original requires consent/account, prefer an actual publicly downloadable alternative rather than bypassing access controls.

**P76-P18 court:** `ORIGINAL_PDF_SOURCE_LINKS_RECOVERED_34 / ORIGINAL_BYTES_NOT_ACQUIRED / SCIENCE_QUERY_NOT_RUN / NO_IRREVERSIBLE_LOSS_CLAIM / PAPER_HOLD`.
