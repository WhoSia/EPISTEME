# EPISTEME-P76-W9 — ALEPH archive_curvature code-level variance audit

2026-10-21 KST. Direct read of source code AND persisted covariance output, not independent raw-event rerun. P76 OPEN, P77 HOLD, PAPER HOLD.

## Exact files read at public repository
External repository jfc-mit/analysis_aleph_z_lineshape (GitHub search showed c9e84a6a57a73e14d4252c0cb73bbdd7d08c662a), paths:
- phase4_inference/4c_observed/src/systematics_full.py
- phase4_inference/4c_observed/src/covariance_full.py
- phase4_inference/4c_observed/outputs/results/systematics_full.json
- phase4_inference/4c_observed/outputs/results/covariance_full.json

## Trace
1. systematics_full.py explicitly calculates archive_curvature_gammaz_MeV = float(res_base["Gamma_Z_err_GeV"] * 1000.0). It labels this sizing as the one-sigma profile width, which for this fit equals the baseline Gamma_Z statistical error. It creates a separate systematics["archive_curvature"] record (8.269319908817963 MeV).
2. covariance_full.py builds per-point covariance matrices with source terms and fits to obtain res_total. It then makes a per-quantity post-fit lineshape_lim. M_Z receives the scanned sqrt(s) tilt; Gamma_Z receives archive_curvature IN PLACE OF tilt; sigma0 receives tilt, plus its distinct scale handle.
3. The final total is literally total[q] = float(np.hypot(np.hypot(infit, lineshape_lim[q]), scale)), where infit is the standard error from the covariance-based refit. Consequently Gamma_Z combines 9.18858198921435 MeV in-fit error with 8.269319908817963 MeV archive-curvature (not in-fit) -> 12.361702582042955 MeV final error.
4. The JSON explicitly preserves statistical 8.269319908817963, in-fit systematic covariance 4.006043836273044 (quadrature difference), total 12.361702582042955. This is NOT equal to adding the 12.7562 MeV sqrt(s) tilt as well; that term is superseded for Gamma_Z.
5. Justification gap: selecting the archive-curvature 'independent systematic' magnitude from the same fit profile statistical error may double use source information. But sharing the numerical magnitude does not, by itself, establish wrong frequentist coverage or illegal variance addition; need state a stochastic model for the alleged extra uncertainty and calibrate the one-sided/two-sided interval under mocks and alternative samples. Its documented 5.55 MeV LOO check EXCLUDES loss of central 1993 peak, which produces a degenerate ndf=0 case.
6. This confirms how the code combines errors but does NOT authenticate independent physical calibration, full systematic covariance, original ALEPH precision replay, or the P76 causal adoption claim.

## Falsifiable next experiment
Specify simulator with known Z width and sample-level incomplete selection, free yearly normalization, independent detector-systematics variation. Compare nominal 68/95 percent empirical coverage for (a) in-fit only, (b) +same-profile 1σ archive term, (c) +independently estimated shift variance, using held-out or externally calibrated perturbations. Match ALEPH source semantics; until then label archive error as 'post-fit conservative prescription', NOT 'independent systematic experimentally validated'. Also compare total error if source correlations are nonzero.

## Writing and promotion gate
Paper 1 and 3 should describe disclosed W9 limitation in manuscript prose, without treating an outside team's analysis as our own empirical result. Strongest prior art: DPHEP preservation and standard uncertainty propagation. P77 not promoted; P28 CI receipt still not confirmed.
