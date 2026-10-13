# EPISTEME-P75-P1 — Original VitaminC Revision-Ecology Admission, Independent Minimum Warrant & Costed Switching Protocol

**Internal section within formally OPEN P75** · **Date:** 2026-10-13 KST · **Verdict sought:** source/format admission and preregistration, NOT a newly identified behavioral or causal effect.
**Evidence status:** Actual external author dataset/primary full paper read and *public TRAIN viewer rows inspected*. Original full JSONL bytes, Wikipedia historical page revisions, independent human review, switch utilities and hosted models **NOT** acquired/verified. This is a meaningful upgrade from P75-P0's metadata-only proposal, but **NOT a third completed experimental ecology**.

## 1. Actual independent authored-source ecology and primary paper

**Original scientific source:** Schuster, Fisch & Barzilay (2021), *Get Your Vitamin C! Robust Fact Verification with Contrastive Evidence*, NAACL, ACL Anthology [paper](https://aclanthology.org/2021.naacl-main.52/) · [original full PDF](https://aclanthology.org/2021.naacl-main.52.pdf), DOI 10.18653/v1/2021.naacl-main.52. This 20-page **original PDF** was inspected directly, including the figures and methods §3–4. The authors reported real Wikipedia factual revisions plus a **separate synthetic edit** portion; real-revision source labels **cannot automatically become certificates of historical article truth or Wikipedia timestamp authenticity**. Their example Fig. 1 includes Wikipedia revision ID 336934876; the paper uses a very similar pre/post evidence context to a fixed claim. The original paper's own contrastive fact-verification/rationale/minimal masking method means **P75 must not claim to invent contrastive revision tests or word-level rationale selection**.

**Primary dataset source:** [author GitHub](https://github.com/TalSchuster/VitaminC), original [DATA_LICENSE](https://github.com/TalSchuster/VitaminC/blob/main/DATA_LICENSE) verified through GitHub connector at blob SHA `24bc3f6b5731f9825285bea10ddaa0ecbf0d26c5`. License directs users to the applicable Wikipedia policy and otherwise CC BY-SA 3.0; the synthetic material derives from FEVER. [Hugging Face author-published data](https://huggingface.co/datasets/tals/vitaminc) reports a `cc-by-sa-3.0` license field, but downstream use still obeys article-level attribution/share-alike requirements. Dataset repository publicly lists commit `be6febb761b0b2807687e61e0b5282e459df2fa0` and three source JSONL files, with **published manifest pointers**:

| Dataset file | Published Xet pointer SHA256 (provider metadata, not independently recalculated) | Full bytes retrieved here? |
| --- | --- | --- |
| `train.jsonl` | `7461c6fd1a13459590317c5ccdc8651dd2daf7c1ad8ae4b10ccd88d164fccd5a` | No |
| `dev.jsonl` | `544934677f5d133873e6d38f4557f8966f4efa5d3d70874ffe6913f2091b86b5` | No |
| `test.jsonl` | `7ad1808dbc30c62e0a1427a53022d0dfaff668a1fde3c4b612a2d266edd753ad` | No |

[train file metadata](https://huggingface.co/datasets/tals/vitaminc/blob/main/train.jsonl) · [dev file metadata](https://huggingface.co/datasets/tals/vitaminc/blob/main/dev.jsonl) · [test file metadata](https://huggingface.co/datasets/tals/vitaminc/blob/main/test.jsonl). SHA strings are **published expected checksums**, not a claim of in-runtime file-hash validation. No dataset redistribution or copyrighted original claims/evidence on public GitHub.

### 1.1 Actually inspected real row-level samples — explorative TRAIN only

The public Hugging Face **TRAIN viewer** exposes real released author-row metadata (`unique_id, case_id, wiki_revision_id, label, claim, evidence, page, revision_type`). Two wholly distinct source-article groups were manually read from the visible original source (8 authentic displayed dataset rows; actual source status read-only, not independently adjudicated):
- `Manchester`, `case_id=5ec5598dc9e77c000842c3cd`, `wiki_revision_id=925488060`, `revision_type=real`, four labelled records `SUPPORTS / NOT ENOUGH INFO / NOT ENOUGH INFO / SUPPORTS`.
- `Defy Media`, `case_id=5ec7d50dc9e77c00084418c7`, `wiki_revision_id=567579153`, `revision_type=real`, four labelled records `NOT ENOUGH INFO / REFUTES / NOT ENOUGH INFO / SUPPORTS`.

**These are illustrative source previews, NOT a random sample, heldout packets, human-signed labels or 8 independent mechanism clusters.** Dataset-reported `real` is the *author's revision-type metadata*. No actual MediaWiki revision endpoints, original page historical bytes and as-of public availability were independently recaptured; even labelled pairs with identical `wiki_revision_id` must not be presumed independently chronological from their row suffixes. The case IDs and revision IDs are publicly documented to allow a later externally pinned source retrieval.

**Executable source-admission court:** [src/p75_p1_vitaminc_source_admission.py](../src/p75_p1_vitaminc_source_admission.py). Checks real provider-published source case/revision labels, 2 distinct pages and 8 public TRAIN rows; rejects duplicate claim/revision group, fake `test`/synthetic promotion and fake independent original authentication. Public code stores **metadata only**, not third-party claim/evidence body text.

### 1.2 Independent ecology entry verdict

- Original author, published method, license, dataset version manifest & TWO exploratory real TRAIN case-group references: **SOURCE-PROVENANCE DESK PASS**.
- Third ecology as an **independently authored scientific mechanism family** (contrastive edited Wikipedia evidence): **SOURCE FAMILY DISCOVERED**.
- Third ecology with **byte-authenticated raw original data, independent historical article revision certification, genuinely heldout claim-group split, blinded warrant and policy outcomes**: **RESEARCH-ECOLOGY EMPIRICAL ADMISSION HOLD**.
- Original paper's training/evaluation split by article means **repetitions with different `case_id` are not necessarily independent source pages**; split and inference units must be frozen at `original_page × revision-family` after complete source retrieval. Literal author labels are not independent gold adjudicators.

## 2. P18-failure-resistant matched witness design

P18 had a fatal unmatched control: Rich kept the source-linked witness in retained history and relation; Recoverable-Coarse referenced the witness only in relation notes, not source trace. For P75-P1:
- `FULL_ORIGINAL`: all licensed, captured original evidence atoms and references.
- `MATCHED_RECOVERABLE`: fewer irrelevant atoms, but **same actual decisive evidence ID** must survive in *retained history trace AND relation mapping*, with unchanged referent/temporal role.
- `LOST_DECISIVE`: matched length/position/context but the witness atom is genuinely absent, with decoy in that position.
- `NULL`: equally salient provenance link but invariant/irrelevant to the exact claim.
- No declared positive control passes solely because the annotator believes the witness is present. A source-custodian and two blinded raters must find it independently. Decoy citations do not satisfy minimal sufficiency. If there are multiple legitimate minimal proof sets, accept any independently validated minimum, not only one author-coded path.
- Never use the **dataset's claim label** as automatic warrant correctness for a shortened packet.

Formal layout test [src/p75_p1_vitaminc_source_admission.py](../src/p75_p1_vitaminc_source_admission.py) purposely rejects the old 'witness in relation notes but not retained source history' positive-control mismatch. **This is a unit test, not measured human recovery.**

## 3. Prospective masked independent-human protocol

[Executable blinded-review and cost-admission validator](../src/p75_p1_blind_warrant_utility_protocol.py). All sampled review identities in CI are `SIMULATED_`, **no actual humans contacted**.

**Experimental unit** = original independent *source article × revision lineage/claim-cluster*; not individual response or four correlated dataset rows. Conditions will be source-version- and claim-specific; published access date, original predecessor and successor wiki revision IDs, available evidence atom list and license are frozen before any human exposure. A source custodian independent of the packet author must authorize original/archival wording and actual time-role claims.

**Allocation**: Four externally verified independent reviewers prospectively requested per claim group, two per `FULL_ORIGINAL` and two per `MATCHED_PROJECTED`, with crossed reviewer assignment across balanced claim groups. Each reviewer sees **only one evidence-view arm of the same claim cluster**; across different clusters, arms reverse. Randomized cluster order and hidden author-packet gold and model outputs prevent direct carryover; review condition may be distinguishable from packet contents, so **do not pretend perfect blindness**. CI generates a synthetic four-cluster × four-reviewer schedule (16 MOCK slots, 0 actual independent judgments).

**Per adjudication:**
1. independent three-way `SUPPORTS/REFUTES/NOT ENOUGH INFO` judgment for the precise claim and as-of date;
2. immutable actual source/revision SHA & provenance access limitations; no unproven legal/current authority;
3. select a candidate minimally sufficient evidence-atom set, mark sufficiency of the full set and necessity after *each single atom removal*; evaluate alternate valid minimal sets; **single-deletion minimality is not always enough** when entailment is nonmonotone, so where necessary exhaust proper subsets or escalate;
4. separate source/proof role, relevance, contradiction and ambiguous/omitted evidence; retained or altered evidence IDs must be independently checked;
5. decide `KEEP`, `SWITCH`, or `REVIEW` given a stated hypothetical cost matrix and expected evidence access;
6. second human independently adjudicates same evidence arm. Conflicts go to a **third distinct adjudicator** under predeclared conflict rule, with initial disagreement preserved.

**Identity/custody:** reviewer pseudonyms are not signatures; actual independence needs an outside custodian, informed consent, non-overlap with packet authors, minimal access and private sealed records. Public GitHub receives only counts, schema & hashed aggregate receipts, never identifiable names or licensed raw original text. Any submitted Boolean `real_human_review=True` is **not** sufficient to claim an actual independent verdict; the validator emits `OUT_OF_BAND_CUSTODIAL_CONFIRMATION` pending direct readback. No recruitment initiated.

**Controls and analysis:** P69 schema validity distinct from grounded correctness, P70 original 10 questions/10 answers and 8 projected usable QA cannot be collapsed into generic semantic labels, P71 full vs projected original human 0/32 remains separate, P57 interaction transport not established. Include packet SHA/type/length checks, matched positive vs truly missing vs null decoy, source-time role shifts, original article cluster exclusion across validation/test, crossed reviewers & two-rater agreement/disagreement, order randomization and cluster-aware uncertainty. A third ecology’s existence does not make P75 mechanism invariant across all three; hypothesis must survive **ecology-specific interaction tests**.

**Primary scientific estimand candidate**: on independently source-authenticated and meaning-adjudicated heldout claim clusters, the paired effect of source-/warrant-preserving `FULL→MATCHED_PROJECTED` exposure on the proportion of *independently justified* KEEP/SWITCH/REVIEW actions under preregistered cost assumptions, contrasting competent bitemporal+PROV+proof-role and minimax-regret / Blackwell information-based rivals. A task-class or changing evidence-year alone does not identify causal transfer. The complete statistical analysis plan (cluster power, outcomes, multiplicity, conflict handling, preregistered sample size) is **NOT SEALED**, because true cluster census, human custodian and utility calibration are missing.

## 4. Costed transition utility / decision-value protocol

Predefine actions `a∈{KEEP,SWITCH,REVIEW}`, claim states `s`, and externally validated costs/rewards *before* observing reviewer/model condition outcomes:
- `U(KEEP,s)`: conventional representation's evidence-qualified decision loss;
- `U(SWITCH,s)`: proposed representation's qualified loss minus transition cost, false-switch harm and irreversibility penalty;
- `U(REVIEW,s)`: information benefit after independent review minus reviewer cost, access delay and possible feedback-induced source change.
- `ΔU = E[U(π_P75,S)-U(π_STRONG_BASELINE,S)]` at fixed claim-source lineage and the same access, source version and cost assumptions. If costs or counterfactual outcomes unobserved, output **IDENTIFICATION HOLD**; don't substitute a positive simulation for measured utility.
- Strongest comparator implements correct valid/system-time provenance plus proof-role + legitimate minimal-warrant check and a proper standard decision rule. A trivial latest-document parser is a deliberately weak ablation, not the primary opponent. Under pure regret, a policy may opt SWITCH without warrant; this is **not** proof that the normative certification policy is socially superior.

**Utility validator** rejects negative/non-Fraction costs, and always flags `SWITCH_UTILITY_EMPIRICAL_HOLD` absent externally calibrated costs. Marking `externally_calibrated=True` only yields `REQUIRE_EXTERNAL_RECEIPT`; cannot promote a typed record to independently obtained real utility.

**Hard paper gate:** original-data SHA verified in runtime; genuinely independent latest/historical source page revision + access time; licensed evidence atoms and rights; source-group-disjoint heldout third ecology; externally verified non-author human reviews; preregistered decision utility and primary comparator; measured blind randomized blocks and cluster-aware statistic; evidence of improvement *over the strongest comparator*. All not currently satisfied.

## 5. Exact counts and adversarial falsifiers

- **Actually acquired in this step:** full 20-page original publisher-hosted research article **read**, author repo README/LICENSE **read**, Hugging Face published source-manifest checksum values **recorded but not rehashed**, real TRAIN viewer *eight* dataset rows over *two* source groups **manually read and metadata recorded**. A publicly verifiable external research ecology exists and can be anchored by exact source IDs.
- **Not acquired:** complete original dataset JSONL bytes, independently witnessed MediaWiki old/new source page snapshots, a new holdout split, authoritative original SHA recalculation, human reviewers/consent, real switching decisions, new paid LLM outputs.
- **Potential failure modes**: page-lineage leakage across train/test; 'real' dataset label masquerading as factual legal/source certification; annotation of a synthetic revision as historical; source-id shadowing while evidence witness disappears from trace; circular independent gold; rater/condition confounding, presentation-order leakage; confidence without cost calibration; peer-reviewed VitaminC original known method being relabelled novel P75; P69 evidence count 288 being duplicated; green CI falsely used as human study confirmation.

**P75-P1 scientific verdict sought:** `ORIGINAL_ECOLOGY_SOURCE_METADATA_PASS / MATCHED_WITNESS_AND_HUMAN_COST_PROTOCOL_READY / ACTUAL_SEMANTIC_SWITCHING_EFFECT_HOLD`. No new formal version P76 opened.

## 6. Next admissible move

Obtain complete `dev.jsonl`/source-hash verified bytes in a license-compliant private archive and verify actual MediaWiki revision diff/oldid for cluster-disjoint *real* cases; original-paper PDF canonical Drive filing is desirable but currently **Drive 미확보(색인 검색 기준)**, do not invent a Drive file. Then freeze a heldout cluster census + independently reviewed minimal sets. Do not spend on LLM calls or recruit people until source custody and consent are authorized.

**G-001 hard rule:** read-only GitHub Actions `permissions: contents: read`; no Actions bot commits/pushes/tags; new scientific commit author/committer = authenticated `WhoSia`. All failures/negative results and costs remain explicit.
