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