# EPISTEME P77 W3 — Five Newly Acquired Papers: Canonicalization, Reading Court, and Epistemic Measurement

Date: 2026-11-04 (KST). Scope: five first-page bibliographic verifications, source-text section review; not an independent statistical reproduction. Distinguish reported outcomes from our observations.

## Custody / moves
Four newly uploaded PDFs in Research OS `00_INTAKE` were source-identified, renamed and moved to `10_PAPERS` via Drive with successful parent readback:
1. Yucheng Wang et al. (2026), The Illusion of What If: Evaluating the Breakdown of Counterfactual Reasoning in LLMs, Findings EMNLP 17106–17129; drive 1xNFjjFDTSC6eGrrdjgUVYQ5vHpWa-6go.
2. Raia Abu Ahmad et al. (2026), Does Finetuning with Scientific Data Increase Hallucinations? A Multi-domain Factuality Evaluation of LLMs, EMNLP 14040–14064; drive 1i4ixh7qtP6_igsCHW5NaeQn1MilHXrv7.
3. Hantian Zhang & Wentai Wu (2026), Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention Calibration in Retrieval-Augmented Generation, Computer Materials & Continua doi:10.32604/cmc.2026.086343; drive 15sWpgBjLzS9LMUThPA7iI54UKtnrm21O.
4. Yang Liu & Chenhui Chu (2026), Understanding the Prompt Sensitivity, ACL 44362–44388; drive 1ql_Oaag_0IbjojZk_B6-3TVYFnrZePr_.
Fifth file: Ruiyang Qin et al. (2026), Evaluating and Explaining Prompt Sensitivity of LLMs Using Interactions, ICML PMLR 306, drive 1Z8c292JoDteom1HRYPP7N6meV6ENAe77. Another copy with preprint label already at 10_PAPERS: 1HK-iuEjv7Hv6qBaDN3xf5uDnBoXqPle1. Sizes 8,245,543 versus 8,206,204 bytes; no hash comparison; new file RENAMED `DUPLICATE CANDIDATE — ... — BYTE CHECK HOLD.pdf` and left in 00_INTAKE, no deletion.

## Reading court (results quoted/reported by authors, not independently verified)
### Wang et al. WhatIfBench / PRISM
220 open-form counterfactual questions: 113 STEM, 79 HSS, 28 hybrid; semantic causal graph derived *from generated explanation*, process metric plus rubric metric; six models, best composite 64.62% in study. Failure types include causal gap, premise drift, fragmented graph, missing mechanism. Section Limitations explicitly says PRISM is NOT ground-truth causal oracle; semantic graph is response-derived, so structural consistency is not real-world causal truth. P77 cannot claim an evaluative causal graph itself proves scientific counterfactual correctness.

### Abu Ahmad et al. SciFactCheck
2500 prompts, 5 domains, 18 LLMs (various scientific fine-tunes plus bases), three separable classes: unverifiability, overclaiming, attribution. Reports fine-tuned models often degraded factual reliability and can be linguistically more assertive even when less internally confident. Authors' limitations: overclaiming auto proxy not validated as full measure; CiteVal checks whether citations exist, NOT whether they support proposition; evidence retrieval source authority limited; expert consensus on check-worthy statements contested. EPISTEME 'scientific warrant' metric not simply cite accuracy or confidence.

### Zhang & Wu ESB
200 seed QA examples (SQuAD/HotpotQA) × five evidence states × three prompts; seven LLMs and approx. 29,400 model calls incl L5 order randomization. Conflict L5 provokes 65–91% over-answer in authors' setup, despite higher abstention on absent L4; important conflict/absence dissociation. Weakness: general-domain seeded tests; string-match answer, explicit refusal phrases, not independent multi-expert annotations; authors say L5 auto vs human 75% agreement. P77 should not assume conflict always warrants abstention: if one source has independently established authority it may warrant selecting the stronger claim.

### Qin et al. IPS
Output-score interaction decomposition, reveals interaction shifts even when outputs unchanged. Study of 50 open-source LLMs; factors reducing IPS in authors' design: fine-tuning, model size, dense models, few-shot prompting; primarily stabilizing low-order interactions. Strong prior art against superficial novelty in prompt-interaction explanations. Mechanism refers to analytical interaction representation, not independent evidence of causal internal circuit without intervention. ICML file vs arXiv preprint requires actual SHA/pdf-version verification before deduplication.

### Liu & Chu first-order logit bound
First-order Taylor expansion of next-token log-probability w.r.t. hidden state; Cauchy–Schwarz yields a bound on sensitivity, with reported strong association with PromptSensiScore. 12 templates over 500 items per selected datasets, models mainly small/medium open-weight series. Templates appear more influential than question content for considered logits. Authors restrict conclusion to single next-token coordinate and first-order approximation; broad full-sequence behavior not proved and loose upper bound alone need not identify mechanism.

## Cross-paper pressure and potential residue
- Narrative causal coherence vs real-world warranted causal inference remain different constructs (Wang).
- Confidence/citations vs evidence warrant are not interchangeable (Abu Ahmad).
- Evidence absence vs conflict create different calibration failures; correct handling must condition on independently established evidence authority rather than always abstain (Zhang & Wu).
- Output invariance does not imply interaction invariance (Qin), whereas next-token derivative bounds are not sequence-level causal explanations (Liu & Chu).
- Mere conjunction is not new. Potential Harvest seed: **authority-calibrated evidence-conflict adjudication** with independently witnessed source hierarchy and an evaluator-error sensitivity court. Existing evidence ranking, provenance, Bayesian updates and selective prediction are direct rivals. Novelty HOLD. Avoid overextending user project P76 into a new 'warrant' general theory.

## Next gate
Compare raw EPISTEME P59–P65 original scores with independent human adjudication and evaluate model/evaluator misclassification separately, using existing author-acknowledged limitations. No P78 / manuscript / mechanism claim until directly measured advantage vs strong baselines. Preserve 00 duplicate on HOLD until byte/provenance checks.
