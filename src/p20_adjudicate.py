from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p20_packets import hidden_key


def norm_challenge(v: Any) -> str:
    if v is None:
        return "NONE"
    t = str(v).strip()
    return "NONE" if t.upper() == "NONE" else t


def replicate_correct(row: dict[str, Any], audit: dict[str, Any]) -> bool:
    if row.get("status") != "OK":
        return False

    ans = row.get("parsed_response") or {}
    challenge = norm_challenge(ans.get("challenge"))

    if not audit["expected_specific_criticism"]:
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
        votes = [replicate_correct(r, audit) for r in reps]
        packets.append({
            **audit,
            "packet_id": pid,
            "replicate_n": len(reps),
            "correct_votes": sum(votes),
            "packet_correct": sum(votes) >= 2,
            "format_or_api_failures": sum(r.get("status") != "OK" for r in reps),
        })

    cells: dict[str, dict[str, int]] = {}
    for cell in ("P0H0", "P0H1", "P1H0", "P1H1"):
        rows = [r for r in packets if r["cell"] == cell]
        if cell == "P1H1":
            success = sum(r["packet_correct"] for r in rows)
            cells[cell] = {"specific_success": success, "n": len(rows)}
        else:
            correct_none = sum(r["packet_correct"] for r in rows)
            cells[cell] = {
                "false_positive": len(rows) - correct_none,
                "n": len(rows),
            }

    gate = (
        cells["P1H1"]["specific_success"] >= 3
        and cells["P0H0"]["false_positive"] <= 1
        and cells["P0H1"]["false_positive"] <= 1
        and cells["P1H0"]["false_positive"] <= 1
    )

    return {
        "model_key": receipt["model_key"],
        "provider": receipt["provider"],
        "model": receipt["model"],
        "cells": cells,
        "conjunctive_gate_pass": gate,
        "packets": sorted(packets, key=lambda x: (x["world_id"], x["cell"])),
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

    pass_count = sum(m["conjunctive_gate_pass"] for m in models.values())
    primary_pair_pass = (
        models["qwen"]["conjunctive_gate_pass"]
        and models["gemini"]["conjunctive_gate_pass"]
    )

    result = {
        "stage": "EPISTEME-P20",
        "rule": {
            "packet_correct": ">=2/3 correct replicates",
            "P1H1_specific_success": ">=3/4",
            "P0H0_false_positive": "<=1/4",
            "P0H1_false_positive": "<=1/4",
            "P1H0_false_positive": "<=1/4",
            "program_level": ">=2/3 models pass the full conjunctive gate",
        },
        "models": models,
        "program_level_behavioral_svec": {
            "two_of_three_models_pass": pass_count >= 2,
            "primary_pair_pass": primary_pair_pass,
            "promotion_eligible": pass_count >= 2,
            "interpretation": (
                "Promotion eligibility requires selective criticism only in the jointly "
                "provenance-linked and history-sensitive cell while matched key visibility "
                "does not induce criticism in either single-factor or double-negative controls."
            ),
        },
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
