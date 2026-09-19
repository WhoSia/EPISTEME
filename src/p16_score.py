from __future__ import annotations

import json
from typing import Any

from p16_packets import hidden_key


def parse_answer(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": raw["packet_id"],
        "challenge": raw.get("challenge", "NONE"),
        "intervention": raw.get("intervention"),
        "predicted_direction": raw.get("predicted_direction"),
        "rationale_ids": raw.get("rationale_ids", []),
    }


def admissible(answer: dict[str, Any], key: dict[str, Any]) -> bool:
    if key["audit_class"] == "null":
        return answer["challenge"] == "NONE"

    if answer["challenge"] == "NONE":
        return False

    return (
        answer["intervention"] == key["oracle_intervention"]
        and answer["predicted_direction"] == key["oracle_direction"]
    )


def score_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    key = hidden_key()
    scored = []

    for raw in rows:
        answer = parse_answer(raw)
        audit = key[answer["packet_id"]]
        scored.append(
            {
                **audit,
                "packet_id": answer["packet_id"],
                "admissible": admissible(answer, audit),
                "returned_none": answer["challenge"] == "NONE",
            }
        )

    summary: dict[str, Any] = {}
    for audit_class in ("critical", "recoverable", "null"):
        for retention in ("R", "C", "S"):
            sub = [
                row for row in scored
                if row["audit_class"] == audit_class and row["retention"] == retention
            ]
            summary[f"{audit_class}:{retention}"] = {
                "n": len(sub),
                "admissible": sum(row["admissible"] for row in sub),
                "none": sum(row["returned_none"] for row in sub),
            }

    return {"summary": summary, "scored": scored}


def transfer_prompt(source_criticism: dict[str, Any], target_packet: dict[str, Any]) -> dict[str, Any]:
    """Create a cross-model criticism-transfer packet.

    Source wording is transferred, but hidden retention labels and audit labels are not.
    The target model must decide whether the criticism is coherent and whether, if its
    predicted contrast were observed, the incumbent sufficiency claim should be revised.
    """
    return {
        "target_archive": target_packet,
        "transferred_criticism": {
            "challenge": source_criticism.get("challenge"),
            "intervention": source_criticism.get("intervention"),
            "predicted_direction": source_criticism.get("predicted_direction"),
        },
        "question": (
            "Is this criticism scientifically coherent given the archive? "
            "If the stated contrast were observed, would it challenge the incumbent "
            "sufficiency claim? Answer ACCEPT/REJECT and KEEP/REVISE."
        ),
    }


if __name__ == "__main__":
    raise SystemExit(
        "Import score_rows() after collecting blinded external-model outputs. "
        "Routine result ledgers belong in Drive/Notion, not GitHub."
    )
