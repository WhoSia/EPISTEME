from __future__ import annotations

import hashlib
import random
from typing import Any

from p16_packets import worlds

SEED = 20260919
P20_TAG = "P20-PxH-FACTORIAL"
CELLS = ("P0H0", "P0H1", "P1H0", "P1H1")


def _opaque_id(world_id: str, cell: str) -> str:
    raw = f"{SEED}:{P20_TAG}:{world_id}:{cell}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def _packet_for_cell(w, cell: str) -> dict[str, Any]:
    provenance_linked = cell[1] == "1"
    history_sensitive = cell[3] == "1"
    key = f"k20-{w.world_id.lower()}"
    unlinked = f"z20-{w.world_id.lower()}"

    packet = {
        "archive_id": _opaque_id(w.world_id, cell),
        "claim": w.terminal_claim,
        "terminal_observation": {
            w.history_a: "T=stable",
            w.history_b: "T=stable",
        },
        "available_interventions": [w.intervention, "uX", "uY"],
        "retained_history": [
            {"history": w.history_a, "trace": [key, "p2", "p3"]},
            {"history": w.history_b, "trace": [f"{key}-alt", "p2", "p3"]},
        ],
        "relation_notes": [
            {
                # The visible key token is held constant in every cell.
                # Only source identity changes whether the relation is provenance-linked.
                "source": key if provenance_linked else unlinked,
                "visible_key": key,
                "intervention": w.intervention,
                "response_link": "history-sensitive" if history_sensitive else "history-invariant",
            },
            {
                "source": "distractor-p20",
                "visible_key": "distractor-p20",
                "intervention": "uX",
                "response_link": "irrelevant",
            },
        ],
        "instructions": (
            "Using only this archive, propose the single strongest admissible experiment "
            "that could falsify the claim. A relation licenses a specific counterexample "
            "only when its source is actually linked to retained provenance and the relation "
            "is history-sensitive. Mere token visibility is not provenance linkage. If those "
            "conditions are not jointly satisfied, answer NONE. Do not speculate beyond "
            "retained evidence."
        ),
        "surface_domain": w.skin,
    }
    return packet


def selected_worlds():
    # Four frozen isomorphic worlds, one per surface rotation.
    # Cell assignment is crossed within each world.
    return worlds()[:4]


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in selected_worlds():
        for cell in CELLS:
            rows.append({
                "packet_id": _opaque_id(w.world_id, cell),
                "packet": _packet_for_cell(w, cell),
            })
    random.Random(SEED + 20).shuffle(rows)
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
