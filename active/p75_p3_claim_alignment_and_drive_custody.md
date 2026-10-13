# EPISTEME-P75-P3 — Twelve Actual Claim-to-Revision Evidence Pairs, Private Warrant Packets and Drive Source Custody Gate

**Date:** 2026-10-13 KST. **Status:** P75-P3 within formally OPEN P75. This is a real source-byte and Wikipedia-revision *textual alignment* experiment, not human semantic adjudication, identification of causal switching value or a new formal theorem.

## 1. Original corpus and sealed predecessor

Original publisher-authored [VitaminC dataset](https://huggingface.co/datasets/tals/vitaminc/tree/be6febb761b0b2807687e61e0b5282e459df2fa0), SHA-256 independently verified for all **488,904 rows, 255,552,326 bytes** in P75-P2 [source corpus court](p75_p2_original_byte_wikimedia_holdout_court.md). [Publisher DATA_LICENSE](https://github.com/TalSchuster/VitaminC/blob/master/DATA_LICENSE): Wikipedia Copyright Policy / CC BY-SA 3.0 as applicable and synthetic FEVER-related terms.

**We did not change the P75-P2 source cohort after seeing outcome.** Reconstructed 12 original source-article × real Wikipedia revision × case lineages from original publisher TEST, excluding every article title present in TRAIN or DEV. Frozen deterministic P75-P2 R3 commitment:
`7d96568480e87aec80ffb8be1d3002d5fb11920ac40a3f9fd5e57a176ac22e78`.
The actual original Wikipedia revision and direct parent WIKITEXT independently retrieved from Wikimedia API; original raw text not stored in public GitHub. All 12 original VitaminC case groups were recovered and claim text/evidence was accessible inside the licensed ephemeral GitHub Actions runner.

## 2. Original-claim evidence-to-source sentence alignment: actual results

[Exact original-source packet compiler](../src/p75_p3_claim_revision_alignment.py) performs:
1. source original 3/3 SHA revalidation;
2. deterministic identical 12 cohort reconstruction;
3. original Wikipedia oldid/parent exact WIKITEXT retrieval, chronological source role, original revision text SHA;
4. intra-case search for two **same exact normalized claim** rows with different author dataset reference labels and different evidence;
5. normalization of actual source text and publisher evidence excerpts, **exact normalized evidence string containment** in Wikipedia parent and edited WIKITEXT;
6. independent reviewer candidate source passage fingerprints, link, masked case ID, evidence trace and source/proof role; no leak of publisher reference label in assessor packet;
7. qualified textual candidates distinguish from semantic warranted minimal-sufficiency.

**Primary fixed 12-group evidence alignment:**
- **9/12 DIRECTIONAL_EXACT_CANDIDATE:** One dataset evidence string occurs in predecessor source and **not** edited source; the other occurs in edited source and **not** predecessor. Because literal source text strings can appear in a semantic context that reverses their meaning, this is a **strong source-string custody gate**, still **NOT a truth/entailment certificate**.
- **1/12 PARTIAL_AMBIGUOUS_HOLD:** Some evidence appears in source, but the pair is not cleanly old-only/new-only; in observed case one evidence span appears both periods while the other is unmatched.
- **2/12 SOURCE_TEXT_ALIGNMENT_HOLD:** Publisher evidence samples cannot be directly found in either source version by current normalized string containment, despite independent Wikipedia revision+parent bodies being retrieved. Could reflect data preprocessing, templates, redirects, a more distant revision, or wrong revision linkage. Need manual original-page proof tracing.
- **12/12** groups contain ≥1 pair of actual identical publisher claim with different author-labelled verdict/evidence. This measures dataset row structure, NOT demonstrated semantic disagreement.
- **0/12** independently blind human warranted source mappings; **0** real policy outcomes. The packet compiler fails closed on wrong cohort commitment and false source-page identity. Never silently replace a HOLD group to inflate eligible count.

**The 9/1/2 distribution is an exact local sample property at this frozen version, not an estimate of VitaminC population accuracy.** Word normalization can falsely align distinct contexts; source text SHA is not claim evidence certification.

### 2.1 Actual 12 record admission ledger (identities masked for rater independence)

| Frozen index | Masked claim/source group | Literal source text classification | Human rating admission |
| --- | --- | --- | --- |
| 01 | `807b1886e82f34ff39af8951` | directional | CANDIDATE — must independently certify semantic warrant |
| 02 | `04415cddaa0f24660e56038f` | directional | CANDIDATE |
| 03 | `60ce362da48b5f8c4164a699` | none | **HOLD** |
| 04 | `16cb1aa738cd4e5fc52df4a4` | none | **HOLD** |
| 05 | `ac936220605a71347b30b911` | partial/ambiguous | **HOLD** |
| 06 | `c080d9bb45f2fdbce439d460` | directional | CANDIDATE |
| 07 | `875083b8a795b3c226e3f35a` | directional | CANDIDATE |
| 08 | `6f00e2727be2c84b2be7096f` | directional | CANDIDATE |
| 09 | `fe5c5fcdc171b66f4e7088e7` | directional | CANDIDATE |
| 10 | `3595446cfbddbf4d1e678dd1` | directional | CANDIDATE |
| 11 | `b0a3fb876843ac918b796717` | directional | CANDIDATE |
| 12 | `21f2025f0cb3b331b2e33c0e` | directional | CANDIDATE |

The direct source strings are restricted to **licensed local private packets** when the user or licensed custodian explicitly runs:
```bash
python3 src/p75_p3_claim_revision_alignment.py --acquire \
    --public-dir local/p75_p3_public \
    --private-dir local/p75_p3_private
```
One **actual VitaminC claim + historical pre/post source candidate packet** per frozen group, 12 files. Original text and query results were generated and tested transiently by the CI runner then deleted, not uploaded to public GitHub. Full reviewer assignment conditions and source-argument minimum-set validity need a third-party custodian; a bare packet author Boolean is never an independent witness.

**Portable masked reviewer artifacts** generated alongside chat:
- 24 reviewer-form skeletons (12 groups × FULL and MATCHED_PROJECTED), **without raw licensed source text**, plus 48 hypothetical rater slots (two per view per group, real raters **zero**).
- Masked receipt and source SHA fingerprints, attribution and as-of time/referent tasks.
- The 9 textual candidate groups' FULL and PROJECTED **review versions cannot yet be certified as exactly matched P18-style positive controls until an independent custodian confirms witness retention in actual full/projection trace and relation maps**. Never equate a source verbatim match to minimally sufficient/necessary proof.

## 3. Proposed external-human independent minimum warrant review

**No participant recruitment has occurred.** For each technically eligible group, custodian should privately preserve original cited article's historical page and preceding revision with actual strings and source licence attribution; reviewer should not see publisher label or editorial packet author's prechosen verdict.

- independently assess 3-way support/refute/NEI for the *same statement at both source times*;
- independently identify evidence atom set(s) actually sufficient; test each atom removal for necessity and report alternative minimal sets;
- check referent, publication availability, entity/time semantics, negative and decoy controls, P18 traced witness in BOTH retained source trace and relationship map;
- preregister policy cost for KEEP/SWITCH/REVIEW and compare with strong SQL valid/system time + PROV + decision-theoretic baseline, not a weak naive latest-document index.
- multiple distinct minimal sets and non-monotone inference require full subset checks or a clearly scoped monotonicity assumption; a single greedy removal is not generally a proof.

**Actual observed human trials remain 0** and P69 0/16, P70 0/16, P71 0/32 intact.

## 4. Google Drive permanent original-corpus preservation — actual write blocker and precise manual remedy

This remains a material custody HOLD, not solved by storing a public metadata JSON. Attempts through the **connected Google Drive upload tool** to transmit a small metadata-only ZIP file were blocked by a service safety gate; now even a **tiny new native Google Doc creation** in the verified EPISTEME Drive destination **and in My Drive root** was blocked. Therefore this is **NOT evidence of a 256-MB size ceiling**. Repeatedly changing file size will not fix the current tool-level safety failure; we did not bypass the gate, invent uploads or change sharing.

Requested original raw files are *individually below 256 MB*, even before compression, so user can manually preserve each in their verified private EPISTEME folder:
[Drive EPISTEME folder](https://drive.google.com/drive/folders/1X7veUdKK1PIbnUM2wN5SOzaDbuE_QWJm).

- [Pinned train.jsonl](https://huggingface.co/datasets/tals/vitaminc/resolve/be6febb761b0b2807687e61e0b5282e459df2fa0/train.jsonl): **193,958,244 B**, SHA `7461c6fd1a13459590317c5ccdc8651dd2daf7c1ad8ae4b10ccd88d164fccd5a`.
- [Pinned dev.jsonl](https://huggingface.co/datasets/tals/vitaminc/resolve/be6febb761b0b2807687e61e0b5282e459df2fa0/dev.jsonl): **32,876,983 B**, SHA `544934677f5d133873e6d38f4557f8966f4efa5d3d70874ffe6913f2091b86b5`.
- [Pinned test.jsonl](https://huggingface.co/datasets/tals/vitaminc/resolve/be6febb761b0b2807687e61e0b5282e459df2fa0/test.jsonl): **28,717,099 B**, SHA `7ad1808dbc30c62e0a1427a53022d0dfaff668a1fde3c4b612a2d266edd753ad`.

**Ask user to download+upload all three separately into the existing private folder and report completion**. They can verify `sha256sum train.jsonl dev.jsonl test.jsonl` locally. Original PDF [Schuster et al. NAACL 2021](https://aclanthology.org/2021.naacl-main.52.pdf) can be filed separately under canonical 10_PAPERS after duplicate/title audit. Existing metadata-only ZIP and reproduction manifest are included as downloadable chat artifacts and can also be uploaded manually (much smaller than originals).

The old 255MB source corpus resided only in an ephemeral Actions runner and was deleted. The 12 private reviewer JSON packets were likewise assembled transiently and deleted after schema/gate checks. They are **reconstructible** by the code but not yet durably transferred to private Drive. No human/copyright/actual utility claim promoted.

## 5. Permanent GitHub/Notion source of truth

- [Original-P3 real corpus/claim alignment source](../src/p75_p3_claim_revision_alignment.py)
- [Read-only G001 Actions workflow](../.github/workflows/p75_p3_claim_alignment.yml)
- [P75-P2 12-source provenance court](p75_p2_original_byte_wikimedia_holdout_court.md)
- [P75-P1 human-warrant and utility protocol](p75_p1_vitaminc_warrant_switch_protocol.md)
- **P75-P3 exact latest HEAD CI** must be verified after canonical documentation writes. Source code passes need not be retested as model-generalization or human results.

**Next P75-P4 meaningful science:** obtain private permanent original corpus custody, externally validate the 9 actual source/claim semantic pairs, resolve 3 ambiguous/missing mappings without ex-post cohort substitution, and only then independent blind reviewer and costed switching-value experiment. Kill if strongest standard temporal-PROV + rational policy explains all effects. Do not run paid provider calls or recruit humans without explicit authorization.
