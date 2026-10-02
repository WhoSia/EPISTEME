from __future__ import annotations
import json, os, random, sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from groq import Groq
from google import genai

import p53_cross_task as p53
from p42_reopen import CANARY, CANARY_PROMPT, parse, gemini_raw, groq_raw
from p44_field import CONTRACTS, MODELS
from p51_sufficiency import beta_mix_cs

STAGE="EPISTEME-P55"
TASKS=p53.TASKS
MODELS_P53=("gemini","gptoss120")
WIDTH=0.50
NPERM=5000
P54_RUN_ID=37004809384
EXPECTED_ROWS=12288
EXPECTED_REMAINING={"gemini":415,"gptoss120":1}

def row_key(r:dict[str,Any]):
    return (r["model"],r["task"],r["draw"],r["cell_index"],r["semantic"])

def classify_error(r):
    txt=" ".join(str(r.get(k) or "") for k in ("error","p54_replay_error")).lower()
    if "resource_exhausted" in txt or "quota" in txt or "429" in txt:return "RESOURCE_OR_QUOTA"
    if "503" in txt or "unavailable" in txt:return "UNAVAILABLE"
    if "json" in txt or "schema" in txt or "parse" in txt:return "SCHEMA_OR_PARSE"
    return "OTHER"

def validate_source(d):
    if d.get("stage")!="EPISTEME-P54":raise RuntimeError("not P54 source")
    rows=d.get("raw_rows")
    if not isinstance(rows,list) or len(rows)!=EXPECTED_ROWS:raise RuntimeError("P54 row count")
    for m,n in EXPECTED_REMAINING.items():
        rem=sum(r["model"]==m and r["status"]!="OK" for r in rows)
        if rem!=n:raise RuntimeError(f"{m} remaining={rem}")
    return rows

def joint_sequence(rows,model,task,vertex_index):
    by={}
    for r in rows:
        if r["model"]==model and r["task"]==task and r["vertex_index"]==vertex_index:
            by[(r["draw"],r["semantic"])]=r
    seq=[]
    detail=[]
    for draw in range(1,33):
        rv=by[(draw,"valid")];rn=by[(draw,"null")]
        observed=[]
        for r in (rv,rn):
            if r["status"]=="OK":observed.append(bool(r["primary_correct"]))
        if any(x is False for x in observed):
            j=0
        elif rv["status"]=="OK" and rn["status"]=="OK":
            j=int(bool(rv["primary_correct"]) and bool(rn["primary_correct"]))
        else:
            j=None
        seq.append(j)
        detail.append((draw,rv,rn,j))
    return seq,detail

def possible_taus(seq):
    # State=(successes_so_far, first_stop_or_0)
    states={(0,0)}
    for t,x in enumerate(seq,1):
        nxt=set()
        vals=(0,1) if x is None else (int(x),)
        for s,stop in states:
            for val in vals:
                ns=s+val;nstop=stop
                if nstop==0:
                    lo,hi=beta_mix_cs(ns,t,.05)
                    if hi-lo<=WIDTH:nstop=t
                nxt.add((ns,nstop))
        states=nxt
    return sorted({stop if stop else 33 for _,stop in states})

def missingness_geometry(rows):
    out={}
    for model in MODELS_P53:
        fs=[r for r in rows if r["model"]==model and r["status"]!="OK"]
        q=Counter()
        for r in fs:
            q[classify_error(r)]+=1
        by_task=Counter(r["task"] for r in fs)
        by_sem=Counter(r["semantic"] for r in fs)
        by_draw=Counter(r["draw"] for r in fs)
        by_vertex=Counter(r["vertex"] for r in fs)
        draws=[r["draw"] for r in fs]
        out[model]={
            "failures":len(fs),
            "error_class":dict(q),
            "by_task":dict(by_task),
            "by_semantic":dict(by_sem),
            "first_draw":min(draws) if draws else None,
            "last_draw":max(draws) if draws else None,
            "last_8_draw_fraction":sum(d>=25 for d in draws)/len(draws) if draws else 0,
            "last_16_draw_fraction":sum(d>=17 for d in draws)/len(draws) if draws else 0,
            "by_draw":{str(k):by_draw[k] for k in sorted(by_draw)},
            "top_vertices":by_vertex.most_common(10)
        }
    return out

