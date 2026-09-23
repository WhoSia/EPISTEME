from __future__ import annotations

import hashlib
import random
from typing import Any

from p16_packets import worlds

SEED = 20260923
P23_TAG = "P23-FAILURE-GEOMETRY"

REPRESENTATIONS = (
    "canonical",
    "rename_only",
    "history_order_only",
    "trace_order_only",
    "relation_order_only",
    "alpha_full",
    "minimal",
)
SEMANTICS = ("valid", "null")
ABLATIONS = (
    "minimal_no_provenance",
    "minimal_no_source_join",
    "minimal_no_intervention",
)


def _opaque_id(world_id: str, family: str, semantic: str) -> str:
    raw = f"{SEED}:{P23_TAG}:{world_id}:{family}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def selected_worlds():
    # P23 is diagnostic rather than promotion-bearing; three worlds keep the
    # geometry tractable while preserving cross-world replication.
    return worlds()[:3]


def _base(w) -> dict[str, Any]:
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


def _canonical(w, semantic: str) -> dict[str, Any]:
    key = f"k23-{w.world_id.lower()}c"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key, "p2", "p3"]},
        {"history": w.history_b, "trace": [f"{key}-alt", "p2", "p3"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        },
        {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
    ]
    return packet


def _rename_only(w, semantic: str) -> dict[str, Any]:
    key = f"zeta23-{w.world_id.lower()}"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key, "p2", "p3"]},
        {"history": w.history_b, "trace": [f"{key}-alt", "p2", "p3"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        },
        {"source": "decoy-z", "intervention": "uX", "response_link": "irrelevant"},
    ]
    return packet


def _history_order_only(w, semantic: str) -> dict[str, Any]:
    key = f"k23-{w.world_id.lower()}c"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_b, "trace": [f"{key}-alt", "p2", "p3"]},
        {"history": w.history_a, "trace": [key, "p2", "p3"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        },
        {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
    ]
    return packet


def _trace_order_only(w, semantic: str) -> dict[str, Any]:
    key = f"k23-{w.world_id.lower()}c"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": ["p2", "p3", key]},
        {"history": w.history_b, "trace": ["p2", "p3", f"{key}-alt"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        },
        {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
    ]
    return packet


def _relation_order_only(w, semantic: str) -> dict[str, Any]:
    key = f"k23-{w.world_id.lower()}c"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key, "p2", "p3"]},
        {"history": w.history_b, "trace": [f"{key}-alt", "p2", "p3"]},
    ]
    packet["relation_notes"] = [
        {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        },
    ]
    return packet


def _alpha_full(w, semantic: str) -> dict[str, Any]:
    key = f"zeta23-{w.world_id.lower()}"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_b, "trace": ["q9", "q4", f"{key}-alt"]},
        {"history": w.history_a, "trace": ["q9", "q4", key]},
    ]
    packet["relation_notes"] = [
        {"source": "decoy-z", "intervention": "uX", "response_link": "irrelevant"},
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        },
    ]
    return packet


def _minimal(w, semantic: str) -> dict[str, Any]:
    key = f"m23-{w.world_id.lower()}"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key]},
        {"history": w.history_b, "trace": [f"{key}-alt"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive" if semantic == "valid" else "history-invariant",
        }
    ]
    return packet


def build_representation(w, family: str, semantic: str) -> dict[str, Any]:
    fn = {
        "canonical": _canonical,
        "rename_only": _rename_only,
        "history_order_only": _history_order_only,
        "trace_order_only": _trace_order_only,
        "relation_order_only": _relation_order_only,
        "alpha_full": _alpha_full,
        "minimal": _minimal,
    }[family]
    packet = fn(w, semantic)
    packet["archive_id"] = _opaque_id(w.world_id, family, semantic)
    return packet


def build_ablation(w, ablation: str) -> dict[str, Any]:
    key = f"m23-{w.world_id.lower()}"
    packet = _base(w)

    if ablation == "minimal_no_provenance":
        packet["retained_history"] = [
            {"history": w.history_a, "trace": [key]},
            {"history": w.history_b, "trace": [key]},
        ]
        packet["relation_notes"] = [
            {"source": key, "intervention": w.intervention, "response_link": "history-sensitive"}
        ]

    elif ablation == "minimal_no_source_join":
        packet["retained_history"] = [
            {"history": w.history_a, "trace": [key]},
            {"history": w.history_b, "trace": [f"{key}-alt"]},
        ]
        packet["relation_notes"] = [
            {"source": f"unjoined-{key}", "intervention": w.intervention, "response_link": "history-sensitive"}
        ]

    elif ablation == "minimal_no_intervention":
        packet["available_interventions"] = ["uX", "uY"]
        packet["retained_history"] = [
            {"history": w.history_a, "trace": [key]},
            {"history": w.history_b, "trace": [f"{key}-alt"]},
        ]
        packet["relation_notes"] = [
            {"source": key, "intervention": w.intervention, "response_link": "history-sensitive"}
        ]

    else:
        raise ValueError(ablation)

    packet["archive_id"] = _opaque_id(w.world_id, ablation, "ablation")
    return packet


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in selected_worlds():
        for family in REPRESENTATIONS:
            for semantic in SEMANTICS:
                rows.append({
                    "packet_id": _opaque_id(w.world_id, family, semantic),
                    "packet": build_representation(w, family, semantic),
                })

        for ablation in ABLATIONS:
            rows.append({
                "packet_id": _opaque_id(w.world_id, ablation, "ablation"),
                "packet": build_ablation(w, ablation),
            })

    random.Random(SEED + 23).shuffle(rows)
    return rows


def hidden_key() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for w in selected_worlds():
        for family in REPRESENTATIONS:
            for semantic in SEMANTICS:
                out[_opaque_id(w.world_id, family, semantic)] = {
                    "world_id": w.world_id,
                    "family": family,
                    "semantic_class": semantic,
                    "expected_specific_criticism": semantic == "valid",
                    "oracle_intervention": w.intervention,
                    "oracle_direction": "different",
                }

        for ablation in ABLATIONS:
            out[_opaque_id(w.world_id, ablation, "ablation")] = {
                "world_id": w.world_id,
                "family": ablation,
                "semantic_class": "ablation",
                "expected_specific_criticism": False,
                "oracle_intervention": w.intervention,
                "oracle_direction": "different",
            }
    return out
