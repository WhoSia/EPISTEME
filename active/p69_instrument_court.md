# P69 — Manuscript Instrument, Evidence Scoring, and Predictive Court

## Frozen ancestry and purpose
P69 is publication-directed: narrow P53–P65's existing empirical result to representation-operator effects that reverse across tasks and fail frozen out-of-task prediction, while pressure-testing scoring artifacts, contract availability, and external task/model transport. P56, P59, P62, P65, P66, P67, P68 original judgments remain unaltered.

## Current instrument and independent code-path
`src/p69_task_factory.py` generates 4 distinct hand-coded mechanisms (provenance join, directed two-hop composition, conjunction of guarded conditions, and numeric calibration transformations), each with two parameterized instances, 16 balanced R×T/FHL cube vertices, and valid/null twins: 256 main packets. It separately generates provenance_0 and transformation_0 pilot-only instances (64 packets).
`src/p69_independent_scorer.py` neither reads the generator's hidden `valid/null` class nor imports the factory. From the visible packet it independently reconstructs a sufficient evidence set, requires `u1/different` and matching evidence references for a challenge, and tests coherent abstention for a null. Format-invalid output is unobserved semantic correctness, never an observed semantic error.
Presentation factors: R globally renames IDs; F adds unlinked material; H reverses retained-history row order; T reverses within-trace token positions uniformly; L reverses response-rule ordering. All six edits of the matched R/T nuisance contrasts preserve the oracle outcome under the implemented instrument.

## Two hosted, zero-provider-call Action verdicts
1. https://github.com/WhoSia/EPISTEME/actions/runs/37779096105 — completed SUCCESS: 256 main packet oracles, 64 separate pilot packet oracles, 128 indispensable-edge deletion tests and 128 fabricated-rationale rejection tests.
2. https://github.com/WhoSia/EPISTEME/actions/runs/37779477761 — completed SUCCESS: also verifies independent synthetic outcome-lattice analysis on 8,192 identity rows (4,096 valid/null paired cells). A flat fixture and a pair of oppositely signed R-effect families exercise the estimator. This is an analysis test, NOT an LLM experimental result.
`src/p69_offline_audit.py`, `src/p69_predictive_analysis.py`, workflow `.github/workflows/p69_offline.yml`. Workflow permissions `contents: read`, `actions: read`; repository writes and `github-actions[bot]` authored commits are absent.

## Prediction estimand and precise limitations
Within each model and provider-specific channel, define all-call `J` as whether BOTH valid and null semantic twins return correctly grounded, parse-valid answers for the same task/vertex/draw label. `J=0` for provider/format failure operationally, but never label the missing latent semantic answer incorrect. `R` and `T` effect sizes average 8 matched presentation edges. Draw labels are independent attempts, NOT model-API seeds.
LOFO: leave out both instances of one entire mechanism family, learn the mean representation deviation on 6 training tasks, then calibrate held-out task intercept on I/R/T/RT anchors (FHL 000), and predict 12 unseen vertices. Brier accuracy is scored on held-out draws; compare candidate to an anchor-only task baseline. Separate mechanism-family results, model bundle and output channel; no treating 8,192 calls as independent task-family replications.

## Failure and manuscript gates
The two task variants are HAND-CODED under the SAME compiler. They do not qualify as independently authored task ecologies. The current 4 mechanism clusters are too few to prove a universal transport/no-transport claim. Critical recoverable-coarse/sham-rich and external human-scored cases are not implemented in this compiler. Thus `PAPER_CONSTRUCT_HOLD` remains binding despite offline validation.
Two distinct output contracts per model are unverified in provider live response; Gemini support must be audited without switching providers based on results. The P67 hosted channel experiment has NOT run, only two zero-call preflights. P69 pilot is not authorized until response-contract readiness and exact inference protocol are frozen. Budget limits: 192 instrumentation-only calls; 8,192 model calls maximum afterward; NONE executed in P69.
Paper novelty CANNOT be task-dependent prompt sensitivity, tensor factorization, low-rank transport or parser differences alone. Prior art: Hua et al. 2025, Qin et al. 2026, Yang et al. 2026, Lin et al. 2026. The future contribution needs independently grounded task ecology, scorer-artifact control, second-model replication and genuinely held-out predictive results.

## Repository and Lab hygiene
Orphan EPISTEME-P54 Labs row was moved under canonical EPISTEME Lab without deleting content or changing its historical P54 TECHNICAL_HOLD. Other Lab rows are unchanged.
Commit author and committer must both be WhoSia. No GitHub Actions bot commits, workflow pushes or content write permissions.

## P69 v2 scorer and retention-construct court (2026-10-08)

**Original scorer defect discovered BEFORE any P69 model run:** the first version accepted any rationale_ids superset of the required proof, provided all extra IDs existed somewhere in the packet. A shotgun list of all genuine evidence IDs was incorrectly certified. This constitutes a possible measurement artifact and invalidates any future inference based on the original permissive rule; previous GitHub instrument PASS receipts refer to the earlier, weaker tests, not the new v2 standard.

