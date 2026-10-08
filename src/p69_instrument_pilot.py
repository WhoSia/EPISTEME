"""P69 prospective 192-slot measurement-only pilot; never run on git push.

Two bundles x two canary-only tasks x four R/T vertices x valid/null twins
x two response contracts x three independent invocations = 192 slots.

All model calls require manual workflow dispatch AFTER actual canary PASS.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,time
from pathlib import Path
from p69_task_factory import PILOT_TASKS,VERTICES,build,canonical_json
from p69_independent_scorer import score,oracle_response
from p69_provider_canary import MODEL_IDS,CHANNELS,groq_call,gemini_call

VERTEX_PILOT=tuple(x for x in VERTICES if not (set(x)-set("RT")))
SEMANTICS=("valid","null")
DRAWS=(1,2,3)
assert len(VERTEX_PILOT)==4

def identity_grid(model):
    if model not in MODEL_IDS:raise ValueError("P69_UNKNOWN_MODEL")
    grid=[(task,vertex,semantic,channel,draw)
          for task in PILOT_TASKS for vertex in VERTEX_PILOT
          for semantic in SEMANTICS for channel in CHANNELS for draw in DRAWS]
    assert len(grid)==96 and len(set(grid))==96
    random.Random(690069+list(MODEL_IDS).index(model)).shuffle(grid)
    return grid

def call_provider(model,channel,prompt,client=None):
    if model=="gptoss120":return groq_call(channel,prompt,client)
    return gemini_call(channel,prompt,client)

def run(model,offline=False):
    if model not in MODEL_IDS:raise ValueError(model)
    client=None
    if not offline:
        if model=="gptoss120":
            from groq import Groq
            client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=0)
        else:
            from google import genai
            from google.genai import types
            client=genai.Client(api_key=os.environ["GEMINI_API_KEY"],
                http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)))
    out=[]
    for task,vertex,semantic,channel,draw in identity_grid(model):
        packet=build(task,vertex,semantic)
        canonical=canonical_json(packet)
        prompt=("You are reviewing a retained scientific evidence archive. "
                "Using only the archive, assess whether the focus-object terminal sufficiency claim "
                "is contradicted by an admissible u1 intervention. Do not invent facts. "
                "If no contradiction is justified, answer NONE. Return exactly one JSON object "
                "with keys challenge, intervention, predicted_direction, rationale_ids. "
                "Include only indispensable evidence_id values; do not add extraneous IDs.\n\nARCHIVE:\n"
                +canonical)
        start=time.monotonic_ns()
        raw=None;version=None;error_type=None;provider_status="RESPONSE"
        try:
            raw,version=(oracle_response(packet),MODEL_IDS[model]) if offline else call_provider(model,channel,prompt,client)
            evaluation=score(packet,raw)
        except Exception as exc:
            provider_status="PROVIDER_FAILURE";error_type=type(exc).__name__
            evaluation=score(packet,None)
        out.append({
            "model":model,"model_requested":MODEL_IDS[model],
            "model_reported":version,"task":task,"vertex":"".join(vertex) or "I",
            "semantic":semantic,"channel":channel,"draw":draw,
            "packet_sha256":hashlib.sha256(canonical.encode()).hexdigest(),
            "prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),
            "provider_status":provider_status,"error_type":error_type,
            "raw_response":raw,"latency_ms":(time.monotonic_ns()-start)/1e6,
            **evaluation,
            "server_seed_sent":False,"client_request_retry_policy":"Groq max_retries=0; Gemini HttpRetryOptions(attempts=1) explicit",
            "pilot_only":True
        })
    assert len(out)==96
    return {"stage":"EPISTEME-P69","kind":"INSTRUMENTATION_PILOT",
            "model_bundle":model,"mode":"SYNTHETIC_ORACLE_FIXTURE" if offline else "ACTUAL_PROVIDER",
            "calls_ceiling":96,"rows":out,
            "authority":"MEASUREMENT ONLY: cannot estimate publishable effect from this pilot."}

def self_test():
    from collections import defaultdict
    assert set(VERTEX_PILOT)=={(),("R",),("T",),("R","T")}
    for model in MODEL_IDS:
        doc=run(model,offline=True)
        assert doc["mode"]=="SYNTHETIC_ORACLE_FIXTURE"
        assert len(doc["rows"])==96
        matches=defaultdict(set);prompts=defaultdict(set)
        for row in doc["rows"]:
            key=(row["task"],row["vertex"],row["semantic"],row["draw"])
            matches[key].add((row["channel"],row["packet_sha256"]))
            prompts[key].add(row["prompt_sha256"])
            assert row["format_valid"] and row["semantic_correct"] is True
        assert len(matches)==48
        assert all({x[0] for x in s}==set(CHANNELS) and len({x[1] for x in s})==1 for s in matches.values())
        assert all(len(s)==1 for s in prompts.values())
    print("P69_PILOT_OFFLINE_PASS model_slots=192 provider_calls=0 paired_prompts=96")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--model",choices=tuple(MODEL_IDS))
    parser.add_argument("--out")
    parser.add_argument("--offline",action="store_true")
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:self_test()
    else:
        if not args.model or not args.out:parser.error("--model --out are mandatory")
        doc=run(args.model,args.offline)
        path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n")
        print("P69_PILOT_BATCH_WRITTEN",args.model,"slots",len(doc["rows"]))
