"""P69/P70 actual-original-artifact construct validity court, zero API calls.

Read genuine historical provider rows downloaded from fixed GitHub run IDs.
Do not publish original model strings, task text or source claim text.
"""
from __future__ import annotations
import argparse,collections,json
from pathlib import Path

TASKS=("provenance_0","transformation_0")
CHANNELS=("strict_schema","json_object")
MODELS=("gemini","gptoss120")

def load(path):
    files=list(Path(path).rglob("*.json"))
    if len(files)!=1:raise ValueError("P69_HISTORICAL_ARTIFACT_MISSING_OR_DUPLICATE")
    return json.loads(files[0].read_text())

def count(rows):
    return {"n":len(rows),"provider_response":sum(x["provider_status"]=="RESPONSE" for x in rows),
       "format_valid":sum(x.get("format_valid") is True for x in rows),
       "answer_correct":sum(x.get("answer_correct") is True for x in rows),
       "grounded_correct":sum(x.get("semantic_correct") is True for x in rows),
       "reasons":dict(sorted(collections.Counter(x.get("reason") for x in rows).items()))}

def audit_p69(model,pilot,r1):
    if pilot.get("mode")!="ACTUAL_PROVIDER" or r1.get("mode")!="ACTUAL_PROVIDER":
        raise ValueError("P69_NOT_PAID_ORIGINAL_ROWS")
    if pilot.get("model_bundle")!=model or r1.get("model_bundle")!=model:
        raise ValueError("P69_WRONG_MODEL")
    p=pilot["rows"];r=r1["rows"]
    if len(p)!=96 or len(r)!=32:raise ValueError("P69_BAD_GRID_SIZE")
    kp=[(x["task"],x["vertex"],x["semantic"],x["channel"],x["draw"]) for x in p]
    kr=[(x["task"],x["semantic"],x["version"],x["channel"],x["draw"]) for x in r]
    expected_p={(t,v,s,c,d) for t in TASKS for v in ("I","R","T","RT")
                for s in ("valid","null") for c in CHANNELS for d in (1,2,3)}
    expected_r={(t,s,v,c,d) for t in TASKS for s in ("valid","null")
                for v in ("frozen_v0","procedure_v1") for c in CHANNELS for d in (1,2)}
    if len(set(kp))!=96 or set(kp)!=expected_p or len(set(kr))!=32 or set(kr)!=expected_r:
        raise ValueError("P69_MISSING_DUPLICATE_OR_CHANGED_GRID")
    for rows,keys,index in ((p,kp,(0,1,2,4)),(r,kr,(0,1,2,4))):
        grouped=collections.defaultdict(set)
        for key,row in zip(keys,rows):
            group=tuple(key[i] for i in index)
            grouped[group].add(row["prompt_sha256"])
        if any(len(s)!=1 for s in grouped.values()):
            raise ValueError("P69_CONTRACT_ARMS_DIFFERENT_PROMPT")
    if any(x["provider_status"]!="RESPONSE" for x in p+r):
        raise ValueError("P69_MISSING_RESPONSE")
    arms={ver:{channel:{sem:count([x for x in r if (x["version"],x["channel"],x["semantic"])==(ver,channel,sem)])
                      for sem in ("valid","null")} for channel in CHANNELS}
          for ver in ("frozen_v0","procedure_v1")}
    tasks={task:{ver:{channel:count([x for x in r if x["task"]==task and
                  x["version"]==ver and x["channel"]==channel and x["semantic"]=="valid"])
                  for channel in CHANNELS} for ver in ("frozen_v0","procedure_v1")}
           for task in TASKS}
    return {"initial_pilot":{c:count([x for x in p if x["channel"]==c]) for c in CHANNELS},
            "repair_arms":arms,"repair_positive_by_authored_task":tasks,
            "independent_authored_task_clusters":2}

