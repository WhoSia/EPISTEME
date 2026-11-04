# EPISTEME-P77 W9 — Solar-Neutrino Discriminability and the Historical Testability Court
**Official program:** EPISTEME-P77 — Research Identity Adjudication: Historical Testability, Philosophical Reconstitution & Terminal Review
**Date:** 2026-11-04 KST
**Status:** source-grounded pilot and strong-prior-art court; **NO NEW SCIENTIFIC DISCOVERY**, P78 / manuscript HOLD.

## Research problem, carefully separated
The solar-neutrino anomaly initially admitted (at least) two broad rival explanations: failure of solar-flux astrophysical predictions and flavor transformation of neutrinos in transit. Historians, experimenters and philosophers have ALREADY described how the two were discriminated. Our research task is whether documenting the *historical availability and selection* of a discriminating experiment teaches something beyond measurement-concept formation (MQR) and inductive triangulation (Evans & Thébault 2020). It may well not.

Do not conflate:
1. **Physical identifiability** — is there a possible measurement mapping separating parameter values / rivals under stated assumptions?
2. **Instrumental realizability** — can a detector, calibration procedure and background control realize that measurement?
3. **Historical accessibility** — could contemporary people obtain the needed heavy water, site, funding, collaboration and know-how?
4. **Epistemic warrant** — did the actual completed tests + uncertainties support the substantive conclusion?
The chain of implications is neither automatic nor reversible. Evidence of delay is not proof of active suppression/lock-in.

## Direct original source sequence and specific observations
- **Chen (1985), PRL 55 1534**, DOI 10.1103/PhysRevLett.55.1534, [full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.55.1534/fulltext). Explicitly proposed heavy water deuterium CC (electron flavor) vs NC (all active flavors) to test both flux model and flavor transition *separately*. This **defeats any original EPISTEME priority claim** about the discriminating design. Chen already noted operational feasibility factors: large underground light-water experiments, Canadian heavy-water reactor resources, sensitivity of NC neutron detection.
- **Collaborative development** SNO official detector history, https://sno.phy.queensu.ca/sno2.html: 1983 underground site proposal, 1984 collaboration and heavy-water plan, source acquisition and mine infrastructure. Hime 1996 historical account, https://digital.library.unt.edu/ark:/67531/metadc675002/m1/4/, reports 1985 feasibility funding, 1988 international review, January 1990 construction funding. Important archive and user-specific potential *historical-access* record, not evidence of policy induced lost rival testing.
- **SNO (2001), PRL 87 071301**, DOI 10.1103/PhysRevLett.87.071301. Compare electron-only CC at SNO with flavor-weighted ES at Super-Kamiokande: ~3.3 sigma evidence for non-electron active component, under error assumptions.
- **SNO (2002), PRL 89 011301**, DOI 10.1103/PhysRevLett.89.011301, Research OS exact original PDF ID 1zDBfrf1Ex3a8yOVwSzGDfov-dOVQpakh; using CC/ES/NC and assumed 8B spectrum, reported phi_e=1.76 and phi_mu_tau=3.41 (both ×10^6 cm^-2 s^-1), non-electron component 5.3 sigma >0, total NC flux 5.09 ×10^6 cm^-2 s^-1. Calibration energy-scale uncertainty 1.2% and background assays documented in source. None of these is an EPISTEME measurement.
- **Heeger (2002), dissertation** Research OS ID 1VrbgUykxR_DUrEQMl7gB6vbmP17Paucv. Original hundreds of pages covering calibration, energy response, background and systematics; first-page/contents and targeted calibration passages reviewed, NOT all dissertation pages or calculations.
- **Nakahata (2022), PTEP**, doi 10.1093/ptep/ptac039, https://academic.oup.com/ptep/article/2022/12/12B103/6543725. History from Homestake, Kamiokande, gallium experiments to Super-K and SNO; this history is pre-existing, not a new case discovery.

