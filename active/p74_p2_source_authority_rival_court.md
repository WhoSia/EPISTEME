# EPISTEME-P74-P2 — Bitemporal Authority, Revocation and Evidence-Role Falsification

**Formal status:** Within officially OPEN P74, this is an internal P2 research section, not P75 or a separate Lab. **Date:** 2026-10-10 KST. **Method:** retrospective read-only, genuine public document metadata + source text, deterministic typed-event reconstruction, mutated synthetic regression tests. **No actual institutional audit/contact, legal advice, human assessor, paid-model or current web-page authority certificate.**

## 0. Explanandum and claim ceiling

How can a scientific or administrative proof justify a representation switch if documentary authority changes between publication and effective time, corrections reveal errors in old publication, and independent witnesses only learn of those changes later? This question is descended from P69 contract-driven observability, P70 recorded vs original evidence, P71 switching, P72 typed warrant, P73 reflexive audits, and P74-P0/P1 observational equivalence. See [the bounded P69–P73 inheritance ledger](p74_p69_p73_inheritance_court.md).

`Observed publication`, `claimed legal effective date`, `public knowledge after publication`, `observed bytes`, `independently certified official PDF`, and `proof role` are **six distinct properties**. Do not use a source URL or a copy of HTML as proof of official legal status.

## 1. A true three-document publication/correction/withdrawal chain

Document class: US Food and Drug Administration administrative-hearing procedure under docket **FDA-2024-N-3654**; examined only as *source-documentary event history*, not advice about regulated activity.

| Event | Original record ID | Document publication date (publication-knowledge proxy) | Content of chronological claim |
| --- | --- | --- | --- |
| Original published direct final rule | **2024-21231**, 89 FR 77019 | **2024-09-20** | General planned effective date **2025-02-03**; future effectiveness was conditional on significant comments/no subsequent withdrawal |
| Public correction | **2024-24100**, 89 FR 83781 | **2024-10-18** | The omitted effective date for amendatory instruction 3 was corrected to **2025-12-18**; original main date remained **2025-02-03** |
| Withdrawal | **2025-01145**, 90 FR 5590 | **2025-01-17** | The original direct final rule was expressly **withdrawn effective 2025-01-17**, before either prospective effective date. Withdrawal document bears issued/signed **2025-01-13** and filed **2025-01-16** timestamps |

