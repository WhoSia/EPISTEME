# EPISTEME-P74 — Temporal Authority Dynamics & Causal Identifiability of Epistemic Interventions: Provenance-Transition Semantics, Audit-Induced Evidence Change, Independent Warrant Adjudication & Cross-Ecology Falsification

**Official stage:** P74, opened at user's explicit authorization, 2026-10-10 KST. **First scientific section:** P74-P0 (not the closing of P74). **Evidence class:** deterministic synthetic construction, preprint/scientific discovery not certified. **No paid providers, real institutions, reviewer recruitment, or public audit notices.**

## Explanandum lock / provenance
Predecessor [P73](p73_research_program.md) distinguishes state-dependent safe observations and source-time/authority conflicts; its P5 audit-notice design had two waves and **zero real audits**. P69 remains PAPER_CONSTRUCT_HOLD (original SciFact heldout: 8 claims/8 source documents, human 0/16); P70 full-original-vs-two-QA panel is human 0/16, P71 original review 0/32. These remain separate and do not become P74 results.

**Founding question:** when observation or a publicly announced audit can alter the source it purports to certify, what evidence can distinguish ordinary source drift, audit-notice effects, actual evidence-acquisition effects, changes in legal/temporal authority, reviewer interpretation and downstream switching decisions?

**P74 task boundary:** causal estimand identification is neither an automatic warrant certification nor a factual claim about real institutions.

## P74-P0 — Identical records, opposite effects

Units are eight **wholly synthetic source units**. Source role, authority effective epoch, observer time, deterministic synthetic hash, two pre-notice outcomes and observed post-notice source-change flag are fully recorded. Four units are in notice arm A=0 with post change flags (1,0,0,0); four are in A=1 with flags (1,1,1,0). Both arms have two identical zero-valued pre-periods. A is **not** randomized. The observed descriptive difference in differences is 3/4 - 1/4 = 1/2.

Write Y_i(0),Y_i(1) for the potential binary source-change outcomes *under notice treatment* A_i=0,1 at the fixed post-period. Consistency constrains only Y_i(A_i), leaving one binary missing potential outcome for every unit. Define two complete causal models:

- **M+**: in the nonexposed group all hidden Y_i(1)=1; in the exposed group all hidden Y_i(0)=0. The finite-population ACE equals +3/4.
- **M-**: in the nonexposed group all hidden Y_i(1)=0; in the exposed group all hidden Y_i(0)=1. The finite-population ACE equals -1/4.

Their complete **observable histories are byte-identical** (including artificial role, epoch, and synthetic hash metadata) while ACE signs differ. The model changes only the counterfactual entries that are never observed. Exhaustively enumerating 2^8 binary missing-outcome completions yields nine possible ACE values, with the *sharp finite-population identification interval* **[-1/4,3/4]**, under consistency, binary outcomes, and no interference. Zero belongs to the set. Bounds here are a standard potential-outcomes/partial-identification result, not a novel theorem.

Exact executable: [src/p74_p0_observational_equivalence.py](../src/p74_p0_observational_equivalence.py). Stdlib only; no external source downloads or provider calls.

### Distinguish these propositions
1. Two flat observed pre-periods do **not** establish parallel *untreated post-period counterfactual trends*. Multi-period diagnostics may be useful but do not prove them.
2. A source snapshot's SHA certifies content identity *within the synthetic record*, not independently witnessed publication time, credential authority, or noninterference.
3. The **treatment** in this P0 countermodel is the public **audit notice**. **Actual source acquisition/interrogation is a separate action** and is not modeled as if completed.
4. The **outcome** is a binary recorded source-change flag. It is not truth, warrant validity, source integrity, human judgment or downstream representation switching.
5. Even if a causal effect were identified, a separate original-source/authority and human-warrant court would still be required.

### Mathematical method and claim ceiling
The observational equivalence is established constructively by agreement of Y_i(A_i) and all fixed recorded metadata, together with disagreement on counterfactual Y_i(1-A_i). This is a standard missing-potential-outcome argument; it does not establish a population-level causal-effect estimate, test novel DAG theory, or claim novel epistemic ontology. The exact interval is conditional on the *specified finite eight-unit synthetic population* and unconstrained binary missing outcomes. Interference or multiple versions of notice expands, rather than resolves, the proof obligations.

### Related primary literature (Drive-first review)
- **Manski (2005), Partial identification with missing data: concepts and findings.** Original PDF retrieved and read from canonical Google Drive: https://drive.google.com/file/d/1dVBEhKzemt_qokxS-PTwntbq3RpLONdO/view . [Original claim] Identification regions rather than unsupported point-identification; [Our reconstruction] missing potential outcomes are analogous missing-data cells.
- **Hudgens & Halloran (2008), Toward Causal Inference With Interference.** Original PDF retrieved and read from canonical Google Drive: https://drive.google.com/file/d/135gYAyTkTYbQ4eu7vDwcC91dTBRWdnnZ/view . [Original claim] Group interference changes estimand definition; [Hypothesis to test] audit announcements may spill over between source clusters.
- **Brown, Hod & Kalemaj (2022), Performative Prediction in a Stateful World.** Original PDF retrieved and read from Drive https://drive.google.com/file/d/1690w4PxcI0lHBFgNmTulv_CkFS36r79p/view . [Original claim] actions influence future state distributions conditional on prior state; [Our reconstruction] motivates dynamic audit-induced source transition questions, not a direct causal identification theorem.
- **Rambachan & Roth (2023), A More Credible Approach to Parallel Trends.** Drive 미확보(색인 검색 기준); journal abstract and MIT publication verified: https://economics.mit.edu/research/publications/more-credible-approach-parallel-trends ; actual PDF direct download in publisher indexes, **full text not yet read from canonical Drive**. [Original abstract] sensitivity bounds for violations of parallel trends, a stronger rival than naive DID. Do not claim source custody/full-text review for this paper.

