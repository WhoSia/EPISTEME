"""Constructed finite source-ability hypergraph: full/singleton summaries not sufficient.
These are combinatorial examples, not source-grounded HDF observations.
"""
from itertools import combinations
import json
R=("archive","reader","instrument","calibration")
P={
 "same_channel":(frozenset(("archive","reader")),frozenset(("instrument","calibration"))),
 "cross_channel":(frozenset(("archive","instrument")),frozenset(("reader","calibration")))}
def possible(paths,lost):
    available=set(R)-set(lost)
    return any(p<=available for p in paths)
def minimal_cuts(paths):
    cuts=[]
    for n in range(1,len(R)+1):
        for t in combinations(R,n):
            s=frozenset(t)
            if not possible(paths,s) and not any(c<=s for c in cuts):cuts.append(s)
    return sorted(tuple(sorted(s)) for s in cuts)
assert all(possible(p,()) for p in P.values())
assert all(possible(p,(r,)) for r in R for p in P.values())
different={}
for pair in combinations(R,2):
    v={name:possible(paths,pair) for name,paths in P.items()}
    if len(set(v.values()))==2:different["+".join(pair)]=v
assert len(different)==4, different
assert minimal_cuts(P["same_channel"])!=minimal_cuts(P["cross_channel"])
print(json.dumps({"court":"P76_P5_CONSTRUCTED_NONCANONICAL_DIAGNOSTIC",
 "single_resource_loss_observations_identical":True,
 "distinct_double_failure_responses":different,
 "source_relative_real_migration_evidence_count":0,
 "five_stage_unique_minimality_proved":False,
 "new_theorem_claimed":False,
 "min_cut_sets":{k:minimal_cuts(p) for k,p in P.items()}},indent=2))
