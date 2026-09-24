from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

WORLDS = ("W04", "W05", "W06")

FAIL_SETS = {
    "W04": {
        "F_H_T", "F_L", "H", "H_L", "H_T_L", "R_F_H_T_L",
        "R_H_L", "R_H_T", "R_H_T_L",
    },
    "W05": {
        "F_H_T_L", "H", "H_T_L", "R", "R_F", "R_F_H",
        "R_F_H_T", "R_F_L", "R_H_T", "R_L", "R_T", "R_T_L", "T",
    },
    "W06": {
        "F_H_T_L", "F_L", "F_T_L", "H", "H_L", "H_T_L",
        "R_F_H_L", "R_F_L", "R_H", "R_H_L", "R_H_T",
        "R_H_T_L", "R_L", "R_T_L", "T",
    },
}

VERTICES = (
    "I","R","F","H","T","L","R_F","R_H","R_T","R_L",
    "F_H","F_T","F_L","H_T","H_L","T_L","R_F_H","R_F_T",
    "R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L",
    "H_T_L","R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L",
    "F_H_T_L","R_F_H_T_L",
)


def gf2_rank(rows: list[list[int]]) -> int:
    a = [row[:] for row in rows]
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for i in range(m):
            if i != rank and a[i][col]:
                a[i] = [x ^ y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == m:
            break
    return rank


def main() -> None:
    signatures: dict[str, tuple[int, int, int]] = {}
    classes: dict[tuple[int, int, int], list[str]] = defaultdict(list)

    for vertex in VERTICES:
        sig = tuple(int(vertex in FAIL_SETS[w]) for w in WORLDS)
        signatures[vertex] = sig
        classes[sig].append(vertex)

    persistent_fail = sorted(classes.get((1, 1, 1), []))
    persistent_pass = sorted(classes.get((0, 0, 0), []))
    interaction_shell = sorted(
        v for v, sig in signatures.items()
        if sig not in {(0, 0, 0), (1, 1, 1)}
    )

    matrix = [
        [int(v in FAIL_SETS[w]) for v in VERTICES]
        for w in WORLDS
    ]

    world_hamming = {
        "W04-W05": sum(a != b for a, b in zip(matrix[0], matrix[1])),
        "W04-W06": sum(a != b for a, b in zip(matrix[0], matrix[2])),
        "W05-W06": sum(a != b for a, b in zip(matrix[1], matrix[2])),
    }

    class_rows = {
        "".join(map(str, sig)): sorted(vertices)
        for sig, vertices in sorted(classes.items())
    }

    result = {
        "stage": "EPISTEME-P28",
        "tensor": {
            "shape": [3, 32],
            "world_order": list(WORLDS),
            "failure_counts": {w: len(FAIL_SETS[w]) for w in WORLDS},
            "gf2_row_rank": gf2_rank(matrix),
            "world_pair_hamming_distance": world_hamming,
        },
        "persistent_core_collapse": {
            "persistent_pass_core": persistent_pass,
            "persistent_pass_count": len(persistent_pass),
            "persistent_fail_core": persistent_fail,
            "persistent_fail_count": len(persistent_fail),
            "context_sensitive_interaction_shell": interaction_shell,
            "interaction_shell_count": len(interaction_shell),
        },
        "coarsest_exact_representation_quotient": {
            "class_count": len(classes),
            "classes_by_failure_signature_W04_W05_W06": class_rows,
            "minimality_certificate": (
                "Two representation vertices can be merged iff their complete W04/W05/W06 "
                "failure signatures are identical. Distinct signatures differ in at least "
                "one observed context, so any coarser quotient would lose exact transport."
            ),
        },
        "coarsest_exact_context_quotient": {
            "class_count": 3,
            "classes": [["W04"], ["W05"], ["W06"]],
            "minimality_certificate": (
                "All three world rows are distinct; their pairwise Hamming distances are "
                "strictly positive, so no pair of contexts can be merged under an exact law."
            ),
        },
        "minimal_context_indexed_transport_law": {
            "representation_state": (
                "the 3-bit failure signature sigma(r)=(Y_W04(r),Y_W05(r),Y_W06(r))"
            ),
            "context_state": "one of the three irreducible held-out world classes",
            "law": "Y(W_i,r)=sigma(r)_i",
            "representation_classes_needed": 7,
            "context_classes_needed": 3,
            "world_invariant_classes": ["000", "111"],
            "context_dependent_classes": ["001", "010", "011", "100", "101"],
        },
        "factorization": {
            "representation_only": False,
            "world_shift_xor": False,
            "world_representation_tensor_gf2_rank": gf2_rank(matrix),
            "classification": "MINIMAL_CONTEXT_INDEXED_NONSEPARABLE_TRANSPORT",
        },
        "authority": (
            "Exact only on Gemini over W04-W06 and the frozen 32-vertex representation cube. "
            "This is a deterministic quotient/compression result from sealed P27 data; no new "
            "model calls and no behavioral SVEC promotion."
        ),
    }

    Path("active/p28_result.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