## P74 research program — prospective boundaries

### P74-P1 candidate: authority-transition potential outcomes
Define typed, time-indexed states S_it=(bytes/semantic payload, independently attested authority interval, evidence role, referent, admissible inference). Define source publication/revocation and institutional notice/acquisition as *different intervention channels* N_it, Q_it. Permit observation process to have access effects, measurement coarsening and cluster spillovers. Formalized contrasts are permitted only if treatment versions and intervention timing are well-defined.

### P74-P2 candidate: independent warrant and switching bridge
Separate source correctness, provenance authority, answer sufficiency, independent human warrant, and downstream decision in the causal graph. A P69/P70 scorer form is NOT an actual human reviewer; actual P69 0/16, P70 0/16, P71 0/32 remain. A prospective study must have consent, reviewer independence validated by an external custodian, preregistered contrasts, no private licensed source disclosure in public artifacts and an auditable claim ceiling.

### P74 falsification priorities
- A rival generalized observational model explains the same effect range without epistemic-role semantics -> do not assert P74 ontology.
- Tighter source-time/authority trace reduces the identified set? **Test** whether independent certificate adds information; same metadata text alone cannot.
- Negative controls and multiple pre-waves do not prove parallel counterfactual trends; test admissible sensitivity models.
- Cluster-level exposure interference or nonuniform notice effects require treatment-version-specific estimands.
- Human disagreement or missing/unusable original answers can block warrant certification even if the statistical arm estimate were known.
- Methodological detours must return to original founding question: when evidence standards become entrenched, under what conditions can an alternative representation be legitimately adopted and certified?

## Governance and execution
GitHub Actions must remain read-only: `permissions: contents: read`, no Action commits, pushes, tags, merges, branch mutations, or attribution to bots. Human-account repository promotion only. Run/commit SHA and explicit PASS/HOLD readback needed before CI promotion. No historical CI run is evidence for this new P74 code unless exact commit/build covered it.

**P0 local computation:** PASS for the deterministic fixtures and exhaustive completion model. **External/CI status:** separately record once inspected. **Causal effect on real sources:** HOLD. **New theorem/independent scholarly novelty:** HOLD. **Independent human warrant:** HOLD. **Source authority certification:** HOLD.


## P74-P1 — Authority-transition admissibility versus causal counterfactual identification (executed, synthetic)

[Executable exact court](../src/p74_p1_authority_identification_court.py) · [P69–P73 inheritance / rival registry](p74_p69_p73_inheritance_court.md).

**Primary attack:** does adding a source's separately collected timestamp, content hash, proof role, referent, issuing authority interval, revocation and collector/issuer identity reduce the identification region of the **notice-effect on source change**? Answer in this fixture: **NO**. These are records of the *observed factual world*; they are not measured counterfactuals. They affect the independently typed *authority-admissibility at observation* calculation (7/8 valid, 1/8 revoked in the synthetic fixture), but not the causal potential outcome class (256 completions, ACE [-1/4,+3/4]).

**Only an explicitly introduced cross-world structural bridge changes the ACE set:**
- two exposed units hypothetically satisfy untreated potential source-change Y(0)=0: 64 completions, ACE [0,+3/4];
- all four exposed units hypothetically satisfy Y(0)=0: 16 completions, ACE [+1/4,+3/4].
These are **not empirical discoveries**, **not verified external authority**, and **not consequences of source timestamps**. Code refuses a bridge unless the caller expressly marks it `explicitly_assume_crossworld_bridge=True`, and checks duplicate/invalid constraints. The new sign-identification in the strong case is *assumption-driven*.

**Adversarial failure cases** cover no genuine third-party attestation (synthetic-only self-label remains mandatory), timestamp reversals, future-signed certificates, publisher=attestor identity collision, wrong recorded bytes, proof-role/referent mismatch, duplicated witness, and illicit counterfactual promotion. Time-effective authority `[start,end)` is conceptually distinct from content-updated timestamps and actual notice/acquisition treatment versions.

**Novelty/rival boundary:** Identified-set intersections and metadata-vs-counterfactual distinction are standard partial-identification logic (Manski 2005, Drive original read). Group interference (Hudgens & Halloran 2008), stateful feedback (Brown et al. 2022), and parallel-trend sensitivity (Rambachan & Roth 2023, original full paper not canonical Drive read) remain direct competitors. P74 must seek **independently witnessed real evidence transitions** and nontrivial identification improvements, not promote elementary finite arithmetic as a new theorem.

**Carry-over court:** historical actual P69 hosted 192+64, P70 hosted 32, P70 original QA 10 answers/10 questions vs 8 projection, P69 distinct SciFact holdout 8/8, P71 16 variants ×2 anticipated humans, and P72/P73 proof-role/time/observation antagonists are preserved in [inheritance registry](p74_p69_p73_inheritance_court.md). P69 humans 0/16, P70 new humans 0/16, P71 humans 0/32; *evidence inheritance does not imply new independent validation*.

**Operational gate:** P74-P0 and P74-P1 stdlib programs are run by the existing G-001 read-only CI workflow. Capture the *exact latest HEAD* and run ID from GitHub after this document write. No paid model calls, actual audit notices, humans or institution interventions. All real causal, source-authority and warrant certification claims remain HOLD.
