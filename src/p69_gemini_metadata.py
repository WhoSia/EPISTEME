"""P69 Gemini metadata diagnostic. ONE non-generative models.get request.
Runs only in a read-only GitHub Action, never sends a model prompt.
"""
from __future__ import annotations
import json,os,sys
from pathlib import Path
from p69_provider_canary import MODEL_IDS,gemini_metadata_probe

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        report={"stage":"EPISTEME-P69","kind":"GEMINI_METADATA_DIAGNOSTIC",
                "status":"MISSING_KEY","model_id":MODEL_IDS["gemini"]}
    else:
        z=gemini_metadata_probe(offline=False)
        report={"stage":"EPISTEME-P69","kind":"GEMINI_METADATA_DIAGNOSTIC",**z,
                "requested_model":MODEL_IDS["gemini"],"generation_calls":0,
                "test_scope":"Model lookup/auth/availability ONLY; JSON response contract untested"}
    p=Path("receipts/p69_gemini_metadata.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("P69_GEMINI_METADATA_"+report["status"])
    if report["status"]!="MODEL_GET_SUCCESS":raise SystemExit(2)
if __name__=="__main__":main()
