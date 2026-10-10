# Exploratory Paper A1 — When the Output Contract Changes the Verdict: Measurement Validity in Evidence-Grounded LLM Evaluation

**Genre:** exploratory methods / negative-result workshop paper draft; not a completed full-length manuscript or confirmatory empirical study. **Status:** `DRAFT_OPEN / INDEPENDENT_ORACLE_HOLD / EXTERNAL_VALIDATION_HOLD`. This text records historical evidence and *falsifiable* claims, not publishable certainty.

## Abstract (draft)

Evaluating whether language models recognize a valid evidence-grounded counterexample requires more than parsing a formatted answer. In many benchmark pipelines, the output interface both constrains the response and determines which responses the scorer can inspect. We examine this boundary using a frozen scientific-evidence reasoning instrument, paired response contracts and two hosted model–provider bundles. An initial 192-call instrument pilot collected a response for every request but failed its predeclared technical measurement gates: one provider's JSON-object response format was valid in only 34 of 48 requests, while the other provider produced no strictly grounded correct answers on the valid-semantic cases of the JSON-object arm. A separately versioned, bounded 64-call calibration compared the frozen original prompt with a procedure-guided prompt across two authored task families, two semantic classes, two response contracts and two draws per cell. In the Gemini bundle, the guided prompt produced **0/4** strictly grounded positive cases under strict-schema output and **4/4** under JSON-object output, even though both guided-format arms were **8/8 schema-valid**. The corresponding original-prompt positive counts were **2/4** and **0/4**, yielding a descriptive prompt-by-contract difference of changes of **6/4**. On the same small calibration, both Groq improved-format arms satisfied the predeclared measurement signal gate. The overall R1 gate nevertheless failed because one Gemini strict-schema arm lost positive evidence discrimination.

These results provide an empirical **warning about measurement-contract sensitivity**, not an identified model-internal mechanism or a population effect. The task set contains only two authored task families with two invocations per cell, and the frozen source-level oracle has not been independently adjudicated by humans. We distinguish provider nonresponse, structural format validity, answer-direction errors, inclusion-minimal warrant errors and correctness conditional on format, retaining the historical failure artifacts and all adverse cases. We derive an exact arithmetic decomposition of all-call executable correctness into format selection and conditional correctness and identify its limitations as a noncausal identity. Finally, we propose a prospective falsification design using independently authored held-out evidence ecologies, blinded packet-level annotation, identical prompt hashes within contract comparisons and prespecified call-block controls. Our contribution is to specify conditions under which an apparent gain from a representation or prompting procedure can be a property of the **measurement interface** rather than reliable transferable epistemic competence.

## 1. Construct and explicit estimand

**[Target construct]** Whether the model correctly recognizes and substantiates an *admissible* evidence-grounded counterexample in a packet whose semantics and minimal proof/witness sets have independently certified ground truth.

**[Observable instrument endpoint]** `X=1` iff the provider responds, the returned object satisfies the frozen schema, its answer direction is correct relative to the frozen local oracle, and its cited evidence belongs to one inclusion-minimal justified proof set. Report provider responses, schema compliance, correctness conditional on schema compliance and full-call `X` separately.

**[Do not conflate]** An all-call endpoint is not a direct measurement of latent model reasoning when malformed output content is unobserved. Postselecting only valid JSON changes the estimand and may be a collider/selection effect; identifying mediation requires more than an arithmetic decomposition.

Let `f=P(format_valid)`, `q=P(strictly_correct|format_valid)`, `x=fq`. For arms A and B, `x_A-x_B=(f_A-f_B)q_B+f_A(q_A-q_B)`. This is an **exact descriptive identity**, not the isolated causal effect of syntax constraints. A hypothetical completion of non-format-valid outputs is a sensitivity interval, not direct latent semantic truth.

## 2. Frozen design and actual observations

| Study | Source | Hosted calls | Prior gate | Outcome |
|---|---|---:|---|---|
| P69 initial instrument | internally authored evidence packets | 192 provider responses | Predefined channel format/signal criteria | `TECHNICAL_PILOT_HOLD` |
| P69-R1 contract repair | same two authored canary task classes | 4 actual fresh prior-canary + 64 paired calibration | Four improved model–contract arms require provider 8/8, format ≥7/8, positive and null grounded signals | `REPAIR_MEASUREMENT_HOLD` |
| P70 original SciFact | four original independently authored scientific claims, one ecology | 32 provider responses | source version & exact schema gates | `PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE`; source-label agreement Groq 16/16, Gemini 8/16; no multiecology transport |

