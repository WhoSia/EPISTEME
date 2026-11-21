"""W60 original-source cohort audit regression tests, stdlib only."""
import copy
import json
import unittest
from p77_w60_zenodo_cohort_court import (
    parse_concatenated_json, accession, cohort_court, sha256, COHORTS, METHODS
)


def fake_items():
    """Three disjoint 800-sample GEO cohorts with nine model result files."""
    items = {}
    refs = {
        c: [{"gse": f"GSE_{c}_{i}", "gsm": [f"GSM_{c}_{i}"],
             "title": [f"{c} {i}"]} for i in range(800)]
        for c in COHORTS
    }
    for c in COHORTS:
        items[f"Data/{c}_cancer_geo.json"] = json.dumps(refs[c]).encode()
        for method in METHODS:
            rows = [{"BioSample": item, "LLM": {"tissue": c},
                     "LLM+CEDAR": {"tissue": f"{c}_{method}"}}
                    for item in refs[c]]
            items[f"Data/{c}_cancer_{method}_geo_output.json"] = (
                "\n".join(json.dumps(r) for r in rows)).encode()
    return items, refs


class ZenodoCohortTests(unittest.TestCase):
    def test_adjacent_json_objects_and_array(self):
        rows = [{"gse": "a", "gsm": ["b"]}, {"gse": "c", "gsm": ["d"]}]
        self.assertEqual(parse_concatenated_json(json.dumps(rows).encode()), rows)
        stream = "\n".join(json.dumps(x) for x in rows)
        self.assertEqual(parse_concatenated_json(stream.encode()), rows)

    def test_missing_accession_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing GEO"):
            accession({"gse": "GSE1"})

    def test_correctly_aligned_reference_cohorts(self):
        items, _ = fake_items()
        result = cohort_court(items)
        for row in result["model_input_matching"]:
            expected = row["file"].split("/")[1].split("_cancer")[0]
            for ref in COHORTS:
                self.assertEqual(row[f"position_matched_{ref}"],
                                 800 if ref == expected else 0)

    def test_cross_label_lung_input_is_detected(self):
        items, _ = fake_items()
        # Create the exact pathology that W60 found in the released originals.
        items["Data/liver_cancer_llama3_geo_output.json"] = items[
            "Data/lung_cancer_llama3_geo_output.json"]
        bad = cohort_court(items)
        liver = next(r for r in bad["model_input_matching"]
                     if r["file"] == "Data/liver_cancer_llama3_geo_output.json")
        self.assertEqual(liver["position_matched_lung"], 800)
        self.assertEqual(liver["position_matched_liver"], 0)
        self.assertTrue(bad["liver_and_lung_llama3_full_bytes_identical"])

    def test_duplicate_gold_accession_rejected(self):
        items, refs = fake_items()
        bad = copy.deepcopy(refs["liver"])
        bad[1] = bad[0]
        items["Data/liver_cancer_geo.json"] = json.dumps(bad).encode()
        with self.assertRaisesRegex(ValueError, "Duplicate reference"):
            cohort_court(items)

    def test_model_output_bad_accession_rejected(self):
        items, refs = fake_items()
        bad = [{"BioSample": refs["liver"][0]}] * 800
        items["Data/liver_cancer_gpt4_geo_output.json"] = (
            "\n".join(json.dumps(r) for r in bad)).encode()
        with self.assertRaisesRegex(ValueError, "duplicate or missing"):
            cohort_court(items)


if __name__ == "__main__":
    unittest.main()