def substitution_audit(rows):
    keyed=defaultdict(dict)
    for r in rows:
        if r["status"]=="OK":
            k=(r["task"],r["draw"],r["cell_index"],r["semantic"])
            keyed[k][r["model"]]=r
    overlap=disc=0
    for k,v in keyed.items():
        if all(m in v for m in MODELS_P53):
            overlap+=1
            disc+=bool(v["gemini"]["primary_correct"])!=bool(v["gptoss120"]["primary_correct"])
    # Joint outcome discordance
    joint_overlap=joint_disc=0
    for task in TASKS:
        for draw in range(1,33):
            for vi in range(32):
                vals={}
                for model in MODELS_P53:
                    seq,_=joint_sequence(rows,model,task,vi)
                    vals[model]=seq[draw-1]
                if vals["gemini"] is not None and vals["gptoss120"] is not None:
                    joint_overlap+=1;joint_disc+=vals["gemini"]!=vals["gptoss120"]
    return {
        "semantic_row_overlap":overlap,
        "semantic_row_disagreements":disc,
        "semantic_row_disagreement_rate":disc/overlap if overlap else None,
        "joint_overlap":joint_overlap,
        "joint_disagreements":joint_disc,
        "joint_disagreement_rate":joint_disc/joint_overlap if joint_overlap else None,
        "literal_substitution_equivalent":disc==0 and joint_disc==0
    }

def estimand_audit(rows):
    out={};critical=[]
    for model in MODELS_P53:
        tasks={}
        for task in TASKS:
            vertices=[]
            for vi in range(32):
                seq,detail=joint_sequence(rows,model,task,vi)
                taus=possible_taus(seq)
                exact=len(taus)==1
                vertices.append({"vertex":p53.VERTICES[vi],"possible_taus":taus,"identified":exact})
                if not exact:
                    latest=max(taus)
                    for draw,rv,rn,j in detail:
                        if j is None and draw<=min(latest,32):
                            for r in (rv,rn):
                                if r["status"]!="OK":
                                    critical.append({
                                        "model":model,"task":task,"draw":draw,
                                        "vertex":r["vertex"],"vertex_index":vi,
                                        "cell_index":r["cell_index"],"semantic":r["semantic"],
                                        "alias":r["alias"]
                                    })
            tasks[task]={
                "identified_vertices":sum(v["identified"] for v in vertices),
                "all_identified":all(v["identified"] for v in vertices),
                "vertices":vertices
            }
        out[model]=tasks
    # dedup conservative replay-bound rows
    seen=set();dedup=[]
    for r in critical:
        k=tuple(r[x] for x in ("model","task","draw","cell_index","semantic"))
        if k not in seen:seen.add(k);dedup.append(r)
    return out,dedup

def canary_probe():
    result={}
    # Gemini 3 calls
    g=[]
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    for seed in (5591,5592,5593):
        try:
            o=parse(gemini_raw(client,MODELS["gemini"]["model"],CANARY_PROMPT,seed))
            ok=o==CANARY;err=None
        except Exception as e:
            ok=False;err=type(e).__name__+":"+str(e)[:240]
        g.append({"seed":seed,"ok":ok,"error":err})
    result["gemini"]={"calls":g,"ok":sum(x["ok"] for x in g),"point_access":all(x["ok"] for x in g)}
    # GPT-OSS same frozen contract, 3 calls
    gg=[];clientg=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=4)
    contract=CONTRACTS["gptoss120"]
    for i in range(3):
        try:
            o=parse(groq_raw(clientg,MODELS["gptoss120"]["model"],CANARY_PROMPT,contract))
            ok=o==CANARY;err=None
        except Exception as e:
            ok=False;err=type(e).__name__+":"+str(e)[:240]
        gg.append({"replicate":i+1,"ok":ok,"error":err})
    result["gptoss120"]={"calls":gg,"ok":sum(x["ok"] for x in gg),"point_access":all(x["ok"] for x in gg)}
    return result

