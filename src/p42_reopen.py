from __future__ import annotations
import hashlib,json,os,time
from collections import defaultdict
from pathlib import Path

from groq import Groq
from google import genai
from google.genai import types

STAGE="EPISTEME-P42"
MODELS={
 "gptoss20":{"provider":"groq","family":"gpt-oss","model":"openai/gpt-oss-20b"},
 "gptoss120":{"provider":"groq","family":"gpt-oss","model":"openai/gpt-oss-120b"},
 "gemini":{"provider":"gemini","family":"gemini","model":"gemini-3.5-flash-lite"},
}
SCREEN_VERTICES=("I","R","H_T_L","R_F_H","R_F_T_L","R_F_H_T_L")
VERTICES=("I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L","R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L","R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L")
SCREEN_SEEDS=(4201,4202,4203,4204,4205)
GEOM_SEEDS=(4211,4212,4213)
PROMPT=("You are reviewing a scientific archive and an incumbent sufficiency claim. Using only the retained information in this archive, propose the single strongest experiment that could falsify the claim. Do not invent missing variables, relations, or measurements. If the archive does not justify a specific falsifying experiment, return NONE. Return only a JSON object with exactly these keys: challenge, intervention, predicted_direction, rationale_ids.")
SCHEMA={
 "type":"object",
 "properties":{
  "challenge":{"anyOf":[{"type":"string"},{"type":"null"}]},
  "intervention":{"anyOf":[{"type":"string"},{"type":"null"}]},
  "predicted_direction":{"anyOf":[{"type":"string","enum":["different","same"]},{"type":"null"}]},
  "rationale_ids":{"type":"array","items":{"type":"string"}}
 },
 "required":["challenge","intervention","predicted_direction","rationale_ids"],
 "additionalProperties":False
}
CANARY={"challenge":"contract-canary","intervention":"u0","predicted_direction":"same","rationale_ids":["canary-0"]}
CANARY_PROMPT=("This is a response-contract canary, not a scientific task. Return exactly one JSON object with challenge='contract-canary', intervention='u0', predicted_direction='same', and rationale_ids=['canary-0']. No other keys or text.")


def parse(text):
 t=(text or "").strip()
 try:o=json.loads(t)
 except Exception:
  i=t.find("{")
  if i<0:raise
  o,_=json.JSONDecoder().raw_decode(t[i:])
 validate(o);return o

def validate(o):
 if not isinstance(o,dict) or set(o)!={"challenge","intervention","predicted_direction","rationale_ids"}:raise ValueError("exact-schema")
 if o["challenge"] is not None and not isinstance(o["challenge"],str):raise ValueError("challenge-type")
 if o["intervention"] is not None and not isinstance(o["intervention"],str):raise ValueError("intervention-type")
 if o["predicted_direction"] not in {"different","same",None}:raise ValueError("direction")
 if not isinstance(o["rationale_ids"],list) or not all(isinstance(x,str) for x in o["rationale_ids"]):raise ValueError("rationale")

def vertex_set(label):return set() if label=="I" else set(label.split("_"))

def packet(label,semantic,phase):
 v=vertex_set(label); renamed="R" in v; filler="F" in v; rh="H" in v; wl="T" in v; rr="L" in v
 # Fresh aliases; semantic relation is the only valid/null difference.
 prefix="lambda42" if renamed else "kappa42"; key=f"{prefix}-source-q11"; alt=key+"-counterpart"
 fills=["aux-17","aux-23"] if filler else ["aux-5","aux-31"]
 def tr(t):return [*fills,t] if wl else [t,*fills]
 ha_id="trajectory-42-alpha";hb_id="trajectory-42-beta"
 ha={"history":ha_id,"trace":tr(key)};hb={"history":hb_id,"trace":tr(alt)}
 histories=[hb,ha] if rh else [ha,hb]
 target={"source":key,"intervention":"u1","response_link":"history-sensitive" if semantic=="valid" else "history-invariant"}
 decoy={"source":"lambda42-decoy" if renamed else "kappa42-decoy","intervention":"uX","response_link":"irrelevant"}
 relations=[decoy,target] if rr else [target,decoy]
 aid="ar42-"+hashlib.sha256(f"{phase}:0101:A1N1:{label}:{semantic}".encode()).hexdigest()[:14]
 return {"archive_id":aid,"claim":"The retained terminal summary is sufficient to predict the challenge response.","terminal_observation":{ha_id:"T=stable",hb_id:"T=stable"},"available_interventions":["u1","uX","uY"],"instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.","surface_domain":"measurement-pipeline","retained_history":histories,"relation_notes":relations}

