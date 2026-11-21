"""W66: six query task-grain checks, no unpublished run inference."""
import unittest
from p77_w66_subcohort_grain_audit import describe_task_grain


class SubcohortGrainTests(unittest.TestCase):
    def test_distinct_positive_labels_share_candidate_pool(self):
        labels = ['lung'] * 616 + ['blood'] * 64 + ['unknown'] * 120
        rows = [{} for _ in range(800)]
        out = describe_task_grain(rows, labels, 'lung')
        self.assertEqual(out['shared_source_candidate_rows_for_both_queries'], 800)
        self.assertEqual(out['organ_relevant_rows'], 616)
        self.assertEqual(out['blood_relevant_rows'], 64)
        self.assertEqual(out['overlap_of_heuristic_relevant_positive_indices'], 0)
        self.assertEqual(out['remaining_rows_in_neither_relevant_subset'], 120)

    def test_denominator_checked(self):
        with self.assertRaisesRegex(ValueError, '800'):
            describe_task_grain([{}] * 799, ['lung'] * 800, 'lung')
        with self.assertRaisesRegex(ValueError, '800'):
            describe_task_grain([{}] * 800, ['lung'] * 799, 'lung')

    def test_no_assumption_of_run_independence(self):
        out = describe_task_grain([{}] * 800, ['ovary'] * 457 +
                                  ['blood'] * 154 + ['unknown'] * 189, 'ovary')
        self.assertIn('does not identify manuscript ANOVA', out['interpretation'])
