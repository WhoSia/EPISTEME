"""Read-only validator for public nbreznau/CRI data/cri_team.csv.

Checks table grain, source-schema drift and team-zero inclusion; it does NOT
reproduce 1,253 model estimates, settle ISSP survey rights or test AI adapters.
"""
import argparse
import csv
import io
import json
from collections import Counter
from pathlib import Path

EXPECTED = {
    "rows": 89,
    "columns": 464,
    "distinct_ids_including_team_zero": 73,
    "nonzero_team_rows": 88,
    "distinct_ids_excluding_team_zero": 72,
    "numeric_ame_rows": 88,
    "missing_ame_rows": 1,
    "hresult_counts": {"No test": 11, "Reject": 55, "Support": 23},
}


def audit(raw: str) -> dict:
    reader = csv.DictReader(io.StringIO(raw))
    fields = reader.fieldnames or []
    if len(fields) != len(set(fields)):
        raise ValueError("Duplicated header names")
    necessary = {"u_teamid", "AME", "Hresult"}
    if not necessary.issubset(fields):
        raise ValueError(f"Required fields missing: {necessary-set(fields)}")
    rows = list(reader)
    if any(None in row or any(x is None for x in row.values()) for row in rows):
        raise ValueError("CSV column count inconsistent")
    ids = [row["u_teamid"] for row in rows]
    counts = Counter(row["Hresult"] for row in rows)
    n_numeric = 0
    for row in rows:
        value = row["AME"].strip()
        if value and value.upper() != "NA":
            float(value)
            n_numeric += 1
    return {
        "rows": len(rows),
        "columns": len(fields),
        "distinct_ids_including_team_zero": len(set(ids)),
        "nonzero_team_rows": sum(x != "0" for x in ids),
        "distinct_ids_excluding_team_zero": len(set(ids)-{"0"}),
        "numeric_ame_rows": n_numeric,
        "missing_ame_rows": len(rows)-n_numeric,
        "hresult_counts": dict(sorted(counts.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sample = 'u_teamid,AME,Hresult,note\n0,0.1,Reject,"x,y"\n1,NA,No test,none\n1,0.2,Support,same\n'
        result = audit(sample)
        assert result["rows"] == 3 and result["columns"] == 4
        assert result["distinct_ids_excluding_team_zero"] == 1
        assert result["missing_ame_rows"] == 1
        assert result["hresult_counts"] == {"No test": 1, "Reject": 1, "Support": 1}
        print("PASS synthetic parser tests; no original R rerun")
        return
    if args.csv_path is None:
        parser.error("Provide local original CSV or --self-test")
    result = audit(args.csv_path.read_text(encoding="utf-8-sig"))
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    mismatch = {k: {"expected": v, "actual": result[k]} for k, v in EXPECTED.items() if result[k] != v}
    if mismatch:
        raise SystemExit("SOURCE STRUCTURAL DRIFT: " + json.dumps(mismatch))
    print("PASS original team-level source structure (NOT published model reproduction)")


if __name__ == "__main__":
    main()
