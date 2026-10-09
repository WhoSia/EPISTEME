"""All-attempt P69-R1 64-slot calibration judge, fail closed."""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from p69_provider_canary import MODEL_IDS,CHANNELS
from p69_measurement_repair import VERSIONS,SEMANTICS,DRAWS,PILOT_TASKS,REPAIR_PROTOCOL,run,prompt_for
from p69_task_factory import build,canonical_json


def analyze(root):
    docs=[]
    for f in Path(root).rglob("*.json"):
        try:x=json.loads(f.read_text())
        except (ValueError,OSError):continue
        if x.get("kind")=="PAIRED_MEASUREMENT_REPAIR":docs.append(x)
    if len(docs)!=2 or {d.get("model_bundle") for d in docs}!=set(MODEL_IDS):
        raise ValueError("P69_REPAIR_MISSING_OR_DUPLICATED_BUNDLE")
    arms={}
    for d in docs:
        model=d["model_bundle"]
        if d["protocol"]!=REPAIR_PROTOCOL or d["mode"]!="ACTUAL_PROVIDER" or len(d["rows"])!=32:
            raise ValueError("P69_REPAIR_BAD_SOURCE_OR_COUNT")
        ids={}
        for r in d["rows"]:
            k=(r["task"],r["semantic"],r["version"],r["channel"],r["draw"])
            if k in ids:raise ValueError("P69_REPAIR_DUPLICATE_ID")
            ids[k]=r
        expected={(t,s,v,c,n) for t in PILOT_TASKS for s in SEMANTICS for v in VERSIONS
                  for c in CHANNELS for n in DRAWS}
        if set(ids)!=expected:raise ValueError("P69_REPAIR_MISSING_CELL")
        for (task,semantic,version,channel,draw),row in ids.items():
            pkt=build(task,(),semantic)
            if row["packet_sha256"]!=hashlib.sha256(canonical_json(pkt).encode()).hexdigest():
                raise ValueError("P69_REPAIR_PACKET_CHANGED")
            if row["prompt_sha256"]!=hashlib.sha256(prompt_for(pkt,version).encode()).hexdigest():
                raise ValueError("P69_REPAIR_PROMPT_CHANGED")
            if row["model_requested"]!=MODEL_IDS[model]:
                raise ValueError("P69_REPAIR_MODEL_SUBSTITUTED")
            other=ids[(task,semantic,version,CHANNELS[1-CHANNELS.index(channel)],draw)]
            if row["prompt_sha256"]!=other["prompt_sha256"]:
                raise ValueError("P69_REPAIR_CHANNEL_PROMPTS_DIFFER")
        local={}
        for version in VERSIONS:
            by_channel={}
            for channel in CHANNELS:
                sample=[r for r in d["rows"] if r["version"]==version and r["channel"]==channel]
                assert len(sample)==8
                format_valid=sum(r["format_valid"] is True for r in sample)
                provider_responses=sum(r["provider_status"]=="RESPONSE" for r in sample)
                valid_positive=sum(r["semantic_correct"] is True for r in sample if r["semantic"]=="valid")
                null_correct=sum(r["semantic_correct"] is True for r in sample if r["semantic"]=="null")
                grounded=sum(r["semantic_correct"] is True for r in sample)
                by_channel[channel]={
                    "calls":8,"provider_responses":provider_responses,"format_valid":format_valid,
                    "valid_positive_grounded":valid_positive,"null_grounded":null_correct,
                    "grounded_total":grounded,
                    "reasons":dict(collections.Counter(r["reason"] for r in sample)),
                    "technical_gate":provider_responses==8 and format_valid>=7,
                    "balanced_signal_gate":valid_positive>=1 and null_correct>=1,
                }
            local[version]=by_channel
        arms[model]=local
    repaired=[arms[m]["procedure_v1"][c] for m in MODEL_IDS for c in CHANNELS]
    ready=all(x["technical_gate"] and x["balanced_signal_gate"] for x in repaired)
    comparative={model:{channel:{
        "format_valid_diff":arms[model]["procedure_v1"][channel]["format_valid"]-arms[model]["frozen_v0"][channel]["format_valid"],
        "positive_grounded_diff":arms[model]["procedure_v1"][channel]["valid_positive_grounded"]-arms[model]["frozen_v0"][channel]["valid_positive_grounded"],
        "null_grounded_diff":arms[model]["procedure_v1"][channel]["null_grounded"]-arms[model]["frozen_v0"][channel]["null_grounded"],
    } for channel in CHANNELS} for model in MODEL_IDS}
    return {
        "stage":"EPISTEME-P69","kind":"PAIRED_MEASUREMENT_REPAIR_VERDICT",
        "protocol":REPAIR_PROTOCOL,"provider_slots":64,
        "verdict":"CALIBRATION_SIGNAL_PRESENT" if ready else "REPAIR_MEASUREMENT_HOLD",
        "arms":arms,"paired_descriptive_deltas":comparative,
        "claim_ceiling":"Noninferential calibration. No scientific transport inference, no 192/8192 automatic promotion.",
        "new_provider_calls_authorized":False,
    }


def self_test():
    with tempfile.TemporaryDirectory() as td:
        for m in MODEL_IDS:
            doc=run(m,offline=True)
            doc["mode"]="ACTUAL_PROVIDER"
            Path(td,m+".json").write_text(json.dumps(doc))
        yes=analyze(td)
        assert yes["verdict"]=="CALIBRATION_SIGNAL_PRESENT"
        bad=json.loads(Path(td,"gemini.json").read_text())
        for row in bad["rows"]:
            if row["version"]=="procedure_v1" and row["semantic"]=="valid":
                row["semantic_correct"]=False
        Path(td,"gemini.json").write_text(json.dumps(bad))
        no=analyze(td)
        assert no["verdict"]=="REPAIR_MEASUREMENT_HOLD"
        bad["rows"][0]["prompt_sha256"]="corrupted"
        Path(td,"gemini.json").write_text(json.dumps(bad))
        try:analyze(td)
        except ValueError as e:assert "PROMPT_CHANGED" in str(e)
        else:raise AssertionError("P69_BROKEN_PROMPT_NOT_CAUGHT")
    print("P69_REPAIR_ANALYZER_SELFTEST_PASS green_red=PASS prompt_guard=PASS calls=0")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root")
    p.add_argument("--out")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.root or not a.out:p.error("--root/--out required")
        verdict=analyze(a.root)
        dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(verdict,indent=2)+"\n")
        print("P69_"+verdict["verdict"])
        if verdict["verdict"]!="CALIBRATION_SIGNAL_PRESENT":raise SystemExit(2)
