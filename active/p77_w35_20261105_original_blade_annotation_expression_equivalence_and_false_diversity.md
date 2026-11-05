# EPISTEME-P77 W35 — Source-Authentic BLADE Expert Annotation Equivalence and Method-Diversity False Positives

**Date:** 2026-11-05 KST. **Authority:** [P77 founding charter](../STRATEGY_P77_CURRENT.md), [governance](../GOVERNANCE.md). **Research status:** P77 ACTIVE / P78 HOLD / PAPER HOLD; independent EPISTEME novelty NOT CERTIFIED.
**Predecessors:** [W33 original expert-grain court](p77_w33_20261105_blade_expert_annotation_grain_and_scientific_task_preflight.md), [W34 real original fish source audit](p77_w34_20261105_real_blade_fish_source_estimands_and_poisson_baseline.md).

## 1. Source-driven audit (actually read, no invented 'expert decisions')

The original [behavioral-data/BLADE fish annotations.csv](https://github.com/behavioral-data/BLADE/blob/6118fa8d5007b91aa8c91c518182db82446a4547/blade_bench/datasets/fish/annotations.csv) was fetched through live GitHub and **all its 65 records/8 columns parsed in the connector JS runtime**, including quoted JSON fields:
- 1 dependency graph, 6 conceptual specifications, 13 transformation specifications, 10 model specifications, 4 conceptual-variable annotations, 31 transformation annotations.
- `fish_per_hour`: `df['fish_caught_per_hour'] = df['fish_caught']/df['hours']`.
- `group_size`: `df['group_size'] = df['persons'] + df['child']`.
- `fish_per_hour_person`: `df['fish_caught_per_hour_per_person'] = df['fish_caught']/(df['hours'] * df['group_size'])`.
- `fish_per_hour_per_total_people`: `df['fish_caught_per_hour_per_total_people'] = df['fish_caught_per_hour']/df['group_size']`.

These are source-annotated different **code expressions**, not necessarily different **scientifically relevant analysis procedures**. Source [fish/info.json](https://github.com/behavioral-data/BLADE/blob/6118fa8d5007b91aa8c91c518182db82446a4547/blade_bench/datasets/fish/info.json) explicitly defines `persons` as number of **adults** and `child` as children. Thus `persons + child` is a natural head count; `hours` is **time spent in the park**, not verified actual angling time.

## 2. Executed authentic numerical comparison on all original source rows

Define for every real visit i with fish F_i, hours H_i>0 and head count P_i>0:

`A_i = F_i / (H_i * P_i)` versus `B_i = (F_i / H_i) / P_i`.

In exact real arithmetic, `A_i = B_i`. Both expressions represent the *same visit-level per-person park-hour rate*, not two independently established fishing processes. **All 250 actual GitHub original observations were computed in connector JS** with both expressions:
- **0/250** differ above absolute tolerance `1e-12`.
- **18/250** produce bitwise-unequal IEEE floating-point outputs due only to evaluation order.
- Maximum absolute difference **1.7763568394002505e-15**.
- Source expert annotation contains a separate `remove_outliers` rule filtering `fish_caught_per_hour < 50`, which **actually excludes exactly 1 of 250** real visits. Aggregate original fish per park-hour `0.5964552894` versus `0.5864185465` after selection. This trimming changes the *population/analysis set*, unlike the algebraically identical A and B expressions. Removing a row is a valid decision only with prespecified outlier criteria and relevant scientific justification.

[Executable source-pinned numerical-equivalence auditor](../analysis/p77_w35_fish_expression_equivalence.py) committed. Its synthetic selftest was executed in local Python; the exact 250-source-row evaluation was executed independently in GitHub-connected JS. No AI agent translated source during this audit and no original rows were redistributed.

## 3. Why this matters and why it does NOT establish novelty

**Counting code differences is not counting distinct testable scientific hypotheses.** Conversely, identical program output across two paths doesn't prove independent measurement/provenance or causal correctness. Original BLADE metadata, expert annotation and valid deterministic algebra already explain this source case. It is a new concrete **EPISTEME audit artifact on real source data**, not a new theorem of science. The precision changes are standard floating-point evaluation effects and fit existing software equivalence/provenance theory.

Distinguish three levels:
1. **Syntactic diversity:** different expression trees or variable names.
2. **Numerical/semantically valid transformations:** equal numbers within an explicit tolerance, with the same units and input cohort.
3. **Scientific admissibility:** whether the transformed variables still support an actual, independently justified H0/H1 under the same population, sampling, measurement assumptions, validation resources and alternative trusted routes.

W35 passes the **second** only for two specific arithmetic expressions and their original BLADE source definitions, and exposes one sample-selecting outlier rule. It does NOT automatically pass the third. A versioned AI adapter may fail elsewhere, but **no AI treatment and no community standard adoption events were observed here**.

## 4. Strong adversarial models and outcome

[Engzell 2023 original](https://drive.google.com/file/d/1VpL2sCk2gRSlKVlrGwzoTm5UWW-DgIxp/view), [Auspurg–Brüderl 2024 original](https://drive.google.com/file/d/1s95yC7Rkxp52GK1BpiQzdL_00a4FWlFE/view) and [Mathur et al. 2023 original](https://drive.google.com/file/d/1_f5TrM-tonVpl9k7kDswgCHlQ23VBgrA/view) continue to constrain the relation between distinct estimands, technical transformations and actual evidence. Existing network-standards/economic theories, measurement and data-provenance work cover the generic possibility of incompatible translations. **No independent residual predicted over these rivals.**

## 5. Stop rule / next scientific target

W34 and W35 establish a real-source technical baseline with genuine input bytes, source code, annotated scientific decisions and independent deterministic calculations. **The founding causal question requires entirely different missing observations:** an assigned AI converter Z, credible equal-budget best non-AI baseline, interactive lab/community standard choice A and independently adjudicated scientific H0/H1 test availability T. Current BLADE fish source provides none of that network adoption evidence. Do not escalate into a paper on arithmetic parenthesization or a synthetic 'new epistemic law'.

**Verdict: W35 source expression validity check PASS; full EPISTEME TLP causal evidence NO-GO; P77 ACTIVE / P78 HOLD / PAPER HOLD; independent novelty NOT CERTIFIED.**
