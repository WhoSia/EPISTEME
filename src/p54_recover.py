from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

import p53_cross_task as p53

STAGE = "EPISTEME-P54"
P53_RUN_ID = 36977540899
P53_RECEIPT_SHA256 = "3b5ad9e09476c8d4a3d0871f3ba3fb8d687e69d3c0ca825b241cf50bc2952e13"
EXPECTED_FAILED_ROWS = 441
MODELS = ("gemini", "gptoss120")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def frozen_source_fingerprints() -> dict[str, str]:
    names = (
        "active/p53_manifest.json",
        "src/p53_cross_task.py",
        "src/p44_field.py",
        "src/p42_reopen.py",
        "src/p48_seed_fingerprints.py",
        "src/p51_sufficiency.py",
        "src/p52_allocation.py",
        "active/p51_sufficiency_baseline.json",
    )
    return {name: sha256(Path(name)) for name in names}


def check_source_contract() -> None:
    expected = {
        "active/p53_manifest.json": "d2cbd47ef4e6643b5faa6d48bcb8c8263462d76f788e8d54412bef26c269fbfc",
        "src/p53_cross_task.py": "8fd10fe533b235ccfc8a1775cedbc69b0038010e9bc08112a212489dd0349363",
        "src/p44_field.py": "4cbd295b57532fa43e1883626bbaa555cf59ebc47cc83041b8ffd70264dc0f31",
        "src/p42_reopen.py": "745c42c5b571d761ba5ad3c56f8d6da8affcefd381cae97b9489361b884e76de",
        "src/p48_seed_fingerprints.py": "43e80e74b7be749e60b529bdf1b0a10d757590f56842d9a46ddb9740b86c5926",
        "src/p51_sufficiency.py": "bbaf2e159f884aae1d449e2a395782037558f92466672b668342db090c242c31",
        "src/p52_allocation.py": "2dcf639631efb32d47366bf851f6a2afc3db168e7117b3468e67d2574fb6164f",
        "active/p51_sufficiency_baseline.json": "1ab01edb1bd38fc20b1ac4fd7a90a21938ca785ec5ba3f34404718db6ca2dd28",
    }
    observed = frozen_source_fingerprints()
    if observed != expected:
        mismatches = {k: {"expected": expected[k], "observed": observed.get(k)} for k in expected if observed.get(k) != expected[k]}
        raise RuntimeError(f"P53 source fingerprint mismatch: {mismatches}")


