# P64 — Outcome-Blind Technical Failure Localization

Canonical P63 run: 37563565663; head: 7c86f0daa879c9f65e76afee75eab099f64082b5.
Final result artifact ID: 11471953755; artifact ZIP SHA-256: 3124c5c50693e3fafd7862ca06a1a9d26d05cc7c673a44e523ae9b8956fe2f87.

P63: 48,849 / 49,152 technically OK, 303 technical failures, original verdict TECHNICAL_HOLD.

Every failure: BadRequestError / json_validate_failed. No P63 scientific effect is established.

**Corrected 2x2 structural distribution:**
- History-externalized: **2 / 24,576 = 0.00814%**.
- Terminal-embedded: **301 / 24,576 = 1.22477%**.
- Record framing: 111 / 24,576 = 0.45166%.
- State framing: 192 / 24,576 = 0.78125%.
- Valid semantic: 302 / 24,576.
- Null semantic: 1 / 24,576.

Task failures: RH1 2, RH2 0, RH3 0, RT1 30, RT2 45, RT3 34, SH1 0, SH2 0, SH3 0, ST1 53, ST2 70, ST3 69. Draw blocks A 140, B 163. Exact unique failed identities: 303/303.

**Important correction:** An early chat estimate mistakenly said terminal 302 / history 1; the source-derived count is terminal 301 / history 2. 302 valid / 1 null is separate and correct.

**Explanandum separation:** The extreme conditional concentration is directly observed at the structured-output contract level. It is NOT causal identification of underlying inference behavior. A provider schema error cannot be counted as a scientific incorrect answer.

## Frozen staged court

1. Zero-call localization with proper denominators (this record).
2. Exactly one replay attempt for each of 303 failed P63 identities, and no replay for the 48,849 successes. Same P63 model, provider, packet, output schema, response parsing, vertex, alias, semantic, draw/seed contract.
3. Unchanged P63 scientific adjudicator iff 49,152/49,152 technically complete.
4. Otherwise: separate, sound partial-identification bounds on all admissible missing valid/null outcomes; no missingness probability or imputation model. Exhaustive enumeration only if tractable. A mathematical branch-invariance result is distinct from the original P63 full-completion gate.

## Prior art / literature harvest

- Manski (2005), *Partial identification with missing data: concepts and findings*, DOI 10.1016/j.ijar.2004.10.006: general missing-data identification regions and bounds are prior art.
- Liu et al. (2024), *Lost in the Middle: How Language Models Use Long Contexts*, DOI 10.1162/tacl_a_00638: relevant information location sensitivity is prior art.
- Geng et al. (2025), *Generating Structured Outputs from Language Models: Benchmark and Studies*, arXiv:2501.10868: constrained decoding / schema adherence is prior art.

**Novelty ceiling:** an experimentally predeclared evidence-location intervention interacting with structured-output evaluability, whose scientific operator-sign conclusion must be recovery- or completion-robust; NOT a discovery of missing-data bounds, JSON failures, or position sensitivity.
