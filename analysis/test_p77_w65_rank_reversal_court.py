"""W65: fail-closed regression tests for ranking reversals and ties."""
import unittest
from p77_w65_rank_reversal_court import sign, audit


class RankTests(unittest.TestCase):
    def test_tie_is_not_reversal(self):
        self.assertEqual(sign(0.2, 0.2), 0)
        self.assertEqual(sign(0.1, 0.2), -1)
        self.assertEqual(sign(0.2, 0.1), 1)

    def test_strict_positive_normalized_negative(self):
        fixture = {"results": {"ovarian": {"models": {"gpt4": {
            "BioSample": {"blood": {
                "author_exact_tissue": {"precision": 0.4, "recall": 0.2, "f1": 0.3},
                "alias_casefold_strip": {"precision": 1, "recall": 0.99, "f1": 0.995},
            }},
            "LLM+CEDAR": {"blood": {
                "author_exact_tissue": {"precision": 0.7, "recall": 0.6, "f1": 0.64},
                "alias_casefold_strip": {"precision": 0.8, "recall": 0.7, "f1": 0.74},
            }},
        }}}}}
        out = audit(fixture)
        self.assertEqual(out["pairwise_metric_comparisons"], 3)
        self.assertGreaterEqual(out["strict_rank_reversals"], 1)
        self.assertTrue(any(x["metric"] == "f1" for x in out["reversals"]))

    def test_missing_model_query_rejected(self):
        fixture = {"results": {"liver": {"models": {"gpt4": {
            "BioSample": {"liver": {
                "author_exact_tissue": {"precision": .5, "recall": .5, "f1": .5},
                "alias_casefold_strip": {"precision": .5, "recall": .5, "f1": .5}}},
            "LLM": {},
        }}}}}
        with self.assertRaisesRegex(ValueError, "queries diverge"):
            audit(fixture)

    def test_empty_result(self):
        self.assertEqual(audit({"results": {"lung": {"models": {}}}})["strict_rank_reversals"], 0)


if __name__ == "__main__":
    unittest.main()
