# EPISTEME W6 — Meaning-Preserving Discourse Crossovers: Candidate Court and Blinded Reader Protocol

2026-10-20 KST. **Constructed packets and internal semantic prescreen only. No independent semantic judges or reader observations.** P76 OPEN; P77 HOLD; PAPER HOLD.

## Key repair from W5
An anaphoric edit with an ambiguous demonstrative under one context must be excluded, not counted as a negative preference outcome. This can produce apparent context reversal entirely by **semantic eligibility selection**. W6 therefore isolates an operation more likely to preserve propositional and discourse content: replace one **unambiguous second-mention full noun phrase** by *the same* unambiguous shorter noun phrase (not 'this/that' when contrast introduces ambiguity). Exact referents remain visible.

Frozen E1' rule: on the second mention only, replace 'the archived calibration ledger' with 'the ledger' if exactly one ledger is introduced and no alternative ledger or semantic role becomes available. If the participant needs to choose between archives or calibration sources, the operation is not eligible. Do not reword it to rescue a failed cell. A claimed reversal must use the same eligible operation in both contexts.

## Prototype packets: identical target propositions; contexts changed
A1: Target O 'The archived calibration ledger lists the original correction coefficients.' Target E 'The ledger lists the original correction coefficients.'
Context GIVEN: 'The archived calibration ledger has been digitized. The technician verified the scan.' Semantic prescreen LIKELY PASS.
Context EVIDENCE-SOURCE: 'The committee asks which document, not which person, supplies the coefficients. Only one ledger is available: the archived calibration ledger.' Semantic prescreen LIKELY PASS, but discourse focus on full source name may disfavor abbreviation. **That effect is hypothesized, not observed.** Note that 'the ledger' still unambiguously denotes same source.
Control: ask exact antecedent, provenance and whether coefficients have been independently calibrated; neither target asserts independent calibration.

B1: Target O 'The detector-conditions database records the run-dependent correction.' Target E 'The database records the run-dependent correction.'
Context GIVEN: 'The detector-conditions database was restored on Tuesday. Its contents are being audited.' Provisional LIKELY PASS.
Context CORRECTION: 'A colleague claims that a printed laboratory notebook records the run-dependent correction. The reply must identify the actual source; the detector-conditions database is the only database in the case.' Provisional LIKELY PASS. A shorter phrase could be less informative under correction QUD but is not itself ambiguous.
Control: don't frame the print notebook as a second database.

C1: Target O 'The published luminosity table supplies the normalization values.' Target E 'The table supplies the normalization values.'
Context GIVEN: 'The published luminosity table is the reference. The analyst has consulted it.' Provisional LIKELY PASS.
Context SOURCE-CHALLENGE: 'A critic asks whether the analyst back-calculated normalization from selected event counts instead of using the published luminosity table. Only one table has been mentioned.' Provisional LIKELY PASS, but “the table” can still be enough: genuine sign reversal is not guaranteed.
Control: test whether readers accurately identify published vs derived normalization.

D1 reject: Target O 'The ALEPH archive contains an uncertainty model.' E 'The archive contains an uncertainty model.' Context 'Compare ALEPH and DELPHI archives.' Semantic FAIL if the context does not disambiguate the singular referent. D1 cannot appear as a negative arm in the primary analysis.

E1 reject: O 'The archived evidence may support a partial replay.' E 'The archived evidence supports a replay.' Modal strengthening; FAIL.

## Two-step review, hard gate
Gate 0 algorithmic audit of exact target variants and their differential tokens, context consistency, numerical and epistemic modal preservation. Gate 1 two independent human semantic assessors, blinded to any predicted gain, judge referents, truth-conditions, QUD, contrasts, presuppositions, provenance, practical entailments; PASS requires agreement; disagreements adjudicated without seeing reader outcomes. Current A1–C1 are NOT Gate 1 certified.
Report complete candidate denominator and PASS/FAIL/UNCERTAIN by context; primary reader contrast on **paired-pass** items only, and provide bounded sensitivity analysis for selection effects. A complete semantic-gate FAIL under one context invalidates interpreting its low preference as an interaction effect.

## Reader trial, not run
2×2 design per packet: same target original/edited crossed with GIVEN versus SOURCE-CHALLENGE (counterbalanced between subjects). Outcomes: correct identification of evidential provenance; false endorsement that the records alone guarantee precision replay (negative inference probe); clarity/preference only secondary. Freeze source answers before exposure. Primary effect Δ_c = P(correct|edited,c)-P(correct|original,c), and difference-in-differences δ=Δ_sourcechallenge−Δ_given. A reversal requires opposite signed contextual effects with confidence/credible intervals excluding effects indistinguishable from zero, corrected for items/hypotheses. A significant interaction alone does not establish a strict sign reversal. Reader presentation must not include answers in the prompts; avoid knowledge testing without necessary materials. Pilot determines realistic power.

## Direction audit
Levels A meaning retention; B reader interpretation; C accurate scientific criticism; D historical adoption-induced change of future experimental test set. A↛B↛C↛D. This work is an auxiliary study about communication of scientific epistemic status and belongs in a Writing Loop appendix; it MUST NOT replace primary P76 archaeological HDF4 original acquisition, ALEPH external-run artifact/covariance, or JADE causal luminosity evidence. Language research about givenness/focus is strong prior art. P77 cannot be opened on crossover alone.

## Next
Obtain Gate 1 reviewer pair and external readers, separately reproduce external ALEPH result JSON and inspect uncertainty-propagation code, retain strict claims/limits for Paper 1 & 3. No synthetic reader data, no promoted novelty, no claim of measured reversal.
