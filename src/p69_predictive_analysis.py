"""P69 evaluation, all-call executable endpoints and out-of-mechanism Brier audit.
Requires a COMPLETE 8192-row JSONL result lattice. No provider calls.
"""
import json,itertools
from pathlib import Path

MODELS=("gptoss120","gemini")
CHANNELS=("strict_schema","json_object")
FAMILIES=("provenance","composition","guarded","transformation")
TASKS=tuple(f"{f}_{i}" for f in FAMILIES for i in (1,2))
VERTICES=tuple("".join(k for k,v in zip("RFHTL",(r,f,h,t,l)) if v) or "I"
    for f,h,l in ((0,0,0),(0,1,1),(1,0,1),(1,1,0)) for r,t in itertools.product((0,1),repeat=2))
ANCHORS=("I","R","T","RT")
DRAWS=tuple(range(1,9))

def full_input(path):
    with open(path) as file:rows=[json.loads(line) for line in file if line.strip()]
    if len(rows)!=8192:raise ValueError("P69_INCOMPLETE_CALL_LATTICE")
    data={}
    for row in rows:
        key=tuple(row[k] for k in ("model","task","vertex","semantic","channel","draw"))
        if key in data:raise ValueError("duplicate P69 call")
        if not isinstance(row["format_valid"],bool) or row["semantic_correct"] not in (True,False,None):
            raise ValueError("invalid status")
        if not row["format_valid"] and row["semantic_correct"] is not None:
            raise ValueError("invalid semantic outcome imputation")
        data[key]=row
    for key in itertools.product(MODELS,TASKS,VERTICES,("valid","null"),CHANNELS,DRAWS):
        if key not in data:raise ValueError("missing P69 call identity")
    return data

def report(data):
    executable={}
    for model,task,vertex,channel,draw in itertools.product(MODELS,TASKS,VERTICES,CHANNELS,DRAWS):
        rows=[data[(model,task,vertex,s,channel,draw)] for s in ("valid","null")]
        executable[(model,task,vertex,channel,draw)]=int(all(x["format_valid"] and x["semantic_correct"] is True for x in rows))
    operators=[];predictions=[]
    for model,channel in itertools.product(MODELS,CHANNELS):
        p={t:{v:sum(executable[(model,t,v,channel,d)] for d in DRAWS)/8 for v in VERTICES} for t in TASKS}
        for task in TASKS:
            effects={}
            for op in ("R","T"):
                pair_diffs=[]
                for v in VERTICES:
                    current=set() if v=="I" else set(v)
                    if op in current:continue
                    active="".join(k for k in "RFHTL" if k in current|{op})
                    pair_diffs.append(p[task][active]-p[task][v])
                assert len(pair_diffs)==8
                effects[op]=sum(pair_diffs)/8
            operators.append({"model":model,"channel":channel,"task":task,"family":task.rsplit("_",1)[0],"R_effect":effects["R"],"T_effect":effects["T"]})
        for heldout in FAMILIES:
            train=[t for t in TASKS if not t.startswith(heldout+"_")]
            assert len(train)==6
            offsets={v:sum(p[t][v]-sum(p[t][a] for a in ANCHORS)/4 for t in train)/6 for v in VERTICES}
            for task in (f"{heldout}_1",f"{heldout}_2"):
                base=sum(p[task][a] for a in ANCHORS)/4
                pred={v:min(1,max(0,base+offsets[v])) for v in VERTICES}
                test=[(v,d) for v in VERTICES if v not in ANCHORS for d in DRAWS]
                brier0=sum((executable[(model,task,v,channel,d)]-base)**2 for v,d in test)/len(test)
                brier1=sum((executable[(model,task,v,channel,d)]-pred[v])**2 for v,d in test)/len(test)
                predictions.append({"model":model,"channel":channel,"heldout_family":heldout,"task":task,"baseline_brier":brier0,"transport_brier":brier1,"improvement":brier0-brier1,"test_calls":len(test)})
    return {"stage":"EPISTEME-P69","joint_cells":len(executable),"operator_effects":operators,"heldout_predictions":predictions,
            "claim_ceiling":"Only four independent synthetic mechanism clusters. No significance or naturalistic generalization from point estimates."}

def fixture(path,opposite=False):
    with open(path,"w") as out:
        for model,task,v,semantic,channel,draw in itertools.product(MODELS,TASKS,VERTICES,("valid","null"),CHANNELS,DRAWS):
            value=True if not opposite else (("R" in v)==(task.split("_")[0] in ("provenance","guarded")))
            out.write(json.dumps({"model":model,"task":task,"vertex":v,"semantic":semantic,"channel":channel,"draw":draw,"format_valid":True,"semantic_correct":value})+"\n")

def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
        p=Path(folder)/"mock.jsonl"
        for opposite in (False,True):
            fixture(p,opposite)
            z=report(full_input(p))
            assert z["joint_cells"]==4096 and len(z["operator_effects"])==32 and len(z["heldout_predictions"])==32
            if not opposite:
                assert all(x["R_effect"]==x["T_effect"]==0 for x in z["operator_effects"])
                assert all(x["baseline_brier"]==x["transport_brier"]==0 for x in z["heldout_predictions"])
            else:
                signs={x["family"]:x["R_effect"] for x in z["operator_effects"] if x["model"]=="gptoss120" and x["channel"]=="strict_schema"}
                assert signs["provenance"]>0 and signs["composition"]<0
    print("P69_PREDICTIVE_FIXTURE_PASS rows=8192 joint_cells=4096 families=4 provider_calls=0")

if __name__=="__main__":self_test()
