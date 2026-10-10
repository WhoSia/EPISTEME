"""P72 P0 — exact-rational audit × notification identification court.

Informational acquisition A and public AUDIT ANNOUNCEMENT N are independently
assignable. N=1,A=0 announces intent, NOT disclosure of unavailable results.
Claims of observational/causal identification require real randomized evidence,
positivity, consistency, cluster independence and no interference.
No provider calls, new participant data, or empirical human adjudication.
"""
from __future__ import annotations
from fractions import Fraction as F
from dataclasses import dataclass
from itertools import product
import json

CELLS=("A0N0","A1N0","A0N1","A1N1")
CONTRASTS={
 "acquisition_silent":(-1,1,0,0),
 "announcement_without_acquisition":(-1,0,1,0),
 "announcement_after_acquisition":(0,-1,0,1),
 "joint_vs_neither":(-1,0,0,1),
 "factorial_interaction":(1,-1,-1,1),
}

def rref(rows):
    """Reduced row-echelon form over rationals, not floats."""
    if not rows:return [],[]
    m=[list(map(F,row)) for row in rows]
    k=len(m[0])
    if any(len(row)!=k for row in m):raise ValueError("P72_RAGGED_OBSERVATION_MATRIX")
    pivots=[]
    for col in range(k):
        avail=next((i for i in range(len(pivots),len(m)) if m[i][col]!=0),None)
        if avail is None:continue
        dest=len(pivots);m[dest],m[avail]=m[avail],m[dest]
        div=m[dest][col];m[dest]=[v/div for v in m[dest]]
        for i in range(len(m)):
            if i!=dest:
                factor=m[i][col]
                if factor:m[i]=[x-factor*y for x,y in zip(m[i],m[dest])]
        pivots.append(col)
        if len(pivots)==len(m):break
    return [row for row in m if any(v for v in row)],pivots

def rank(rows):return len(rref(rows)[0])

def identified(matrix,contrast):
    """Linear contrast of four cell means identified iff in row span(M)."""
    if len(contrast)!=4 or any(len(row)!=4 for row in matrix):
        raise ValueError("P72_EXPECT_EXACT_FOUR_POTENTIAL_MEANS")
    return rank(matrix)==rank(matrix+[contrast])

def coordinate_design(observed):
    if len(set(observed))!=len(observed) or any(x not in CELLS for x in observed):
        raise ValueError("P72_BAD_CELL_SUPPORT")
    return [tuple(int(j==CELLS.index(c)) for j in range(4)) for c in observed]

def audit_court(observed):
    matrix=coordinate_design(observed)
    decisions={name:identified(matrix,list(coefs)) for name,coefs in CONTRASTS.items()}
    return {"kind":"P72_FACTORIAL_AUDIT_IDENTIFIABILITY_COURT",
       "observed_cells":list(observed),"observed_cell_count":len(observed),
       "full_factorial_observed":len(observed)==4,
       "contrast_identified_by_design":decisions,
       "interpretation":"LINEAR_IDENTIFICATION_ONLY_ASSUMING_ACTUAL_MEASURED_CELL_MEANS",
       "causal_authority":"NONE_WITHOUT_RANDOMIZATION_EXCHANGEABILITY_SUPPORT_AND_NO_INTERFERENCE",
       "external_independent_human_packet_reviews":0,"provider_calls":0}

def partial_interaction_bounds_three_zero_cells():
    """All available means zero, missing A1N1 in [-1,1]; sharp interaction bounds."""
    observed=("A0N0","A1N0","A0N1")
    assert not audit_court(observed)["contrast_identified_by_design"]["factorial_interaction"]
    values=[]
    for missing in (F(-1),F(1)):
        cell=(F(0),F(0),F(0),missing)
        observed_y=tuple(cell[CELLS.index(c)] for c in observed)
        interaction=sum(F(w)*v for w,v in zip(CONTRASTS["factorial_interaction"],cell))
        values.append((observed_y,interaction))
    assert values[0][0]==values[1][0] and values[0][1]!=values[1][1]
    return {"observed_values":list(map(str,values[0][0])),
       "unseen_worlds_interaction":[str(v[1]) for v in values],
       "sharp_bounds_given_cell_means_bounded_-1_to_1":["-1","1"],
       "proof":"two admissible completions, same observed means, opposite interaction"}

