"""EPISTEME-P70: finite, provider-free transport identification boundary.

The arithmetic checks *conditional formulas*, NOT causal identification in any
hosted LLM system. All examples are labelled synthetic countermodels.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping


class TransportHold(ValueError):
    """Do not promote an unobserved mechanism or a missing bridge."""


@dataclass(frozen=True)
class Bridge:
    """Mechanism/evidence/channel invariance checklist, not an empirical proof."""
    oracle_answer_preserved: bool
    proof_sets_bijective: bool
    intervention_diagram_commutes: bool
    response_contract_comparable: bool
    mechanism_defined_independently_of_outcomes: bool

    def audit(self) -> None:
        if not all((
            self.oracle_answer_preserved,
            self.proof_sets_bijective,
            self.intervention_diagram_commutes,
            self.response_contract_comparable,
            self.mechanism_defined_independently_of_outcomes,
        )):
            raise TransportHold("P70_BRIDGE_UNCERTIFIED")
        # These structural checks NEVER prove behavioral effect invariance.


def _f(x: int | Fraction) -> Fraction:
    if not isinstance(x, (int, Fraction)):
        raise TransportHold("P70_REQUIRE_EXACT_RATIONAL_INPUT")
    return Fraction(x)


def conditional_transport_bound(
    source_effects: Mapping[str, Fraction],
    target_mechanism_mass: Mapping[str, Fraction],
    shift_tolerance: Mapping[str, Fraction],
    estimation_tolerance: Mapping[str, Fraction],
) -> dict:
    """Triangle-inequality interval, assuming bounded cross-ecology shifts.

    For each m: |tau_target(m,o)-tau_source(m,o)|<=epsilon_m.
    Also: |tau_source(m,o)-tau_estimate(m,o)|<=eta_m.
    Then |tau_target(o)-sum_m p_target(m)*tau_estimate(m,o)|
         <= sum_m p_target(m)*(epsilon_m+eta_m).
    The epsilon/eta bounds are assumptions or externally validated inputs, never
    learned by this function. Unit of effect is all-call binary success.
    """
    keys=set(target_mechanism_mass)
    if not keys or keys!=set(source_effects) or keys!=set(shift_tolerance) or keys!=set(estimation_tolerance):
        raise TransportHold("P70_POSITIVITY_OR_SUPPORT_FAILURE")
    mass={k:_f(v) for k,v in target_mechanism_mass.items()}
    if any(v<=0 for v in mass.values()) or sum(mass.values())!=1:
        raise TransportHold("P70_INVALID_TARGET_MECHANISM_DISTRIBUTION")
    effects={k:_f(v) for k,v in source_effects.items()}
    eps={k:_f(v) for k,v in shift_tolerance.items()}
    eta={k:_f(v) for k,v in estimation_tolerance.items()}
    if any(abs(v)>1 for v in effects.values()):
        raise TransportHold("P70_EFFECT_OUTSIDE_BINARY_OUTCOME_RANGE")
    if any(eps[k]<0 or eta[k]<0 for k in keys):
        raise TransportHold("P70_NEGATIVE_UNCERTAINTY")
    point=sum(mass[k]*effects[k] for k in keys)
    radius=sum(mass[k]*(eps[k]+eta[k]) for k in keys)
    return {
        "estimate_exact_rational":str(point),
        "radius_exact_rational":str(radius),
        "lower":str(max(Fraction(-1),point-radius)),
        "upper":str(min(Fraction(1),point+radius)),
        "authority":"CONDITIONAL_ARITHMETIC_ONLY_NO_HOSTED_IDENTIFICATION",
    }


def observationally_indistinguishable_worlds() -> dict:
    """Two synthetic worlds agree on all observed source/target anchors.

    Target intervention outcome is withheld. World A yields +1/4 effect,
    world B -1/4 effect. Source intervention effect is +1/4 in both.
    """
    observed={"source_identity":Fraction(1,2),
              "source_intervention":Fraction(3,4),
              "target_identity":Fraction(1,2)}
    a={**observed,"target_intervention":Fraction(3,4)}
    b={**observed,"target_intervention":Fraction(1,4)}
    assert all(a[k]==b[k] for k in observed)
    delta_a=a["target_intervention"]-a["target_identity"]
    delta_b=b["target_intervention"]-b["target_identity"]
    assert delta_a>0 and delta_b<0
    return {
        "same_observables":True,
        "target_effect_world_a":str(delta_a),
        "target_effect_world_b":str(delta_b),
        "conclusion":"UNIDENTIFIABLE_WITHOUT_TRANSPORT_RESTRICTION",
        "scope":"SYNTHETIC_CONSTRUCTIVE_COUNTEREXAMPLE_ONLY",
    }


def self_test() -> None:
    f=Fraction
    good=Bridge(True,True,True,True,True)
    good.audit()
    for field in good.__dataclass_fields__:
        bad=Bridge(**{x: (x!=field) for x in good.__dataclass_fields__})
        try:bad.audit()
        except TransportHold:pass
        else:raise AssertionError("P70_FALSE_BRIDGE_PROMOTED "+field)
    a=conditional_transport_bound(
        {"provenance":f(1,4),"guard":f(-1,4)},
        {"provenance":f(3,4),"guard":f(1,4)},
        {"provenance":f(1,8),"guard":f(1,8)},
        {"provenance":f(1,16),"guard":f(1,16)},
    )
    assert a["estimate_exact_rational"]=="1/8"
    assert a["radius_exact_rational"]=="3/16"
    assert a["lower"]=="-1/16" and a["upper"]=="5/16"
    assert observationally_indistinguishable_worlds()["target_effect_world_b"]=="-1/4"
    for args in [
        ({"a":f(1,2)},{"a":f(1,2),"b":f(1,2)},{"a":f(0)},{"a":f(0)}),
        ({"a":f(1,2)},{"a":f(1)},{"a":f(-1,5)},{"a":f(0)}),
        ({"a":f(1,2)},{"a":f(1,2)},{"a":f(0)},{"a":f(0)}),
    ]:
        try:conditional_transport_bound(*args)
        except TransportHold:pass
        else:raise AssertionError("P70_BROKEN_SUPPORT_GATE")
    exact=conditional_transport_bound({"a":f(1,4)},{"a":f(1)},{"a":f(0)},{"a":f(0)})
    assert exact["lower"]=="1/4"==exact["upper"]
    print("P70_TRANSPORT_THEORY_SELFTEST_PASS toy_worlds=2 invalid_bridges=5 provider_calls=0")


if __name__=="__main__":
    import argparse,json
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:self_test()
    else:print(json.dumps(observationally_indistinguishable_worlds(),indent=2))
