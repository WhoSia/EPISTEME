from __future__ import annotations
import gc,json,torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from p39_common import PROMPT,SEEDS,screen_packets,parse_json,correct,classify_screen

MODELS=[
 "Qwen/Qwen2.5-0.5B-Instruct",
 "Qwen/Qwen2.5-1.5B-Instruct",
 "Qwen/Qwen3-0.6B",
 "Qwen/Qwen3-1.7B",
]

def run_one(mid):
    tok=AutoTokenizer.from_pretrained(mid,trust_remote_code=True)
    model=AutoModelForCausalLM.from_pretrained(
        mid,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    ).to("cpu")
    model.eval()
    rows=[]
    for item in screen_packets():
        for rep,seed in enumerate(SEEDS,1):
            torch.manual_seed(seed)
            try:
                msg=[{"role":"user","content":PROMPT+"\n\nARCHIVE:\n"+json.dumps(item["packet"],ensure_ascii=False)}]
                kwargs={"tokenize":False,"add_generation_prompt":True}
                if mid.startswith("Qwen/Qwen3-"): kwargs["enable_thinking"]=False
                prompt=tok.apply_chat_template(msg,**kwargs)
                inp=tok(prompt,return_tensors="pt")
                with torch.no_grad():
                    ids=model.generate(
                        **inp,
                        max_new_tokens=256,
                        do_sample=True,
                        temperature=0.6,
                        top_p=0.95,
                        pad_token_id=tok.eos_token_id,
                    )
                txt=tok.decode(ids[0][inp["input_ids"].shape[1]:],skip_special_tokens=True)
                parsed=parse_json(txt)
                ok=correct(parsed,item["semantic"])
                status="OK"
            except Exception as exc:
                ok=False
                status="FORMAT_OR_API_FAIL"
            rows.append({
              "case_id":item["case_id"],"vertex":item["vertex"],"semantic":item["semantic"],
              "replicate":rep,"seed":seed,"status":status,"correct":ok
            })
    out={"model":mid,"classification":classify_screen(rows),"rows":rows}
    del model,tok
    gc.collect()
    return out

def main():
    out=[]
    for mid in MODELS:
        try:
            out.append(run_one(mid))
        except Exception as exc:
            out.append({"model":mid,"classification":"TECHNICAL_UNEVALUABLE","fatal_error":repr(exc),"rows":[]})
    from pathlib import Path
    p=Path("receipts/p39_cpu_qwen_screen.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps({"stage":"EPISTEME-P39","provider":"github-cpu","models":out},indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
