from __future__ import annotations
import argparse,json
from collections import defaultdict
from pathlib import Path
from p24_packets import FAMILIES, hidden_key

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip(); return "NONE" if t.upper()=="NONE" else t

def correct(row,a):
    if row.get("status")!="OK": return False
    ans=row.get("parsed_response") or {}; ch=norm(ans.get("challenge"))
    if not a["expected_specific_criticism"]: return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")==a["oracle_intervention"] and ans.get("predicted_direction")==a["oracle_direction"]

def aggregate(receipt):
    key=hidden_key(); g=defaultdict(list)
    for r in receipt["rows"]: g[r["packet_id"]].append(r)
    packets=[]
    for pid,reps in g.items():
        a=key[pid]; ok=sum(r.get("status")=="OK" for r in reps); votes=sum(correct(r,a) for r in reps)
        packets.append({**a,"packet_id":pid,"ok_replicates":ok,"technically_evaluable":ok>=2,
                        "packet_correct":votes>=2,"format_or_api_failures":sum(r.get("status")!="OK" for r in reps)})
    fams={}
    for fam in FAMILIES:
        v=[p for p in packets if p["family"]==fam and p["semantic_class"]=="valid"]
        n=[p for p in packets if p["family"]==fam and p["semantic_class"]=="null"]
        vs=sum(p["packet_correct"] for p in v); fp=len(n)-sum(p["packet_correct"] for p in n)
        fams[fam]={"valid_success":vs,"null_false_positive":fp,"n":len(v),"selective_pass":vs>=2 and fp<=1}
    return {
        "model_key":receipt["model_key"],
        "arm_evaluable":all(p["technically_evaluable"] for p in packets),
        "families":fams,
        "format_or_api_failures":sum(p["format_or_api_failures"] for p in packets),
        "packets":packets,
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for k in ("qwen","gemini","gptoss"): ap.add_argument("--"+k,required=True)
    ap.add_argument("--out",required=True); a=ap.parse_args()
    models={k:aggregate(json.loads(Path(getattr(a,k)).read_text())) for k in ("qwen","gemini","gptoss")}
    evaluable=[m for m in models.values() if m["arm_evaluable"]]
    result={
      "stage":"EPISTEME-P24",
      "models":models,
      "rule":{
        "packet_correct":">=2/3 replicates",
        "arm_evaluable":"every packet has >=2 OK replicates",
        "family_selective_pass":"valid >=2/3 and null false-positive <=1/3",
        "technical_hold":"<2 evaluable models"
      },
      "program_level":{"evaluable_models":len(evaluable)},
      "authority":"Combine with frozen P23 regime maps to derive boundary normal forms and cross-model quotient classification; diagnostic only."
    }
    Path(a.out).write_text(json.dumps(result,indent=2))
