# EPISTEME-P72-P1 — Typed Proof Survival, Observation-Fibre Court & P73 Formal-Name Proposal

**Scope:** P72-P1 formal/computational research only. `DRIVE_BROWN_ORIGINAL_CONFIRMED / DRIVE_PERDOMO_CONFIRMED / DRIVE_ZHANG_UNVERIFIED_SEARCH_ONLY / P72_P1_FORMAL_COURT_RUNNING_OR_PASS_IF_CI_VERIFIES / NO_EMPIRICAL_P73_ACTIVATION`.

## 1. Updated prior-art custody — verified, not guessed

**Perdomo, Zrnic, Mendler-Dünner & Hardt (2020), *Performative Prediction*.** Google Drive **보유 확인**, two copies: [full author-list copy](https://drive.google.com/file/d/1i3Db3WOaHqxcm5SD5-HewjmAZOVnSv11/view) and [short-title copy](https://drive.google.com/file/d/1xqSmelD1B713q3TSTHJxFVujuKvWDtjC/view). Precedes P72 on deployed decisions changing observed data distributions. The matching exact-title copies are likely duplicates by title, **not SHA-confirmed exact duplicates**.

**Brown, Hod & Kalemaj (2022), *Performative Prediction in a Stateful World*.** Google Drive **신규 보유 확인, 원문 정독**, filename `brown22a.pdf`, [exact Drive source](https://drive.google.com/file/d/1690w4PxcI0lHBFgNmTulv_CkFS36r79p/view). AISTATS 2022 original [PMLR](https://proceedings.mlr.press/v151/brown22a.html). The paper's central transition is `d_{t+1}=Tr(d_t; theta_t)`; it studies k delayed-response groups, geometrically decaying responses and model-dependent Markov matrices. Its epsilon-joint Wasserstein sensitivity, contraction regime, and Theorems 2/4 (as labeled in main paper) give convergent repeated-risk-minimization results under model smoothness/convexity assumptions. **Direct collision:** claiming that stateful/history-dependent deployment, delayed group uptake or convergence under a contractive transition is a new P72 law. Original PDF checked through Drive, not inferred from abstract alone.

**Zhang, Cammarata, Squires, Sapsis & Uhler (2023), *Active learning for optimal intervention design in causal models*.** Correct DOI `10.1038/s42256-023-00719-0`. Targeted exact-title/DOI/author Drive searches and recent file index did **not** identify a matching PDF: **Drive 미확보(검색 기준), 원문 확보 확인 불충분**. The authenticated publisher [original article](https://www.nature.com/articles/s42256-023-00719-0), [NIH author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC13528741/) and [MIT published-source repository](https://dspace.mit.edu/entities/publication/bcca862a-7b77-44cf-a56d-4f8e1f05d410) were checked externally. The paper's intervention-seeking Bayesian causal acquisition function, tractable acquisition calculations, and consistency theory already undermine generic 'we optimize which intervention to sample' originality. Do not claim this external-text review is a Drive read.

**Other relevant in-Drive original sources (explicitly different papers):** [Tigas et al. 2022, *Interventions, Where and How*](https://drive.google.com/file/d/1_z_I2WJ9E4dyxLY0PlIGJhslhgTEjGyR/view), [Hauser & Bühlmann 2014](https://drive.google.com/file/d/1LSnwndyatbqTJBt2i4jX7zREuW7cQbGE/view), [Elahi et al. 2024](https://drive.google.com/file/d/1EIfkGQi8Luuypk0Q8qa6BONoIxQ9DaCS/view). These are **candidate further comparisons, not yet fully re-read for P72**.

## 2. P72-P1 precise problem — proof validity, not only state

A visible citation ID need not be an admissible premise. Define a finite monotone inference state `S=(V,A,R,g,t)`: visible citation handles `V`, admissible premise tokens `A`, valid Horn inference rules `R`, migration conclusion `g` and time `t`. A goal has **warrant** when `g` belongs to the least deductive closure of `A` under `R`. This finite construction is a toy logical model; context-sensitive truth, defeaters and institutional authority are NOT represented adequately by bare Horn rules.

An evidence transformation `phi` transports old premises, valid rules and the old goal into admissible new premises, valid new rules and the same target goal. **Sufficient forward-proof preservation:** by induction on finite proof depth, every derivable old conclusion maps to a new derivable conclusion. This is ordinary forward simulation / proof homomorphism, **not a claimed new theorem**.

**Important non-equivalence:** forward rule-copying is NOT necessary for a given conclusion to survive, because the target might support it through an alternative independent proof. Thus 'phi preserves each old rule iff the final migration goal survives' is false without stronger completeness/reflectivity assumptions. P72-P1 explicitly includes this counterexample.

## 3. Exact identification boundary

Take hidden worlds `W+ / W-` with the same publicly visible citation, same time, initial admissibility and identical inference rules. Both initially justify `MIGRATE`. Under the audit action, the W- underlying premise becomes inadmissible but the public citation handle remains visible. W+ retains the premise. They have **identical post-audit observations** but diverge on migration warrant.

For any finite model with observation map `O` and target warrant predicate `Q`, **exact nonparametric identifiability of Q from O requires and is equivalent to constancy of Q on each observation fibre O^{-1}(o)**. Necessity: two observationally indistinguishable states disagreeing on Q are an impossible inference task. Sufficiency: define a well-posed function `f(o)=Q(s)` for any compatible `s`. This is elementary observable-quotient theory / structural identifiability, **not new EPISTEME mathematics**.

The new computational court [src/p72_warrant_fibre_court.py](../src/p72_warrant_fibre_court.py) uses both counterworlds. A hypothetical independent, passive audit of *hidden revocation status* separates them; merely inspecting the citation handle does not. **Crucial boundary:** this diagnostic probe's true passive, safe and deployable status is NOT empirically established. An intrusive probe may create new changes, thereby invalidating the observation fibre it intended to separate.

## 4. Competition and empirical obligations

| Candidate mechanism | Prior theory / internal ancestry | Testable P72 novelty gap |
| --- | --- | --- |
| History-dependent deployment changes environment | Brown 2022 (Drive original) and P2/P4 internal | No new result merely from state history |
| Optimal choice of causal interventions | Zhang et al. 2023 (external original; Drive not verified), classical active design | No new result merely from information-gain optimisation |
| Partial observations cannot identify counterfactuals | Original P3/P4, existing identification theory | Need a *new* independently certified warrant predicate and nontrivial experimental separation |
| Citation syntax same but proof authority changes | P70/P71 local partial bridge + P72 timed interventions | Candidate target: independent observation of warrant admissibility and sequence-specific proof validity |
| Cheap independent probe safely restores switch decision | Value of information / minimax-risk theory | Must show no intervention-induced probe effect and measured audit/migration cost, not inferred from code |

**Prospective kill tests:** P72 claim FAIL if human-independent ground truth disagrees with the posited warrant graph, if the diagnostic probe changes the target, if history-specific observational fibres remain ambiguous, if effect is entirely explained by Brown-stateful dynamics and ordinary target-variable augmentation, or if proof transport adds no decision value over an untyped observation baseline.

**Empirical gates unchanged:** P71's 16 masked AVeriTeC packets need 2 distinct independent human reviews (0/32 real recorded); claim clusters are 4, not 16 independent real-world claims. P69 manuscript remains HOLD; P70 semantic/transport remains HOLD. New provider calls 0.

## 5. P73 formal title — proposed only, not open

**EPISTEME-P73 — Warrant-Separating Observation under Reflexive Evidence Dynamics: Minimal Discriminating Audits, History-Indexed Proof Transport, Intervention-Safe Identification & Sequential Switching Decisions Court**

**Core question:** Suppose a history-dependent audit system makes the *same available observation* compatible with both a valid and an invalid migration warrant. Which additional **non-destructive, independently admissible observations** are necessary to distinguish those worlds, and can one choose a finite low-cost separating policy without changing the target it intends to identify?

This changes focus from P72's existence of pathwise warrant ambiguity to **the construction and falsification of a separating observation strategy**. An untyped mathematical set-cover solution alone is classic and unpublishable as novelty; a new independently verified passivity/dependency/semantic result and held-out evidence are required.

**P73 admission proposal:**
- P0: identify hidden-world ambiguity classes for target warrant and show a defensible candidate observation whose source-time identity and effect on the system can be independently checked.
- P1: consider multiple admissible candidate probes with costs, auditing harms, and proof-graph coverage; reject cheap probes that erase evidence.
- P2: distinguish observational discrimination from intervention-induced changes (observe/probe/announce are different actions), retaining noncommuting histories.
- P3: compare minimal safe separating probes against classical causal active learning, system identification and robust decision baselines.
- P4: measure SWITCH/RETAIN/HOLD error and actual review costs only after source rights, independent reviewers and a frozen prospective experimental design.
- P5: do not open P73 empirically or incur provider costs by proposing its title.

**Current authority:** `P72_P1_FORMAL_COUNTERMODEL_ONLY / P73_FORMAL_NAME_PROPOSED_NOT_OPEN`.
