# Paper 1 — The Afterlives of Scientific Evidence: Restored Witnesses, Reconstructed Numbers, and the Limits of Precision Reanalysis

**Writing Loop W6 · v0.3 · 2026-10-20 · working draft, NOT publication ready.**  
**Status:** documented reconstruction audit; not an independent ALEPH rerun by EPISTEME; paper HOLD.

## Abstract

Archival survival does not yield an all-or-nothing answer to scientific reproducibility. We distinguish at least three tasks: reconstructing a published number, executing a modern approximation to the historical analysis, and independently defending the original measurement with an appropriate uncertainty model. The distinction becomes unusually testable when historical statements of restricted reuse can be compared with later analysis attempts. JADE provides a positive example of recovering paper-only luminosity records and validating their transcription with a surviving checksum procedure. ALEPH's 2003 policy named precision Z-lineshape measurements as analyses difficult or impossible to repeat using its retained archive. A publicly available 2026 reconstruction project now reports an ISR-convolved hadronic-lineshape fit based on an ALEPH hadronic event-shape skim, published luminosities and supplementary electroweak inputs. Its disclosed headline fit is M_Z = 91.1638 ± 0.040 GeV, Γ_Z = 2.4508 ± 0.012 GeV and σ⁰_had = 42.47 ± 0.69 nb. The authors explicitly report a Γ_Z discrepancy of about −3.6 standard deviations against their PDG comparison and note fragile scan-curvature identification and sample incompleteness. These claims come from that project's recorded logs, not an independent reproduction by us. DELPHI's preservation policy offers a complementary example: original data, derived data, simulation, software and conditions were retained while collaboration expertise required for high-precision analyses was diminishing. Together, the cases support **analysis-relative descriptions** of recovery and warranted reuse, not an EPISTEME-original general law or evidence of irreversible adoption-induced epistemic loss.

## 1. Recovery is not a binary

Scientific archives preserve observations together with tools and procedures of varying completeness. A checksum for raw bytes may confirm custody while revealing little about whether a former calibration correction is still defensible. A modern fit may converge without independently recovering the original systematics budget. Conversely, a failed digital search might be rescued by a paper record, as in JADE.

We adopt three deliberately separable questions for a frozen analysis q: (i) can the historical published result be numerically approximated? (ii) can a computation on surviving event-level or derived data be executed? (iii) can the underlying measurement and uncertainties be **independently scientifically warranted**, without silently importing the desired answer? The third is strongest. Agreement on the first is not sufficient for the third.

## 2. JADE: an independently surviving witness

Bethke and Wagner document the rescue of missing per-run integrated luminosity entries via a paper printout and an old consistency-checking routine that identified five transcription errors. This is a successful witness restoration and a counterexample to the claim that a digital omission necessarily destroys future evidence. It is also a case of source-level reconstructibility whose mechanism was already described by its original investigators, not newly observed by EPISTEME. Whether any given later α_s event-shape result required those exact luminosity values remains unverified; a genuine causal analysis would instead track a luminosity-dependent absolute cross section and its original pipeline.

## 3. ALEPH: the 2003 exclusion statement meets a 2026 analysis

The ALEPH Collaboration's 2003 policy identifies Z-lineshape and W-mass results among analyses that cannot simply be repeated, particularly when detailed systematic effects matter. The statement is dated historical institutional testimony, not a proof that all future attempts must fail.

A useful counterpressure is the public **jfc-mit/analysis_aleph_z_lineshape** project (2026). We inspected its original repository's `experiment_log.md`, `COMMITMENTS.md`, `retrieval_log.md`, and `phase4_inference/4b_partial/outputs/SIGMA0_PAPER_RECOVERY.md`. The project declares an initial sample of 3,050,610 hadronic-selection events across merged 1992–1995 files, with 1994-only detector-simulation MC. The event-shape skim contains no useful independent leptonic channels, so its later R_l, N_ν and α_s values are explicitly **externally conditioned derivations**, not separate four-channel measurements. Its record documents important corrective work: replacing an erroneously duplicated polar acceptance factor, correcting mapped per-energy luminosities, separating 1993 scan and prescan events, excluding or downweighting inadequately represented scan periods and using per-year normalization nuisance parameters.

The log reports the final fit M_Z = 91.1638 ± 0.040 GeV; Γ_Z = 2.4508 ± 0.012 GeV; σ⁰_had = 42.47 ± 0.69 nb; N_ν = 2.864 ± 0.171. The *project's* reference comparison is −3.6σ for Γ_Z versus PDG and +1.4σ for σ⁰_had. Its own review acknowledges that dropping the 1993 peak scan anchor changes the fitted Γ_Z by about −430 MeV and leaves an ndf=0 degeneracy, while more modest leave-one-out changes apply only to other points. The final uncertainty treatment includes partially data-driven systematic assignments; the public record flags limited corroboration of an absolute-scale normalization anchored to 1994. These are not mere cosmetic limitations.

