from __future__ import annotations

import hashlib
import random
from typing import Any

from p16_packets import worlds

SEED = 20260919
P19_TAG = "P19-MATCHED-C"


def _opaque_id(world_id: str) -> str:
    raw = f"{SEED}:{P19_TAG}:{world_id}:C".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def _packet_for_world(w) -> dict[str, Any]:
    packet = {
        "archive_id": _opaque_id(w.world_id),
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

    if w.audit_class == "critical":
        # No surviving counterexample witness.
        packet["retained_history"] = [
            {"history": w.history_a, "trace": ["aggregate-A", "p2", "p3"]},
            {"history": w.history_b, "trace": ["aggregate-A", "p2", "p3"]},
        ]
        packet["relation_notes"] = [
            {"source": "aggregate-A", "intervention": "uX", "response_link": "irrelevant"},
            {"source": "distractor-c", "intervention": "uY", "response_link": "irrelevant"},
        ]

    elif w.audit_class == "recoverable":
        # Matched positive control: the coarse witness is present in both provenance
        # traces and relation notes, mirroring the grounding structure of Rich.
        ck = w.coarse_key
        packet["retained_history"] = [
            {"history": w.history_a, "trace": [ck, "p2", "p3"]},
            {"history": w.history_b, "trace": [f"{ck}-alt", "p2", "p3"]},
        ]
        packet["relation_notes"] = [
            {
                "source": ck,
                "intervention": w.intervention,
                "response_link": "history-sensitive",
            },
            {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
        ]

    elif w.audit_class == "null":
        # Matched structural negative control: provenance linkage is equally explicit,
        # but the relation is history-invariant, so no falsifying contrast is licensed.
        nk = f"k{w.world_id[1:]}c"
        packet["retained_history"] = [
            {"history": w.history_a, "trace": [nk, "p2", "p3"]},
            {"history": w.history_b, "trace": [f"{nk}-alt", "p2", "p3"]},
        ]
        packet["relation_notes"] = [
            {
                "source": nk,
                "intervention": w.intervention,
                "response_link": "history-invariant",
            },
            {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
        ]

    else:
        raise ValueError(w.audit_class)

    return packet


def blinded_packets() -> list[dict[str, Any]]:
    rows = [{"packet_id": _opaque_id(w.world_id), "packet": _packet_for_world(w)} for w in worlds()]
    random.Random(SEED + 19).shuffle(rows)
    return rows


def hidden_key() -> dict[str, Any]:
    return {
        _opaque_id(w.world_id): {
            "world_id": w.world_id,
            "audit_class": w.audit_class,
            "retention": "C",
            "oracle_intervention": w.intervention,
            "oracle_direction": w.oracle_direction,
        }
        for w in worlds()
    }
