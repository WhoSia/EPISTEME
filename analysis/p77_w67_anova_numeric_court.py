"""W67: internal arithmetic consistency of R2 Appendix-C displayed F and p.

The survival function below is *exact* for F(2, d2) with d2>0.
This checks the reported triplet (df, F, p), not the unpublished raw
ANOVA calculation, repeated-measures assumptions or original software.
"""
import json
import math


def f_survival_numerator_df2(f_value, denominator_df):
    if not (math.isfinite(f_value) and f_value>=0 and
            math.isfinite(denominator_df) and denominator_df>0):
        raise ValueError('Finite nonnegative F and positive denominator df required')
    return (denominator_df/(denominator_df+2*f_value))**(denominator_df/2)


def f_from_p_numerator_df2(p, denominator_df):
    if not (0<p<=1 and math.isfinite(p) and
            denominator_df>0 and math.isfinite(denominator_df)):
        raise ValueError('p must be (0,1]; denominator df positive finite')
    return denominator_df/2*(p**(-2/denominator_df)-1)


def adjudicate(display_f, display_p, denominator_df, f_rounding_half_unit, p_rounding_half_unit, alpha=0.05):
    if f_rounding_half_unit<0 or p_rounding_half_unit<0:
        raise ValueError('Rounding half-unit must be nonnegative')
    p_nominal=f_survival_numerator_df2(display_f,denominator_df)
    p_low=f_survival_numerator_df2(display_f+f_rounding_half_unit, denominator_df)
    p_high=f_survival_numerator_df2(max(0,display_f-f_rounding_half_unit),denominator_df)
    if not 0<=display_p<=1:
        raise ValueError('Reported p must belong to [0,1]')
    reported_p_bounds=[max(0,display_p-p_rounding_half_unit),
                       min(1,display_p+p_rounding_half_unit)]
    return {
        'reported_F':display_f,'numerator_df':2,'denominator_df':denominator_df,
        'reported_p':display_p,'recomputed_standard_F_survival_p':p_nominal,
        'p_range_allowing_displayed_F_rounding':[p_low,p_high],
        'p_range_allowing_reported_p_rounding':reported_p_bounds,
        'reported_p_consistent_after_both_roundings':
            p_low <= reported_p_bounds[1] and p_high >= reported_p_bounds[0],
        'F_implied_by_reported_p':f_from_p_numerator_df2(display_p,denominator_df)
            if display_p>0 else None,
        'reported_significant_at_alpha':display_p<alpha,
        'recomputed_significant_at_alpha':p_nominal<alpha,
        'warning':('Only internal standard-F(2,df2) arithmetic; original raw data and '
                   'potential nonstandard adjustments are unavailable. A mismatch '
                   'does not independently establish a wrong significance decision.'),
    }


def court():
    return {
        'BioSample':adjudicate(27.68,.0001,10,.005,.00005),
        'GEO':adjudicate(1.08,.439,10,.005,.0005),
        'source':'Sundaram et al. 2026 GigaScience R2 prepublication manuscript Appendix C, BioSample Tables 5-7 and GEO Table 9',
    }

if __name__=='__main__':
    print(json.dumps(court(),indent=2))
