from __future__ import annotations

import hashlib
import itertools
import random
from typing import Any

from p16_packets import worlds
from p25_packets import COORDS, build as p25_build, label

SEED = 20260924
TAG = "P27-HELDOUT-CUBE-COMPLETION"
SEMANTICS = ("valid", "null")

P25_EXCEPTION_VERTICES = (
    frozenset({"R"}),
    frozenset({"H", "T", "L"}),
    frozenset({"R", "F", "H"}),
    frozenset({"R", "F", "T", "L"}),
)


def all_vertices() -> tuple[frozenset[str], ...]:
    rows = []
    for n in range(len(COORDS) + 1):
        for combo in itertools.combinations(COORDS, n):
            rows.append(frozenset(combo))
    return tuple(rows)


def p26_vertices() -> set[frozenset[str]]:
    out = set(P25_EXCEPTION_VERTICES)
    for vertex in P25_EXCEPTION_VERTICES:
        for coord in COORDS:
            out.add(vertex.symmetric_difference({coord}))
    return out


NEW_VERTICES = tuple(
    v for v in all_vertices() if v not in p26_vertices()
)


def oid(world_id: str, vertex: frozenset[str], semantic: str) -> str:
    raw = f"{SEED}:{TAG}:{world_id}:{label(vertex)}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def selected_worlds():
    return worlds()[3:6]


def build(w, vertex: frozenset[str], semantic: str) -> dict[str, Any]:
    packet = p25_build(w, vertex, semantic)
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
    random.Random(SEED + 27).shuffle(rows)
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
