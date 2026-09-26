from __future__ import annotations
import hashlib,json,math,os
from collections import defaultdict
from pathlib import Path

from groq import Groq
from google import genai
from p42_reopen import PROMPT,VERTICES,parse,correct,groq_raw,gemini_raw

STAGE="EPISTEME-P43"
MODELS={
    "gptoss120":{"provider":"groq","family":"gpt-oss","model":"openai/gpt-oss-120b"},
    "gemini":{"provider":"gemini","family":"gemini","model":"gemini-3.5-flash-lite"},
}
CONTRACTS={
    "gptoss120":{"name":"schema_hidden_medium","format":"schema","reasoning":"medium"},
    "gemini":{"name":"gemini_native_schema","format":"schema","reasoning":None},
}
SCREEN_VERTICES=("I","R","H_T_L","R_F_H","R_F_T_L","R_F_H_T_L")
SCREEN_SEEDS=(4301,4302,4303,4304,4305)
GEOM_SEEDS=(4311,4312,4313)
P42_GPTOSS120_ROW="00000000000001000000000100010000"
P42_EXCEPTIONAL={v for v,b in zip(VERTICES,P42_GPTOSS120_ROW) if b=="1"}

def vertex_set(label):
    return set() if label=="I" else set(label.split("_"))

def packet(label,semantic,phase):
    v=vertex_set(label)
    renamed="R" in v; filler="F" in v; reverse_history="H" in v; witness_last="T" in v; reverse_relation="L" in v
    prefix="nu43" if renamed else "mu43"
    key=f"{prefix}-source-r17"; alt=key+"-counterpart"
    fillers=["aux-43-19","aux-43-37"] if filler else ["aux-43-7","aux-43-29"]
    def trace(token): return [*fillers,token] if witness_last else [token,*fillers]
    ha_id="trajectory-43-alpha"; hb_id="trajectory-43-beta"
    ha={"history":ha_id,"trace":trace(key)}; hb={"history":hb_id,"trace":trace(alt)}
    histories=[hb,ha] if reverse_history else [ha,hb]
    target={"source":key,"intervention":"u1","response_link":"history-sensitive" if semantic=="valid" else "history-invariant"}
    decoy={"source":f"{prefix}-decoy","intervention":"uX","response_link":"irrelevant"}
    relations=[decoy,target] if reverse_relation else [target,decoy]
    aid="ar43-"+hashlib.sha256(f"{phase}:0101:A1N1:{label}:{semantic}".encode()).hexdigest()[:14]
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

def call(model_key,pkt,seed):
    cfg=MODELS[model_key]; contract=CONTRACTS[model_key]
    text=PROMPT+"\n\nARCHIVE:\n"+json.dumps(pkt,ensure_ascii=False)
    if cfg["provider"]=="groq":
        client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=4)
        return parse(groq_raw(client,cfg["model"],text,contract))
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return parse(gemini_raw(client,cfg["model"],text,seed))

def wilson(k,n,z=1.959963984540054):
    if n==0:return [None,None]
    p=k/n; den=1+z*z/n
    c=(p+z*z/(2*n))/den
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,c-h),min(1,c+h)]

def run_screen(model_key):
    rows=[]
    for group,label in enumerate(SCREEN_VERTICES,1):
        for semantic in ("valid","null"):
            pkt=packet(label,semantic,"screen")
            for rep,seed in enumerate(SCREEN_SEEDS,1):
                try:
                    o=call(model_key,pkt,seed); ok=correct(o,semantic); status="OK"; err=None
                except Exception as e:
                    ok=False; status="TECHNICAL_FAIL"; err=type(e).__name__+":"+str(e)[:300]
                rows.append({"group":group,"vertex":label,"semantic":semantic,"replicate":rep,"seed":seed,"status":status,"correct":ok,"error":err})
    by=defaultdict(list)
    for r in rows: by[(r["group"],r["semantic"])].append(r)
    majority={}
    for (g,s),rs in by.items(): majority[(g,s)]=sum(x["correct"] for x in rs)>=3
    v=sum(majority[(g,"valid")] for g in range(1,7)); n=sum(majority[(g,"null")] for g in range(1,7))
    tech=sum(r["status"]=="OK" for r in rows); evaluable=tech>=58
    if not evaluable: cls="TECHNICAL_UNEVALUABLE"
    elif v==0 and n>=5: cls="GLOBAL_ABSTENTION_REGIME"
    elif v>=4 and n>=5: cls="SELECTIVE_PROMOTE"
    elif v>=2 and n>=4: cls="PARTIAL_SELECTIVE_PROMOTE"
    else: cls="NONSELECTIVE_NO_PROMOTION"
    return {"classification":cls,"technical_ok":tech,"valid_majority_correct":v,"null_majority_correct":n,"W":v/6,"N":n/6,"wilson95_W":wilson(v,6),"wilson95_N":wilson(n,6),"rows":rows}

