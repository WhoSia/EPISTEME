from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any

SEED = 20260919


@dataclass(frozen=True)
class CanonicalWorld:
    world_id: str
    audit_class: str   # critical | recoverable | null
    skin: str          # surface narrative only; mechanism remains isomorphic
    terminal_claim: str
    history_a: str
    history_b: str
    intervention: str
    rich_key: str
    coarse_key: str | None
    oracle_direction: str


SKINS = (
    "measurement-pipeline",
    "analysis-pipeline",
    "sample-handling",
)


def worlds() -> list[CanonicalWorld]:
    out: list[CanonicalWorld] = []
    idx = 0

    # Six critical worlds: only rich retains a valid counterexample key.
    for i in range(6):
        idx += 1
        out.append(
            CanonicalWorld(
                world_id=f"W{idx:02d}",
                audit_class="critical",
                skin=SKINS[i % len(SKINS)],
                terminal_claim="The retained terminal summary is sufficient to predict the challenge response.",
                history_a=f"h{idx}a",
                history_b=f"h{idx}b",
                intervention=f"u{(i % 4) + 1}",
                rich_key=f"k{idx}r",
                coarse_key=None,
                oracle_direction="different",
            )
        )

    # Three recoverable controls: coarse retains an equivalent sufficient key.
    for i in range(3):
        idx += 1
        out.append(
            CanonicalWorld(
                world_id=f"W{idx:02d}",
                audit_class="recoverable",
                skin=SKINS[(i + 1) % len(SKINS)],
                terminal_claim="The retained terminal summary is sufficient to predict the challenge response.",
                history_a=f"h{idx}a",
                history_b=f"h{idx}b",
                intervention=f"u{(i % 4) + 1}",
                rich_key=f"k{idx}r",
                coarse_key=f"k{idx}c",
                oracle_direction="different",
            )
        )

    # Three null controls: rich carries detailed history but no genuine defeating relation.
    for i in range(3):
        idx += 1
        out.append(
            CanonicalWorld(
                world_id=f"W{idx:02d}",
                audit_class="null",
                skin=SKINS[(i + 2) % len(SKINS)],
                terminal_claim="The retained terminal summary is sufficient to predict the challenge response.",
                history_a=f"h{idx}a",
                history_b=f"h{idx}b",
                intervention=f"u{(i % 4) + 1}",
                rich_key=f"k{idx}r",
                coarse_key=None,
                oracle_direction="same",
            )
        )

    return out


def _opaque_id(world_id: str, retention: str) -> str:
    raw = f"{SEED}:{world_id}:{retention}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def _surface_text(w: CanonicalWorld, retention: str) -> dict[str, Any]:
    common = {
        "archive_id": _opaque_id(w.world_id, retention),
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
    }

    if retention == "R":
        common["retained_history"] = [
            {"history": w.history_a, "trace": [w.rich_key, "p2", "p3"]},
            {"history": w.history_b, "trace": [f"{w.rich_key}-alt", "p2", "p3"]},
        ]
        common["relation_notes"] = [
            {
                "source": w.rich_key,
                "intervention": w.intervention,
                "response_link": "history-sensitive" if w.audit_class != "null" else "history-invariant",
            },
            {"source": "distractor-r", "intervention": "uX", "response_link": "irrelevant"},
        ]

    elif retention == "C":
        common["retained_history"] = [
            {"history": w.history_a, "trace": ["aggregate-A"]},
            {"history": w.history_b, "trace": ["aggregate-A"]},
        ]
        notes = [{"source": "aggregate-A", "intervention": "uX", "response_link": "irrelevant"}]
        if w.audit_class == "recoverable":
            notes.append(
                {
                    "source": w.coarse_key,
                    "intervention": w.intervention,
                    "response_link": "history-sensitive",
                }
            )
        common["relation_notes"] = notes

    elif retention == "S":
        common["retained_history"] = [
            {"history": w.history_a, "trace": ["aggregate-A", "d1", "d2", "d3"]},
            {"history": w.history_b, "trace": ["aggregate-A", "d4", "d5", "d6"]},
        ]
        common["relation_notes"] = [
            {"source": "d1", "intervention": "uX", "response_link": "irrelevant"},
            {"source": "d4", "intervention": "uY", "response_link": "irrelevant"},
        ]
    else:
        raise ValueError(retention)

    # Surface skin changes wording only, not causal structure.
    common["surface_domain"] = w.skin
    return common


def blinded_packets() -> list[dict[str, Any]]:
    rows = []
    for w in worlds():
        for retention in ("R", "C", "S"):
            packet = _surface_text(w, retention)
            rows.append(
                {
                    "packet_id": packet["archive_id"],
                    "packet": packet,
                }
            )

    rng = random.Random(SEED)
    rng.shuffle(rows)
    return rows


def hidden_key() -> dict[str, Any]:
    # Never send this object to a generator.
    return {
        _opaque_id(w.world_id, retention): {
            "world_id": w.world_id,
            "audit_class": w.audit_class,
            "retention": retention,
            "oracle_intervention": w.intervention,
            "oracle_direction": w.oracle_direction,
        }
        for w in worlds()
        for retention in ("R", "C", "S")
    }


if __name__ == "__main__":
    print(json.dumps({"packets": blinded_packets()}, indent=2))
