"""W67: algebraic counterexamples to two-variance sphericity shortcut."""
import unittest
from p77_w67_sphericity_court import (
    three_pairwise_differences, unidentified_third_variance_bounds,
    sample_covariance, sample_variance,
)

class W67SphericityTests(unittest.TestCase):
    def test_reported_variance_bounds(self):
        x=unidentified_third_variance_bounds(.013,.080)
        self.assertAlmostEqual(x['reported_ratio_if_second_divided_by_first'],.080/.013)
        self.assertAlmostEqual(x['third_var_lower_bound'],0.0285019380136116)
        self.assertAlmostEqual(x['third_var_upper_bound'],0.1574980619863884)
        self.assertFalse(x['third_var_identified'])

    def test_matching_two_variances_do_not_suffice(self):
        ts=[(.3,.3+d,.3+d) for d in (.01,.02,.03,.04,.05,.06)]
        x=three_pairwise_differences(ts)
        self.assertAlmostEqual(x['sample_var_DD_minus_baseline'],x['sample_var_CEDAR_minus_baseline'])
        self.assertAlmostEqual(x['sample_var_CEDAR_minus_DD'],0)
        self.assertFalse(x['all_three_pairwise_variances_equal_in_sample'])

    def test_same_two_marginal_variances_different_third(self):
        d=(.01,.02,.03,.04,.05,.06)
        equal=three_pairwise_differences([(.3,.3+a,.3+a) for a in d])
        inverse=three_pairwise_differences([(.3,.3+a,.3+.07-a) for a in d])
        self.assertAlmostEqual(equal['sample_var_DD_minus_baseline'],inverse['sample_var_DD_minus_baseline'])
        self.assertAlmostEqual(equal['sample_var_CEDAR_minus_baseline'],inverse['sample_var_CEDAR_minus_baseline'])
        self.assertAlmostEqual(inverse['sample_var_CEDAR_minus_DD'],4*inverse['sample_var_DD_minus_baseline'])

    def test_paired_covariance_identity(self):
        rows=[(.3,.3+i/100,.3+(7-i)/100) for i in range(1,7)]
        r=three_pairwise_differences(rows)
        self.assertAlmostEqual(r['sample_var_CEDAR_minus_DD'],r['sample_var_DD_minus_baseline']+
            r['sample_var_CEDAR_minus_baseline']-2*r['sample_cov_two_baseline_sharing_differences'])

    def test_equal_identical_observations(self):
        r=three_pairwise_differences([(.5,.5,.5)]*6)
        self.assertTrue(r['all_three_pairwise_variances_equal_in_sample'])

    def test_validation(self):
        for x in [(-1,.08),(.01,float('nan'))]:
            with self.assertRaises(ValueError):unidentified_third_variance_bounds(*x)
        with self.assertRaises(ValueError):three_pairwise_differences([(.3,.2,.4)]*2)
        with self.assertRaises(ValueError):three_pairwise_differences([(.3,.2,1.2)]*6)
        with self.assertRaises(ValueError):sample_covariance([1,2],[1])

if __name__ == '__main__':unittest.main()
