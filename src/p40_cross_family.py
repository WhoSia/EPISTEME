from __future__ import annotations
import hashlib,json,os,random
from collections import defaultdict
from pathlib import Path

from groq import Groq
from google import genai
from google.genai import types

from p39_common import PROMPT,SEEDS,screen_packets,parse_json,correct,classify_screen

STAGE="EPISTEME-P40"
MODELS={
  "gptoss20":{"provider":"groq","model":"openai/gpt-oss-20b"},
  "gptoss120":{"provider":"groq","model":"openai/gpt-oss-120b"},
  "gemini":{"provider":"gemini","model":"gemini-3.5-flash-lite"},
}
VERTEX_ORDER=[
"I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L",
"R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L",
"R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"
]
RESPONSE_SCHEMA={
 "type":"object",
 "properties":{
  "challenge":{"type":["string","null"]},
  "intervention":{"type":["string","null"]},
  "predicted_direction":{"type":["string","null"],"enum":["different","same",None]},
  "rationale_ids":{"type":"array","items":{"type":"string"}},
 },
 "required":["challenge","intervention","predicted_direction","rationale_ids"],
 "additionalProperties":False,
}

def full_packet(vertex_label,semantic):
    v=set() if vertex_label=="I" else set(vertex_label.split("_"))
    renamed="R" in v; filler="F" in v; rh="H" in v; wl="T" in v; rr="L" in v
    # Frozen P40 common target: measurement × u1, profile 0101, identifier A1N1.
    sep="_"; nonce="q7"; stem="source"; fam="b"; rep=("z" if renamed else "k")+fam+"40"
    key=f"{rep}{sep}{stem}{sep}{nonce}"; alt=f"{key}{sep}alt"
    common=f"hist{sep}{nonce}"; ha_id=f"{common}{sep}a"; hb_id=f"{common}{sep}b{sep}omega"
    fills=["q9","q4"] if filler else ["p2","p3"]
    def tr(t): return [*fills,t] if wl else [t,*fills]
    ha={"history":ha_id,"trace":tr(key)}; hb={"history":hb_id,"trace":tr(alt)}
    histories=[hb,ha] if rh else [ha,hb]
    target={"source":key,"intervention":"u1","response_link":"history-sensitive" if semantic=="valid" else "history-invariant"}
    dist={"source":"decoy-z" if renamed else "distractor-c","intervention":"uX","response_link":"irrelevant"}
    relations=[dist,target] if rr else [target,dist]
    aid="ar40-"+hashlib.sha256(f"0101:{vertex_label}:{semantic}".encode()).hexdigest()[:12]
    return {
      "archive_id":aid,
      "claim":"The retained terminal summary is sufficient to predict the challenge response.",
      "terminal_observation":{ha_id:"T=stable",hb_id:"T=stable"},
      "available_interventions":["u1","uX","uY"],
      "instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.",
      "surface_domain":"measurement-pipeline",
      "retained_history":histories,
      "relation_notes":relations,
    }

def validate(o):
    if set(o)!={"challenge","intervention","predicted_direction","rationale_ids"}: raise ValueError("schema")
    if o["predicted_direction"] not in {"different","same",None}: raise ValueError("direction")
    if not isinstance(o["rationale_ids"],list): raise ValueError("rationale")

def groq_call(model,packet,seed):
    client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=2)
    kwargs={
      "model":model,
      "messages":[{"role":"user","content":PROMPT+"\n\nARCHIVE:\n"+json.dumps(packet,ensure_ascii=False)}],
      "temperature":0.6,"top_p":0.95,"seed":seed,"max_completion_tokens":512,
      "stream":False,
      "response_format":{"type":"json_schema","json_schema":{"name":"episteme_p40","strict":True,"schema":RESPONSE_SCHEMA}},
    }
    if model=="openai/gpt-oss-120b":
        kwargs["reasoning_effort"]="medium"; kwargs["reasoning_format"]="hidden"
    elif model=="openai/gpt-oss-20b":
        kwargs["reasoning_effort"]="medium"; kwargs["reasoning_format"]="hidden"
    resp=client.chat.completions.create(**kwargs)
    o=parse_json(resp.choices[0].message.content or "")
    validate(o); return o

def gemini_call(model,packet,seed):
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    cfg=types.GenerateContentConfig(
      temperature=0.6,top_p=0.95,max_output_tokens=512,seed=seed,
      response_mime_type="application/json",response_json_schema=RESPONSE_SCHEMA,
    )
    resp=client.models.generate_content(
      model=model,
      contents=PROMPT+"\n\nARCHIVE:\n"+json.dumps(packet,ensure_ascii=False),
      config=cfg,
    )
    o=parse_json(resp.text or ""); validate(o); return o

