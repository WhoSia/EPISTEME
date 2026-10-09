# EPISTEME-P70 — Independently Annotated Scientific-Evidence Representation Pilot

**Status:** `EXTERNAL_SOURCE_AUDIT_PASS / OFFLINE_FULL_GRID_PASS / PAID_HOSTED_STUDY_NOT_YET_DISPATCHED`.
Part of [P70 formal theory](p70_theory_program.md), separate from P69 calibration and the P69 proposed manuscript.

## Hypothesis (prospective, not observed)
Across four **original SciFact development claims** chosen from an external scientific fact-verification corpus (not synthetic P69 task factory), renaming evidence identifiers R and reordering evidence presentation H leave the original research claim and evidence sentences unchanged. Does this preserve hosted models' classification and reference-to-evidence behavior?

The study is *independent in corpus origin and annotation*, not independent in research infrastructure, and comprises **one ecology**, four claim clusters, two provider/model bundles. It cannot confirm an ecological transport law. Four claim clusters are inadequate for strong mechanistic inference. Any result is a descriptive pilot and possible falsifier of simplistic operator effects.

## Provenance and evidence scope
- Original source: [SciFact original source repository](https://github.com/allenai/scifact) and its published archive `https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz`.
- Read original `claims_dev.jsonl`/ `corpus.jsonl` directly in ephemeral GitHub runner; do not mirror source text or private gold labels to repository.
- Use exactly two eligible `SUPPORT` and two `CONTRADICT` externally annotated claims, selected by stable SHA-256 ordering of source claim IDs after basic validity checks, not by hosted results. There must be exactly one annotation label per candidate and an authentic rationale text. Add one same-document non-annotated sentence to make row order manipulation meaningful; this extra sentence is **not** assumed to establish null semantics.
- Reuse the original annotated rationale sentences verbatim. Every candidate has an attested positive label in the source annotation. These packet projections do **not** inherit a formally certified minimal proof or an independent human annotation of the specific subset; scored label agreement is agreement with the original source label, not proven packet-level truth.
- The same source original text/evidence multiset is compared within case over `I,R,H,RH`. The R operator renames evidence ID handles; H reverses row presentation. Both preserve visible sentence multiset and original source annotation, subject to an explicit SHA check.
- **No semantic-null twins and no artificial negative-case imputation.** This is a stronger external-source fidelity standard than relabeling missing rationale as `NONE`.

## Frozen 32-call design
2 model+provider bundles × 4 externally annotated claim clusters × 4 R/H representation vertices × 1 structured response contract × 1 invocation per cell = **32 maximum new calls**.

Bundled response schema requires exactly `verdict: SUPPORT|CONTRADICT|INSUFFICIENT` and `evidence_ids: [string]`. The visible prompts contain no original gold annotation labels. Gemini uses JSON MIME + supported strict schema, Groq uses strict schema. Within-provider output contracts are not identical decoding interventions; compare paired R/H contrasts **within a bundle**, not pure model effects.

Report separate:
- provider response existence; format validity; original annotated-label match;
- evidence ID legitimacy/uniqueness and whether an original annotated rationale ID was cited;
- all-call executable-correctness matched R and H differences, derived from pairs within the same original claim; failures never overwrite latent semantic quality.

A single source has no cross-ecology effect or transported effect estimand. Do not claim a p-value from 32 calls; four claim IDs are the relevant source clusters.

## Measurement gate
- Each bundle: 16/16 provider responses, at least 14/16 schema-valid cases.
- At least one matched original annotation from each label class. Otherwise mark `NONSELECTIVE_EXTERNAL_HOLD`.
- All source/evidence hashes, claim/vertex grids, and annotation distributions must match exactly between bundles. Any mismatch is a hard analysis error.
- Passing returns only `PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE`, **not** P70 scientific closure.
- The authoring and scoring program cannot validate itself as a fully independent human adjudicator. Packet-level entailment and original annotation consistency remain separate authorities.

## Runtime and costs
- Provider-free push: original SciFact archive fetched and decoded in temporary Action runner, 4 claims × 4 vertices × 2 models synthetically generated using a mock oracle with **zero actual provider calls**; full source/digest and pair checks.
- Hosted manual dispatch: workflow `p70_external_source.yml` input exact `RUN_32_CALLS`; read-only permissions, no bot-authored commits, no SDK retries or substitute models; scored artifacts contain SHA digests and result enums, not raw SciFact or model response text.
- No hosted calls without explicit human UI dispatch; provider token charges may apply. Do not run the 8192-call P69 planned full study through this pilot.

## What would turn this into real cross-ecology identification?
First reproduce the labeling/abstention contract with an **independently sourced second ecology** (e.g., claim verification from a non-SciFact publisher/dataset) and a separately audited, comparable task definition. Then freeze a cross-ecology `phi` mechanism mapping and held-out task-family predictions *before* hosted response measurement, with independent blinded answer/rationale adjudication. If no oracle-preserving bridge can be established, stop and report `BRIDGE_HOLD` instead of recoding the disagreement as model failure.

## Actual 2026-10-09 hosted 32-call run, recovered without new calls

Historical paid [run #37929439637](https://github.com/WhoSia/EPISTEME/actions/runs/37929439637) used the exact original SciFact source and completed **32/32 provider replies**, but the Actions run FAILED at aggregation because `receipts/` also contained two `OFFLINE_FIXTURE` files. The old aggregate counted four bundles rather than the two actual `ACTUAL_PROVIDER` bundles. This is an **analysis source-mode isolation bug**, not an indication of hosted model failure. The source artifacts remain immutable.

Fixed analyzer: ignore offline fixtures for data selection but require two independently checked ACTUAL_PROVIDER bundle records; self-test now mixes synthetic and real fixture receipts to regress the failure. Run [#37930648628](https://github.com/WhoSia/EPISTEME/actions/runs/37930648628) recovered **`PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE`** with **ZERO additional paid provider calls**. [Recovered verdict Drive archive](https://drive.google.com/file/d/1age6Jwd8yge-JqpVt3LOiffJNCJMn95a/view); [32 original scored model receipts Drive archive](https://drive.google.com/file/d/1AEW5lOxTJpf4genoxkAC7w-bKfA1dIRZ/view).

Actual 4 source claim clusters × I/R/H/RH × two model/provider bundles:
- Groq GPT-OSS-120B: provider response 16/16, exact format 16/16, original annotation label agreement 16/16, annotated rationale cited 16/16. Matched R difference 0/8; matched H difference 0/8.
- Google Gemini 3.5 Flash-Lite: provider response 16/16, exact format 16/16, original annotation label agreement 8/16, annotated rationale cited 12/16. Source-label agreement 4/8 SUPPORT, 4/8 CONTRADICT. Matched R difference 0/8; matched H difference 0/8.
- **Causal authority ceiling:** these are descriptive contrasts with one hosted draw per representation and FOUR independent claim clusters from ONE external source ecology. A zero observed contrast does not prove invariance or transported representation effects, and correct source-label matches do not supersede independent packet-specific semantic annotation. Model+provider differences cannot be attributed solely to model architecture.
- Original source dev SHA256 `86f0435d08fdb65d1aa41d1472684f57e6e71930626497bdf4d7a9ec1a632217`; corpus SHA256 `b8d6c89624cb2ed74dee8938effc4f5d8bd2086887880af8110d64be4ceade62`. No empirical result may override the original source data and packet projections.

**Final scoped status:** `P70_EXTERNAL_SINGLE_ECOLOGY_PILOT_MEASURABLE / TRANSPORT_THEORY_NOT_VALIDATED / P70_RESEARCH_OPEN`. Never rerun the paid 32 calls to fix a previous offline-mixing bug.
