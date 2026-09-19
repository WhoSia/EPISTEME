from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p19_packets import hidden_key


def norm_challenge(v: Any) -> str:
    if v is None:
        return "NONE"
    t = str(v).strip()
    return "NONE" if t.upper() == "NONE" else t


def admissible(row: dict[str, Any], audit: dict[str, Any]) -> bool:
    if row.get("status") != "OK":
        return False
    ans = row.get("parsed_response") or {}
    challenge = norm_challenge(ans.get("challenge"))

    if audit["audit_class"] == "null":
        return challenge == "NONE"

    if challenge == "NONE":
        return False

    return (
        ans.get("intervention") == audit["oracle_intervention"]
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
        votes = [admissible(r, audit) for r in reps]
        packets.append({
            **audit,
            "packet_id": pid,
            "replicate_n": len(reps),
            "admissible_votes": sum(votes),
            "packet_success": sum(votes) >= 2,
            "format_or_api_failures": sum(r.get("status") != "OK" for r in reps),
        })

    def sub(cls: str) -> list[dict[str, Any]]:
        return [r for r in packets if r["audit_class"] == cls]

    critical = sub("critical")
    recoverable = sub("recoverable")
    null = sub("null")

    critical_success = sum(r["packet_success"] for r in critical)
    recoverable_success = sum(r["packet_success"] for r in recoverable)
    null_correct_none = sum(r["packet_success"] for r in null)
    null_fp = len(null) - null_correct_none

    gate = (
        critical_success <= 2
        and recoverable_success >= 2
        and null_fp <= 1
    )

    return {
        "model_key": receipt["model_key"],
        "provider": receipt["provider"],
        "model": receipt["model"],
        "critical_C": {"success": critical_success, "n": len(critical)},
        "recoverable_C": {"success": recoverable_success, "n": len(recoverable)},
        "null_C": {"false_positive": null_fp, "n": len(null)},
        "matched_control_gate_pass": gate,
        "packets": sorted(packets, key=lambda x: x["world_id"]),
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

    pass_count = sum(m["matched_control_gate_pass"] for m in models.values())
    primary_pair_pass = (
        models["qwen"]["matched_control_gate_pass"]
        and models["gemini"]["matched_control_gate_pass"]
    )

    result = {
        "stage": "EPISTEME-P19",
        "rule": {
            "critical_C": "<=2/6",
            "recoverable_C": ">=2/3",
            "null_C_false_positive": "<=1/3",
            "packet_success": ">=2/3 admissible replicates",
        },
        "models": models,
        "program_level_reopening": {
            "two_of_three_models_pass": pass_count >= 2,
            "primary_pair_pass": primary_pair_pass,
            "interpretation": (
                "If the matched control gate succeeds, P18's common recoverable-control "
                "failure is localized to representational mismatch rather than an inherent "
                "inability to use coarse surviving witnesses. This reopens, but does not "
                "itself grant, behavioral SVEC promotion."
            ),
        },
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
