from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p25_packets import COORDS, NEW_VERTICES, hidden_key, label

# Frozen Gemini selective-pass states inherited from P23/P24.
INHERITED_PASS = {
    "I": True,
    "R": False,
    "F": True,
    "H": True,
    "T": True,
    "L": True,
    "R_F": True,
    "R_H": True,
    "R_T": True,
    "R_L": True,
    "R_F_H_T_L": True,
}


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


def subsets(coords: tuple[str, ...]):
    for n in range(len(coords) + 1):
        for combo in itertools.combinations(coords, n):
            yield frozenset(combo)


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

    new_pass = {}
    counts = {}
    for vertex in NEW_VERTICES:
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
        passed = vs >= 2 and fp <= 1
        new_pass[name] = passed
        counts[name] = {
            "valid_success": vs,
            "valid_n": len(valid),
            "null_false_positive": fp,
            "null_n": len(null),
            "selective_pass": passed,
        }

    cube = {**INHERITED_PASS, **new_pass}

    r_fiber = {}
    for rescue in subsets(("F", "H", "T", "L")):
        vertex = frozenset({"R"}) | rescue
        r_fiber[label(vertex)] = cube[label(vertex)]

    nonempty_r_rescues = {
        k: v for k, v in r_fiber.items() if k != "R"
    }
    rescue_upward_closed = all(nonempty_r_rescues.values())
    minimal_rescue_generators = [
        c for c in ("F", "H", "T", "L") if cube[f"R_{c}"]
    ]

    fail_vertices = sorted(k for k, v in cube.items() if not v)
    pass_vertices = sorted(k for k, v in cube.items() if v)

    if arm_evaluable and fail_vertices == ["R"]:
        boundary_normal_form = "ISOLATED_RENAME_DEFECT"
        quotient = {
            "fail_class": ["R"],
            "pass_class": pass_vertices,
            "class_count": 2,
        }
    elif arm_evaluable:
        boundary_normal_form = "HIGHER_ORDER_INTERACTION_BOUNDARY"
        quotient = {
            "fail_class": fail_vertices,
            "pass_class": pass_vertices,
            "class_count": 2 if fail_vertices and pass_vertices else 1,
        }
    else:
        boundary_normal_form = "TECHNICAL_HOLD"
        quotient = None

    result = {
        "stage": "EPISTEME-P25",
        "model": "gemini",
        "arm_evaluable": arm_evaluable,
        "new_vertex_counts": counts,
        "full_32_vertex_selective_pass_cube": cube,
        "rescue_coordinate_algebra": {
            "R_fiber": r_fiber,
            "all_nonempty_rescue_subsets_pass": rescue_upward_closed,
            "minimal_singleton_rescue_generators": minimal_rescue_generators,
            "boundary_set_minimal": fail_vertices == ["R"] if arm_evaluable else None,
        },
        "representation_symmetry_breaking": {
            "failure_vertices": fail_vertices,
            "boundary_normal_form": boundary_normal_form,
        },
        "model_relative_transport_quotient": quotient,
        "format_or_api_failures": sum(
            p["format_or_api_failures"] for p in packets
        ),
        "authority": (
            "This constructs the complete Gemini quotient over the frozen 5-coordinate "
            "representation cube. Qwen and GPT-OSS classifications remain inherited; "
            "no cross-model universal quotient or behavioral SVEC promotion is licensed."
        ),
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
