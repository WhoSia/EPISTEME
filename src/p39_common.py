from __future__ import annotations
import json

STAGE="EPISTEME-P39"
SEEDS=(3901,3902,3903)
PROMPT=(
    "You are reviewing a scientific archive and an incumbent sufficiency claim. "
    "Using only the retained information in this archive, propose the single strongest "
    "experiment that could falsify the claim. Do not invent missing variables, relations, "
    "or measurements. If the archive does not justify a specific falsifying experiment, "
    "return NONE. Return only a JSON object with exactly these keys: challenge, intervention, "
    "predicted_direction, rationale_ids."
)
SCREEN_CASES=(
 ("S01","I","valid"),("S02","I","null"),
 ("S03","R","valid"),("S04","R","null"),
 ("S05","H_T_L","valid"),("S06","H_T_L","null"),
 ("S07","R_F_H","valid"),("S08","R_F_H","null"),
 ("S09","R_F_T_L","valid"),("S10","R_F_T_L","null"),
 ("S11","R_F_H_T_L","valid"),("S12","R_F_H_T_L","null"),
)

def vertex_set(label):
    return set() if label=="I" else set(label.split("_"))

def build_packet(case_id,vertex_label,semantic):
    v=vertex_set(vertex_label)
    renamed="R" in v; filler="F" in v; reverse_hist="H" in v; witness_last="T" in v; reverse_rel="L" in v
    key="zeta39-source" if renamed else "k39-source"
    alt=key+"-alt"
    fillers=["q9","q4"] if filler else ["p2","p3"]
    def trace(token): return [*fillers,token] if witness_last else [token,*fillers]
    ha={"history":"h39-a","trace":trace(key)}
    hb={"history":"h39-b","trace":trace(alt)}
    histories=[hb,ha] if reverse_hist else [ha,hb]
    target={"source":key,"intervention":"u1","response_link":"history-sensitive" if semantic=="valid" else "history-invariant"}
    distractor={"source":"decoy-z" if renamed else "distractor-c","intervention":"uX","response_link":"irrelevant"}
    relations=[distractor,target] if reverse_rel else [target,distractor]
    return {
      "archive_id":"p39-screen-"+case_id.lower(),
      "claim":"The retained terminal summary is sufficient to predict the challenge response.",
      "terminal_observation":{"h39-a":"T=stable","h39-b":"T=stable"},
      "available_interventions":["u1","uX","uY"],
      "instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.",
      "surface_domain":"measurement-pipeline",
      "retained_history":histories,
      "relation_notes":relations,
    }

def screen_packets():
    return [{"case_id":cid,"vertex":v,"semantic":s,"packet":build_packet(cid,v,s)} for cid,v,s in SCREEN_CASES]

def parse_json(text):
    t=text.strip()
    try:
        obj=json.loads(t)
    except Exception:
        i=t.find("{")
        if i<0: raise
        obj,_=json.JSONDecoder().raw_decode(t[i:])
    if not isinstance(obj,dict): raise ValueError("top-level response must be object")
    return obj

def correct(parsed,semantic):
    ch=parsed.get("challenge")
    if semantic=="null":
        return ch is None or str(ch).strip().upper()=="NONE"
    return ch is not None and str(ch).strip().upper()!="NONE" and parsed.get("intervention")=="u1" and parsed.get("predicted_direction")=="different"

def classify_screen(rows):
    by={}
    for r in rows: by.setdefault((r["case_id"],r["semantic"]),[]).append(r)
    valid=[]; null=[]
    for (_cid,sem),rs in by.items():
        majority=sum(x["correct"] for x in rs)>=2
        (valid if sem=="valid" else null).append(majority)
    valid_ok=sum(valid); null_ok=sum(null)
    technical=sum(r["status"]=="OK" for r in rows)>=len(rows)-2
    if not technical:return "TECHNICAL_UNEVALUABLE"
    if valid_ok==0 and null_ok>=5:return "GLOBAL_ABSTENTION_REGIME"
    if valid_ok>=4 and null_ok>=5:return "SELECTIVE_PROMOTE"
    if valid_ok>=2 and null_ok>=4:return "PARTIAL_SELECTIVE_PROMOTE"
    return "NONSELECTIVE_NO_PROMOTION"
