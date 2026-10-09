# P69-R1 — Paired Measurement-Contract Repair, Smallest Bounded Live Retest

**Precommitted 2026-10-09 KST.** Technical repair/calibration, not P69 manuscript closure.
**Status:** `R1_SOURCE_AND_OFFLINE_PREFLIGHT_PASS / LIVE_R1_NOT_DISPATCHED / HISTORICAL_P69_TECHNICAL_PILOT_HOLD`.

## Observed 192-call failure, unchanged
- At exact head `18cb018c4792d814c888e855fd494809d41a6bde`, [live pilot #37925719478](https://github.com/WhoSia/EPISTEME/actions/runs/37925719478) obtained 192/192 provider responses and an aggregate `TECHNICAL_PILOT_HOLD` in artifact #11613872997, notwithstanding the green GitHub Actions runner.
- Groq JSON-object arm: 34/48 format-valid, **14/48 format-invalid**. Several responses use free-text direction vocabulary (for example "contradicts") rather than the prespecified `predicted_direction` enum `same|different|null`; 12 of the 14 format losses occurred in task `transformation_0` positive semantic cases. Missing indispensable evidence IDs are a separate stricter-grounding failure and are not repaired by relabeling.
- Gemini JSON-object arm: 47/48 format-valid, but **0/24** valid-semantic cases had a grounded-correct response. Most positives returned an abstention-like `NONE`, an answer-direction failure rather than an output-format failure. A new JSON schema alone cannot be assumed to fix reasoning.
- Both strict-schema arms achieve 48/48 valid formats but still have distinct grounded-reasoning errors. Output validity, direction correctness, inclusion-minimal proof correctness and provider response are separately recorded.
- Do not retrospectively recode the historical 192 responses, widen the scorer's enum, or treat format-invalid observations as latent negative semantics.

## Research question
Does making the evidence-tracing and exact-output decision procedure explicit improve **measurement feasibility** without erasing positive/null discrimination, compared with the originally frozen P69 task prompt? This experiment measures prompt-version sensitivity, not a transport effect. The semantic oracle and the response channels are otherwise unchanged.

## Frozen 64-slot crossed protocol
- Bundles: `gemini-3.5-flash-lite` on Google and `openai/gpt-oss-120b` on Groq. The bundle is model+provider.
- Cases: `provenance_0`, `transformation_0` × `valid`, `null` × 1 identity R/T vertex.
- Prompt versions: `frozen_v0` (byte-identical to the P69 pilot's task prompt for this cell) and `procedure_v1` (trace focus, compare u1 response with terminal, require complete indispensable evidence chain, enforce exact JSON keys and allowed direction values). Both versions shown to both semantics, never supplied the gold label.
- Response channels: `strict_schema`, `json_object`, with the **same prompt bytes across channels** within each model/task/semantic/version/draw.
- Independent hosted invocations: two per cell, with deterministic randomized order and no SDK retries.
- Total planned = 2 bundles × 2 tasks × 2 semantic classes × 2 prompt versions × 2 output channels × 2 draws = **64 provider calls**. A new same-run four-slot actual canary must succeed *before* any of the 64, for an absolute request ceiling of **68**.
- Both versions are scientifically NEW experimental arms. No results are pooled with the earlier run as if these were the same randomized allocation.
- `src/p69_measurement_repair.py` implements worker and immutable prompt contracts. `src/p69_measurement_repair_analyze.py` verifies exact grid, model IDs, packet+prompt SHA, paired prompt equality, and all-call failure bookkeeping.

## Gates and authority
For each of four (model, channel) groups under **procedure_v1**, 8 draws (2 tasks × 2 semantics × 2 invocations):
- Require exactly 8/8 provider responses and >=7/8 valid JSON/field schemas.
- Require >=1/4 properly grounded positive-valid case and >=1/4 properly grounded null case.
- Store exact descriptive `procedure_v1-frozen_v0` differences for format validity, positive evidence and null evidence. Baseline performance is NOT a post-hoc selection gate.
- A failure in any improved arm returns `REPAIR_MEASUREMENT_HOLD` and process exit 2, with receipt preserved; passing returns `CALIBRATION_SIGNAL_PRESENT`, meaning **only** small-sample feasibility, not efficacy, cross-task transport or publication.
- Avoid hypothesis-test p-values or pretense of independent task replication: there are **two authored canary task clusters**, not 64 independent scientific units.
- Subsequent 192/8192 tests are separately designed, separately human-authorized and blocked until external independent content/ground-truth and readout controls are satisfied.

## Operational governance
- `.github/workflows/p69_measurement_repair.yml` is read-only, manual `workflow_dispatch` for paid calls. Its first stage requires exact input `RUN_68_CALLS`. Any push runs only dependency-loaded offline self-tests; no automatic paid calls, code commits, or worktree modification by Actions.
- User's financial consent is not equivalent to a promise of free API use. The maximum count is bounded; actual service bill depends on provider tokens/rates.
- P69 paper remains `OPEN / MEASUREMENT_HOLD / PAPER_CONSTRUCT_HOLD`, irrespective of a future small calibration success.
