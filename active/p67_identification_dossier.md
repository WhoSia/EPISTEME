# P67 — Selective-Observability Identification Dossier (Post-P66 Source Court)

**Status:** zero-call historical audit CERTIFIED; 384-call paired-channel pilot PRECOMMITTED but NOT executed. This document does not amend P66's frozen TECHNICAL_HOLD.

## 1. Factual source census
- Hosted P66 run `37712504043`, twelve primary shard ZIPs, 12,288 unique (task, draw, cell_index) identities.
- 11,453 received and parsed structured outputs, 835 provider-level technical failures.
- 827/835 technical errors expose `failed_generation: 'NONE'`; seven more include a different `json_validate_failed` fragment; one is a separate schema-validation error. The P66 worker truncated exception text to 250 chars, so the seven partially observed fragments should not be over-interpreted.
- In the original P42 strict schema, the expected abstention must be an object (with `challenge`, `intervention`, `predicted_direction`, `rationale_ids`). A bare token `NONE` is not a valid response under that contract. Such failures are neither known-correct nor known-wrong *semantic answers*.
- The historical P66 code passed a nominal seed into `p44_field.call`, but its Groq `groq_raw` path never sent a provider seed. Original "draw" labels denote invocation replicates, not controlled server-seeded samples.

## 2. Exact finite-ledger missing-data audit
For each task×draw×vertex, a matched valid/null twin has joint correctness `J=Y_valid AND Y_null`. Set `J=1` if both twins are known correct; set `J=0` if any known twin is wrong; otherwise `J∈{0,1}`. No missing-at-random assumption or imputation.

| Binding/location group | certain joint successes | maximal joint successes | denominator |
|---|---:|---:|---:|
| BH (target-linked/history) | 0 | 256 | 1536 |
| BT (target-linked/terminal) | 1361 | 1472 | 1536 |
| DH (decoy-linked/history) | 1379 | 1536 | 1536 |
| DT (decoy-linked/terminal) | 1369 | 1536 | 1536 |

Therefore, **BT − BH belongs to [1105/1536, 1472/1536] = [0.719401..., 0.958333...]**, irrespective of how all 835 unknown semantic outcomes are completed. BH has **zero observed correct valid answers**, despite 1,280 valid responses technically scored in BH. That is an observed semantic-oracle mismatch in addition to formatting errors.

**Meaning:** Missing technical answers alone cannot explain P66's BH-vs-BT outcome disparity. This is a deterministic partial-identification statement, **not** a significant causal estimate, and does not certify the P66 permutation court. Output-contract censoring is real but not a sufficient explanation of the entire BH failure pattern.

## 3. Statistical/causal object
Let `X` denote the archival task and matched packet; `C` the randomized output channel; `S(C)` the event that the channel yields a format-valid response; and `Y(C)` semantic correctness for the generated answer **if that answer is observable**. Define executable criticism `O(C) = S(C)·Y(C)`. Compare `E[O(C_1)−O(C_0)]` on the same packet distribution, without assuming that the latent answer `Y(C)` is channel-invariant.

For an arm with `N` calls, `K` known semantically correct outputs and `M` unobserved or invalid outputs, semantic correctness in the full attempted-call population belongs to `[K/N,(K+M)/N]`. Validity and executable correctness are directly observable all-call process outcomes and need no imputation.

**Important:** A total executable-success treatment effect is causally attributable to the randomized channel policy, not automatically to either decoding alone or "unchanged hidden reasoning." The strict-schema/json-object arms receive **byte-identical prompt text** and differ in provider `response_format`; plain-text arm changes the response envelope instruction too and is a **compound channel+instruction treatment**.

## 4. Prospective pilot contract
- `src/p67_channels.py`: three output-channel treatments, semantic parser and invariant packet SHA.
- `src/p67_pilot_worker.py`: 4 tasks BH1/BT1/DH1/DT1 × 8 balanced operator vertices × 2 semantic twins × 2 invocation repeats × 3 channels = **384 model calls maximum**, SDK retries 0, raw response and error preserved, provider seed not claimed.
- `src/p67_pilot_analyze.py`: checks all 384 identities, each matched packet hash across three channels and descriptive validity/semantics.
- `active/p67_pilot_manifest.json`: frozen pilot allocation, thresholds and interpretation ceiling.
- `.github/workflows/p67_pilot.yml`: push-triggered zero-call preflight; **model calls only on explicit manual workflow_dispatch**. Contents and actions permissions are read-only; no GitHub Actions bot commits.
- The pilot is a **feasibility/construct check**, not evidence for a new general causal mechanism. No post-hoc positive-effect p-value will be promoted from it.

## 5. Fatal literature rivals and paper gate
- [JSONSchemaBench (Geng et al., 2025)](https://arxiv.org/abs/2501.10868) benchmarks constrained output validity, coverage, and quality.
- [The Constraint Tax (Ray, 2026)](https://arxiv.org/abs/2605.26128) already demonstrates schema validity vs semantic/executable correctness tradeoffs in fixed-instance experiments.
- Selective labels, performative prediction and partial identification are foundational prior art. Generic output constraints, MNAR, or differential format failures are not EPISTEME discoveries.

For a publishable **EPISTEME** advance rather than engineering replication, a successor must demonstrate that **changing an epistemic output/retention interface can reopen independently verifiable, non-redundant falsification routes** in held-out challenge grammars and with independently evaluated criticism transfer. Failure of that comparator means classify the P67 family as useful instrumentation, not promotion of Self-Validating Epistemic Compression.

## 6. Governance
Never convert a provider `json_validate_failed` into a silent semantic wrong answer. Never rewrite P66's frozen verdict. Never submit repository commits as `github-actions[bot]`. GitHub Actions is computation/artifact-only.
