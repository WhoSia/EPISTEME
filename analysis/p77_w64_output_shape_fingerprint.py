"""W64: structure-only fingerprint of model dictionaries in a pinned Zenodo ZIP.

Usage: python analysis/p77_w64_output_shape_fingerprint.py Data_v2-v3.zip
The results compare source artifacts, not true labels, model accuracy, or the
actual historical execution graph. No subject-level values are printed.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import zipfile

EXPECTED = "bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c"
MEDLLAMA = {
    "liver": "liver_cancer_medllama_output.json",
    "lung": "lung_cancer_medllama_output.json",
    "ovarian": "ovarian_cancer_medllama_biosample_output.json",
}
GPT_CONTROL = "ovarian_cancer_800_gpt_output.json"


def parse_rows(blob):
    text = blob.decode("utf-8-sig")
    try:
        value = json.loads(text)
        if isinstance(value, list):
            return value
        raise ValueError("JSON whole file is not an array")
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def structural_count(rows, layer):
    if len(rows) != 800:
        raise ValueError("Expected 800 records")
    lengths = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(layer), dict):
            raise ValueError(f"Non-dictionary {layer} output")
        lengths.append(len(row[layer]))
    return {
        "n": len(lengths),
        "zero_key": lengths.count(0),
        "one_key": lengths.count(1),
        "two_or_more_keys": sum(n >= 2 for n in lengths),
        "all_at_most_one_key": all(n <= 1 for n in lengths),
        "key_count_distribution": {str(k): v for k, v in sorted(Counter(lengths).items())},
    }


def audit(archive):
    raw = Path(archive).read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError("Pinned Zenodo ZIP checksum mismatch")
    result = {}
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError("Archive CRC mismatch")
        for cancer, name in MEDLLAMA.items():
            rows = parse_rows(z.read("Data/" + name))
            result[cancer] = {
                layer: structural_count(rows, layer)
                for layer in ("LLM", "LLM+CEDAR")
            }
        gpt = parse_rows(z.read("Data/" + GPT_CONTROL))
        control = structural_count(gpt, "LLM+CEDAR")
    return {
        "zip_sha256": EXPECTED,
        "medllama": result,
        "gpt4_ovarian_control": control,
        "interpretation": (
            "All three held MedLlama output files contain only zero/one-key "
            "dicts at both LLM and LLM+CEDAR layers. That is structurally "
            "compatible with the one-field cedar_samples construction in "
            "historical MetadataCorrection.ipynb, which is selected at final "
            "LLM+CEDAR export instead of llm_cedar_samples. It is NOT evidence "
            "that this exact notebook generated any particular archive row."
        ),
        "not_established": [
            "which executable source generated archive",
            "specific original prompt/seed/temperature per row",
            "correctness of tissue prediction",
            "publication-run identity or six replicate provenance",
            "AI-mediated changes in adopted scientific standards",
        ],
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: p77_w64_output_shape_fingerprint.py Data.zip")
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
