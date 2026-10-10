"""P69-A1 prospective independent-original-claim and independent scorer handoff.

Select eight source-annotated SciFact dev claims outside P70's FOUR selected
claim/document clusters. Their source labels are only a sealed comparison,
NOT independent gold for the projected packet or minimal evidence witness.
Publish only source hashes/counts; raw review material stays private in CI.
"""
from __future__ import annotations
import argparse,collections,hashlib,json
from pathlib import Path
from p69_external_scifact import ingest
from p70_external_source_pilot import (load_source,FROZEN_DEV_SHA256,
                                       FROZEN_CORPUS_SHA256)

LABELS=("SUPPORT","CONTRADICT")
def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,
                                  separators=(",",":")).encode()).hexdigest()
def _candidates(claims,corpus):
    for c in claims:
        if not isinstance(c.get("id"),int) or not isinstance(c.get("claim"),str):
            continue
        anns=[]
        for docid,objects in c.get("evidence",{}).items():
            doc=corpus.get(str(docid))
            if not doc or not isinstance(doc.get("abstract"),list):continue
            sentences=doc["abstract"]
            for ann in objects:
                idx=ann.get("sentences",[])
                if ann.get("label") not in LABELS or not isinstance(idx,list) or not idx:
                    continue
                if any(not isinstance(i,int) or i<0 or i>=len(sentences) or
                       not isinstance(sentences[i],str) or not sentences[i].strip()
                       for i in idx):continue
                selected=sorted(set(idx))
                decoys=[i for i,s in enumerate(sentences)
                        if i not in selected and isinstance(s,str) and s.strip()]
                if not decoys:continue
                anns.append((ann["label"],str(docid),selected,min(decoys)))
        if len({a[0] for a in anns})!=1 or not anns:continue
        label,doc,idx,decoy=sorted(anns,key=lambda a:(a[1],a[2],a[3]))[0]
        yield {"id":c["id"],"claim":c["claim"],"label":label,
               "docid":doc,"indices":idx,"decoy":decoy}

def compile_handoff(claim_path,corpus_path):
    originals,c,source=load_source(claim_path,corpus_path)
    excluded_claim={claim["id"] for claim,_ in originals}
    excluded_doc={ann[1] for _,ann in originals}
    claims=list(ingest(claim_path))
    allc=list(_candidates(claims,c))
    groups={label:[] for label in LABELS}
    for row in allc:
        if row["id"] not in excluded_claim and row["docid"] not in excluded_doc:
            groups[row["label"]].append(row)
    chosen=[];used_docs=set(excluded_doc)
    for label in LABELS:
        for row in sorted(groups[label],key=lambda a:digest(str(a["id"]))):
            if row["docid"] in used_docs:continue
            chosen.append(row);used_docs.add(row["docid"])
            if sum(x["label"]==label for x in chosen)==4:break
    if len(chosen)!=8 or collections.Counter(x["label"] for x in chosen)!={"SUPPORT":4,"CONTRADICT":4}:
        raise ValueError("P69_NOT_EIGHT_DISTINCT_EXTERNAL_ORIGINAL_CLAIM_DOC_CLUSTERS")
    if any(x["id"] in excluded_claim or x["docid"] in excluded_doc for x in chosen):
        raise ValueError("P69_HOLDOUT_LEAK_P70_CLAIM_OR_DOCUMENT")
    public=[];sealed=[]
    for row in chosen:
        abstract=c[row["docid"]]["abstract"]
        positions=row["indices"]+[row["decoy"]]
        evidence=[{"evidence_id":"q"+digest([row["id"],row["docid"],i])[:12],
                   "text":abstract[i]} for i in positions]
        case_id="P69_EXTERNAL_"+digest([row["id"],row["docid"]])[:15]
        packet={"case_id":case_id,"claim":row["claim"],"evidence":evidence,
                "instructions":"Evaluate using ONLY shown evidence. Cite indispensable evidence IDs; mark insufficiency or ambiguity explicitly."}
        public.append(packet)
        sealed.append({"case_id":case_id,"packet_sha256":digest(packet),
          "source_claim_id":row["id"],"source_document_id":row["docid"],
          "original_annotation_label_SEALED":row["label"],
          "available_ids":[x["evidence_id"] for x in evidence],
          "annotation_indices_SEALED":row["indices"]})
    if len({p["case_id"] for p in public})!=8:raise ValueError("P69_DUPLICATE_HOLDOUT_PACKET")
    return public,sealed,source,excluded_claim,excluded_doc

