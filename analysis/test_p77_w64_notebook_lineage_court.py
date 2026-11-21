"""Synthetic regression tests for W64 historical notebook source-flow auditor.

All tests operate on tiny made-up notebooks. Historical author blobs are checked
separately by the pinned Git clone path and by source retrieval in research court.
"""
import copy
import unittest
from p77_w64_notebook_lineage_court import (
    NOTEBOOK_BLOBS, audit, code_cells, git_blob_sha1
)


def notebook(*sources, executed=False):
    return {"cells": [
        {"cell_type": "code", "source": source.splitlines(keepends=True),
         "execution_count": 1 if executed else None,
         "outputs": [{"output_type": "stream"}] if executed else []}
        for source in sources
    ]}


def fake():
    return {
        "GEODatasetGenerator.ipynb": notebook(
            "for d in datasets:\n    if 'liver cancer' in d['title']:\n        pass\n",
            "import random\nrandom_samples = random.sample(final_data, 800)\n",
            "with open('ovarian_cancer_geo.json', 'w') as f:\n    pass\n"
        ),
        "MetadataCorrection.ipynb": notebook(
            "cedar_samples = []\ncedar_samples.append(k)\n",
            "llm_cedar_samples = []\nllm_cedar_samples.append(eval(ans))\n",
            "dict_sample['LLM+CEDAR'] = cedar_samples[i]\n"
        ),
        "MetadataCorrection-gpt.ipynb": notebook(
            "llm_samples = []\nllm_samples.append(d['LLM'])\n",
            "llm_samples = []\n",
            "llm_samples.append(eval(ans))\n",
            "dict_sample['LLM'] = llm_samples[i]\n"
        ),
        "Rules.ipynb": notebook(
            "tissue = tissue.lower()\n"
            "if 'PBMC' in tissue or 'blood' in tissue: nam='blood'\n"
        ),
        "metadata-refine.ipynb": notebook(
            'tissue_lung_biosample = search(samples, "tissue", "blood")\n',
            "print(evaluate(tissue_lung_biosample, ground_truth, 'ovary'))\n"
        ),
    }


class W64Tests(unittest.TestCase):
    def test_historical_positive_contract(self):
        result = audit(fake())
        self.assertTrue(result["GEO_selection_to_filename"]["liver_title_filter_present"])
        self.assertTrue(result["GEO_selection_to_filename"]["ovarian_output_filename_present"])
        self.assertTrue(result["MedLlama_BioSample_CEDAR_export"]["llm_cedar_generated_in_source"])
        self.assertEqual(result["MedLlama_BioSample_CEDAR_export"]["final_LLM_plus_CEDAR_array"],
                         "cedar_samples")
        self.assertFalse(result["MedLlama_BioSample_CEDAR_export"]
                         ["the_llm_cedar_array_is_used_for_that_export"])

    def test_notebook_metadata_not_evidence_of_never_run(self):
        x = fake()
        x["Rules.ipynb"]["cells"][0]["execution_count"] = 4
        x["Rules.ipynb"]["cells"][0]["outputs"] = [{"output_type": "stream"}]
        o = audit(x)["notebook_summary"]["Rules.ipynb"]
        self.assertEqual(o["stored_execution_count"], 1)
        self.assertEqual(o["stored_nonempty_output"], 1)

    def test_changed_geo_filename_fails_closed(self):
        x = fake()
        x["GEODatasetGenerator.ipynb"]["cells"][2]["source"][0] = \
            "with open('liver_cancer_geo.json', 'w') as f:\n"
        with self.assertRaisesRegex(ValueError, "mismatch"):
            audit(x)

    def test_production_array_name_change_fails_closed(self):
        x = fake()
        x["MetadataCorrection.ipynb"]["cells"][2]["source"][0] = \
            "dict_sample['LLM+CEDAR'] = llm_cedar_samples[i]\n"
        with self.assertRaisesRegex(ValueError, "export array"):
            audit(x)

    def test_missing_generated_layer_fails_closed(self):
        x = fake()
        x["MetadataCorrection.ipynb"]["cells"][1]["source"][1] = "pass\n"
        with self.assertRaisesRegex(ValueError, "arrays not found"):
            audit(x)

    def test_rng_seed_detection(self):
        x = fake()
        x["GEODatasetGenerator.ipynb"]["cells"][1]["source"].append("random.seed(42)\n")
        o = audit(x)["GEO_selection_to_filename"]
        self.assertFalse(o["visible_random_sample_800_unseeded"])

    def test_gpt_reset_negative_control(self):
        x = fake()
        result = audit(x)["GPT4_GEO_negative_control"]
        self.assertTrue(result["llm_samples_reset_before_new_append"])
        self.assertTrue(result["LLM_export_reads_llm_samples"])

    def test_broken_gpt_negative_control_detected(self):
        x = fake()
        x["MetadataCorrection-gpt.ipynb"]["cells"][1]["source"] = ["pass\n"]
        self.assertFalse(audit(x)["GPT4_GEO_negative_control"]
                         ["llm_samples_reset_before_new_append"])

    def test_missing_notebook_rejected(self):
        x = fake()
        del x["Rules.ipynb"]
        with self.assertRaisesRegex(ValueError, "five pinned"):
            audit(x)

    def test_blob_sha1_matches_git_object_definition(self):
        import hashlib
        data = b"hello\n"
        canonical = b"blob 6\0hello\n"
        self.assertEqual(git_blob_sha1(data), hashlib.sha1(canonical).hexdigest())


if __name__ == "__main__":
    unittest.main()
