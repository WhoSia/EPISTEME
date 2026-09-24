from __future__ import annotations

import hashlib
import itertools
import random
from typing import Any

from p16_packets import worlds

SEED = 20260924
TAG = "P25-BOOLEAN-TRANSPORT-CUBE"
COORDS = ("R", "F", "H", "T", "L")
SEMANTICS = ("valid", "null")

# Frozen vertices already measured in P23/P24.
INHERITED_VERTICES = {
    frozenset(),                 # canonical
    frozenset({"R"}),            # rename-only
    frozenset({"F"}),
    frozenset({"H"}),
    frozenset({"T"}),
    frozenset({"L"}),
    frozenset({"R", "F"}),
    frozenset({"R", "H"}),
    frozenset({"R", "T"}),
    frozenset({"R", "L"}),
    frozenset(COORDS),           # alpha-full
}


def all_vertices() -> tuple[frozenset[str], ...]:
    out = []
    for n in range(len(COORDS) + 1):
        for combo in itertools.combinations(COORDS, n):
            out.append(frozenset(combo))
    return tuple(out)


NEW_VERTICES = tuple(v for v in all_vertices() if v not in INHERITED_VERTICES)


def label(vertex: frozenset[str]) -> str:
    if not vertex:
        return "I"
    return "_".join(c for c in COORDS if c in vertex)


def oid(world_id: str, vertex: frozenset[str], semantic: str) -> str:
    raw = f"{SEED}:{TAG}:{world_id}:{label(vertex)}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def selected_worlds():
    return worlds()[:3]


def base(w) -> dict[str, Any]:
    return {
        "claim": w.terminal_claim,
        "terminal_observation": {
            w.history_a: "T=stable",
            w.history_b: "T=stable",
        },
        "available_interventions": [w.intervention, "uX", "uY"],
        "instructions": (
            "Using only this archive, propose the single strongest admissible experiment "
            "that could falsify the claim. If the archive does not justify a specific "
            "counterexample test, answer NONE. Do not speculate beyond retained evidence."
        ),
        "surface_domain": w.skin,
    }


def build(w, vertex: frozenset[str], semantic: str) -> dict[str, Any]:
    renamed = "R" in vertex
    filler_renamed = "F" in vertex
    reverse_histories = "H" in vertex
    witness_last = "T" in vertex
    reverse_relations = "L" in vertex

    key = f"zeta25-{w.world_id.lower()}" if renamed else f"k25-{w.world_id.lower()}c"
    alt = f"{key}-alt"
    fillers = ["q9", "q4"] if filler_renamed else ["p2", "p3"]

    def trace(token: str) -> list[str]:
        return [*fillers, token] if witness_last else [token, *fillers]

    h_a = {"history": w.history_a, "trace": trace(key)}
    h_b = {"history": w.history_b, "trace": trace(alt)}
    histories = [h_b, h_a] if reverse_histories else [h_a, h_b]

    target = {
        "source": key,
        "intervention": w.intervention,
        "response_link": (
            "history-sensitive" if semantic == "valid" else "history-invariant"
        ),
    }
    distractor = {
        "source": "decoy-z" if renamed else "distractor-c",
        "intervention": "uX",
        "response_link": "irrelevant",
    }
    relations = [distractor, target] if reverse_relations else [target, distractor]

    packet = base(w)
    packet["retained_history"] = histories
    packet["relation_notes"] = relations
    packet["archive_id"] = oid(w.world_id, vertex, semantic)
    return packet


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in selected_worlds():
        for vertex in NEW_VERTICES:
            for semantic in SEMANTICS:
                rows.append({
                    "packet_id": oid(w.world_id, vertex, semantic),
                    "packet": build(w, vertex, semantic),
                })
    random.Random(SEED + 25).shuffle(rows)
    return rows


def hidden_key() -> dict[str, Any]:
    return {
        oid(w.world_id, vertex, semantic): {
            "world_id": w.world_id,
            "vertex": label(vertex),
            "coordinates": [c for c in COORDS if c in vertex],
            "semantic_class": semantic,
            "expected_specific_criticism": semantic == "valid",
            "oracle_intervention": w.intervention,
            "oracle_direction": "different",
        }
        for w in selected_worlds()
        for vertex in NEW_VERTICES
        for semantic in SEMANTICS
    }


if __name__ == "__main__":
    print(len(NEW_VERTICES), [label(v) for v in NEW_VERTICES])
