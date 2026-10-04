from __future__ import annotations

import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import p53_cross_task as p53

STAGE = "EPISTEME-P56"
TASKS = p53.TASKS
TEST_ORDER = tuple(
    [f"historical:{t}" for t in TASKS] +
    [f"loo:{t}" for t in TASKS]
)

def load_source(path: Path):
    d=json.loads(path.read_text(encoding="utf-8"))
    if d.get("stage")!="EPISTEME-P55":
        raise RuntimeError("source is not P55")
    est=d["estimand_identifiability"]["by_model_task"]["gemini"]
    unresolved=[]
    fixed={t:{} for t in TASKS}
    for task in TASKS:
        vs=est[task]["vertices"]
        if len(vs)!=32: raise RuntimeError("unexpected vertex count")
        for vi,v in enumerate(vs):
            poss=tuple(int(x) for x in v["possible_taus"])
            if len(poss)==1:
                fixed[task][vi]=poss[0]
            elif len(poss)==2:
                unresolved.append({
                    "task":task,
                    "vertex":v["vertex"],
                    "vertex_index":vi,
                    "possible":poss
                })
            else:
                raise RuntimeError(f"non-binary unresolved tau: {task} {v['vertex']} {poss}")
    if sum(len(x) for x in fixed.values())!=90 or len(unresolved)!=6:
        raise RuntimeError("P55 90/96 identifiability contract violated")
    worlds=1
    for u in unresolved: worlds*=len(u["possible"])
    if worlds!=64: raise RuntimeError(f"expected 64 worlds, got {worlds}")
    return d,fixed,unresolved

def branch_for(tau):
    base=json.loads(Path("active/p51_sufficiency_baseline.json").read_text(encoding="utf-8"))
    hist=np.asarray(base["mean_tau"]["gemini"]["0.5"],float)
    tests=p53.primary_tests(tau,hist)
    holm=p53.holm(tests)
    historical_pass=sum(
        bool(holm["rejected"][f"historical:{t}"]) and
        tests[f"historical:{t}"]["statistic"] is not None and
        tests[f"historical:{t}"]["statistic"]>0
        for t in TASKS
    )
    loo_pass=sum(
        bool(holm["rejected"][f"loo:{t}"]) and
        tests[f"loo:{t}"]["statistic"] is not None and
        tests[f"loo:{t}"]["statistic"]>0
        for t in TASKS
    )
    all6=all(
        tests[k]["statistic"] is not None and
        tests[k]["statistic"]>0 and
        bool(holm["rejected"][k])
        for k in TEST_ORDER
    )
    factor=p53.factorization(np.stack([tau[t] for t in TASKS]))
    if all6:
        branch="CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_PRIMARY_ONLY"
    elif loo_pass==3 and historical_pass<3:
        branch="FRESH_TASK_COMMON_COMPONENT_PRIMARY_ONLY"
    elif historical_pass>=1 and loo_pass>=1:
        branch="PARTIAL_TASK_TRANSPORT_PRIMARY_ONLY"
    elif factor["share_interaction"]>factor["share_representation"]:
        branch="TASK_INTERACTION_DOMINATES_PRIMARY_ONLY"
    else:
        branch="NO_CROSS_TASK_MEASUREMENT_LAW_PRIMARY_ONLY"
    rejection=tuple(bool(holm["rejected"][k]) for k in TEST_ORDER)
    return {
        "tests":tests,
        "holm":holm,
        "historical_pass_count":int(historical_pass),
        "loo_pass_count":int(loo_pass),
        "factorization":factor,
        "branch":branch,
        "rejection_vector":rejection
    }

def enumerate_worlds(fixed,unresolved):
    records=[]
    for bits in itertools.product((0,1),repeat=len(unresolved)):
        tau={t:np.empty(32,float) for t in TASKS}
        for t in TASKS:
            for vi,val in fixed[t].items(): tau[t][vi]=val
        assignments=[]
        for bit,u in zip(bits,unresolved):
            val=u["possible"][bit]
            tau[u["task"]][u["vertex_index"]]=val
            assignments.append({
                "task":u["task"],"vertex":u["vertex"],
                "value":int(val),"bit":int(bit)
            })
        a=branch_for(tau)
        records.append({
            "world_id":"".join(map(str,bits)),
            "bits":list(bits),
            "assignments":assignments,
            "branch":a["branch"],
            "rejection_vector":list(a["rejection_vector"]),
            "historical_pass_count":a["historical_pass_count"],
            "loo_pass_count":a["loo_pass_count"],
            "tests":a["tests"],
            "holm":a["holm"],
            "factorization":a["factorization"]
        })
    if len(records)!=64: raise RuntimeError("world count")
    return records

def range_summary(worlds):
    test_ranges={}
    for k in TEST_ORDER:
        stats=[w["tests"][k]["statistic"] for w in worlds if w["tests"][k]["statistic"] is not None]
        raw=[w["tests"][k]["p"] for w in worlds if w["tests"][k]["p"] is not None]
        adj=[w["holm"]["adjusted_p"][k] for w in worlds if w["holm"]["adjusted_p"][k] is not None]
        rej={bool(w["holm"]["rejected"][k]) for w in worlds}
        test_ranges[k]={
            "statistic_min":min(stats) if stats else None,
            "statistic_max":max(stats) if stats else None,
            "raw_p_min":min(raw) if raw else None,
            "raw_p_max":max(raw) if raw else None,
            "holm_p_min":min(adj) if adj else None,
            "holm_p_max":max(adj) if adj else None,
            "rejection_support":sorted(rej),
            "rejection_invariant":len(rej)==1
        }
    fs={}
    for key in ("share_task","share_representation","share_interaction"):
        vals=[w["factorization"][key] for w in worlds]
        fs[key]={"min":min(vals),"max":max(vals)}
    return test_ranges,fs

