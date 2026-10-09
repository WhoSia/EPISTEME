# EPISTEME-P70 ECO2-P1 — Four Real Packet Meaning Audits, Blinded Adjudication Contract and Held-Label Court

**Nature of review:** This is an **unblinded AI/author-side desk triage**, conducted after access to the original AVeriTeC labels and justifications. It is *not independent human annotation*, not two masked raters, not external truth verification, and not packet-level semantic certification. Its purpose is to specify concrete objections that truly independent masked reviewers must address. Review packets compiled by `src/p70_packet_adjudication.py` OMIT author source labels and justifications. **Original publisher CC BY-NC 4.0 source text stays in an ephemeral runner; no dataset snippets are mirrored here.**

**Original source:** [Schlichtkrull, Guo & Vlachos (2023), AVeriTeC](https://arxiv.org/pdf/2305.13117) and [original dataset](https://github.com/MichSchli/AVeriTeC). Original frozen dev blob commit `7c62d1ec8df3fb560d6efe2b85fa191135636f81`, SHA-256 `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`. Source design originally employs independently generated QA and a separate sufficiency check, but its judgments covered **the source's full question-evidence selection, not our projected two-QA packets**. That original independent annotation is useful evidence, not a license to transfer the verdict unchanged.

## Actual four selected claim fingerprints and triage (not new observations by reviewers)

| Fingerprint | Original source row | Original full-claim label (sealed in blind review) | Two-QA projected-packet concern | Author-side preliminary status |
| --- | ---: | --- | --- | --- |
| `a8ddb723e9ef...` | 194 | SUPPORTED | Population near independence: independence date refers to early October 1960; reported 45.1m estimate is for July 1960. Approximation tolerance and referent/time consistency are not explicit in QA. | `PROVISIONAL_CONDITIONAL_SUPPORT / DATE_GRANULARITY_HOLD` |
| `f65945ae30f6...` | 144 | SUPPORTED | A source claim dated October 2020 asserts WTO director-general appointment. The retained QA describes appointment outcome, with risks of later knowledge inserted into evidence for an earlier claim; a different QA names a competitor. **Time of evidence publication and retrospective update must be checked.** | `TEMPORAL_LEAKAGE_AND_CLAIM_TIME_HOLD` |
| `6b336f350384...` | 272 | REFUTED | In the actual code, an uncited `Metadata` question is excluded. The two retained QA items concern legal paper ballot-retention and a report that ballots physically remain. The allegation concerns **digital ballot images**, which are not the same object as physical ballots. A positive statement about physical ballots need not logically refute destruction of electronic images. | `EVIDENCE_OBJECT_IDENTITY_HOLD` |
| `591a9b339edf...` | 493 | REFUTED | One QA dates the first identified US COVID case; another discusses continued China-related travel even after restrictions. The original wording intermixes first case, domestic spread, exception classes and *all travel*. A packet verdict depends on the precise target of the comparison. | `TEMPORAL_SCOPE_AND_QUANTIFIER_HOLD` |

**Crucial correction for claim index 272:** The original dataset contains three questions; one answer's source field is literally `Metadata`, not an HTTP(S) citation. The compiler's `_clean_qa` excludes it, so the actual two projected QAs are the legal-retention QA and a later source assertion about physical ballot storage—not the first two raw question array entries. This is verified against the original JSON blob, not guessed from an author rationale.

## Genuine reviewer procedure and anti-contamination requirements

- Two **distinct human reviewers independently** read the same 16 *masked* packet presentations; they are blind to source labels, justification, historical model responses and each other's answers. Each packet must show original claim text, exactly the projected QA answers and provenance URLs, with explicit instruction not to browse external facts for the first-stage packet-evidence verdict.
- Each reviewer supplies: `SUPPORT / CONTRADICT / INSUFFICIENT / AMBIGUOUS`, one or more necessary evidence IDs if asserting SUPPORT or CONTRADICT, whether QA ordering is safe, flags (temporal scope, subject identity, evidence specificity, cross-QA dependency, source access, context dependence), and an auditable reason.
- Reviewers must separately confirm whether original claim date and source date are consistent. A URL or historical archive is **not** by itself an audit of source publication time. If independent source lookup is allowed, it must occur in a **second documented source-verification phase** and not contaminate the closed-packet verdict.
- Paper's original multi-round human annotations are never counted as either new project reviewer. A model-generated mock `--self-test` is never counted as a human review.
- Two reviewers' source-blind verdicts that disagree, have unresolved ambiguity, or lack necessary evidence **cannot be collapsed by majority vote**. Require adjudication by an authorized third human reviewer with a disagreement ledger or mark `HOLD`.
- Independent expert/QA organization authentication is outside the code's authority; the software validates declarations and consistency, not whether people were really independent.

## What has actually been completed

1. All four original record fingerprints were traced back to the authoritative JSON; in each case the real QA questions, answers, source URLs and original justification were inspected by the assistant.
2. Four concrete candidate failure mechanisms documented above; none is a certified counterexample without human review and provenance-time scrutiny.
3. A **source-label-blind** 16-packet compiler and a conservative 2-reviewer agreement/continuation validator implemented in `src/p70_packet_adjudication.py`; pure fake fixtures test that incomplete reviews, same reviewer IDs and disagreements do not yield semantic acceptance.
4. Read-only original-source CI fetches actual frozen AVeriTeC data, stages raw masked packets ephemerally, emits a **review HOLD receipt only**, and deletes all raw/sealed material before artifact upload. No paid provider calls or AI-generated fake independent raters.

**Current scientific result:** `ECO2_PACKET_COMPILER_VERIFIED / UNBLINDED_TRIAGE_COMPLETED / TWO_EXTERNAL_BLIND_REVIEWS=0 / PACKET_SEMANTIC_CERTIFICATION=HOLD`.

The four original claim cases are only author-side triage. Avoid saying that independent adjudication or the ECO2 science phase is complete.
