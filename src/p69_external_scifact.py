"""P69 SciFact external ecology adapter — schema verified, data NOT bundled.

SciFact CONTRADICT annotations identify published evidence rationale sentences.
Removing an annotated rationale does NOT prove semantic NONE; human review is
mandatory before using a withheld-evidence twin as a null ground truth.

This script only reads user-supplied SciFact claims/corpus JSONL files.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

SOURCE="Wadden et al. (EMNLP 2020) SciFact"
SOURCE_SCHEMA="https://github.com/allenai/scifact/blob/master/doc/data.md"

def digest(*parts):
    return hashlib.sha256(("P69|SCIFACT|"+("|".join(map(str,parts)))).encode()).hexdigest()

def ingest(path):
    with open(path,encoding="utf-8") as fd:
        for line in fd:
            if line.strip():yield json.loads(line)

def evidence_rationales(claim,corpus):
    result=[]
    for doc_id,anns in claim.get("evidence",{}).items():
        doc=corpus.get(str(doc_id))
        if not doc:continue
        abstract=doc.get("abstract",[])
        if not isinstance(abstract,list):continue
        for ann in anns:
            if ann.get("label")!="CONTRADICT":continue
            ix=ann.get("sentences",[])
            if not ix or len(ix)>3 or not all(isinstance(i,int) and 0<=i<len(abstract) for i in ix):continue
            if not all(isinstance(abstract[i],str) and abstract[i].strip() for i in ix):continue
            result.append((str(doc_id),tuple(sorted(set(ix))),tuple(abstract[i] for i in ix)))
    return sorted(set(result))

def prepare(claims,corpus,max_claims=16):
    if max_claims<=0:raise ValueError("invalid cap")
    candidates=[]
    for claim in claims:
        if not isinstance(claim.get("id"),int) or not isinstance(claim.get("claim"),str):continue
        rationale=evidence_rationales(claim,corpus)
        if not rationale:continue
        candidates.append((digest(claim["id"]),claim,rationale[0]))
    candidates.sort(key=lambda x:x[0])
    rows=[];sealed=[]
    for _,claim,(doc,indices,sentences) in candidates[:max_claims]:
        for rename in (False,True):
            for reorder in (False,True):
                for retained in ("gold_attested","gold_withheld"):
                    rows_visible=[]
                    for i,text in zip(indices,sentences):
                        if retained=="gold_withheld" and i==indices[-1]:continue
                        eid=("sid-"+digest(claim["id"],doc,i,"renamed" if rename else "original")[:12])
                        rows_visible.append({"evidence_id":eid,"source_document":doc,"sentence_index":i,"text":text})
                    if reorder:rows_visible.reverse()
                    case_id="P69EXT-"+digest(claim["id"],rename,reorder,retained)[:18]
                    rows.append({"case_id":case_id,"claim":claim["claim"],"evidence":rows_visible,
                        "instructions":"Judge ONLY supplied evidence; do not use memorized facts or retrieve other documents. Cite exact evidence IDs.",
                        "source_task":"Scientific claim verification","annotation_label":None})
                    sealed.append({"case_id":case_id,"scifact_claim_id":claim["id"],"original_gold":"CONTRADICT",
                        "projected_gold_status":retained,"rationale_indices":indices,
                        "claim_of_semantic_null":"NOT_AUTHORIZED",
                        "needs_independent_annotation":True})
    assert len(rows)==len(sealed)==8*min(max_claims,len(candidates))
    assert len({r["case_id"] for r in rows})==len(rows)
    return rows,sealed

def self_test():
    corpus={"10":{"doc_id":10,"abstract":["Evidence alpha.","Evidence beta.","Distractor."]}}
    claims=[{"id":7,"claim":"A scientific claim","evidence":{"10":[{"label":"CONTRADICT","sentences":[0,1]}]}}]
    public,key=prepare(claims,corpus,max_claims=1)
    assert len(public)==len(key)==8
    assert all("CONTRADICT" not in json.dumps(x) for x in public)
    for a in public:
        assert len(a["evidence"]) in (1,2)
        assert a["annotation_label"] is None
    assert all(z["needs_independent_annotation"] and z["claim_of_semantic_null"]=="NOT_AUTHORIZED" for z in key)
    print("P69_SCIFACT_SCHEMA_PASS cases=8 labeled_semantic_null=0 provider_calls=0")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--claims",required=True)
    ap.add_argument("--corpus",required=True)
    ap.add_argument("--max-claims",type=int,default=16)
    ap.add_argument("--public",required=True)
    ap.add_argument("--sealed",required=True)
    args=ap.parse_args()
    corpus={str(z["doc_id"]):z for z in ingest(args.corpus) if "doc_id" in z}
    public,sealed=prepare(ingest(args.claims),corpus,args.max_claims)
    for destination,records in ((args.public,public),(args.sealed,sealed)):
        path=Path(destination);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text("".join(json.dumps(z,ensure_ascii=False)+"\n" for z in records),encoding="utf-8")
    print("P69_EXTERNAL_SCIFACT_IMPORTED cases="+str(len(public))+" human_null_adjudication=REQUIRED")

if __name__=="__main__":
    self_test() if __import__("sys").argv[1:]==["--self-test"] else main()
