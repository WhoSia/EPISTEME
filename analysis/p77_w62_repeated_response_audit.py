"""W62: source-equivalent BioSample records and response disagreement audit.

Audits the *published, held* Sundaram 2026 Zenodo v2/v3 Data.zip.
Identical source fields are not necessarily one biological sample unless accession
identity is present. This measures artifact inconsistency, not a new LLM run,
independent scientific replicates, or publication-level F1.
Use: python analysis/p77_w62_repeated_response_audit.py Data.zip
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
import zipfile

EXPECTED_ZIP_SHA256 = "bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c"
FILES = {
    "liver": {
        "gpt4": "liver_cancer_800_gpt_output_updated.json",
        "llama3_dd": "liver_cancer_llama3_output_dd.json",
        "llama3_cedar": "liver_cancer_llama3_output_cedar.json",
        "medllama": "liver_cancer_medllama_output.json",
    },
    "lung": {
        "gpt4": "lung_cancer_800_gpt_output.json",
        "llama3": "lung_cancer_llama3_output.json",
        "medllama": "lung_cancer_medllama_output.json",
    },
    "ovarian": {
        "gpt4": "ovarian_cancer_800_gpt_output.json",
        "llama3": "ovarian_cancer_llama3_output.json",
        "medllama": "ovarian_cancer_medllama_biosample_output.json",
    }
}
LAYERS = ("LLM", "LLM+CEDAR")
MISSING = "<ABSENT>"


def parse_json_stream(data):
    text = data.decode("utf-8-sig")
    decoder = json.JSONDecoder()
    pos, rows = 0, []
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos == len(text):
            break
        part, pos = decoder.raw_decode(text, pos)
        rows.extend(part if isinstance(part, list) else [part])
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Non-object JSON record")
    return rows


def fingerprint(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def source_signature(row):
    source = row.get("BioSample")
    if not isinstance(source, dict):
        raise ValueError("Non-object BioSample source")
    return fingerprint({k: v for k, v in source.items()
                        if k != "biosample_accession"})


def tissue_token(layer):
    # This is *structural*, not a clinical or ontology-correct label.
    if not isinstance(layer, dict):
        raise ValueError("Malformed prediction layer")
    value = layer.get("tissue", layer.get("tissue_type"))
    return value.strip().casefold() if isinstance(value, str) else MISSING


def summarize(rows, require_accession=False):
    if len(rows) != 800:
        raise ValueError("Expected precisely 800 rows in archived output")
    groups = defaultdict(list)
    for row in rows:
        groups[source_signature(row)].append(row)
    repeated = [group for group in groups.values() if len(group) > 1]
    with_accession = [r["BioSample"]["biosample_accession"]
                      for r in rows if "biosample_accession" in r["BioSample"]]
    if require_accession:
        if len(with_accession) != len(rows):
            raise ValueError("Missing liver-GPT4 accession")
        for group in repeated:
            if len({r["BioSample"]["biosample_accession"] for r in group}) != 1:
                raise ValueError("Different accession IDs share one source signature")
        by_accession = defaultdict(set)
        for r in rows:
            by_accession[r["BioSample"]["biosample_accession"]].add(
                source_signature(r))
        if any(len(sigs) > 1 for sigs in by_accession.values()):
            raise ValueError("One accession points to different source fields")
        if len(by_accession) != len(groups):
            raise ValueError("Accession cardinality != source-signature cardinality")
    out = {
        "rows": len(rows),
        "unique_source_signatures": len(groups),
        "repeated_groups": len(repeated),
        "rows_in_repeated_groups": sum(len(g) for g in repeated),
        "redundant_rows_if_one_per_signature": sum(len(g)-1 for g in repeated),
        "repetition_group_sizes": dict(sorted(Counter(map(len, repeated)).items())),
        "max_group_size": max((len(g) for g in groups.values()), default=0),
        "accession_field_rows": len(with_accession),
        "unique_accessions_if_present": len(set(with_accession)) if with_accession else None,
    }
    for layer_name in LAYERS:
        if not any(layer_name in row for row in rows):
            continue
        if any(layer_name not in row for row in rows):
            raise ValueError("Partial model-output layer: " + layer_name)
        preds = [row[layer_name] for row in rows]
        if any(not isinstance(layer, dict) for layer in preds):
            raise ValueError("Non-dictionary prediction")
        out[layer_name] = {
            "rows_with_tissue_or_tissue_type_key": sum(
                tissue_token(pred) != MISSING for pred in preds),
            "repeated_groups_with_distinct_full_outputs": sum(
                len({fingerprint(r[layer_name]) for r in g}) > 1
                for g in repeated),
            "repeated_groups_with_distinct_tissue_tokens": sum(
                len({tissue_token(r[layer_name]) for r in g}) > 1
                for g in repeated),
            "repeated_groups_with_missing_tissue_token": sum(
                any(tissue_token(r[layer_name]) == MISSING for r in g)
                for g in repeated),
        }
    return out


def audit(zip_path):
    raw = Path(zip_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_ZIP_SHA256:
        raise ValueError("Unexpected Zenodo ZIP digest")
    response = {}
    with zipfile.ZipFile(zip_path) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC failure")
        for cancer, names in FILES.items():
            response[cancer] = {}
            for method, filename in names.items():
                parsed = parse_json_stream(z.read("Data/" + filename))
                response[cancer][method] = summarize(
                    parsed, require_accession=(cancer == "liver" and method == "gpt4"))
    return {
        "source_zip_sha256": EXPECTED_ZIP_SHA256,
        "artifact_level_not_authors_publication_experiment": True,
        "cohorts": response,
        "interpretation": "Only liver GPT4 has accession IDs for all rows; for lung/ovarian equal source objects do not prove same biospecimen. Tissue token differs from valid ontology mapping. Repeated rows can carry different model output fields without implying identical run parameters.",
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: p77_w62_repeated_response_audit.py v2v3_Data.zip")
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