## Strong philosophical rival directly involving this kind of case
**Evans and Thébault (2020), On the Limits of Experimental Knowledge**, Philos. Trans. R. Soc. A 378 20190235, DOI 10.1098/rsta.2019.0235, Research OS PDF ID 1iZbkpGtZIZsw5T4y1yBE_JxpceBUG1_p. The article explicitly uses stellar processes and solar neutrino oscillations to discuss source-target induction and **inductive triangulation**. Its central claim is that epistemic strength depends on availability of distinct, independently justified forms of inductive support, not merely target access or ability to manipulate the target. Thus 'multiple experimental methods finally discriminate an inaccessible scientific alternative' is ALREADY strong philosophical prior art. Treat this paper as a FATAL RIVAL to generic EPISTEME philosophical originality.

## Mathematical sanity check — NOT original inference
Let unknown flux vector x=(phi_e,phi_mu_tau) and idealized row-normalized observables be:
- y_CC = phi_e
- y_ES = phi_e + r phi_mu_tau, r ≈ 1/6.5 (illustrative, not exact response-folding)
- y_NC = phi_e + phi_mu_tau
with A_CC=[[1,0]], A_CC+ES=[[1,0],[1,r]], A_CC+NC=[[1,0],[1,1]].
RANK: 1,2,2 respectively, under r>0. In this arbitrary equal-scale toy, 2-norm condition numbers ~13.077 (CC+ES) and 2.618 (CC+NC). Higher condition number reflects noise amplification **ONLY IF** comparable scaling and noise; actual scientific uncertainty requires complete covariance, flux spectral assumptions, backgrounds, cross-section priors, detector acceptance and source dependence. Even CC+ES can be algebraically identifiable (and WAS used in 2001), so falsely claiming rank only increased in 2002 would be wrong.
Reproducible code: [src/p77_solar_neutrino_identifiability_toy.py](../src/p77_solar_neutrino_identifiability_toy.py); independently executed locally on 2026-11-04. NumPy required. Tests cover alternate r.

## Serious falsification of independent EPISTEME contribution
**Rival 1 (physics design):** Chen (1985) formulated exactly the experimental response complementarity and its feasibility constraints.
**Rival 2 (measurement/philosophy):** Evans & Thébault (2020) explain why complementary, independently supported inferences justify the resulting knowledge; MQR can study calibration and instruments.
**Rival 3 (institutional history):** official SNO and subsequent historical reconstructions detail heavy-water availability, mine infrastructure, international collaboration and funding. Merely relabeling this 'historical testability' is not original.
**Candidate residual hypothesis, strictly unpromoted:** can we establish that a specific institutional/procurement choice (rather than physics or funding) *removed* an otherwise feasible rival-testing path, against a matched negative case? For this case, current evidence supports construction and eventual success, **not foreclosure**. A case of successful restoration/expansion actively falsifies any blanket 'standardized infrastructure destroys alternatives' narrative.

## Disposition
**Court result: CASE VALUABLE AS A NEGATIVE CONTROL FOR EPISTEME, NOT A NOVEL EPISTEME DISCOVERY.**
For robust philosophy research we need original primary records demonstrating a nontrivial difference from Chen 1985 / Evans & Thébault 2020 / MQR. An intellectual migration from software benchmarking to HPS is permissible for study, but the P77 terminal gate remains open. Do not auto-open P78.
No paid experiment, new participant, claim of detector access or laboratory measurement.

## Library inventory / acquisition targets
IN DRIVE: SNO 2002 original PDF 1zDBfrf1Ex3a8yOVwSzGDfov-dOVQpakh; Heeger 2002 dissertation 1VrbgUykxR_DUrEQMl7gB6vbmP17Paucv; Evans & Thébault 2020 1iZbkpGtZIZsw5T4y1yBE_JxpceBUG1_p.
NOT IDENTIFIED IN DRIVE BY TITLE SEARCH: Chen 1985 original (https://doi.org/10.1103/PhysRevLett.55.1534), Nakahata 2022 (https://doi.org/10.1093/ptep/ptac039), Hime 1996 historical report (https://digital.library.unt.edu/ark:/67531/metadc675002/). No claim of definitive absence.

## Next case
Find an actually **foreclosed** historical experimental alternative documented in original contemporaneous records. Compare against case of **expanded** possibilities (SNO) and disprove generic accounts of technical maturity, laboratory contingency, political economy, and MQR measurement formation. If no independent residual is recoverable, P77 should recommend transfer/retirement instead of another label.
