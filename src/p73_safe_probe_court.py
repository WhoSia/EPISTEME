"""EPISTEME-P73-P0: EXACT SAFE WARRANT-SEPARATING PROBE DECISION TREES.

Static deterministic finite worlds; probes are *assumed verified safe* if they
pass explicit finite transition and provenance checks on every enumerated world.
Checking in a toy world is NOT independent empirical certification of passivity.
The recurrence and pairwise-signature criterion are classical decision-tree
theory, not claimed new EPISTEME theorems.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from typing import Optional
import json

from p72_warrant_fibre_court import Rule, WarrantWorld, proves

@dataclass(frozen=True)
class Probe:
    name: str
    cost: F
    observations: tuple[str, ...]
    independent_source_attested: bool
    # None means explicitly unchanged; non-None is a state after applying
    # this synthetic probe, used to attack a falsely 'passive' probe.
    post_states: tuple[WarrantWorld, ...] | None = None

def source_fingerprint(w: WarrantWorld):
    return (w.visible, w.admissible, w.rules, w.goal, w.time, w.hidden_revocation)

def probe_is_model_safe(probe: Probe, worlds: tuple[WarrantWorld,...]) -> bool:
    if (type(probe.cost) is not F or probe.cost <= 0 or
        not probe.independent_source_attested or
        len(probe.observations) != len(worlds)):
        return False
    if probe.post_states is None:
        return True
    if len(probe.post_states) != len(worlds):
        return False
    return all(source_fingerprint(before) == source_fingerprint(after)
               for before, after in zip(worlds,probe.post_states))

def validate_model(worlds: tuple[WarrantWorld,...], probes: tuple[Probe,...]):
    if not worlds or len(worlds)>16:raise ValueError("P73_FINITE_WORLD_COUNT_1_TO_16")
    if len({p.name for p in probes})!=len(probes):
        raise ValueError("P73_DUPLICATE_PROBE")
    for p in probes:
        if len(p.observations)!=len(worlds):
            raise ValueError("P73_WRONG_PROBE_WORLD_ALIGNMENT")
    return tuple(p for p in probes if probe_is_model_safe(p,worlds))

def goal_labels(worlds: tuple[WarrantWorld,...]):
    return tuple(proves(w) for w in worlds)

def same_goal(mask:int, goals:tuple[bool,...])->bool:
    x={goals[i] for i in range(len(goals)) if (mask>>i)&1}
    return len(x)<2

def split(mask:int, observations:tuple[str,...]):
    partitions={}
    for i,signal in enumerate(observations):
        if (mask>>i)&1:partitions[signal]=partitions.get(signal,0)|(1<<i)
    return tuple(sorted(partitions.items()))

def pairwise_separation(worlds:tuple[WarrantWorld,...], probes:tuple[Probe,...]):
    """Safe static policy exists iff every opposite-goal pair has a safe
    probe with unequal responses. Global signature partition criterion.
    """
    safe=validate_model(worlds,probes)
    ys=goal_labels(worlds)
    failures=[]
    for i in range(len(worlds)):
        for j in range(i+1,len(worlds)):
            if ys[i]!=ys[j] and not any(p.observations[i]!=p.observations[j]
                                        for p in safe):
                failures.append((i,j))
    return {"exists":not failures,
            "unseparated_opposing_pairs":failures,
            "safe_probe_names":tuple(p.name for p in safe),
            "excluded_probe_names":tuple(p.name for p in probes if p not in safe)}

def adaptive_minimax(worlds:tuple[WarrantWorld,...], probes:tuple[Probe,...]):
    safe=validate_model(worlds,probes)
    labels=goal_labels(worlds)
    full=(1<<len(worlds))-1
    @lru_cache(None)
    def opt(mask:int):
        if same_goal(mask,labels):
            decision="SWITCH_WARRANT_PRESENT" if any(
                labels[i] for i in range(len(labels)) if (mask>>i)&1
            ) else "WARRANT_ABSENT"
            return (F(0),{"decision":decision,"size":mask.bit_count()})
        best=None
        for probe in safe:
            groups=split(mask,probe.observations)
            if len(groups)<2:continue  # no progress; positive costs
            downstream=[opt(subset) for _,subset in groups]
            if any(item is None for item in downstream):continue
            candidate=probe.cost+max(item[0] for item in downstream)
            tree={"probe":probe.name,"cost":str(probe.cost),
                  "branches":{signal:item[1] for (signal,_),item in zip(groups,downstream)}}
            key=(candidate,probe.name)
            if best is None or key<best[0]:best=(key,tree)
        return None if best is None else (best[0][0],best[1])
    z=opt(full)
    return {"possible":z is not None,"worst_case_cost":str(z[0]) if z else None,
            "policy":z[1] if z else None,"model_safe_probe_count":len(safe)}

def fixed_nonadaptive_minimax(worlds:tuple[WarrantWorld,...],probes:tuple[Probe,...]):
    safe=validate_model(worlds,probes)
    label=goal_labels(worlds)
    best=None
    for size in range(len(safe)+1):
        for subset in combinations(safe,size):
            signatures=[tuple(p.observations[i] for p in subset)
                        for i in range(len(worlds))]
            identified=all(label[i]==label[j] or signatures[i]!=signatures[j]
                           for i in range(len(worlds))
                           for j in range(i+1,len(worlds)))
            if not identified:continue
            cost=sum((p.cost for p in subset),F(0))
            trial=(cost,tuple(p.name for p in subset))
            if best is None or trial<best:best=trial
    return {"possible":best is not None,
            "cost":str(best[0]) if best else None,
            "probes":list(best[1]) if best else []}

def example():
    # All four abstract source worlds publicly display the same citation;
    # evidence admissibility, not the name of that citation, sets the goal.
    rule=(Rule(("admissible_evidence",),"MIGRATE"),)
    w=tuple(WarrantWorld(frozenset({"PUBLIC_CITATION"}),
              frozenset({"admissible_evidence"}) if y else frozenset(),
              rule,time=1)
              for y in (False,True,False,True))
    A=Probe("A_route",F(1),("L","L","R","R"),True)
    B=Probe("B_left",F(2),("0","1","x","x"),True)
    C=Probe("C_right",F(2),("x","x","0","1"),True)
    # Extremely cheap 'detect revocation' option precisely separates goal,
    # but destroys admissible evidence in all cases: MUST be excluded.
    destructive=Probe("D_destroying_probe",F(1,4),("0","1","0","1"),
       True,tuple(WarrantWorld(x.visible,frozenset(),x.rules,x.goal,x.time,
                                x.hidden_revocation) for x in w))
    # A hypothetical auditor with no independent source custody attestation
    # is also excluded, even if it reveals goal and has zero side effects.
    unattested=Probe("E_unverified_source",F(1,8),("0","1","0","1"),False)
    return w,(A,B,C,destructive,unattested)

def adversarial_tests():
    worlds,probes=example()
    check=pairwise_separation(worlds,probes)
    assert check["exists"] and len(check["safe_probe_names"])==3
    assert "D_destroying_probe" in check["excluded_probe_names"]
    assert "E_unverified_source" in check["excluded_probe_names"]
    ad=adaptive_minimax(worlds,probes)
    fixed=fixed_nonadaptive_minimax(worlds,probes)
    assert ad["possible"] and ad["worst_case_cost"]=="3"
    assert fixed["possible"] and fixed["cost"]=="4"
    assert ad["policy"]["probe"]=="A_route"
    # Proof of no safe policy under incomplete probe availability: R-branch
    # has two opposite warrant states with the same remaining signatures.
    q=(probes[0],probes[1],probes[3],probes[4])
    impossible=pairwise_separation(worlds,q)
    assert not impossible["exists"] and (2,3) in impossible["unseparated_opposing_pairs"]
    assert not adaptive_minimax(worlds,q)["possible"]
    assert not fixed_nonadaptive_minimax(worlds,q)["possible"]
    # All observation signatures coincide on visible citation/time, yet
    # proof validity varies. Raw citation cannot be used as certificate.
    assert len({tuple(sorted(x.visible))+(str(x.time),) for x in worlds})==1
    assert len(set(goal_labels(worlds)))==2
    # No shortcut from unsafe perfect probe even if it's cheap.
    assert not adaptive_minimax(worlds,(probes[3],probes[4]))["possible"]
    # The terminal claim is specific to the binary proof predicate, NOT to
    # fully distinguishing every hidden source world.
    return {
       "kind":"P73_P0_STATIC_SAFE_SEPARATION_COURT",
       "safe_signature_iff_countertest":"PASS",
       "adaptive_minimax_cost":ad["worst_case_cost"],
       "nonadaptive_cost":fixed["cost"],
       "adaptive_vs_nonadaptive_strict_gap":"PASS",
       "unsafe_information_rich_probe_excluded":"PASS",
       "source_unattested_probe_excluded":"PASS",
       "opposite_warrant_indistinguishable_when_C_missing":"PASS",
       "independent_real_world_probe_safety":"NOT_VERIFIED",
       "relation_to_classical_decision_trees":"ESTABLISHED_METHOD",
       "new_theorem_authority":"NONE",
       "actual_human_review_count":0,
       "new_paid_model_calls":0
    }

if __name__=="__main__":
    report=adversarial_tests()
    print("P73_P0_SAFE_SEPARATION_SELFTEST_PASS adaptive=3 fixed=4 missing_C=NO_SAFE_POLICY provider_calls=0")
    print(json.dumps(report,indent=2,sort_keys=True))
