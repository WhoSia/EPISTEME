"""W62 probability-mass weighting bound: counterexample and edge tests."""
import unittest
from p77_w62_accession_weighting_bound import bound


class WeightBoundTests(unittest.TestCase):
    def test_all_unique_no_shift(self):
        out = bound(["A", "B", "C", "D"])
        self.assertEqual(out["total_variation_weight_shift"], 0)
        self.assertEqual(out["maximum_accession_row_weight_ratio_to_unique_weight"], 1)

    def test_repeated_one_of_two(self):
        out = bound(["A", "A", "A", "B"])
        self.assertAlmostEqual(out["total_variation_weight_shift"], .25)
        self.assertAlmostEqual(out["maximum_accession_row_weight_ratio_to_unique_weight"], 1.5)

    def test_actual_liver_multiplicity_signature(self):
        keys = []
        sizes = [1] * 728 + [2] * 11 + [3] * 9 + [4] * 3 + [11]
        for i, n in enumerate(sizes):
            keys.extend([f"SAMN{i}"] * n)
        out = bound(keys)
        self.assertEqual((out["row_count"], out["distinct_accession_count"]), (800, 752))
        self.assertAlmostEqual(out["upper_bound_mean_score_difference_percentage_points"], 5.808510638297872)
        self.assertAlmostEqual(out["maximum_accession_row_weight_ratio_to_unique_weight"], 10.34)

    def test_all_identical_no_weight_shift(self):
        out = bound(["X"] * 10)
        self.assertEqual(out["total_variation_weight_shift"], 0)

    def test_reject_missing_accession(self):
        with self.assertRaises(ValueError):
            bound(["A", ""])


if __name__ == "__main__":
    unittest.main()
