"""W62 source-equivalence audit: compact adversarial and regression tests."""
import unittest
import json
from p77_w62_repeated_response_audit import summarize, parse_json_stream, tissue_token


def fixture_groups():
    # 728 singleton signatures + 24 repeated groups = 800 rows, 752 signatures.
    # Repeated groups: 11x2, 9x3, 3x4, 1x11 = 72 repeated rows; 48 extras.
    groups = [1] * 728 + [2] * 11 + [3] * 9 + [4] * 3 + [11]
    rows = []
    for gid, count in enumerate(groups):
        for rep in range(count):
            acc = "SAMN" + str(gid)
            rows.append({
                "BioSample": {"biosample_accession": acc, "tissue": "liver", "case": gid},
                "LLM": {"tissue": "liver" if rep == 0 else "LUNG"},
                "LLM+CEDAR": {"tissue": "liver"},
            })
    return rows


class W62Tests(unittest.TestCase):
    def test_manifest_shapes_and_nonindependent_counts(self):
        r = summarize(fixture_groups(), require_accession=True)
        self.assertEqual((r["rows"],r["unique_source_signatures"],r["repeated_groups"],
                          r["rows_in_repeated_groups"],r["redundant_rows_if_one_per_signature"]),
                         (800,752,24,72,48))
        self.assertEqual(r["max_group_size"],11)
        self.assertEqual(r["unique_accessions_if_present"],752)

    def test_tissue_normalization_and_field_fallback(self):
        self.assertEqual(tissue_token({"tissue":" Liver "}),"liver")
        self.assertEqual(tissue_token({"tissue_type":"LIVER"}),"liver")
        self.assertEqual(tissue_token({}),"<ABSENT>")

    def test_detects_repeated_input_prediction_changes(self):
        r = summarize(fixture_groups(), require_accession=True)
        self.assertEqual(r["LLM"]["repeated_groups_with_distinct_full_outputs"],24)
        self.assertEqual(r["LLM"]["repeated_groups_with_distinct_tissue_tokens"],24)
        self.assertEqual(r["LLM+CEDAR"]["repeated_groups_with_distinct_tissue_tokens"],0)

    def test_liver_accession_conflict_rejected(self):
        rows = fixture_groups()
        rows[729]["BioSample"]["biosample_accession"] = "DIFFERENT"
        with self.assertRaisesRegex(ValueError,"Different accession"):
            summarize(rows,require_accession=True)

    def test_same_accession_with_changed_source_rejected(self):
        rows = fixture_groups()
        rows[0]["BioSample"]["case"] = -3
        rows[0]["BioSample"]["biosample_accession"] = rows[1]["BioSample"]["biosample_accession"]
        with self.assertRaisesRegex(ValueError,"One accession"):
            summarize(rows,require_accession=True)

    def test_no_biosample_accession_does_not_infer_biological_identity(self):
        rows = fixture_groups()
        for row in rows:
            del row["BioSample"]["biosample_accession"]
        r = summarize(rows,require_accession=False)
        self.assertEqual(r["accession_field_rows"],0)
        self.assertIsNone(r["unique_accessions_if_present"])

    def test_partial_layer_rejected(self):
        rows=fixture_groups()
        del rows[0]["LLM"]
        with self.assertRaisesRegex(ValueError,"Partial"):
            summarize(rows)

    def test_malformed_source_rejected(self):
        rows=fixture_groups()
        rows[10]["BioSample"]=[]
        with self.assertRaisesRegex(ValueError,"Non-object BioSample"):
            summarize(rows)

    def test_unexpected_row_count_rejected(self):
        with self.assertRaisesRegex(ValueError,"800"):
            summarize(fixture_groups()[:-1])

    def test_json_array_and_adjacent_objects(self):
        self.assertEqual(parse_json_stream(b'[{"x":1},{"x":2}]'),
                         [{"x":1},{"x":2}])
        self.assertEqual(parse_json_stream(b'{"x":1}\n{"x":2}'),
                         [{"x":1},{"x":2}])


if __name__ == "__main__":
    unittest.main()