**Source verification (read-only):**
- [Original Federal Register publication XML rendering](https://www.federalregister.gov/documents/2024/09/20/2024-21231/regulatory-hearing-before-the-food-and-drug-administration-general-provisions-amendments).
- [Correction public-inspection source record](https://public-inspection.federalregister.gov/2024-24100.pdf) and [official govinfo PDF locator](https://www.govinfo.gov/content/pkg/FR-2024-10-18/pdf/2024-24100.pdf); date correction visible in extracted public-inspection text.
- [Withdrawal Federal Register public XML rendering](https://www.federalregister.gov/documents/2025/01/17/2025-01145/regulatory-hearing-before-the-food-and-drug-administration-general-provisions-amendments-withdrawal) and [official govinfo PDF locator](https://www.govinfo.gov/content/pkg/FR-2025-01-17/pdf/2025-01145.pdf).

**Provenance caution:** FederalRegister.gov itself explicitly disclaims that the displayed XML rendition is the *official legal edition*, directing legal readers to govinfo.gov. The official PDF locators are known; **verified official original PDF file bytes and SHA-256 have NOT been obtained in the present runtime**. Do not claim the official electronic PDFs were byte-authenticated, independently timestamped, or independently cross-rendered. Source URL is not a capture receipt. Publication day is a **public documentary knowledge timestamp**, *NOT* the Federal Register database's actual transaction commit time or the first moment any observer could have known a pending draft. The historical public-inspection record may precede publication; it has a different access role and must not be silently equated to published authoritative status.

## 2. Research model

Define a record `e` with:
- `pub(e)`: publication day in official bulletin's public history (transaction-time **proxy only**);
- `issue(e)`, `file(e)`: signed/filing days when known, not substituted for publication time;
- `scheduled(e, scope)`: scope-specific projected effective date;
- `withdraw(e, affected_original)`: agency action cancelling a prospective rule, effective on recorded withdrawal date;
- `proof_role(e)`: one of `HISTORICAL_PUBLICATION`, `PROPOSED_FUTURE_NORMATIVE_EFFECT`, `CORRECTION_OF_EFFECTIVE_DATE`, `WITHDRAWAL_OF_ORIGINAL_RULE`, `CURRENT_ENFORCEABLE_AMENDMENT`;
- `source_fidelity(e)`: `PUBLIC_INDEX_AND_TEXT_DESK_REVIEW`, NOT `OFFICIAL_AUTHENTICATED_PDF_VERIFIED`.

For factual valid-date **v**, publication-knowledge cutoff **r**, and proof role **rho**, define a *document-level, source-relative* query `Q(doc,v,r,rho)`. The query returns a **typed epistemic status**, not a Boolean material truth value or a legal opinion. For `r < pub(e)`, an event's published record is unavailable in the public as-of set even if a later researcher knows it. For `v > r`, an apparent future effect is `PROJECTED_EFFECTIVE_CONDITIONAL_ON_NO_FUTURE_WITHDRAWAL`, never an already-certified past fact. A completed withdrawal before the original effective date yields `WITHDRAWN_BEFORE_ORIGINAL_EFFECTIVE_DATE`. `HISTORICAL_PUBLICATION` remains supported even after withdrawal, because revoking a prospective rule is not deleting the event that it was previously published.

### Exact implemented discriminators

| Query | State |
| --- | --- |
| Knowledge cutoff **2024-09-30**, special instruction 3 | `SPECIAL_EFFECTIVE_DATE_UNSPECIFIED_AT_THIS_RECORD_DATE` |
| Knowledge cutoff **2024-11-01**, special instruction 3 scheduled for **2025-02-04** | `SCHEDULED_NOT_YET_EFFECTIVE` (special date is 2025-12-18) |
| Knowledge cutoff **2024-11-01**, main rule targeted **2025-02-04** | `PROJECTED_EFFECTIVE_CONDITIONAL_ON_NO_FUTURE_WITHDRAWAL` |
| Knowledge cutoff **2025-01-20**, main rule targeted **2025-02-04** | `WITHDRAWN_BEFORE_ORIGINAL_EFFECTIVE_DATE` |
| Knowledge cutoff **2026-01-01**, role `HISTORICAL_PUBLICATION` of original rule | `DOCUMENTARY_EVENT_SUPPORTED` |
| Same content and date with role `CURRENT_ENFORCEABLE_AMENDMENT` | `WITHDRAWN_BEFORE_ORIGINAL_EFFECTIVE_DATE` |

Source-position-aware event roles prevent an invalid semantic substitution: the **correction document** is not itself the **original amendment**, and a withdrawal document is evidence about withdrawal, not an authorization to enforce the withdrawn amendment.

**Executable self-testing source:** [src/p74_p2_bitemporal_federal_register_court.py](../src/p74_p2_bitemporal_federal_register_court.py); stdlib Python. This is a **curated factual metadata ledger, not a runtime HTTP ingestion or a cryptographic source-validation pipeline**.

## 3. Rival countermodels and scientific falsification verdicts

1. **Rival R-T1: publication time = effective time. REJECTED for this specific real event chain.** The 2024-09-20 publication did not make the proposed new rule effective on publication. Source document planned 2025-02-03, and it was withdrawn beforehand. Not a general theorem: statutes and rules can have immediate effectiveness in other cases.
2. **Rival R-T2: one monotonically increasing rule-status scalar suffices. REJECTED if required queries include both 'was published' and 'was normatively effective'.** Following withdrawal, historical existence remains true while rule-effectiveness is absent. A scalar could encode all states artificially; the real failure is *untyped scalar semantics*, not a mathematical impossibility for arbitrary encodings.
3. **Rival R-T3: later metadata may be inserted into a past as-of decision. REJECTED as retrospective leakage.** 2024-11-01 knowledge did not contain 2025-01-17 withdrawal publication, though the latter is available in a 2025 retrospective historical analysis.
4. **Rival R-T4: two temporal dimensions plus provenance are new to EPISTEME. REJECTED as novelty claim.** Standard bitemporal DB SQL and W3C PROV-O already represent distinct timelines, generation and invalidation. P74 should seek a stronger domain-specific discriminator, not claim 'bitemporal time' as invention.
5. **Rival R-T5: historical chain establishes an effect of a public scientific audit on source authority. NOT IDENTIFIED.** This documentary timeline had no research audit intervention; the agency's withdrawal after submitted comments is NOT causally attributable to the P74 researcher. Do not confuse administrative comments with experiment randomization or causal counterfactuals.
6. **Rival R-T6: public-page citation proves original document content and legal standing. REJECTED as an authentication shortcut.** Federal Register XML states it is informational; official govinfo original PDF byte-level verification remains HOLD. Factual metadata reading is useful but lower authority than verified official, contemporaneously captured originals.
7. **Rival R-T7: proof role can be inferred from timestamp alone. REJECTED in this specific typed query.** The exact same historical artifact supports a claim *that the document was published* but does not support *that the withdrawn prospective amendment is currently in force*. Source authority alone does not determine the proposition or inference target.

**Code attacks:** rejects wrong source docket or locator, swapped event times, later signatures, incorrect instruction-specific date, source role laundering, attempts to relabel public-index inspection as cryptographically authenticated official PDF and premature use of a later published withdrawal. Historical event remains recorded; effective authority is not retroactively granted.

## 4. Genuine prior art and literature controls

- [ISO/IEC 19075-2:2021 abstract](https://www.iso.org/standard/78933.html): explicitly covers SQL application-time, system-versioned and bitemporal tables. **Drive 미확보(색인 검색 기준)**; paid full standard not obtained/read.
- [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/): `prov:generatedAtTime`, `prov:invalidatedAtTime`, generation and invalidation activities. **Original public standard directly read on the Web**; no private Drive PDF identified, which is not required for a freely published W3C web standard.
- [Pérez, Rubio Garcia & Zapata (2025), PROV-IDEA](https://drive.google.com/file/d/1uWNj6eYFDnjIJzsbbR4BFZhTZGJV5Y_9/view): original PDF obtained/read from canonical Google Drive; PROV-compatible schema/data evolution and nonintrusive provenance tracking are direct competitors to generic P74 provenance claims.
- [Menotti et al. (2025), Provenance-driven nanopublications](https://drive.google.com/file/d/1OYSmdtKsVzWdJS2MyaYLaGcIYeoT8YLE/view): canonical Drive PDF retrieved/read; provenance of aggregated multi-source scientific assertions, including supporting/conflicting evidence, directly competes with generic multi-source warrant ideas.
- [Manski (2005), original PDF in Drive](https://drive.google.com/file/d/1dVBEhKzemt_qokxS-PTwntbq3RpLONdO/view): incomplete observations allow partial rather than point identification. P74-P1 already showed public authority time records by themselves do not identify the missing audit potential outcomes.

No paper-level originality, new legal analysis, new real-world causal discovery or empirical P69/P70 semantic bridge is claimed at P74-P2.

## 5. Next falsifier: signed temporal facts vs independent original warrant

A stronger genuinely informative P74-P3 should choose a **real, publicly verifiable, stable, non-sensitive and permission-compatible** record series for which official signed historical snapshots and independent record-time captures (not merely a retrospective summary) are obtainable. Require **two non-redundant evidence carriers** for a given proposition; preregister the inference role and original authority/edition before evaluating. Compare:
- source-event *documentary* provenance;
- externally authenticated effective-period authority;
- semantic entailment relative to the precisely stated claim;
- retrospective `known_as_of` and prospective *information actually available then*;
- effect of evidence upon downstream representation-switch decisions.

The decisive endpoint is whether admissible evidence and independent warrant permit a justified **switch of an entrenched representation**, not whether a temporal SQL query returns an aesthetically tidy status.

**Standing HOLD:** actual institution audit intervention=0; recruited independent human P69 0/16, P70 0/16, P71 0/32; original official PDF SHA, historical independent timestamps, current legal completeness, manuscript novelty and transport claims remain unverified. **G-001:** GitHub Actions only `contents: read`, authored commits via user account only.