def frozen_primary_if_identified(rows,estimand):
    gem=estimand["gemini"]
    full=all(gem[t]["all_identified"] for t in TASKS)
    if not full:return {"eligible":False,"reason":"not all 96 Gemini stopping times identified"}
    tau={}
    for task in TASKS:
        tau[task]=np.asarray([v["possible_taus"][0] for v in gem[task]["vertices"]],float)
    base=json.loads(Path("active/p51_sufficiency_baseline.json").read_text())
    hist=np.asarray(base["mean_tau"]["gemini"]["0.5"],float)
    tests=p53.primary_tests(tau,hist);h=p53.holm(tests)
    hist_pass=sum(h["rejected"][f"historical:{t}"] and tests[f"historical:{t}"]["statistic"]>0 for t in TASKS)
    loo_pass=sum(h["rejected"][f"loo:{t}"] and tests[f"loo:{t}"]["statistic"]>0 for t in TASKS)
    factor=p53.factorization(np.stack([tau[t] for t in TASKS]))
    all6=all(tests[k]["statistic"] is not None and tests[k]["statistic"]>0 and h["rejected"][k] for k in tests)
    if all6:branch="CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_PRIMARY_ONLY"
    elif loo_pass==3 and hist_pass<3:branch="FRESH_TASK_COMMON_COMPONENT_PRIMARY_ONLY"
    elif hist_pass>=1 and loo_pass>=1:branch="PARTIAL_TASK_TRANSPORT_PRIMARY_ONLY"
    elif factor["share_interaction"]>factor["share_representation"]:branch="TASK_INTERACTION_DOMINATES_PRIMARY_ONLY"
    else:branch="NO_CROSS_TASK_MEASUREMENT_LAW_PRIMARY_ONLY"
    return {"eligible":True,"tests":tests,"holm":h,"historical_pass_count":hist_pass,"loo_pass_count":loo_pass,
            "factorization":factor,"frozen_primary_branch":branch}

def main():
    src=Path(sys.argv[1] if len(sys.argv)>1 else "receipts/p54_source/p54_result.json")
    d=json.loads(src.read_text());rows=validate_source(d)
    geom=missingness_geometry(rows)
    sub=substitution_audit(rows)
    estimand,critical=estimand_audit(rows)
    canary=canary_probe()
    primary=frozen_primary_if_identified(rows,estimand)
    gem_ident=sum(estimand["gemini"][t]["identified_vertices"] for t in TASKS)
    if primary["eligible"]:
        verdict="FROZEN_PRIMARY_MEASUREMENT_LAW_REOPENED_BY_ESTIMAND_COMPLETENESS" if "LAW" in primary["frozen_primary_branch"] else "FROZEN_PRIMARY_REOPENED_AND_NULL_ADJUDICATED"
    elif canary["gemini"]["point_access"] and any(r["model"]=="gemini" for r in critical):
        verdict="SAME_MODEL_REENTRY_ELIGIBLE_ON_ESTIMAND_CRITICAL_ROWS_ONLY"
    elif gem_ident>0:
        verdict="PARTIAL_ESTIMAND_IDENTIFICATION_WITHOUT_REENTRY_AUTHORITY"
    else:
        verdict="ACCESS_REGIME_UNRESOLVED_TECHNICAL_HOLD"
    out={
      "stage":STAGE,
      "source":{"p54_run":P54_RUN_ID,"rows":len(rows)},
      "missingness_geometry":geom,
      "substitution_audit":sub,
      "estimand_identifiability":{
        "by_model_task":estimand,
        "gemini_identified_tau":gem_ident,
        "gemini_total_tau":96,
        "critical_missing_rows_upper_bound":len(critical),
        "critical_rows":critical
      },
      "access_canary":canary,
      "frozen_p53_primary_reopening":primary,
      "scientific_cell_replays":0,
      "constitutional_verdict":verdict,
      "authority":"P55 distinguishes raw-row completeness from estimand identifiability, audits nonrandom technical missingness without ignorability assumptions, forbids literal cross-model substitution when observed behavior differs, and limits any future replay authority to same-model estimand-critical rows. Canary success establishes only current point access, not bulk capacity.",
    }
    Path("receipts").mkdir(exist_ok=True)
    Path("receipts/p55_result.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({"verdict":verdict,"gemini_identified_tau":gem_ident,"critical_rows":len(critical),"canary":canary,"substitution":sub},indent=2))

if __name__=="__main__":
    if "--self-test" in sys.argv:
        z=possible_taus([0]*32)
        assert len(z)==1 and 1<=z[0]<=33
        u=possible_taus([None]*32)
        assert len(u)>=1 and all(1<=x<=33 for x in u)
        print("P55_PRECHECK_PASS")
    else:main()
