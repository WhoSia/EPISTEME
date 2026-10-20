# EPISTEME-P76-W7 — ALEPH Artifact Readback, Systematics Structure, and P28 Parallel Track

2026-10-20 KST. Connected GitHub source artifact read; no original ntuple execution, no external CI attestation.

## ALEPH new stronger evidence
Read jfc-mit/analysis_aleph_z_lineshape/phase4_inference/4c_observed/outputs/results/systematics_full.json directly (the previous W4 mainly relied on project narrative log). Artifact has a true baseline_fit object, point list, named systematic components, correlation matrix and sensitivity shifts. Reconstructed SOURCE-REPORTED central fit:
M_Z=91.1637945314673 GeV, Gamma_Z=2.450822319552185 GeV, sigma0_had=42.471788551649034 nb.
Base fit statistical errors 0.003274 GeV, 0.008269 GeV, 0.064822 nb; **these are not the full W4 reported total uncertainties** (~0.040 GeV, 0.012 GeV, 0.69 nb) which include other sources. Strong risk if readers conflate base fit errors with total uncertainty.
6 selected scan points (1993 three, 1994 one, 1995 two), 5 fit parameters, ndf=1 and χ²≈0.297355; per-year free scale parameters norm_1993=0.79120949 and norm_1995=0.75350823 (1994 baseline). This weak residual degree of freedom limits how informative good fit χ² can be.
Correlation Gamma_Z with 1995 normalization = −0.7558419411; with 1993 normalization = −0.5589189043. Model uncertainty cannot be judged by central value proximity alone.
The largest scanned systematic is energy-dependent per-year normalization tilt; source says ±1.43%/GeV central slope (±0.56%/GeV) and explicit coherent versus antisymmetric variation. For Gamma_Z antisymmetric central shift −12.756 MeV, for M_Z coherent shift −40.053 MeV, plus several smaller named calibration, background, ISR, luminosity, beam-energy uncertainty components. This is an internal sensitivity estimate, NOT external validation of its covariance construction. Covariance sources partly reconstructed/scanned, with incomplete original ALEPH detector/control inputs. Artifact JSON exists; outputs have not been reproduced by running raw data locally.

Cite precise artifact: https://github.com/jfc-mit/analysis_aleph_z_lineshape/blob/master/phase4_inference/4c_observed/outputs/results/systematics_full.json . Treat repository's selfcheck booleans as self-reported only.

## P28 distinct stream
EPISTEME P27 source-pair original HDF4/HDF5 result preserved; P28 A/B/C code and CI workflow configured with fresh native HDF4 receipt validation (GitHub commit c607165c1338f56df09a47e6bd61a7e3334bca36). **No verified P28 Actions run ID, log, and resulting JSON receipt obtained in this W7 turn.** No three-way PASS claimed. Need authenticated workflow execution evidence and physical original acquisition semantics before general scientific normalization conclusions.

## Direction and promotion
The Writing Loop reader test probes science-communication accuracy (A–C), not institutional adoption causality (D). ALEPH artifact proves greater traceability than W4 narrative-only read, but the ndf=1 / nuisance correlations suggest serious identification sensitivity. Still no evidence of a unique adoption-driven defeat-route change; no P77 promotion. Preserve original P76 goal, independent strong rivals, DPHEP/LEP precedent, and paper submission HOLD.
