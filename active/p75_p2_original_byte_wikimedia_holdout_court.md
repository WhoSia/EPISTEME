# EPISTEME-P75-P2 — Original VitaminC Full-Byte SHA-256, Wikipedia Revision/Parent Content & Source-Disjoint Holdout Court

**Date:** 2026-10-13 KST. **Stage:** P75-P2 within OPEN P75. **Execution:** read-only GitHub Actions on authenticated user's repository. **Original licensed text** present only transiently on runner and deleted; no raw claim/evidence rows, Wikipedia wikitext, individual selected case identifiers, or source plaintext appear in public GitHub commits/receipts. **Independent human reviews and actual switch utility:** 0.

## 1. Acquisition/rehash outcome — real released original bytes, not hypothetical metadata

[Reproducible executable](../src/p75_p2_original_dataset_custody.py) downloads **all three original, publisher-authorized VitaminC JSONL files** from the pinned exact Hugging Face [repository revision](https://huggingface.co/datasets/tals/vitaminc/tree/be6febb761b0b2807687e61e0b5282e459df2fa0), using ephemeral working files, streams SHA256 over the downloaded bytes and verifies exact agreement with the publisher's original release **Xet pointer expected SHA**. It then parses every JSONL record, computes split/source-page census, deletes originals, and preserves **metadata-only** cryptographic receipts via the read-only workflow. **All three SHA matches independently computed.**

| Original provider file | Full bytes received on runner | Rows actually parsed | Independently recomputed SHA-256 |
| --- | ---: | ---: | --- |
| `train.jsonl` | **193,958,244** | **370,653** | `7461c6fd1a13459590317c5ccdc8651dd2daf7c1ad8ae4b10ccd88d164fccd5a` |
| `dev.jsonl` | **32,876,983** | **63,054** | `544934677f5d133873e6d38f4557f8966f4efa5d3d70874ffe6913f2091b86b5` |
| `test.jsonl` | **28,717,099** | **55,197** | `7ad1808dbc30c62e0a1427a53022d0dfaff668a1fde3c4b612a2d266edd753ad` |

**Total: 255,552,326 actual original bytes; 488,904 published examples; all three SHA matches PASS.**

This proves the runner's downloaded bytes are identical to the provider-published checksummed files at the pinned revision, not that the underlying Wikipedia evidence was true at its historical date or that the dataset annotations represent independently certified warrant.

**Source license:** [Author's original DATA_LICENSE](https://github.com/TalSchuster/VitaminC/blob/master/DATA_LICENSE), streamed and checked against mandatory Wikipedia and Attribution-ShareAlike terms, receipt SHA256 `153a128e86c7d0e978243c8c8994dbb5fba9081a36e`. Dataset metadata says `cc-by-sa-3.0` but original Wikipedia article/source notices and FEVER-derived synthetic rows can impose additional obligations. Retain author/publication/licence links with every downstream quote or transcript; no third-party original dataset uploaded to public GitHub.

**Storage truth:** The original complete corpus was in the runner's **temporary** directory and securely released by context manager; a **permanent private Google Drive copy of raw original JSONL is NOT yet established**. The *permanent custody established* here is pinned publisher version + independent SHA check + replayable code + public small receipt, **not private raw byte hosting**. Re-execution can reproducibly fetch originals, but that is conditional on provider retention/network. Drive receipt upload was attempted but blocked by the available upload pathway's safety check, so no Drive copy is claimed. Do not conflate independently verified on-the-fly source bytes with persistent user-held custody.

## 2. Crucial unanticipated full-corpus quality finding: published train/dev/test are NOT fully disjoint by page

Distinct publisher `page` strings normalized by underscore→space, whitespace trimming and Unicode `casefold`. Actual source page counts:

| Split | Distinct page titles |
| --- | ---: |
| train | **22,195** |
| dev | **2,975** |
| test | **3,068** |

Cross-split source page intersections: **train/dev 18; train/test 22; dev/test 2**. The split names alone do **NOT** guarantee source-page isolation. This is a new verified *census fact for this pinned file version*, not proof of benchmark-wide information leakage in a specific pretrained LLM and not a claim that the original authors promised strict page-disjointness. A heldout panel selected from all test rows without source-page exclusion is not defensibly independent at the page/revision family level.

For P75-P2, `test-only pages = 3,045` after exclusion of ALL pages seen in train or dev. Among these, **2,810** pages have at least one author-labeled `real` revision `case_id` with two distinct verification labels under current simple eligibility rule; a full independent expert warrant review is still required. Sample selection stratifies on author-provided contrastive labels, so future inference applies to this contrastive subset, not the unconditional VitaminC test distribution.

## 3. Independent Wikimedia verification and the R1→R2→R3 correction lineage

[Original MediaWiki Revisions API reference](https://www.mediawiki.org/wiki/API:Revisions). Publisher-provided `wiki_revision_id` strings are tested *independently against English Wikipedia's own authoritative revision API*, not assumed valid from the dataset.

**R1 (first pass, superseded):** deterministic SHA commitment `ca3fe32c0a57b24c04cb6676973c36c68cb32ee52ced0d37da5f05dc58b08471` on 12 test-only page-group candidates; 8 newly proposed original revision IDs plus 2 previously visible TRAIN revisions queried. API returned all 10; both TRAIN preview IDs matched article name, but only **5/8** candidate revision IDs matched source article title. **R1 12-candidate selection NOT PROMOTED.**

**R2 (source metadata verification):** Widened deterministically ranked pool to 48 test-only source-page candidates. API returned **50/50 revision metadata records** (48 selected + 2 previously exposed preview), each with independent Wikipedia timestamp/SHA-1/size; **40/48** candidate Wikipedia revision ID→article titles matched, **8/48** did not. Only matching page lineages admitted. The first 12 distinct metadata-confirmed source-page cases were frozen by commitment:
`a481ef8cd3b421ae5e81f242f1035fdbbf48c501cf8f695fa158c103b314759e`.

**R3 (actual historical revision body/diff):** Retrieved original English Wikipedia **WIKITEXT** for **24** R2 title-matched candidate revision IDs **plus their immediate parent revisions (24 more)**. All 24 requested revision bodies and all 24 parent bodies were returned. **24/24** had different actual revision/parent SHA256 fingerprints. The **first 12** source-page-disjoint, title-matched, timestamped, SHA-1-metadata-bearing and parent-diff-positive entries were selected, with *frozen source/revision/parent-content commitment*:

`7d96568480e87aec80ffb8be1d3002d5fb11920ac40a3f9fd5e57a176ac22e78`.

Additional R2 48-pool unverified ordering commitment:
`78196bff133a63c1872566a06f86c6910b0f50efdd1727f938901a6a156ca8d1`.

**Interpretation:** The publisher original data has been byte checked, and the independent authoritative Wikipedia API confirmed real historic revision/parent content change for the 12 selected **page lineages**. This does **not** prove:
- that the particular Wikipedia changed sentence is the one referred to by the VitaminC `claim`/`evidence` field;
- that the label changed truth in the world or entails the claimed proposition;
- that the Wikipedia page content was captured/accessible by an independent historical observer at the claimed time;
- that a dataset label is an independent blind human warrant;
- that these 12 are independently held out from **model pretraining exposure**;
- that a unique `page` title is a perfectly independent source identity under redirects/mergers;
- any randomized intervention or actual `KEEP/SWITCH/REVIEW` policy advantage.

**Unit:** one `page × original-revision lineage × author-case` as one candidate source cluster; all other rows from same page excluded across train/dev. The deterministic source-group commitment is reproducible from public code and original version. **It is a frozen assignment, not a cryptographically secret/independently blinded heldout set**; a genuine sealed identity list for future raters must be held separately by an approved custodian, outside the public repo.

## 4. Verification hierarchy and P75-P3 paper gate

| Requirement | Status |
| --- | --- |
| Published original train/dev/test bytes retrieved and SHA verified | **PASS all 3** |
| License string/link and publisher commit preserved | **PASS** |
| Test page disjoint from entire train and dev in dataset page strings | **PASS for selected 12** |
| Wikimedia revision ID, article title, timestamp and SHA-1 metadata | **PASS for selected 12** |
| Independent actual Wikipedia revision and parent full body hashes differ | **PASS for selected 12** |
| Specific changed evidence span semantically entails/undercuts exact claim | **HOLD** |
| Third-party blinded human minimum sufficient warrant | **0; HOLD** |
| Historical observer's first-available timestamp separately corroborated | **HOLD** |
| Original 255 MB bytes durably saved to user's private Drive | **NOT DONE; provider pinned original remains** |
| Economic utility/legitimate representation switching estimated | **0; HOLD** |
| Novel mechanism beyond VitaminC + temporal PROV + Blackwell/decision baseline | **HOLD** |

The original author's data use `real` and `synthetic` edit types. Selected clusters explicitly require `revision_type=real` and do NOT convert the source license into a legal or truth certificate. Cases span Wikipedia articles, a single provenance ecology; 12 groups are **not 12 independent mechanism families**. This is a source-custody and audit methodology result, **not a new behavioral/causal result**.

## 5. Governance, CI, durable source links
- [P75-P2 source/receipt code](../src/p75_p2_original_dataset_custody.py).
- [Read-only source acquisition workflow](../.github/workflows/p75_p2_original_byte_custody.yml): `permissions: contents: read`, temp files, no external models or participants, Github artifact holds **only public metadata JSON**, not copyrighted original raw data. G-001 author WhoSia only.
- [Publisher original dataset](https://huggingface.co/datasets/tals/vitaminc/tree/be6febb761b0b2807687e61e0b5282e459df2fa0).
- [Wikipedia Revisions API technical contract](https://www.mediawiki.org/wiki/API:Revisions).
- [Version 1 first all-file byte and partial source-ID run](https://github.com/WhoSia/EPISTEME/actions/runs/38346958733) and [R2 metadata candidate counterexample run](https://github.com/WhoSia/EPISTEME/actions/runs/38347153407).
- **Final verified R3 exact-head source CI**: [GitHub Actions #38347299857](https://github.com/WhoSia/EPISTEME/actions/runs/38347299857), SUCCESS 1/1, source SHA `4dbf438c123c9e5ac0af5b5243631bc19250eaf3`.
- **Durable public R3 metadata artifact**: workflow artifact `p75-p2-original-source-public-metadata-only`, ID `11789207974`; 30-day retention on GitHub Actions, not permanent. Store results and checksums in this Markdown court and Notion canonical page, so the proof facts don't disappear with artifact expiry.

**Next disciplined step:** trace each selected dataset `evidence` span to independently archived pre/post Wikipedia article text with a human-readable citation, check edition-time information actually available then, seal full source claim packets in licensed private custody, obtain non-author raters and predeclared costed policy baseline. No further 200 MB model execution is necessary merely to make the current metadata PASS greener. No unauthorized model calls/recruitment.
