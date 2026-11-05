"""P77 W33: read-only BLADE soccer expert annotation grain auditor.

Run against original behavioral-data/BLADE/blade_bench/datasets/soccer/annotations.csv.
Counts specification records, NOT analyst subjects, experiments, valid scientific
claims or observed AI format-translation effects. No records are redistributed.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory

FIELDS = ("dependency_graph", "conceptual_spec_json", "transform_spec_json",
          "model_spec_json", "tisane_spec_json", "annotate_cvar_spec_json",
          "annotate_transform_spec_json")
EXPECTED = {"records": 98, "columns": 8,
            "nonempty": {"dependency_graph": 1, "conceptual_spec_json": 16,
                         "transform_spec_json": 40, "model_spec_json": 41,
                         "tisane_spec_json": 0, "annotate_cvar_spec_json": 0,
                         "annotate_transform_spec_json": 0}}


def audit(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        assert len(header) == len(set(header)), "Duplicate columns"
        assert "spec_id" in header and set(FIELDS).issubset(header)
        counts = Counter()
        records = 0
        for row in reader:
            assert None not in row and all(v is not None for v in row.values())
            assert row["spec_id"].strip()
            records += 1
            for name in FIELDS:
                if row[name].strip():
                    json.loads(row[name])
                    counts[name] += 1
    return {"records": records, "columns": len(header),
            "nonempty": {k: counts[k] for k in FIELDS}}


def synthetic_self_test() -> None:
    with TemporaryDirectory() as tmp:
        f = Path(tmp) / "test.csv"
        f.write_text("spec_id," + ",".join(FIELDS) + "\n"
                     'test_id,,"{""variable"":1}",,,,,\n', encoding="utf-8")
        actual = audit(f)
        assert actual["records"] == 1
        assert actual["nonempty"]["conceptual_spec_json"] == 1
    print("PASS: invented multiline/quoted JSON specification parser")
    print("LIMIT: not the complete expert annotations, nor AI or research result")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("original_annotations_csv", nargs="?", type=Path)
    args = p.parse_args()
    if args.original_annotations_csv is None:
        synthetic_self_test()
    else:
        observed = audit(args.original_annotations_csv)
        assert observed == EXPECTED, (observed, EXPECTED)
        print(json.dumps(observed, indent=2))
        print("PASS: source-level specification granularity, not scientific validity")