def row_identity(row: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(row.get(name) for name in (
        "model", "task", "draw", "cell_index", "vertex", "vertex_index",
        "alias", "alias_index", "semantic", "semantic_index", "gemini_seed",
        "position", "pair_rank",
    ))


def expected_schedule() -> dict[tuple[Any, ...], dict[str, Any]]:
    jobs = {}
    for model, task, draw, draw_index, position, pair_rank, cell in p53.schedule():
        seed = p53.GEMINI_SEEDS[draw_index] if model == "gemini" else 5300 + draw
        expected = {
            **cell,
            "model": model,
            "task": task,
            "draw": draw,
            "gemini_seed": seed if model == "gemini" else None,
            "position": position,
            "pair_rank": pair_rank,
        }
        identity = row_identity(expected)
        if identity in jobs:
            raise RuntimeError(f"duplicate P53 schedule identity: {identity}")
        jobs[identity] = expected
    if len(jobs) != 12288:
        raise RuntimeError(f"unexpected P53 schedule size: {len(jobs)}")
    return jobs


def load_and_validate_receipt(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not path.is_file():
        raise RuntimeError(f"missing P53 artifact receipt: {path}")
    observed_sha = sha256(path)
    if observed_sha != P53_RECEIPT_SHA256:
        raise RuntimeError(f"P53 artifact receipt SHA-256 mismatch: {observed_sha}")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("stage") != "EPISTEME-P53" or receipt.get("constitutional_verdict") != "TECHNICAL_HOLD":
        raise RuntimeError("P53 artifact is not the sealed technical-hold receipt")
    rows = receipt.get("raw_rows")
    if not isinstance(rows, list) or len(rows) != 12288:
        raise RuntimeError(f"P53 raw row count mismatch: {len(rows) if isinstance(rows, list) else 'missing'}")
    expected = expected_schedule()
    seen = set()
    for row in rows:
        identity = row_identity(row)
        if identity not in expected:
            raise RuntimeError(f"row outside frozen P53 schedule: {identity}")
        if identity in seen:
            raise RuntimeError(f"duplicate row in P53 receipt: {identity}")
        seen.add(identity)
        if row.get("status") not in {"OK", "TECHNICAL_FAIL"}:
            raise RuntimeError(f"unknown P53 row status: {row.get('status')}")
    if seen != set(expected):
        raise RuntimeError(f"P53 schedule coverage mismatch: absent={len(set(expected)-seen)}")
    failures = [r for r in rows if r["status"] != "OK"]
    actual_counts = {m: sum(r["model"] == m for r in rows) for m in MODELS}
    if actual_counts != {"gemini": 6144, "gptoss120": 6144}:
        raise RuntimeError(f"P53 per-model denominator mismatch: {actual_counts}")
    if len(failures) != EXPECTED_FAILED_ROWS:
        raise RuntimeError(f"P53 failure-row count mismatch: {len(failures)}")
    technical = receipt.get("technical", {})
    if technical.get("gemini", {}).get("ok") != 5729 or technical.get("gptoss120", {}).get("ok") != 6118:
        raise RuntimeError("P53 technical totals differ from the frozen receipt inventory")
    return receipt, failures


def replay_failures(failures: list[dict[str, Any]]) -> tuple[dict[tuple[Any, ...], dict[str, Any]], Counter]:
    replayed = {}
    statuses = Counter()
    for index, prior in enumerate(failures, 1):
        identity = row_identity(prior)
        packet = p53.packet(prior["task"], prior["vertex"], prior["semantic"], prior["alias"])
        seed = prior["gemini_seed"] if prior["model"] == "gemini" else 5300 + prior["draw"]
        started = time.perf_counter_ns()
        try:
            output = p53.call(prior["model"], packet, seed)
            primary = p53.correct(output, prior["semantic"])
            shadow = p53.shadow_correct(output, prior["semantic"])
            status, error = "OK", None
        except Exception as exc:  # preserve one bounded recovery attempt per failed original row
            primary = shadow = None
            status = "TECHNICAL_FAIL"
            error = type(exc).__name__ + ":" + str(exc)[:300]
        replayed[identity] = {
            **prior,
            "p54_replay_attempts": 1,
            "p54_replay_latency_ms": (time.perf_counter_ns() - started) / 1e6,
            "p54_replay_status": status,
            "p54_replay_primary_correct": primary,
            "p54_replay_shadow_correct": shadow,
            "p54_replay_error": error,
        }
        statuses[(prior["model"], status)] += 1
        if index % 25 == 0:
            print(f"P54 failed-row replay progress: {index}/{len(failures)}", flush=True)
    if len(replayed) != len(failures):
        raise RuntimeError("not every distinct P53 failed row received exactly one P54 attempt")
    return replayed, statuses


def merge_rows(prior_rows: list[dict[str, Any]], replayed: dict[tuple[Any, ...], dict[str, Any]]) -> list[dict[str, Any]]:
    merged = []
    for row in prior_rows:
        replacement = replayed.get(row_identity(row))
        if replacement is None:
            merged.append(row)
        elif replacement["p54_replay_status"] == "OK":
            merged.append({
                **row,
                "status": "OK",
                "primary_correct": replacement["p54_replay_primary_correct"],
                "shadow_correct": replacement["p54_replay_shadow_correct"],
                "error": None,
                "p54_recovered": True,
                "p54_replay_attempts": 1,
            })
        else:
            merged.append({
                **row,
                "p54_recovered": False,
                "p54_replay_attempts": 1,
                "p54_replay_status": "TECHNICAL_FAIL",
                "p54_replay_error": replacement["p54_replay_error"],
            })
    return merged


def technical(rows: list[dict[str, Any]], model: str) -> dict[str, Any]:
    selected = [r for r in rows if r["model"] == model]
    ok = sum(r["status"] == "OK" for r in selected)
    disagreements = sum(r["status"] == "OK" and r["primary_correct"] != r["shadow_correct"] for r in selected)
    return {
        "ok": ok,
        "total": len(selected),
        "complete": ok == 6144,
        "shadow_disagreement_rate": disagreements / ok if ok else None,
        "p54_recovered": sum(r.get("p54_recovered") is True for r in selected),
        "remaining_failed": len(selected) - ok,
    }


def analyze_complete(rows: list[dict[str, Any]], source_receipt_sha256: str, replay_summary: dict[str, Any]) -> dict[str, Any]:
    baseline = json.loads(Path("active/p51_sufficiency_baseline.json").read_text(encoding="utf-8"))
    historical = np.asarray(baseline["mean_tau"]["gemini"]["0.5"], float)
    matrices = {model: {task: p53.jmatrix(rows, model, task) for task in p53.TASKS} for model in MODELS}
    if any(np.isnan(matrices[m][t]).any() for m in MODELS for t in p53.TASKS):
        raise RuntimeError("complete technical receipt still yielded missing task×vertex outcomes")
    taus = {m: {t: p53.tau_vec(matrices[m][t]) for t in p53.TASKS} for m in MODELS}
    gemini_tests = p53.primary_tests(taus["gemini"], historical)
    gemini_holm = p53.holm(gemini_tests)
    full = all(
        gemini_tests[key]["statistic"] is not None
        and gemini_tests[key]["statistic"] > 0
        and gemini_holm["rejected"][key]
        for key in gemini_tests
    )
    historical_passes = sum(
        gemini_holm["rejected"][f"historical:{task}"]
        and gemini_tests[f"historical:{task}"]["statistic"] > 0
        for task in p53.TASKS
    )
    loo_passes = sum(
        gemini_holm["rejected"][f"loo:{task}"]
        and gemini_tests[f"loo:{task}"]["statistic"] > 0
        for task in p53.TASKS
    )
    oss_tests = {}
    for index, task in enumerate(p53.TASKS):
        others = [other for other in p53.TASKS if other != task]
        prediction = np.mean([taus["gptoss120"][other] - taus["gptoss120"][other].mean() for other in others], axis=0)
        target = taus["gptoss120"][task] - taus["gptoss120"][task].mean()
        oss_tests[f"loo:{task}"] = p53.perm_corr(prediction, target, 5380 + index)
    oss_holm = p53.holm(oss_tests)
    factor = {model: p53.factorization(np.stack([taus[model][task] for task in p53.TASKS])) for model in MODELS}
    policy = {task: p53.policy_secondary(matrices["gemini"][task], baseline["mean_tau"]["gemini"]["0.5"]) for task in p53.TASKS}
    policy_gate = all(
        policy[task][direction]["field_no_worse"] and policy[task][direction]["field_false_certified"] == 0
        for task in p53.TASKS for direction in ("A_to_B", "B_to_A")
    )
    artifact_dominant = any((technical(rows, model)["shadow_disagreement_rate"] or 0) >= 0.10 for model in MODELS)
    if artifact_dominant:
        verdict = "EVALUATION_ARTIFACT_DOMINANT"
    elif full and policy_gate:
        verdict = "CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_WITH_ZERO_SHOT_POLICY_TRANSFER"
    elif full:
        verdict = "CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_WITHOUT_OPERATIONAL_TRANSFER"
    elif loo_passes == 3 and historical_passes < 3:
        verdict = "FRESH_TASK_COMMON_COMPONENT_WITHOUT_HISTORICAL_TRANSPORT"
    elif historical_passes >= 1 and loo_passes >= 1:
        verdict = "PARTIAL_TASK_TRANSPORT_ONLY"
    elif factor["gemini"]["share_interaction"] > factor["gemini"]["share_representation"]:
        verdict = "TASK_INTERACTION_DOMINATES_REPRESENTATION_DIFFICULTY"
    else:
        verdict = "NO_CROSS_TASK_MEASUREMENT_LAW"
    return {
        "stage": STAGE,
        "predecessor": {"stage": "EPISTEME-P53", "run_id": P53_RUN_ID, "source_receipt_sha256": source_receipt_sha256},
        "technical": {model: technical(rows, model) for model in MODELS},
        "recovery": replay_summary,
        "design": {"tasks": list(p53.TASKS), "models": list(MODELS), "draws_per_task_model": 32, "replayed_failed_rows_max": EXPECTED_FAILED_ROWS, "new_failed_cell_replay_invocations": EXPECTED_FAILED_ROWS, "provider_retry_semantics": "unchanged P53 call wrapper; 441 is the cell-replay bound, not a transport-request bound", "primary_width": p53.WIDTH},
        "gemini": {
            "tau": {task: taus["gemini"][task].tolist() for task in p53.TASKS},
            "primary_tests": gemini_tests,
            "holm": gemini_holm,
            "factorization": factor["gemini"],
            "historical_pass_count": historical_passes,
            "loo_pass_count": loo_passes,
        },
        "gptoss120": {
            "tau": {task: taus["gptoss120"][task].tolist() for task in p53.TASKS},
            "loo_tests": oss_tests,
            "holm": oss_holm,
            "factorization": factor["gptoss120"],
        },
        "zero_shot_policy_transfer": policy,
        "policy_gate": policy_gate,
        "constitutional_verdict": verdict,
        "raw_rows": rows,
        "authority": "P54 closes the P53 technical hold by replaying only prior technical failures. Complete data reuse the unchanged P53 thresholds and branch rules. Descriptive cross-task transport and operational utility remain separate. No provider-internal, neural-state, generic prompt-robustness, or behavioral-SVEC claim is licensed.",
    }


def main() -> None:
    if os.environ.get("GITHUB_RUN_ATTEMPT", "1") != "1":
        raise RuntimeError("P54 is a one-shot recovery; GitHub rerun attempts are prohibited")
    check_source_contract()
    source_path = Path(sys.argv[1] if len(sys.argv) > 1 else "receipts/p53_source/p53_result.json")
    out_path = Path(sys.argv[2] if len(sys.argv) > 2 else "receipts/p54_result.json")
    source_receipt, failures = load_and_validate_receipt(source_path)
    prior_rows = source_receipt["raw_rows"]
    replayed, status_counts = replay_failures(failures)
    rows = merge_rows(prior_rows, replayed)
    gates = {model: technical(rows, model) for model in MODELS}
    replay_summary = {
        "planned_failed_rows": len(failures),
        "replayed_rows": len(replayed),
        "by_model_and_status": {f"{model}:{status}": count for (model, status), count in sorted(status_counts.items())},
        "successful_p53_rows_replayed": 0,
        "one_attempt_per_failed_row": True,
    }
    if not all(gate["complete"] for gate in gates.values()):
        out = {
            "stage": STAGE,
            "predecessor": {"stage": "EPISTEME-P53", "run_id": P53_RUN_ID, "source_receipt_sha256": sha256(source_path)},
            "technical": gates,
            "recovery": replay_summary,
            "constitutional_verdict": "TECHNICAL_HOLD",
            "raw_rows": rows,
            "authority": "P53 thresholds and analysis were not applied because technical completeness was not recovered. No additional retries or outcome-driven repairs are authorized by this stage.",
        }
    else:
        out = analyze_complete(rows, sha256(source_path), replay_summary)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"stage": STAGE, "technical": gates, "constitutional_verdict": out["constitutional_verdict"], "recovery": replay_summary}, indent=2))


if __name__ == "__main__":
    main()

