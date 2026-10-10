# EPISTEME-P71 — Proof-Bearing Representation Migration across Interface and Evidence Ecologies: Independent Warrant Certification, Partial Semantic-Bridge Completion, Contract-Conditioned Decision Stability & Prospective Switching-Cost Falsification Court

**Status 2026-10-10 KST:** `P71_OFFICIALLY_OPEN / P0_PACKET_HANDOFF_READY / REAL_INDEPENDENT_HUMAN_REVIEWS_0_OF_32 / SCIENTIFIC_CLAIMS_HOLD / PROVIDER_CALLS_0`. Parent EPISTEME [canonical root](https://app.notion.com/p/3dfef561cf928159a05fc412236be36e), [P71 Notion](https://app.notion.com/p/3f5ef561cf92819eaeafcf76bb85feaf), [P69/P70 scoped closure](p69_p70_scoped_closure_court.md).

## 1. The actual primitive question

When a new representation apparently works better on a locally evaluated task, when may a person or institution **responsibly migrate** from the incumbent representation—given evidence adequacy, provenance, translation loss, interface and model/provider contracts, downstream uncertainty, independent checking labor and irreversible switch costs?

This is the EPISTEME founding question of switchability/entrenchment, **not** a purely generative LLM leaderboard or a software migration checklist. A candidate can be technically better locally and still fail to warrant migration. The central research target is a falsifiable **proof-bearing partial migration certificate** with a justified abstain/repair decision.

## 2. Prior evidence, with hard authority caps

- P69 original 192 calls: actual instrument pilot `TECHNICAL_PILOT_HOLD`; Groq JSON format 34/48; Gemini JSON valid-semantic grounded zero. No manuscript construct closure.
- P69-R1: actual 4-call canary + 64-call calibration. Prompt procedure changed Gemini `strict_schema` positive 2/4→0/4 and `json_object` 0/4→4/4; strict and JSON output forms 8/8 each under `procedure_v1`. The +6/4 descriptive difference-in-differences uses **two authored task families × two invocations**, not independently sampled task distributions. Mechanism H1/H5/H6 unresolved.
- P70: exact conditional-transport triangle bound and observational nonidentification under explicit assumptions, 256 within-compiler synthetic witness/trace audits, format-selection decomposition, original real 32-call SciFact pilot on four external source claims (Groq original source-label 16/16, Gemini 8/16), and independently authored AVeriTeC original data with 16 structural R/H packets. The eight paired `SciFact–AVeriTeC` matches establish shared **polarity/provenance metadata** only. No target semantic bridge or behavioral transport identified.
- P69/P70 bounded experimental phases are sealed as completed, *not* papers completed; 8,192 calls never run.

## 3. P71 subphases and evidence contracts

**P71-P0 — Masked human packet warrant court.** [`src/p71_review_handoff.py`](../src/p71_review_handoff.py) reconstructs 16 selected source-anchored AVeriTeC packet variants with original exact source SHA, builds independently shuffled reviewer A/B distributions, response **templates**, source-label-sealed custodian ledger and a non-destructive disagreement queue. It never invents actual human answers. Original data CC BY-NC 4.0 with attribution; participant packets kept outside publicly indexed repository and CI artifacts. The source-label/justification and old model outputs must remain masked for stage-1 packet-only assessment. **Exactly 16 cases × 2 distinct reviewers = 32 real judgments** needed. The completed/declared reviewer provenance must be verified by the responsible human custodian, not trusted merely because JSON has a boolean.

**P71-P0.1 — Independent disagreement reconciliation.** Collect individual verdict `SUPPORT|CONTRADICT|INSUFFICIENT|AMBIGUOUS`, indispensable evidence IDs, QA order safety, flags and reason. Compare each case (verdict/evidence roles/order/flags) without averaging away conflicts. A distinct third human adjudicator rules on each unresolved dispute, preserving all originals; outcome `INSUFFICIENT` or `AMBIGUOUS` is valid data, not forced into original AVeriTeC Supported/Refuted. Reviews submitted by AI or mock fixtures cannot be counted.

**P71-P1 — Proof/warrant bridge construction.** From reviewers' independently certified *packet-level* content, build typed partial maps between SciFact minimal evidence sets and AVeriTeC QA dependency graphs. A map exists only if claim referents, temporal predicates, source/evidence roles, witness sufficiency and intervention commutation survive. An *incomparable* case is `BRIDGE_HOLD`, not a negative model response. Alpha-renaming R may be structurally safe while order H may not preserve anaphoric QA meaning; separate them.

**P71-P2 — Contract-conditioned outcome stability.** Pre-register model+provider bundle, output schema, decoding controls, token budgets, prompt hashes, full request ordering, stopping rule, all-call correctness and conditional-format validity. Freeze *whole original claim cluster* as inference unit. Use truly held-out source organizations and mechanism structures; do not treat 64 serial invocations as 64 independent tasks. No paid calls before P0/P1 pass and fresh approval.

**P71-P3 — Switching decision court.** [`src/p71_switch_certificate.py`](../src/p71_switch_certificate.py) provides a finite exact-rational, assumption-conditional decision interval with interface-specific gates. It returns migration/retention/review-HOLD only after the **real** reviewer/oracle, bridge, temporal, contract and cost warrants are certified. It is decision arithmetic, not a new statistical guarantee or a discovery about hosted models. No current P69/P70 data justify populating all warrant fields as TRUE.

**P71-P4 — Manuscripts and external rivalry.** See [paper candidate and novelty audit](p71_paper_candidate_court.md). Paper-ready requires independent packet semantics, adequate claim-cluster support, preregistered held-out evaluation and appropriately scoped quantitative analysis. A conceptual/negative-methods paper may be defensible earlier if explicitly labeled exploratory, but full P69 paper claim cannot be silently repurposed as P71 confirmatory evidence.

## 4. Exact 16×2 human review workflow and files

Original source **`MichSchli/AVeriTeC`**, pinned git commit `7c62d1ec8df3fb560d6efe2b85fa191135636f81`, original dev SHA-256 `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300`; no source drift tolerated.

Run the provider-free author tool in a local Python 3.12 environment after placing the exact downloaded source under a working directory:

```bash
PYTHONPATH=src python src/p71_review_handoff.py \
  --source path/to/original_averitec_dev.json \
  --outdir private/p71_human_review \
  --out private/p71_handoff_receipt.json
```

Distribute **only** `reviewer_A_masked.json` and `reviewer_A_response_TEMPLATE.json` to reviewer A, and the analogous B files to reviewer B. Verify non-commercial use/AVeriTeC credit. **Never** distribute `CUSTODIAN_ONLY_sealed_ledger.json` or P70 source labels; keep responses private, named by pseudonym. Reviewers set `independent_from_author_and_model_outputs=true` only if genuine. Inter-reviewer discussion is prohibited before separate submissions.

After two *real* responses, run the same script with `--review-a private/A.json --review-b private/B.json --out private/court.json`, which compares them against the exact frozen packet ledger and reports disputes. For disagreements a **third distinct person** can submit separate `--arbitration private/C.json` addressing only the exact disputed set, with original two votes preserved. Software deliberately cannot turn attested identities into verified external human independence.

**Operational warning:** the public GitHub Action `p71_review_admission.yml` compiles these masked packets only in an ephemeral runner and uploads **status metadata, not licensed packet text**. To furnish actual human reviewers with packets, run this code locally or through a user-authorized private file exchange; the CI's green badge does NOT mean any completed human ratings.

## 5. Source-specific reviewer challenges (unblinded triage ≠ human label)

Four frozen AVeriTeC source instances (one source claim each, four R/H views):
- population of Nigeria at independence: July vs October 1960 estimate/approximation scope;
- WTO directorship: date of original claim vs later appointment/reported selection;
- Massachusetts election claim: physically retained *paper ballots* cannot alone establish survival of *digital ballot images*;
- first US COVID case vs spread/community transmission and qualifier about who could travel.

These are **pre-identified adversarial context flags** in [P70 desk triage](p70_packet_semantic_triage.md). The blind reviewer should not see the unblinded notes before grading. These four cases cannot produce reliable estimates of corpus-level independent-human agreement, population transportability or contract effects.

## 6. Inference, stopping and authority

All study claims must state `[Original authors' claim]`, `[Our reconstruction]`, `[Hypothesis]`, `[Observed]` and `[Hold]` separately. Pre-specify:
- primary endpoint: human-adjudicated evidence-grounded answer direction **over all provider requests**, with absent/invalid responses tracked separately;
- secondary endpoints: conditional-on-format grounded correctness, evidence role validity, null/ambiguous response and QA dependency sensitivity;
- clustered uncertainty by original claim/source organization, not by response row or R/H replica;
- source organization and true source ecology, not surface format alone, as held-out transfer units;
- abstention: real adjudicators may legitimately rule packet insufficient; lack of 32 reviews prevents empirical estimand identification;
- costed decision: a migration policy must outperform not only a no-change baseline but also an information-acquisition/partial review policy under explicit costs. Any purported novelty over established decision theory and selective risk methods needs an *actual new empirical pattern or nontrivial theorem*.

**Current state:** `P71_OFFICIAL_OPEN / P0_HANDOFF_TESTED / 0_OF_32_REAL_INDEPENDENT_REVIEWS / P1_SEMANTIC_BRIDGE_HOLD / P2_MODEL_STUDY_NOT_AUTHORIZED / P3_MATHEMATICAL_ONLY / P4_PAPER_NOT_READY`.