def coordinate_influence(worlds,unresolved):
    bybits={tuple(w["bits"]):w for w in worlds}
    out=[]
    for i,u in enumerate(unresolved):
        branch_flips=0;reject_flips=0
        low_branches=set();high_branches=set()
        low_rej=set();high_rej=set()
        for bits,w in bybits.items():
            (high_branches if bits[i] else low_branches).add(w["branch"])
            rv=tuple(w["rejection_vector"])
            (high_rej if bits[i] else low_rej).add(rv)
        for background in itertools.product((0,1),repeat=len(unresolved)-1):
            b0=list(background); b0.insert(i,0)
            b1=list(background); b1.insert(i,1)
            w0=bybits[tuple(b0)];w1=bybits[tuple(b1)]
            branch_flips+=w0["branch"]!=w1["branch"]
            reject_flips+=tuple(w0["rejection_vector"])!=tuple(w1["rejection_vector"])
        out.append({
            **u,
            "matched_background_pairs":32,
            "branch_flip_pairs":branch_flips,
            "rejection_vector_flip_pairs":reject_flips,
            "branch_influential":branch_flips>0,
            "holm_influential":reject_flips>0,
            "low_branch_support":sorted(low_branches),
            "high_branch_support":sorted(high_branches)
        })
    return out

def verdict(worlds,test_ranges):
    branches=Counter(w["branch"] for w in worlds)
    rejection_vectors=Counter(tuple(w["rejection_vector"]) for w in worlds)
    branch_identified=len(branches)==1
    holm_invariant=len(rejection_vectors)==1
    only=next(iter(branches)) if branch_identified else None
    if branch_identified and only=="CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_PRIMARY_ONLY":
        v="MISSINGNESS_ASSUMPTION_FREE_PRIMARY_LAW_IDENTIFIED"
    elif branch_identified and only in {
        "NO_CROSS_TASK_MEASUREMENT_LAW_PRIMARY_ONLY",
        "TASK_INTERACTION_DOMINATES_PRIMARY_ONLY"
    }:
        v="MISSINGNESS_ASSUMPTION_FREE_PRIMARY_NULL_IDENTIFIED"
    elif holm_invariant:
        v="HOLM_INVARIANT_BUT_BRANCH_FACTOR_AMBIGUOUS"
    else:
        v="COMPLETION_SENSITIVE_PRIMARY_BRANCH_REMAINS_PARTIALLY_IDENTIFIED"
    return v,branches,rejection_vectors,branch_identified,holm_invariant

def main():
    src=Path(sys.argv[1] if len(sys.argv)>1 else "receipts/p55_source/p55_result.json")
    _source,fixed,unresolved=load_source(src)
    worlds=enumerate_worlds(fixed,unresolved)
    tr,fr=range_summary(worlds)
    influence=coordinate_influence(worlds,unresolved)
    v,branches,rvecs,bid,hinv=verdict(worlds,tr)
    out={
      "stage":STAGE,
      "provider_calls":0,
      "scientific_cell_replays":0,
      "source":{"p55_run":37006966589,"admissible_worlds":64},
      "unresolved_tau":[
          {"task":u["task"],"vertex":u["vertex"],"possible":list(u["possible"])}
          for u in unresolved
      ],
      "world_branch_counts":dict(branches),
      "rejection_vector_counts":{
          "".join("1" if x else "0" for x in k):n for k,n in rvecs.items()
      },
      "branch_identified":bid,
      "holm_rejection_vector_invariant":hinv,
      "test_ranges":tr,
      "factorization_share_ranges":fr,
      "coordinate_influence":influence,
      "worlds":worlds,
      "constitutional_verdict":v,
      "authority":"P56 exhaustively evaluates the unchanged P53 primary Gemini test family over every P55-admissible stopping-time completion. Worlds are unweighted; no missingness model, imputation, provider call, or scientific replay is used. Operational policy-transfer authority remains closed."
    }
    Path("receipts").mkdir(exist_ok=True)
    Path("receipts/p56_result.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({
      "verdict":v,
      "branch_counts":dict(branches),
      "holm_invariant":hinv,
      "branch_identified":bid,
      "influential_coordinates":[x["vertex"] for x in influence if x["branch_influential"] or x["holm_influential"]]
    },indent=2))

if __name__=="__main__":
    if "--self-test" in sys.argv:
        assert len(TEST_ORDER)==6
        fake=[{"bits":[0]*6,"branch":"A","rejection_vector":[True]*6,"factorization":{"share_task":.2,"share_representation":.3,"share_interaction":.5},
               "tests":{k:{"statistic":1.0,"p":.01} for k in TEST_ORDER},
               "holm":{"adjusted_p":{k:.02 for k in TEST_ORDER},"rejected":{k:True for k in TEST_ORDER}}}]
        tr,fr=range_summary(fake)
        assert all(tr[k]["rejection_invariant"] for k in TEST_ORDER)
        print("P56_PRECHECK_PASS")
    else:
        main()
