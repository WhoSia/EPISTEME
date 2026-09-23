from __future__ import annotations

import hashlib
import random
from typing import Any

from p16_packets import worlds

SEED = 20260923
P22_TAG = "P22-CROSS-REPRESENTATION"
REPRESENTATIONS = ("canonical", "alpha_permuted", "minimal")
SEMANTICS = ("valid", "null")


def _opaque_id(world_id: str, representation: str, semantic: str) -> str:
    raw = f"{SEED}:{P22_TAG}:{world_id}:{representation}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def selected_worlds():
    return worlds()[:4]


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
    key = f"k22-{w.world_id.lower()}c"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key, "p2", "p3"]},
        {"history": w.history_b, "trace": [f"{key}-alt", "p2", "p3"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": (
                "history-sensitive" if semantic == "valid" else "history-invariant"
            ),
        },
        {"source": "distractor-c", "intervention": "uX", "response_link": "irrelevant"},
    ]
    return packet


def _alpha_permuted(w, semantic: str) -> dict[str, Any]:
    # Same latent provenance-relation graph as canonical, but identifiers,
    # list order, and trace order are changed without changing semantics.
    key = f"zeta-{w.world_id.lower()}"
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
            "response_link": (
                "history-sensitive" if semantic == "valid" else "history-invariant"
            ),
        },
    ]
    return packet


def _minimal(w, semantic: str) -> dict[str, Any]:
    # Candidate minimal sufficient archive: only the provenance contrast and
    # its target relation survive; terminal observation/intervention vocabulary
    # remain unchanged.
    key = f"m22-{w.world_id.lower()}"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key]},
        {"history": w.history_b, "trace": [f"{key}-alt"]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": (
                "history-sensitive" if semantic == "valid" else "history-invariant"
            ),
        }
    ]
    return packet


def _minimal_no_provenance(w) -> dict[str, Any]:
    # Necessity ablation for minimality: preserve the target relation wording
    # but erase the history-discriminating provenance contrast.
    key = f"m22-{w.world_id.lower()}"
    packet = _base(w)
    packet["retained_history"] = [
        {"history": w.history_a, "trace": [key]},
        {"history": w.history_b, "trace": [key]},
    ]
    packet["relation_notes"] = [
        {
            "source": key,
            "intervention": w.intervention,
            "response_link": "history-sensitive",
        }
    ]
    return packet


def build_packet(w, representation: str, semantic: str) -> dict[str, Any]:
    if representation == "canonical":
        packet = _canonical(w, semantic)
    elif representation == "alpha_permuted":
        packet = _alpha_permuted(w, semantic)
    elif representation == "minimal":
        packet = _minimal(w, semantic)
    else:
        raise ValueError(representation)
    packet["archive_id"] = _opaque_id(w.world_id, representation, semantic)
    return packet


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in selected_worlds():
        for representation in REPRESENTATIONS:
            for semantic in SEMANTICS:
                rows.append({
                    "packet_id": _opaque_id(w.world_id, representation, semantic),
                    "packet": build_packet(w, representation, semantic),
                })

        ablation_id = _opaque_id(w.world_id, "minimal", "no_provenance")
        packet = _minimal_no_provenance(w)
        packet["archive_id"] = ablation_id
        rows.append({"packet_id": ablation_id, "packet": packet})

    random.Random(SEED + 22).shuffle(rows)
    return rows


def hidden_key() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for w in selected_worlds():
        for representation in REPRESENTATIONS:
            for semantic in SEMANTICS:
                out[_opaque_id(w.world_id, representation, semantic)] = {
                    "world_id": w.world_id,
                    "representation": representation,
                    "semantic_class": semantic,
                    "equivalence_class": (
                        "WITNESS_VALID" if semantic == "valid" else "WITNESS_NULL"
                    ),
                    "expected_specific_criticism": semantic == "valid",
                    "oracle_intervention": w.intervention,
                    "oracle_direction": "different",
                }
        out[_opaque_id(w.world_id, "minimal", "no_provenance")] = {
            "world_id": w.world_id,
            "representation": "minimal",
            "semantic_class": "no_provenance",
            "equivalence_class": "WITNESS_INSUFFICIENT",
            "expected_specific_criticism": False,
            "oracle_intervention": w.intervention,
            "oracle_direction": "different",
        }
    return out
