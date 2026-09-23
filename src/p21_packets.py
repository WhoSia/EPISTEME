from __future__ import annotations

import hashlib
import random
from typing import Any

from p16_packets import worlds

SEED = 20260923
P21_TAG = "P21-SCHEMA-INVARIANT-ROLE-SWAP"
CELLS = ("P0H0", "P0H1", "P1H0", "P1H1")


def _opaque_id(world_id: str, cell: str) -> str:
    raw = f"{SEED}:{P21_TAG}:{world_id}:{cell}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def selected_worlds():
    # Frozen before execution. Four isomorphic worlds are crossed through all four cells.
    return worlds()[:4]


def _packet_for_cell(w, cell: str) -> dict[str, Any]:
    provenance_linked = cell[1] == "1"
    history_sensitive = cell[3] == "1"

    # A is the history-discriminating provenance family: A vs A-alt.
    # B is deliberately history-invariant: the same token occurs in both traces.
    # The trace schema and token multiset are identical in every cell.
    a = f"k21-{w.world_id.lower()}a"
    b = f"k21-{w.world_id.lower()}b"

    target_source = a if provenance_linked else b
    other_source = b if provenance_linked else a

    packet = {
        "archive_id": _opaque_id(w.world_id, cell),
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
        "retained_history": [
            {"history": w.history_a, "trace": [a, b, "p3"]},
            {"history": w.history_b, "trace": [f"{a}-alt", b, "p3"]},
        ],
        "relation_notes": [
            {
                "source": target_source,
                "intervention": w.intervention,
                "response_link": (
                    "history-sensitive" if history_sensitive else "history-invariant"
                ),
            },
            {
                "source": other_source,
                "intervention": "uX",
                "response_link": "irrelevant",
            },
        ],
    }
    return packet


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in selected_worlds():
        for cell in CELLS:
            rows.append(
                {
                    "packet_id": _opaque_id(w.world_id, cell),
                    "packet": _packet_for_cell(w, cell),
                }
            )
    random.Random(SEED + 21).shuffle(rows)
    return rows


def hidden_key() -> dict[str, Any]:
    return {
        _opaque_id(w.world_id, cell): {
            "world_id": w.world_id,
            "cell": cell,
            "provenance_linked": cell[1] == "1",
            "history_sensitive": cell[3] == "1",
            "expected_specific_criticism": cell == "P1H1",
            "oracle_intervention": w.intervention,
            "oracle_direction": "different",
        }
        for w in selected_worlds()
        for cell in CELLS
    }
