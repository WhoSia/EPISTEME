"""EPISTEME P72-P1 — Typed Warrant Survival, Observation Fibres and Nonstationary Proofs.

Finite mathematical countermodels only. Existing forward-simulation/identifiability
principles are rivals; this does not prove a new universal theorem or inspect
real institutional behavior. No human judgements or provider requests.
"""
from __future__ import annotations
from dataclasses import dataclass,replace
from itertools import product
from typing import FrozenSet
import json

@dataclass(frozen=True)
class Rule:
    premises: tuple[str,...]
    conclusion: str

@dataclass(frozen=True)
class WarrantWorld:
    """'visible' are references shown to observers; 'admissible' are usable facts."""
    visible: FrozenSet[str]
    admissible: FrozenSet[str]
    rules: tuple[Rule,...]
    goal: str="MIGRATE"
    time: int=0
    hidden_revocation: bool=False

def proves(w:WarrantWorld)->bool:
    """Finite Horn closure; source visibility does not imply evidentiary validity."""
    found=set(w.admissible)
    for _ in range(len(w.rules)+1):
        before=len(found)
        for r in w.rules:
            if all(x in found for x in r.premises):found.add(r.conclusion)
        if len(found)==before:break
    return w.goal in found

def observe(w:WarrantWorld)->tuple:
    # The observer sees citation handles, public time and announcement state,
    # not hidden admissibility, rule validity, or revocation.
    return (tuple(sorted(w.visible)),w.time)

def step(w:WarrantWorld,action:str)->WarrantWorld:
    if action=="TICK":
        return replace(w,time=w.time+1)
    if action=="AUDIT":
        # Audit detects a hidden revocation only in revoked worlds, and removes
        # the admissibility of the weak warrant while retaining its citation.
        new=w.admissible-{"evidence"} if w.hidden_revocation else w.admissible
        return replace(w,admissible=frozenset(new))
    if action=="ANNOUNCE":
        return replace(w,time=w.time+1)
    raise ValueError("P72_UNKNOWN_ACTION")

def fibre_court(worlds:tuple[WarrantWorld,...],history:tuple[str,...]):
    states=[]
    for w in worlds:
        for action in history:w=step(w,action)
        states.append(w)
    # Equal observations, disagreeing proof validity: nonidentifiable.
    fibres={}
    for s in states:fibres.setdefault(observe(s),set()).add(proves(s))
    is_id=all(len(x)==1 for x in fibres.values())
    return {"identified":is_id,"observable_classes":len(fibres),
            "conflicting_observable_classes":sum(len(x)>1 for x in fibres.values()),
            "proof_values":[proves(s) for s in states]}

def forward_simulation(old:WarrantWorld,new:WarrantWorld,mapping:dict[str,str])->bool:
    """Strong, sufficient (NOT necessary) one-step proof-transport certificate."""
    terms=set(old.admissible)
    for r in old.rules:terms.update(r.premises);terms.add(r.conclusion)
    terms.add(old.goal)
    if not terms.issubset(mapping):return False
    if mapping[old.goal]!=new.goal:return False
    if not all(mapping[t] in new.admissible for t in old.admissible):return False
    represented={(r.premises,r.conclusion) for r in new.rules}
    for r in old.rules:
        pair=(tuple(mapping[t] for t in r.premises),mapping[r.conclusion])
        if pair not in represented:return False
    return True

def strong_certificate_test():
    old=WarrantWorld(frozenset({"citation"}),frozenset({"evidence"}),
       (Rule(("evidence",),"MIGRATE"),))
    new=WarrantWorld(frozenset({"citation_renamed"}),frozenset({"evidence_prime"}),
       (Rule(("evidence_prime",),"MIGRATE"),))
    phi={"evidence":"evidence_prime","MIGRATE":"MIGRATE"}
    assert proves(old) and proves(new)
    assert forward_simulation(old,new,phi)
    # Equal citation identities cannot certify proof after the evidence is
    # rendered inadmissible by audit or expiry.
    broken=replace(new,admissible=frozenset())
    assert not forward_simulation(old,broken,phi)
    assert not proves(broken)
    # Logical survival may hold through a different proof; copying the old
    # inference rule is NOT necessary. Prevent a false biconditional theorem.
    alternative=replace(new,admissible=frozenset({"MIGRATE"}),
                        rules=())
    assert proves(alternative)
    assert not forward_simulation(old,alternative,phi)
    return {"forward_simulation_sufficient":True,
            "forward_simulation_not_necessary":True,
            "citation_only_is_insufficient":True}

def observational_counterworld():
    base=WarrantWorld(frozenset({"citation"}),frozenset({"evidence"}),
          (Rule(("evidence",),"MIGRATE"),))
    worlds=(base,replace(base,hidden_revocation=True))
    baseline=fibre_court(worlds,())
    assert baseline["identified"] and baseline["proof_values"]==[True,True]
    after=fibre_court(worlds,("AUDIT",))
    assert not after["identified"] and after["proof_values"]==[True,False]
    assert after["conflicting_observable_classes"]==1
    # Even after a TICK or public ANNOUNCE, purely visible citation/time
    # snapshots cannot distinguish the two admissibility states.
    for suffix in (("TICK",),("ANNOUNCE",),("ANNOUNCE","TICK")):
        assert not fibre_court(worlds,("AUDIT",)+suffix)["identified"]
    return {"worlds":2,"same_observed_post_audit_reference":True,
            "different_hidden_proof_admissibility":True,
            "post_audit_warrant_identification":"FAIL"}

def separating_probe(worlds:tuple[WarrantWorld,...],reveals_revocation:bool):
    """A truly independent, passive probe is only a hypothetical capability."""
    inspected=[]
    for w in worlds:
        s=step(w,"AUDIT")
        output=(observe(s), w.hidden_revocation if reveals_revocation else None)
        inspected.append((output,proves(s)))
    fibres={}
    for observation,value in inspected:fibres.setdefault(observation,set()).add(value)
    return all(len(values)==1 for values in fibres.values())

def self_test():
    strong=strong_certificate_test()
    nonid=observational_counterworld()
    base=WarrantWorld(frozenset({"citation"}),frozenset({"evidence"}),
                      (Rule(("evidence",),"MIGRATE"),))
    worlds=(base,replace(base,hidden_revocation=True))
    assert not separating_probe(worlds,False)
    assert separating_probe(worlds,True)
    # Positivity of the probe in actual field data remains unverified.
    assert not fibre_court(worlds,("AUDIT",))["identified"]
    for action in ("BAD",):
        try:step(base,action)
        except ValueError:pass
        else:raise AssertionError("P72_UNKNOWN_ACTION_ACCEPTED")
    return {"kind":"P72_P1_TYPED_WARRANT_FIBRE_COURT",
       "sufficient_not_necessary_proof_mapping":strong,
       "observation_fibre_nonidentification":nonid,
       "independent_passive_probe_can_separate_toy_worlds":True,
       "actual_probe_observability":"NOT_ESTABLISHED",
       "comparison_class":"FORWARD_SIMULATION_PLUS_FIBRE_IDENTIFIABILITY",
       "novel_theorem_authority":"NONE",
       "real_human_packet_reviews":0,"new_provider_calls":0}

if __name__=="__main__":
    z=self_test()
    print("P72_P1_WARRANT_FIBRE_COURT_PASS worlds=2 strong_certificate_sufficient_only=true model_calls=0")
    print(json.dumps(z,indent=2))
