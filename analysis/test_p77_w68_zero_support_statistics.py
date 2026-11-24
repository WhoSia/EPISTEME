import unittest
from p77_w68_zero_support_statistics import calculate

class ZeroSupportTests(unittest.TestCase):
    def test_invalid_matrix(self):
        for x in ([[1,2,3]],[[0,.1,.2],[0,.1,2]],[[0,0,0],[0,0,0]]):
            with self.assertRaises(ValueError): calculate(x)
    def test_all_tie_row_not_independent_information(self):
        m=[[0,.1,.8],[.8,0,0],[.2,.1,.5],[.1,0,.9],[0,.2,.6]]
        a,b=calculate(m),calculate(m+[[0,0,0]])
        self.assertEqual(a['df'],[2,8]); self.assertEqual(b['df'],[2,10])
        self.assertAlmostEqual(a['friedman'],b['friedman'])
        for v,w in zip(a['means'],b['means']): self.assertAlmostEqual(v*5/6,w)
    def test_with_original_workbook_values(self):
        m=[[0,0,.435897435897435],[0,0,0],[.0942760942760942,0,.646319569120287],[.8,0,0],[0,.122807017543859,.91578947368421],[0,0,.642276422764227]]
        a,b=calculate(m),calculate(m[:1]+m[2:])
        self.assertAlmostEqual(a['F'],2.740247265706394)
        self.assertAlmostEqual(a['p'],.11248014006749694)
        self.assertAlmostEqual(b['F'],2.9544773098774697)
        self.assertAlmostEqual(b['p'],.10944148751441368)
        self.assertAlmostEqual(a['friedman'],b['friedman'])
