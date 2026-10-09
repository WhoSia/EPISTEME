# EPISTEME-P70 — Contract-Conditional Representation Effects: Adversarial Explanatory Rivals and Independent-Ecology Expansion Court

**Status:** `P70_THEORY_OPEN / R1_ORIGINAL_FORENSICS_PASS / ECOLOGY2_ORIGINAL_SOURCE_PASS / ECOLOGY2_PACKET_SEMANTICS_HOLD / CROSS_ECOLOGY_TRANSPORT_NOT_IDENTIFIED`.
**This is a P70 subprogram, not P71.** No new model calls, provider spend, paper promotion or repository bot commit.

## 1. Origin and observed, frozen record

The founding EPISTEME question asks when allegedly superior representations, standards or knowledge systems can replace an entrenched format. This project probes a bounded mechanism of *switching failure*: representation operators that preserve the task answer can still change whether a system recognizes, reports and substantiates counterexamples under a particular output interface. The goal is to explain **when switching-relevant gains travel beyond the original evaluation contract**; auditing mere formatted-JSON correctness is instrumental, not the explanandum.

**[Observed result: P69 R1, not a causal theorem]**
Source: real paid run [#37931512662](https://github.com/WhoSia/EPISTEME/actions/runs/37931512662) at frozen experiment code SHA `2363dc9b`, with actual 64 of 64 provider responses. This run's final judge was `P69_REPAIR_MEASUREMENT_HOLD`; the P69 manuscript remains `PAPER_CONSTRUCT_HOLD`. The historical R1 valid-semantic outcome counts, each of four per cell:

| Bundle | Prompt version | Strict schema positive | JSON-object positive | Strict null | JSON null |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash-Lite / Google | frozen_v0 | 2/4 | 0/4 | 4/4 | 4/4 |
| Gemini 3.5 Flash-Lite / Google | procedure_v1 | **0/4** | **4/4** | 4/4 | 3/4 |
| GPT-OSS-120B / Groq | frozen_v0 | 1/4 | 0/4 | 3/4 | 4/4 |
| GPT-OSS-120B / Groq | procedure_v1 | 4/4 | 4/4 | 3/4 | 4/4 |

**All eight Gemini procedure_v1 strict/JSON replies were format-valid.** The four positive failures under strict schema were scored `ANSWER_WRONG`, not `NONMINIMAL_OR_WRONG_WITNESS` or `FORMAT_UNOBSERVED`: provenance_0 failed both draws; transformation_0 failed both draws. Procedure_v1 JSON recovered both positive draws for each task, but lost one null draw. All 32 Gemini responses reported `gemini-3.5-flash-lite`. This *disfavors* a source-level model-ID swap and a pure formatting failure; it **cannot exclude hidden provider or reasoning changes, task-specific abstraction, or stochastic drift**.

Positive-response prompt-by-contract descriptive difference-in-differences for Gemini:

    (json_v1 - json_v0) - (strict_v1 - strict_v0)
      = (4/4 - 0/4) - (0/4 - 2/4) = 6/4 = 1.50.

The interaction exceeding one is arithmetically possible for a difference of two probability changes. With only two authored task clusters, two hosted draws per cell, and random invocation order but no shared random seed or full token traces, **1.50 is a finite-ledger descriptive contrast, not a generalizable effect, a p-value, or identified causal mediation**. Both provider contracts have the same task-prompt SHA within matched cell; they do not share the same response envelope.

## 2. Explanatory rival court and discriminators

The [machine-readable six-hypothesis receipt](../src/p70_r1_rival_court.py) is generated from the **exact original** Gemini+Groq artifacts (not copied historical scores) and archived separately. A claim can be falsified as a *sole explanation* without the mechanism it describes being absent.

| Hypothesis | Prospective discriminating signature | Historical status | What would refute it |
| --- | --- | --- | --- |
| H1 Schema-interface interaction | Equal prompt bytes but changed representation-dependent decision/abstention under different response schema | Descriptive contrast present, causal mechanism not identified | Held-out task clusters with matched schema controls and no channel-by-version response difference |
| H2 Global instruction-induced caution | Procedure length/explicit proof constraint increases abstention on positives **in both** channels, preserves nulls | **Inadequate as a contract-invariant explanation:** JSON positive rose to 4/4 | Opposite-channel positive recoveries on a larger held-out ecology |
| H3 One difficult task family | Schema-v1 failures concentrate in just provenance OR transformation | **Inadequate:** both strict positive task clusters failed 0/2 | Matched independently written topologies show same cross-task contrast |
| H4 Evaluator or format artifact | Apparent drop is due to invalid JSON or wrong witness-ID only | **Inadequate for measured Gemini strict positive rows:** all four are `ANSWER_WRONG` with valid format | Independent masked judges disagree with compiler oracle on the purported positive |
| H5 Stochastic/order/provider drift | Effect disappears or reverses under block-randomized repeats with full finish/token/version receipts | Unresolved; reported model ID unchanged, other hidden conditions not frozen | Stable preregistered replication with independently authored cases and diagnostics |
| H6 API schema semantics or hidden reasoning/token budget | Response-envelope effect remains when channel prompts are byte-identical but schema strictness, reasoning/length limits, or provider API decoding differ | Mechanism unobserved, fully OPEN | Carefully controlled equivalent-schema and token-budget intervention has no effect |

**Additional nonexclusive rival:** P69's generated task oracle might fail independent human adjudication. The machine's `ANSWER_WRONG` is an observation *relative to that oracle*, not evidence that a hosted model violated a human-validated causal truth. Prioritize independent ground-truth adjudication before costly scaling.

### Attacks *before* new paid requests

- Preserve both model families and both channels; do **not** remove Gemini strict after seeing the failure.
- Report always `provider_response`, `format_valid`, `answer_direction_correct`, `minimal_witness_correct`, `all_call_executable_correct`, and `null_false_positive`. Format selection and semantic scoring have different missingness.
- Freeze the meaning and processing of `NONE`, no silent repair from `predicted_direction=contradicts` to `different`.
- Do not use repeated invocations of the same generated packet as independent tasks.
- No H1/H6 internal mechanism claim is possible from existing score-only receipts; the old R1 artifact does not include raw text/decoding finish reasons or token-level traces.

## 3. Second ecology selected — AVeriTeC real-world web verification

**[Original source]** Schlichtkrull, Guo & Vlachos, *AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web*, NeurIPS 2023. Read the original arXiv preprint v3 PDF directly: https://arxiv.org/pdf/2305.13117 . Primary dataset: https://github.com/MichSchli/AVeriTeC ; licensed **CC-BY-NC-4.0**. The source authors report 4,568 real-world claims from 50 fact-checking organizations with question-answer evidence, provenance URLs, and justifications; the **development subset actually audited here has 500 records**. This is a different construction and evidence ecology from SciFact's synthetically generated scientific-abstract claims.

**Literature custody:** targeted canonical Drive index searches for `AVeriTeC`, `Schlichtkrull` and adjacent FEVER resources did not identify this exact paper: **Drive 미확보(색인 검색 기준)**. Direct original PDF verified above. Search absence is not universal absence.

**[Our new original-source implementation]** `src/p70_ecology_averitec.py` reads the actual author-owned `data/dev.json` from original GitHub commit `7c62d1ec8df3fb560d6efe2b85fa191135636f81`. The first hosted zero-call source audit [#37987405886](https://github.com/WhoSia/EPISTEME/actions/runs/37987405886) passed:
- Original bytes **1,785,475** and exact SHA-256 `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`; development records **500**.
- Four deterministically fingerprint-selected cases: **two original Supported and two Refuted**, each having two available cited QA atoms. The raw original claims, questions and answer texts are kept only on ephemeral CI runners, not published to the EPISTEME repository or CI artifacts.
- I, R (identifier renaming), H (QA row order inversion), RH: **16 purely structural candidate packets**. In each original claim, the question/answer/source-URL multiset is unchanged; evidence IDs differ for R.
- The original metadata has two or three available questions in these selected cases; only two are projected. **Crucial: original full-evidence labels are NOT packet-level oracle labels.** AVeriTeC QAs may refer to previous QAs, so reordering can change pragmatic dependency even if the multiset is unchanged. Both equivalence certificates and projected labels remain `HUMAN_HOLD`.

**Do not map** AVeriTeC `Conflicting Evidence/Cherrypicking` or `Not Enough Evidence` to SciFact `null`. Its `Supported`→`SUPPORT`, `Refuted`→`CONTRADICT` map is only a *tentative category bridge*, not a logical isomorphism. SciFact's exact minimal rationale sentences and AVeriTeC's grouped QA answers differ in inference grain, task provenance, and licensed data workflow.

## 4. Transportability hierarchy and scientific obligations

Distinguish these gates:

1. **Source independence `SOURCE_PASS`:** different original annotators and publication/data-generation lineages. Now checked for SciFact and AVeriTeC as source designs; independent random sampling is not implied.
2. **Evidence-preservation `STRUCTURAL_PASS`:** pairwise exact text and source citation multiset equality under R/H. Achieved in 16 constructed AVeriTeC packets, only *as structure*.
3. **Packet truth `SEMANTIC_HOLD`:** at least two genuinely independent masked annotators check each projected packet's label and admissible evidence witness; disagreements get an adjudicated record. **Cannot be inherited from original full QAs or reporting-source claim label.**
4. **Intervention bridge `BRIDGE_HOLD`:** show label-preserving transformation and dependency-graph commutation, separately for R and H. Do not treat H as safe when cross-question references are present.
5. **Behavior measurement `NOT_RUN`:** prospectively fix both provider+model bundles, response envelope, token budget, label mappings, counterbalanced invocation order and graded endpoints. No new API calls now.
6. **Conditional cross-ecology effect `NOT_IDENTIFIED`:** only after held-out mechanisms, appropriate task clusters and source-specific uncertainty accounting test P70-T1 against rivals. Four claims/ecology are calibration-only, not a population inference design.

The mechanism is best modeled as a **partial bridge** between evidence dependency/warrant graphs, not a total map between raw sentences and QA records. A projected label's truth is an *additional premise that needs inspection*, not a mathematical consequence of matching counts. If no common truth-preserving bridge exists, report `INCOMPARABLE_ECOLOGIES`, not `TRANSPORT_FAILURE`. Null abstention effects cannot be transported across datasets lacking a certified common null endpoint.

## 5. Prospective experiments and decisions — NOT authorized for model calls

**ECO2-P0 (done):** original data acquisition, exact SHA/bytes, balanced label source, 16 structurally paired packets; zero API calls. Output `SOURCE_PASS / STRUCTURAL_PASS / PACKET_TRUTH_HOLD`.

**ECO2-P1 (next, no provider calls):** independently adjudicate the *visible packet only* for four claims and all proposed variants, documenting QA dependency, original claim time/date, whether a two-QA projection truly suffices, and acceptable evidence citations; exclude no case post hoc on the basis of model response. If no adjudicator is available, explicitly retain `SEMANTIC_HOLD`, do not substitute the model as a gold rater.

**ECO2-P2 (after P1):** freeze mechanism strata *without using model correctness*: source citation count, linked vs independent QA dependencies, contradictory vs affirmative evidence, evidence temporal qualifiers, and provenance-role equality. For source-target alignment, produce a bridge construction or an explicit non-comparability proof per proposed stratum.

**ECO2-P3 (future experimental approval only):** pre-register matched I/R contrasts (H/RH only with human dependency certificate), paired answer-direction and evidence-ID outcomes for both bundles and strict/JSON channels; hold out *whole claim clusters and original source organizations* in a truly prospective test. Include baseline nonmechanism predictors, chance/randomization uncertainty, the contract-by-prompt rival set, and stopping rules. **No fixed large call budget is justified until packet and bridge gates pass.**

**Return to origin:** A defensible outcome predicts *when a representation migration is worth doing under changes of task ecology and output contract* and when the evidence required for such a claim does not exist. An outcome merely showing that a new JSON format parses correctly fails the founding EPISTEME explanandum.

## 6. Files, receipts, and authority

- Native full R1 forensic analysis: `src/p70_r1_rival_court.py`
- Independent AVeriTeC source audit: `src/p70_ecology_averitec.py`
- Read-only independent data/rival CI: `.github/workflows/p70_rival_ecology.yml`
- Historic immutable Gemini/Groq R1 actual shards and judge verdict remain archived in the user's existing EPISTEME Drive folder, and in paid GitHub run #37931512662.
- **Authority ledger:** `ORIGINAL_DATA != PACKET_TRUTH`; `MATCHED_EVIDENCE_MULTISET != ORDER-SEMANTIC_INVARIANCE`; `OUTPUT_CONTRACT_INTERACTION != CAUSALLY_IDENTIFIED_DECODING_MECHANISM`; `ONE_ECOLOGY_MODEL_EVIDENCE != TRANSPORT`; `CI_PASS != P69_SCIENCE_PASS`.
