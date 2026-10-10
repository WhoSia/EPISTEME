"""P71-P5: endogenous audit and robust switching boundary, zero external calls.

All propositions are elementary conditional decision arithmetic/countermodels
against existing performative prediction and minimax regret literature.
No new universal identification or empirical human/model result is claimed.
"""
from __future__ import annotations
from fractions import Fraction as F
import json

def regret_comparison(lower:F,upper:F):
    """Net SWITCH-RETAIN utility d ranges over nonempty interval [lower,upper].
    Ex-post oracle chooses max(d,0); regret of SWITCH=max(-d,0), RETAIN=max(d,0).
    """
    if type(lower) is not F or type(upper) is not F or lower>upper:
        raise ValueError("P71_EXACT_NONEMPTY_EFFECT_INTERVAL_REQUIRED")
    r_switch=max(F(0),-lower)
    r_retain=max(F(0),upper)
    rule=("SWITCH_MINIMAX_REGRET" if r_switch<r_retain else
          "RETAIN_MINIMAX_REGRET" if r_retain<r_switch else
          "TIE_MINIMAX_REGRET")
    robust=("SWITCH_ROBUST_DOMINANCE" if lower>0 else
            "RETAIN_ROBUST_DOMINANCE" if upper<0 else "ROBUST_HOLD")
    return {"lower":str(lower),"upper":str(upper),
            "switch_worst_regret":str(r_switch),
            "retain_worst_regret":str(r_retain),
            "minimax_regret_choice":rule,
            "robust_dominance":robust,
            "claim_type":"CLASSICAL_DECISION_RULE_ACCOUNTING_NOT_A_NEW_THEOREM"}

def audit_shift_bound(lower:F,upper:F,delta:F):
    """Conditional |d_postaudit-d_preaudit|<=delta implies
    postaudit d in [lower-delta,upper+delta]. If no delta, no certificate.
    This bound itself has no causal basis absent observed audit controls.
    """
    if not all(type(x) is F for x in (lower,upper,delta)):
        raise ValueError("P71_EXACT_FRACTIONS_ONLY")
    if lower>upper or delta<0:raise ValueError("P71_BAD_SHIFT_BOUND")
    out=regret_comparison(lower-delta,upper+delta)
    return {**out,"delta":str(delta),
            "bound_authority":"CONDITIONAL_ON_INDEPENDENT_AUDIT_SHIFT_CERTIFICATE"}

def observational_pair():
    """Audit only (A=1) observational law same; no-audit (A=0) effects differ.
    Both worlds report audited d=1/4, while unaudited d=±1/4. A model
    observing only A=1 and the audited net utility cannot discriminate them.
    """
    worlds=(
        {"world":"W_plus","audit_d":F(1,4),"no_audit_d":F(1,4)},
        {"world":"W_minus","audit_d":F(1,4),"no_audit_d":F(-1,4)}
    )
    observed={(w["audit_d"],F(1)) for w in worlds}
    assert len(observed)==1
    assert len({w["no_audit_d"]>F(0) for w in worlds})==2
    return {"same_observed_audit_response":str(worlds[0]["audit_d"]),
            "observed_audit_indicator":"1_only",
            "unobserved_no_audit_effect_world_plus":str(worlds[0]["no_audit_d"]),
            "unobserved_no_audit_effect_world_minus":str(worlds[1]["no_audit_d"]),
            "causal_identification":"FAIL_WITH_AUDIT_ONLY_OBSERVATIONS",
            "constructive_synthetic_counterworlds":2}

def self_test():
    x=regret_comparison(F(-1,5),F(3,5))
    assert x["minimax_regret_choice"]=="SWITCH_MINIMAX_REGRET"
    assert x["robust_dominance"]=="ROBUST_HOLD"
    y=regret_comparison(F(-3,5),F(1,5))
    assert y["minimax_regret_choice"]=="RETAIN_MINIMAX_REGRET"
    assert y["robust_dominance"]=="ROBUST_HOLD"
    assert regret_comparison(F(1,5),F(3,5))["robust_dominance"]=="SWITCH_ROBUST_DOMINANCE"
    assert regret_comparison(F(-3,5),F(-1,5))["robust_dominance"]=="RETAIN_ROBUST_DOMINANCE"
    t=audit_shift_bound(F(1,10),F(3,10),F(1,5))
    assert t["lower"]=="-1/10"
    assert t["robust_dominance"]=="ROBUST_HOLD"
    assert audit_shift_bound(F(1,10),F(3,10),F(0))["robust_dominance"]=="SWITCH_ROBUST_DOMINANCE"
    pair=observational_pair()
    assert pair["causal_identification"].startswith("FAIL")
    for bad in [(F(1,2),F(1,4)),(F(1,5),F(-1,5))]:
        try:regret_comparison(*bad)
        except ValueError:pass
        else:raise AssertionError("P71_BAD_INTERVAL_PROMOTED")
    try:audit_shift_bound(F(-1,5),F(1,5),F(-1,10))
    except ValueError:pass
    else:raise AssertionError("P71_NEGATIVE_AUDIT_SHIFT_ACCEPTED")
    return {"kind":"P71_ENDOGENOUS_AUDIT_STRESS_COURT",
            "minimax_vs_robust":"DISTINCT_DECISION_OBJECTIVES",
            "finite_regret_examples":"PASS",
            "conditional_audit_shift":"TRIANGLE_INEQUALITY_ONLY",
            "audit_only_no_audit_identification":"FAIL_BY_TWO_WORLDS",
            "source_model_or_human_evidence":"NONE",
            "real_independent_human_reviews":0,
            "provider_calls":0,
            "paper_claim":"A_FALSIFICATION_DESIGN_NOT_A_NOVEL_CAUSAL_THEOREM"}

if __name__=="__main__":
    outcome=self_test()
    print("P71_ENDOGENOUS_AUDIT_COURT_SELFTEST_PASS counterworlds=2 no_human_claims=true model_calls=0")
    print(json.dumps(outcome,sort_keys=True))
