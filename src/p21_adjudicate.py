from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p21_packets import hidden_key


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
        ok_reps = sum(r.get("status") == "OK" for r in reps)
        votes = [scientific_correct(r, audit) for r in reps]
        packets.append(
            {
                **audit,
                "packet_id": pid,
                "replicate_n": len(reps),
                "ok_replicates": ok_reps,
                "correct_votes": sum(votes),
                "packet_correct": sum(votes) >= 2,
                "technically_evaluable": ok_reps >= 2,
                "format_or_api_failures": sum(
                    r.get("status") != "OK" for r in reps
                ),
            }
        )

    arm_evaluable = all(p["technically_evaluable"] for p in packets)

    cells: dict[str, dict[str, int]] = {}
    for cell in ("P0H0", "P0H1", "P1H0", "P1H1"):
        rows = [r for r in packets if r["cell"] == cell]
        if cell == "P1H1":
            cells[cell] = {
                "specific_success": sum(r["packet_correct"] for r in rows),
                "n": len(rows),
            }
        else:
            correct_none = sum(r["packet_correct"] for r in rows)
            cells[cell] = {
                "false_positive": len(rows) - correct_none,
                "n": len(rows),
            }

    scientific_gate = (
        cells["P1H1"]["specific_success"] >= 3
        and cells["P0H0"]["false_positive"] <= 1
        and cells["P0H1"]["false_positive"] <= 1
        and cells["P1H0"]["false_positive"] <= 1
    )

    return {
        "model_key": receipt["model_key"],
        "provider": receipt["provider"],
        "model": receipt["model"],
        "arm_evaluable": arm_evaluable,
        "scientific_gate_pass": scientific_gate if arm_evaluable else None,
        "cells": cells,
        "format_or_api_failures": sum(
            p["format_or_api_failures"] for p in packets
        ),
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

    evaluable = [m for m in models.values() if m["arm_evaluable"]]
    pass_count = sum(m["scientific_gate_pass"] is True for m in evaluable)

    if len(evaluable) < 2:
        verdict = "TECHNICAL_HOLD"
        promotion_eligible = False
    elif pass_count >= 2:
        verdict = "PASS_REIDENTIFICATION"
        promotion_eligible = True
    else:
        verdict = "FAIL_REIDENTIFICATION"
        promotion_eligible = False

    result = {
        "stage": "EPISTEME-P21",
        "rule": {
            "packet_correct": ">=2/3 correct replicates",
            "arm_evaluable": "every packet has >=2 OK replicates",
            "P1H1_specific_success": ">=3/4",
            "P0H0_false_positive": "<=1/4",
            "P0H1_false_positive": "<=1/4",
            "P1H0_false_positive": "<=1/4",
            "program_level": ">=2 evaluable models pass full scientific gate",
            "technical_hold": "<2 evaluable models",
        },
        "models": models,
        "program_level": {
            "evaluable_models": len(evaluable),
            "models_passing": pass_count,
            "verdict": verdict,
            "behavioral_svec_reidentification": promotion_eligible,
        },
        "interpretation": (
            "A PASS supports re-identification of the P19 witness relation under a "
            "schema-invariant A/B source-role swap: criticism must survive only when the "
            "target relation is both history-sensitive and sourced from the history-"
            "discriminating provenance family. This stage does not yet establish broad "
            "cross-representation invariance."
        ),
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
