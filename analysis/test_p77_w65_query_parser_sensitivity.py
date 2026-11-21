"""W65: tests of released-source parser assumptions; stdlib only."""
import unittest
from p77_w65_query_parser_sensitivity import parse_stream, select, confusion


class SourceParserTests(unittest.TestCase):
    def test_stream_and_array(self):
        self.assertEqual(parse_stream(b'{"a":1}{"a":2}'), [{"a":1},{"a":2}])
        self.assertEqual(parse_stream(b'[{"a":1},{"a":2}]'), [{"a":1},{"a":2}])

    def test_exact_tissue_case_sensitive(self):
        self.assertFalse(select({"tissue": "Lung"}, "lung", "author_exact_tissue"))
        self.assertFalse(select({"tissue_type": "lung"}, "lung", "author_exact_tissue"))
        self.assertTrue(select({"tissue": "lung"}, "LUNG", "author_exact_tissue"))

    def test_fallback_exact_and_casefold(self):
        self.assertTrue(select({"tissue_type": "lung"}, "lung", "alias_exact"))
        self.assertFalse(select({"tissue_type": "Lung"}, "lung", "alias_exact"))
        self.assertTrue(select({"tissue_type": " Lung "}, "lung", "alias_casefold_strip"))
        self.assertFalse(select({"description": "lung"}, "lung", "alias_casefold_strip"))

    def test_original_tissue_key_preempts_fallback(self):
        self.assertFalse(select({"tissue": "bad", "tissue_type": "lung"},
                                "lung", "alias_casefold_strip"))

    def test_exact_confusion_matrix(self):
        rows = [{"LLM": {"tissue": "lung"}} for _ in range(800)]
        m = confusion(rows, ["lung"] * 800, "LLM", "lung", "author_exact_tissue")
        self.assertEqual((m["tp"], m["fp"], m["fn"], m["f1"]), (800, 0, 0, 1.0))

    def test_search_truth_mismatch_is_not_true_positive(self):
        rows = [{"LLM": {"tissue": "blood"}} for _ in range(800)]
        m = confusion(rows, ["ovary"] * 800, "LLM", "blood", "author_exact_tissue")
        self.assertEqual((m["tp"], m["fp"], m["fn"]), (0, 800, 0))

    def test_bad_denominator_rejected(self):
        with self.assertRaisesRegex(ValueError, "800"):
            confusion([], [], "LLM", "lung", "author_exact_tissue")

    def test_missing_model_layer_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing layer"):
            confusion([{}] * 800, ["lung"] * 800,
                      "LLM", "lung", "author_exact_tissue")

    def test_unknown_mode_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown parser"):
            select({"tissue": "lung"}, "lung", "nonsense")


if __name__ == "__main__":
    unittest.main()
