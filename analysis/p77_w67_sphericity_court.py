"""W67: three-level repeated-measures sphericity algebra, not a paper p-value rerun.

All input triples are paired observations (baseline, LLM+DD, LLM+CEDAR).
The actual manuscript 6-by-3 per-repository raw table has NOT been identified.
Reported variances (.013,.080) are approximate, without known covariance.
"""
import json
import math
import sys


def sample_covariance(x, y):
    if len(x) != len(y) or len(x) < 2:
        raise ValueError('Paired arrays must have equal length at least 2')
    mx, my = sum(x)/len(x), sum(y)/len(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(len(x)-1)


def sample_variance(x):
    return sample_covariance(x,x)


def three_pairwise_differences(triples):
    if len(triples) < 3:
        raise ValueError('At least three paired subjects needed')
    if any(len(row)!=3 or any(not isinstance(x,(int,float)) or
            not math.isfinite(x) or x<0 or x>1 for x in row) for row in triples):
        raise ValueError('Recall observations must be finite triples inside [0,1]')
    d1 = [dd-b for b,dd,cedar in triples]
    d2 = [cedar-b for b,dd,cedar in triples]
    d3 = [cedar-dd for b,dd,cedar in triples]
    var1, var2, var3 = map(sample_variance,(d1,d2,d3))
    cov = sample_covariance(d1,d2)
    if not math.isclose(var3, var1+var2-2*cov,rel_tol=1e-9,abs_tol=1e-12):
        raise AssertionError('Paired difference identity violated')
    return {
        'subjects':len(triples),
        'sample_var_DD_minus_baseline':var1,
        'sample_var_CEDAR_minus_baseline':var2,
        'sample_var_CEDAR_minus_DD':var3,
        'sample_cov_two_baseline_sharing_differences':cov,
        'all_three_pairwise_variances_equal_in_sample':
            max(var1,var2,var3)-min(var1,var2,var3)<1e-10,
        'caution':'Sample variance equality is an algebraic check, not a statistical sphericity test.',
    }


def unidentified_third_variance_bounds(var_dd_base, var_cedar_base):
    """Cauchy-Schwarz range of third difference variance, with covariance unknown."""
    if not (isinstance(var_dd_base,(int,float)) and isinstance(var_cedar_base,(int,float)) and
            math.isfinite(var_dd_base) and math.isfinite(var_cedar_base) and
            var_dd_base >= 0 and var_cedar_base >= 0):
        raise ValueError('Non-negative finite variances required')
    a,b=math.sqrt(var_dd_base),math.sqrt(var_cedar_base)
    return {'known_variances':[var_dd_base,var_cedar_base],
            'third_var_lower_bound':(a-b)**2,
            'third_var_upper_bound':(a+b)**2,
            'third_var_identified':math.isclose(a*b,0,abs_tol=1e-14),
            'reported_ratio_if_second_divided_by_first':
                var_cedar_base / var_dd_base if var_dd_base>0 else None,
            'limitation':('The two difference scores share the baseline and are paired; '
                          'their covariance is unreported. A conventional F(5,5) '
                          'independent-variance test is not established solely from these summaries. '
                          'The third pairwise variance and original 6x3 data remain unknown.')}


if __name__ == '__main__':
    if len(sys.argv) != 1:
        raise SystemExit('usage: python p77_w67_sphericity_court.py')
    print(json.dumps(unidentified_third_variance_bounds(.013,.080), indent=2))
