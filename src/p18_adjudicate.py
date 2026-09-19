from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p16_packets import hidden_key

MODELS = ("qwen", "gemini", "gptoss")


def normalize_challenge(value: Any) -> str:
    if value is None:
        return "NONE"
    text = str(value).strip()
    return "NONE" if text.upper() == "NONE" else text


def replicate_admissible(row: dict[str, Any], audit: dict[str, Any]) -> bool:
    if row.get("status") != "OK":
        return False

    parsed = row.get("parsed_response") or {}
    challenge = normalize_challenge(parsed.get("challenge"))

    if audit["audit_class"] == "null":
        return challenge == "NONE"

    if challenge == "NONE":
        return False

    return (
        parsed.get("intervention") == audit["oracle_intervention"]
        and parsed.get("predicted_direction") == audit["oracle_direction"]
    )


def aggregate_model(receipt: dict[str, Any]) -> dict[str, Any]:
    key = hidden_key()
    by_packet: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in receipt["rows"]:
        by_packet[row["packet_id"]].append(row)

    packet_rows = []
    for packet_id, reps in by_packet.items():
        if packet_id not in key:
            raise KeyError(f"unknown packet id: {packet_id}")

        audit = key[packet_id]
        votes = [replicate_admissible(r, audit) for r in reps]
        packet_success = sum(votes) >= 2

        packet_rows.append({
            **audit,
            "packet_id": packet_id,
            "replicate_n": len(reps),
            "admissible_votes": sum(votes),
            "packet_success": packet_success,
            "format_or_api_failures": sum(r.get("status") != "OK" for r in reps),
        })

    summary: dict[str, Any] = {}
    for audit_class in ("critical", "recoverable", "null"):
        for retention in ("R", "C", "S"):
            sub = [
                r for r in packet_rows
                if r["audit_class"] == audit_class and r["retention"] == retention
            ]
            summary[f"{audit_class}:{retention}"] = {
                "n": len(sub),
                "packet_successes": sum(r["packet_success"] for r in sub),
            }

    critical_r = summary["critical:R"]["packet_successes"]
    critical_c = summary["critical:C"]["packet_successes"]
    critical_s = summary["critical:S"]["packet_successes"]
    recoverable_c = summary["recoverable:C"]["packet_successes"]

    null_fp = {}
    for retention in ("R", "C", "S"):
        # For null packets, admissible means correctly returning NONE.
        correct_none = summary[f"null:{retention}"]["packet_successes"]
        null_fp[retention] = summary[f"null:{retention}"]["n"] - correct_none

    conjunctive_pass = (
        critical_r >= 5
        and critical_c <= 2
        and critical_s <= 2
        and recoverable_c >= 2
        and all(v <= 1 for v in null_fp.values())
    )

    return {
        "model_key": receipt["model_key"],
        "provider": receipt["provider"],
        "model": receipt["model"],
        "summary": summary,
        "null_false_positives": null_fp,
        "generation_signature_pass": conjunctive_pass,
        "packet_rows": sorted(packet_rows, key=lambda r: r["packet_id"]),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qwen", required=True)
    ap.add_argument("--gemini", required=True)
    ap.add_argument("--gptoss", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    receipts = {}
    for key, path in {
        "qwen": args.qwen,
        "gemini": args.gemini,
        "gptoss": args.gptoss,
    }.items():
        receipts[key] = json.loads(Path(path).read_text(encoding="utf-8"))

    result = {
        "stage": "EPISTEME-P18",
        "rule": "2-of-3 replicate aggregation; frozen P16 conjunctive signature",
        "models": {k: aggregate_model(v) for k, v in receipts.items()},
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
