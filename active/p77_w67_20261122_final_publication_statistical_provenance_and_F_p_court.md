# EPISTEME-P77 W67 — Statistical Subject Identity, Three-Contrast Sphericity and Final-Publication F/p Arithmetic Court

**2026-11-22 KST.** Scientific semantic authority: [Notion current evidence ledger](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385). **Status: P77 identity REVIEW ACTIVE, standalone S-BIAD602 causal case PAUSED, P78/PAPER HOLD; 18 missing evidence categories (F7/A6/B5).** A09 (9/9 review/manuscript PDF packets) has already been acquired. A08 author-run statistical subject membership and row-to-output-to-workbook graph remain unresolved. This is an **original-source internal-consistency and partial artifact audit**, not a rerun of the paper's unarchived ANOVA or a causal EPISTEME hypothesis test.

## Original sources and visual cross-check

1. [Sundaram et al. (2026), final OUP/GigaScience article, DOI 10.1093/gigascience/giag019](https://academic.oup.com/gigascience/article/doi/10.1093/gigascience/giag019/8504119), published March 3, 2026 and corrected/typeset April 24. In Data Description it states **800 input records per cancer × 3 cancers per repository**, i.e. **2,400 BioSample and 2,400 GEO**. Its main Statistical Analysis says **six independent experimental runs, each aggregating about 2,400 predictions**, while its Appendix C says **six subcohorts × 800 underlying source samples, with no overlap between subcohorts**, for *each* of BioSample and GEO. The two distinct meanings of "run" and "subcohort" are not connected by a publicly evidenced identity map.
2. [Publisher-preserved revision-2 manuscript](https://drive.google.com/file/d/1vQg-1h7cL65CpAt2UPi3VZRto7FAFFAE/view), SHA-256 \`d8e6f1235e3d187824b1d0ce4d761e55e7908c54b73e95c909a4ea392cfa75e0\`. Its Appendix C GEO Table 9 and body were checked both as extracted text **and as a rendered original PDF page 16** (also duplicated as page 31 in the manuscript bundle); it visibly prints **df (2,10), F≈1.08, p=0.439**. This same triplet appears in the **final OUP publication**, so it is not merely a prepublication typesetting artifact.
3. [Actual Zenodo v2/v3 source Data.zip](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view), 3,992,768 B, SHA-256 \`bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c\`, read and CRC-checked locally, *without* executing any original model notebooks.
4. The 2025 [original Reviewer 2](https://drive.google.com/file/d/1ZWG3gxk8HaoynLhd3ZaLrEF793xbe-5L/view) and [R1/R2 versions](https://drive.google.com/file/d/17A7BUA2rAEIX6ag_De25KoHjn9zr6tvu/view) were already compared in W66-B. Reviewer 2 raised baseline normalization concerns; authors added a 5%-manual-check description and retained deliberate exact matching. W67 does **not** claim this concern originated here.

## Court 1 — six disjoint 800-source subjects against an archive of 2,400

The final paper's Appendix C asserts that **6** subcohorts in **each database** consist of **800** input samples and share **no underlying samples**. Taken literally as subcohorts selected **only from the published 2,400 records per repository**, this would require **6 × 800 = 4,800 distinct input records** in *that one repository*. A union of 6 disjoint sets of size 800 cannot be drawn from a population of only 2,400 records; there must be **at least 2,400 repeated memberships** if every subcohort is selected from that original pool.

The original archived BioSample release itself contains three files of 800 source records (liver, lung, ovarian). We canonicalized only each row's original \`BioSample\` JSON object by sorted-key JSON serialization and counted:

| Archived cohort | Input positions | Distinct original JSON objects |
| --- | ---: | ---: |
| Liver | 800 | 752 |
| Lung | 800 | 780 |
| Ovarian | 800 | 777 |
| Combined | **2,400** | **2,309** |

There are **91 repeated canonical JSON objects** across 2,400 archived rows (all repeated values within their respective cancer cohort; no exact canonical object overlaps between cancer cohorts). *These are not verified biological or accession-distinct subjects*: one biological sample can have multiple representations, and identical records need not prove a subject identity. The sample-count discrepancy **does not prove authors' actual independent runs were reused or flawed**: a separate unarchived source population, reruns with different predictions, alternate subcohort definitions or an imprecise written description could explain it. No original six by 800 subject-ID manifests or 6×3 statistic input was found. W66-B additionally showed that organ and blood queries reuse each cancer's 800-candidate pool but have **disjoint positive-label subsets**; reused candidates alone cannot diagnose statistical *positive-subset* independence.

**Required discriminant:** For BioSample and GEO independently, obtain six distinct \`subcohort_id\` values, each member's stable source record/accession, 800-member assignment, paired baseline/DD/CEDAR predictions, the actual per-query positive denominator, and exact six paired recall triples. Also require the independent run identifiers described in the main Methods and clarify whether these coincide with the Appendix's subcohort IDs.

## Court 2 — three-condition sphericity has three difference variances

For three paired conditions baseline B, dictionary D and CEDAR C, sphericity requires:

\`Var(D-B) = Var(C-B) = Var(C-D)\`.

The paper compares only \`d1=D-B\` and \`d2=C-B\`, calling them "independent difference scores." They share the same baseline B and are paired within each statistical subject, so their covariance cannot **automatically** be set to zero. Algebraically,

\`Var(C-D) = Var(d2) + Var(d1) - 2 Cov(d1,d2)\`.

The BioSample appendix gives \`Var(d1) ≈ 0.013\`, \`Var(d2) ≈ 0.080\`, and its variance ratio is \`0.080/0.013 ≈ 6.1538\`. Without the actual paired covariance, Cauchy–Schwarz only bounds the third sample variance to approximately **[0.028502, 0.157498]**; it cannot identify its value. A two-sample independent-variance F test yielding the manuscript's approximate \`p≈0.07\` is not justified merely by these paired difference-score summaries. The true authors' six-by-three data may or may not satisfy a properly tested sphericity assumption; we **cannot** assert a corrected significance test result.

[Pairwise algebra and covariance estimator](../analysis/p77_w67_sphericity_court.py), [6 synthetic tests](../analysis/test_p77_w67_sphericity_court.py) include counterexamples where the first two variance estimates are identical, but the third is either **0** or **4×** the first; hence equality of only two is insufficient.

## Court 3 — verify published GEO F(2,10) vs p numerical identity

The final published article's GEO Appendix C Table C5 and narrative give **F≈1.08**, **df=(2,10)**, **p=0.439**. For a standard F distribution with numerator df 2 and denominator df 10, the survival probability has a closed form,

\`Pr(F_{2,10}≥f) = (10/(10+2f))^5\`.

Thus **F=1.08 implies p≈0.3761249347**, not 0.439. Even allowing for the printed F rounded to two decimal places, \`f∈[1.075,1.085]\` gives **p∈[0.374582,0.377675]**, disjoint from the printed three-decimal \`0.439\` interval \`[0.4385,0.4395]\`. Conversely, under F(2,10), p=0.439 implies F≈**0.894909**. The identical values in the final publication establish a genuine **reported-number mismatch**, though alternative unpublished software/model adjustments cannot be excluded without the code and data. **Both 0.376 and 0.439 are above 0.05, so this correction alone does not change the non-significant GEO conclusion.**

**Negative control:** BioSample Table C3 gives F(2,10)=27.68, p=0.0001. Its recomputed p≈**0.00008384** is *consistent when BOTH printed F and p rounding intervals are applied* (p rounded to four decimal places). The first W67 synthetic test erroneously demanded literal equality of p=0.0001 to the F-tail across the F-only rounding band; it **failed and was corrected** by modelling each printed statistic's own display precision. Corrected source/test now pass 18/18 local tests. This prevents a false-positive allegation against BioSample.

[Pure-stdlib exact F(2,ν) audit](../analysis/p77_w67_anova_numeric_court.py), [5 synthetic regression tests](../analysis/test_p77_w67_anova_numeric_court.py) check inverse tails, rounding intervals, failure cases and the unchanged significance conclusion. This does **not** reproduce an author model fit, residuals, Friedman inputs, Holm procedure or original ANOVA results.

## Computational receipt and research decision

- [Original ZIP grain auditor](../analysis/p77_w67_subject_grain_court.py), [7 original parser/math tests](../analysis/test_p77_w67_subject_grain_court.py).
- [Sphericity audit](../analysis/p77_w67_sphericity_court.py) and [6 tests](../analysis/test_p77_w67_sphericity_court.py).
- [Reported F-tail audit](../analysis/p77_w67_anova_numeric_court.py) and [5 tests](../analysis/test_p77_w67_anova_numeric_court.py).
- [Machine-readable original-source and arithmetic receipt](../analysis/p77_w67_original_source_and_anova_arithmetic_receipt.json).
- **18/18 local tests pass**, actual Zenodo SHA/CRC and source grain audits run successfully. The final article's HTML was directly checked; the exact GEO statistics were independently inspected on a rendered original PDF page. No GitHub Actions tests or author's unarchived 6×3 ANOVA data rerun is claimed.

**Adversarially bounded finding:** The 2026 final paper has one strictly confirmable *displayed* F/p arithmetic mismatch (GEO), one conditional sample-grain nonidentifiability (6×800 vs 2,400 publicly described inputs), and a mathematically incomplete, paired-covariance-dependent sphericity check. These are genuine **scientific reproducibility/audit results**, not sufficient grounds to declare the overall paper false. Importantly, none identifies the independent **AI transformation → scientific-community standard adoption → feasibility of rival H0/H1 testing** pathway that defines EPISTEME's prospective original contribution.

**Priority:** A08 original 6×3 per-repository recall matrix, stable 800-member subcohort lists and actual independent execution IDs; after obtaining it, rerun the original ANOVA/Friedman/Holm and covariance-aware sphericity procedures. Keep A09 closed, B10/B11 partial, F01/F02/F05 unresolved. **P77 REVIEW ACTIVE, S-BIAD602 PAUSED, P78/PAPER HOLD, current missing 18 (F7/A6/B5).**