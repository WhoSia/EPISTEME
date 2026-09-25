from __future__ import annotations
import argparse,json,os
from pathlib import Path
from groq import Groq
from p39_common import PROMPT,SEEDS,screen_packets,parse_json,correct,classify_screen

TEMPERATURE=0.6
TOP_P=0.95
MAXTOK=512

def list_qwen(client):
    return sorted(m.id for m in client.models.list().data if "qwen" in m.id.lower())

def call(client,model,packet,seed):
    kwargs={
      "model":model,
      "messages":[{"role":"user","content":PROMPT+"\n\nARCHIVE:\n"+json.dumps(packet,ensure_ascii=False)}],
      "temperature":TEMPERATURE,
      "top_p":TOP_P,
      "seed":seed,
      "max_completion_tokens":MAXTOK,
      "stream":False,
    }
    try:
        kwargs["reasoning_format"]="hidden"
        resp=client.chat.completions.create(**kwargs)
    except Exception:
        kwargs.pop("reasoning_format",None)
        resp=client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content or ""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=2)
    models=list_qwen(client)
    result={}
    for model in models:
        rows=[]
        for item in screen_packets():
            for rep,seed in enumerate(SEEDS,1):
                try:
                    parsed=parse_json(call(client,model,item["packet"],seed))
                    ok=correct(parsed,item["semantic"])
                    status="OK"
                except Exception as exc:
                    ok=False
                    status="FORMAT_OR_API_FAIL"
                    parsed={"error":repr(exc)}
                rows.append({
                  "case_id":item["case_id"],"vertex":item["vertex"],"semantic":item["semantic"],
                  "replicate":rep,"seed":seed,"status":status,"correct":ok
                })
        result[model]={"classification":classify_screen(rows),"rows":rows}
    out={"stage":"EPISTEME-P39","provider":"groq","discovered_qwen_models":models,"models":result}
    p=Path(a.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
