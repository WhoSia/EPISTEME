"""W67: exact analytic F-tail checks and wrong-df safeguards."""
import unittest
from p77_w67_anova_numeric_court import (
    f_survival_numerator_df2,f_from_p_numerator_df2,adjudicate,court
)

class AnovaNumericTests(unittest.TestCase):
    def test_biosample_rounding_accepts_p(self):
        c=court()['BioSample']
        self.assertTrue(c['reported_p_consistent_after_both_roundings'])
        self.assertAlmostEqual(c['recomputed_standard_F_survival_p'],8.383778242804627e-05)
        self.assertTrue(c['recomputed_significant_at_alpha'])

    def test_geo_discrepancy_well_beyond_display_rounding(self):
        c=court()['GEO']
        self.assertFalse(c['reported_p_consistent_after_both_roundings'])
        self.assertAlmostEqual(c['recomputed_standard_F_survival_p'],.376124934671626)
        self.assertAlmostEqual(c['F_implied_by_reported_p'],.8949089325396331)
        self.assertFalse(c['reported_significant_at_alpha'])
        self.assertFalse(c['recomputed_significant_at_alpha'])

    def test_p_monotonicity_and_inverse(self):
        for f in (0,1.08,27.68,100):
            p=f_survival_numerator_df2(f,10)
            self.assertAlmostEqual(f_from_p_numerator_df2(p,10),f,places=8)
        self.assertLess(f_survival_numerator_df2(2,10),f_survival_numerator_df2(1,10))

    def test_invalid_arguments_rejected(self):
        for args in [(-1,10),(1,0),(float('nan'),10),(1,float('inf'))]:
            with self.assertRaises(ValueError):f_survival_numerator_df2(*args)
        with self.assertRaises(ValueError):adjudicate(1.08,1.4,10,.005,.0005)
        with self.assertRaises(ValueError):adjudicate(1.08,.439,10,-.005,.0005)

    def test_wrong_numerator_df_is_not_supported(self):
        # Do not silently substitute F(3,10) into F(2,10) formula.
        self.assertEqual(court()['GEO']['numerator_df'],2)

if __name__=='__main__':unittest.main()
