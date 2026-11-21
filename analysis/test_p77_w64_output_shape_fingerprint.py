"""W64 zero/one-key model-output shape validation."""
import json
import unittest
from p77_w64_output_shape_fingerprint import parse_rows, structural_count


class OutputShapeTests(unittest.TestCase):
    def test_json_lines_and_array(self):
        rows = [{"LLM": {}}, {"LLM": {"k": "v"}}]
        self.assertEqual(parse_rows(json.dumps(rows).encode()), rows)
        self.assertEqual(parse_rows(b'{"LLM":{}}\n{"LLM":{"k":"v"}}\n'), rows)

    def test_one_key_fingerprint(self):
        data = [{"LLM": {}}] * 260 + [{"LLM": {"tissue": "lung"}}] * 540
        out = structural_count(data, "LLM")
        self.assertEqual((out["n"], out["zero_key"], out["one_key"],
                          out["two_or_more_keys"]), (800, 260, 540, 0))
        self.assertTrue(out["all_at_most_one_key"])

    def test_multi_key_gpt_control(self):
        data = [{"LLM+CEDAR": {"a": "1", "b": "2"}} for _ in range(800)]
        self.assertFalse(structural_count(data, "LLM+CEDAR")["all_at_most_one_key"])

    def test_reject_corrupt_or_missing_layer(self):
        data = [{"LLM": {"tissue": "lung"}}] * 799 + [{}]
        with self.assertRaisesRegex(ValueError, "Non-dictionary"):
            structural_count(data, "LLM")

    def test_reject_unexpected_denominator(self):
        with self.assertRaisesRegex(ValueError, "800"):
            structural_count([{"LLM": {}}], "LLM")


if __name__ == "__main__":
    unittest.main()
