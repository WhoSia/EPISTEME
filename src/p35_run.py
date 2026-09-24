from __future__ import annotations

import argparse,hashlib,json,random
from datetime import datetime,timezone
from pathlib import Path

from p17_external_run import MODELS,REPLICATE_SEEDS,TEMPERATURE,TOP_P,MAX_OUTPUT_TOKENS,call_model
from p35_design import (
    ANCHOR,EXTERNAL,EXTERNAL_TEST_PROFILES,BASELINE_PROFILE,VERTICES,VERTEX_ORDER,
    phase_a_packets,phase_b_packets,phase_c_packets,self_audit,profile_label
)

STAGE="EPISTEME-P35"
MODEL_KEY="gemini"

def now_iso(): return datetime.now(timezone.utc).isoformat()

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip()
    return "NONE" if t.upper()=="NONE" else t

def response_correct(row,semantic,intervention="u1"):
    if row.get("status")!="OK": return False
    ans=row.get("parsed_response") or {}
    ch=norm(ans.get("challenge"))
    if semantic=="null": return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")==intervention and ans.get("predicted_direction")=="different"

def run_packets(packet_items,phase,offset):
    rows=[]
    for rep,seed in enumerate(REPLICATE_SEEDS,1):
        ordered=list(packet_items)
        random.Random(seed+offset).shuffle(ordered)
        for item in ordered:
            started=now_iso()
            try:
                raw,parsed,attempts,repairs=call_model(MODEL_KEY,item["packet"],seed); status="OK"
            except Exception as exc:
                raw={"error":repr(exc)}; parsed=None; attempts=0; repairs=0; status="FORMAT_OR_API_FAIL"
            rows.append({
              "stage":STAGE,"phase":phase,"provider":MODELS[MODEL_KEY]["provider"],"model":MODELS[MODEL_KEY]["model"],
              "packet_id":item["packet_id"],"context":item["context"],"profile":item["profile"],
              "vertex":item["vertex"],"semantic_class":item["semantic_class"],
              "replicate":rep,"seed":seed,"run_started_at":started,
              "sampling":{"temperature":TEMPERATURE,"top_p":TOP_P,"max_output_tokens":MAX_OUTPUT_TOKENS},
              "http_attempts":attempts,"format_repairs":repairs,"status":status,
              "raw_response":raw,"parsed_response":parsed,
            })
    return rows

def aggregate_rows(rows):
    from collections import defaultdict
    g=defaultdict(list)
    for r in rows:
        g[(r["context"],r["profile"],r["vertex"],r["semantic_class"])].append(r)
    sem={}
    for k,reps in g.items():
        ok=sum(r["status"]=="OK" for r in reps)
        votes=sum(response_correct(r,k[3]) for r in reps)
        sem[k]={"ok":ok,"correct":votes>=2}
    worlds={}
    contexts=sorted({k[0] for k in g})
    profiles=sorted({k[1] for k in g})
    for c in contexts:
        for p in profiles:
            if (c,p,VERTEX_ORDER[0],"valid") not in sem: continue
            bits=[]
            for v in VERTEX_ORDER:
                va=sem[(c,p,v,"valid")]
                nu=sem[(c,p,v,"null")]
                passed=va["correct"] and nu["correct"]
                bits.append("0" if passed else "1")
            worlds[(c,p)]="".join(bits)
    return worlds,sem

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); a=ap.parse_args()
    assert self_audit()

    # Phase A: identify anchor construction-effect geometry.
    A=run_packets(phase_a_packets(),"A_anchor_full_factorial",35100)
    worldsA,semA=aggregate_rows(A)
    anchor0=worldsA[("anchor",profile_label(BASELINE_PROFILE))]
    delta={}
    for p in EXTERNAL_TEST_PROFILES:
        lab=profile_label(p)
        row=worldsA[("anchor",lab)]
        delta[lab]="".join(str(int(x!=y)) for x,y in zip(row,anchor0))

    # Phase B: obtain external-context baselines before any target-profile call.
    B=run_packets(phase_b_packets(),"B_external_baselines",35200)
    worldsB,semB=aggregate_rows(B)

    predictions={}
    for c in ("analysis","sample"):
        base=worldsB[(c,profile_label(BASELINE_PROFILE))]
        predictions[c]={}
        for p in EXTERNAL_TEST_PROFILES:
            lab=profile_label(p)
            predictions[c][lab]="".join(str(int(x)^int(d)) for x,d in zip(base,delta[lab]))

    preseal_payload={
      "created_before_phase_C":True,
      "created_at":now_iso(),
      "anchor_baseline":anchor0,
      "anchor_effect_deltas":delta,
      "external_baselines":{c:worldsB[(c,profile_label(BASELINE_PROFILE))] for c in ("analysis","sample")},
      "predicted_external_rows":predictions,
      "test_profiles":[profile_label(p) for p in EXTERNAL_TEST_PROFILES],
    }
    canonical=json.dumps(preseal_payload,sort_keys=True,separators=(",",":"))
    preseal_payload["sha256"]=hashlib.sha256(canonical.encode()).hexdigest()

    # Materialize a pre-Phase-C sidecar before any external target-profile call.
    out_path=Path(a.out)
    preseal_path=out_path.with_name(out_path.stem+"_preseal.json")
    preseal_path.parent.mkdir(parents=True,exist_ok=True)
    preseal_path.write_text(json.dumps(preseal_payload,ensure_ascii=False,indent=2),encoding="utf-8")

    # Only after the sidecar preseal exists do we call external target profiles.
    C=run_packets(phase_c_packets(),"C_external_transport_test",35300)

    out={
      "stage":STAGE,
      "model_key":MODEL_KEY,
      "provider":MODELS[MODEL_KEY]["provider"],
      "model":MODELS[MODEL_KEY]["model"],
      "preseal":preseal_payload,
      "rows":A+B+C,
    }
    p=Path(a.out); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
