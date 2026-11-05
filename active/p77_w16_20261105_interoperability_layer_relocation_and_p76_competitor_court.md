# EPISTEME-P77 W16 — Interoperability Layer Relocation, Goal-Relative Conversion, and Source-Link Repair

**Date:** 2026-11-05 KST
**Status:** P77 Phase 1 ACTIVE / novelty NOT certified / P78 HOLD / PAPER HOLD
**Authority:** [Current P77 strategic charter](../STRATEGY_P77_CURRENT.md), [Notion official decision](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53), [W15 court](p77_w15_20261105_founder_genealogy_translation_standard_prior_art_court.md).

## 1. Input custody and corrected bibliography

**Verified Drive intake:**
- [Samuele Marro & Philip Torr (2026), *Position: LLM Agents Are the Antidote to Walled Gardens*](https://drive.google.com/file/d/1oj1sQq0CWf_Z93_H0jFclL8DWXtpPOCR/view), *Proceedings of the 43rd International Conference on Machine Learning*, PMLR 306, 249,966-byte original PDF.
- Uploaded file was initially titled `marro26b.pdf` under `00_INTAKE` with file ID `1oj1sQq0CWf_Z93_H0jFclL8DWXtpPOCR`. It was **metadata-renamed and moved** to `10_PAPERS`, **same ID and size read back**. No independent raw-byte SHA-256 computed. This is a **POSITION** paper: its statement is not direct evidence of lowered platform concentration in scientific research.

**Previously broken source URL corrected in W15:**
- Rosero Abad, S., Bekkers, R., and Raiteri, E. (2026), *Open standards, closed standards or vertical integration? Interoperability pathways in markets with network effects*. *Journal of Standardisation* vol. 5. **DOI:** https://doi.org/10.59490/jos.2026.8038; **publisher:** https://journals.open.tudelft.nl/jos/article/view/8038; **institutional repository:** https://research.tue.nl/en/publications/open-standards-closed-standards-or-vertical-integration-interoper/.
- The previously shared ScienceOpen URL was not accessible to the user and did not fetch reliably. **Do not repeat it as a download/canonical page.** Publisher and institutional records directly corroborate identity. The publisher abstract reports four case studies—EVs, game consoles, payment systems, home computers—and finds outcomes conditional on incentives to supply complementary assets. **PDF not yet present in verified Drive intake/collection search; full text not claimed read.**

**Two additional actually-held original documents read in this turn:**
- [Murat Bakeev (2026), *Model Transfer, the Challenge of Tractability Standards, and Methodological Embedding*](https://drive.google.com/file/d/1cV3Q42I9uE5Ek1LpFkNtJuqB9gXc4Tqy/view), *Philosophy of Science*, https://doi.org/10.1017/psa.2026.10259; relevant abstract and sections on hybrid agent-based models in macroeconomics.
- [Robert E. McGrath and NCSA HDF Group (2000), *Transition from HDF4 to HDF5: Notes about Compatibility, Conversion, and Interoperability of HDF and HDF-EOS*](https://drive.google.com/file/d/1lxBHdARPJE5FlrWLocOgAyxO1rT2RCJl/view), dated 2000-09-12. The introduction explicitly defines compatibility relative to *user goals and needs*, rejecting one absolute compatibility criterion.

## 2. A genuinely useful but NON-NOVEL distinction: interoperability's location

Marro & Torr propose that AI agents reduce application/service interoperability cost and thereby weaken incumbent platforms' data walls. Crucially, their own full text (Introduction, position statement, §7 conclusion) **already warns about new agent-framework lock-in** and agent-caused technical debt, silent mapping errors, security vulnerabilities and legal uncertainty. Thus there is no clean antinomy between `AI adapters weaken service lock-in` and `AI adapters strengthen another interface or agent standard`. **The site of lock-in can change.** Calling that observation `layer relocation` is a bookkeeping label, not EPISTEME's novel discovered mechanism.

Rosero Abad et al.'s publisher abstract adds a different condition: open standards require complementary suppliers' incentives; sometimes vertical integration seeds a market while open standards later become advantageous. The detailed four-case evidence is **not evaluated yet**; it cannot be substituted for P77 experiments.

Bakeev (2026) establishes an additional distinct dimension: *syntactic portability of a computational model* does not guarantee acceptability under disciplinary **tractability standards**. Hybrid macroeconomic agent-based models illustrate methodological embedding; this is already a philosophically explicit account, so merely labeling it 'epistemic interoperability' is not a novel argument.

McGrath & NCSA (2000) independently caution that HDF4/HDF5 compatibility is purpose-relative. Format conversions and interfaces have many distinct compatibility senses. A one-field translation discrepancy or metadata alias is not itself evidence that the reachable set of physical scientific tests has shrunk.

## 3. An adversarial four-layer table

| Layer | Actual observable | Existing explanation | Gap before EPISTEME novelty |
|---|---|---|---|
| **Interface** (service/APIs/data format) | adapter coverage, mapping errors, multi-homing effort, task completion | Marro–Torr 2026; McGrath–NCSA 2000 | none identified |
| **Market / coordination** | incumbent share, relative adopter payoffs, complementary supply, agent-layer dependency | Farrell–Saloner 1985, Liu et al. 2011, Rosero Abad et al. 2026 | no established uncaptured mechanism |
| **Method execution** | domain-accepted tractability, computational methods, reproducible execution constraints | Bakeev 2026; scientific software/interoperability practices | not identified |
| **Epistemic test & warrant** | which rival hypotheses can actually be discriminated with feasible data, and under which error/reliability controls | Beauchemin–Staley, Mattig–Stöltzner, Leonelli, MQR | requires real new case, matched rival & warrant measurements |

**Inference restriction:** A change in `interface portability` does not imply a change in `scientific discriminability`. Neither market concentration, profitability, nor a successful conversion certifies a new inferential route. Conversely failure of a converter need not imply an actual lost hypothesis test if alternative pipelines remain available.

## 4. Two-source W16 head-to-head: Bakeev vs P76

- Bakeev's macroeconomic model transfer: **different local validity/tractability norms** produce a challenge even when model syntax persists; representational restructuring can render methods acceptable. This **already provides philosophical causal language** for a research group's practical adoption decisions.
- P76 NeXus/HDF4/HDF5: earlier EPISTEME found source-pair representation and alias discrepancies, but the prior evidence never established changed physics or lost hypothesis discrimination. McGrath–NCSA's 2000 guide already describes goal-relative incompatibility. Its difference is an implementation provenance issue, not yet a philosophical extension.
- **Conclusion:** two apparent positive source pairs are **explained or plausibly covered by prior art** on present receipts. There is no valid basis for promoting P77 to P78 from either example.

## 5. Test design without fabricated scientific novelty

For any future field-specific trial, independently specify:
(1) target hypotheses H0 and H1, (2) measurement data and intervention, (3) source and target technical formats, (4) converter's semantic error profile and validation rules, (5) executable instrument/computation budget, (6) discipline's acceptable inferential controls, and (7) alternative existing routes.
A converter-induced change in ability to discriminate H0 from H1 must survive a **strong baseline**: manually validated conversion, explicit schema mapping, or the best existing practical method under matched resources. If it does not, record a bounded engineering effect, not a new epistemic mechanism.

**No field experiment was conducted in W16**; no novel physical result, no real multi-user adoption statistics, and no newly established causal law.

## 6. Corrective tasks and current next step

- **W15 source link fixed:** replace unreliable ScienceOpen reference with TU Delft OPEN official journal page, DOI, and TU/e cross-check; preserve original mistaken reference in provenance note.
- **W16 intake:** Marro & Torr full PDF is now **HELD**, moved into `10_PAPERS`, remove from missing-Drive table.
- **W17 next:** adjudicate *testability* rather than general interoperability in a deliberately narrow, source-backed domain. Before any experiment, identify H0/H1, claimed discriminating observable, strongest accepted comparator, and actual source data; otherwise retain P77 phase 1 reading.
- **Outstanding missing PDFs:** Rosero Abad et al. (2026) DOI 10.59490/jos.2026.8038, Janssen et al. (2026) DOI 10.1002/adem.71258 (targeted title search not found; no global absence claim). CERN 2000 decision minutes remain nonpriority historical debt (not essential to W17).

**Custody:** Notion semantic authority; GitHub human-authored science notes; Drive original PDFs. No github-actions[bot] commits. No paper/P78 promotion.
