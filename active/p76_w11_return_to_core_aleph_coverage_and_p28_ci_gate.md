# EPISTEME P76 W11 — Back to Core: ALEPH Confidence-Interval Identification and P28 CI Gate
2026-10-21 KST. Reader-study design preserved as valuable methodology, but HUMAN READER STUDY DEFERRED. This work does not prove new causal law. P77 WATCH/HOLD.

## Why the founding question still governs
Do not equate a prose-preference crossover, code PASS, byte-equivalence, and an independently warranted test of a scientific rival. EPISTEME's central claim is an adoption-history-driven change in the *feasibility of valid discriminatory science*. ALEPH is an adversarial evidence-warrant case, not yet an adoption-effect case. Papers 1–3 should keep this distinction.

## ALEPH code facts (direct source inspection)
External jfc-mit/analysis_aleph_z_lineshape paths phase4_inference/4c_observed/src/systematics_full.py and covariance_full.py and outputs/results/covariance_full.json. The source generates archive-curvature scale by multiplying baseline Gamma_Z statistical error by 1000 (to MeV). Post-fit Gamma_Z total uses that amount as an additive independent-in-quadrature term to refitted covariance standard error; replaces the energy-tilt term for this parameter. From persisted JSON: baseline Gamma_Z statistical 8.2693199 MeV; in-fit Gamma_Z error 9.1885820 MeV; archive-curvature 8.2693199 MeV; final 12.3617026 MeV. Hence the use of the *same baseline estimate* to set a second term is proven; misuse, independence or coverage is not proven. The Gamma_Z result has 6 scan points, 5 fitted parameters and 1 residual degree of freedom.

## Idealized negative control: no independently real curvature systematic
Let an unbiased estimator T of gamma have Gaussian sampling error sigma, known sigma, and no extra independent nuisance. Normal nominal central 68.27% interval T±sigma has 68.27% coverage. Replacing that by T±sqrt(2)sigma by quadrature adding another sigma sourced from the same sampling error yields about 84.27% true coverage under this *hypothetical model*. This shows increased conservatism, not undercoverage, but demonstrates that the enlarged interval cannot be interpreted as an empirically calibrated 68% confidence interval without specifying more physical uncertainty. If the real source contains a separate bias/nuisance that is externally corroborated, an enlargement may be defensible; exact actual coverage remains unknown. Here the actual covariance refit standard error is larger than baseline and a proper simulation needs that structure (not simply sqrt2).

## Prospective independent simulation
Generate known truth with 6 scan points and nuisance year normalizations, model instrumental offsets and physical beam errors separately; use held-out calibration/noise to size uncertainty. Compare CI rules: (A) in-fit error, (B) in-fit plus same-profile magnitude, (C) independently estimated systematic variance, (D) a robust/profiled nuisance alternative. Refit every replicate, assess 68/95% coverage, calibration and interval length for shifts/no shifts, vary central-peak loss. The generator cannot use target published Gamma_Z to set corrections; log source versions, numerical convergence, selection and cases where ndf=0. Synthetic coverage only validates those generator assumptions, not ALEPH original covariance.

## P28 verified static code contract and trigger hole
Read actual src/p76_p27_source_pair_alias_query_intervention.py, src/p76_p28_three_representation_court.py and .github/workflows/p76_p28_three_representation.yml. P27 DOES emit exact fields expected by P28 for both source hash, 20 paths, semantic units/datetimes, elementwise numeric values, alias fracture, and path-wise checks; guessed schema mismatch that once looked possible is not an immediate problem.
Workflow executes P27 then P28 and uploads both receipts; it has read-only contents permission, no bot commit, on main artifact-only intent. BUT its push path filters include only P28 code and workflow itself, not P27 script. A P27-only edit will not automatically rerun the triple verification. Needs a minimal workflow path-filter patch with P27 source added. Another issue: no actual workflow execution log/receipt retrieved in this turn; source compatibility ≠ CI success. Also P28 vendor installer execution is an external-binary integrity risk whose fixed SHA and download origin should be checked, and no physical acquisition identity should be inferred from aliasing.

## Direction / workload
1. P28 CI authenticity & original source semantics.
2. ALEPH interval coverage experiment plus source-level covariance audit.
3. Historical adoption chronology and JADE restoration negative control, then assess Paper 1–3.
4. Reader study remains a high-quality optional design; do not recruit or expand further without relevant science-judgment hypothesis.
No new P77 or paper submission promotion.
