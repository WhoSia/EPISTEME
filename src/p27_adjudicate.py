from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from p25_packets import COORDS, label
from p27_packets import NEW_VERTICES, hidden_key


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


def all_labels() -> list[str]:
    out = []
    for n in range(len(COORDS) + 1):
        for combo in itertools.combinations(COORDS, n):
            out.append(label(frozenset(combo)))
    return out


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def xor_factorizable(world_maps: dict[str, dict[str, bool]]) -> bool:
    worlds = sorted(world_maps)
    vertices = all_labels()
    base = worlds[0]
    for w in worlds[1:]:
        deltas = {
            world_maps[w][v] ^ world_maps[base][v]
            for v in vertices
        }
        if len(deltas) != 1:
            return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gemini", required=True)
    ap.add_argument("--p26-result", default="active/p26_result.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    receipt = json.loads(Path(args.gemini).read_text(encoding="utf-8"))
    p26 = json.loads(Path(args.p26_result).read_text(encoding="utf-8"))

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

    new_world_maps: dict[str, dict[str, bool]] = {w: {} for w in ("W04", "W05", "W06")}
    counts = {}
    for world_id in new_world_maps:
        for vertex in NEW_VERTICES:
            name = label(vertex)
            valid = [
                p for p in packets
                if p["world_id"] == world_id
                and p["vertex"] == name
                and p["semantic_class"] == "valid"
            ][0]
            null = [
                p for p in packets
                if p["world_id"] == world_id
                and p["vertex"] == name
                and p["semantic_class"] == "null"
            ][0]
            state = valid["packet_correct"] and null["packet_correct"]
            new_world_maps[world_id][name] = state
            counts[f"{world_id}:{name}"] = {
                "valid_packet_correct": valid["packet_correct"],
                "null_packet_correct": null["packet_correct"],
                "world_selective_pass": state,
            }

    full_maps = {}
    partial = p26["world_indexed_partial_geometry"]
    labels = set(all_labels())
    for world_id in ("W04", "W05", "W06"):
        fail_from_p26 = set(partial[f"{world_id}_fail"])
        inherited_vertices = labels - set(new_world_maps[world_id])
        inherited_map = {
            v: v not in fail_from_p26
            for v in inherited_vertices
        }
        full_maps[world_id] = {
            **inherited_map,
            **new_world_maps[world_id],
        }

    fail_sets = {
        w: {v for v, state in m.items() if not state}
        for w, m in full_maps.items()
    }
    persistent_core = set.intersection(*fail_sets.values())
    volatile_union = set.union(*fail_sets.values())
    representation_only = all(
        len({full_maps[w][v] for w in full_maps}) == 1
        for v in all_labels()
    )
    xor_sep = xor_factorizable(full_maps)

    if representation_only:
        factorization = "WORLD_INVARIANT_REPRESENTATION_LAW"
    elif xor_sep:
        factorization = "WORLD_SHIFT_XOR_FACTORIZATION"
    else:
        factorization = "NONSEPARABLE_WORLD×REPRESENTATION_INTERACTION"

    pairwise = {
        "W04-W05": jaccard(fail_sets["W04"], fail_sets["W05"]),
        "W04-W06": jaccard(fail_sets["W04"], fail_sets["W06"]),
        "W05-W06": jaccard(fail_sets["W05"], fail_sets["W06"]),
    }

    result = {
        "stage": "EPISTEME-P27",
        "model": "gemini",
        "arm_evaluable": arm_evaluable,
        "new_vertex_world_results": counts,
        "world_indexed_behavioral_geometry": {
            "W04_fail": sorted(fail_sets["W04"]),
            "W05_fail": sorted(fail_sets["W05"]),
            "W06_fail": sorted(fail_sets["W06"]),
            "persistent_exception_core": sorted(persistent_core),
            "exception_union": sorted(volatile_union),
            "pairwise_failset_jaccard": pairwise,
        },
        "representation_law_factorization": {
            "representation_only": representation_only,
            "world_shift_xor_factorizable": xor_sep,
            "classification": factorization,
        },
        "model_indexed_constitution": {
            "gemini": "world-indexed 32-vertex pass/fail quotients Q_Gemini(W04), Q_Gemini(W05), Q_Gemini(W06)",
            "qwen": "inherited global-abstention regime on prior tested domain",
            "gptoss": "unconstituted because of persistent technical unevaluability",
            "cross_model_universal_representation_law": false,
        },
        "format_or_api_failures": sum(
            p["format_or_api_failures"] for p in packets
        ),
        "authority": (
            "P27 constitutes held-out world-indexed Gemini geometry and tests exact "
            "representation-law factorization on W04-W06. It does not license behavioral "
            "SVEC promotion or extrapolation beyond the tested model/world/representation family."
        ),
    }

    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
