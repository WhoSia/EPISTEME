"""W64: bounded source-title composition check against 2025 generator notebook.

Requires only held Sundaram v2/v3 original ZIP, never executes author notebooks.
  python analysis/p77_w64_geo_title_crosscheck.py "Data v2-v3.zip"

A title keyword is not biological ground truth or execution provenance.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ZIP_SHA256 = "bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c"
COHORTS = ("liver", "lung", "ovarian")


def text_title(record):
    raw = record.get("title", "")
    if isinstance(raw, str):
        return raw.casefold()
    if isinstance(raw, list) and all(isinstance(x, str) for x in raw):
        return " ".join(raw).casefold()
    raise ValueError("Unexpected GEO title type")


def count_title_markers(records):
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("GEO source records must be dictionaries")
    names = [text_title(r) for r in records]
    return {
        "rows": len(names),
        "titles_containing_liver_cancer": sum("liver cancer" in t for t in names),
        "titles_containing_lung_cancer": sum("lung cancer" in t for t in names),
        "titles_containing_ovarian_cancer": sum("ovarian cancer" in t for t in names),
    }


def audit(zip_file):
    payload = Path(zip_file).read_bytes()
    if hashlib.sha256(payload).hexdigest() != ZIP_SHA256:
        raise ValueError("Held Zenodo release hash mismatch")
    results = {}
    with zipfile.ZipFile(zip_file) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC error")
        for cohort in COHORTS:
            raw = z.read(f"Data/{cohort}_cancer_geo.json")
            rows = json.loads(raw)
            if not isinstance(rows, list) or len(rows) != 800:
                raise ValueError("Unexpected GEO cohort size")
            results[cohort] = count_title_markers(rows)
    return {
        "source_sha256": ZIP_SHA256,
        "GEO_titles": results,
        "source_code_contrast": (
            "The historical GEODatasetGenerator.ipynb selects 'liver cancer' "
            "from a series-title field but saves the result using the ovarian "
            "file basename. The held ovarian Data input instead has ovarian "
            "in all 800 sample titles, liver cancer in zero. This is a "
            "cross-source discrepancy, NOT proof of which notebook execution "
            "created the held data: parsed listing titles and fetched GEO "
            "titles must be independently joined to establish equivalence."
        ),
        "claim_limit": (
            "Cancer words in a study title are not diagnostic gold labels; "
            "the code and released archive do not reconstruct model execution, "
            "six independent runs or published performance."
        )
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: p77_w64_geo_title_crosscheck.py v2v3_Data.zip")
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