The project also exposes an instructive failure-and-repair chain: an early σ⁰ estimate around 54.9 nb reflected an extra acceptance correction; it documented a non-circular paper-driven repair and settled near 42.47 nb. This provides evidence that a surviving original analysis description can be operationally significant. It does **not** authenticate every corrected result, nor negate the original collaboration's concern that full precision systematics may be unavailable.

Therefore the observed verdict is **PUBLIC_RECONSTRUCTION_WITH_REPORTED_LIMITS**, not VERIFIED_FULL_ALEPH_PRECISION_REPLAY. We did not acquire its input ntuples, independently execute its code, reproduce its JSON fits, or certify its covariance model in this W4 pass. Public code and self-reported reviewer gates are audit material, not independent CI or experimental replication evidence.

## 4. DELPHI: data and software can coexist with missing warrant

The 2024 DELPHI release documents a substantial retained body of raw data, reconstructed data and simulations, a conditions database and modernized software. Its warning about fading detailed detector/run knowledge concerns reproducible high-precision inference, not the mere ability to open an event file. The proper comparison requires one supported lower-complexity positive-control analysis and one predeclared precision observable with missing or difficult nuisance inputs. We have not yet executed that comparison.

## 5. A falsifiable evidence-status protocol

For each predeclared scientific q, label its source custody, accessible measurement data, software execution, independent calibration, systematic-covariance authentication and interpretation authority separately. At minimum, possible outcomes include SOURCE_AVAILABLE, COMPUTATION_EXECUTED_BY_OTHER_TEAM, NUMERIC_REFERENCE_APPROACHED, UNCERTAINTY_MODEL_PARTIALLY_RECONSTRUCTED, and WARRANTED_ORIGINAL_PRECISION_REPLAY. These should not be collapsed into a single 'preserved' flag.

The protocol is a transparent application of well-known DPHEP, provenance and reproducibility ideas. Its distinctive value would require an independent, question-specific audit yielding a genuine previously unresolved discrimination, not these category labels alone.

## 6. What this paper cannot conclude

Neither 2003 ALEPH policy nor 2026 independent-reconstruction logs identify an infrastructure adoption decision that caused a superior rival to become untestable. Apparent Γ_Z discrepancies can reflect sample incompleteness, limited scan coverage or theory/fit choices rather than historically induced loss of knowledge. The JADE case, moreover, supplies a clear recovery counterexample. We do not convert any of these into evidence for permanent loss.

The immediate next stage is to reproduce at least one of the ALEPH project's numerical artifacts from pinned inputs, independently inspect covariance and source-to-result provenance, and compare each claim to the original ALEPH scientific error budget.

## Sources

- ALEPH Collaboration, 2003 archival statement: https://dphep.web.cern.ch/sites/default/files/archive_data.pdf
- ALEPH original Z resonance parameters, Eur. Phys. J. C 14 (2000), CERN-EP-99-104: https://cds.cern.ch/record/396345
- jfc-mit/analysis_aleph_z_lineshape, dated 2026-06 public project: https://github.com/jfc-mit/analysis_aleph_z_lineshape
- Experiment log: https://github.com/jfc-mit/analysis_aleph_z_lineshape/blob/master/experiment_log.md
- Binding commitments and explicit limitations: https://github.com/jfc-mit/analysis_aleph_z_lineshape/blob/master/COMMITMENTS.md
- Paper-driven σ⁰ correction report: https://github.com/jfc-mit/analysis_aleph_z_lineshape/blob/master/phase4_inference/4b_partial/outputs/SIGMA0_PAPER_RECOVERY.md
- JADE revival: https://doi.org/10.1140/epjh/s13129-022-00047-8
- DELPHI: https://opendata.cern.ch/record/417
- DPHEP synthesis: https://doi.org/10.1140/epjc/s10052-023-11885-1

**Current research gate:** WORKING_DRAFT_W4 / INDEPENDENT_EXECUTION_HOLD / CROSS-CASE_CAUSALITY_HOLD / PAPER_HOLD.

## W6 — Discourse-sensitive science-prose audit

The reconstruction claim must be intelligible under two distinct reader questions: **what did the other team numerically compute?** and **what source independently authorizes the precision inference?** We therefore avoid weakening 'the original ALEPH calibration and uncertainty chain' into an underspecified 'that information' when the reader must distinguish archival records, reconstructed fits and calibration witnesses. The shorter reference may be appropriate after a uniquely established antecedent, but should not be used to imply that the external project's approximation is full scientific replication. No empirical reader advantage has yet been demonstrated; the candidate edits are held at semantic prescreen only. The underlying limits of the 2026 project, especially the reported Γ_Z discrepancy and fragility of the 1993 scan anchor, remain unchanged.

**Writing diff / retained claim:** Keep explicit source labels in the high-stakes inference paragraph; allow second-mention shortening only after unambiguous provenance. Do not alter science or numeric qualifications. See `../active/p76_writing_loop_w6_semantic_pair_pass_crossover_court.md`.
