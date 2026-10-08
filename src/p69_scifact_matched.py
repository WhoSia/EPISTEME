"""P69 SciFact evidence-budget matched external contrast.

Independently annotated CONTRADICT rationale vs same-document non-rationale
sentences, with identical COUNT but not certified semantic equivalence.
This never asserts the non-annotated arm lacks contradicting evidence.
"""
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path
from p69_external_scifact import ingest,evidence_rationales,digest

def select_decoy_sentences(abstract,gold_ids):
    needed=len(gold_ids)
    gold_text=[abstract[i] for i in gold_ids]
    goal=sum(len(x) for x in gold_text)
    choices=[i for i,x in enumerate(abstract) if i not in gold_ids and isinstance(x,str) and x.strip()
             and x not in gold_text]
    if len(choices)<needed:return None
    # Deterministically select same-count distractors with minimal character-length imbalance.
    limit=choices[:30]
    sets=itertools.combinations(limit,needed)
    return min(sets,key=lambda ss:(abs(sum(len(abstract[i]) for i in ss)-goal),ss),default=None)

def compile_cases(claims,corpus,max_claims=16):
    candidate=[]
    for cl in claims:
        if not isinstance(cl.get("id"),int) or not isinstance(cl.get("claim"),str):continue
        for doc,ix,gold in evidence_rationales(cl,corpus):
            abstract=corpus[doc]["abstract"]
            decoy=select_decoy_sentences(abstract,ix)
            if decoy is not None:
                candidate.append((digest(cl["id"],doc),cl,doc,ix,decoy))
                break
    candidate.sort(key=lambda z:z[0])
    if len(candidate)<max_claims:raise ValueError("P69_SCIFACT_MATCHED_ELIGIBLE_LT_TARGET")
    public,private=[],[]
    for _,cl,doc,ix,decoy in candidate[:max_claims]:
        for arm,positions in (("annotated_contradiction",ix),("same_doc_unannotated",decoy)):
            for renamed in (False,True):
                for reversed_order in (False,True):
                    ids=list(positions)
                    if reversed_order:ids.reverse()
                    evidence=[{"evidence_id":"e"+digest(cl["id"],doc,pos,"R" if renamed else "I")[:16],
                               "text":corpus[doc]["abstract"][pos]} for pos in ids]
                    case_id="P69SCIFACTMATCH-"+digest(cl["id"],arm,renamed,reversed_order)[:16]
                    public.append({"case_id":case_id,"claim":cl["claim"],"evidence":evidence,
                        "instruction":"Assess claim using only visible evidence. Cite indispensable IDs; abstain if evidence is inconclusive.",
                        "annotation":{"challenge_exists":None,"rationale_ids":[]}})
                    private.append({"case_id":case_id,"claim_id":cl["id"],"doc_id":doc,
                        "source_annotation_status":arm,"sentence_indices":ids,
                        "semantic_abstention_certified":False,
                        "human_annotation_required":True})
    assert len(public)==len(private)==max_claims*2*2*2
    for j in range(0,len(public),8):
        records=public[j:j+8];source=private[j:j+8]
        assert len({len(r["evidence"]) for r in records})==1
        assert len({r["claim"] for r in records})==1
        for arm in ("annotated_contradiction","same_doc_unannotated"):
            sel=[records[i] for i in range(8) if source[i]["source_annotation_status"]==arm]
            assert len(sel)==4
            assert len({tuple(sorted(e["text"] for e in r["evidence"])) for r in sel})==1
    return public,private

def self_test():
    corp={"1":{"abstract":["A contradictory one.","A contradictory two.",
          "Ordinary observation alpha.","Ordinary observation beta.","Additional observations."]}}
    claims=[{"id":4,"claim":"Test fact","evidence":{"1":[{"label":"CONTRADICT","sentences":[0,1]}]}}]
    rows,key=compile_cases(claims,corp,1)
    assert len(rows)==len(key)==8
    assert all(len(row["evidence"])==2 for row in rows)
    assert all("semantic_abstention_certified" not in row for row in rows)
    assert not any(k["semantic_abstention_certified"] for k in key)
    print("P69_SCIFACT_MATCHED_SCHEMA_PASS 8_cases equal_evidence_count=PASS null_truth=HOLD")

if __name__=="__main__":
    import sys
    if sys.argv[1:]==["--self-test"]:self_test()
    else:
        p=argparse.ArgumentParser()
        p.add_argument("--claims",required=True);p.add_argument("--corpus",required=True)
        p.add_argument("--out",required=True);p.add_argument("--private",required=True)
        p.add_argument("--n",type=int,default=16)
        a=p.parse_args()
        corp={str(d["doc_id"]):d for d in ingest(a.corpus)}
        data,key=compile_cases(ingest(a.claims),corp,a.n)
        for name,rows in ((a.out,data),(a.private,key)):
            target=Path(name);target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rows))
        print("P69_SCIFACT_MATCHED_SOURCE_PASS cases="+str(len(data))+" semantic_null=HOLD")
