"""EPISTEME-P70 ECO2: original AVeriTeC source projection, provider-free.

Original AVeriTeC presents REAL-WORLD claims, web-sourced QA evidence and
four-class annotations, unlike the SciFact science-abstract evidence ecology.

This module DOES NOT certify that a projected QA subset entails its label.
It produces an audit-only packet specification and source receipt; no models.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,re
from pathlib import Path

SOURCE_REPO_COMMIT="7c62d1ec8df3fb560d6efe2b85fa191135636f81"
SOURCE_URL=("https://raw.githubusercontent.com/MichSchli/AVeriTeC/"+
            SOURCE_REPO_COMMIT+"/data/dev.json")
SOURCE_LICENSE="CC-BY-NC-4.0"
FROZEN_SOURCE_SHA256="499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300"
FROZEN_SOURCE_SIZE=1785475
ELIGIBLE={"supported":"SUPPORT","refuted":"CONTRADICT"}
TARGET_PER_LABEL=2
VERTICES=("I","R","H","RH")

def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def source_checks(file):
    raw=Path(file).read_bytes()
    if len(raw)>5_000_000 or len(raw)<100_000:
        raise ValueError("P70_ECO2_UNEXPECTED_ORIGINAL_SOURCE_SIZE")
    if len(raw)!=FROZEN_SOURCE_SIZE or hashlib.sha256(raw).hexdigest()!=FROZEN_SOURCE_SHA256:
        raise ValueError("P70_ECO2_ORIGINAL_SOURCE_DRIFT__NO_DATA_PROMOTION")
    try:data=json.loads(raw)
    except (UnicodeError,ValueError) as e:raise ValueError("P70_ECO2_BAD_JSON") from e
    if not isinstance(data,list) or len(data)<100:
        raise ValueError("P70_ECO2_UNEXPECTED_DEVELOPMENT_LIST")
    return data,{"source_revision":SOURCE_REPO_COMMIT,"sha256":hashlib.sha256(raw).hexdigest(),
         "bytes":len(raw),"records":len(data),"license":SOURCE_LICENSE,"source":SOURCE_URL}

def _clean_qa(qa):
    if not isinstance(qa,dict) or not isinstance(qa.get("question"),str) or not qa["question"].strip():
        return None
    candidates=[]
    for ans in qa.get("answers",[]):
        if not isinstance(ans,dict):continue
        v=ans.get("answer")
        url=ans.get("source_url")
        if (not isinstance(v,str) or not v.strip() or
            not isinstance(url,str) or not url.startswith(("http://","https://")) or
            "No answer could be found" in v):continue
        candidates.append({"answer":v.strip(),"source_url":url,
                           "question":qa["question"].strip(),
                           "answer_type":str(ans.get("answer_type",""))})
    return sorted(candidates,key=lambda a:(a["source_url"],a["answer"]))[0] if candidates else None

def select(data):
    pools={l:[] for l in ELIGIBLE.values()}
    for idx,claim in enumerate(data):
        if not isinstance(claim,dict):continue
        orig_label=claim.get("label")
        if not isinstance(orig_label,str):continue
        normalized=ELIGIBLE.get(orig_label.lower().strip())
        if normalized is None:continue
        text=claim.get("claim")
        if not isinstance(text,str) or len(text.strip())<8:continue
        questions=claim.get("questions")
        if not isinstance(questions,list):continue
        qa=[s for obj in questions if (s:=_clean_qa(obj)) is not None]
        if len(qa)<2:continue
        # Choose TWO complete Q/A atoms deterministically. Their *joint*
        # sufficiency is NOT an inherited fact from AVeriTeC.
        two=qa[:2]
        if two[0]["question"]==two[1]["question"]:continue
        record={"source_position":idx,"claim":text.strip(),
                "source_label":normalized,
                "original_source_label":orig_label,
                "qa":two,
                "original_question_count":len(questions),
                "selected_qa_count":2,
                "reporting_source":str(claim.get("reporting_source","")),
                "source_claim_id":sha_text(str(idx)+"|"+text),
                "human_packet_level_reannotation_required":True}
        pools[normalized].append((sha_text(text),record))
    result=[]
    for label in ELIGIBLE.values():
        sorted_candidates=sorted(pools[label],key=lambda x:x[0])
        if len(sorted_candidates)<TARGET_PER_LABEL:raise ValueError("P70_ECO2_NOT_ENOUGH_SOURCE_ELIGIBLE_CASES")
        selected=sorted_candidates[:TARGET_PER_LABEL]
        result.extend(r for _,r in selected)
    if len({r["source_claim_id"] for r in result})!=4:raise ValueError("P70_ECO2_SOURCE_CLAIMS_COLLIDE")
    return result

def packet(source,vertex):
    if vertex not in VERTICES:raise ValueError("P70_ECO2_UNKNOWN_OPERATOR")
    qa=source["qa"]
    visible=[]
    for idx,row in enumerate(qa):
        # Source URL preserved to expose original provenance, but user models
        # will be forbidden to retrieve. A source URL is NOT proof content.
        evid_id="e"+sha_text(source["source_claim_id"]+"|"+str(idx)+
                               ("|R" if "R" in vertex else "|I"))[:12]
        visible.append({"evidence_id":evid_id,**row})
    if "H" in vertex:visible.reverse()
    public={"case_id":"P70ECO2-"+sha_text(source["source_claim_id"]+"|"+vertex)[:17],
            "claim":source["claim"],"question_answer_evidence":visible,
            "instructions":"Use ONLY provided QA text. Source URLs are citations, not permission to search."}
    private={"source_claim_id":source["source_claim_id"],"source_label":source["source_label"],
             "vertex":vertex,"original_source_label":source["original_source_label"],
             "qa_multiset_sha256":sha_text(json.dumps(sorted(
                 (row["question"],row["answer"],row["source_url"]) for row in visible))),
             "original_question_count":source["original_question_count"],
             "independent_packet_truth":"UNADJUDICATED",
             "multi_question_order_invariance":"UNPROVEN",
             "original_source_label_not_proof_of_packet_label":True}
    return public,private

def audit(data,source_receipt):
    selected=select(data)
    census={"SUPPORT":2,"CONTRADICT":2}
    assert dict(collections.Counter(x["source_label"] for x in selected))==census
    grouping=[]
    for src in selected:
        records=[packet(src,v) for v in VERTICES]
        hashes={meta["qa_multiset_sha256"] for _,meta in records}
        if len(hashes)!=1:raise ValueError("P70_ECO2_QA_MULTISETS_CHANGED_BY_OPERATOR")
        for (public,meta),v in zip(records,VERTICES):
            if len(public["question_answer_evidence"])!=2 or meta["vertex"]!=v:
                raise ValueError("P70_ECO2_BAD_PACKET_CONSTRUCTION")
            if v in ("I","R") and public["question_answer_evidence"][0]["question"]!=src["qa"][0]["question"]:
                raise ValueError("P70_ECO2_H_CHANGED_IDENTITY_ORDER")
        assert records[0][0]["question_answer_evidence"][0]["evidence_id"] != records[1][0]["question_answer_evidence"][0]["evidence_id"]
        assert records[2][0]["question_answer_evidence"][0]["question"]==records[0][0]["question_answer_evidence"][1]["question"]
        grouping.append({"claim_fingerprint":src["source_claim_id"],"label":src["source_label"],
                         "qa_count":2,"original_question_count":src["original_question_count"],
                         "structural_multiset_hash":next(iter(hashes)),
                         "packet_semantic_invariance":"HUMAN_HOLD",
                         "packet_level_gold":"HUMAN_HOLD"})
    return {"stage":"EPISTEME-P70","kind":"INDEPENDENT_ECOLOGY_ORIGINAL_SOURCE_AUDIT",
            "source_receipt":source_receipt,
            "selected_claims":4,"source_label_balance":census,
            "constructed_structural_packets":len(selected)*len(VERTICES),
            "operator_content_multiset_preserved":True,
            "qa_dependency_commutation":"NOT_PROVEN",
            "packet_ground_truth":"UNADJUDICATED",
            "target_domains":["original SciFact science-abstract rationale","AVeriTeC real-world web fact-checking QA"],
            "cross_ecology_mechanism_bridge":"HOLD",
            "provider_calls":0,"selected":grouping,
            "allowed_promotion":"DATA_SOURCE_AND_STRUCTURAL_ONLY"}

def self_test():
    labels=("Supported","Supported","Refuted","Refuted")
    data=[]
    for j in range(140):
        lab=labels[j%4]
        data.append({"claim":"Independent original mock claim number "+str(j),
                     "label":lab,"reporting_source":"synthetic-source",
                     "questions":[{"question":"Q1 "+str(j),
                       "answers":[{"answer":"First evidence "+str(j),"source_url":"https://example.org/a"}]},
                      {"question":"Q2 "+str(j),
                       "answers":[{"answer":"Second evidence "+str(j),"source_url":"https://example.org/b"}]}]})
    report=audit(data,{"source":"SYNTHETIC_FIXTURE"})
    assert report["constructed_structural_packets"]==16
    assert report["cross_ecology_mechanism_bridge"]=="HOLD"
    claim=select(data)[0]
    p,meta=packet(claim,"RH")
    assert len(p["question_answer_evidence"])==2
    assert meta["independent_packet_truth"]=="UNADJUDICATED"
    bad=[dict(x) for x in data]
    bad[0]={"claim":"failing","label":"Refuted","questions":[]}
    assert all(item["source_claim_id"]!=sha_text("0|failing") for item in select(bad))
    print("P70_ECO2_SOURCE_SELFTEST_PASS mock_cases=140 mock_packets=16 provider_calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source");p.add_argument("--out");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.source or not a.out:p.error("--source/--out required")
        data,receipt=source_checks(a.source)
        outcome=audit(data,receipt)
        path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(outcome,indent=2,ensure_ascii=False)+"\n")
        print("P70_ECO2_ORIGINAL_SOURCE_AUDIT_PASS cases=4 packets=16 provider_calls=0 packet_truth=HOLD")
        print("P70_ECO2_ORIGINAL_SHA256="+receipt["sha256"])
