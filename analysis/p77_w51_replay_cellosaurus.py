"""Replay Ikeda et al. 2025 Cellosaurus evaluation from published files.

Reference and archived outputs: Zenodo 10.5281/zenodo.14881142.
Usage: python analysis/p77_w51_replay_cellosaurus.py INPUT_DIRECTORY
This scores saved outputs. It does not run a mapping pipeline or model.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


FILES = {
    "gold_standard.tsv": "c9edfb4bea76656a22dd095b0d1eb4d3",
    "result_metasra.tsv": "1b06e0478a3014fa99991d7901c16db4",
    "result_llm_assisted.tsv": "90a11f62706353f226c9d36d161080d8",
    "testset.json": "ae35e7a975c397b13fb729d3e76adedd",
}
PREFIX = "biosample_cellosaurus_mapping_"
BIOPROJECT = re.compile(r"\bPRJ(?:NA|EB|DB)\d+\b")


def keyed(rows, key, source):
    by_id = {}
    for row in rows:
        accession = row[key]
        if not accession or accession in by_id:
            raise ValueError(f"{source}: missing or duplicate accession {accession!r}")
        by_id[accession] = row
    return by_id


def load_inputs(directory):
    paths = {name: directory / (PREFIX + name) for name in FILES}
    fixity = {}
    for name, expected in FILES.items():
        data = paths[name].read_bytes()
        actual = hashlib.md5(data).hexdigest()
        if actual != expected:
            raise ValueError(f"{name}: expected Zenodo MD5 {expected}, got {actual}")
        fixity[name] = {"bytes": len(data), "md5": actual,
                        "sha256": hashlib.sha256(data).hexdigest()}
    tables = {}
    for name, path in paths.items():
        with path.open(encoding="utf-8", newline="") as stream:
            if name.endswith(".tsv"):
                # Quotation marks are literal inside the authors' TSV fields.
                tables[name] = keyed(csv.DictReader(stream, delimiter="\t",
                                                   quoting=csv.QUOTE_NONE),
                                     "BioSample ID", name)
            else:
                tables[name] = keyed(json.load(stream), "accession", name)
    return tables, fixity


def outcome(answer, prediction):
    if answer == prediction:
        return "correct_id" if answer else "correct_blank"
    if not prediction:
        return "missed_id"
    return "wrong_id" if answer else "unexpected_id"


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def metrics(records, predict):
    categories = Counter(outcome(r["reference"], predict(r)) for r in records)
    correct = categories["correct_id"]
    wrong = categories["wrong_id"]
    return {
        "n": len(records), "outcomes": dict(sorted(categories.items())),
        "exact_accuracy": ratio(correct + categories["correct_blank"], len(records)),
        "id_precision": ratio(correct, correct + wrong + categories["unexpected_id"]),
        "id_recall": ratio(correct, correct + wrong + categories["missed_id"]),
    }


def replay(tables):
    gold, meta, llm, inputs = (tables[name] for name in FILES)
    for table in (meta, llm, inputs):
        if table.keys() != gold.keys():
            raise ValueError("Published input/reference/output accession sets differ")
    records = []
    for accession, g in gold.items():
        m, l = meta[accession], llm[accession]
        answer = g["mapping answer ID"]
        if answer != m["Gold standard Cellosaurus term ID"] or answer != l["Gold standard Cellosaurus term ID"]:
            raise ValueError(f"{accession}: inconsistent reference IDs")
        reference_kind = "reference_id" if answer else (
            "named_without_id" if g["extraction answer"] else "no_reference_name"
        )
        records.append({"reference": answer, "reference_kind": reference_kind,
                        "experiment": "ATAC-Seq" if g["Experiment type"] == "ATAC-Seq" else "ChIP-Seq",
                        "metasra": m["Mapped Cellosaurus term ID"], "llm": l["Final output"]})

    paired = Counter((r["metasra"] == r["reference"], r["llm"] == r["reference"])
                     for r in records)
    methods = {
        "metasra": lambda r: r["metasra"],
        "llm_assisted": lambda r: r["llm"],
        "metasra_then_llm_if_blank": lambda r: r["metasra"] or r["llm"],
        "llm_then_metasra_if_blank": lambda r: r["llm"] or r["metasra"],
        "agree_on_id": lambda r: r["metasra"] if r["metasra"] == r["llm"] else "",
    }
    groups = {
        "all": records,
        **{kind: [r for r in records if r["reference_kind"] == kind]
           for kind in ("reference_id", "named_without_id", "no_reference_name")},
        **{kind: [r for r in records if r["experiment"] == kind]
           for kind in ("ATAC-Seq", "ChIP-Seq")},
    }
    return {
        "shared_accessions": len(records),
        "raw_records_with_explicit_bioproject_token": sum(
            bool(BIOPROJECT.search(json.dumps(record))) for record in inputs.values()
        ),
        "paired_exactness": {f"metasra_{m}_llm_{l}": n for (m, l), n in sorted(paired.items())},
        "metrics": {group: {name: metrics(rows, predict) for name, predict in methods.items()}
                    for group, rows in groups.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_directory", type=Path)
    args = parser.parse_args()
    tables, fixity = load_inputs(args.input_directory)
    print(json.dumps({"fixity": fixity, **replay(tables)}, indent=2))


if __name__ == "__main__":
    main()
