from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p23_packets import REPRESENTATIONS, ABLATIONS, hidden_key


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
            "ok_replicates": ok_reps,
            "technically_evaluable": ok_reps >= 2,
            "correct_votes": votes,
            "packet_correct": votes >= 2,
            "format_or_api_failures": sum(r.get("status") != "OK" for r in reps),
        })

    arm_evaluable = all(p["technically_evaluable"] for p in packets)

    families = {}
    for family in REPRESENTATIONS:
        valid = [
            p for p in packets
            if p["family"] == family and p["semantic_class"] == "valid"
        ]
        null = [
            p for p in packets
            if p["family"] == family and p["semantic_class"] == "null"
        ]
        vs = sum(p["packet_correct"] for p in valid)
        fp = len(null) - sum(p["packet_correct"] for p in null)
        families[family] = {
            "valid_success": vs,
            "valid_n": len(valid),
            "null_false_positive": fp,
            "null_n": len(null),
            "selective_pass": vs >= 2 and fp <= 1,
        }

    ablations = {}
    for ablation in ABLATIONS:
        rows = [p for p in packets if p["family"] == ablation]
        fp = len(rows) - sum(p["packet_correct"] for p in rows)
        ablations[ablation] = {
            "false_positive": fp,
            "n": len(rows),
            "necessity_pass": fp <= 1,
        }

    canonical_pass = families["canonical"]["selective_pass"]
    single_coordinates = (
        "rename_only",
        "history_order_only",
        "trace_order_only",
        "relation_order_only",
    )
    boundary = {}
    for family in single_coordinates:
        boundary[family] = {
            "selective_pass": families[family]["selective_pass"],
            "changes_pass_state_vs_canonical": (
                families[family]["selective_pass"] != canonical_pass
            ),
        }

    alpha_interaction_residual = (
        families["alpha_full"]["selective_pass"]
        != all(families[f]["selective_pass"] for f in single_coordinates)
    )

    minimal_sufficient = (
        families["minimal"]["selective_pass"]
        and all(v["necessity_pass"] for v in ablations.values())
    )

    return {
        "model_key": receipt["model_key"],
        "provider": receipt["provider"],
        "model": receipt["model"],
        "arm_evaluable": arm_evaluable,
        "families": families,
        "boundary_localization": boundary,
        "alpha_interaction_residual": alpha_interaction_residual,
        "minimal_necessity": ablations,
        "minimal_sufficient_under_test": minimal_sufficient if arm_evaluable else None,
        "format_or_api_failures": sum(p["format_or_api_failures"] for p in packets),
        "packets": sorted(
            packets,
            key=lambda x: (x["world_id"], x["family"], x["semantic_class"]),
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

    if len(evaluable) < 2:
        verdict = "TECHNICAL_HOLD"
        law = "UNRESOLVED"
    else:
        pass_maps = {
            tuple(
                (f, m["families"][f]["selective_pass"])
                for f in REPRESENTATIONS
            )
            for m in evaluable
        }
        necessity_maps = {
            tuple(
                (a, m["minimal_necessity"][a]["necessity_pass"])
                for a in ABLATIONS
            )
            for m in evaluable
        }

        if len(pass_maps) == 1 and len(necessity_maps) == 1:
            verdict = "SHARED_TRANSPORT_LAW_CANDIDATE"
            law = "MODEL-CONSENSUS_WITHIN_TESTED_FAMILY"
        else:
            verdict = "MODEL_CONDITIONAL_TRANSPORT"
            law = "MODEL-SPECIFIC_BOUNDARY_GEOMETRY"

    result = {
        "stage": "EPISTEME-P23",
        "rule": {
            "packet_correct": ">=2/3 correct replicates",
            "arm_evaluable": "every packet has >=2 OK replicates",
            "representation_selective_pass": "valid success >=2/3 and null false-positive <=1/3",
            "ablation_necessity_pass": "false-positive <=1/3",
            "technical_hold": "<2 evaluable models",
            "law_extraction": (
                "shared candidate only if all evaluable models have identical representation "
                "pass maps and identical necessity maps; otherwise report model-conditional geometry"
            ),
        },
        "models": models,
        "program_level": {
            "evaluable_models": len(evaluable),
            "verdict": verdict,
            "transport_law": law,
        },
        "authority": (
            "P23 is diagnostic. It may identify model-conditional or shared transport rules "
            "within the frozen transformation family, but it does not promote behavioral SVEC "
            "and does not establish a universal representation law."
        ),
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
