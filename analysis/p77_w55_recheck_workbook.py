"""Audit the source workbook's three metric blocks against its own task sheets.

The six query tasks are three organ searches followed by three blood searches.
This reads the held original Zenodo v3 XLSX. It never assumes that equal column
headers imply matching row identities.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import openpyxl

ZENODO_V3_MD5 = "66fa6ffbf5470a73c9737f3d94470bbc"
SHEETS = {
    "BioSample": {
        "detail": "BioSample - GPT-4",
        "recall": (2, 3, 4),
        "precision": (11, 12, 13),
        "f1": (20, 21, 22),
    },
    "GEO": {
        "detail": "geo-gpt4",
        "recall": (6, 7, 8),
        "precision": (15, 16, 17),
        "f1": (24, 25, 26),
    },
}
QUERY_NAMES = (
    "ovary-organ",
    "liver-organ",
    "lung-organ",
    "ovary-blood",
    "liver-blood",
    "lung-blood",
)
SOURCE_ROWS = (5, 18, 26, 5, 18, 26)
SOURCE_COLUMNS = ((2, 3, 4),) * 3 + ((6, 7, 8),) * 3


def matches(a, b):
    return a == b or (isinstance(a, (int, float)) and isinstance(b, (int, float))
                      and abs(a - b) < 1e-10)


def audit(path):
    digest = hashlib.md5(path.read_bytes()).hexdigest()
    if digest != ZENODO_V3_MD5:
        raise ValueError(f"Zenodo v3 hash mismatch: {digest}")
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    overview = workbook["overall tissue"]
    findings = []
    for repository, specification in SHEETS.items():
        detailed = workbook[specification["detail"]]
        for metric, source_offset in (
            ("recall", 1),
            ("precision", 0),
            ("f1", 2),
        ):
            summary_cols = specification[metric]
            for method in range(3):
                # Each cancer block has three method rows. Organ and blood
                # queries occupy different metric triplets in the detail sheet.
                source_values = [
                    detailed.cell(row + method, SOURCE_COLUMNS[index][0] + source_offset).value
                    for index, row in enumerate(SOURCE_ROWS)
                ]
                # Overview precision starts on row 3; recall/F1 on row 4.
                first_row = 3 if metric == "precision" else 4
                observed = [
                    overview.cell(first_row + index, summary_cols[method]).value
                    for index in range(6)
                ]
                # Recall/detail start uses column C/G; precision B/F; F1 D/H.
                disagreements = [
                    QUERY_NAMES[index] for index, (a, b) in enumerate(zip(source_values, observed))
                    if not matches(a, b)
                ]
                identical_multiset = Counter(source_values) == Counter(observed)
                findings.append({
                    "repository": repository,
                    "metric": metric,
                    "method": method,
                    "row_disagreements": disagreements,
                    "source_values": source_values,
                    "overview_values": observed,
                    "multiset_equal": identical_multiset,
                    "mean_source": sum(source_values) / 6,
                    "mean_overview": sum(observed) / 6,
                })
    if any(not item["multiset_equal"] for item in findings):
        raise ValueError("The overview contains different metric values")
    if any(item["row_disagreements"] for item in findings if item["metric"] == "recall"):
        raise ValueError("Expected the previously verified recall identities")
    return {"source_md5": digest, "findings": findings}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receipt = audit(args.workbook)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    for metric in ("recall", "precision", "f1"):
        groups = [r for r in receipt["findings"] if r["metric"] == metric]
        print(metric, "disagreements", sum(len(r["row_disagreements"]) for r in groups),
              "of", len(groups) * 6,
              "same-multiset", sum(r["multiset_equal"] for r in groups), "/", len(groups))


if __name__ == "__main__":
    main()
