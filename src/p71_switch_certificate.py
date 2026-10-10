"""EPISTEME-P71 P0: proof-gated robust representation switching.

This is a finite rational decision certificate under explicit external bounds,
not a new general causal-identification algorithm or experimental result.
Unknown warrant, missing causal transport shift bounds, incomplete contract
support and unaudited costs must yield HOLD, not an optimistic point decision.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
import json

class AuthorityHold(ValueError):
    pass

def finite(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise AuthorityHold("P71_EXACT_RATIONAL_INPUT_REQUIRED")
    return F(x)

@dataclass(frozen=True)
class Warrant:
    independent_human_review_count:int
    required_review_count:int
    packet_oracle_adjudicated:bool
    role_and_proof_bridge_certified:bool
    temporal_scope_certified:bool
    source_license_and_custody_verified:bool
    inference_unit_and_trial_protocol_frozen:bool

    def missing(self):
        failures=[]
        if self.independent_human_review_count<self.required_review_count or self.required_review_count<=0:
            failures.append("INDEPENDENT_PACKET_REVIEW_INCOMPLETE")
        if not self.packet_oracle_adjudicated:failures.append("PACKET_ORACLE_UNCERTIFIED")
        if not self.role_and_proof_bridge_certified:failures.append("PROOF_BRIDGE_UNCERTIFIED")
        if not self.temporal_scope_certified:failures.append("TEMPORAL_SCOPE_UNCERTIFIED")
        if not self.source_license_and_custody_verified:failures.append("CUSTODY_OR_LICENSE_HOLD")
        if not self.inference_unit_and_trial_protocol_frozen:failures.append("PROSPECTIVE_PROTOCOL_HOLD")
        return failures

@dataclass(frozen=True)
class ContractBound:
    contract:str
    target_effect_estimate:F
    estimation_error_bound:F
    cross_ecology_shift_bound:F
    reward_per_correct_execution:F
    migration_cost:F
    audit_cost:F
    irreversible_loss_bound:F=F(0)

    def interval(self):
        point=finite(self.target_effect_estimate)
        error=finite(self.estimation_error_bound)
        shift=finite(self.cross_ecology_shift_bound)
        reward=finite(self.reward_per_correct_execution)
        migration=finite(self.migration_cost)
        audit=finite(self.audit_cost)
        loss=finite(self.irreversible_loss_bound)
        if not self.contract or any(x<0 for x in (error,shift,reward,migration,audit,loss)):
            raise AuthorityHold("P71_INVALID_COST_OR_UNCERTAINTY")
        if abs(point)>1:raise AuthorityHold("P71_BINARY_EFFECT_OUT_OF_RANGE")
        d=error+shift
        lo=max(F(-1),point-d);hi=min(F(1),point+d)
        # Negative utility of unobserved adverse downstream consequences is
        # included as worst-case loss in conservative lower endpoint.
        return (reward*lo-migration-audit-loss,
                reward*hi-migration-audit)

def decide(warrant:Warrant,bounds:list[ContractBound], *,
           required_contracts:tuple[str,...]=("strict_schema","json_object")):
    missing=warrant.missing()
    names=[b.contract for b in bounds]
    if len(names)!=len(set(names)):
        raise AuthorityHold("P71_DUPLICATED_CONTRACT_LEDGER")
    missing_contracts=set(required_contracts)-set(names)
    if missing_contracts:missing.append("INCOMPLETE_CONTRACT_SUPPORT")
    if missing:
        return {"verdict":"P71_INSTITUTIONAL_SWITCH_HOLD",
                "missing":sorted(set(missing)),
                "contract_intervals":{},
                "note":"No authority to recommend migration even when a point estimate looks positive."}
    intervals={b.contract:b.interval() for b in bounds}
    lower=min(intervals[c][0] for c in required_contracts)
    upper=max(intervals[c][1] for c in required_contracts)
    # For robust dominance, accept only if every required contract's
    # lower bound strictly exceeds 0. Reject only when ALL upper bounds < 0.
    if lower>0:verdict="P71_ROBUST_SWITCH_CERTIFIED_CONDITIONALLY"
    elif upper<0:verdict="P71_ROBUST_REJECT_SWITCH_CONDITIONALLY"
    else:verdict="P71_DECISION_INDETERMINATE"
    return {
      "verdict":verdict,
      "minimum_contract_lower_utility":str(lower),
      "maximum_contract_upper_utility":str(upper),
      "per_contract_intervals":{k:[str(a),str(b)] for k,(a,b) in intervals.items()},
      "assumptions":"Externally certified full warrant, effect/shift bounds and costs. Certificate arithmetic not certification of inputs.",
      "publication_claim":"CONDITIONAL_DECISION_ALGORITHM_NOT_CAUSAL_TRANSPORT_RESULT",
    }

def self_test():
    complete=Warrant(32,32,True,True,True,True,True)
    held=Warrant(0,32,False,False,False,True,False)
    b1=ContractBound("strict_schema",F(2,5),F(1,20),F(1,20),
                     F(10),F(1),F(1,2),F(1,4))
    b2=ContractBound("json_object",F(2,5),F(1,20),F(1,20),
                     F(10),F(1),F(1,2),F(1,4))
    assert decide(held,[b1,b2])["verdict"]=="P71_INSTITUTIONAL_SWITCH_HOLD"
    assert decide(complete,[b1,b2])["verdict"]=="P71_ROBUST_SWITCH_CERTIFIED_CONDITIONALLY"
    bad=ContractBound("json_object",F(-1,2),F(1,20),F(1,20),
                      F(10),F(1),F(1,2),F(1,4))
    assert decide(complete,[b1,bad])["verdict"]=="P71_DECISION_INDETERMINATE"
    both_bad=ContractBound("strict_schema",F(-1,2),F(1,20),F(1,20),
                           F(10),F(1),F(1,2),F(1,4))
    assert decide(complete,[both_bad,bad])["verdict"]=="P71_ROBUST_REJECT_SWITCH_CONDITIONALLY"
    missing=decide(complete,[b1])
    assert "INCOMPLETE_CONTRACT_SUPPORT" in missing["missing"]
    # Neither equal observable source performance nor positive point benefit
    # identifies a target effect absent a transport restriction.
    uncertain=ContractBound("strict_schema",F(2,5),F(0),F(1),
                            F(10),F(0),F(0))
    assert decide(complete,[uncertain,uncertain.__class__("json_object",
                         F(2,5),F(0),F(1),F(10),F(0),F(0))])["verdict"]=="P71_DECISION_INDETERMINATE"
    for kwargs in [{"target_effect_estimate":F(2)},
                   {"migration_cost":F(-1)}]:
        d={**b1.__dict__,**kwargs}
        try:ContractBound(**d).interval()
        except AuthorityHold:pass
        else:raise AssertionError("P71_INVALID_BOUND_PROMOTED")
    print("P71_SWITCH_CERTIFICATE_SELFTEST_PASS warrant_hold=PASS contract_adversary=PASS wide_transport_hold=PASS real_human_reviews=0 provider_calls=0")

if __name__=="__main__":
    self_test()