def call(model_key,packet,seed):
    cfg=MODELS[model_key]
    return groq_call(cfg["model"],packet,seed) if cfg["provider"]=="groq" else gemini_call(cfg["model"],packet,seed)

def screen_one(model_key):
    rows=[]
    for item in screen_packets():
        for rep,seed in enumerate(SEEDS,1):
            try:
                o=call(model_key,item["packet"],seed)
                ok=correct(o,item["semantic"]); status="OK"
            except Exception as exc:
                ok=False; status="FORMAT_OR_API_FAIL"
            rows.append({
              "case_id":item["case_id"],"vertex":item["vertex"],"semantic":item["semantic"],
              "replicate":rep,"seed":seed,"status":status,"correct":ok
            })
    by=defaultdict(list)
    for r in rows: by[(r["case_id"],r["semantic"])].append(r)
    v=n=0
    for (_c,s),rs in by.items():
        maj=sum(x["correct"] for x in rs)>=2
        if s=="valid": v+=int(maj)
        else: n+=int(maj)
    return {
      "classification":classify_screen(rows),
      "valid_majority_correct":v,
      "null_majority_correct":n,
      "W":v/6,
      "N":n/6,
      "technical_ok":sum(r["status"]=="OK" for r in rows),
      "rows":rows,
    }

def geometry_one(model_key):
    rows=[]
    for vertex in VERTEX_ORDER:
        for semantic in ("valid","null"):
            packet=full_packet(vertex,semantic)
            for rep,seed in enumerate(SEEDS,1):
                try:
                    o=call(model_key,packet,seed)
                    ok=correct(o,semantic); status="OK"
                except Exception as exc:
                    ok=False; status="FORMAT_OR_API_FAIL"
                rows.append({
                  "vertex":vertex,"semantic":semantic,"replicate":rep,"seed":seed,
                  "status":status,"correct":ok
                })
    bits=[]
    technical=True
    for vertex in VERTEX_ORDER:
        vr=[r for r in rows if r["vertex"]==vertex and r["semantic"]=="valid"]
        nr=[r for r in rows if r["vertex"]==vertex and r["semantic"]=="null"]
        technical &= sum(r["status"]=="OK" for r in vr)>=2 and sum(r["status"]=="OK" for r in nr)>=2
        vp=sum(r["correct"] for r in vr)>=2
        np=sum(r["correct"] for r in nr)>=2
        bits.append("0" if vp and np else "1")
    return {"row":"".join(bits),"technical_evaluable":technical,"rows":rows}

def hamming(a,b): return sum(x!=y for x,y in zip(a,b))

def main():
    screens={k:screen_one(k) for k in MODELS}
    promotable=[k for k,s in screens.items() if s["classification"] in {"SELECTIVE_PROMOTE","PARTIAL_SELECTIVE_PROMOTE"}]
    geometries={k:geometry_one(k) for k in promotable}

    pairwise={}
    keys=sorted(geometries)
    for i,a in enumerate(keys):
        for b in keys[i+1:]:
            pairwise[f"{a}|{b}"]=hamming(geometries[a]["row"],geometries[b]["row"])

    out={
      "stage":STAGE,
      "screen_models":MODELS,
      "screens":screens,
      "promoted_models":promotable,
      "full_geometry_condition":"measurement-pipeline|u1|profile0101|A1N1",
      "geometries":geometries,
      "pairwise_geometry_hamming":pairwise,
      "inherited_p39":{
        "qwen/qwen3.8-27b":{"classification":"GLOBAL_ABSTENTION_REGIME","W":0.0,"N":1.0},
        "qwen/qwen3.6-27b":{"classification":"TECHNICAL_UNEVALUABLE"},
        "Qwen/Qwen2.5-0.5B-Instruct":{"classification":"NONSELECTIVE_NO_PROMOTION","W":0.0,"N":0.0},
        "Qwen/Qwen2.5-1.5B-Instruct":{"classification":"NONSELECTIVE_NO_PROMOTION","W":0.0,"N":0.0},
        "Qwen/Qwen3-0.6B":{"classification":"NONSELECTIVE_NO_PROMOTION","W":0.0,"N":0.0},
        "Qwen/Qwen3-1.7B":{"classification":"NONSELECTIVE_NO_PROMOTION","W":0.0,"N":0.0}
      }
    }
    p=Path("receipts/p40_cross_family.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
