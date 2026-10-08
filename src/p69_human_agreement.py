"""P69 external HUMAN annotation agreement ledger, no model/provider calls.

Accepts independent human ratings on a fixed public case_id list.
No labels are filled from oracle. Cannot certify independent review when
the files are synthetic fixtures.
"""
from __future__ import annotations
import argparse,json,math,tempfile
from pathlib import Path

VALID=(True,False,None)

def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]

def compare(a,b):
    aa={z["case_id"]:z for z in a}
    bb={z["case_id"]:z for z in b}
    if len(aa)!=len(a) or len(bb)!=len(b) or set(aa)!=set(bb):raise ValueError("P69_MISMATCHED_ANNOTATOR_PANELS")
    paired=[]
    for case in sorted(aa):
        x,y=aa[case],bb[case]
        if x.get("challenge_exists") not in VALID or y.get("challenge_exists") not in VALID:
            raise ValueError("bad class")
        for row in (x,y):
            ids=row.get("rationale_ids",[])
            if not isinstance(ids,list) or any(not isinstance(q,str) for q in ids):raise ValueError("bad IDs")
        paired.append((x,y))
    n=len(paired)
    if n==0:raise ValueError("empty ratings")
    usable=[(x,y) for x,y in paired if x["challenge_exists"] is not None and y["challenge_exists"] is not None]
    unresolved=[x["case_id"] for x,y in paired if x["challenge_exists"] is None or y["challenge_exists"] is None
                or x["challenge_exists"]!=y["challenge_exists"]]
    m=len(usable)
    observed=sum(x["challenge_exists"]==y["challenge_exists"] for x,y in usable)/m if m else None
    kappa=None
    if m:
        a_yes=sum(x["challenge_exists"] is True for x,y in usable)/m
        b_yes=sum(y["challenge_exists"] is True for x,y in usable)/m
        pe=a_yes*b_yes+(1-a_yes)*(1-b_yes)
        if pe<1-1e-14:kappa=(observed-pe)/(1-pe)
    exact_refs=[set(x["rationale_ids"])==set(y["rationale_ids"]) for x,y in usable
                if x["challenge_exists"] is True and y["challenge_exists"] is True]
    return {"n_cases":n,"n_both_decidable":m,"disputed_or_unknown":len(unresolved),
            "unresolved_case_ids":unresolved,"challenge_agreement":observed,"cohen_kappa":kappa,
            "both_positive_rationale_exact_agreement":sum(exact_refs)/len(exact_refs) if exact_refs else None,
            "rationale_comparison_n":len(exact_refs),
            "blind_independence_claim":"NOT_AUTOMATIC: two externally recruited independent annotators required",
            "publication_annotation_gate":"PASS" if not unresolved and (kappa is not None and kappa>=0.70) else "HOLD",
            "provider_calls":0}

def self_test():
    agree=[{"case_id":str(i),"challenge_exists":i<5,"rationale_ids":["evidence"] if i<5 else []}
           for i in range(10)]
    z=compare(agree,agree)
    assert z["cohen_kappa"]==1 and z["publication_annotation_gate"]=="PASS"
    altered=json.loads(json.dumps(agree))
    altered[2]["challenge_exists"]=False
    z=compare(agree,altered)
    assert z["disputed_or_unknown"]==1 and z["publication_annotation_gate"]=="HOLD"
    z=compare([{"case_id":"only","challenge_exists":None,"rationale_ids":[]}],
              [{"case_id":"only","challenge_exists":False,"rationale_ids":[]}])
    assert z["cohen_kappa"] is None and z["publication_annotation_gate"]=="HOLD"
    identical=[{"case_id":str(i),"challenge_exists":False,"rationale_ids":[]} for i in range(4)]
    assert compare(identical,identical)["cohen_kappa"] is None
    print("P69_HUMAN_AGREEMENT_ALGORITHM_PASS kappa=1 discordance_hold=PASS degenerate_hold=PASS")
    print("NO_REAL_HUMAN_ANNOTATIONS_PRESENT provider_calls=0")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--annotator-a",required=True)
    p.add_argument("--annotator-b",required=True)
    p.add_argument("--out",required=True)
    v=p.parse_args()
    result=compare(read_jsonl(v.annotator_a),read_jsonl(v.annotator_b))
    path=Path(v.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(result["publication_annotation_gate"])

if __name__=="__main__":
    import sys
    self_test() if sys.argv[1:]==["--self-test"] else main()
