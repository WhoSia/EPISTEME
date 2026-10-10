"""P73-P2: finite winning-belief fixed-point for modeled safe observations.

This is a classical partial-observation reachability/predecessor calculation.
It checks admissibility across each entire belief, NOT merely pairwise worlds.
No actual human observations or independently validated audit passivity.
"""
from __future__ import annotations
from collections import deque
import json
from fractions import Fraction as F
from p73_history_safe_court import Action,State,apply,safe,exact_minimax,test as p1test

def successor_beliefs(belief:frozenset[State],action:Action):
    groups={}
    for s in belief:
        response,next_s=apply(s,action)
        groups.setdefault(response,set()).add(next_s)
    return tuple(sorted(((o,frozenset(v)) for o,v in groups.items()),key=lambda x:x[0]))

def reach(start:frozenset[State],actions:tuple[Action,...]):
    discovered={start};queue=deque((start,))
    while queue:
        b=queue.popleft()
        for a in actions:
            if not safe(b,a):continue
            for _,nb in successor_beliefs(b,a):
                if nb not in discovered:
                    discovered.add(nb);queue.append(nb)
    return discovered

def winning_fixpoint(start:frozenset[State],actions:tuple[Action,...]):
    beliefs=reach(start,actions)
    rank={b:0 for b in beliefs if len({w.warranted for w in b})<=1}
    stages=[]
    while True:
        new={}
        for belief in beliefs:
            if belief in rank:continue
            for a in actions:
                if not safe(belief,a):continue
                outcomes=successor_beliefs(belief,a)
                if all(next_belief in rank for _,next_belief in outcomes):
                    bound=1+max(rank[next_belief] for _,next_belief in outcomes)
                    if belief not in new or bound<new[belief]:new[belief]=bound
        if not new:break
        rank.update(new);stages.append(len(new))
    return {
       "policy_exists":start in rank,
       "minimal_winning_horizon":rank.get(start),
       "reachable_belief_count":len(beliefs),
       "winning_belief_count":len(rank),
       "levels_added":stages
    }

def test():
    p1test()
    beliefs=frozenset((State("W0",False),State("W1",True)))
    actions=(Action("PREPARE",F(1)),Action("READ",F(1)),
       Action("DAMAGING_READ",F(1,8)),Action("UNVERIFIED_READ",F(1,16),False))
    result=winning_fixpoint(beliefs,actions)
    assert result["policy_exists"] and result["minimal_winning_horizon"]==2
    assert exact_minimax(beliefs,actions)["worst_cost"]=="2"
    b3=frozenset((State("A",False),State("B",True),State("C",True)))
    local=(Action("LOCAL_AB",F(1),True,frozenset(("A","B"))),
           Action("LOCAL_AC",F(1),True,frozenset(("A","C"))))
    failure=winning_fixpoint(b3,local)
    assert not failure["policy_exists"]
    assert not exact_minimax(b3,local)["verdict"]=="POLICY_FOUND"
    # A direct modeled read can make a policy if globally available and safe.
    setup=frozenset(State(s.world,s.warranted,s.proof_token,True) for s in b3)
    assert winning_fixpoint(setup,(Action("READ",F(1)),))["policy_exists"]
    return {"kind":"P73_P2_WINNING_BELIEF_FIXED_POINT_COURT",
            "prep_read_horizon":result["minimal_winning_horizon"],
            "globally_unavailable_pair_tests":"NO_POLICY",
            "predecessor_vs_exact_cost_dp":"AGREE_ON_FINITE_FIXTURES",
            "classical_antecedent":"PARTIAL_OBSERVATION_REACHABILITY",
            "novel_theorem":"NOT_CLAIMED",
            "real_independent_safety_certificates":0,
            "new_model_calls":0,"human_reviews":0}

if __name__=="__main__":
    x=test()
    print("P73_P2_WINNING_BELIEF_FIXPOINT_PASS horizon=2 local_pairwise_not_global=true calls=0")
    print(json.dumps(x,indent=2,sort_keys=True))
