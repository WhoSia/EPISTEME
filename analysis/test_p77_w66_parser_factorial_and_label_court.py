"""W66: exact model, deterministic label dependency and negative-control tests."""
import unittest
from p77_w66_parser_factorial_and_label_court import (
    contains, metrics, label_consistency, rotate, sign, reversal,
)


class W66Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'BioSample': {'tissue': 'Blood'},
                      'LLM+CEDAR': {'tissue': 'blood'}} for _ in range(800)]
        self.labels = ['blood'] * 800

    def test_exact_vs_value_only(self):
        self.assertFalse(contains({'tissue': 'Blood'}, 'blood'))
        self.assertTrue(contains({'tissue': 'Blood'}, 'blood', normalize=True))

    def test_alias_only_does_not_casefold(self):
        self.assertFalse(contains({'tissue_type': 'Blood'}, 'blood', alias=True))
        self.assertTrue(contains({'tissue_type': 'Blood'}, 'blood', alias=True, normalize=True))

    def test_original_key_preempts_fallback(self):
        row = {'tissue': 'wrong', 'tissue_type': 'blood'}
        self.assertFalse(contains(row, 'blood', alias=True, normalize=True))

    def test_normalization_does_not_infer_synonyms(self):
        self.assertFalse(contains({'tissue': 'whole blood'}, 'blood', normalize=True))
        self.assertFalse(contains({'description': 'blood'}, 'blood', normalize=True))

    def test_confusion_exact_vs_normalized(self):
        exact = metrics(self.rows, self.labels, 'BioSample', 'blood')
        normal = metrics(self.rows, self.labels, 'BioSample', 'blood', normalize=True)
        self.assertEqual((exact['tp'], exact['fn']), (0, 800))
        self.assertEqual((normal['tp'], normal['fn']), (800, 0))

    def test_repeated_token_consistency(self):
        x = label_consistency(self.rows, self.labels)
        self.assertEqual(x['distinct_normalized_tissue_values'], 1)
        self.assertEqual(x['minority_label_rows_within_same_tissue'], 0)
        self.assertEqual(x['rows_with_other_same_tissue_rows'], 800)

    def test_conflicting_labels_detected(self):
        bad = self.labels.copy()
        bad[0] = 'ovary'
        x = label_consistency(self.rows, bad)
        self.assertEqual(x['minority_label_rows_within_same_tissue'], 1)
        self.assertEqual(x['tissue_values_with_multiple_labels'], 1)

    def test_rotation_preserves_marginals_not_links(self):
        self.assertEqual(rotate(['a', 'b', 'c'], 1), ['b', 'c', 'a'])
        self.assertEqual(sorted(rotate(['a', 'b', 'c'], 2)), ['a', 'b', 'c'])

    def test_rank_sign_ties(self):
        self.assertEqual(sign(0), 0)
        self.assertEqual(sign(0.1), 1)
        self.assertEqual(sign(-0.1), -1)

    def test_missing_layer_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Missing layer'):
            metrics([{}] * 800, self.labels, 'BioSample', 'blood')

    def test_incorrect_denominator_rejected(self):
        with self.assertRaisesRegex(ValueError, '800'):
            metrics(self.rows, self.labels[:-1], 'BioSample', 'blood')

    def test_non_dictionary_rejected(self):
        with self.assertRaisesRegex(ValueError, 'dictionary'):
            contains('blood', 'blood')


if __name__ == '__main__':
    unittest.main()
