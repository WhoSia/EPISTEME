from __future__ import annotations
import argparse, hashlib, itertools, json, subprocess, sys, tempfile
from pathlib import Path

STAGE = "EPISTEME-P59"
EXPECTED_P58_RESULT_SHA256 = "37c44c75b846f93eb23b71fe8bf61801bcd58347c8ad86485f1067119dabe78f"
EXPECTED_P57_RECOVERED_SHA256 = "381cd8376a6ccad23fb240e3f9d46342a9d1025e7463753ade3f1bd56bbec475"
TASKS = ("FAULT_DIAGNOSIS_HISTORY", "NORMALIZATION_PIPELINE", "MATERIAL_PRECONDITIONING")
TARGET = {
    "task": "MATERIAL_PRECONDITIONING",
    "draw": 55,
    "cell_index": 57,
    "vertex": "R_F_T_L",
    "semantic": "null",
    "alias": "A",
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def identity(row):
    return (row["task"], int(row["draw"]), int(row["cell_index"]))

def rejection_vector(result):
    h = result["holm_familywise_005"]["rejected"]
    return {k: bool(h[k]) for k in sorted(h)}

def affected_tau(result):
    return result["fresh_tau"]["MATERIAL_PRECONDITIONING"]["B"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p58-result", required=True)
    ap.add_argument("--p57-recovered", required=True)
    ap.add_argument("--p55", required=True)
    ap.add_argument("--analyzer", default="src/p57_analyze_shards.py")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    p58_path = Path(args.p58_result)
    p57_path = Path(args.p57_recovered)
    if sha256(p58_path) != EXPECTED_P58_RESULT_SHA256:
        raise RuntimeError("P58_RESULT_FINGERPRINT_MISMATCH")
    if sha256(p57_path) != EXPECTED_P57_RECOVERED_SHA256:
        raise RuntimeError("P57_RECOVERED_FINGERPRINT_MISMATCH")

    p58 = json.loads(p58_path.read_text(encoding="utf-8"))
    src = json.loads(p57_path.read_text(encoding="utf-8"))
    if p58.get("stage") != "EPISTEME-P58" or p58.get("constitutional_verdict") != "TECHNICAL_HOLD":
        raise RuntimeError("P58_AUTHORITY_MISMATCH")
    rows = src.get("raw_rows", [])
    if len(rows) != 12288:
        raise RuntimeError(f"P57_ROW_COUNT_MISMATCH:{len(rows)}")
    failed = [r for r in rows if r.get("status") != "OK"]
    if len(failed) != 1:
        raise RuntimeError(f"EXPECTED_ONE_REMAINING_FAILURE_GOT:{len(failed)}")
    target = failed[0]
    for k, v in TARGET.items():
        if target.get(k) != v:
            raise RuntimeError(f"TARGET_MISMATCH:{k}:{target.get(k)}:{v}")

    target_vi = int(target["vertex_index"])
    worlds = []
    with tempfile.TemporaryDirectory(prefix="p59_") as td:
        root = Path(td)
        for pc, sc in itertools.product((False, True), repeat=2):
            tag = f"pc{int(pc)}_sc{int(sc)}"
            wroot = root / tag / "rows"
            wroot.mkdir(parents=True)
            completed = []
            for r in rows:
                q = dict(r)
                if identity(q) == identity(target):
                    q.update({
                        "status": "OK",
                        "primary_correct": pc,
                        "shadow_correct": sc,
                        "error": None,
                        "p59_completion": True,
                        "p59_completion_world": tag,
                    })
                completed.append(q)
            for task in TASKS:
                rs = [r for r in completed if r["task"] == task]
                if len(rs) != 4096:
                    raise RuntimeError(f"{task}_COUNT:{len(rs)}")
                (wroot / f"{task}.json").write_text(
                    json.dumps({"task": task, "rows": rs}, indent=2), encoding="utf-8"
                )
            out = root / tag / "p57_result.json"
            subprocess.run(
                [sys.executable, args.analyzer, "--rows-root", str(wroot),
                 "--p55", args.p55, "--out", str(out)],
                check=True,
            )
            res = json.loads(out.read_text(encoding="utf-8"))
            if res.get("technical", {}).get("complete") is not True:
                raise RuntimeError(f"COMPLETION_WORLD_NOT_TECHNICALLY_COMPLETE:{tag}")
            tau = affected_tau(res)
            worlds.append({
                "world": tag,
                "primary_correct": pc,
                "shadow_correct": sc,
                "affected_tau_vector": tau,
                "affected_vertex_index": target_vi,
                "affected_vertex_tau": tau[target_vi],
                "constitutional_verdict": res["constitutional_verdict"],
                "rejection_vector": rejection_vector(res),
                "family_pass_counts": res["family_pass_counts"],
                "strict_operator_reversals": res["strict_operator_reversals"],
                "primary_tests": res["primary_tests"],
                "holm_familywise_005": res["holm_familywise_005"],
            })

    verdicts = {w["constitutional_verdict"] for w in worlds}
    vectors = {json.dumps(w["rejection_vector"], sort_keys=True) for w in worlds}
    affected_taus = {w["affected_vertex_tau"] for w in worlds}
    full_tau_vectors = {json.dumps(w["affected_tau_vector"]) for w in worlds}
    branch_invariant = len(verdicts) == 1
    holm_invariant = len(vectors) == 1
    stopping_invariant = len(affected_taus) == 1 and len(full_tau_vectors) == 1
    closure = branch_invariant and holm_invariant

    unique_verdict = next(iter(verdicts)) if branch_invariant else None
    if closure and unique_verdict == "OPERATOR_REVERSAL_WITH_NONTRANSPORTABLE_INTERACTION":
        p59_verdict = "MISSINGNESS_FREE_OPERATOR_REVERSAL_WITH_NONTRANSPORTABLE_INTERACTION"
    elif closure:
        p59_verdict = "MISSINGNESS_FREE_P57_BRANCH_IDENTIFIED"
    else:
        p59_verdict = "P57_BRANCH_PARTIALLY_IDENTIFIED"

    out = {
        "stage": STAGE,
        "provider_calls": 0,
        "source": {
            "p58_result_sha256": EXPECTED_P58_RESULT_SHA256,
            "p57_recovered_result_sha256": EXPECTED_P57_RECOVERED_SHA256,
            "remaining_cell": TARGET,
        },
        "completion_lattice": {
            "world_count": 4,
            "probability_model": None,
            "weights": None,
            "worlds": worlds,
        },
        "invariance": {
            "stopping_time_invariant": stopping_invariant,
            "affected_vertex_tau_values": sorted(affected_taus),
            "holm_rejection_vector_invariant": holm_invariant,
            "constitutional_branch_invariant": branch_invariant,
        },
        "identified_p57_verdict": unique_verdict,
        "p59_verdict": p59_verdict,
        "closure_authorized": closure,
        "authority": (
            "Zero-provider-call exhaustive completion-lattice adjudication. "
            "No missingness probability model or completion weighting is used. "
            "The frozen P57 analyzer is executed unchanged in every admissible world."
        ),
    }
    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
