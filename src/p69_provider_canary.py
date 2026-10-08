"""P69 bounded provider-contract canary. Exactly four potential model calls.
No scientific inference or main/pilot promotion. No SDK automatic retries.
"""
from __future__ import annotations
import argparse,hashlib,json,os,time
from pathlib import Path

from p42_reopen import SCHEMA,CANARY,CANARY_PROMPT

MODEL_IDS={"gptoss120":"openai/gpt-oss-120b","gemini":"gemini-3.5-flash-lite"}
CHANNELS=("strict_schema","json_object")
P69_CANARY_SCHEMA=SCHEMA

def prompt_text():
    return CANARY_PROMPT+" Return JSON and only JSON."

def source_receipt():
    prompt=prompt_text()
    return {"prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),
            "schema_sha256":hashlib.sha256(json.dumps(P69_CANARY_SCHEMA,sort_keys=True).encode()).hexdigest(),
            "prompt_identical_across_channel":True}

def groq_call(channel,prompt):
    from groq import Groq
    kwargs={"model":MODEL_IDS["gptoss120"],"messages":[{"role":"user","content":prompt}],
            "temperature":0.2,"top_p":0.95,"max_completion_tokens":1536,"stream":False,
            "reasoning_effort":"medium","reasoning_format":"hidden"}
    if channel=="strict_schema":
        kwargs["response_format"]={"type":"json_schema","json_schema":{
            "name":"episteme_p69_canary","strict":True,"schema":P69_CANARY_SCHEMA}}
    else:kwargs["response_format"]={"type":"json_object"}
    response=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=0).chat.completions.create(**kwargs)
    return response.choices[0].message.content or "",getattr(response,"model",MODEL_IDS["gptoss120"])

def gemini_call(channel,prompt):
    from google import genai
    from google.genai import types
    config={"temperature":0.2,"top_p":0.95,"max_output_tokens":1536,
            "response_mime_type":"application/json"}
    if channel=="strict_schema":config["response_json_schema"]=P69_CANARY_SCHEMA
    result=genai.Client(api_key=os.environ["GEMINI_API_KEY"]).models.generate_content(
        model=MODEL_IDS["gemini"],contents=prompt,config=types.GenerateContentConfig(**config))
    return result.text or "",getattr(result,"model_version",MODEL_IDS["gemini"])

def offline_fake(model,channel,prompt):
    assert model in MODEL_IDS and channel in CHANNELS
    return json.dumps(CANARY),MODEL_IDS[model]

def run(model,offline=False):
    if model not in MODEL_IDS:raise ValueError("unsupported model bundle")
    prompt=prompt_text()
    rows=[]
    for channel in CHANNELS:
        start=time.monotonic_ns()
        error=None;raw=None;seen_model=None;valid=False
        try:
            raw,seen_model=(offline_fake(model,channel,prompt) if offline
                            else groq_call(channel,prompt) if model=="gptoss120"
                            else gemini_call(channel,prompt))
            parsed=json.loads(raw)
            valid=(parsed==CANARY)
        except Exception as exc:
            error=type(exc).__name__
        rows.append({"model_bundle":model,"requested_model_id":MODEL_IDS[model],
                     "returned_model_version":seen_model,"channel":channel,
                     "api_invocation_attempted":not offline and bool(os.environ.get("GROQ_API_KEY" if model=="gptoss120" else "GEMINI_API_KEY")),
                     "response_received":raw is not None,
                     "schema_and_canary_valid":valid,"error_type":error,
                     "raw_response_sha256":hashlib.sha256(raw.encode()).hexdigest() if raw is not None else None,
                     "elapsed_ms":(time.monotonic_ns()-start)/1e6,
                     **source_receipt()})
    assert len(rows)==2
    return {"stage":"EPISTEME-P69","kind":"PROVIDER_CONTRACT_CANARY",
            "mode":"PROVIDER_FREE_FIXTURE" if offline else "ACTUAL_PROVIDER",
            "model_bundle":model,"calls_ceiling":2,"observations":rows,
            "provider_invocation_slots":0 if offline else 2,
            "contract_pass":all(x["schema_and_canary_valid"] for x in rows),
            "authority":"API contract feasibility only; no scientific task, no causal or behavioral claims."}

def self_test():
    z={k:run(k,offline=True) for k in MODEL_IDS}
    assert sum(v["provider_invocation_slots"] for v in z.values())==0
    assert all(v["contract_pass"] for v in z.values())
    assert all(v["observations"][0]["prompt_sha256"]==v["observations"][1]["prompt_sha256"] for v in z.values())
    assert len({x["channel"] for v in z.values() for x in v["observations"]})==2
    print("P69_PROVIDER_CANARY_OFFLINE_PASS actual_model_calls=0 prospective_calls=4")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--model",choices=tuple(MODEL_IDS))
    p.add_argument("--out")
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--offline",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.model or not a.out:p.error("--model and --out required unless --self-test")
        report=run(a.model,offline=a.offline)
        target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
        print("P69_PROVIDER_CANARY_"+("PASS" if report["contract_pass"] else "TECHNICAL_HOLD")
              +" model="+a.model+" requests="+str(report["provider_invocation_slots"]))
