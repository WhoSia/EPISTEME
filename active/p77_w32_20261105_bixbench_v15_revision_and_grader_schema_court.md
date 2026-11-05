# EPISTEME-P77 W32 — BixBench v1.5 Source/Grader Contract, Dataset Version Drift and Evaluation NO-GO

**Date:** 2026-11-05 KST; [binding P77 strategy](../STRATEGY_P77_CURRENT.md), [governance](../GOVERNANCE.md).
**Director verdict:** VERSION/SCHEMA RISK CONFIRMED in inspected public interfaces; **a failure in the official agent pipeline NOT proven**; no full agent evaluation, no causal converter or communal-adoption estimate, independent theory novelty NOT CERTIFIED; P77 ACTIVE / P78+PAPER HOLD.
**Source lineage:** [W31 feasibility screen](p77_w31_20261105_authentic_scientific_agent_benchmark_screen_and_adoption_gap.md).

## 1. Tool choice and authentic source receipts

We chose **installed GitHub** for actual code and executable source identity, **installed Hugging Face** for the dataset card (dataset search endpoint disabled, hub_repo_details succeeded), **web** solely to verify the current official public dataset version and 2025 revision announcement, **Python** for a deliberately synthetic interface contract. Google Drive and Notion remain canonical archival and decision surfaces. We did **not** treat a random MCP/LLM "reasoning booster" as independent evidence or a scientific grader.

Original inspected sources:
- Hugging Face dataset [futurehouse/BixBench](https://huggingface.co/datasets/futurehouse/BixBench), dataset viewer advertises **train: 205 rows**, fields including `id`, `version`, `question`, `ideal`, `capsule_uuid`, `hypothesis`, `paper`, `data_folder`, **`eval_mode`**. Dataset size advertised **5.91GB**, mostly source capsules; not acquired into Drive or local scratch.
- Official source announcement (2025-09-23): Original dataset contained many under-specified/open-answer questions; substantial re-review; flattened to **one question per row**; historical version preserved at `v1.0`, updated `main` and `v1.5`. **Published benchmark numbers from different versions are not directly comparable even when file and row units appear similar.**
- [Future-House/BixBench README](https://github.com/Future-House/BixBench/blob/main/README.md) (read directly). 205 questions from 60 real published computational-biology notebooks/capsules; Docker `futurehouse/bixbench:aviary-notebook-env`; Hugging Face authentication described. **README is an overview, not an assurance every corresponding computation is executable with exact scientific meaning**.
- [grade_outputs.py](https://github.com/Future-House/BixBench/blob/main/grade_outputs.py), actual content SHA obtained through GitHub API; its direct CSV grading loop uses `row.get("evaluation_mode", "llm_verifier")` in open-answer mode.
- [bixbench/graders.py](https://github.com/Future-House/BixBench/blob/main/bixbench/graders.py), Git blob `f2e81b05e489e54de5131f700b65e98772cfa0e5`, shows **llm_verifier / str_verifier / range_verifier** and LLM availability requirement.
- [pyproject.toml](https://github.com/Future-House/BixBench/blob/main/pyproject.toml) requires Python **>=3.12**, and git dependency `fhda ...@v1.5.0`. This is distinct from BLADE's separately specified Python 3.10 environment: do **NOT** install both into one unconstrained environment.

## 2. Specific *conditional* interface risk

The public dataset's source field is `eval_mode`; the command-line standalone `grade_outputs.py` expects `evaluation_mode` in each input CSV row. If one directly loads the current dataset metadata **without a mapping**, and passes those rows to this standalone grading CLI, `row.get(..., "llm_verifier")` defaults to a judge-based mode instead of preserving requested `str_verifier` or `range_verifier`.

This is not yet a confirmed bug in the authors' normal workflow: their full harness may map fields properly before invoking the CLI. In particular, `postprocessing.py` uses a separate historical semantics for `eval_mode` that cannot be equated one-to-one without run-path tracing. **A candidate preflight check is not a claim of changed published scores.**

[Executable read-only W32 interface-contract test](../analysis/p77_w32_bixbench_v15_schema_contract.py) was run in the container with **three invented metadata-only cases** (no real benchmark questions/answers):
```
PASS: invented 3-mode cases; naive direct input mismatches in 2 modes
PASS: explicit alias adapter preserves all 3 modes
PASS: missing/invalid/contradictory mode aliases rejected
SCOPE: synthetic schema test; official pipeline not run; no performance result
```

This is an **engineering source compatibility potential failure**; well-known schema contract mismatch, not a new scientific law, not an AI agent evaluation result.

## 3. Genuine scientific-epistemic admissibility and dataset correctness

A grade on a published ideal answer is not automatically a valid scientific **H0/H1 distinguishing observation**. The record must fix: source capsule and notebook version, domain dataset and rights, preprocessing and scientific transformation, hypothesis and measurement scale, independent oracle, external code/environment versions, and named uncertainty; keep deterministic string/range verifiers separate from an LLM judge (the latter cannot be treated as an exact invariant without repeated, blinded validation). The dataset publishes ideal answers; benchmark contamination/leakage is a separate measurement threat to model score validity.

**Against original founding TLP:** BixBench provides a technical task/grade and may support **Z -> task fidelity** under a strong official/manual transformation comparator. It does **not** supply randomized **AI format-converter** assignment or actual **research community standard adoption** (A) and a measured test-feasible-set (T). No complete `Z->A->T` is identified.

## 4. Data gate and next W33

Do **not** ask the user to download all 5.91GB: only a specific licensed small capsule + metadata and runnable deterministic baseline are worth retrieving once the scientific task oracle is fixed. There is no reason to re-download original CRI ZIP or the three already-held PNAS critiques.

**W33** separately tests the alternative BLADE original expert annotation **granularity** and whether a predefined scientific question offers stronger source-grounded transformation checks. **P77 ACTIVE; P78 HOLD; PAPER HOLD; no independent novelty certification.**
