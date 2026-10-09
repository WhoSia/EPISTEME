"""P70 R1 adversarial hypothesis court: existing 64 paid rows, ZERO model calls.

Requires both ORIGINAL ACTUAL_PROVIDER ledgers. Observed score contrasts are
finite-sample descriptive; rivals concern possible mechanisms, not diagnoses.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,tempfile
from pathlib import Path

BUNDLES=("gemini","gptoss120")
PROMPTS=("frozen_v0","procedure_v1")
CHANNELS=("strict_schema","json_object")
TASKS=("provenance_0","transformation_0")
SEMANTICS=("valid","null")
DRAWS=(1,2)

def load(root):
    found={}
    for path in Path(root).rglob("*.json"):
        try:d=json.loads(path.read_text())
        except (OSError,ValueError):continue
        if d.get("kind")!="PAIRED_MEASUREMENT_REPAIR" or d.get("mode")!="ACTUAL_PROVIDER":
            continue
        key=d.get("model_bundle")
        if key not in BUNDLES or key in found:raise ValueError("P70_DUPLICATE_OR_UNKNOWN_PROVIDER_LEDGER")
        if len(d.get("rows",[]))!=32:raise ValueError("P70_MISSING_PROVIDER_ROWS")
        found[key]=d
    if set(found)!=set(BUNDLES):raise ValueError("P70_PAIRED_REAL_BUNDLES_INCOMPLETE")
    return found

def analyze(found):
    result={"kind":"P70_GEMINI_CONTRACT_RIVAL_COURT",
            "source_run_id":37931512662,"original_model_calls":64,
            "additional_model_calls":0,"source_authority":"FROZEN_EXPLORATORY_TWO_TASK_TWO_DRAW_LEDGER"}
    by_model={}
    expected={(task,semantic,prompt,channel,draw)
        for task in TASKS for semantic in SEMANTICS for prompt in PROMPTS
        for channel in CHANNELS for draw in DRAWS}
    for name in BUNDLES:
        d=found[name]
        if d.get("mode")!="ACTUAL_PROVIDER":raise ValueError("P70_SYNTHETIC_MEASURED_AS_REAL")
        rows=d["rows"]; index={}
        for r in rows:
            k=(r["task"],r["semantic"],r["version"],r["channel"],r["draw"])
            if k in index:raise ValueError("P70_DUPLICATED_PAIR")
            index[k]=r
            if r["provider_status"]!="RESPONSE":raise ValueError("P70_PROVIDER_FAILURE_UNRECOVERED")
        if set(index)!=expected:raise ValueError("P70_UNBALANCED_GRID")
        model_stats={}
        model_versions=sorted({str(r.get("model_reported")) for r in rows})
        for version in PROMPTS:
            by_channel={}
            for channel in CHANNELS:
                subgroup=[r for r in rows if r["version"]==version and r["channel"]==channel]
                assert len(subgroup)==8
                by_channel[channel]={
                    "format_valid":sum(r["format_valid"] is True for r in subgroup),
                    "answer_correct":sum(r["answer_correct"] is True for r in subgroup),
                    "minimal_witness_correct":sum(r["semantic_correct"] is True for r in subgroup),
                    "positive_grounded":sum(r["semantic_correct"] is True for r in subgroup if r["semantic"]=="valid"),
                    "null_grounded":sum(r["semantic_correct"] is True for r in subgroup if r["semantic"]=="null"),
                    "positive_wrong_answer":sum(r["reason"]=="ANSWER_WRONG" for r in subgroup if r["semantic"]=="valid"),
                    "positive_witness_only_fail":sum(r["reason"]=="NONMINIMAL_OR_WRONG_WITNESS" for r in subgroup if r["semantic"]=="valid"),
                    "by_task_positive":{task:sum(r["semantic_correct"] is True for r in subgroup
                         if r["semantic"]=="valid" and r["task"]==task) for task in TASKS},
                    "failure_reasons":dict(sorted(collections.Counter(r["reason"] for r in subgroup).items()))
                }
                for r in subgroup:
                    sibling=index[(r["task"],r["semantic"],r["version"],
                                   CHANNELS[1-CHANNELS.index(channel)],r["draw"])]
                    if r["prompt_sha256"]!=sibling["prompt_sha256"]:
                        raise ValueError("P70_CHANNEL_PROMPT_MISMATCH")
                    # This is not a reproducible same-seed paired sample;
                    # equal prompts do not establish equivalent decoded outputs.
            model_stats[version]=by_channel
        change_strict=(model_stats["procedure_v1"]["strict_schema"]["positive_grounded"] -
                       model_stats["frozen_v0"]["strict_schema"]["positive_grounded"])
        change_json=(model_stats["procedure_v1"]["json_object"]["positive_grounded"] -
                     model_stats["frozen_v0"]["json_object"]["positive_grounded"])
        by_model[name]={
            "model_versions_reported":model_versions,
            "cells":model_stats,
            "positive_prompt_change_strict_numerator_over_four":change_strict,
            "positive_prompt_change_json_numerator_over_four":change_json,
            "json_minus_strict_prompt_change_interaction_numerator_over_four":change_json-change_strict,
        }
    g=by_model["gemini"];r=g["cells"]["procedure_v1"]
    assert (r["strict_schema"]["positive_grounded"],r["json_object"]["positive_grounded"])==(0,4)
    assert all(v==0 for v in r["strict_schema"]["by_task_positive"].values())
    assert all(v==2 for v in r["json_object"]["by_task_positive"].values())
    assert g["json_minus_strict_prompt_change_interaction_numerator_over_four"]==6
    result["bundles"]=by_model
    result["rivals"]=[
        {"id":"H1","claim":"Response-contract-specific decoding/selection interacts with identical explicit procedure.",
         "observed":"SUPPORTS_INTERACTION_DESCRIPTION_ONLY",
         "discriminator":"Hold task and prompt bytes fixed; compare channel manipulation with multiple randomized invocation blocks, observe output token/finish diagnostics."},
        {"id":"H2","claim":"General instruction-induced conservatism suppresses all positive judgments independently of contract.",
         "observed":"CONTRADICTED_AS_CONTRACT_INVARIANT_EXPLANATION",
         "discriminator":"Investigate valid-positive abstentions and null false alarms separately; enforce nonabstention against a neutral positive oracle only in a new preregistration."},
        {"id":"H3","claim":"One task family intrinsically caused all Gemini failures.",
         "observed":"CONTRADICTED_AS_SINGLE_FAMILY_EXPLANATION_FOR_PROCEDURE_V1",
         "discriminator":"Replicate in genuinely independent provenance and transformation topologies, not same-compiler twins."},
        {"id":"H4","claim":"Strict failures arise purely from evidence-minimality scoring or malformed JSON.",
         "observed":"CONTRADICTED_FOR_GEMINI_PROCEDURE_STRICT_POSITIVE_ROWS",
         "discriminator":"Require separate answer direction, minimal witness and format endpoints (current strict positive all ANSWER_WRONG)."},
        {"id":"H5","claim":"Stochastic sampling/order or a time/context shift generated the apparent sign reversal.",
         "observed":"NOT_EXCLUDED",
         "discriminator":"Randomize order/blocking; freeze model version and decoding controls; increase independent claims, not draws alone."},
        {"id":"H6","claim":"Prompt x contract x provider API interaction arises from schema semantics, token budget or hidden reasoning regime.",
         "observed":"NOT_IDENTIFIED",
         "discriminator":"Prespecified cross-provider schema-equivalence controls, response finish reasons, token budgets and independent schemas."},
    ]
    result["forward_claim_ceiling"]="RIVAL_PRIORITY_ONLY_NOT_CAUSAL_MEDIATION_NOT_TRANSPORT_NOT_P69_REPAIR_PASS"
    return result

def self_test():
    rows={}
    for model in BUNDLES:
        rr=[]
        for task in TASKS:
            for semantic in SEMANTICS:
                for version in PROMPTS:
                    for draw in DRAWS:
                        packet="h"+hashlib.sha256((task+semantic+version).encode()).hexdigest()
                        for channel in CHANNELS:
                            # Synthetic fixture mirrors the vulnerable P69 Gemini cells.
                            g=(model=="gemini")
                            valid=not g or semantic=="null" or (version=="procedure_v1" and channel=="json_object") or (version=="frozen_v0" and channel=="strict_schema" and task=="provenance_0")
                            rr.append({"task":task,"semantic":semantic,"version":version,
                                "channel":channel,"draw":draw,"provider_status":"RESPONSE",
                                "prompt_sha256":packet,"format_valid":True,
                                "answer_correct":valid,"semantic_correct":valid,
                                "reason":"MINIMAL_GROUNDED" if valid else "ANSWER_WRONG",
                                "model_reported":"MOCK"})
        rows[model]={"kind":"PAIRED_MEASUREMENT_REPAIR","mode":"ACTUAL_PROVIDER",
                     "model_bundle":model,"rows":rr}
    result=analyze(rows)
    assert result["bundles"]["gemini"]["json_minus_strict_prompt_change_interaction_numerator_over_four"]==6
    with tempfile.TemporaryDirectory() as td:
        for model in BUNDLES:
            Path(td,model+".json").write_text(json.dumps(rows[model]))
            d=dict(rows[model]);d["mode"]="OFFLINE_FIXTURE"
            Path(td,"mock_"+model+".json").write_text(json.dumps(d))
        recovered=load(td)
        assert len(recovered)==2
        broken=rows["gemini"]["rows"][0]
        original=broken["prompt_sha256"];broken["prompt_sha256"]="drift"
        try:analyze(rows)
        except ValueError as e:assert "PROMPT_MISMATCH" in str(e)
        else:raise AssertionError("P70_FORGED_SAME_PROMPT_ACCEPTED")
        broken["prompt_sha256"]=original
    print("P70_R1_RIVALS_SELFTEST_PASS synthetic_layout_only=PASS real_calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root");p.add_argument("--out");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.root or not a.out:p.error("--root/--out mandatory")
        z=analyze(load(a.root))
        path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(z,indent=2,ensure_ascii=False)+"\n")
        print("P70_R1_RIVAL_COURT_PASS real_rows=64 gemini_positive_interaction_numerator=6 denominator=4 paid_calls=0")
