# EPISTEME-P73 — Warrant-Separating Observation under Reflexive Evidence Dynamics

**Full formal name:** EPISTEME-P73 — Warrant-Separating Observation under Reflexive Evidence Dynamics: Minimal Discriminating Audits, History-Indexed Proof Transport, Intervention-Safe Identification & Sequential Switching Decisions Court

**Status:** P73 formally OPEN, P0 finite-model study. Notion: https://app.notion.com/p/3f5ef561cf928145862cdfdc1fa556b6

## Original question

When two possible states show identical source citations and timestamps but differ in whether evidence validly warrants migration, which additional source-certified **non-disruptive** tests can determine warrant validity, at minimum worst-case review cost? The test must not change the evidentiary condition it is intended to assess.

Predecessors: EPISTEME P2–P4 already studied endogenous evidence, disappearing experiments and path-dependent observability. P72-P1 proved only standard forward simulation and fibre-identification counterexamples. P69 paper remains HOLD; P70 semantic/behavioral ecology transport remains HOLD; P71 real AVeriTeC human reviewer labels are 0/32. No model or participant study newly authorized.

## P73-P0 — Exact finite model

For finite possible worlds W, binary target warrant Q(w), and deterministic static passively authenticated probes p with finite outcome r_p(w), positive cost c_p:

A finite safe policy exists **iff every pair with opposite Q labels is separated by at least one certified safe probe**. Necessity: an opposite-label pair responding identically to all safe probes follows one indistinguishable decision path. Sufficiency: measure all safe probes once and classify by the resulting signatures. This is a classical observational equivalence result, **not a new theorem**.

For compatible worlds S, worst-case sequential probe cost satisfies Bellman's rule V(S)=0 if Q constant; otherwise V(S)=min_p(c_p+max_o V({w in S: r_p(w)=o})), excluding non-splitting probes. Exact dynamic programming terminates since subsets shrink and costs are positive. This is standard adaptive decision-tree optimization.

[Executable P73 P0](../src/p73_safe_probe_court.py): Four synthetic worlds with opposite warranted decisions, common visible citation, and three source-certified *in-model* static probes. First low-cost route probe A costs 1; follow-up left/right discriminators B,C each cost 2. Adaptive minimax worst cost 3; minimum fixed nonadaptive subset costs 4. Deleting C leaves an opposite-label pair indistinguishable and returns NO_SAFE_POLICY.

A highly informative low-cost probe that mutates the warrant-relevant evidence is excluded; another probe lacking independent source attestation is excluded. These audits are **synthetic model checks**, not real-world noninterference evidence. P73 never grants real passive authority from an assumed boolean test fixture.

## Prior research — actual Google Drive custody