**v2 repair:** `src/p69_witness_enumerator.py` enumerates all inclusion-minimal focus-owned u1/different proof sets for four grammars. `src/p69_independent_scorer.py` now separately returns `answer_correct` (direction/abstention correct), `rationale_minimal` (exactly one minimal proof with no duplicate or irrelevant evidence IDs), and `semantic_correct` (legacy API name for strict GROUNDED correctness). Malformed format yields an unobserved answer rather than an incorrect latent answer. A model with a correct direction but additional irrelevant evidence is answer-correct and grounded-incorrect, not indistinguishably wrong.

**Projection controls:** `src/p69_retention_controls.py` constructs 8 tasks × 16 vertices × 3 latent world classes × 3 projections = **1,152 model-visible packets** from **384 synthetic latent conditions**. Truth signatures: critical Rich/Coarse/Sham 1/0/0; recoverable 1/1/0; null 0/0/0. All coarse views delete actual rich facts; each sham draws its extra nondefeating decoy attestations from the same latent truth reserve, keeps the rich view's fact count, and contains NO fabricated evidence. These projections are **offline-only** and are NOT part of the 8,192-call main lattice; adding hosted control calls requires a new, explicitly frozen allocation.

**Independent implementation check:** `src/p69_retention_selftest.py` uses a separate reference reachability and rule evaluator; 1,152/1,152 decisions agree with the minimal-proof enumerator. 128 shotgun rationales and 128 duplicated-rationale attacks rejected. Two distinct sufficient proofs accepted for each recoverable-rich cell (256 acceptance cases). [Read-only hosted run 37782896510](https://github.com/WhoSia/EPISTEME/actions/runs/37782896510) PASS, 0 provider calls.

**External adjudication preparation:** `src/p69_blind_adjudication.py` creates a 72-case human evaluation panel balanced across 8 tasks × 3 classes × 3 projections. Public case IDs and all evidence identifiers are consistently pseudonymized, the order is fixed-shuffled, and the public artifact has `case_id/archive/annotation` only. Ground truth labels and acceptable proof sets are NOT part of the published artifact. [Read-only hosted run 37783527335](https://github.com/WhoSia/EPISTEME/actions/runs/37783527335) PASS; public artifact ID `11553141646`, JSONL SHA-256 `0beb6fd69296ef454b4f5828534ef678da30c6ff25555c116ff9e1b6a5abc103`; model calls=0. A separate container check verified 72 unique cases and absence of oracle labels/keys. **No independent human evaluation has yet occurred.**

**Paper gate still locked:** only independent evidence-grounded external adjudication, truly different task-world authorship and externally verified realistic artifacts can remove the publication construct hold. Separate model/provider format calibration (P67) and a preregistered cluster-level statistical inference decision are also necessary. A 1,152-cell offline pass does not establish LLM behavior, and the 72-case public pack is an annotation instrument, not annotation evidence.

**Human-only repository history:** GitHub Actions permissions `contents:read`, `actions:read`, upload artifact only. Zero github-actions[bot] authored or committed changes.


## P69 post-audit blinding correction — public preview versus genuine blind evaluation

**Critical correction after the successful 72-case artifact run:** the original `case_id` was a SHA-256 digest of one of only 8×3×3 publicly enumerable task/class/view combinations. An evaluator with access to the open compiler could recover the hidden pairing by trying all 72 combinations. Hiding label columns alone was NOT sufficient cryptographic blinding.

- Existing [run 37783527335](https://github.com/WhoSia/EPISTEME/actions/runs/37783527335) artifact `11553141646` is henceforth **PUBLIC LABEL-OMITTED PREVIEW, NOT SECURE BLIND ANNOTATION**. Its historical successful code integration is retained, but its public case identifiers have no genuine independent-blind authority.
- `src/p69_blind_adjudication.py` now has a two-mode contract: `--preview` explicitly produces nonblind deterministic examples; production external scoring requires `--secret-file` containing at least 32 privately held random bytes, using HMAC-SHA256 for case identifiers, identifier remapping and secret-dependent case ordering. Its optional `--private-key` matching oracle is allowed only in local secret-key mode.
- `.github/workflows/p69_offline.yml` explicitly uses `--preview`, marks any artifact `p69-annotation-preview-NOT-BLIND`, and never accesses the private key or uploads a sealed oracle. The secret is not in this repository.
- A meaningful independent third-party score requires a new private-salt production export, separate private answer-key custody, annotators who were not exposed to the condition mapping, and a frozen annotation rubric. **No such completed third-party adjudication exists.** All paper-level claims retain `PAPER_CONSTRUCT_HOLD`.

This safety correction does not change the old P56/P59/P62/P65 scientific verdicts or the P69 main experiment budget.
