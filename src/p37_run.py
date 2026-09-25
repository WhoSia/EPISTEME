from __future__ import annotations

import argparse,hashlib,json,random
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path

from p17_external_run import MODELS,REPLICATE_SEEDS,TEMPERATURE,TOP_P,MAX_OUTPUT_TOKENS,call_model
from p37_design import (
    PROFILES,ARMS,BASE_ARM,VERTEX_ORDER,phase_a_packets,phase_b_packets,phase_c_packets,
    self_audit,profile_label,arm_label
)

STAGE="EPISTEME-P37"
MODEL_KEY="gemini"

def now_iso(): return datetime.now(timezone.utc).isoformat()

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip()
    return "NONE" if t.upper()=="NONE" else t

def response_correct(r):
    if r.get("status")!="OK": return False
    ans=r.get("parsed_response") or {}
    ch=norm(ans.get("challenge"))
    if r["semantic_class"]=="null": return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")=="u1" and ans.get("predicted_direction")=="different"

def run_packets(items,phase,offset):
    rows=[]
    for rep,seed in enumerate(REPLICATE_SEEDS,1):
        ordered=list(items)
        random.Random(seed+offset).shuffle(ordered)
        for item in ordered:
            started=now_iso()
            try:
                raw,parsed,attempts,repairs=call_model(MODEL_KEY,item["packet"],seed); status="OK"
            except Exception as exc:
                raw={"error":repr(exc)}; parsed=None; attempts=0; repairs=0; status="FORMAT_OR_API_FAIL"
            rows.append({
              "stage":STAGE,"phase":phase,"provider":MODELS[MODEL_KEY]["provider"],"model":MODELS[MODEL_KEY]["model"],
              "packet_id":item["packet_id"],"context":item["context"],"profile":item["profile"],"arm":item["arm"],
              "vertex":item["vertex"],"semantic_class":item["semantic_class"],
              "replicate":rep,"seed":seed,"run_started_at":started,
              "sampling":{"temperature":TEMPERATURE,"top_p":TOP_P,"max_output_tokens":MAX_OUTPUT_TOKENS},
              "http_attempts":attempts,"format_repairs":repairs,"status":status,
              "raw_response":raw,"parsed_response":parsed,
            })
    return rows

def aggregate(rows):
    g=defaultdict(list)
    for r in rows:
        g[(r["context"],r["profile"],r["arm"],r["vertex"],r["semantic_class"])].append(r)
    worlds={}; technical=True
    keys=sorted({(k[0],k[1],k[2]) for k in g})
    for c,p,a in keys:
        bits=[]
        for v in VERTEX_ORDER:
            vr=g[(c,p,a,v,"valid")]
            nr=g[(c,p,a,v,"null")]
            vok=sum(x["status"]=="OK" for x in vr); nok=sum(x["status"]=="OK" for x in nr)
            technical &= vok>=2 and nok>=2
            vp=sum(response_correct(x) for x in vr)>=2
            np=sum(response_correct(x) for x in nr)>=2
            bits.append("0" if vp and np else "1")
        worlds[(c,p,a)]="".join(bits)
    return worlds,technical

def xor(a,b): return "".join(str(int(x!=y)) for x,y in zip(a,b))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); a=ap.parse_args()
    assert self_audit()

    # Phase A: full orthogonal identifier factorial in anchor context.
    Arows=run_packets(phase_a_packets(),"A_anchor_identifier_factorial",37100)
    Aworlds,Atech=aggregate(Arows)

    # Phase B: external A0N0 baselines only.
    Brows=run_packets(phase_b_packets(),"B_external_baselines",37200)
    Bworlds,Btech=aggregate(Brows)

    # Construct anchor identifier-arm effects relative to A0N0.
    effects={}
    for p in PROFILES:
        pl=profile_label(p)
        base=Aworlds[("measurement",pl,arm_label(BASE_ARM))]
        effects[pl]={}
        for arm in ARMS:
            al=arm_label(arm)
            effects[pl][al]=xor(Aworlds[("measurement",pl,al)],base)

    # Predict all external nonbaseline arms before Phase C.
    predictions={}
    for c in ("analysis","sample"):
        predictions[c]={}
        for p in PROFILES:
            pl=profile_label(p)
            base=Bworlds[(c,pl,arm_label(BASE_ARM))]
            predictions[c][pl]={}
            for arm in ARMS:
                if arm==BASE_ARM: continue
                al=arm_label(arm)
                predictions[c][pl][al]="".join(str(int(x)^int(d)) for x,d in zip(base,effects[pl][al]))

    preseal={
      "created_before_phase_C":True,
      "created_at":now_iso(),
      "anchor_identifier_effects":effects,
      "external_baselines":{
        c:{profile_label(p):Bworlds[(c,profile_label(p),arm_label(BASE_ARM))] for p in PROFILES}
        for c in ("analysis","sample")
      },
      "predicted_external_rows":predictions,
      "prospective_cells":2*3*3*32
    }
    canonical=json.dumps(preseal,sort_keys=True,separators=(",",":"))
    preseal["sha256"]=hashlib.sha256(canonical.encode()).hexdigest()

    out_path=Path(a.out); out_path.parent.mkdir(parents=True,exist_ok=True)
    preseal_path=out_path.with_name(out_path.stem+"_preseal.json")
    preseal_path.write_text(json.dumps(preseal,ensure_ascii=False,indent=2),encoding="utf-8")

    # Phase C only after preseal sidecar exists.
    Crows=run_packets(phase_c_packets(),"C_external_identifier_transport_test",37300)

    out={
      "stage":STAGE,"model_key":MODEL_KEY,"provider":MODELS[MODEL_KEY]["provider"],"model":MODELS[MODEL_KEY]["model"],
      "preseal":preseal,
      "technical_prephase":Atech and Btech,
      "rows":Arows+Brows+Crows
    }
    out_path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
