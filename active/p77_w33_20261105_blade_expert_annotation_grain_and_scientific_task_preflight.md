# EPISTEME-P77 W33 — Real BLADE Expert Annotation Grain, Source-Grounded H0/H1 Candidate and Oracle Independence

**Date:** 2026-11-05 KST. **Authority:** [binding P77 charter](../STRATEGY_P77_CURRENT.md), [governance](../GOVERNANCE.md). **Status:** Authentic BLADE source annotation inspection PASS; no complete benchmark or AI translation intervention run; independent EPISTEME novelty **NOT CERTIFIED**; P77 ACTIVE / P78+PAPER HOLD.

## 1. Original source identities and exact scope

Live GitHub source fetch from [behavioral-data/BLADE](https://github.com/behavioral-data/BLADE), not a fabricated benchmark:
- [blade_bench/datasets/soccer/info.json](https://github.com/behavioral-data/BLADE/blob/main/blade_bench/datasets/soccer/info.json): actual Git blob `149ca52c0f2a87aa289de2242fdf90b235ccb1c2`. Describes one real observational sports-science research question about player skin tone and red-card assignments, **146,028 player-referee dyad records** in source description, and 27 source fields. The number describes dataset **metadata**, not independently executed data-row read.
- [blade_bench/datasets/soccer/annotations.csv](https://github.com/behavioral-data/BLADE/blob/main/blade_bench/datasets/soccer/annotations.csv): actual Git blob `dfa852591f6b6b347f37a3e3fd531ed1970a402c`, entire CSV text fetched and **actually parsed** as quoted-field multiline CSV in tool-local JS.
- [blade_bench/data/load_annotation.py](https://github.com/behavioral-data/BLADE/blob/main/blade_bench/data/load_annotation.py): actual blob `6cd625058dc1343fcc347b423800d24429c1825c`, source indicates annotations are loaded into a structured ground-truth graph, not simply 'one annotated answer per record'.
- [blade_bench/eval/evaluator.py](https://github.com/behavioral-data/BLADE/blob/main/blade_bench/eval/evaluator.py), blob `bec6136973679a0ae8962a82c03e73130f3a7c50`, evaluator code fetched. Grading depends on conversion, annotations, model and other matcher implementations; no claim of an independent deterministic scientific oracle.
- [pyproject.toml](https://github.com/behavioral-data/BLADE/blob/main/pyproject.toml), blob `c383684195bef7bdf60efbc60f0f1aced6f4e7ee`: BLADE `blade-bench 0.1.1`, Python ^3.10, various LLM client dependencies and scientific numerical libraries. It cannot be assumed compatible with the BixBench Python >=3.12/Docker runtime in the same environment.

## 2. New real original-data annotation measurement

**Full downloaded source `annotations.csv` successfully parsed in JS**, including multiline, escaped quote JSON cells. Structural result:
- **98 annotation specification records, 8 CSV columns.**
- `spec_id`: 98 nonempty.
- `dependency_graph`: 1 nonempty (and valid JSON).
- `conceptual_spec_json`: 16 nonempty, all 16 valid JSON.
- `transform_spec_json`: 40 nonempty, all 40 valid JSON.
- `model_spec_json`: 41 nonempty, all 41 valid JSON.
- Three other `tisane_spec_json`, `annotate_cvar_spec_json`, `annotate_transform_spec_json`: 0 nonempty.
- All 98 rows parsed to exactly 8 fields, and **all 98 are one of the four above mutually nonempty specification types in aggregate**.

**Crucial epistemic grain:** `98` is neither **98 research teams** nor **98 independent scientific hypothesis tests**. One graph plus three kinds of annotated design choices are linked within a *single* BLADE scientific dataset. An expert's annotation is **evidence of an annotated proposal**, not automatically a unique correct causal answer. Treating a match to annotation as a scientifically warranted conclusion would repeat the flawed meta-estimand confusion diagnosed by [Auspurg & Brüderl 2024](https://drive.google.com/file/d/1s95yC7Rkxp52GK1BpiQzdL_00a4FWlFE/view).

Reproducibility tool [analysis/p77_w33_blade_expert_annotation_grain.py](../analysis/p77_w33_blade_expert_annotation_grain.py) committed as a read-only Python source CSV auditor, with explicit expected 98/8/1/16/40/41 checks and fail-closed JSON parsing. A local **synthetic quoted-JSON parser selftest passed**. Actual original GitHub CSV was independently parsed in **tool JS**, not by executing the committed Python script on the original file. Preserve that distinction.

## 3. A candidate pilot scientific target (SOURCE-GROUNDED, not run)

**Question:** Within the original dataset of player/referee repeated dyads, is skin tone associated with red-card decisions under a prespecified population and analysis unit? This is an **observational association**, not proof of racial bias or a causal skin-tone effect.

**Admissible source-level checks** for a future test:
- Preserve data unit as *player-referee dyads*, not unique independent players; record multiple matches per dyad and repeated referee/player dependence.
- Preserve exact outcome/exposure scale, missingness, conditioning, cluster structure and confidence inference.
- Fix the substantive **estimand** and conditioning variables *before* translation; alternate controls may answer different scientific questions rather than change truth of one.
- Select original expert-justified model/transformation(s) from BLADE annotations as **candidate reference**, but require independent audit of their assumptions before designating an oracle.
- Benchmark strong existing **official/deterministic/manual** workflow with equal compute/time/validation budget against a **versioned AI format/analysis converter**. Neither treatment has been implemented here.
- Distinguish confidence interval/p-value equality from validated identification and provenance: agreement of numbers cannot establish causal warrant.

**This is not yet a user data request.** No complete soccer `data.csv` received, no R/Python model rerun, no AI model assigned, and no ethical/participant intervention attempted. User-supplied CRI ZIP and three PNAS original PDFs are already held. Human participant recruitment is not assumed.

## 4. Confounding and fatal rivals

The BLADE scoring mechanism evaluates existing expert choices; it does not by itself supply an oracle of true causal effects or a community choice record. This is a strong **existing technical competitor** to 'AI workflow defensibility benchmark' claims. BixBench similarly has v1.5 version and explicit grader distinctions; a direct schema adapter might be a mundane engineering fix, not a discovery about science.

Historical PNAS primary rivals [Mathur 2023](https://drive.google.com/file/d/1_f5TrM-tonVpl9k7kDswgCHlQ23VBgrA/view), [Engzell 2023](https://drive.google.com/file/d/1VpL2sCk2gRSlKVlrGwzoTm5UWW-DgIxp/view) and [Auspurg–Brüderl 2024](https://drive.google.com/file/d/1s95yC7Rkxp52GK1BpiQzdL_00a4FWlFE/view) prohibit extrapolating variable-choice/annotation dispersion to a common scientific test without estimand alignment. Underlying Farrell–Saloner/Liu/Arthur converter and standard lock-in economics remain already established. **No lab-level longitudinal standards adoption A is present**, hence full TLP `Z->A->T` remains unidentified.

## 5. Explicit director go/no-go

- **PASS:** Original annotated source discovered, byte-indexed via Git SHA, actual CSV record/JSON-structure integrity inspected, real scientific question and data-grain identified.
- **CONDITIONAL GO only for a technical dry-run:** Obtain one licensed `soccer/data.csv` plus original dependent transforms, strong non-AI exact reference, separate Python 3.10 environment, independent domain/evidence reviewer and a controlled AI conversion under equal resources.
- **NO-GO for empirical founding TLP:** No randomized assignment of AI conversion, no observed community standard migration or lock-in, no measured feasible hypothesis-test set, and no novelty over established epistemology/economics.
- **Stop rule:** Do not mistake source annotation matching for real epistemic warrant, or a converter schema-field compatibility fix for scientific-theory novelty. Record any matched experimental failure as conventional workflow/provenance until an independently predicted difference survives strong rivals.

**Next W34:** Source-level deterministic baseline/real dataset feasibility check before any user asks for big dataset download; if no legally and scientifically valid reference task can be fixed, retain NO-GO. P77 ACTIVE / P78+PAPER HOLD.