@dataclass(frozen=True)
class InstitutionalState:
    counterevidence_available:bool=True
    evidence_snapshot_captured:bool=False
    auditor_informed:bool=False
    public_announcement:bool=False

def acquire(state:InstitutionalState)->InstitutionalState:
    return InstitutionalState(
        counterevidence_available=state.counterevidence_available,
        evidence_snapshot_captured=state.evidence_snapshot_captured or state.counterevidence_available,
        auditor_informed=True,public_announcement=state.public_announcement)

def announce(state:InstitutionalState)->InstitutionalState:
    # Synthetic institutional response: after review, publicity closes a route.
    # This is a mathematical adversary, NOT measured real institutional conduct.
    return InstitutionalState(
        counterevidence_available=state.counterevidence_available and not state.auditor_informed,
        evidence_snapshot_captured=state.evidence_snapshot_captured,
        auditor_informed=state.auditor_informed,public_announcement=True)

def sequence_court():
    origin=InstitutionalState()
    acquire_then_announce=announce(acquire(origin))
    announce_then_acquire=acquire(announce(origin))
    assert acquire_then_announce!=announce_then_acquire
    assert acquire_then_announce.counterevidence_available is False
    assert announce_then_acquire.counterevidence_available is True
    return {"same_action_multiset":True,"different_final_state":True,
       "route_available_acquire_then_announce":False,
       "route_available_announce_then_acquire":True,
       "structural_authority":"SYNTHETIC_SEQUENCE_COUNTEREXAMPLE_NOT_FIELD_EVIDENCE"}

def self_test():
    assert rank([[1,0,0,0],[0,1,0,0],[0,0,1,0]])==3
    assert rank([[1,0,0,0],[1,0,0,0]])==1
    full=audit_court(CELLS)
    assert all(full["contrast_identified_by_design"].values())
    three=audit_court(CELLS[:3])
    assert not three["contrast_identified_by_design"]["factorial_interaction"]
    assert three["contrast_identified_by_design"]["acquisition_silent"]
    assert three["contrast_identified_by_design"]["announcement_without_acquisition"]
    assert not three["contrast_identified_by_design"]["joint_vs_neither"]
    two=audit_court(("A0N0","A1N0"))
    assert two["contrast_identified_by_design"]["acquisition_silent"]
    assert not two["contrast_identified_by_design"]["announcement_without_acquisition"]
    assert not audit_court(())["contrast_identified_by_design"]["factorial_interaction"]
    sharp=partial_interaction_bounds_three_zero_cells()
    assert sharp["unseen_worlds_interaction"]==["-1","1"]
    seq=sequence_court()
    assert seq["different_final_state"]
    for bad in (("A0N0","A0N0"),("FAKE_CELL",)):
        try:audit_court(bad)
        except ValueError:pass
        else:raise AssertionError("P72_INVALID_DESIGN_PROMOTED")
    return {"kind":"P72_P0_FORMAL_COUNTEREXAMPLE_COURT",
       "four_cell_linear_completeness":"PASS",
       "three_cell_interaction_unidentified":"PASS",
       "two_world_sharp_counterexample":"PASS",
       "state_transition_noncommutation":"PASS",
       "human_review_count":0,"paid_provider_calls":0,
       "paper_claim_authority":"EXISTING_LINEAR_IDENTIFICATION_AND_SYNTHETIC_COUNTERMODELS_ONLY"}

if __name__=="__main__":
    report=self_test()
    print("P72_P0_FACTORIAL_IDENTIFICATION_SELFTEST_PASS synthetic_worlds=2 human_reviews=0 provider_calls=0")
    print(json.dumps(report,sort_keys=True))