def reviewer_schema(public,sealed,reviewer):
    import random
    order=list(public);random.Random(107 if reviewer=="A" else 401).shuffle(order)
    mapping={row["case_id"]:row for row in sealed}
    return ({"role":"P69_INDEPENDENT_EXTERNAL_SOURCE_SCORER","reviewer_assignment":reviewer,
      "source_label_visible":False,"model_replies_visible":False,
      "cases":order},
      {"role":"P69_EXTERNAL_SCORER_RESPONSE","reviewer_id":"REPLACE_WITH_REAL_PSEUDONYM",
       "independent_of_author_and_model":False,
       "judgments":[{"case_id":x["case_id"],"packet_sha256":mapping[x["case_id"]]["packet_sha256"],
                     "verdict":None,"indispensable_evidence_ids":[],
                     "answer_adequacy":None,"ambiguity_flags":[],
                     "reason":""} for x in order]})

def review_verdict(public,sealed,ra=None,rb=None):
    if ra is None or rb is None:
        return {"verdict":"P69_INDEPENDENT_SCORER_HOLD",
                "expected_reviewers":2,"actual_reviewers":0,
                "target_claim_clusters":8,"scorer_judgments":0}
    reviewer_ids=[x.get("reviewer_id") for x in (ra,rb)]
    if (any(not isinstance(x,str) or len(x.strip())<3 or x.startswith("REPLACE_") for x in reviewer_ids)
        or len(set(reviewer_ids))!=2
        or not all(x.get("independent_of_author_and_model") is True for x in (ra,rb))):
        raise ValueError("P69_NOT_INDEPENDENT_DISTINCT_REVIEWERS")
    ref={x["case_id"]:x for x in sealed}
    case_ids=set(ref)
    for review in (ra,rb):
        judgments=review.get("judgments",[])
        if len(judgments)!=8 or {x.get("case_id") for x in judgments}!=case_ids:
            raise ValueError("P69_SCORER_INCOMPLETE_OR_DUPLICATE")
        for j in judgments:
            old=ref[j["case_id"]]
            if j.get("packet_sha256")!=old["packet_sha256"]:
                raise ValueError("P69_SCORER_PACKET_DRIFT")
            if j.get("verdict") not in ("SUPPORT","CONTRADICT","INSUFFICIENT","AMBIGUOUS"):
                raise ValueError("P69_SCORER_BAD_VERDICT")
            selected=j.get("indispensable_evidence_ids")
            if (not isinstance(selected,list) or len(selected)!=len(set(selected))
                or not set(selected).issubset(old["available_ids"])):
                raise ValueError("P69_SCORER_BAD_EVIDENCE_WITNESS")
            if j["verdict"] in LABELS and not selected:
                raise ValueError("P69_POSITIVE_WITHOUT_WITNESS")
            if not isinstance(j.get("reason"),str) or len(j["reason"].strip())<15:
                raise ValueError("P69_SCORER_REASON_MISSING")
            if (not isinstance(j.get("ambiguity_flags"),list)
                or any(not isinstance(flag,str) or not flag.strip() for flag in j["ambiguity_flags"])):
                raise ValueError("P69_SCORER_AMBIGUITY_FLAGS_INVALID")
            if j.get("answer_adequacy") not in (True,False):
                raise ValueError("P69_SCORER_INDEPENDENT_ANSWER_REQUIRED")
    a={x["case_id"]:x for x in ra["judgments"]};b={x["case_id"]:x for x in rb["judgments"]}
    disagreements=[cid for cid in case_ids if
            (a[cid]["verdict"],sorted(a[cid]["indispensable_evidence_ids"]),a[cid]["answer_adequacy"])!=
            (b[cid]["verdict"],sorted(b[cid]["indispensable_evidence_ids"]),b[cid]["answer_adequacy"])]
    return {"verdict":"P69_DUAL_SCORER_REVIEW_CUSTODY_HOLD",
            "expected_reviewers":2,"actual_reviewers":2,"scorer_judgments":16,
            "disagreements":len(disagreements),"independent_custodian_verification":"NOT_CRYPTOGRAPHICALLY_PROVEN",
            "paper_confirmatory_gate":"HOLD"}

