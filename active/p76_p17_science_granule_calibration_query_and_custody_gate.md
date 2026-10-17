# EPISTEME P76-P17 — Real Observation Source Gate and Calibration-Semantics Prior Art

2026-10-17 KST. P76 continues, no P77, manuscript HOLD.

## Direct source evidence
- [Open HDF-EOS4/HDF4 NASA science mission sample collection](https://hdfeos.org/zoo/Data_Collection/index.php), directly retrieved by [GitHub Action 39038449693 SUCCESS](https://github.com/WhoSia/EPISTEME/actions/runs/39038449693). HTTP content 10,769 bytes, HTML SHA256 `9113161e08fa99b9014423962948ed798b4feb2ba7a01f1465d14ece27e33157`, 52 HTML anchors with named real NASA mission summary pages (GES DISC AIRS/TRMM, LAADS MOD/MYD, NSIDC AMSR, LaRC MISR, PODAAC, OBPG). No original HDF observation bytes downloaded and no native observation query executed; catalog retrieval is NOT data custody.
- [HDF EOS LAADS MOD actual observation examples](https://hdfeos.org/zoo/Data_Collection/LAADS_MOD_Summary.php) explicitly describes real Terra MODIS Level1/Level2 geolocation dimension-maps, scale+offset choices, fill value semantics, and non-CF-compliant metadata. One example MOD021KM source archive is named `MOD021KM.A2000055.0000.005.2010041143816.hdf`, 42MB, real Terra MODIS Level1 radiance; original mission source requires verification before using mirror.
- [NSIDC-0397 official NASA sample, DOI 10.5067/P1B2VYBCJ95O](https://nsidc.org/data/nsidc-0397/versions/1), the most directly relevant original scientific source and Duerr et al. 2009 independent layout-map reader; prior P16 test original server HTTP200 but zero file anchors, raw data not acquired.
- [NSIDC official FTP/wget access guide](https://nsidc.org/data/user-resources/help-center/how-access-nsidc-data-using-ftp-client-command-line-wget-or-python) states some NSIDC archives can be retrieved anonymously through FTP, but it does NOT establish this particular NSIDC-0397 folder is FTP-accessible; keep data-access uncertainty visible.
- [NASA MODIS MOD021KM metadata](https://hdfeos.org/zoo/Data_Collection/LAADS_MOD_Summary.php) provides a strongly discriminating actual scientific question: does mapping preserve calibrated radiance for a preregistered pixel/band after distinguishing radiance_scales/offsets from reflectance_scales/offsets, the fill mask, and swath geolocation dimension map? Raw value equality is insufficient; a converter may preserve source SDS values but change or omit the transformations required for physically meaningful observations.

## The strongest research revision
Do not say these are new P76 concepts: science calibration and coordinate handling are established remote-sensing data semantics. Their role here is to **kill** misleading 214/214 numeric-only data-preservation verdicts as evidence of full scientific equivalence.

Exact next empirical object on byte-acquired science granule:
1. freeze original granule SHA, temporal/mission sensor ID, source variables and science question;
2. old HDF4 + original applied scale/offset and fill mask + geolocation as comparator;
3. versioned official HDF4→HDF5 route and independent recovered original-reader route;
4. compare physical calibrated radiance and geolocation, not just integer SDS values; mismatch is not inherently caused by representation adoption unless version/history and existing correction choices controlled;
5. admit full Forand option retention, Duerr layout-reader and ETL/PROV scientific metadata alternatives.

P76-P17 outcome: `SCIENTIFIC_CATALOG_ACCESS_PASS / FIRST_HDF4_SCIENCE_GRANULE_BYTES_HOLD / CALIBRATED_RADIANCE_QUERY_PREDECLARED / NO_QUERY_EXECUTION / STRONG_PRIOR_ART_SURVIVES / PAPER_HOLD`. No human recruitment or paid inference.
