import unittest
from p77_w63_author_example_audit import rule, search, evaluate

class ExampleAuditTests(unittest.TestCase):
    def test_rule_priority_and_original_case_behavior(self):
        self.assertEqual(rule('LUNG and blood'), 'lung')
        self.assertEqual(rule('PBMC'), 'unknown')
        self.assertEqual(rule('whole blood'), 'blood')
    def test_exact_key_and_exact_value(self):
        rows=[{'LLM':{'tissue':'blood'}},{'LLM':{'tissue_type':'blood'}},{'LLM':{'tissue':'Blood'}},{'LLM':{}}]
        self.assertEqual(search(rows,'LLM','blood'),[0])
    def test_mismatched_query_detectable(self):
        labels=['blood','ovary','blood']
        self.assertEqual(evaluate([0],labels,'blood')['tp'],1)
        self.assertEqual(evaluate([0],labels,'ovary')['tp'],0)

if __name__=='__main__': unittest.main()

