"""Optional real-archive integration contract for W66 (no data committed).

To run on held original: EPISTEME_W66_ZIP="/path/to/Data.zip" python -m unittest
discover -s analysis -p 'test_p77_w66_*.py' -v
Without the environmental source path, the source-contract test is skipped.
"""
import os
import unittest
from p77_w66_parser_factorial_and_label_court import audit


@unittest.skipUnless(os.environ.get('EPISTEME_W66_ZIP'),
                     'Original Zenodo ZIP path not supplied')
class W66OriginalSourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = audit(os.environ['EPISTEME_W66_ZIP'])

    def test_actual_aggregate_invariants(self):
        r = self.r
        self.assertEqual(r['retrieval_cells'], 56)
        self.assertEqual(r['rank_metric_comparisons'], 108)
        self.assertEqual(r['cells_changed_by_alias_only'], 1)
        self.assertEqual(r['cells_changed_by_normalization_only'], 34)
        self.assertEqual(r['strict_rank_reversals_vs_original'],
                         {'alias_only': 0, 'normalize_only': 2,
                          'alias_and_normalize': 2})

    def test_source_label_alignment_is_unique_under_cyclic_offsets(self):
        d = self.r['source_label_circular_controls']
        self.assertEqual({k: d[k]['number_of_circular_offsets_with_zero_tissue_conflicts']
                          for k in d}, {'liver': 1, 'lung': 1, 'ovarian': 1})
        self.assertEqual({k: d[k]['original']['tissue_values_with_multiple_labels']
                          for k in d}, {'liver': 0, 'lung': 0, 'ovarian': 0})

    def test_invalid_label_rotations_dont_falsify_rank_reversal(self):
        d = self.r['ovarian_blood_reversal_shift_control']
        self.assertEqual(d['recall']['rank_reversals_under_all_800_circular_offsets'], 794)
        self.assertEqual(d['f1']['rank_reversals_under_all_800_circular_offsets'], 721)
