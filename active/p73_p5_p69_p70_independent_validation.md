# EPISTEME P73-P5 × P69 × P70 — Prospective Source-Time Audit, Independent Scorer and Full-Evidence Comparison Court

**Date:** 2026-10-10 KST.
**Executed gate:** [G-001 read-only CI #38044552352](https://github.com/WhoSia/EPISTEME/actions/runs/38044552352), **SUCCESS, three distinct jobs**. Original failed runs 38044394639, 38044439184 and workflow-YAML errors were retained in immutable GitHub history and fixed without replacing results. **All successful claims below concern design/instrument preparation only; none is a real human study or a causal field audit.**

## A. P73-P5 — External authority, historical exposure and observational noninterference

**Starting problem:** repeated reads of a *pinned Git revision* in P73-P4 showed stable source bytes, not evidence that a public audit had no influence on a mutable real source, its gatekeepers or its proof role.

**Three distinct state changes:** (1) independent source publication or revocation over ordinary calendar time, (2) an externally visible announcement that an audit is planned, and (3) the audit's actual evidence-acquisition and interrogation operations. A study should not call (2) an audit-result disclosure nor silently merge (1), (2), (3).

**Prospective two-arm panel contract:** At least two source units per planned `audit_notice` and `control` arm, with source- and site-specific baseline snapshots before and after a predeclared announcement event. Field implementation MUST preregister source-level allocation, consent/legal/ethics status, immutable version and per-page capture hash, independent collector identifiers, explicit source-authority effective times, original source update times, underlying referent and proof role, source-organization clustering and spillover network. Don't choose a mutable target by contacting or publicly exposing it without authorization.

**Runnable proof-of-concept** [`src/p73_p5_prospective_audit_design.py`](../src/p73_p5_prospective_audit_design.py) checks: no exposure before specified announcement date; no future-dated source publication/authority; no incomplete panel wave; no changing role/authorization silently attributed to audit; separate snapshot collectors; no accepted unreviewed field plan. Under an entirely **synthetic** 4-source × 2-time panel, arithmetic difference-in-differences is 1 unit. This is a program test **NOT a result from any actual institution**. The true confidence interval remains unknown.

```text
Observed difference-in-differences
  = audit-notice effect
  + untreated counterfactual trend imbalance
  + unmeasured spillovers
  + source-role/authority measurement effects.
```

With only two panel waves, parallel trends cannot be established; the test explicitly outputs `HOLD_FIELD_STUDY_NOT_CONDUCTED`. A future scientifically useful design needs multiple **pre-announcement** observation times and a held-out no-exposure negative-control endpoint to interrogate trend assumptions, plus interference-aware allocation and publication policy. External source-page authority/epoch cannot be replaced by a boolean `attested=True` in the toy fixture. Separate original warrant validity `Q(s_0)` from post-audit validity `Q(s_1)`.

**Formal current status:** `P73_P5_PROSPECTIVE_PANEL_DESIGN_TEST_PASS / FIELD_NONINTERFERENCE_NOT_IDENTIFIED / EXTERNAL_SOURCE_TIME_ROLE_CERT_HOLD`. No public announcements or source-target interventions actually made, no participants recruited.

## B. P69 — Real external holdout cases and independent human scorer validity

The original P69 192-call + R1 64-call evidence remains unchanged. See [P73-P4/P69/P70 original artifact report](p73_p4_p69_p70_joint_research_court.md). The Gemini valid-format strict 0/4 versus JSON 4/4 positive split is real but two authored task clusters cannot support general effect claims. Further, exact automatic witness-set matching is not an independent packet-level semantic adjudication.

**New executable** [`src/p69_external_holdout_scorer_handoff.py`](../src/p69_external_holdout_scorer_handoff.py) reads the authentic exact-hash SciFact dev/corpus in a no-provider CI job and selects **eight original annotated claim clusters plus eight distinct original document IDs**, four source SUPPORT and four CONTRADICT. Selection excludes the **four original P70 claims and four original P70 source documents** to avoid overt test overlap; uses stable SHA-based selection and independently source-annotated rationales with one same-document decoy. Gold labels and source indices remain **sealed**, not visible to reviewers. Two independently assigned, differently ordered private review packs and empty answer forms are compiled, checked, and deleted from the Actions runner before artifacts upload. Public receipt records source hashes, counts and HOLDs only.

**Independence qualifications:** Those eight claims have distinct source claim and document IDs but all derive from *one SciFact dataset ecology*. Neither distinct organizational annotation nor eight distinct mechanism families is established. They are independent of the authors' synthetic P69 task factory in original claim authorship, **not** a new ecosystem relative to P70. No inference based on 8 as an adequate population sample.

**Independent scorer protocol:** Two different blinded raters (not collected) must each submit 8 complete answers, including category, evidence IDs required to justify verdict, answer sufficiency flag, ambiguity and independently reasoned justification. The code rejects duplicate reviewers, missing rows, wrong packet hashes and invented evidence IDs. Any final scorer must also distinguish error in answer direction from correct answer with incomplete evidence; source-label agreement is a preliminary reference only, never independent proof truth. A third-party adjudicator handles disagreements without erasing disagreement distribution. The current acceptance path for synthetic reviewer fixtures is **not actual human participation**.

**Gate:** `8_SOURCE_CLAIMS / 8_DISTINCT_SOURCE_DOCUMENTS / P70_OVERLAP_0 / BLINDED_SCORER_READINESS_PASS / REAL_REVIEW_0_OF_16 / PAPER_CONSTRUCT_HOLD`. No model has been evaluated on those eight holdout tasks and no new paid call authorized.

## C. P70 — Complete *original QA question set* versus truncated two-QA package

The AVeriTeC original pinned development source, revision `7c62d1ec8df3fb560d6efe2b85fa191135636f81`, original SHA-256 `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`, contains for the four selected source claims **10 original question records**. The previous P70/P71 task projector retained **8 complete QA atoms** and omitted **2 original questions**. New source-level check also finds **1/10 original questions without a usable original answer under the dataset extractor**. That still does *not* show that the remaining omitted question was semantically dispensable.

**New executable** [`src/p70_full_vs_projected_review.py`](../src/p70_full_vs_projected_review.py) builds 8 claim-condition packets from the actual original data: for each claim, a `FULL_ORIGINAL_QA` packet listing **every original question**, including unanswered/unusable entries explicitly labelled, and a `PROJECTED_TWO_QA` packet containing exactly the currently used selected evidence. It fail-closes if a projected QA triple (question, answer, source URL) is absent from the original; holds the source gold label outside the reviewer surface. Important: *full original QAs* means full QAs captured in the frozen source JSON, **not independently revisited web-page content**.

**Panel design:** Four distinct blind human reviewers, two **separate** reviewers for each condition; each reviewer sees four claims, never the competing condition. Prospectively **16 additional judgments** (4 claims × 2 conditions × 2 reviewers) would be needed. The already planned **P71 16 packet-variants × two reviewers = 32 different judgments** remain `0/32`. P70 additional `0/16` is *not* double-counted toward P71. Contrasts are grouped at 4 original claim clusters; adjudicate role, truth, time/referent, missing evidence, question dependencies and reviewer disagreements within arms before comparing them. Between-reviewer differences may confound apparent packet-projection effects; random assignment/counterbalancing and independent source checks are required before causal attribution.

**Gate:** `ORIGINAL_FULL_SOURCE_QA_PRESENT / 10_ORIGINAL_QUESTIONS / 8_RETAINED_QA / 2_QUESTIONS_OMITTED / 1_UNUSABLE_OR_MISSING_ANSWER / REAL_NEW_REVIEW_0_OF_16 / P71_REAL_REVIEW_0_OF_32 / SEMANTIC_BRIDGE_HOLD`.

## D. Scientific and operational constraints

**Old real observations untouched:** P69 original 192+64; P70 hosted SciFact 32; 288 original historical paid responses already reanalyzed in [previous original-data CI #38043376874](https://github.com/WhoSia/EPISTEME/actions/runs/38043376874). No provider rerun, no new human review, no P69 paper promotion, no P70 behavior transport promotion.

**Actual new G-001-safe evidence:** [the three-job original-source and synthetic design Actions #38044552352](https://github.com/WhoSia/EPISTEME/actions/runs/38044552352), `permissions: contents: read`. All licensed private source and masked human packet text remained only on ephemeral runners and were deleted before public artifacts. Never place original AVeriTeC claim/QA text or reviewer private IDs in public receipts. Actions did not create Git commits, tags or pull request merges.

**Durable proof of execution, Google Drive, checked separately:**
- [P73-P5 synthetic design and HOLD receipt](https://drive.google.com/file/d/1bd-ELHsF801hNuH_da78xSAI9gnJammg/view)
- [P69 8 original heldout clusters, 0/16 scorer receipt](https://drive.google.com/file/d/1j4psNjZi6xcS7Ob6gy6UE3wn8LDk1alc/view)
- [P70 original vs projected comparison, 0/16 human receipt](https://drive.google.com/file/d/1OCllIKsyZmUmvjnlCLzDom0EuL_buYjs/view)

**Next paper-court decision:** P69 A1 can be written as a transparent exploratory negative-methods preprint only, reporting all original contract and scoring failures. P70/P71 warrant-bridge paper remains blocked by actual independent reviewers and original-source page authority; P73 field causal audit paper remains blocked by genuine consent-based time-indexed measurements and causal controls. The strongest next deliverable is an independent blind-review study without duplicate inference from packet variants, not another toy precision improvement.
