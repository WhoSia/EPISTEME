from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p22_packets import REPRESENTATIONS, hidden_key


def norm_challenge(v: Any) -> str:
    if v is None:
        return "NONE"
    t = str(v).strip()
    return "NONE" if t.upper() == "NONE" else t


def scientific_correct(row: dict[str, Any], audit: dict[str, Any]) -> bool:
    if row.get("status") != "OK":
        return False
    ans = row.get("parsed_response") or {}
    challenge = norm_challenge(ans.get("challenge"))

    if not audit["expected_specific_criticism"]:
        return challenge == "NONE"

    return (
        challenge != "NONE"
        and ans.get("intervention") == audit["oracle_intervention"]
        and ans.get("predicted_direction") == audit["oracle_direction"]
    )


def aggregate(receipt: dict[str, Any]) -> dict[str, Any]:
    key = hidden_key()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in receipt["rows"]:
        grouped[row["packet_id"]].append(row)

    packets = []
    for pid, reps in grouped.items():
        audit = key[pid]
        ok_reps = sum(r.get("status") == "OK" for r in reps)
        votes = sum(scientific_correct(r, audit) for r in reps)
        packets.append({
            **audit,
            "packet_id": pid,
            "replicate_n": len(reps),
            "ok_replicates": ok_reps,
            "technically_evaluable": ok_reps >= 2,
            "correct_votes": votes,
            "packet_correct": votes >= 2,
            "format_or_api_failures": sum(r.get("status") != "OK" for r in reps),
        })

    arm_evaluable = all(p["technically_evaluable"] for p in packets)

    representations = {}
    for rep in REPRESENTATIONS:
        valid = [
            p for p in packets
            if p["representation"] == rep and p["semantic_class"] == "valid"
        ]
        null = [
            p for p in packets
            if p["representation"] == rep and p["semantic_class"] == "null"
        ]
        representations[rep] = {
            "valid_success": sum(p["packet_correct"] for p in valid),
            "valid_n": len(valid),
            "null_false_positive": len(null) - sum(p["packet_correct"] for p in null),
            "null_n": len(null),
        }
        representations[rep]["gate_pass"] = (
            representations[rep]["valid_success"] >= 3
            and representations[rep]["null_false_positive"] <= 1
        )

    worlds = sorted({p["world_id"] for p in packets})
    valid_transport = 0
    null_transport = 0
    for world_id in worlds:
        v = [
            p for p in packets
            if p["world_id"] == world_id and p["semantic_class"] == "valid"
        ]
        n = [
            p for p in packets
            if p["world_id"] == world_id and p["semantic_class"] == "null"
        ]
        valid_transport += int(
            len(v) == len(REPRESENTATIONS) and all(p["packet_correct"] for p in v)
        )
        null_transport += int(
            len(n) == len(REPRESENTATIONS) and all(p["packet_correct"] for p in n)
        )

    ablation = [
        p for p in packets if p["semantic_class"] == "no_provenance"
    ]
    ablation_fp = len(ablation) - sum(p["packet_correct"] for p in ablation)

    full_invariance_gate = (
        all(representations[r]["gate_pass"] for r in REPRESENTATIONS)
        and valid_transport >= 3
        and null_transport >= 3
        and ablation_fp <= 1
    )

    return {
        "model_key": receipt["model_key"],
        "provider": receipt["provider"],
        "model": receipt["model"],
        "arm_evaluable": arm_evaluable,
        "representations": representations,
        "cross_representation_transport": {
            "valid_worlds_all_representations_correct": valid_transport,
            "null_worlds_all_representations_correct": null_transport,
            "n_worlds": len(worlds),
        },
        "minimal_no_provenance": {
            "false_positive": ablation_fp,
            "n": len(ablation),
        },
        "full_invariance_gate_pass": full_invariance_gate if arm_evaluable else None,
        "format_or_api_failures": sum(p["format_or_api_failures"] for p in packets),
        "packets": sorted(
            packets,
            key=lambda x: (
                x["world_id"],
                x["representation"],
                x["semantic_class"],
            ),
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qwen", required=True)
    ap.add_argument("--gemini", required=True)
    ap.add_argument("--gptoss", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    paths = {"qwen": args.qwen, "gemini": args.gemini, "gptoss": args.gptoss}
    models = {
        k: aggregate(json.loads(Path(v).read_text(encoding="utf-8")))
        for k, v in paths.items()
    }

    evaluable = [m for m in models.values() if m["arm_evaluable"]]
    pass_count = sum(m["full_invariance_gate_pass"] is True for m in evaluable)

    if len(evaluable) < 2:
        verdict = "TECHNICAL_HOLD"
        representation_invariant = False
    elif pass_count >= 2:
        verdict = "PASS_REPRESENTATION_INVARIANCE"
        representation_invariant = True
    else:
        verdict = "FAIL_REPRESENTATION_INVARIANCE"
        representation_invariant = False

    result = {
        "stage": "EPISTEME-P22",
        "rule": {
            "packet_correct": ">=2/3 correct replicates",
            "arm_evaluable": "every packet has >=2 OK replicates",
            "per_representation": "valid >=3/4 and null false-positive <=1/4",
            "valid_cross_representation_transport": ">=3/4 worlds correct in all representations",
            "null_cross_representation_transport": ">=3/4 worlds correct in all representations",
            "minimal_no_provenance_false_positive": "<=1/4",
            "program_level": ">=2 evaluable models pass the full invariance gate",
            "technical_hold": "<2 evaluable models",
        },
        "models": models,
        "program_level": {
            "evaluable_models": len(evaluable),
            "models_passing": pass_count,
            "verdict": verdict,
            "behavioral_svec_representation_invariant": representation_invariant,
        },
        "authority": (
            "PASS licenses representation-invariance only across the three frozen "
            "equivalence-preserving encodings and certifies the tested minimal encoding "
            "against its no-provenance ablation. It does not imply invariance to arbitrary "
            "representations or establish a universal sufficient statistic."
        ),
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