**P69-R1 positive-valid grounded count, out of 4 in each cell:**

| Model/provider bundle | Frozen prompt strict | Frozen prompt JSON | Guided prompt strict | Guided prompt JSON |
|---|---:|---:|---:|---:|
| Gemini 3.5 Flash-Lite / Google | 2 | 0 | 0 | 4 |
| GPT-OSS-120B / Groq | 1 | 0 | 4 | 4 |

No multiple-comparison-corrected p-values are appropriate for these tiny *historical, exploratory* task allocations. The observed Gemini difference-in-differences `(4−0−(0−2))/4=1.5` is a contrast of risk differences, not a 150% relative gain. A negative R1 technical gate is not a negative proof of the corresponding scientific hypothesis in all tasks.

## 3. Registered rival explanations

H1 contract/procedure interaction; H2 globally increased conservatism; H3 single task-family difficulty; H4 scorer/format artifact; H5 random order, decoding, historical provider changes; H6 internal schema-guided generation or reasoning-budget interactions. The historical Gemini strict positive failures were classified `ANSWER_WRONG`, not merely malformed JSON. H2–H4 are insufficient as **sole** descriptions for these four rows; H1/H5/H6 internal causal attribution remains untested. Treat H1 as a hypothesis, not a revealed decoder property.

## 4. Forward falsification before submission

1. **Independent ground truth first:** each original generated packet and projected external source evidence receives two separately submitted blinded human judgments. Resolve disagreements without altering original votes or silently imposing the historical compiler gold. Preserve genuine `AMBIGUOUS` and `INSUFFICIENT` rather than manufacturing a required binary label.
2. **Held-out independent items:** sample substantially more independent evidence/claim structures, with distinct authoring and source organizations. Balance genuine positive and insufficient/negative classes, and freeze inference units at source claim clusters or independent organizational units.
3. **Contract experiment:** compare genuinely matched response contracts while controlling prompt bytes, model version, schema vocabulary, decoding temperature and token cap; randomize invocation order in blocks, capture provider finish reasons and version data. Hold an orthogonal answer-direction endpoint that is robust to syntactic encoding and compare it to strict-scoring selection.
4. **Audited analysis:** preregister primary and secondary endpoints, an uncertainty interval clustered at original claims (not at repeated draws), a multiplicity plan, outcome missingness sensitivity, a task-family held-out check and a stop/no-promote criterion.
5. **Paper decision:** if the contrast vanishes under independent human scoring or held-out ecologies, publish a reproducible negative methods result or discontinue the broad version. If it persists, still avoid model-internal causal diagnosis without controlled schema/decoding intervention.

## 5. Closest validated source rivals and scope

- Baan et al. (2022), *Stop Measuring Calibration When Humans Disagree*: original [Drive PDF](https://drive.google.com/file/d/1almvYH7czW2Db-uDvspOZTxAFBSWSCYu/view). Disagreement-aware human labels and invalid majority-gold assumptions; not our proposed novelty.
- Mani, Liang & Lipton (2024), *Fast Evidence Extraction for Grounded Language Model Outputs*: original [Drive PDF](https://drive.google.com/file/d/1yU-Pqxkg5PFvvU7ZYqbXu-Y0yxdUFhqx/view). Evidence retrieval vs verification cost; may be a useful review-workflow baseline.
- Angelopoulos et al. (2025), *Learn Then Test*: original [Drive PDF](https://drive.google.com/file/d/1OC0CSHbj6DeFNeNiop81QDUHc9pduzTy/view). Actual risk guarantees require justified calibration methodology, not chosen sensitivity parameters.
- P69 frozen and recovered source artifacts: [192-call actual run](https://github.com/WhoSia/EPISTEME/actions/runs/37925719478); [64-call actual R1 run](https://github.com/WhoSia/EPISTEME/actions/runs/37931512662); [original evidence-bounded closeout](p69_p70_scoped_closure_court.md).

**Authorial boundary:** This is a real extended abstract backed by actually executed small pilots and source receipts; it is **not** peer-reviewed and does not establish that the observed phenomenon will generalize. The eventual paper should include all failed and nonvalid arms, not only positive-looking contrasts.
