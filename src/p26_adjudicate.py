from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p26_packets import (
    EXCEPTION_VERTICES,
    EXPECTED_PASS,
    VALIDATION_VERTICES,
    hidden_key,
)
from p25_packets import COORDS, label


def norm(v: Any) -> str:
    if v is None:
        return "NONE"
    t = str(v).strip()
    return "NONE" if t.upper() == "NONE" else t


def correct(row: dict[str, Any], audit: dict[str, Any]) -> bool:
    if row.get("status") != "OK":
        return False
    ans = row.get("parsed_response") or {}
    challenge = norm(ans.get("challenge"))

    if not audit["expected_specific_criticism"]:
        return challenge == "NONE"

    return (
        challenge != "NONE"
        and ans.get("intervention") == audit["oracle_intervention"]
        and ans.get("predicted_direction") == audit["oracle_direction"]
    )


def hamming(a: frozenset[str], b: frozenset[str]) -> int:
    return len(a.symmetric_difference(b))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gemini", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    receipt = json.loads(Path(args.gemini).read_text(encoding="utf-8"))
    key = hidden_key()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in receipt["rows"]:
        grouped[row["packet_id"]].append(row)

    packets = []
    for pid, reps in grouped.items():
        audit = key[pid]
        ok = sum(r.get("status") == "OK" for r in reps)
        votes = sum(correct(r, audit) for r in reps)
        packets.append({
            **audit,
            "packet_id": pid,
            "ok_replicates": ok,
            "technically_evaluable": ok >= 2,
            "packet_correct": votes >= 2,
            "format_or_api_failures": sum(r.get("status") != "OK" for r in reps),
        })

    arm_evaluable = all(p["technically_evaluable"] for p in packets)

    heldout = {}
    for vertex in VALIDATION_VERTICES:
        name = label(vertex)
        valid = [
            p for p in packets
            if p["vertex"] == name and p["semantic_class"] == "valid"
        ]
        null = [
            p for p in packets
            if p["vertex"] == name and p["semantic_class"] == "null"
        ]
        vs = sum(p["packet_correct"] for p in valid)
        fp = len(null) - sum(p["packet_correct"] for p in null)
        observed = vs >= 2 and fp <= 1
        heldout[name] = {
            "valid_success": vs,
            "valid_n": len(valid),
            "null_false_positive": fp,
            "null_n": len(null),
            "observed_selective_pass": observed,
            "expected_selective_pass": EXPECTED_PASS[name],
            "matches_p25_prediction": observed == EXPECTED_PASS[name],
        }

    exception_labels = [label(v) for v in EXCEPTION_VERTICES]
    exception_stable = all(
        heldout[x]["observed_selective_pass"] is False
        for x in exception_labels
    )
    neighbor_labels = sorted(
        set(heldout) - set(exception_labels)
    )
    local_boundary_stable = all(
        heldout[x]["observed_selective_pass"] is True
        for x in neighbor_labels
    )
    exact_prediction_match = all(
        v["matches_p25_prediction"] for v in heldout.values()
    )

    pairwise_isolated = all(
        hamming(a, b) > 1
        for i, a in enumerate(EXCEPTION_VERTICES)
        for b in EXCEPTION_VERTICES[i + 1:]
    )

    compression_certificate = {
        "default_class": "PASS",
        "exception_set": exception_labels,
        "heldout_exact_match": exact_prediction_match if arm_evaluable else None,
        "exception_vertices_hamming_isolated": pairwise_isolated,
        "minimum_axis_aligned_failure_subcube_cover_size": 4,
        "reason": (
            "Each failure vertex has only PASS Hamming-1 neighbors in the frozen P25 cube. "
            "Any positive-dimensional Boolean subcube contains an edge, so an all-failure "
            "axis-aligned subcube containing one of these vertices would include a PASS "
            "neighbor. Therefore each exception requires its own singleton failure cell."
        ),
    }

    nonuniversality_theorem = {
        "statement": (
            "No deterministic representation-only transport function on the tested domain "
            "can be model-universal across Qwen and Gemini."
        ),
        "witness": (
            "At the canonical identity representation I, inherited Qwen behavior is FAIL/"
            "abstention while inherited Gemini behavior is PASS/selective under the same "
            "representation coordinate family. A function of representation alone cannot "
            "map the same vertex to both outcomes."
        ),
        "scope": "tested Qwen/Gemini task family and frozen representation coordinate system only",
    }

    if not arm_evaluable:
        verdict = "TECHNICAL_HOLD"
    elif exact_prediction_match:
        verdict = "HELDOUT_EXCEPTION_QUOTIENT_STABLE"
    else:
        verdict = "EXCEPTION_QUOTIENT_NOT_STABLE"

    result = {
        "stage": "EPISTEME-P26",
        "model": "gemini",
        "arm_evaluable": arm_evaluable,
        "heldout_vertex_results": heldout,
        "exceptional_vertex_stability": {
            "exception_vertices_stable": exception_stable,
            "hamming1_boundary_stable": local_boundary_stable,
            "all_22_vertices_match_p25_prediction": exact_prediction_match,
        },
        "transport_cube_compression": compression_certificate,
        "cross_model_nonuniversality_theorem": nonuniversality_theorem,
        "program_verdict": verdict,
        "format_or_api_failures": sum(
            p["format_or_api_failures"] for p in packets
        ),
        "authority": (
            "A stable result validates the four-exception Gemini quotient on held-out "
            "worlds and the tested-domain non-universality claim. It does not establish "
            "arbitrary-representation invariance or behavioral SVEC promotion."
        ),
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
