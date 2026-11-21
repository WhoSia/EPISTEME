# EPISTEME-P77 W66-B — Reviewer-Requested Baseline, Manuscript Revisions, and Six-Task Unit Audit

**2026-11-22, source-grounded follow-up.** Exact publisher files were acquired by the parallel Work-mode and then six originals were independently downloaded into this Chat's analysis environment, with their SHA-256 bytes matched to the Work admission record. The three manuscript versions and the original Reviewer 2 report/author reply were read in full or at the relevant methodological sections, with key pages rendered and inspected. This supplement does **not** claim author executable-run reproduction or a new scientific-standard adoption effect.

## Original-source chain

| Document | Source | Material observed |
| --- | --- | --- |
| Original manuscript | [Publisher-original PDF archived in Drive](https://drive.google.com/file/d/1HExlxx5ZZzBE4hAUDJPnefJYMQxrOLSY/view) | Original PDF page 7 (journal page 4) explicitly constructs approximate tissue labels using ordered substring rules on original tissue values, and evaluates queries with exact value equality, excluding partial matching/stemming/synonyms. Original PDF SHA-256 `2ebbf60e1dc74c35fa0f7a02237537273c47f3ce74b802a04afddc899e7c6272`. |
| Reviewer 2 initial, dated August 9 2025 | [Report PDF](https://drive.google.com/file/d/1ZWG3gxk8HaoynLhd3ZaLrEF793xbe-5L/view) | Report PDF p. 1 explicitly asks whether the original baseline is disadvantaged by lacking ordinary stemming/linguistic preprocessing and asks how much of the approximate reference labels were manually reviewed. SHA-256 `d6af7d89cd7eec28a3338af0654553f8bffda1b07540ae8cedb5bc40f37b9527`. |
| Original author reply | [Reply PDF](https://drive.google.com/file/d/1WwZnihkaUR4VaqO8m7s1adtyVcF1VrbC/view) | Original reply thanks Reviewer 2 generally; does not include a separately reported normalization-control results table. SHA-256 `5347ed2c11cb85ee5898748fd3031b191bc45fd866df0176ec1118e3b5b1aeb6`. |
| Revision 1 manuscript | [R1 PDF](https://drive.google.com/file/d/17A7BUA2rAEIX6ag_De25KoHjn9zr6tvu/view) | PDF p. 10 says the researchers manually inspected 5% of the heuristic reference and **considered stemming and other cleanup**, but found no effect on final cohort **precision** (not a universal statement about recall or F1). Exact-match search rule retained. SHA-256 `a7f4ce8aa6d4b47e04c3a4e6b82ed1f8669e20629cd75a50e1dce203ccab3912`. |
| Revision 2 manuscript | [R2 PDF](https://drive.google.com/file/d/1vQg-1h7cL65CpAt2UPi3VZRto7FAFFAE/view) | Methodology preserved on PDF pp. 8–9, including 5% manual check and limited statement about precision. Appendix C on PDF pp. 14–16 newly describes a 6-subcohort × 3-method repeated-measures recall analysis (18 observations per repository), with between-subcohort independence assumed. SHA-256 `d8e6f1235e3d187824b1d0ce4d761e55e7908c54b73e95c909a4ea392cfa75e0`. |

**Interpretation of the reviewers and response:** the preprocessing objection was explicitly raised **before publication**. The revised manuscript **did respond substantively in its Methods**, even though the separate original reviewer-response PDF offers only a general acknowledgement. It would be inaccurate to say the authors ignored the issue entirely. However, the revised statement is restricted to **precision** under the authors' tested cleanup methods; W66's simple case-folding changes the particular released ovarian blood query's **recall** and **F1** considerably, while the original source's precision stays 1.0. These observations can coexist. We do not claim to have reproduced exactly what the authors meant by 'stemming and other methods' or their final cohort-level precision calculation.

## Actual observational units behind the six statistical 'sub-cohorts'

The revised Appendix C treats **six sub-cohorts as the repeated-measures subjects**, not six independently rerun model API calls. Hence the older W63 phrase 'six independent runs' is too strong unless separate execution logs exist. This version correction is material.

[Original 800-row six-query task grain audit](../analysis/p77_w66_subcohort_grain_audit.py) and [three synthetic checks](../analysis/test_p77_w66_subcohort_grain_audit.py) compare the three source cohort input pools and their released heuristic reference labels:

| Cancer | Original candidate pool reused in organ/blood queries | Organ relevant-positive rows | Blood relevant-positive rows | Positive-index overlap | Neither relevant |
| --- | ---: | ---: | ---: | ---: | ---: |
| Liver | same 800 | 593 | 20 | 0 | 187 |
| Lung | same 800 | 616 | 64 | 0 | 120 |
| Ovarian | same 800 | 457 | 154 | 0 | 189 |

The **full 800-record candidate pool is reused for two different queries per cancer**, but the selected *positive-labeled subsets* for organ and blood are disjoint. Therefore:
- It is **not** justified to call six independent model runs merely from this six-task structure.
- It is **not** justified to declare Appendix C's independence assumption false solely because the 800-record input pool is shared: positive recall denominators could be non-overlapping.
- It is scientifically necessary to recover the exact per-subcohort **denominator/grain, subject ID, repeated-use rules and covariance structure**, since the published appendix describes recall means over '800 samples' while the per-query positive denominators in the released heuristic labels are e.g. 20 for liver blood and 154 for ovarian blood.
- The released files are neither a complete original execution trace nor an independent label standard. No manuscript ANOVA p-value was recalculated here.

## Falsifiers and research-director decision

The true source-to-invocation-to-query-to-workbook graph (A08) must resolve whether the six subjects were six independently selected data units, six query tasks formed from three shared source populations, or a mixture. Disjointness of positive labels is relevant but cannot answer model execution or shared-run effects. One needs at minimum the original six row-level test-ID sets and the exact 6×3 statistics, including whether the six positive-task cohorts were independently sampled, along with original prompt/model/run ID.

A09 acquisition is closed by Work's 9/9 PDF admission. B10 and B11 remain partial. **Latest missing evidence categories: 18 (F7/A6/B5).** P77 identity REVIEW ACTIVE, standalone BIA causal study PAUSED, P78/PAPER HOLD. Retain W66 normalization and label-dependency findings as bounded Research OS methodology, not a new independent EPISTEME philosophical result.
