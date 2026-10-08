# P69 — Gemini Provider-Contract Failure and Repair Court

**Recorded 2026-10-09 (KST). Stage P69 remains open.** This is a technical diagnosis and instrumentation patch, not a completed behavioral study and not proof that the failed Gemini request now works.

## Frozen evidence

- Live [run 37793112647](https://github.com/WhoSia/EPISTEME/actions/runs/37793112647), event `workflow_dispatch`, HEAD `930330ed8dda517d674c81b45e2b04af83597201`.
- Actual model tasks: Groq strict 1/1 PASS, Groq JSON object 1/1 PASS. Gemini strict 0/1 ClientError, Gemini JSON-only 0/1 ClientError.
- Original [verdict artifact 11558120027](https://github.com/WhoSia/EPISTEME/actions/runs/37793112647/artifacts/11558120027) returned `TECHNICAL_CONTRACT_HOLD` while GitHub job's operating-system exit code was 0. Do not interpret Action-level `success` as an approved provider contract.
- Gemini shard [11557361464](https://github.com/WhoSia/EPISTEME/actions/runs/37793112647/artifacts/11557361464): only `ClientError`, no HTTP code or body were captured; exact cause cannot be reconstructed from those stored fields.
- Official [Gemini 3.5 Flash-Lite model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite) lists `gemini-3.5-flash-lite` as a stable, structured-output-capable model. That does not establish access by the project's particular API key.

## Source-level repairs after the failed run, without new model generation

1. `src/p69_safe_error.py` derives redacted HTTP code and allowlisted diagnostic category; raw error text, prompts, key material and full response bodies are **never** stored as error diagnostics.
2. `src/p69_provider_canary.py` now records per-contract `error_diagnostic`. When Gemini fails, it additionally does one *non-generative* `models.get` metadata lookup and records only availability or categorized failure. No fallback model substitutions and no null/error-to-semantic-imputation.
3. Gemini clients use explicit `types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1))` to prevent SDK-level retry inflation. The same policy is applied to `src/p69_instrument_pilot.py` (the original Groq client already had max_retries=0). This changes the request operational contract before any P69 pilot, not after its results.
4. `src/p69_provider_canary_analyze.py` now includes the scrubbed diagnostics. A `TECHNICAL_CONTRACT_HOLD` produces nonzero process exit after writing its receipt; the workflow's `if: always()` step still uploads the result. This prevents deceptively green failed tests.
5. Model/contract success and failure cases are included in provider-free self-tests. They are **software tests only**, not a live Gemini verification.
6. Optional [.github/workflows/p69_gemini_metadata.yml](../.github/workflows/p69_gemini_metadata.yml) performs only a non-generative model metadata lookup, with no model text generation; its source registration is not evidence it has run.

## Strict reauthorization

- After final source/documentation commits, **do not update main** between the next manual four-slot canary and subsequent 192-slot pilot, because the latter verifies the originating successful canary's exact HEAD SHA.
- A user-triggered [P69 Provider Contract Canary](https://github.com/WhoSia/EPISTEME/actions/workflows/p69_canary.yml) on the then-current `main` is required to observe the fixed diagnostic. If it fails again, inspect the redacted HTTP/status category and stop; **do not** launch the 192-slot pilot or replace Gemini with a more favorable model.
- Only a real `MEASUREMENT_CONTRACT_READY` artifact permits the separate manual measurement-only pilot. A successful 192-slot pilot still cannot establish P69's paper claim, because independent task ecologies, masked human ratings and enough independently authored mechanism families have not been obtained.
- The 8,192 main study remains on research HOLD with no execution authorization.

**Verdict today:** `TECHNICAL_DIAGNOSTIC_REPAIR_COMMITTED / LIVE_GEMINI_VALIDATION_PENDING / PAPER_CONSTRUCT_HOLD`.

**Repository governance:** manual WhoSia GitHub-account commits only. Never allow `github-actions[bot]` to author or commit. Read-only workflow permissions with no writeback.