def correct(o,semantic):
 ch=o.get("challenge")
 if semantic=="null":return ch is None or str(ch).strip().upper()=="NONE"
 return ch is not None and str(ch).strip().upper()!="NONE" and o.get("intervention")=="u1" and o.get("predicted_direction")=="different"

def groq_raw(client,model,prompt,contract):
 kw={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0.2,"top_p":0.95,"max_completion_tokens":1536,"stream":False}
 if contract["reasoning"]:kw["reasoning_effort"]=contract["reasoning"];kw["reasoning_format"]="hidden"
 if contract["format"]=="schema":kw["response_format"]={"type":"json_schema","json_schema":{"name":"episteme_p42","strict":True,"schema":SCHEMA}}
 elif contract["format"]=="object":kw["response_format"]={"type":"json_object"}
 return client.chat.completions.create(**kw).choices[0].message.content or ""

def calibrate_groq(model):
 client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=4)
 candidates=[{"name":"schema_hidden_medium","format":"schema","reasoning":"medium"},{"name":"object_hidden_medium","format":"object","reasoning":"medium"},{"name":"object_hidden_low","format":"object","reasoning":"low"},{"name":"plain_hidden_low","format":"plain","reasoning":"low"}]
 audit=[]
 for c in candidates:
  ok=0;errs=[]
  for _ in range(3):
   try:
    o=parse(groq_raw(client,model,CANARY_PROMPT,c)); good=o==CANARY;ok+=int(good)
    if not good:errs.append("canary-value-mismatch")
   except Exception as e:errs.append(type(e).__name__+":"+str(e)[:240])
  audit.append({"contract":c,"ok":ok,"errors":errs})
  if ok==3:return c,audit
 return None,audit

def gemini_raw(client,model,prompt,seed):
 cfg=types.GenerateContentConfig(temperature=0.2,top_p=0.95,max_output_tokens=1536,seed=seed,response_mime_type="application/json",response_json_schema=SCHEMA)
 return client.models.generate_content(model=model,contents=prompt,config=cfg).text or ""

def calibrate_gemini(model):
 client=genai.Client(api_key=os.environ["GEMINI_API_KEY"]);errs=[];ok=0
 for seed in (4291,4292,4293):
  try:
   o=parse(gemini_raw(client,model,CANARY_PROMPT,seed));good=o==CANARY;ok+=int(good)
   if not good:errs.append("canary-value-mismatch")
  except Exception as e:errs.append(type(e).__name__+":"+str(e)[:240])
 return ({"name":"gemini_native_schema","format":"schema","reasoning":None} if ok==3 else None),[{"contract":"gemini_native_schema","ok":ok,"errors":errs}]

def call(model_key,contract,pkt,seed):
 cfg=MODELS[model_key];text=PROMPT+"\n\nARCHIVE:\n"+json.dumps(pkt,ensure_ascii=False)
 if cfg["provider"]=="groq":
  client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=4);return parse(groq_raw(client,cfg["model"],text,contract))
 client=genai.Client(api_key=os.environ["GEMINI_API_KEY"]);return parse(gemini_raw(client,cfg["model"],text,seed))

def run_screen(model_key,contract):
 rows=[]
 for i,label in enumerate(SCREEN_VERTICES,1):
  for semantic in ("valid","null"):
   pkt=packet(label,semantic,"screen")
   for rep,seed in enumerate(SCREEN_SEEDS,1):
    try:o=call(model_key,contract,pkt,seed);ok=correct(o,semantic);status="OK";err=None
    except Exception as e:ok=False;status="TECHNICAL_FAIL";err=type(e).__name__+":"+str(e)[:300]
    rows.append({"group":i,"vertex":label,"semantic":semantic,"replicate":rep,"seed":seed,"status":status,"correct":ok,"error":err})
 by=defaultdict(list)
 for r in rows:by[(r["group"],r["semantic"])].append(r)
 v=n=0
 for (_g,s),rs in by.items():
  maj=sum(x["correct"] for x in rs)>=3
  if s=="valid":v+=int(maj)
  else:n+=int(maj)
 tech=sum(r["status"]=="OK" for r in rows);evaluable=tech>=58
 if not evaluable:cls="TECHNICAL_UNEVALUABLE"
 elif v==0 and n>=5:cls="GLOBAL_ABSTENTION_REGIME"
 elif v>=4 and n>=5:cls="SELECTIVE_PROMOTE"
 elif v>=2 and n>=4:cls="PARTIAL_SELECTIVE_PROMOTE"
 else:cls="NONSELECTIVE_NO_PROMOTION"
 return {"classification":cls,"technical_ok":tech,"valid_majority_correct":v,"null_majority_correct":n,"W":v/6,"N":n/6,"rows":rows}

