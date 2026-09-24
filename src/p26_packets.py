from __future__ import annotations

import hashlib
import random
from typing import Any

from p16_packets import worlds
from p25_packets import COORDS, build as p25_build, label

SEED = 20260924
TAG = "P26-EXCEPTION-STABILITY"
SEMANTICS = ("valid", "null")

EXCEPTION_VERTICES = (
    frozenset({"R"}),
    frozenset({"H", "T", "L"}),
    frozenset({"R", "F", "H"}),
    frozenset({"R", "F", "T", "L"}),
)


def validation_vertices() -> tuple[frozenset[str], ...]:
    out = set(EXCEPTION_VERTICES)
    for vertex in EXCEPTION_VERTICES:
        for coord in COORDS:
            out.add(vertex.symmetric_difference({coord}))
    return tuple(
        sorted(
            out,
            key=lambda v: (len(v), tuple(COORDS.index(c) for c in COORDS if c in v)),
        )
    )


VALIDATION_VERTICES = validation_vertices()
EXPECTED_PASS = {
    label(v): v not in set(EXCEPTION_VERTICES)
    for v in VALIDATION_VERTICES
}


def oid(world_id: str, vertex: frozenset[str], semantic: str) -> str:
    raw = f"{SEED}:{TAG}:{world_id}:{label(vertex)}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def selected_worlds():
    # Fully held out from P23-P25 W01-W03 geometry construction.
    return worlds()[3:6]


def build(w, vertex: frozenset[str], semantic: str) -> dict[str, Any]:
    packet = p25_build(w, vertex, semantic)
    packet["archive_id"] = oid(w.world_id, vertex, semantic)
    return packet


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in selected_worlds():
        for vertex in VALIDATION_VERTICES:
            for semantic in SEMANTICS:
                rows.append({
                    "packet_id": oid(w.world_id, vertex, semantic),
                    "packet": build(w, vertex, semantic),
                })
    random.Random(SEED + 26).shuffle(rows)
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
            "expected_selective_pass": EXPECTED_PASS[label(vertex)],
        }
        for w in selected_worlds()
        for vertex in VALIDATION_VERTICES
        for semantic in SEMANTICS
    }


if __name__ == "__main__":
    print(len(VALIDATION_VERTICES), [label(v) for v in VALIDATION_VERTICES])
