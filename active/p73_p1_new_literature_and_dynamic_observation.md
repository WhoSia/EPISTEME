# EPISTEME P73-P1 — History-Safe Observation and Original Decision-Tree Literature Court

**Status:** `P73_P1_FINITE_DYNAMIC_DIAGNOSIS_CI_PASS / CLASSICAL_THEORY_PRIOR_ART / REAL_PROBE_SAFETY_HOLD / P69_PAPER_HOLD / P70_SEMANTIC_BRIDGE_HOLD / P71_HUMAN_REVIEW_0_OF_32`

## Four newly received primary sources, all read in Google Drive

The uploader placed exactly four files in `00_INTAKE — Literature Radar` on 2026-10-10 around 09:33–09:34 UTC. The PDFs were identified by **file ID and original front matter**, not only fuzzy search. After searching for exact titles/duplicate metadata, each was canonicalized and transferred to `10_PAPERS — Canonical Literature Commons`, **preserving the original Drive file ID**.

| Original paper | Canonical Drive original | Source state | Relationship |
| --- | --- | --- | --- |
| **Hyafil & Rivest (1976), *Constructing Optimal Binary Decision Trees Is NP-Complete***, *Information Processing Letters* 5(1):15–17, DOI 10.1016/0020-0190(76)90095-8 | [Drive PDF](https://drive.google.com/file/d/1i4AUMzbYhYOLvA_H5Mw7wBVBATP4YsGR/view) | **Drive secured, original full short paper inspected; scanned character extraction imperfect** | Direct complexity antecedent: a decision tree minimizing expected tests to identify an unknown object is NP-complete. The text also discusses worst-case variants. P73's 4-state exact DP is not an efficient general solution or original complexity result. |
| **Verwer & Zhang (2019), *Learning Optimal Classification Trees Using a Binary Linear Program Formulation***, AAAI-19 | [Drive PDF](https://drive.google.com/file/d/1kQMSkaCz1fhLn4fAHn5OI5EYygcqSj8y/view) | **Drive secured, methods/body inspected** | BinOCT encodes fixed-depth classification-tree learning with a binary linear program, improving split-threshold encoding. Its objective is training-sample classification, **not** adaptive interactive probe cost under a warrant-safety restriction. |
| **Avellaneda (2020), *Efficient Inference of Optimal Decision Trees***, AAAI-20, DOI 10.1609/aaai.v34i04.5717 | [Drive PDF](https://drive.google.com/file/d/11VHs_cumtrE08i1otc3llbVV9s0wGLNA/view) | **Drive secured, methods/body inspected** | Incremental SAT / counterexample-driven refinement seeks minimum-depth classifiers consistent with the training set. Useful alternative optimization encoding, but not itself a proof that observation is evidence-preserving. |
| **Firat, Crognier, Gabor, Hurkens & Zhang (2020), *Column Generation Based Heuristic for Learning Classification Trees***, *Computers & Operations Research* 116:104866, DOI 10.1016/j.cor.2019.104866 | [Drive accepted manuscript](https://drive.google.com/file/d/1U-Yly-n0h-nccac3payWJ-0nyVuZUJ_x/view) | **Drive secured, 2019-accepted/pre-publication manuscript read** | Original retained cover title *Column Generation Based Math-Heuristic for Classification Trees*; final published title differs. Integer-programming path columns and CART-selected candidate splits accelerate classification-tree training. Does not solve safety verification or dynamic interactive identification. |

**Publication-title check:** Firat's DOI resolves to *Column generation based heuristic for learning classification trees* (2020); do not mistake a 2019 accepted manuscript for the 2020 publisher PDF. Original scan-based Hyafil transcription has character errors, so do not rely on copied symbols without page-image verification.

The four **were not exact-byte duplicate files among these IDs** as shown by distinct IDs/metadata sizes, but a canonical title/DOI search is *not* a cryptographic whole-Drive duplicate audit. Do not report global byte-level nonduplication absent SHA/MD5 corroboration.

### Further nearby originals previously in Drive

Türker, Ünlüyurt & Yenigün (2016), adaptive distinguishing sequences, [Drive original](https://drive.google.com/file/d/10N6hZKeeKT6zMp0udLza4Si1yIaYEKUm/view) is more directly comparable to active probe trees than three classifier-training papers. Hauser & Bühlmann (2012), interventional DAG equivalence, [Drive original](https://drive.google.com/file/d/1eMqlfzxAZpNGbMFOCS96ZU_oosXUNxkN/view), preempts generic identification claims. Brown et al. (2022), stateful performativity, [Drive original](https://drive.google.com/file/d/1690w4PxcI0lHBFgNmTulv_CkFS36r79p/view), preempts generic history/state-change claims. Rivest & Schapire (1993), homing sequences, [Drive file](https://drive.google.com/file/d/1JNqBDFbRgaUEHBwDQJVhgWM1CPkFn1pp/view) present but extractable body was unavailable at last check.

## P73-P1 technical result — finite active observability with safety restrictions

[`src/p73_history_safe_court.py`](../src/p73_history_safe_court.py) explores a finite deterministic belief-set model. A world carries a fixed binary warrant predicate `Q`, an evidence/proof token and a mutable private-reader readiness bit. The `PREPARE` action (cost 1) changes readiness without changing `Q` or the proof token. `READ` (cost 1) returns `unready` before preparation; afterward it returns the true warrant predicate without modifying the world. Therefore the exact best worst-case plan is **PREPARE, then READ**, with worst cost **2**.

By contrast, the stronger **full-state identity** standard rejects PREPARE simply because a measurement capability changed, even though proof-relevant state did not. It yields `NO_CERTIFIED_SAFE_POLICY` on this artificial example. The result illustrates the need to define the *part* of the state the proof certificate protects.

### Admissibility-aware global obstruction

Consider three candidate worlds A (warrant false), B and C (warrant true). `LOCAL_AB` distinguishes A vs B but cannot be executed in C; `LOCAL_AC` distinguishes A vs C but cannot be executed in B. Each opposite-label **pair considered separately** has an available safe test. Yet no test is admissible across the original three-world belief set; **there is no globally safe first action and no safe policy**.

This explicitly refutes carrying P73-P0's fixed-availability pairwise separation iff into state-/belief-dependent probe availability without modification. The correct dynamic research object is an **admissibility-aware, history-indexed policy**, not a globally fixed union of all individually separating tests.

The current exact finite-policy algorithm recursively considers only actions preserving the currently modeled proof token and `Q` on **every reachable possible world**, rejecting globally inadmissible, source-unattested and destructive actions. This is a *model-relative check*, not externally verified noninterference. Its absence of a policy for a finite toy belief is not a theorem about real systems. It retains classical active diagnosis as the closest prior theory.

## P73-P2 target and proof obligations

1. Build a typed history-state observation kernel `T(s,a)` and define **which proof-relevant predicates or witness roles must be preserved**. Compare exact invariant-preserving transitions to weaker observational/bisimulation equivalence. The pre-specified target must not silently switch from pre-audit to post-audit warrant.
2. Construct a finite **controllable-predecessor / winning-belief fixpoint** and prove correctness for terminating finite policies with positive costs; compare it with active automata learning, ADS and partial-observation safety games. This fixpoint concept is already classic: novelty must come from certified proof-role obligations or an independently testable empirical separation.
3. Attack 'safety by boolean declaration': a probe marked attested in fixture is not an independent custodian signature or proof of noninterference. Require reproducible source snapshots, time-stamped provenance and a genuine audit-safety witness before any real-world PASS.
4. Compare optimizing expected/worst cost, *target-specific* warrant identification versus full-state identification, and the cost of refusal/extra review. Record no-safe-policy even when an unsafe perfect-information test appears cheap.
5. Re-open the paper gate only if actual held-out source ecologies and independent human adjudicators certify the target warrant and probe effects. P71 AVeriTeC independent 16×2 ratings still **0/32**; don't use them as observed labels or treat four underlying claims as sixteen independent cases.

**Epistemic ceiling:** exact mathematical **toy tests passed**, four newly added primary papers now read and canonicalized, no novel theorem or empirical noninterference established. No P69/P70 scientific HOLD is lifted, no new provider calls or participant study.
