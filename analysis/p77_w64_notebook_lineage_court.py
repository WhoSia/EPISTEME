"""W64: static audit of original 2025 author notebooks; never executes cells.

Use an already cloned author Git repository with the pinned commit available:
  python analysis/p77_w64_notebook_lineage_court.py /path/FAIRMetadataCuration

This checker verifies actual Git blob bytes and extracts source-level wiring only.
No LLM or evaluation calls. It does NOT establish which code generated the paper.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

AUTHOR_COMMIT = "fcc91cc321c649fd96895eb435e978fb57d00acc"
NOTEBOOK_BLOBS = {
    "GEODatasetGenerator.ipynb": "76ac30a05712cb375f956e7f46178c3182005d74",
    "MetadataCorrection.ipynb": "1ef81302d7f12b333706bd321bcd90d8ea4f1fb3",
    "MetadataCorrection-gpt.ipynb": "2c0720bbdfa00753d3e9c213a5ee51b8b42d87e0",
    "Rules.ipynb": "be0d1c324cd351af70e89fe49bfc6b2a864be27a",
    "metadata-refine.ipynb": "cbb64b519014ad4f68e1ddfe68f3db488040d2cb",
}


def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def load_pinned_notebooks(repo):
    result = {}
    for name, expected_sha in NOTEBOOK_BLOBS.items():
        raw = subprocess.check_output(
            ["git", "-C", str(repo), "show", AUTHOR_COMMIT + ":" + name]
        )
        if git_blob_sha1(raw) != expected_sha:
            raise ValueError("Historical author notebook blob mismatch: " + name)
        result[name] = json.loads(raw)
    return result


def code_cells(notebook):
    if not isinstance(notebook, dict) or not isinstance(notebook.get("cells"), list):
        raise ValueError("Invalid notebook")
    return [
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]


def checked_source(notebook):
    return "\n\n".join(code_cells(notebook))


def occurrence_count(source, variable):
    return len(re.findall(r"\b" + re.escape(variable) + r"\b", source))


def audit(notebooks):
    if set(notebooks) != set(NOTEBOOK_BLOBS):
        raise ValueError("Expected five pinned author notebooks")
    summary = {}
    for name, nb in notebooks.items():
        cells = [c for c in nb["cells"] if c.get("cell_type") == "code"]
        summary[name] = {
            "historical_blob": NOTEBOOK_BLOBS[name],
            "code_cells": len(cells),
            "stored_execution_count": sum(c.get("execution_count") is not None for c in cells),
            "stored_nonempty_output": sum(bool(c.get("outputs")) for c in cells),
        }

    generator = checked_source(notebooks["GEODatasetGenerator.ipynb"])
    source_filter_liver = bool(re.search(
        r"""if\s+['"]liver cancer['"]\s+in\s+d\[['"]title['"]\]""", generator
    ))
    saved_ovarian = bool(re.search(
        r"""with\s+open\(\s*['"]ovarian_cancer_geo\.json['"]\s*,\s*['"]w['"]""",
        generator,
    ))
    sample_without_explicit_seed = (
        "random.sample(final_data, 800)" in generator
        and not re.search(r"\brandom\.seed\(|\brandom\.Random\(|\bdefault_rng\(", generator)
    )
    if not (source_filter_liver and saved_ovarian):
        raise ValueError("Historical GEO selection/output mismatch no longer reproducible")

    med = checked_source(notebooks["MetadataCorrection.ipynb"])
    extra_cedar_generated = bool(re.search(r"\bllm_cedar_samples\.append\(", med))
    final_field = re.search(
        r"""dict_sample\[['"]LLM\+CEDAR['"]\]\s*=\s*([a-zA-Z_]\w*)\[i\]""",
        med,
    )
    if not final_field or not extra_cedar_generated:
        raise ValueError("Historical metadata-correction arrays not found")
    final_array = final_field.group(1)
    if final_array != "cedar_samples":
        raise ValueError("Historical export array no longer matches audited source")
    llm_cedar_referenced_in_export = final_array == "llm_cedar_samples"

    gpt = code_cells(notebooks["MetadataCorrection-gpt.ipynb"])
    reset_positions = [i for i, code in enumerate(gpt)
                       if re.search(r"(?m)^\s*llm_samples\s*=\s*\[\]\s*$", code)]
    append_positions = [i for i, code in enumerate(gpt)
                        if "llm_samples.append(eval(ans))" in code]
    exported_gpt = "dict_sample['LLM'] = llm_samples[i]" in "\n".join(gpt)
    old_append_positions = [i for i, code in enumerate(gpt)
                            if "llm_samples.append(d['LLM'])" in code]
    if not reset_positions or not append_positions or not old_append_positions:
        raise ValueError("Expected GPT-4 old-output, reset and new-output cells missing")
    reset_prior_to_append = any(
        prior < reset < generated
        for prior in old_append_positions
        for reset in reset_positions
        for generated in append_positions
    )

    refinement = checked_source(notebooks["metadata-refine.ipynb"])
    has_blood_query = bool(re.search(
        r"""search\(\s*samples\s*,\s*['"]tissue['"]\s*,\s*['"]blood['"]""",
        refinement,
    ))
    has_ovary_scoring = bool(re.search(
        r"""evaluate\(\s*tissue_lung_biosample\s*,\s*ground_truth\s*,\s*['"]ovary['"]""",
        refinement,
    ))

    rules = checked_source(notebooks["Rules.ipynb"])
    pbmc_case_mismatch = ".lower()" in rules and "'PBMC' in tissue" in rules

    return {
        "author_commit": AUTHOR_COMMIT,
        "notebook_summary": summary,
        "GEO_selection_to_filename": {
            "liver_title_filter_present": source_filter_liver,
            "ovarian_output_filename_present": saved_ovarian,
            "visible_random_sample_800_unseeded": bool(sample_without_explicit_seed),
            "scope": "Code path conditional on notebook cell execution; not evidence this path generated ZIP",
        },
        "MedLlama_BioSample_CEDAR_export": {
            "llm_cedar_generated_in_source": extra_cedar_generated,
            "final_LLM_plus_CEDAR_array": final_array,
            "the_llm_cedar_array_is_used_for_that_export": llm_cedar_referenced_in_export,
            "source_occurrences_llm_cedar_samples": occurrence_count(med, "llm_cedar_samples"),
            "scope": "Generated branch is not the array assigned to final output; actual release run unknown",
        },
        "GPT4_GEO_negative_control": {
            "llm_samples_reset_before_new_append": reset_prior_to_append,
            "LLM_export_reads_llm_samples": exported_gpt,
            "caution": "Do not misdiagnose older LLM data as always retained: source resets array before append",
        },
        "metadata_refine_example": {
            "blood_query_present": has_blood_query,
            "ovary_truth_scoring_present": has_ovary_scoring,
            "scope": "Notebook example, not manuscript table generator",
        },
        "Rules_example": {
            "uppercase_PBMC_test_after_lowercase": pbmc_case_mismatch
        },
        "claim_boundary": (
            "Five pinned historical notebooks have no stored execution counts/outputs, "
            "but absence of stored outputs is NOT proof they were never run. "
            "Static data-flow findings do not identify the actual published run "
            "nor explain the released cross-cancer mismatch without run provenance."
        )
    }


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit("Usage: p77_w64_notebook_lineage_court.py AUTHOR_REPO_CLONE")
    print(json.dumps(audit(load_pinned_notebooks(Path(argv[0]))),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
