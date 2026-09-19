from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable, Tuple

Packet = Dict[str, Any]


def _differing_history_nodes(packet: Packet) -> list[str]:
    h1, h2 = packet["histories"]
    by_target: dict[Tuple[str, str], dict[str, float]] = defaultdict(dict)

    for src, dst, edge_type, value in packet["edges"]:
        if src in (h1, h2):
            by_target[(dst, edge_type)][src] = value

    out = []
    for (dst, _edge_type), sig in by_target.items():
        if h1 in sig and h2 in sig and sig[h1] != sig[h2]:
            out.append(dst)
    return out


def graph_cut_generator(packet: Packet) -> bool:
    """Blind generator A.

    Emits a challenge only when a history distinction reaches the intervention
    through the retained graph and the intervention predicts a non-zero
    response contrast.
    """
    intervention = packet["intervention"]
    response = packet["response"]
    edges = packet["edges"]

    adjacency: dict[str, list[str]] = defaultdict(list)
    for src, dst, _edge_type, _value in edges:
        adjacency[src].append(dst)

    def reachable(start: str, target: str) -> bool:
        stack = [start]
        seen = set()
        while stack:
            node = stack.pop()
            if node == target:
                return True
            if node in seen:
                continue
            seen.add(node)
            stack.extend(adjacency.get(node, []))
        return False

    response_weight = sum(
        value
        for src, dst, _edge_type, value in edges
        if src == intervention and dst == response
    )

    return (
        response_weight != 0
        and any(reachable(node, intervention) for node in _differing_history_nodes(packet))
    )


def constraint_witness_generator(packet: Packet, max_depth: int = 3) -> bool:
    """Blind generator B.

    Uses a bounded local constraint witness rather than unrestricted graph
    reachability. This creates a deliberately non-identical generator.
    """
    intervention = packet["intervention"]
    response = packet["response"]
    edges = packet["edges"]

    links = {(src, dst) for src, dst, _edge_type, _value in edges}

    def reaches_within(start: str, target: str) -> bool:
        frontier = {start}
        for _ in range(max_depth):
            nxt = {dst for src, dst in links if src in frontier}
            if target in nxt:
                return True
            frontier = nxt
        return False

    response_values = [
        value
        for src, dst, _edge_type, value in edges
        if src == intervention and dst == response
    ]

    return bool(
        response_values
        and response_values[0] != 0
        and any(
            reaches_within(node, intervention)
            for node in _differing_history_nodes(packet)
        )
    )
