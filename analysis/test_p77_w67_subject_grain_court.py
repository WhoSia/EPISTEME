"""W67: synthetic invariants; original archive integration is run separately."""
import unittest
from p77_w67_subject_grain_court import parse_json_stream, pool_lower_bound

class W67SubjectTests(unittest.TestCase):
    def test_disjoint_impossible_with_2400_rows(self):
        r = pool_lower_bound(2400, 6, 800)
        self.assertEqual(r['subject_memberships_required'], 4800)
        self.assertEqual(r['minimum_repeated_memberships_if_only_published_pool'], 2400)
        self.assertFalse(r['pairwise_disjoint_possible_under_same_pool'])

    def test_disjoint_possible_with_sufficient_unarchived_rows(self):
        self.assertTrue(pool_lower_bound(4800, 6, 800)['pairwise_disjoint_possible_under_same_pool'])

    def test_four_or_fewer_subjects_on_pool(self):
        r = pool_lower_bound(2400, 3, 800)
        self.assertTrue(r['pairwise_disjoint_possible_under_same_pool'])
        self.assertEqual(r['minimum_repeated_memberships_if_only_published_pool'], 0)

    def test_validation_positive_denominators(self):
        for args in [(0, 6, 800), (2400, 0, 800), (2400, 6, -1)]:
            with self.assertRaises(ValueError):
                pool_lower_bound(*args)

    def test_parse_concatenated_and_array(self):
        want = [{'x': 1}, {'x': 2}]
        self.assertEqual(parse_json_stream(b'{"x":1}{"x":2}'), want)
        self.assertEqual(parse_json_stream(b'[{"x":1},{"x":2}]'), want)

    def test_reject_non_json_record(self):
        with self.assertRaisesRegex(ValueError, 'not a JSON object'):
            parse_json_stream(b'[1,2,3]')

    def test_counting_does_not_assume_metadata_identity(self):
        r = pool_lower_bound(2400, 6, 800)
        self.assertIn('different definition', r['note'])

if __name__ == '__main__':
    unittest.main()
