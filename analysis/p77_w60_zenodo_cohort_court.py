"""P77 W60: independently audit the *held* Sundaram Zenodo ZIP archives.

Usage: python analysis/p77_w60_zenodo_cohort_court.py v1_Data.zip v2v3_Data.zip
Only JSON aggregates (no raw sample rows) are printed. Requires stdlib only.
This tests released artifacts, not whether these files fed the publication's tables.
"""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

RELEASES = {
    "v1": {"size": 4001077, "md5": "8ae6475067de8ae03ba4a9a0c1efd8c5",
           "sha256": "ffa343983f41e6db6a02a4e2e3558c36d112c8163e8637005cd088f3a85d6396"},
    "v2v3": {"size": 3992768, "md5": "9ebd58bd9770bdb75722d0e3fe6c06ef",
             "sha256": "bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c"},
}
COHORTS = ("liver", "lung", "ovarian")
METHODS = ("gpt4", "llama3", "medllama")


def sha256(payload):
    return hashlib.sha256(payload).hexdigest()


def load_archive(path, release):
    b = Path(path).read_bytes()
    expected = RELEASES[release]
    if len(b) != expected["size"] or hashlib.md5(b).hexdigest() != expected["md5"] or sha256(b) != expected["sha256"]:
        raise ValueError(f"{release}: Drive-retrieved bytes do not match published acquisition receipt")
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError(f"{release}: ZIP CRC mismatch")
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError(f"{release}: duplicated ZIP paths")
        if any(n.startswith("/") or ".." in n.split("/") or "\\" in n for n in names):
            raise ValueError(f"{release}: invalid ZIP path")
        items = {n: z.read(n) for n in names if not n.endswith("/")}
    return items


def parse_concatenated_json(payload):
    """Handle both an array JSON and a stream of adjacent JSON objects."""
    s = payload.decode("utf-8-sig")
    decoder = json.JSONDecoder()
    pos = 0
    rows = []
    while pos < len(s):
        while pos < len(s) and s[pos].isspace():
            pos += 1
        if pos == len(s):
            break
        record, pos = decoder.raw_decode(s, pos)
        if isinstance(record, list):
            rows.extend(record)
        else:
            rows.append(record)
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Non-object JSON records")
    return rows


def accession(record):
    src = record.get("BioSample", record)
    if not isinstance(src, dict):
        raise ValueError("Invalid BioSample source record")
    gse, gsm = src.get("gse"), src.get("gsm")
    if not isinstance(gse, str) or not isinstance(gsm, list) or not gsm:
        raise ValueError("Missing GEO accession identity")
    return (gse, tuple(gsm))


def cohort_court(items):
    reference = {
        c: parse_concatenated_json(items[f"Data/{c}_cancer_geo.json"])
        for c in COHORTS
    }
    if any(len(rows) != 800 for rows in reference.values()):
        raise ValueError("Reference GEO files no longer have 800 records each")
    ids = {c: list(map(accession, rows)) for c, rows in reference.items()}
    if any(len(set(keys)) != 800 for keys in ids.values()):
        raise ValueError("Duplicate reference GSE/GSM accession")
    for i, c in enumerate(COHORTS):
        for d in COHORTS[i+1:]:
            if set(ids[c]) & set(ids[d]):
                raise ValueError("Reference cancer cohorts are not accession-disjoint")
    table = []
    records = {}
    for cancer in COHORTS:
        for method in METHODS:
            filename = f"Data/{cancer}_cancer_{method}_geo_output.json"
            rows = parse_concatenated_json(items[filename])
            keys = list(map(accession, rows))
            if len(keys) != 800 or len(set(keys)) != 800:
                raise ValueError(f"{filename}: duplicate or missing accession")
            record = {"file": filename, "n": len(keys)}
            for ref_cancer in COHORTS:
                record[f"position_matched_{ref_cancer}"] = sum(
                    a == b for a, b in zip(keys, ids[ref_cancer])
                )
                record[f"unique_overlap_{ref_cancer}"] = len(
                    set(keys) & set(ids[ref_cancer])
                )
            table.append(record)
            records[(cancer, method)] = rows

    liver = items["Data/liver_cancer_llama3_geo_output.json"]
    lung = items["Data/lung_cancer_llama3_geo_output.json"]
    lung_r = records[("lung", "llama3")]
    ovarian_r = records[("ovarian", "llama3")]
    return {
        "reference_counts": {c: len(ids[c]) for c in COHORTS},
        "model_input_matching": table,
        "liver_and_lung_llama3_full_bytes_identical": liver == lung,
        "liver_and_lung_llama3_sha256": sha256(liver),
        "ovarian_llama3_source_equals_lung_800": sum(
            a["BioSample"] == b["BioSample"] for a, b in zip(ovarian_r, lung_r)
        ),
        "ovarian_vs_lung_llama3_predictions_equal": {
            k: sum(a.get(k) == b.get(k) for a, b in zip(ovarian_r, lung_r))
            for k in ("LLM", "LLM+CEDAR")
        },
        "scope": "Published ZIP source-record pairing; not yet the author's actual statistical execution graph",
    }


def audit(v1_path, v2v3_path):
    a = load_archive(v1_path, "v1")
    b = load_archive(v2v3_path, "v2v3")
    a_data = {n: sha256(v) for n, v in a.items() if n.startswith("Data/")}
    b_data = {n: sha256(v) for n, v in b.items() if n.startswith("Data/")}
    if set(a_data) != set(b_data):
        raise ValueError("Changed names in data file set")
    changes = [n for n in sorted(a_data) if a_data[n] != b_data[n]]
    extra = sorted(set(a) - set(b))
    if any(not n.startswith("__MACOSX/") for n in extra) or set(b) - set(a):
        raise ValueError("Unexpected non-macOS version change")
    return {
        "release_sha256": {k: RELEASES[k]["sha256"] for k in RELEASES},
        "v1_payload_file_count": len(a_data),
        "v2v3_payload_file_count": len(b_data),
        "payload_files_changed": changes,
        "v1_extra_macos_metadata_files": len(extra),
        "zip_entry_count": {"v1": len(a)+1, "v2v3": len(b)+1},
        "GEO": cohort_court(b),
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: p77_w60_zenodo_cohort_court.py V1.zip V2V3.zip")
    print(json.dumps(audit(*sys.argv[1:]), ensure_ascii=False, indent=2))