- **Türker, Ünlüyurt & Yenigün (2016)**, *Effective Algorithms for Constructing Minimum Cost Adaptive Distinguishing Sequences*: **Drive 보유·원문 정독**, [original PDF](https://drive.google.com/file/d/10N6hZKeeKT6zMp0udLza4Si1yIaYEKUm/view). Adaptive distinguishing sequences and their optimization/hardness are prior art.
- **Hauser & Bühlmann (2012)**, *Characterization and Greedy Learning of Interventional Markov Equivalence Classes*: **Drive 보유·원문 정독**, [original PDF](https://drive.google.com/file/d/1eMqlfzxAZpNGbMFOCS96ZU_oosXUNxkN/view). Experimental interventions refining equivalence classes are prior art.
- **Brown, Hod & Kalemaj (2022)**, *Performative Prediction in a Stateful World*: **Drive 보유·원문 분석**, [original PDF](https://drive.google.com/file/d/1690w4PxcI0lHBFgNmTulv_CkFS36r79p/view). State-dependent performative response and history dependence are not novel.
- **Rivest & Schapire (1993)**, *Inference of Finite Automata Using Homing Sequences*: **Drive 파일 발견·본문 검증 불충분**, [PDF](https://drive.google.com/file/d/1JNqBDFbRgaUEHBwDQJVhgWM1CPkFn1pp/view), extractor returned no usable text.
- **Hyafil & Rivest (1976)**, *Constructing Optimal Binary Decision Trees is NP-Complete*: **Drive 미확보(색인 검색 기준)**; publisher DOI https://doi.org/10.1016/0020-0190(76)90095-8 ; original author publication record https://people.csail.mit.edu/rivest/pubs.html .

None of those source-status statements implies the full relevant literature has been exhaustively searched.

## P73-P1 research boundary

In a reflexive state-transition system, each probe may change future evidence availability, time, source-provenance and the target proof. The static theorem does NOT apply unless passivity is actually certified. P1 must seek a **history-indexed safety witness** preserving the required warrant and future admissible observations, or explicitly return NO_CERTIFIED_SAFE_POLICY. Conditional equivalence of future observation behavior may support a weaker notion than full-state identity, but must compete with established machine-state equivalence and active diagnostic theory. Do not claim novel mathematics before establishing a nontrivial difference and a real independent dataset.

**G-001:** Actions read-only, no bot commits/merge/push. Current limits: HUMAN_REVIEWS=0/32; PAID_MODEL_CALLS=0; PAPER_NOVELTY_HOLD.

## P73-P1/P2 — Original-Literature Replacement and Belief-State Reachability

**Drive intake closure (verified by metadata readback):** The user supplied four new primary papers in `00_INTAKE — Literature Radar`. Their original files have been fully checked at the level of main text, renamed and moved into `10_PAPERS — Canonical Literature Commons` **without changing IDs**. Read the [source-by-source comparison and DOI/version distinctions](p73_p1_new_literature_and_dynamic_observation.md).

- [Hyafil & Rivest (1976) original](https://drive.google.com/file/d/1i4AUMzbYhYOLvA_H5Mw7wBVBATP4YsGR/view): direct expected-probe-cost NP-complete result; scanned transcription imperfect; **Drive secured, original examined**.
- [Verwer & Zhang (2019) AAAI](https://drive.google.com/file/d/1kQMSkaCz1fhLn4fAHn5OI5EYygcqSj8y/view): binary linear program for *training an optimal classification tree*; **Drive secured, original examined**.
- [Avellaneda (2020) AAAI](https://drive.google.com/file/d/11VHs_cumtrE08i1otc3llbVV9s0wGLNA/view): incremental SAT for min-depth classification-tree inference; **Drive secured, original examined**.
- [Firat et al. (2020) journal accepted manuscript](https://drive.google.com/file/d/1U-Yly-n0h-nccac3payWJ-0nyVuZUJ_x/view): column-generation heuristic for training classification trees; **Drive secured, original accepted manuscript examined**, published title *Column generation based heuristic for learning classification trees*. Different from the accepted manuscript title.
- Original related ADS competitor [Türker et al. (2016)](https://drive.google.com/file/d/10N6hZKeeKT6zMp0udLza4Si1yIaYEKUm/view) remains the nearest **dynamic testing** rival, not three supervised-learning classifiers. All four are different original files but **whole-library cryptographic duplicate completeness was not asserted**.

**Mathematical P1:** [`src/p73_history_safe_court.py`](../src/p73_history_safe_court.py) computes a finite worst-case cost-optimal history-indexed observation policy. A private measurement-setup action may change reader readiness while preserving the target warrant and evidence token. The first measurement is nondiscriminating; `PREPARE` then `READ` yields the warrant with synthetic worst cost 2. A full-world-identity standard is overly restrictive in this toy setting. Opposing-warrant pairs may be **locally** distinguishable with world-specific probes yet the original larger belief may admit no safe initial action. Thus P73-P0's static fixed-admissibility pairwise signature condition does not survive generalization to belief-dependent probe availability.

**Mathematical P2:** [`src/p73_winning_belief_court.py`](../src/p73_winning_belief_court.py) enumerates model-permitted reachable beliefs and computes the standard controllable-predecessor fixed point. Homogeneous-warrant beliefs are terminal winning; a belief enters the winning set if one model-safe action leads only to already winning successors. The smallest iteration rank gives a finite required horizon (2 on the preparation example); the all-pairs-locally-separable but no-global-action construction remains outside the winning set. This is existing partial-observation reachability mathematics, not a claimed novel theorem.

**Observed CI:** [GitHub read-only P73 P0–P2 Actions #38042213562](https://github.com/WhoSia/EPISTEME/actions/runs/38042213562) PASS, 0 new paid calls and 0 real human evaluations. This is an internal synthetic and mathematical reproducibility court only. Source rights, independently certified audit passivity, real proof-role witnesses and prospective held-out source ecologies remain `HOLD`.

**Next P73-P3 attack:** Replace test-fixture `model_attested=True` with externally verified, provenance/time-indexed proof invariants. Attack whether a measurement that preserves the binary conclusion but *changes the source proof role* can still be admitted, and compare invariant/bisimulation criteria against ordinary system diagnosis. Until then, do not promote P73 to paper-ready status, and preserve P69/P70/P71 science HOLDs.
