from __future__ import annotations
import argparse,json,torch
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from p39_common import PROMPT,SEEDS,screen_packets,parse_json,correct,classify_screen

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",required=True)
    a=ap.parse_args()

    q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_compute_dtype=torch.bfloat16)
    tok=AutoTokenizer.from_pretrained(a.model,trust_remote_code=True)
    model=AutoModelForCausalLM.from_pretrained(
        a.model,
        device_map="auto",
        quantization_config=q,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )

    rows=[]
    for item in screen_packets():
        for rep,seed in enumerate(SEEDS,1):
            torch.manual_seed(seed)
            try:
                messages=[{"role":"user","content":PROMPT+"\n\nARCHIVE:\n"+json.dumps(item["packet"],ensure_ascii=False)}]
                prompt=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
                inputs=tok(prompt,return_tensors="pt").to(model.device)
                with torch.no_grad():
                    ids=model.generate(
                        **inputs,
                        max_new_tokens=512,
                        do_sample=True,
                        temperature=0.6,
                        top_p=0.95,
                        pad_token_id=tok.eos_token_id,
                    )
                text=tok.decode(ids[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True)
                parsed=parse_json(text)
                ok=correct(parsed,item["semantic"])
                status="OK"
            except Exception as exc:
                parsed={"error":repr(exc)}
                ok=False
                status="FORMAT_OR_API_FAIL"
            rows.append({
              "case_id":item["case_id"],"vertex":item["vertex"],"semantic":item["semantic"],
              "replicate":rep,"seed":seed,"status":status,"correct":ok
            })
    out={"stage":"EPISTEME-P39","provider":"huggingface-job","model":a.model,"classification":classify_screen(rows),"rows":rows}
    print("P39_RESULT_JSON="+json.dumps(out,separators=(",",":")))

if __name__=="__main__":
    main()
