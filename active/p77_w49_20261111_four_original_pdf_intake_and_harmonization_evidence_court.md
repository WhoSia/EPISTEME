# EPISTEME-P77 W49 — Four Newly Held Originals, AI Metadata Evidence-Granularity Court and Reproducibility Boundaries

**Date:** 2026-11-11 KST. **Authority:** [P77 binding strategy](../STRATEGY_P77_CURRENT.md), [W48 source screening](p77_w48_20261111_authentic_ai_metadata_harmonization_and_joint_causal_identification_court.md), Research OS literature naming/custody doctrine. **Status:** P77 ACTIVE / P78 HOLD / PAPER HOLD / independent novelty NOT CERTIFIED.

## 1. Actual four primary PDFs read from user Drive, bibliographic authority and byte custody

The four items surfaced as uploaded **real original PDF objects** in `00_INTAKE — Literature Radar` (not inferred from a web link). The Drive text extraction was inspected for full article/report structure, methods, results, limitations, references and relevant tables. After matching exact DOI/title/author with sources and checking file metadata, each original **same file ID** was metadata-renamed and moved (not copied, not raw-byte rewritten), then id/name/parent/size independently re-read:

| Primary original | Verified PDF size | Canonical file ID | Destination | Role |
|---|---:|---|---|---|
| Long et al. (2026), *A new AI assisted approach aligns data standards and accelerates interoperability in biomedical research*, npj Digital Medicine 9:733, DOI 10.1038/s41746-026-02795-z | 1,286,800 B | [1GOTrIJOycsrSR7wE9qmFkvnbF8pV7nOy](https://drive.google.com/file/d/1GOTrIJOycsrSR7wE9qmFkvnbF8pV7nOy/view) | 10_PAPERS | Original peer-reviewed paper |
| Ostropolets et al. (2026), *Real-World Use of Controlled Terminologies, Ontologies, and Vocabularies for Evidence Generation Across a Large International Observational Network*, JMIR Medical Informatics 14:e92727, DOI 10.2196/92727 | 928,185 B | [1a8ttaIhIm9NZVBZX1qToJHYFOpudQsYe](https://drive.google.com/file/d/1a8ttaIhIm9NZVBZX1qToJHYFOpudQsYe/view) | 10_PAPERS | Original peer-reviewed paper |
| Sundaram, Gonçalves & Musen (2026), *Toward total recall: Enhancing data FAIRness through AI-driven metadata standardization*, GigaScience 15:giag019, DOI 10.1093/gigascience/giag019 | 2,172,989 B | [1yB1uCs70TCO64tBzzuF7ziKoGEfC7k2M](https://drive.google.com/file/d/1yB1uCs70TCO64tBzzuF7ziKoGEfC7k2M/view) | 10_PAPERS | Original peer-reviewed paper |
| Sheridan, Schneider & Klein (**December 2025**, not 2026), *AI-Ready Data Pilot Project Report*, PNNL-38797, DOI 10.2172/3020608 | 364,364 B | [1it5BE3OFpeGLnetFg1CjQ9LoRtbL4mSe](https://drive.google.com/file/d/1it5BE3OFpeGLnetFg1CjQ9LoRtbL4mSe/view) | 20_NON_PAPER_SOURCES | Technical report, explicitly NOT journal paper |

**Fixity scope:** source Drive IDs, reported byte sizes and resulting parent IDs verified. The raw bytes were not programmatically hashed before/after; no SHA-256 continuity claim. Provider PDF main text was read; linked supplementary articles, underlying code/data/medical source files were NOT downloaded/re-executed in W49. Original source PDF corpus should not be duplicated into lab-local Github.

## 2. Long 2026 — detailed original analysis and unresolved arithmetic

GPT-4-0613 + expert auditing and Elasticsearch built CDEs from 31 inputs, Table 1 shows **42,379 objects** in aggregate; explicitly describes external ADNI/GP2 headers left out of repository construction. The article's `94.0%` is *metadata-field no-manual-revision weighted audit rate*, not scientific accuracy, file-pair interoperability success, independent gold-standard truth, or the fraction of novel ambiguous records correctly standardized. Study distinguishes **83.8% source-unweighted semi-structured no-edit rate** from overall 85.9% source-unweighted, and sources include 84.6% established coding systems where extant names and controlled values simplify review. Highest reported auditing throughput >4000 CDE/week applies best-case structured sources; ambiguous sparse sources ~1500/week; paper refers to conventional manual ~400/week, but **not a randomized/equal-cost head-to-head direct platform comparison**.

**Externally untrained held-out source matching, Table 2:** GP2 421 headers, 29.4% confirmed matches; ADNI Merge 116, 12.1%; ADNI MoCA 56, 17.8%; ADNI ADSXLIST 41, 34.1%; clinical free-text chief complaints 27,660 unique terms, 4.4% matched; an ICD subset 13,425 codes, 48.9% matched. Table 3 reports GP2 composite interoperability 46.8, ADNI Merge 55.3, MoCA 61.2, ADSXLIST 51.8. Abstract reports 32.4% of unseen headers matched, whereas Results state 25.8% for external headers. **Different denominator or reporting basis is unresolved** and must not be silently collapsed into one performance estimate.

**Repeatability is not general scientific test warrant:** a separate 25 randomly selected CDE re-generation analysis gave descriptions only 46.7% ± 11.4% semantically equivalent across runs; complete four-component equivalence 29.3%; names 76.0% ± 9.7%, titles 69.3% ±10.5%, permissible values 65.3% ±10.8%. The paper states no formal inter-rater reliability statistic (e.g. Cohen's kappa) for expert revisions. It explicitly acknowledges **absence of direct quantitative comparison with alternative harmonization platforms**, names OHDSI Usagi and semantic mapping rivals as different tasks. Public code is cited at [datatecnica/GenCDE](https://github.com/datatecnica/GenCDE), but code was not run in W49.

**Numerical integrity open issue (not corrected by invention):** Table 1's 31 row totals add to 42,379. In separate Results prose the subcounts 35,853 established + 6,508 semi-structured add to **42,361**, **18 fewer** than Table 1. This may reflect classification/subset conventions or a publication inconsistency; without supplementary/author derivation do NOT call it fraud, assume the missing 18's category, or silently rewrite source counts. Confirm denominator and field-weight formula before any new calculation.

## 3. Ostropolets 2026 — source of network context, NOT converter effect

2026 publication reports a **six-month 2023 OHDSI landscape assessment**: survey covered 144 institutions, terminology-use information 60 data sources, detailed code-use info only 22; these denominators are distinct. Of 89 terminologies used, 61 were used in fewer than 10% of data sources; 95 of 742,337 codes were present in all assessed sources. Data source-level heterogeneity remains even with a common referential standard. Survey design, code-source selection and chronology do not allocate AI translators, establish pre/post standards migration effects, or independently score fixed H0/H1 test validity. Actual vocabulary exposure and code diversity are not equivalent to community lock-in. Original survey questionnaire and tables are in *Multimedia Appendix 1* (DOCX) and are not yet separately held/checked. Versioning/rights constraints remain methodological rivals.

## 4. Sundaram et al. 2026 — stronger source-backed negative control and real measured effects

The original journal article compares raw metadata baseline, GPT-4 + data dictionary (LLM+DD), and GPT-4 + CEDAR template (LLM+CEDAR) for retrieval over BioSample and GEO. Reported overall recall rises from 17.65% raw baseline to 62.87% GPT-4+CEDAR (not a scientific hypothesis confirmation rate); two-source pooled comparison can mask heterogeneity. The reference labels are *heuristically constructed* using tissue string rules, with 5% manually inspected — this is a measured retrieval proxy, not an independently blind validated scientific-truth oracle.

**Crucial Appendix C full-read:** BioSample repeated-measures ANOVA F(2,10)=27.68, p=0.0001; Friedman ~9.48, p=.0087; Holm-adjusted comparisons baseline vs GPT-4+CEDAR .007 and DD vs CEDAR .007, baseline vs DD .887. For **GEO** repeated-measures F≈1.08, p=.439 and Friedman ~4.59, p=.10: **NO statistically significant overall method difference** (six sub-cohorts). Do not promote the pooled headline into a statistically supported universal gain on each source. Open-source repo cited [musen-lab/FAIRMetadataCuration](https://github.com/musen-lab/FAIRMetadataCuration); Zenodo underlying data cited in manuscript, but not downloaded/rerun here. This paper supports a domain-specific *metadata discovery* capability, but not demonstrated changes in scientific standards adoption or warrant.

## 5. Sheridan et al. 2025 — real expert validity and task-execution concerns

The report is dated **December 2025** on its cover (corrects W48's erroneous '2026 report' shorthand). Three data scientists, three public CSV datasets, eight hours for all three, followed by 60–90 minute interviews. Small convenience sample and tabular-only scope make it a qualitative AI-readiness/stewardship comparator rather than an AI treatment. Interview findings emphasize human comprehension of source measurements, units, documentation, missingness and trustworthy provenance. The final checklist and their *Red Flags* are prospective guidance; not a validated standardized score and not evidence of lab-wide TLP causal effect.

## 6. Adversarial causal/novelty ruling

- **Z (versioned AI adapter + strong non-AI matched counterfactual):** observed GPT-4 uses and comparator designs in Long/Sundaram, but **no equal-cost, identical-goal, multi-path scientifically validated adapter intervention**; Long explicitly lacks direct platform benchmark.
- **A (individual and collective standard switching):** 2023 institutional heterogeneity from Ostropolets, but no linked individual-to-collective longitudinal standard choice as a consequence of a specified AI adapter.
- **T (scientifically warranted H0/H1 test affordances):** retrieval recall, header mapping, expert field revision and AI-ready usability are **not** independent warrant of an actual experimental hypothesis test, with raw alternatives/permissions/budget accounted for.
- **Rivals:** information retrieval + FAIR metadata standards + established ontology/curation practices, standard-choice economics (Farrell–Saloner/Arthur/Liu), resource allocation, and MQR measurement validation. Stronger genuine experimental metadata retrieval literature exists. No standalone EPISTEME explanatory residual demonstrated.
- **Gates:** A founding continuity PASS; B prior art adverse/PASS-for-research, C independent explanandum FAIL-to-certify, D matched fatal comparator incomplete, E real sources PASS but full causal evidence FAIL, F MQR distinctness unresolved. **No promotion.**

**W49 director conclusion:** New actual source PDF originals and a genuine within-science retrieval improvement were read and admitted; technical effect is scientifically meaningful *at retrieval level* and should not be dismissed. However no demonstrated Z→A→T effect exists here. Scientific work should next focus on source-verified **same-task non-AI vs AI gold-oracle, independent domain-test**, rather than inventing general lock-in metrics or expanding cross-sectional indices. No new actual experiment, Python reproduction, treatment assignment, source code execution, or byte hash computed in W49.

## 7. Missing companion originals / data, after removal of four arrived PDFs

| Priority | Outstanding source | Custody status |
|---|---|---|
| P1 | Long et al. (2026) Supplementary Information / source lists & prompting templates | Publisher supplement URL discovered; Drive exact companion not verified; attempted publisher attachment fetch yielded cache miss. |
| P1 | Long et al. actual reproducible GenCDE input set, code version and CDE auditing protocol | Public code and some sources linked; no source-fixed raw outcome bundle verified |
| P1 | Sundaram et al. (2026) Zenodo exact data/reference labels and pinned code revision | Main PDF held; supporting data not yet downloaded/verified |
| P2 | Ostropolets et al. (2026) Multimedia Appendix 1 (DOCX) and detailed per-source anonymized code matrix | Main PDF held; separate appendix not yet admitted |
| P2 | Sundaram et al. peer-review/revision supporting PDFs in publisher Supplementary Data | Publisher lists multiple reports and versions; not held/verified; methodological dispute worth source-reading |
| P2 | PNNL report's 3 original public CSV datasets (DOIs listed in Methods) and anonymized interview transcripts if released | Main report held; dataset bytes not re-executed; no evidence transcripts accessible |

**Current outcome:** P77 ACTIVE / P78 HOLD / PAPER HOLD / novelty NOT CERTIFIED. No additional main-PDF re-upload needed for these four.
