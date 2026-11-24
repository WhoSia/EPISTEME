import unittest
from p77_w68_label_rule_replay import predict, RULE, LUNG, LIVER, OVARY, compare, records, retrieval
class Tests(unittest.TestCase):
    def test_acronym_case(self):
        self.assertEqual(predict('HCC'), 'liver'); self.assertEqual(predict('HCC',LIVER),'unknown')
        self.assertEqual(predict('PBMC'), 'blood'); self.assertEqual(predict('PBMC',LUNG),'unknown')
    def test_plasma_precedence(self):
        self.assertEqual(predict('blood plasma', RULE),'blood'); self.assertEqual(predict('blood plasma',OVARY),'plasma')
    def test_word_boundary(self):
        self.assertEqual(predict('lunglike'),'lung'); self.assertEqual(predict('lunglike',whole_word=True),'unknown')
    def test_missing(self): self.assertEqual(predict(None),'unknown')
    def test_compare(self):
        self.assertEqual(compare(['lung']*800,['lung']*799+['unknown'])['matches'],799)
        with self.assertRaises(ValueError): compare([],[])
    def test_records(self):
        self.assertEqual(records(b'{"a":1}{"b":2}'),[{'a':1},{'b':2}])
        with self.assertRaises(ValueError): records(b'[1]')
    def test_self_reference(self):
        self.assertEqual(retrieval(['lung','blood'],['lung','blood'],'lung')['f1'],1)
        self.assertIsNone(retrieval(['lung'],['lung'],'blood')['f1'])