def self_test():
    fixture=[{"case_id":"c"+str(i),"claim":"synthetic",
              "evidence":[{"evidence_id":"e"+str(i),"text":"synthetic evidence"}]} for i in range(8)]
    sealed=[{"case_id":p["case_id"],"packet_sha256":digest(p),
             "available_ids":[p["evidence"][0]["evidence_id"]]} for p in fixture]
    assert review_verdict(fixture,sealed)["scorer_judgments"]==0
    def mock(id):
        return {"reviewer_id":id,"independent_of_author_and_model":True,
                "judgments":[{"case_id":p["case_id"],"packet_sha256":digest(p),
                  "verdict":"SUPPORT","indispensable_evidence_ids":[p["evidence"][0]["evidence_id"]],
                  "answer_adequacy":True,"ambiguity_flags":[],"reason":"Independent MOCK only; not a real reviewer."}
                 for p in fixture]}
    assert review_verdict(fixture,sealed,mock("REVIEWER_A"),mock("REVIEWER_B"))["scorer_judgments"]==16
    try:review_verdict(fixture,sealed,mock("REVIEWER_A"),mock("REVIEWER_A"))
    except ValueError:pass
    else:raise AssertionError("P69_FALSE_INDEPENDENCE")
    return "P69_EXTERNAL_SCORER_CONTRACT_TEST_PASS_REAL_HUMANS_ZERO"

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for x in ("claims","corpus","outdir","receipt"):p.add_argument("--"+x)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:print(self_test())
    else:
        if not all((a.claims,a.corpus,a.outdir,a.receipt)):
            p.error("source paths + outdir and receipt required")
        public,sealed,source,excluded_claim,excluded_doc=compile_handoff(a.claims,a.corpus)
        target=Path(a.outdir);target.mkdir(parents=True,exist_ok=True)
        for reviewer in ("A","B"):
            x,y=reviewer_schema(public,sealed,reviewer)
            (target/f"reviewer_{reviewer}_PRIVATE.json").write_text(json.dumps(x,ensure_ascii=False,indent=2))
            (target/f"response_{reviewer}_UNFILLED_PRIVATE.json").write_text(json.dumps(y,ensure_ascii=False,indent=2))
        (target/"CUSTODIAN_SEALED.json").write_text(json.dumps(sealed,indent=2))
        outcome={"kind":"P69_HELDOUT_EXTERNAL_ORIGINAL_SCORER_HANDOFF",
           "original_source_dev_sha256":source["dev_sha256"],
           "original_source_corpus_sha256":source["corpus_sha256"],
           "external_holdout_claim_clusters":8,
           "external_holdout_source_documents":8,
           "excluded_p70_original_claim_count":len(excluded_claim),
           "excluded_p70_original_source_documents":len(excluded_doc),
           "claims_or_documents_reused_from_p70":0,
           "new_independent_task_mechanism_families":0,
           "dataset_ecologies":1,
           "actual_independent_scorer_judgments":0,
           "requested_blinded_human_judgments":16,
           "model_calls":0,
           "semantic_packet_truth":"HUMAN_HOLD",
           "paper_ready":"NO"}
        Path(a.receipt).parent.mkdir(parents=True,exist_ok=True)
        Path(a.receipt).write_text(json.dumps(outcome,indent=2,sort_keys=True))
        print("P69_ORIGINAL_HELDOUT_EIGHT_CLUSTER_SCORER_HANDOFF_READY human_scores=0 provider_calls=0")