def run_geometry(model_key):
    rows=[]; bits=[]
    for label in VERTICES:
        local={}
        for semantic in ("valid","null"):
            rs=[]; pkt=packet(label,semantic,"geometry")
            for rep,seed in enumerate(GEOM_SEEDS,1):
                try:
                    o=call(model_key,pkt,seed); ok=correct(o,semantic); status="OK"; err=None
                except Exception as e:
                    ok=False; status="TECHNICAL_FAIL"; err=type(e).__name__+":"+str(e)[:300]
                rr={"vertex":label,"semantic":semantic,"replicate":rep,"seed":seed,"status":status,"correct":ok,"error":err}
                rows.append(rr); rs.append(rr)
            local[semantic]=rs
        tech=all(sum(x["status"]=="OK" for x in local[s])>=2 for s in ("valid","null"))
        selective=tech and all(sum(x["correct"] for x in local[s])>=2 for s in ("valid","null"))
        bits.append("0" if selective else "1")
    technical=all(sum(r["status"]=="OK" for r in rows if r["vertex"]==v and r["semantic"]==s)>=2 for v in VERTICES for s in ("valid","null"))
    row="".join(bits)
    return {"row":row,"technical_evaluable":technical,"exceptional_vertices":[v for v,b in zip(VERTICES,row) if b=="1"],"rows":rows}

def cube_distance(a,b):
    return len(vertex_set(a)^vertex_set(b))

def hausdorff(a,b):
    a=set(a); b=set(b)
    if not a and not b:return 0
    if not a or not b:return None
    def directed(x,y):return max(min(cube_distance(i,j) for j in y) for i in x)
    return max(directed(a,b),directed(b,a))

def quotient(rows):
    order=list(rows); blocks=defaultdict(list)
    for i,v in enumerate(VERTICES):
        sig=tuple(rows[k][i] for k in order); blocks[sig].append(v)
    return {"row_order":order,"blocks":[{"signature":"".join(sig),"vertices":vs} for sig,vs in sorted(blocks.items())]}

def main():
    screens={k:run_screen(k) for k in MODELS}
    promoted=[k for k,s in screens.items() if s["classification"] in {"SELECTIVE_PROMOTE","PARTIAL_SELECTIVE_PROMOTE"}]
    replicated_gptoss=screens["gptoss120"]["classification"] in {"SELECTIVE_PROMOTE","PARTIAL_SELECTIVE_PROMOTE"}
    cross_family_screen=len({MODELS[k]["family"] for k in promoted})>=2
    geoms={k:run_geometry(k) for k in MODELS} if cross_family_screen else {}
    evaluable=bool(geoms) and all(g["technical_evaluable"] for g in geoms.values())
    p43_rows={k:g["row"] for k,g in geoms.items()} if evaluable else {}
    pairwise_hamming=None; boundary_homology=None; q=None; persistent_core=[]; union_exceptional=[]; gptoss_replication=None
    if evaluable:
        pairwise_hamming=sum(a!=b for a,b in zip(p43_rows["gptoss120"],p43_rows["gemini"]))
        e_g=set(geoms["gptoss120"]["exceptional_vertices"]); e_m=set(geoms["gemini"]["exceptional_vertices"])
        boundary_homology={"exceptional_jaccard":len(e_g&e_m)/len(e_g|e_m) if e_g|e_m else 1.0,"boolean_cube_hausdorff":hausdorff(e_g,e_m)}
        gptoss_replication={"p42_to_p43_hamming":sum(a!=b for a,b in zip(P42_GPTOSS120_ROW,p43_rows["gptoss120"])),"p42_exceptional":sorted(P42_EXCEPTIONAL),"p43_exceptional":sorted(e_g),"exceptional_jaccard":len(P42_EXCEPTIONAL&e_g)/len(P42_EXCEPTIONAL|e_g) if P42_EXCEPTIONAL|e_g else 1.0,"boolean_cube_hausdorff":hausdorff(P42_EXCEPTIONAL,e_g)}
        persistent_core=[v for i,v in enumerate(VERTICES) if P42_GPTOSS120_ROW[i]=="0" and p43_rows["gptoss120"][i]=="0" and p43_rows["gemini"][i]=="0"]
        union_exceptional=[v for i,v in enumerate(VERTICES) if P42_GPTOSS120_ROW[i]=="1" or p43_rows["gptoss120"][i]=="1" or p43_rows["gemini"][i]=="1"]
        q=quotient({"p42_gptoss120":P42_GPTOSS120_ROW,"p43_gptoss120":p43_rows["gptoss120"],"p43_gemini":p43_rows["gemini"]})
    if evaluable: verdict="NONVACUOUS_CROSS_FAMILY_BEHAVIORAL_QUOTIENT_CONSTITUTED"
    elif cross_family_screen: verdict="CROSS_FAMILY_SELECTIVITY_REPLICATED_BUT_GEOMETRY_TECHNICALLY_UNEVALUABLE"
    elif replicated_gptoss: verdict="GPTOSS_SELECTIVITY_REPLICATED__CROSS_FAMILY_DOMAIN_NOT_REOPENED"
    else: verdict="P42_SELECTIVITY_NOT_REPLICATED"
    out={"stage":STAGE,"contracts_frozen_from_p42":CONTRACTS,"screens":screens,"promoted_models":promoted,"gptoss120_selectivity_replication":replicated_gptoss,"cross_family_screen_constituted":cross_family_screen,"geometries":geoms,"pairwise_hamming":pairwise_hamming,"gptoss120_p42_p43_replication":gptoss_replication,"cross_family_boundary_homology":boundary_homology,"persistent_selective_core":persistent_core,"union_exceptional_set":union_exceptional,"three_row_quotient":q,"constitutional_verdict":verdict,"authority":"Independent prospective behavioral replication under P42-frozen response contracts. Cross-family means observed model instances from distinct families, not a population-level family capability theorem; no neural-mechanism or behavioral-SVEC promotion claim."}
    p=Path("receipts/p43_result.json");p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding="utf-8")

if __name__=="__main__":main()
