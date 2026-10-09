"""P69-R1: predeclared 64-slot paired measurement-contract repair.

A calibration experiment, not a confirmatory behavioral or cross-task test.
2 bundles x 2 pilot tasks x 2 semantics x 2 channels x 2 prompt
versions x 2 independent draws. Integrated fresh canary is separate (4).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import time
from pathlib import Path

from p69_instrument_pilot import call_provider
from p69_task_factory import PILOT_TASKS, build, canonical_json
from p69_independent_scorer import score, oracle_response
from p69_provider_canary import MODEL_IDS, CHANNELS

VERSIONS=("frozen_v0","procedure_v1")
SEMANTICS=("valid","null")
DRAWS=(1,2)
VERTEX=()
REPAIR_PROTOCOL="P69-R1-20261009"


def prompt_for(packet, version):
    original=("You are reviewing a retained scientific evidence archive. "
              "Using only the archive, assess whether the focus-object terminal sufficiency claim "
              "is contradicted by an admissible u1 intervention. Do not invent facts. "
              "If no contradiction is justified, answer NONE. Return exactly one JSON object "
              "with keys challenge, intervention, predicted_direction, rationale_ids. "
              "Include only indispensable evidence_id values; do not add extraneous IDs.\n\nARCHIVE:\n"
              +canonical_json(packet))
    if version=="frozen_v0":
        return original
    if version!="procedure_v1":
        raise ValueError("P69_REPAIR_UNKNOWN_VERSION")
    procedure=(
        "Review procedure: (1) trace only focus_object, never a decoy; "
        "(2) compare its retained terminal observation with the explicitly justified "
        "u1 response, including every necessary provenance, transition, gate, or calibration link; "
        "(3) terminal stability by itself does not establish the u1 response; "
        "(4) choose a refutation only if the linked u1 response is different; "
        "(5) for a justified refutation return challenge as a non-NONE string, "
        "intervention exactly u1, predicted_direction exactly different, "
        "and the IDs of one complete inclusion-minimal supporting evidence set; "
        "(6) if no complete justification exists, return challenge NONE, "
        "intervention null, predicted_direction null, rationale_ids []; "
        "(7) predicted_direction must be one of the exact tokens same, different or null. "
        "Return valid JSON with exactly the four specified keys. "
        "Do not infer what the intended gold label is from this procedure.\n\n"
    )
    return procedure+original


def grid(model):
    if model not in MODEL_IDS:
        raise ValueError("P69_REPAIR_UNKNOWN_BUNDLE")
    cases=[(task,semantic,version,channel,draw)
           for task in PILOT_TASKS for semantic in SEMANTICS
           for version in VERSIONS for channel in CHANNELS for draw in DRAWS]
    assert len(cases)==32
    random.Random(690170+list(MODEL_IDS).index(model)).shuffle(cases)
    return cases


def run(model,offline=False):
    client=None
    if not offline:
        if model=="gptoss120":
            from groq import Groq
            client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=0)
        else:
            from google import genai
            from google.genai import types
            client=genai.Client(
                api_key=os.environ["GEMINI_API_KEY"],
                http_options=types.HttpOptions(
                    retry_options=types.HttpRetryOptions(attempts=1)))
    rows=[]
    for task,semantic,version,channel,draw in grid(model):
        packet=build(task,VERTEX,semantic)
        prompt=prompt_for(packet,version)
        start=time.monotonic_ns()
        provider_status="RESPONSE"
        error_type=None
        reported_model=None
        try:
            raw,reported_model=((oracle_response(packet),MODEL_IDS[model]) if offline
                                else call_provider(model,channel,prompt,client))
            result=score(packet,raw)
        except Exception as exc:
            provider_status="PROVIDER_FAILURE"
            error_type=type(exc).__name__
            result=score(packet,None)
        rows.append({
            "task":task,"semantic":semantic,"version":version,"channel":channel,
            "draw":draw,"model_bundle":model,"model_requested":MODEL_IDS[model],
            "model_reported":reported_model,
            "provider_status":provider_status,"error_type":error_type,
            "packet_sha256":hashlib.sha256(canonical_json(packet).encode()).hexdigest(),
            "prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),
            "elapsed_ms":(time.monotonic_ns()-start)/1e6,
            **result,
        })
    return {"stage":"EPISTEME-P69","kind":"PAIRED_MEASUREMENT_REPAIR",
            "protocol":REPAIR_PROTOCOL,"mode":"OFFLINE_FIXTURE" if offline else "ACTUAL_PROVIDER",
            "model_bundle":model,"maximum_calls":32,"rows":rows,
            "claims":"Calibration only; baseline/repair effects not confirmatory."}


def self_test():
    for model in MODEL_IDS:
        x=run(model,offline=True)
        assert len(x["rows"])==32
        assert len({(r["task"],r["semantic"],r["version"],r["channel"],r["draw"]) for r in x["rows"]})==32
        assert all(r["semantic_correct"] is True for r in x["rows"])
        for task in PILOT_TASKS:
            for semantic in SEMANTICS:
                packet=build(task,VERTEX,semantic)
                for version in VERSIONS:
                    p=prompt_for(packet,version)
                    same=[r for r in x["rows"] if (r["task"],r["semantic"],r["version"])==(task,semantic,version)]
                    assert len(same)==4 and len({r["prompt_sha256"] for r in same})==1
                    assert same[0]["prompt_sha256"]==hashlib.sha256(p.encode()).hexdigest()
    assert prompt_for(build(PILOT_TASKS[0],(),SEMANTICS[0]),VERSIONS[0]).startswith("You are reviewing")
    print("P69_REPAIR_WORKER_SELFTEST_PASS paired_slots=64 provider_calls=0")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--model",choices=tuple(MODEL_IDS))
    p.add_argument("--out")
    p.add_argument("--offline",action="store_true")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.model or not a.out:p.error("--model and --out required")
        doc=run(a.model,a.offline)
        target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(doc,indent=2)+"\n")
        print("P69_REPAIR_WORKER_FINISHED model="+a.model+" slots="+str(len(doc["rows"])))
