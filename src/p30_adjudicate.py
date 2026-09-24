from __future__ import annotations
import argparse,json
from collections import defaultdict
from pathlib import Path
from p30_design import PROSPECTIVE_WORLDS,VERTICES,VERTEX_ORDER,PREDICTED_FAILURE_ROWS,hidden_key,label

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip(); return "NONE" if t.upper()=="NONE" else t

def correct(row,a):
    if row.get("status")!="OK": return False
    ans=row.get("parsed_response") or {}; ch=norm(ans.get("challenge"))
    if not a["expected_specific_criticism"]: return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")==a["oracle_intervention"] and ans.get("predicted_direction")==a["oracle_direction"]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--gemini",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    receipt=json.loads(Path(a.gemini).read_text(encoding="utf-8")); key=hidden_key(); g=defaultdict(list)
    for r in receipt["rows"]: g[r["packet_id"]].append(r)
    packets={}
    technical=True; failures=0
    for pid,reps in g.items():
        audit=key[pid]; ok=sum(r.get("status")=="OK" for r in reps); votes=sum(correct(r,audit) for r in reps)
        technical &= ok>=2; failures += sum(r.get("status")!="OK" for r in reps)
        packets[pid]={**audit,"ok_replicates":ok,"packet_correct":votes>=2}
    cells=[]; rows={}
    exact=True
    for w in PROSPECTIVE_WORLDS:
        observed_bits=[]; predicted=PREDICTED_FAILURE_ROWS[w.world_id]
        matches=0
        for i,v in enumerate(VERTICES):
            valid=packets[next(pid for pid,x in packets.items() if x["world_id"]==w.world_id and x["vertex"]==label(v) and x["semantic_class"]=="valid")]
            null=packets[next(pid for pid,x in packets.items() if x["world_id"]==w.world_id and x["vertex"]==label(v) and x["semantic_class"]=="null")]
            observed_pass=valid["packet_correct"] and null["packet_correct"]
            predicted_pass=predicted[i]=="0"
            match=observed_pass==predicted_pass
            exact &= match; matches += int(match); observed_bits.append("0" if observed_pass else "1")
            cells.append({"world_id":w.world_id,"vertex":label(v),"predicted_pass":predicted_pass,"observed_pass":observed_pass,"match":match})
        rows[w.world_id]={"predicted_failure_row":predicted,"observed_failure_row":"".join(observed_bits),"matching_cells":matches,"n":32,"exact_row_match":matches==32}
    if not technical: verdict="TECHNICAL_HOLD"
    elif exact: verdict="PROSPECTIVE_ADDITIVE_GEOMETRY_SURVIVES"
    else: verdict="ADDITIVE_GEOMETRY_DEFEATED_INTERACTION_REQUIRED"
    result={
      "stage":"EPISTEME-P30","model":"gemini","arm_evaluable":technical,
      "balanced_crossing":{"complete_3x4_after_run":True,"fresh_worlds":6,"geometry_cells":192},
      "world_rows":rows,
      "exact_cell_matches":sum(c["match"] for c in cells),"total_cells":192,
      "all_192_match":exact if technical else None,
      "program_verdict":verdict,
      "format_or_api_failures":failures,
      "authority":"Exact prospective test of the P29 GF(2) additive skin+intervention geometry law on the six previously unobserved cells of the complete 3x4 crossing. Survival does not establish a universal causal law; failure requires context interaction within the tested design. No behavioral SVEC promotion."
    }
    Path(a.out).write_text(json.dumps(result,indent=2),encoding="utf-8")
if __name__=="__main__": main()
