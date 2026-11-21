"""W65: fail-closed manuscript provenance graph evidence admission gate.

A pinned original ZIP or a notebook code line is NOT execution evidence.
This only validates attestation shape. Even a passing graph still requires
independent source-byte and original-run verification before paper replication.

usage: python p77_w65_provenance_gate.py manually_reviewed_claims.json
"""
import json
import re
import sys
from pathlib import Path

EDGES = {
    "source_to_input": "source_bytes",
    "input_to_invocation": "run_trace",
    "invocation_to_output": "run_trace",
    "output_to_query": "query_trace",
    "query_to_confusion": "evaluation_trace",
    "confusion_to_workbook": "workbook_cell_trace",
    "workbook_to_paper": "publication_trace",
}
REQUIRED = ("edge", "source_ref", "target_ref", "evidence_uri", "sha256", "join_key")
RUNTIME = set(EDGES) - {"source_to_input"}


def gate(claims):
    if not isinstance(claims, list):
        raise ValueError("Claims must be a list")
    proven = {name: [] for name in EDGES}
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("Claim must be an object")
        for field in REQUIRED:
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                raise ValueError("Missing field: " + field)
        edge = claim["edge"]
        if edge not in EDGES:
            raise ValueError("Unknown provenance edge")
        if not re.fullmatch(r"[0-9a-f]{64}", claim["sha256"]):
            raise ValueError("Evidence hash must be lower-case SHA256")
        if claim.get("evidence_kind") != EDGES[edge]:
            raise ValueError("Evidence category does not prove claimed edge")
        if edge in RUNTIME:
            if not isinstance(claim.get("run_id"), str) or not claim["run_id"].strip():
                raise ValueError("Execution-related edge requires explicit run_id")
        if claim.get("reviewed") is not True:
            raise ValueError("Unreviewed evidence is not admitted")
        proven[edge].append(claim)

    missing = [edge for edge in EDGES if not proven[edge]]
    run_ids = {c["run_id"] for edge in RUNTIME for c in proven[edge]}
    return {
        "admissible_edge_counts": {edge: len(items) for edge, items in proven.items()},
        "missing_edges": missing,
        "candidate_run_ids": sorted(run_ids),
        "complete_single_run_attestation": not missing and len(run_ids) == 1,
        "warning": (
            "This schema gate cannot authenticate external evidence or resolve "
            "accidental label joins. Recheck every source byte and execution "
            "trace independently; a pass is not proof of the published result."
        ),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: p77_w65_provenance_gate.py reviewed_claims.json")
    print(json.dumps(gate(json.loads(Path(sys.argv[1]).read_text())), indent=2))
