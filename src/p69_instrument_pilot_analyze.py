"""P69 all-attempt instrumentation pilot readiness, no hypothesis test."""
from __future__ import annotations
import argparse,hashlib,json,collections
from pathlib import Path
from p69_provider_canary import MODEL_IDS,CHANNELS
from p69_instrument_pilot import PILOT_TASKS,VERTEX_PILOT,SEMANTICS,DRAWS,build,canonical_json

def analyze(root):
    docs=[]
    for f in Path(root).rglob("*.json"):
        try:z=json.loads(f.read_text())
        except (ValueError,OSError):continue
        if z.get("stage")=="EPISTEME-P69" and z.get("kind")=="INSTRUMENTATION_PILOT":docs.append(z)
    if len(docs)!=2 or {z["model_bundle"] for z in docs}!=set(MODEL_IDS):
        raise ValueError("P69_PILOT_MISSING_OR_DUPLICATED_BUNDLE")
    results={}
    for z in docs:
        if z["mode"]!="ACTUAL_PROVIDER" or len(z["rows"])!=96:raise ValueError("P69_PILOT_BAD_MODE_OR_ROWS")
        model=z["model_bundle"]
        got={}
        for row in z["rows"]:
            k=(row["task"],row["vertex"],row["semantic"],row["channel"],row["draw"])
            if k in got:raise ValueError("duplicate P69 pilot identity")
            got[k]=row
        for task in PILOT_TASKS:
            for vertex in VERTEX_PILOT:
                v="".join(vertex) or "I"
                for semantic in SEMANTICS:
                    packet=build(task,vertex,semantic)
                    canonical=canonical_json(packet)
                    h=hashlib.sha256(canonical.encode()).hexdigest()
                    for channel in CHANNELS:
                        for draw in DRAWS:
                            k=(task,v,semantic,channel,draw)
                            if k not in got:raise ValueError("missing P69 pilot identity")
                            row=got[k]
                            if row["packet_sha256"]!=h or row["model_requested"]!=MODEL_IDS[model]:
                                raise ValueError("P69 packet/model substitution")
                            other=got[(task,v,semantic,CHANNELS[1-CHANNELS.index(channel)],draw)]
                            if row["prompt_sha256"]!=other["prompt_sha256"]:
                                raise ValueError("P69 response contract prompt mismatch")
        by={}
        for channel in CHANNELS:
            local=[x for x in z["rows"] if x["channel"]==channel]
            assert len(local)==48
            provider=sum(x["provider_status"]=="RESPONSE" for x in local)
            valid=sum(x["format_valid"] is True for x in local)
            executable=sum(x["semantic_correct"] is True and x["format_valid"] for x in local)
            valid_positive=sum(x["semantic_correct"] is True for x in local if x["semantic"]=="valid")
            null_correct=sum(x["semantic_correct"] is True for x in local if x["semantic"]=="null")
            answer=sum(x["answer_correct"] is True for x in local)
            by[channel]={"calls":48,"provider_responses":provider,"format_valid":valid,
                "strict_grounded_correct":executable,
                "answer_direction_correct":answer,
                "grounded_valid_positive":valid_positive,"grounded_null_correct":null_correct,
                "selection_unknown":48-valid,
                "contract_technical_gate":provider>=36 and valid>=36,
                "positive_negative_signal_gate":valid_positive>=1 and null_correct>=1}
        results[model]=by
    technical=all(v["contract_technical_gate"] for by in results.values() for v in by.values())
    signal=all(v["positive_negative_signal_gate"] for by in results.values() for v in by.values())
    verdict="MEASUREMENT_PILOT_READY" if technical and signal else (
      "TECHNICAL_PILOT_HOLD" if not technical else "GLOBAL_ABSTENTION_OR_NONSELECTIVE_HOLD")
    return {"stage":"EPISTEME-P69","kind":"P69_PILOT_MEASUREMENT_RESULT",
        "verdict":verdict,"provider_invocation_slots":192,"arms":results,
        "provider_observability":"All-call executable correctness, technical failures NOT treated as latent semantic errors.",
        "claim_ceiling":"Measurement feasibility ONLY. Does not authorize confirmatory 8192-call main study.",
        "main_study_precommit_still_pending":True}

def self_test():
    import tempfile
    from p69_instrument_pilot import run
    with tempfile.TemporaryDirectory() as td:
        # Synthetic data are converted to ACTUAL_PROVIDER mode only for parser tests,
        # and this simulated outcome is NEVER a hosted scientific receipt.
        for model in MODEL_IDS:
            d=run(model,offline=True)
            d["mode"]="ACTUAL_PROVIDER"
            Path(td,model+".json").write_text(json.dumps(d))
        x=analyze(td)
        assert x["verdict"]=="MEASUREMENT_PILOT_READY"
        assert x["provider_invocation_slots"]==192
        assert all(v["calls"]==48 for by in x["arms"].values() for v in by.values())
        d=json.loads(Path(td,"gemini.json").read_text())
        d["rows"][0]["prompt_sha256"]="corrupted"
        Path(td,"gemini.json").write_text(json.dumps(d))
        try:analyze(td)
        except ValueError as exc:assert "prompt mismatch" in str(exc)
        else:raise AssertionError("P69_PROMPT_MISMATCH_NOT_CAUGHT")
    print("P69_PILOT_AGGREGATOR_SELFTEST_PASS fixture=192 provider_calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root")
    p.add_argument("--out")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.root or not a.out:p.error("--root and --out required")
        doc=analyze(a.root)
        target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(doc,indent=2)+"\n")
        print("P69_"+doc["verdict"])
