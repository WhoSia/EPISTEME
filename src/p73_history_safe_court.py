"""P73 P1: exact finite dynamic safe observation court, synthetic only.

Theorem/recurrence is an existing active machine diagnosis principle.  A
boolean attestation in a toy model is NOT real independent certification.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import json

@dataclass(frozen=True)
class State:
    world: str
    warranted: bool
    proof_token: str = "original_evidence_v1"
    reader_ready: bool = False

@dataclass(frozen=True)
class Action:
    name: str
    cost: F
    model_attested: bool = True
    available_worlds: frozenset[str] | None = None

def apply(s: State, a: Action):
    if a.name == "PREPARE":
        return "ready", State(s.world,s.warranted,s.proof_token,True)
    if a.name == "READ":
        return ("yes" if s.warranted else "no") if s.reader_ready else "unready",s
    if a.name == "DAMAGING_READ":
        return ("yes" if s.warranted else "no"),State(s.world,False,"revoked",s.reader_ready)
    if a.name == "UNVERIFIED_READ" or a.name.startswith("LOCAL_"):
        return ("yes" if s.warranted else "no"),s
    raise ValueError("P73_UNKNOWN_ACTION")

def safe(belief: frozenset[State],a:Action,full_identity:bool=False):
    if type(a.cost) is not F or a.cost<=0 or not a.model_attested:
        return False
    if a.available_worlds is not None and any(s.world not in a.available_worlds for s in belief):
        return False
    for s in belief:
        _,after=apply(s,a)
        if (s.warranted,s.proof_token)!=(after.warranted,after.proof_token):
            return False
        if full_identity and after!=s:
            return False
    return True

def exact_minimax(start:frozenset[State],actions:tuple[Action,...], *, full_identity=False):
    if not start or len({s.world for s in start})!=len(start):
        raise ValueError("P73_BAD_START")
    if len({a.name for a in actions})!=len(actions):
        raise ValueError("P73_DUPLICATE_ACTION")
    cache={};visiting=set()
    def solve(belief):
        if belief in cache:return cache[belief]
        if len({s.warranted for s in belief})==1:
            return (F(0),{"decision":"WARRANTED" if next(iter(belief)).warranted else "UNWARRANTED"})
        if belief in visiting:return None
        visiting.add(belief)
        winner=None
        for a in actions:
            if not safe(belief,a,full_identity):continue
            buckets={}
            for s in belief:
                response,new=apply(s,a)
                buckets.setdefault(response,set()).add(new)
            buckets={k:frozenset(v) for k,v in buckets.items()}
            if len(buckets)==1 and next(iter(buckets.values()))==belief:
                continue
            branches={};costs=[]
            for response,new_belief in sorted(buckets.items()):
                sub=solve(new_belief)
                if sub is None:break
                costs.append(sub[0]);branches[response]=sub[1]
            else:
                cost=a.cost+max(costs)
                candidate=(cost,a.name,{"action":a.name,"branches":branches})
                if winner is None or candidate[:2]<winner[:2]:
                    winner=candidate
        visiting.remove(belief)
        cache[belief]=None if winner is None else (winner[0],winner[2])
        return cache[belief]
    result=solve(start)
    return {"verdict":"POLICY_FOUND" if result else "NO_CERTIFIED_SAFE_POLICY",
            "worst_cost":str(result[0]) if result else None,
            "policy":result[1] if result else None,
            "warrant_integrity":"TOY_STATE_ASSERTION_NOT_EXTERNAL_ATTESTATION"}

def test():
    belief=frozenset((State("W0",False),State("W1",True)))
    p=(Action("PREPARE",F(1)),Action("READ",F(1)),
       Action("DAMAGING_READ",F(1,8)),Action("UNVERIFIED_READ",F(1,16),False))
    assert all(len({apply(s,a)[0] for s in belief})==1 for a in p if safe(belief,a))
    a=exact_minimax(belief,p)
    assert a["worst_cost"]=="2" and a["policy"]["action"]=="PREPARE"
    assert exact_minimax(belief,p,full_identity=True)["verdict"]=="NO_CERTIFIED_SAFE_POLICY"
    assert exact_minimax(belief,(p[1],))["verdict"]=="NO_CERTIFIED_SAFE_POLICY"
    assert exact_minimax(belief,p[2:])["verdict"]=="NO_CERTIFIED_SAFE_POLICY"
    three=frozenset((State("A",False),State("B",True),State("C",True)))
    local=(Action("LOCAL_AB",F(1),True,frozenset(("A","B"))),
           Action("LOCAL_AC",F(1),True,frozenset(("A","C"))))
    for probe in local:
        pair=frozenset(s for s in three if s.world in probe.available_worlds)
        assert exact_minimax(pair,(probe,))["verdict"]=="POLICY_FOUND"
    assert exact_minimax(three,local)["verdict"]=="NO_CERTIFIED_SAFE_POLICY"
    return {"kind":"P73_P1_HISTORY_CONDITIONED_SAFE_OBSERVATION",
      "static_read_not_informative":"PASS",
      "warrant_preserving_prepare_then_read_cost":"2",
      "full_state_identity_only":"NO_POLICY",
      "local_pairwise_distinguishability_not_global_safe_policy":"PASS",
      "destructive_and_unattested_probes":"EXCLUDED",
      "external_passivity_certified":False,
      "novel_theorem":"NO",
      "real_independent_human_reviews":0,"paid_provider_calls":0}

if __name__=="__main__":
    z=test()
    print("P73_P1_HISTORY_SAFE_COURT_PASS prepare_then_read=2 no_global_policy_counterexample=PASS paid_calls=0")
    print(json.dumps(z,indent=2,sort_keys=True))
