# /// script
# dependencies = ["transformers>=4.55","torch>=2.7","accelerate>=1.5","bitsandbytes>=0.46","huggingface_hub>=0.34"]
# ///
from __future__ import annotations
import gc,json,torch
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig

MODELS=[
 "Qwen/Qwen2.5-7B-Instruct",
 "Qwen/Qwen3-4B",
 "Qwen/Qwen3-8B",
 "Qwen/Qwen3-14B",
]
SEEDS=(3901,3902,3903)
PROMPT=(
 "You are reviewing a scientific archive and an incumbent sufficiency claim. "
 "Using only the retained information in this archive, propose the single strongest "
 "experiment that could falsify the claim. Do not invent missing variables, relations, or measurements. "
 "If the archive does not justify a specific falsifying experiment, return NONE. "
 "Return only a JSON object with exactly these keys: challenge, intervention, predicted_direction, rationale_ids."
)
CASES=(
 ("S01","I","valid"),("S02","I","null"),("S03","R","valid"),("S04","R","null"),
 ("S05","H_T_L","valid"),("S06","H_T_L","null"),("S07","R_F_H","valid"),("S08","R_F_H","null"),
 ("S09","R_F_T_L","valid"),("S10","R_F_T_L","null"),("S11","R_F_H_T_L","valid"),("S12","R_F_H_T_L","null"),
)

def packet(cid,label,semantic):
    v=set() if label=="I" else set(label.split("_"))
    renamed="R" in v; filler="F" in v; rh="H" in v; wl="T" in v; rr="L" in v
    key="zeta39-source" if renamed else "k39-source"
    alt=key+"-alt"; fills=["q9","q4"] if filler else ["p2","p3"]
    def tr(t): return [*fills,t] if wl else [t,*fills]
    ha={"history":"h39-a","trace":tr(key)}; hb={"history":"h39-b","trace":tr(alt)}
    histories=[hb,ha] if rh else [ha,hb]
    target={"source":key,"intervention":"u1","response_link":"history-sensitive" if semantic=="valid" else "history-invariant"}
    dist={"source":"decoy-z" if renamed else "distractor-c","intervention":"uX","response_link":"irrelevant"}
    relations=[dist,target] if rr else [target,dist]
    return {
      "archive_id":"p39-screen-"+cid.lower(),
      "claim":"The retained terminal summary is sufficient to predict the challenge response.",
      "terminal_observation":{"h39-a":"T=stable","h39-b":"T=stable"},
      "available_interventions":["u1","uX","uY"],
      "instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.",
      "surface_domain":"measurement-pipeline","retained_history":histories,"relation_notes":relations,
    }

def parse(text):
    t=text.strip()
    try:o=json.loads(t)
    except Exception:
        i=t.find("{")
        if i<0: raise
        o,_=json.JSONDecoder().raw_decode(t[i:])
    if not isinstance(o,dict): raise ValueError("not object")
    return o

def correct(o,semantic):
    ch=o.get("challenge")
    if semantic=="null": return ch is None or str(ch).strip().upper()=="NONE"
    return ch is not None and str(ch).strip().upper()!="NONE" and o.get("intervention")=="u1" and o.get("predicted_direction")=="different"

def classify(rows):
    by={}
    for r in rows: by.setdefault((r["case_id"],r["semantic"]),[]).append(r)
    vo=no=0
    for (_c,s),rs in by.items():
        maj=sum(x["correct"] for x in rs)>=2
        if s=="valid": vo+=int(maj)
        else:no+=int(maj)
    if sum(r["status"]=="OK" for r in rows)<len(rows)-2:return "TECHNICAL_UNEVALUABLE"
    if vo==0 and no>=5:return "GLOBAL_ABSTENTION_REGIME"
    if vo>=4 and no>=5:return "SELECTIVE_PROMOTE"
    if vo>=2 and no>=4:return "PARTIAL_SELECTIVE_PROMOTE"
    return "NONSELECTIVE_NO_PROMOTION"

def run_model(mid):
    q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_compute_dtype=torch.bfloat16)
    tok=AutoTokenizer.from_pretrained(mid,trust_remote_code=True)
    model=AutoModelForCausalLM.from_pretrained(mid,device_map="auto",quantization_config=q,torch_dtype=torch.bfloat16,trust_remote_code=True)
    rows=[]
    for cid,label,semantic in CASES:
        p=packet(cid,label,semantic)
        for rep,seed in enumerate(SEEDS,1):
            torch.manual_seed(seed)
            try:
                msg=[{"role":"user","content":PROMPT+"\n\nARCHIVE:\n"+json.dumps(p,ensure_ascii=False)}]
                s=tok.apply_chat_template(msg,tokenize=False,add_generation_prompt=True,enable_thinking=False)
                inp=tok(s,return_tensors="pt").to(model.device)
                with torch.no_grad():
                    ids=model.generate(**inp,max_new_tokens=384,do_sample=True,temperature=0.6,top_p=0.95,pad_token_id=tok.eos_token_id)
                txt=tok.decode(ids[0][inp["input_ids"].shape[1]:],skip_special_tokens=True)
                o=parse(txt); ok=correct(o,semantic); status="OK"
            except Exception as exc:
                ok=False; status="FORMAT_OR_API_FAIL"
            rows.append({"case_id":cid,"vertex":label,"semantic":semantic,"replicate":rep,"seed":seed,"status":status,"correct":ok})
    out={"model":mid,"classification":classify(rows),"rows":rows}
    del model,tok
    gc.collect(); torch.cuda.empty_cache()
    return out

all_results=[]
for mid in MODELS:
    try: all_results.append(run_model(mid))
    except Exception as exc: all_results.append({"model":mid,"classification":"TECHNICAL_UNEVALUABLE","fatal_error":repr(exc),"rows":[]})
print("P39_MULTI_RESULT_JSON="+json.dumps({"stage":"EPISTEME-P39","provider":"huggingface-job","models":all_results},separators=(",",":")))
