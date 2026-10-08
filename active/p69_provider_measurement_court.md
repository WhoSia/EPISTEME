# EPISTEME-P69 — Provider Contracts, Technical Pilot and Research Boundary

**State:** Both workflows REGISTERED, both provider-free integration preflights PASS; actual model-provider call data **NOT YET COLLECTED**. P69 itself remains OPEN / PAPER_CONSTRUCT_HOLD. No successor title.

## Source and verification

- Provider-contract worker: [src/p69_provider_canary.py](../src/p69_provider_canary.py), fail-closed aggregator [src/p69_provider_canary_analyze.py](../src/p69_provider_canary_analyze.py).
- Four-slot canary workflow: [.github/workflows/p69_canary.yml](../.github/workflows/p69_canary.yml). The push-triggered [run 37791683578](https://github.com/WhoSia/EPISTEME/actions/runs/37791683578) had **preflight SUCCESS** and the provider and judge jobs **SKIPPED**.
- Pilot worker: [src/p69_instrument_pilot.py](../src/p69_instrument_pilot.py), strict results validator [src/p69_instrument_pilot_analyze.py](../src/p69_instrument_pilot_analyze.py), prospective [pilot manifest](p69_instrument_pilot_manifest.json).
- 192-slot pilot workflow: [.github/workflows/p69_instrument.yml](../.github/workflows/p69_instrument.yml). Push-triggered [run 37792215371](https://github.com/WhoSia/EPISTEME/actions/runs/37792215371) **preflight SUCCESS**, pilot/analyze jobs **SKIPPED**. The synthetic 192-row identity simulation and fail-closed aggregation passed without a provider.
- Original P69 paper preflight previously retained a stale state-suffix assertion inconsistent with updated canonical P69 statuses; it now imports the *real* task IDs/vertices and tests an explicitly open, zero-provider state. This repair was completed before hosted pilot calls.

## What '4+192 calls' means

**Canary:** Groq `openai/gpt-oss-120b`, Gemini `gemini-3.5-flash-lite`. Within each provider the exact same prompt and test JSON object is sent under strict JSON Schema and JSON-object/JSON MIME response policies. One invocation slot per bundle×contract = 4 logical slots maximum. Strict API support in documentation does not guarantee this user's keys, quota, concrete API version or strict validation path; an actual `workflow_dispatch` run must establish those facts. SDK retries may introduce more than one lower-level HTTP request (Google SDK policy not certified) despite no user-level retry loop.

**Pilot:** 2 bundles × 2 PILOT-ONLY task instances × 4 R/T-only vertices × valid/null × 2 response contracts × 3 invocation labels = 192 model invocation slots. Groq/Gemini differ by provider and model family and are NOT an isolated model-family treatment. Within provider channels share byte-identical task payload and prompt. The pilot has no confirmatory p-values, no paper-level effect and no results used for posthoc selection.

**Gate:** pilot `workflow_dispatch` requires the actual 4-call canary's `MEASUREMENT_CONTRACT_READY` artifact, verifies originating workflow/event, and matches the **exact Git head SHA**. It will refuse missing/stale canary artifacts. Four pilot arms must each have >=36/48 provider responses and valid formats plus >=1 grounded true witness and >=1 correct null abstention; otherwise pilot is explicit HOLD, no adaptive rerun or upgrade. An all-zero valid-positive instrument cannot automatically graduate.

## Scientific manuscript gate unchanged

[Formal publication-readiness court](p69_manuscript_readiness_court.md) establishes that the original eight task instances belong to only four shared-authored mechanism families. A four-family signed-symmetry sensitivity reference yields a best possible two-sided p=0.125, not a 0.05 inference. The existing 8192 main-call ceiling is a *planning limit only*. No evidence of model task-effect transport, independent human scoring, externally authored task-mechanism replication or realistic negative semantic controls has been collected by these two technical workflow registrations.

[External SciFact audit](p69_manuscript_readiness_court.md) did verify a real 5,183-entry corpus, 300 development claims, 16 selected source-annotated contradictions, and 128+128 alternative evidence/presentation inputs. But removal or replacement of an annotated source rationale is NOT independently certified null. Two external blind human annotations with privately held HMAC release/ground truth, or a comparably independent valid evidence adjudication protocol, must precede scientific pooling. Passing GitHub's code tests is NOT an independent scientific evaluation.

## Operation and contributor governance

- **First manual action (later):** visit [P69 Contract Canary Actions](https://github.com/WhoSia/EPISTEME/actions/workflows/p69_canary.yml), choose main, Run workflow; the actual run ID is necessary for the next step.
- Inspect that run's artifact `p69-contract-canary-verdict` and require `MEASUREMENT_CONTRACT_READY`. If it fails, stop and preserve the technical error, do not claim a P69 behavioral conclusion.
- Only then open [P69 Instrumentation Pilot Actions](https://github.com/WhoSia/EPISTEME/actions/workflows/p69_instrument.yml), choose main, enter `canary_run_id`. Use the *same head SHA* (no intervening commits). No run occurs merely from a push or a chat message.
- **All workflows read-only:** `contents:read`/`actions:read`. No git push/writeback; `github-actions[bot]` is forbidden as author and committer.
