# P71-P0 — Independent Human Adjudication Operational Contract

**Authority:** 0/32 actual human judgments; A/B participants and, where necessary, a third independent arbiter must be real people. Repository Actions tests use artificial data only, not independent judgments.

## Genuine private handoff (no vendor, account, browser network or new model calls)

Required original source `AVeriTeC data/dev.json` from commit `7c62d1ec8df3fb560d6efe2b85fa191135636f81` with SHA256 `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`. Data license CC BY-NC 4.0; noncommercial use, maintain original attribution and source notice. Source and selected QA texts should not be deposited into a public writable issue/thread.

Run from the EPISTEME repository:

```bash
PYTHONPATH=src python src/p71_review_handoff.py \
  --source path/to/original_averitec_dev.json \
  --outdir private/p71_p0 \
  --out private/p71_p0/source_receipt.json

PYTHONPATH=src python src/p71_review_html.py \
  --masked private/p71_p0/reviewer_A_masked.json \
  --template private/p71_p0/reviewer_A_response_TEMPLATE.json \
  --out private/p71_p0/reviewer_A_OFFLINE.html

PYTHONPATH=src python src/p71_review_html.py \
  --masked private/p71_p0/reviewer_B_masked.json \
  --template private/p71_p0/reviewer_B_response_TEMPLATE.json \
  --out private/p71_p0/reviewer_B_OFFLINE.html
```

Transfer A HTML **only to reviewer A** and B HTML **only to reviewer B** through a private, noncommercial channel. The 16 packets are shuffled differently, and identical claims may recur under different source ID/QA order treatment, which reviewers must assess separately. Do not send original source gold, the custodian-only sealed ledger, each other's responses, or the unblinded P70 triage.

The offline HTML contains no API fetch requests, cookies, logging, tracking or autosave. Each reviewer supplies a pseudonym, independently checks each of 16 packet-only cases, and exports their response JSON locally. They should verify that they have not read original labels or prior model answers, and may choose `AMBIGUOUS` or `INSUFFICIENT`. Evidence IDs for SUPPORT and CONTRADICT must be indispensable within the *shown packet*. When a claim's time/referent is not secured by the packet, annotate the relevant flag and do not assume the source label transfers.

After receiving both **actual independent** JSON outputs:

```bash
PYTHONPATH=src python src/p71_review_handoff.py \
  --source path/to/original_averitec_dev.json \
  --outdir private/p71_p0/rebuild \
  --review-a private/p71_p0/human_A.json \
  --review-b private/p71_p0/human_B.json \
  --out private/p71_p0/two_human_court.json
```

The court checks 16/16 rows per reviewer, original packet hashes, reviewer pseudonyms, identical evidence-role sets within each case, QA ordering, flags, reason text and exact disagreement IDs. A later third human adjudication file contains only disputed cases, is independent of A and B, and is passed with `--arbitration private/p71_p0/human_C.json`. It **does not modify** original submissions. The fact that a JSON contains an independence checkbox/attestation does not prove authentic independent provenance; the human custodian must verify that separately.

**Third reviewer JSON required structure:**

```json
{
  "role": "THIRD_INDEPENDENT_HUMAN_ADJUDICATOR",
  "reviewer_id": "REAL_DISTINCT_PRIVATE_PSEUDONYM",
  "independent_from_original_reviewers": true,
  "judgments": [
    {
      "case_id": "EXACT_CASE_ID_FROM_DISPUTE_QUEUE",
      "verdict": "AMBIGUOUS",
      "reason": "At least twelve characters stating independent warrant reasons"
    }
  ]
}
```

This schema is illustrative; replace *every* item with authentic review evidence. The court requires that all and only the disputed cases are included. Even after third review, a truth-preserving SciFact–AVeriTeC dependency/warrant map must be independently tested. **Two humans can agree and both be wrong; unanimous annotations are a candidate certificate, not automatic causal ground truth.**

## Human-subject ethics and inclusion

Before presenting these judgments as new human-study results, check with the intended institution, supervisor or ethics/IRB administrator whether human-participant review/consent approval is required. The project must document voluntariness, time burden, any compensation, pseudonymous privacy/custody, secure handling, reviewer inclusion criteria and withdrawal procedures. Do not identify reviewers in public GitHub artifacts or claim institutional approval without a real determination. P71 GitHub CI verifies **software contracts**, not ethics clearance or participant independence.

## After genuine review

Freeze both review JSONs and a read-only hash/custody receipt under private access. Report disagreements *including true ambiguity* rather than recoding into original AVeriTeC labels. Review corrections must preserve a new revision with reason, not overwrite raw votes. Only a **separate** proof/witness graph and temporal-dependency audit may promote a *limited* SciFact–AVeriTeC semantic mapping. Only then consider paper-grade held-out experimental predictions and a separately approved paid model budget.

Current status: `P71_TWO_DIFFERENT_MASKED_HTML_HANDOFFS_TESTED / REAL_REVIEWER_SUBMISSIONS_0_OF_2 / REAL_JUDGMENTS_0_OF_32 / INDEPENDENT_SEMANTIC_ORACLE_HOLD`.