def audit_scifact(path):
    docs={}
    for f in Path(path).rglob("*.json"):
        if f.name in ("p70_actual_gemini.json","p70_actual_gptoss120.json"):
            if f.name in docs:raise ValueError("P70_DUPLICATE_BUNDLE")
            docs[f.name]=json.loads(f.read_text())
    if len(docs)!=2:raise ValueError("P70_MISSING_REAL_BUNDLES")
    report={}; grids=[]
    for model in MODELS:
        d=docs["p70_actual_"+model+".json"];rows=d["rows"];src=d["source_receipt"]
        if d["mode"]!="ACTUAL_PROVIDER" or d["model_bundle"]!=model or len(rows)!=16:
            raise ValueError("P70_NOT_ACTUAL_16")
        grid=[(r["claim_id"],r["version"]) for r in rows]
        if len(set(grid))!=16 or len({c for c,v in grid})!=4 or set(v for c,v in grid)!={"I","R","H","RH"}:
            raise ValueError("P70_SOURCE_GRID_INVALID")
        if src["dev_sha256"]!="86f0435d08fdb65d1aa41d1472684f57e6e71930626497bdf4d7a9ec1a632217":
            raise ValueError("P70_DEV_SHA_MISMATCH")
        if src["corpus_sha256"]!="b8d6c89624cb2ed74dee8938effc4f5d8bd2086887880af8110d64be4ceade62":
            raise ValueError("P70_CORPUS_SHA_MISMATCH")
        grids.append(tuple(sorted(grid)))
        pairs={(x["claim_id"],x["version"]):x for x in rows}
        multiclass={}
        binary={}
        for op,edges in (("R",(("I","R"),("H","RH"))),
                         ("H",(("I","H"),("R","RH")))):
            transitions=[];binary_transitions=[]
            for claim_id in sorted({x["claim_id"] for x in rows}):
                for a,b in edges:
                    x,y=pairs[claim_id,a],pairs[claim_id,b]
                    transitions.append(x["model_verdict"]!=y["model_verdict"])
                    binary_transitions.append(
                        (x["label_matches_original_annotation"] is True)!=
                        (y["label_matches_original_annotation"] is True))
            multiclass[op]=sum(transitions)
            binary[op]=sum(binary_transitions)
        report[model]={"provider_responses":sum(r["provider_status"]=="RESPONSE" for r in rows),
               "format_valid":sum(r["format_valid"] is True for r in rows),
               "source_label_matches":sum(r["label_matches_original_annotation"] is True for r in rows),
               "annotated_rationale_cited":sum(r["annotated_rationale_cited"] is True for r in rows),
               "underlying_original_claim_clusters":4,
               "wrong_label_even_though_annotated_rationale_cited":sum(
                   r["label_matches_original_annotation"] is not True and
                   r["annotated_rationale_cited"] is True for r in rows),
               "multiclass_label_switches_R_out_of_8":multiclass["R"],
               "multiclass_label_switches_H_out_of_8":multiclass["H"],
               "binary_correctness_switches_R_out_of_8":binary["R"],
               "binary_correctness_switches_H_out_of_8":binary["H"],
               "semantic_packet_truth":"EXTERNAL_ADJUDICATION_MISSING"}
    if grids[0]!=grids[1]:raise ValueError("P70_MISMATCHED_MODEL_SOURCE_CLAIMS")
    return report

def audit(pilot,repair,scifact):
    m={model:audit_p69(model,load(Path(pilot)/model),load(Path(repair)/model)) for model in MODELS}
    p70=audit_scifact(scifact)
    gem=m["gemini"]["repair_arms"]["procedure_v1"]
    assert gem["strict_schema"]["valid"]["grounded_correct"]==0
    assert gem["json_object"]["valid"]["grounded_correct"]==4
    assert all(gem[c][s]["format_valid"]==4 for c in CHANNELS for s in ("valid","null"))
    assert p70["gemini"]["source_label_matches"]==8
    assert p70["gptoss120"]["source_label_matches"]==16
    assert p70["gemini"]["multiclass_label_switches_R_out_of_8"]==1
    assert p70["gemini"]["multiclass_label_switches_H_out_of_8"]==1
    assert p70["gemini"]["binary_correctness_switches_R_out_of_8"]==0
    assert p70["gemini"]["binary_correctness_switches_H_out_of_8"]==0
    assert p70["gemini"]["wrong_label_even_though_annotated_rationale_cited"]==4
    assert p70["gptoss120"]["multiclass_label_switches_R_out_of_8"]==0
    assert p70["gptoss120"]["multiclass_label_switches_H_out_of_8"]==0
    return {"kind":"P69_P70_FROZEN_ACTUAL_ORIGINAL_ROWS_REPLAY","p69":m,"p70":p70,
            "real_provider_observations":192+64+32,
            "new_provider_calls":0,"independent_human_packet_judgments":0,
            "gemini_positive_contract_interaction":"POST_HOC_EXPLORATORY_0_OF_4_VS_4_OF_4",
            "scientific_paper_verdict":"P69_CONSTRUCT_HOLD_P70_SEMANTIC_BRIDGE_HOLD",
            "not_a_causal_or_population_effect":True}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--pilot",required=True);p.add_argument("--repair",required=True)
    p.add_argument("--scifact",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    result=audit(a.pilot,a.repair,a.scifact)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("P69_P70_ORIGINAL_ACTUAL_ROWS_REPLAY_PASS 192+64+32 historical requests scientific_hold=true new_calls=0")
