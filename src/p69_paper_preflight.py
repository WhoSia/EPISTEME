"""P69 provider-free design audit. No SDK, network, API tokens or model calls."""
from __future__ import annotations

import itertools,json
from pathlib import Path
from p69_task_factory import TASKS, VERTICES as PACKET_VERTICES, FHL_CONTEXTS

OPS=("R","F","H","T","L")
MODELS=("gptoss120","gemini")
CHANNELS=("contract_a","contract_b")
SEMANTICS=("valid","null")

def vertices():
    out=[]
    for f,h,l in FHL_CONTEXTS:
        for r,t in itertools.product((0,1),repeat=2):
            v=frozenset(k for k,x in zip(OPS,(r,f,h,t,l)) if x)
            out.append(v)
    assert len(out)==len(set(out))==16
    assert set(out)=={frozenset(v) for v in PACKET_VERTICES}
    return tuple(out)

def operator_pairs(op):
    vv=set(vertices())
    return tuple(sorted(
        ((tuple(sorted(v)),tuple(sorted(v|{op})))
         for v in vv if op not in v and v|{op} in vv)
    ))

def full_ids():
    for m,t,v,s,c,d in itertools.product(MODELS,TASKS,vertices(),SEMANTICS,CHANNELS,range(1,9)):
        yield (m,t,tuple(sorted(v)),s,c,d)

def self_test():
    m=json.loads(Path("active/p69_paper_program.json").read_text())
    d=m["experiment"]
    assert d["tasks"]==len(TASKS)==8
    assert d["vertices"]==len(vertices())==16
    assert d["invocations_per_cell"]==8
    assert len(MODELS)==len(d["models"])==2
    assert len(CHANNELS)==d["response_policies"]==2
    assert len(SEMANTICS)==2
    for op in ("R","T"):
        edges=operator_pairs(op)
        assert len(edges)==8
        assert all(set(a).symmetric_difference(b)=={op} for a,b in edges)
    for idx in range(3):
        assert sum(x[idx] for x in FHL_CONTEXTS)==2
    assert all(sum(x)%2==0 for x in FHL_CONTEXTS)
    ids=set(full_ids())
    assert len(ids)==8192==d["maximum_calls"]
    assert d["pilot_max_calls"]==192
    assert m["commit_governance"]["github_actions_bot_commits"]=="ABSOLUTELY_FORBIDDEN"
    # Audit the prospective design without erasing the historical hosted canary.
    # Provider-free describes THIS script, not the entire P69 experimental history.
    state=m["state"]
    assert state.startswith("OPEN /")
    assert "CONTRACT_TECHNICAL_HOLD" in state
    assert "GENERATECONTENT_RETEST_PENDING" in state
    assert "PAPER_CONSTRUCT_HOLD" in state
    print("P69_PROVIDER_FREE_DESIGN_PASS")
    print("full_unique_calls=8192 pilot_ceiling=192")
    print("R_paired_edges=8 T_paired_edges=8 FHL_contexts=4")
    print("provider_calls=0 bot_commit_permission=0")
if __name__=="__main__":self_test()
