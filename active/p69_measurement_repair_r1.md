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

## Historical first paid launch, judge bug and nonduplicating recovery

User-dispatched [#37929410643](https://github.com/WhoSia/EPISTEME/actions/runs/37929410643) at frozen source SHA `2363dc9b176afbd574dd1efce5999fdded25b1a1` successfully executed both two-call model Canary jobs (all four output contracts valid). It then FAILED at `canary_gate` and `analyze` due to missing existing Groq provider SDK dependency imported transitively through `p42_reopen.py`. **No 64-call calibration job executed.** The original 4 calls are real and must never be restaged solely to fix the workflow.

Current `.github/workflows/p69_measurement_repair.yml` now installs the SDKs in both read-only judge jobs; provider-free push CI passed. A separate read-only [receipt recovery run #37930648628](https://github.com/WhoSia/EPISTEME/actions/runs/37930648628) downloaded and verified the original two model shards with zero provider calls; verdict **`MEASUREMENT_CONTRACT_READY`**. [Gemini Canary source](https://drive.google.com/file/d/1OkJqdXmiMaqsd1SfAEcAWa9QfN1ytDip/view), [Groq Canary source](https://drive.google.com/file/d/1R-cByC7nNgmpj1sz89_uFGzyinFpRSTl/view), [recovered Canary verdict](https://drive.google.com/file/d/1Obx1y6WyKUOe3gXdc_FVsbE42-8YxzA7/view) are independently archived in EPISTEME Drive; folder metadata readback verified.

**Do NOT repeat `RUN_68_CALLS`.** The correct continuation is [P69 R1 resume only remaining 64 workflow](https://github.com/WhoSia/EPISTEME/actions/workflows/p69_r1_resume_64.yml), with exact `confirm_spend=RUN_REMAINING_64`. Its first job checks the old dispatch ID, original exact source SHA and four actual prior model contracts; every source checkout is frozen at the original `2363dc9b` commit so newer workflow fixes do not mutate the original experiment's prompt/instrument. It then executes two 32-slot batches, and fail-closed analyzes their receipts. The new 64 calls require a separate manual authorizing dispatch; **no further P69 provider calls have been made**. Offline push preflight [#37930782814](https://github.com/WhoSia/EPISTEME/actions/runs/37930782814) PASS: same-SHA historical canary, worker grid, judge red/green tests, 0 provider calls.

**Paper status:** Historical P69 192-call pilot remains `TECHNICAL_PILOT_HOLD`; P69 R1 64-call repair calibration is `NOT_RUN`; 8,192-call main remains unauthorized. Salvaged provider canary PASS does not promote science.

## Verified actual R1 continuation — 64-call result (2026-10-09 KST)

The intended remaining-64-only [human workflow_dispatch #37931512662](https://github.com/WhoSia/EPISTEME/actions/runs/37931512662) did execute at the **original frozen experiment source** SHA `2363dc9b`, after verifying the historical four-call Canary. Both provider jobs completed 32/32; the judge returned `P69_REPAIR_MEASUREMENT_HOLD`, exit 2, despite successful provider jobs. Do NOT retry, scale, or re-label this result as a CI infrastructure bug.

**Observed predeclared gate by provider and response contract (8 calls per arm; 4 valid / 4 null):**

| Bundle | Prompt | Channel | Format-valid | Grounded valid | Grounded null | Repaired-arm gate |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Gemini | frozen_v0 | strict | 8/8 | 2/4 | 4/4 | baseline |
| Gemini | frozen_v0 | JSON object | 8/8 | 0/4 | 4/4 | baseline |
| Gemini | procedure_v1 | strict | 8/8 | **0/4** | 4/4 | **HOLD** |
| Gemini | procedure_v1 | JSON object | 8/8 | 4/4 | 3/4 | PASS |
| GPT-OSS | frozen_v0 | strict | 8/8 | 1/4 | 3/4 | baseline |
| GPT-OSS | frozen_v0 | JSON object | 5/8 | 0/4 | 4/4 | baseline |
| GPT-OSS | procedure_v1 | strict | 8/8 | 4/4 | 3/4 | PASS |
| GPT-OSS | procedure_v1 | JSON object | 8/8 | 4/4 | 4/4 | PASS |

The Gemini strict arm's two positive task clusters both returned `ANSWER_WRONG` in both draws; the response contract was satisfied in every case, making this an **answer-direction/grounded-signal** failure rather than a malformed-JSON failure. The same procedure apparently helps Gemini's JSON-object arm, so interpreting one prompt edit as a transferable improvement would conflate decoding contracts, model/provider bundle, and task ecology. Two authored tasks and two draws per cell do not establish a stable causal interaction.

**Provenance/custody:** original R1 verdict artifact #11616108547; actual Gemini #11616326279 and Groq #11616008880. Same artifacts archived in canonical EPISTEME Drive with successful folder listing:
[Gemini rows](https://drive.google.com/file/d/1-YaUoImgmCeu4NqVfqFSKu0kHdZuHlKi/view) · [Groq rows](https://drive.google.com/file/d/1iwSu4A1QQekLvHdsykCtC-hBfyKrO2HE/view) · [HOLD verdict](https://drive.google.com/file/d/1Uehn5mxby4Kcvgx0dpc-IUSHKpHmqRmJ/view).

**Authority:** `R1_LIVE_COMPLETED / REPAIR_MEASUREMENT_HOLD / P69_PAPER_CONSTRUCT_HOLD`. All 64 calibration slots spent; no additional provider calls authorized. The user should NOT start any prior R1 workflow again. Next activity: theory-led response-contract interaction and external ecological/independent scorer discrimination, without immediate billed scale-up.

## Paper-construct reappraisal from full original hosted rows (2026-10-10)

The full **192 historical pilot + 64 actual repaired live** provider replies, plus P70's 32 actual SciFact responses, were fetched using `actions: read` from their original source runs and replayed in [P69/P70 forensic code](../src/p69_p70_frozen_paper_court.py). Actual zero-new-call [GitHub #38043376874](https://github.com/WhoSia/EPISTEME/actions/runs/38043376874) SUCCESS. [Full scientific court](p73_p4_p69_p70_joint_research_court.md), [Drive receipt](https://drive.google.com/file/d/16xPtTFG7ryS0_si8esB7klvzdTKaCIBg/view).

**Strongest observed empirical contrast:** Gemini explicit `procedure_v1` positive cells Strict `0/4`, JSON `4/4`, with both formats `8/8` valid; the failure lies in answer-direction classification. Baselines were Strict `2/4` and JSON `0/4`. Positive fraction difference-in-differences = `1.5` **descriptively**; the two task clusters differ in their baseline contrast, and two hosted draws per cell do not supply a replicable scientific sampling frame.

**Independent measurement hazard confirmed in original SciFact rows:** Gemini's category verdict switched from `INSUFFICIENT` to `CONTRADICT` under H for one SUPPORT source claim while binary source-label correctness stayed false for both. Matched R/H 8-pair binary correctness margins were zero despite 1/8 raw category changes for each operator. Hence coarse binary correctness can conceal substantive label movement; do not fold format loss, wrong answer, and witness grounding into a single unexplained error category. These are single-ecology, noninferential observations, **not** evidence of a causal decoder mechanism.

**Original near-neighbor literature secured and checked in Drive:** Hua et al. 2025 [PDF](https://drive.google.com/file/d/1kgdRModSJhJuL7JY6jeanltkUofSegkk/view); Lior et al. 2025 RELIABLEEVAL [PDF](https://drive.google.com/file/d/1oWRRfG3OZipkyAWOa0CPn1zgxnKxgIv1/view); Seleznyov et al. 2025 [PDF](https://drive.google.com/file/d/1brnjch0BDDnHT0OHrBlfekshh75AJEPZ/view). Rigid scoring artifacts, stochastic variation and broad prompt-format perturbation robustness are established rivals. P69 therefore remains **`PAPER_CONSTRUCT_HOLD`** until a preregistered larger externally-authored task-family design and independently adjudicated source/witness scorer can distinguish them. Neither old 68-call workflow nor SciFact hosted 32 calls should be rerun.

## New source-authored heldout task and independent scorer protocol (2026-10-10)

[`src/p69_external_holdout_scorer_handoff.py`](../src/p69_external_holdout_scorer_handoff.py) successfully selected 8 original SciFact dev claims (4 SUPPORT, 4 CONTRADICT) with 8 distinct original source documents, excluding all 4 previously used P70 source claims and documents; authentic dev/corpus SHA pinned. It compiled two differently ordered, masked, private task packets with original label and reference indices held only in custodian ledger. [Read-only CI #38044552352](https://github.com/WhoSia/EPISTEME/actions/runs/38044552352) PASS, [Drive counts-only receipt](https://drive.google.com/file/d/1j4psNjZi6xcS7Ob6gy6UE3wn8LDk1alc/view). This verifies holdout **source-case independence**, NOT eight independent ecologies or novel task-mechanism families. No human scoring has occurred: **0/16**, no provider outcomes on these cases, and no experiment to infer contractual effects. Independent scorers must review answer, evidence sufficiency, grounding and ambiguity without original labels/hosted responses, then retain disagreements. `P69_PAPER_CONSTRUCT_HOLD` remains.

