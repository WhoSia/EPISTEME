from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable

from generators import constraint_witness_generator, graph_cut_generator

SEED = 20260919


@dataclass(frozen=True)
class WorldSpec:
    world_id: str
    audit_class: str
    family: str
    terminal: str
    baseline: int
    intervention: str
    true_contrast: int


CRITICAL_FAMILIES = [
    "phase_lag",
    "branch_residue",
    "reset_memory",
    "cross_cancel",
    "threshold_delay",
    "context_remap",
    "merge_origin",
    "direction_coupling",
]


def build_worlds() -> list[WorldSpec]:
    worlds: list[WorldSpec] = []

    for i, family in enumerate(CRITICAL_FAMILIES, 1):
        worlds.append(
            WorldSpec(
                world_id=f"K{i:02d}",
                audit_class="critical",
                family=family,
                terminal=f"o{i % 3}",
                baseline=50 + i,
                intervention=f"u{i % 4}",
                true_contrast=(1 if i % 2 else -1) * (5 + i),
            )
        )

    for i in range(1, 6):
        worlds.append(
            WorldSpec(
                world_id=f"R{i:02d}",
                audit_class="recoverable",
                family=f"recover_{i}",
                terminal=f"o{i % 3}",
                baseline=70 + i,
                intervention=f"v{i % 4}",
                true_contrast=(1 if i % 2 else -1) * (3 + i),
            )
        )

    for i in range(1, 6):
        worlds.append(
            WorldSpec(
                world_id=f"N{i:02d}",
                audit_class="null",
                family=f"null_{i}",
                terminal=f"o{i % 3}",
                baseline=80 + i,
                intervention=f"w{i % 4}",
                true_contrast=0,
            )
        )

    return worlds


def _stretch_path(packet: Dict[str, Any], source: str, length: int = 4) -> None:
    intervention = packet["intervention"]
    new_edges = []
    replaced = False

    for edge in packet["edges"]:
        src, dst, edge_type, value = edge
        if src == source and dst == intervention:
            replaced = True
            continue
        new_edges.append(edge)

    if not replaced:
        return

    previous = source
    for idx in range(length - 1):
        node = f"q{idx}"
        packet["nodes"].append(node)
        new_edges.append((previous, node, f"qE{idx}", 1))
        previous = node

    new_edges.append((previous, intervention, f"qE{length - 1}", 1))
    packet["edges"] = new_edges


def make_packet(world: WorldSpec, retention: str) -> Dict[str, Any]:
    h1, h2 = "n0", "n1"
    terminal, feature, aggregate = "n2", "n3", "n4"
    intervention, response, decoy = "n5", "n6", "n7"

    nodes = [h1, h2, terminal, feature, aggregate, intervention, response, decoy]
    edges = [
        (h1, terminal, "e0", 1),
        (h2, terminal, "e0", 1),
    ]

    if retention == "R":
        edges += [
            (h1, feature, "e1", 1),
            (h2, feature, "e1", -1),
            (feature, intervention, "e2", 1),
            (intervention, response, "e3", world.true_contrast),
            (h1, decoy, "e4", 1),
            (h2, decoy, "e4", -1),
        ]
    elif retention == "C":
        if world.audit_class == "recoverable":
            edges += [
                (h1, aggregate, "e5", 1),
                (h2, aggregate, "e5", -1),
                (aggregate, intervention, "e6", 1),
                (intervention, response, "e3", world.true_contrast),
            ]
        else:
            edges += [
                (h1, aggregate, "e5", 1),
                (h2, aggregate, "e5", 1),
                (h1, decoy, "e4", 1),
                (h2, decoy, "e4", -1),
                (intervention, response, "e3", world.true_contrast),
            ]
    elif retention == "S":
        nodes += ["n8", "n9"]
        edges += [
            (h1, decoy, "e4", 1),
            (h2, decoy, "e4", -1),
            (decoy, "n8", "e7", 1),
            ("n9", intervention, "e8", 1),
            (intervention, response, "e3", world.true_contrast),
        ]
    else:
        raise ValueError(f"unknown retention: {retention}")

    packet: Dict[str, Any] = {
        "world_id": world.world_id,
        "retention": retention,
        "terminal": terminal,
        "baseline": world.baseline,
        "histories": [h1, h2],
        "intervention": intervention,
        "response": response,
        "nodes": nodes,
        "edges": edges,
    }

    # Two presealed disagreements make cross-generator concordance informative
    # rather than tautologically perfect.
    if world.world_id == "K04" and retention == "R":
        _stretch_path(packet, "n3", length=4)
    if world.world_id == "R03" and retention == "C":
        _stretch_path(packet, "n4", length=4)

    return packet


def execute() -> Dict[str, Any]:
    random.seed(SEED)
    worlds = build_worlds()
    records = []

    for world in worlds:
        for retention in ("R", "C", "S"):
            packet = make_packet(world, retention)

            records.append(
                {
                    "world_id": world.world_id,
                    "audit_class": world.audit_class,
                    "retention": retention,
                    "g_graph_cut": graph_cut_generator(packet),
                    "g_constraint": constraint_witness_generator(packet),
                    "true_contrast": world.true_contrast,
                }
            )

    return {
        "seed": SEED,
        "world_count": len(worlds),
        "packet_count": len(records),
        "records": records,
    }


def summarize(payload: Dict[str, Any]) -> Dict[str, Any]:
    records = payload["records"]
    summary: Dict[str, Dict[str, int]] = {}

    for audit_class in ("critical", "recoverable", "null"):
        for retention in ("R", "C", "S"):
            subset = [
                row for row in records
                if row["audit_class"] == audit_class and row["retention"] == retention
            ]
            summary[f"{audit_class}:{retention}"] = {
                "n": len(subset),
                "graph_cut": sum(bool(row["g_graph_cut"]) for row in subset),
                "constraint": sum(bool(row["g_constraint"]) for row in subset),
            }

    concordant = sum(
        row["g_graph_cut"] == row["g_constraint"]
        for row in records
    )
    summary["cross_generator"] = {
        "n": len(records),
        "concordant": concordant,
        "discordant": len(records) - concordant,
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print full ephemeral ledger")
    args = parser.parse_args()

    payload = execute()
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(summarize(payload), indent=2))


if __name__ == "__main__":
    main()