def run_geometry(model_key,contract):
 rows=[];bits=[]
 for label in VERTICES:
  local={}
  for semantic in ("valid","null"):
   rs=[];pkt=packet(label,semantic,"geometry")
   for rep,seed in enumerate(GEOM_SEEDS,1):
    try:o=call(model_key,contract,pkt,seed);ok=correct(o,semantic);status="OK";err=None
    except Exception as e:ok=False;status="TECHNICAL_FAIL";err=type(e).__name__+":"+str(e)[:300]
    rr={"vertex":label,"semantic":semantic,"replicate":rep,"seed":seed,"status":status,"correct":ok,"error":err};rows.append(rr);rs.append(rr)
   local[semantic]=rs
  tech=all(sum(x["status"]=="OK" for x in local[s])>=2 for s in ("valid","null"))
  selective=tech and all(sum(x["correct"] for x in local[s])>=2 for s in ("valid","null"))
  bits.append("0" if selective else "1")
 return {"row":"".join(bits),"technical_evaluable":all(sum(r["status"]=="OK" for r in rows if r["vertex"]==v and r["semantic"]==s)>=2 for v in VERTICES for s in ("valid","null")),"rows":rows}

def quotient(geoms):
 keys=sorted(geoms);blocks=defaultdict(list)
 for i,v in enumerate(VERTICES):blocks[tuple(geoms[k]["row"][i] for k in keys)].append(v)
 return {"model_order":keys,"blocks":[{"signature":"".join(sig),"vertices":vs} for sig,vs in sorted(blocks.items())]}

def main():
 contracts={};calibration={}
 for k,cfg in MODELS.items():
  contract,audit=(calibrate_groq(cfg["model"]) if cfg["provider"]=="groq" else calibrate_gemini(cfg["model"]))
  contracts[k]=contract;calibration[k]=audit
 screens={}
 for k in MODELS:
  screens[k]=run_screen(k,contracts[k]) if contracts[k] else {"classification":"TECHNICAL_UNRECOVERED","technical_ok":0,"rows":[]}
 promoted=[k for k,s in screens.items() if s["classification"] in {"SELECTIVE_PROMOTE","PARTIAL_SELECTIVE_PROMOTE"}]
 geoms={k:run_geometry(k,contracts[k]) for k in promoted}
 eval_geoms={k:g for k,g in geoms.items() if g["technical_evaluable"]}
 pairwise={}
 ks=sorted(eval_geoms)
 for i,a in enumerate(ks):
  for b in ks[i+1:]:pairwise[f"{a}|{b}"]=sum(x!=y for x,y in zip(eval_geoms[a]["row"],eval_geoms[b]["row"]))
 families=sorted({MODELS[k]["family"] for k in eval_geoms})
 cross=len(families)>=2
 out={"stage":STAGE,"contracts":contracts,"contract_calibration":calibration,"screens":screens,"promoted_models":promoted,"geometries":geoms,"pairwise_hamming":pairwise,"promoted_families":families,"cross_family_domain_constituted":cross,"quotient":quotient(eval_geoms) if cross else None,"constitutional_verdict":"NONVACUOUS_CROSS_FAMILY_GEOMETRY_CONSTITUTED" if cross else "SELECTIVITY_DOMAIN_REOPENED_BUT_CROSS_FAMILY_GEOMETRY_NOT_CONSTITUTED" if promoted else "SELECTIVITY_DOMAIN_REMAINS_CLOSED","authority":"Prospective P42 behavior under technically calibrated response contracts; no neural-mechanism or family-capability claim."}
 p=Path("receipts/p42_result.json");p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding="utf-8")

if __name__=="__main__":main()
