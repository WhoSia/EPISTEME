"""P69 two-bundle API response-contract feasibility receipt.

Fail-closed on missing or duplicate model bundles. Not a scientific result.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from p69_provider_canary import MODEL_IDS,CHANNELS,source_receipt

def inspect(directory):
    root=Path(directory)
    data=[]
    for path in root.rglob("*.json"):
        try:obj=json.loads(path.read_text())
        except (OSError,ValueError):continue
        if obj.get("stage")=="EPISTEME-P69" and obj.get("kind")=="PROVIDER_CONTRACT_CANARY":
            data.append(obj)
    if {z["model_bundle"] for z in data}!=set(MODEL_IDS) or len(data)!=len(MODEL_IDS):
        raise ValueError("P69_CANARY_INCOMPLETE_OR_DUPLICATED_BUNDLE")
    results={}
    for rec in data:
        if rec["mode"]!="ACTUAL_PROVIDER" or len(rec["observations"])!=2:
            raise ValueError("P69_CANARY_NOT_REAL_TWO_CONTRACT")
        if set(z["channel"] for z in rec["observations"])!=set(CHANNELS):
            raise ValueError("P69_CANARY_WRONG_CONTRACT")
        for row in rec["observations"]:
            if row["prompt_sha256"]!=source_receipt()["prompt_sha256"]:
                raise ValueError("P69_CANARY_PROMPT_DRIFT")
            if row["schema_sha256"]!=source_receipt()["schema_sha256"]:
                raise ValueError("P69_CANARY_SCHEMA_DRIFT")
            if row["requested_model_id"]!=MODEL_IDS[rec["model_bundle"]]:
                raise ValueError("P69_CANARY_MODEL_SUBSTITUTION")
        results[rec["model_bundle"]]={
            "n_contracts":2,"valid":sum(x["schema_and_canary_valid"] for x in rec["observations"]),
            "errors":[{"channel":x["channel"],"error_type":x["error_type"],
                        "redacted_diagnostic":x.get("error_diagnostic")}
                      for x in rec["observations"] if not x["schema_and_canary_valid"]],
            "model_metadata_diagnostic":rec.get("model_metadata_diagnostic"),
            "requested":MODEL_IDS[rec["model_bundle"]],
            "observed_versions":sorted(set(str(x["returned_model_version"]) for x in rec["observations"]))}
    ok=all(z["valid"]==2 for z in results.values())
    return {"stage":"EPISTEME-P69","kind":"PROVIDER_CONTRACT_CANARY_SUMMARY",
            "verdict":"MEASUREMENT_CONTRACT_READY" if ok else "TECHNICAL_CONTRACT_HOLD",
            "logical_invocation_slots":4,"bundles":results,
            "permissions":"Read-only artifact; no repository writeback",
            "paper_science_authority":"NONE, API canary only. Does not authorize 192-call pilot or 8192-call main."}

def self_test():
    import tempfile
    from p69_provider_canary import run as canary_run
    with tempfile.TemporaryDirectory() as root:
        for name in MODEL_IDS:
            doc=canary_run(name,offline=True)
            doc["mode"]="ACTUAL_PROVIDER" # Only a regression fixture; NOT a live receipt.
            Path(root,name+".json").write_text(json.dumps(doc))
        assert inspect(root)["verdict"]=="MEASUREMENT_CONTRACT_READY"
        x=json.loads(Path(root,"gemini.json").read_text())
        x["observations"][0]["schema_and_canary_valid"]=False
        x["observations"][0]["error_type"]="ClientError"
        x["observations"][0]["error_diagnostic"]={"exception_type":"ClientError","http_status":403,"failure_category":"AUTH_OR_PERMISSION"}
        Path(root,"gemini.json").write_text(json.dumps(x))
        verdict=inspect(root)
        assert verdict["verdict"]=="TECHNICAL_CONTRACT_HOLD"
        assert verdict["bundles"]["gemini"]["errors"][0]["redacted_diagnostic"]["http_status"]==403
    print("P69_CANARY_ANALYZER_PASS success_case=PASS hold_case=PASS provider_calls=0")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root")
    p.add_argument("--out")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:return self_test()
    if not args.root or not args.out:p.error("--root and --out required")
    summary=inspect(args.root)
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(summary,indent=2)+"\n")
    print("P69_"+summary["verdict"])
    if summary["verdict"]!="MEASUREMENT_CONTRACT_READY":
        raise SystemExit(2) # Verdict artifact uploaded by workflow if:always(); FAIL is real failure.
if __name__=="__main__":main()
