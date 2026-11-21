"""W65: Conditional exact-key vs normalized-key query reproduction on released BioSample.

Historical notebook metadata-refine.ipynb searches sample['tissue'] == value.lower().
This script reads the held Zenodo v2/v3 ZIP and performs only aggregate
calculations using *positionally aligned* published heuristic labels.

Do not call these author-reported metrics, real model reruns, or robust
independent gold-standard evaluation. No individual subjects are printed.
Run: python analysis/p77_w65_query_parser_sensitivity.py original_v2v3_Data.zip
"""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ZIP_SHA256 = "bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c"
CONFIG = {
    "liver": {"label": "annotated_800_simple_liver.txt", "query": "liver", "outputs": {
        "gpt4": ("liver_cancer_800_gpt_output_updated.json", ("BioSample", "LLM", "LLM+CEDAR")),
        "llama3_dd": ("liver_cancer_llama3_output_dd.json", ("BioSample", "LLM")),
        "llama3_cedar": ("liver_cancer_llama3_output_cedar.json", ("BioSample", "LLM+CEDAR")),
        "medllama": ("liver_cancer_medllama_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
    }},
    "lung": {"label": "annotated_800_simple_lung.txt", "query": "lung", "outputs": {
        "gpt4": ("lung_cancer_800_gpt_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
        "llama3": ("lung_cancer_llama3_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
        "medllama": ("lung_cancer_medllama_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
    }},
    "ovarian": {"label": "annotated_800_simple_ovary.txt", "query": "ovary", "outputs": {
        "gpt4": ("ovarian_cancer_800_gpt_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
        "llama3": ("ovarian_cancer_llama3_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
        "medllama": ("ovarian_cancer_medllama_biosample_output.json", ("BioSample", "LLM", "LLM+CEDAR")),
    }},
}


def parse_stream(blob: bytes) -> list[dict]:
    text = blob.decode("utf-8-sig")
    decoder = json.JSONDecoder()
    pos, result = 0, []
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos == len(text):
            break
        obj, pos = decoder.raw_decode(text, pos)
        result.extend(obj if isinstance(obj, list) else [obj])
    if any(not isinstance(item, dict) for item in result):
        raise ValueError("Non-record JSON payload")
    return result


def select(layer: dict, query: str, mode: str) -> bool:
    """The second/third modes are proposed sensitivity controls, NOT author methods."""
    if not isinstance(layer, dict) or not isinstance(query, str):
        raise ValueError("Bad layer or query")
    if mode == "author_exact_tissue":
        return layer.get("tissue") == query.lower()
    if mode not in ("alias_exact", "alias_casefold_strip"):
        raise ValueError("Unknown parser mode")
    value = layer.get("tissue", layer.get("tissue_type"))
    if not isinstance(value, str):
        return False
    return (value == query.lower() if mode == "alias_exact"
            else value.strip().casefold() == query.strip().casefold())


def confusion(rows: list[dict], labels: list[str], layer: str, query: str, mode: str):
    if len(rows) != 800 or len(labels) != 800:
        raise ValueError("Expected precisely 800 row-position labels")
    hits = []
    for row in rows:
        if layer not in row:
            raise ValueError("Missing layer " + layer)
        hits.append(select(row[layer], query, mode))
    is_relevant = [x == query for x in labels]
    tp = sum(a and b for a, b in zip(hits, is_relevant))
    fp = sum(a and not b for a, b in zip(hits, is_relevant))
    fn = sum(not a and b for a, b in zip(hits, is_relevant))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "retrieved": tp + fp,
            "relevant": tp + fn, "precision": precision, "recall": recall, "f1": f1}


def audit(zip_path):
    payload = Path(zip_path).read_bytes()
    if hashlib.sha256(payload).hexdigest() != ZIP_SHA256:
        raise ValueError("Original Zenodo ZIP SHA256 mismatch")
    modes = ("author_exact_tissue", "alias_exact", "alias_casefold_strip")
    results = {}
    with zipfile.ZipFile(zip_path) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC mismatch")
        for cancer, cfg in CONFIG.items():
            labels = z.read("Data/" + cfg["label"]).decode("utf-8-sig").splitlines()
            if len(labels) != 800:
                raise ValueError("Unexpected label length")
            results[cancer] = {"gold_distribution": {
                k: labels.count(k) for k in sorted(set(labels))}, "models": {}}
            for model, (filename, layers) in cfg["outputs"].items():
                rows = parse_stream(z.read("Data/" + filename))
                results[cancer]["models"][model] = {}
                for layer in layers:
                    if any(layer not in row or not isinstance(row[layer], dict)
                           for row in rows):
                        raise ValueError(f"Incomplete {model}/{layer} layer")
                    results[cancer]["models"][model][layer] = {
                        query: {mode: confusion(rows, labels, layer, query, mode)
                                for mode in modes}
                        for query in (cfg["query"], "blood")
                    }
    return {
        "source_zip_sha256": ZIP_SHA256, "parsers": modes,
        "results": results,
        "scope": ("Conditional row-position pairing using released heuristic "
                  "labels and published notebook's exact tissue query; "
                  "normalization parsers are independent sensitivity controls, "
                  "not manuscript publication metric reproduction."),
        "not_established": ["biological ground truth", "original run IDs",
                            "author's exact evaluation DAG", "causal standards adoption"],
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python p77_w65_query_parser_sensitivity.py Zenodo_v2v3_Data.zip")
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
