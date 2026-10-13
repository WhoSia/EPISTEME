# EPISTEME-P75-P4 — Label-Blind Source-Relative Warrant Adjudication and Three Failed-Alignment Repairs

**Date:** 2026-10-13 KST · **Parent:** formally OPEN EPISTEME-P75, no P76. **Study stage:** 12 original VitaminC test-only article/revision families, frozen by P75-P2 SHA-256 `7d96568480e87aec80ffb8be1d3002d5fb11920ac40a3f9fd5e57a176ac22e78`. **Author of case judgments:** ChatGPT assistant manually reviewed historical original source/excerpts *without publisher reference labels*, NOT a human panel, independent third-party study, new LLM paid run, independently verified Wikipedia truth, or general theorem. Do not confuse code checking author's semantic categories with external scientific validation.

[Reproducible encrypted original packet generator](../src/p75_p3_claim_revision_alignment.py) · [P4 case-attack logic](../src/p75_p4_source_relative_warrant_court.py) · [source lineage and original SHA court](p75_p2_original_byte_wikimedia_holdout_court.md) · [publisher original](https://huggingface.co/datasets/tals/vitaminc/tree/be6febb761b0b2807687e61e0b5282e459df2fa0) · [author's license](https://github.com/TalSchuster/VitaminC/blob/master/DATA_LICENSE).

## 0. Actual evidence acquisition and secure review

Before analytical judgment, read-only GitHub Actions verified the publisher's pinned full original train/dev/test JSONL file SHA as in P75-P2, reconstructed **the exact same twelve heldout source page/revision families**, fetched from English Wikipedia the real before and after historical Wikitext, and generated 12 nonpublic packets (same claim, contrastive publisher evidence, old/new Wikipedia source excerpts and diff hunks) without dataset label values. The G-001 workflow generated a *temporary* private ZIP, encrypted it using OpenSSL CMS enveloped encryption and a **public-only RSA recipient certificate**, erased raw private packets from the runner, and published **ciphertext only**. The recipient private key remained in ChatGPT's current working container, never posted on GitHub, Drive, runner or issue. Ciphertext was fetched to the private local runtime and decrypted; all 12 files were actually read. The public JSON contains only **masked group IDs, reviewer-written paraphrase and status codes**, not licensed claim/evidence or source excerpts. The encrypted original artifact expires; the code and this judgment summary persist.

**Privacy and capability caveat:** This is an independent *reading of the dataset's hidden publisher label*, but it is **not independent external human research adjudication** because the assistant authored the explanations. Nor does encrypting copyrighted material remove attribution/share-alike obligations; licensed source packets remain private. Read-only GitHub bot never commits/pushes or authors research.

## 1. The necessary three-valued distinction

For a precise claim `c`, temporal/evidentiary scope `t`, full source document `S_t`, and candidate source-witness set `W`, separate three claims:

1. **Byte/text source match:** a dataset excerpt or edit is present or changes in the historical Wikitext (source diff). This is a documentary property, not independently justified world truth.
2. **Source-relative sufficiency:** `W ⊨_{S_t,scope} c` given explicit referent, quantifier and date. For source-relative *minimal* sufficiency require `W\{w} ⊭ c` for every essential atom `w`, and examine alternative proof sets and nonmonotone entailment. One sentence being an apparent candidate does **not** establish minimality for the full Wikipedia document.
3. **Legitimate/independent warrant and action:** a competent outside source/reviewer adjudicates provenance credibility and cross-version effect, and a costed decision rule compares KEEP/SWITCH/REVIEW to credible bitemporal PROV, information-structure and decision-theoretic baselines. None exists at P75-P4.

An early proof of string change never upgrades silently into a proof of qualified world fact or into a warranted representation switch.

## 2. All 12 source families: author/assistant label-blind attack table

Original licensed excerpts live in the encrypted private packet, not in this public paper. **Identifiers below are masked source-group IDs**, not automatically blind gold.

| No. | Group prefix | Original claim focus (short independently written paraphrase) | Direct source-relative finding | Status |
| --- | --- | --- | --- | --- |
| 1 | 807b1886 | Razorlight guitarist | Original-vs-revision differs at first live show membership, but a *first concert roster* does not establish unqualified present tense **plays in the group**. Founder/current temporal scope unresolved. | `HISTORICAL_SCOPE_HOLD` |
| 2 | 04415cdd | Austin as second-most populous state capital | Updated lead explicitly asserts second after Phoenix; before text does not. **One source sentence as candidate** for frozen article-version evidence. Does not authenticate census truth globally. | `ONE_SENTENCE_WITNESS_CANDIDATE` |
| 3 | 60ce362d | Historical classification of Pythagoras as mathematician | Wikitext lead did add `[[mathematician]]`; the SAME historical line contained an editorial warning disputing this attribution and advising editors not to add it. **This is directly observed source-internal contest**, not a certified new historical fact. | `MARKUP_REPAIRED_EDITOR_OBJECTION_HOLD` |
| 4 | 16cb1aa7 | Macau among top two for density | Historical source rank changed to place Macau and Monaco above Singapore. The original claim says **locations**, while the source discusses country-level ranking; relevant universe/date unclear. | `CITATION_REPAIRED_QUANTIFIER_SCOPE_HOLD` |
| 5 | ac936220 | Syrian refugees' subjective comfort in Somalia | Newly inserted healthcare/business/settlement sentence is verifiably present, but asserting a new home was **suitable** does not show subjective **comfort** or independent external source truth. | `INSERTION_REPAIRED_SEMANTIC_GAP_HOLD` |
| 6 | c080d9bb | Animal-rights organizations' concern with pet-keeping | Revised source explicitly names organizations as agents of concern; previous version had a grammatically incomplete source relation. **One source sentence as candidate**, without generalizing to all such organizations or treating Wiki as authority beyond text. | `ONE_SENTENCE_WITNESS_CANDIDATE` |
| 7 | 875083b8 | Chart peak after Leonard Cohen's death | Revised album page mentions a later peak, but **'Cohen's album'** is an underspecified referent and chart market/date require disambiguation; 2008 vs 2016 chart snapshots cannot be collapsed. | `ALBUM_REFERENT_SCOPE_HOLD` |
| 8 | 6f00e272 | PV battery systems as flexible power | Edited source speaks of competition from **PV coupled to battery storage**, not unambiguously batteries as the energy source; semantic source-to-claim substitution is indirect. | `ENERGY_TECH_REFERENT_HOLD` |
| 9 | fe5c5fcd | Maximum Overdrive reviews | Revised article uses an apparently favorable word alongside the same low **18%** approval figure; wording is at least pragmatically self-inconsistent and cannot be blindly promoted to better warrant. | `SOURCE_INTERNAL_CONSISTENCY_HOLD` |
| 10 | 3595446c | Victorious follows Tori Vega's adventures | Adding a single word about 'adventures' leaves essentially the same narrative referent as the prior sentence. **Strong negative control: textual change without a defensible warrant switch.** | `SEMANTIC_WARRANT_UNCHANGED_CONTROL` |
| 11 | b0a3fb87 | Relation between a person and a discovery in a truck | Syntactic reordering preserves almost the same event information; neither phrasing entails that the named person **left** the other there. **No premise sufficiency.** | `REORDERING_NOT_WARRANT_FOR_ACTION` |
| 12 | 21f2025f | Marceline's nickname | The updated introductory excerpt removes a nickname, but the original and revised page retain the nickname in the infobox. **A lost snippet is not a lost full-page warrant.** | `FULL_PAGE_WARRANT_PERSISTS_CONTROL` |

**Count:** 2/12 author-*provisional* one-sentence source-relative witness candidates, 10/12 categories of contextual, evidentiary, source-credibility or unchanged-warrant HOLD/control. **Actual independently human-approved minimally sufficient proof sets: 0/12.** These statuses are neither a conventional empirical accuracy rate nor a measured contrastive verification model result. Cases were purposively selected from a contrastive author-labeled dataset, and the assistant's judgments may themselves be contestable.

## 3. Actual repairs for P3's three original source-text alignment misses

Previous P3 reported 9 directional exact text matches, 1 partial and 2 missing. Direct original Wikitext review distinguishes the text-alignment failures:

- **#3 Pythagoras:** Original sentence sits deep behind nested Wiki phonetic/citation templates and a long line including comments; sentence splitter chose an unrelated paragraph. Found actual `[[mathematician]]` edit by comparing old/new source lead. **Text-referent link repaired; editorial objection means epistemic warrant HOLD.**
- **#4 Macau/Singapore:** Publisher evidence is flattened with mixed URL/citation fragments, whereas the source wikitext includes wiki links `[[Macau]]` and `[[Monaco]]` inside the actual population-density ranking change. Read the correctly isolated edited line. **Ranked-source relation recovered; 'locations' universe and temporal data validity HOLD.**
- **#5 Syrian refugees:** Publisher evidence blends a newly inserted settlement/healthcare sentence into a longer unrelated news paragraph; exact sentence matching failed. Original source edit does add the settlement claim. **Document insertion recovered; 'suitable' ≠ 'comfortable' and no independent factual authority, hence semantic gap HOLD.**

These are **document-link recovery**, not proof that all three claims are supported. The old P3 **9/1/2 strict-normalized-text matching numbers remain historically intact**; R4 records a separate richer Wikitext-line location tier and does not rewrite past failed measurements.

## 4. Research consequences and the P75 challenge

The source-level observations are significant negative controls against naive studies that judge a representation switch by an added token, a changed dataset label, or a temporal-provenance-valid source URI:

- **Strongest falsifier (Marceline):** a phrase is deleted from one passage while the decisive witness remains accessible elsewhere in the original article. A short-answer evidence projection can appear to lose ground truth while the original document retains it.
- **Distinct countermodel (Victorious):** added wording that does not change basic entailment.
- **Source authority conflict (Pythagoras):** updated source publication is not a warrant certificate, particularly when page-internal editor warning explicitly contests the inserted proposition.
- **Quantifier/temporal leakage (Razorlight, Macau, Cohen):** a claim's referent/scope can shift while matching excerpts remain mechanically verifiable.

This reinforces inherited **P18 matched witness recovery**, **P69 output-contract correctness vs grounded warrant**, **P70 full-vs-projected omitted QA**, **P74 equal-capability conventional temporal+PROV rival**, and original VitC's published contrastive-edit method. Neither tuple/mask/Wikitext diff nor these examples alone is a newly proven general representation theorem. Prior original research directly motivates need for controlled human, not more self-referential toy PASS counts.

## 5. Next necessary independent-world task

Request an ethically consented **external, independent human source reviewer panel** only after private licensed packets are held by an outside custodian. Predeclare one exact claim/time/source-cutoff for each retained case and distinguish the ***decision to keep/replace an answer*** from ***changing the source evidence presentation***. Give raters both the old/new source edition and citations; hide dataset author labels, output-contract assignment, reference judgment and the present assistant audit status. Compare against competent temporal SQL/PROV + Blackwell/minimax/standard decision baseline, not publication-only strawman. For ambiguous and unaligned cases, present them as HOLD/falsification probes, not favorable treatment examples.

**Governance:** new paid hosted-model calls=0, real external human adjudications=0, actual costed KEEP/SWITCH/REVIEW outcomes=0, new claims of independent semantic gold=0, real institutional intervention=0. Original raw source texts and reviewer-level claims remain outside public GitHub. Public summary includes independent *analysis from hidden dataset labels*, not independent participant testimony.

**CI:** P75-P4 masked semantic-source court and P75-P3 linked real-source original SHA/revision packet reconstruction via G-001 read-only workflow [run #38349937973](https://github.com/WhoSia/EPISTEME/actions/runs/38349937973) SUCCESS 1/1 job, original code HEAD `f5ae7ee18110be722d7934ad1420faf260e5e875`; final document-integrated CI must confirm exact newer HEAD after canonical patch.
