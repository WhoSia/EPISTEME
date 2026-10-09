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
