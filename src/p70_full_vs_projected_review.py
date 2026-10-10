"""P70 full-original-question vs projected-two-QA independent human comparison.

Private four-panel, source-label-masked materials. Four distinct reviewers,
two per condition, four original claim clusters, 16 prospective judgments.
This study is ADDITIONAL to unfinished P71 16 packets x2 = 32 judgments.
It does not retrieve remote cited pages or certify source truth.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,random
from pathlib import Path
from p70_ecology_averitec import (source_checks,select,packet,_clean_qa,
                                    FROZEN_SOURCE_SHA256)

def digest(x):
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,
                       separators=(",",":")).encode()).hexdigest()

def build(source):
    data,receipt=source_checks(source)
    if receipt["sha256"]!=FROZEN_SOURCE_SHA256:raise ValueError("P70_FULL_SOURCE_NOT_FROZEN")
    selected=select(data)
    if len(selected)!=4:raise ValueError("P70_FOUR_SOURCE_CLAIMS_EXPECTED")
    public=[];sealed=[];counts=collections.Counter()
    for row in selected:
        original=data[row["source_position"]]
        questions=original.get("questions")
        if not isinstance(questions,list):raise ValueError("P70_NO_ORIGINAL_QUESTIONS")
        if len(questions)!=row["original_question_count"]:
            raise ValueError("P70_SOURCE_QUESTION_CENSUS_CHANGED")
        projected,meta=packet(row,"I")
        projected_roles={(e["question"],e["answer"],e["source_url"])
                         for e in projected["question_answer_evidence"]}
        available=[]
        for i,q in enumerate(questions):
            item=_clean_qa(q)
            evidence_id="full_"+digest([row["source_claim_id"],i])[:12]
            if item is not None:
                available.append({"evidence_id":evidence_id,
                      "question":item["question"],"answer":item["answer"],
                      "source_url":item["source_url"],"answer_state":"PRESENT_IN_ORIGINAL"})
            else:
                available.append({"evidence_id":evidence_id,
                      "question":str(q.get("question","")) if isinstance(q,dict) else "",
                      "answer":"","source_url":None,
                      "answer_state":"NO_ELIGIBLE_ORIGINAL_ANSWER"})
        if len(available)!=len(questions):raise ValueError("P70_LOST_ORIGINAL_QA")
        # The projection chooses first two complete QA entries, not
        # necessarily the first two original question positions.
        full_roles={(e["question"],e["answer"],e["source_url"])
                    for e in available if e["answer_state"]=="PRESENT_IN_ORIGINAL"}
        if not projected_roles.issubset(full_roles):
            raise ValueError("P70_PROJECTION_NOT_PRESENT_IN_FULL_ORIGINAL")
        counts["original_questions"]+=len(available)
        counts["projection_retained_qa"]+=len(projected_roles)
        counts["original_questions_beyond_projection"]+=len(available)-len(projected_roles)
        counts["original_answer_missing_or_unusable"]+=sum(x["answer_state"]!="PRESENT_IN_ORIGINAL" for x in available)
        for view,evidence in (("FULL_ORIGINAL_QA",available),
                              ("PROJECTED_TWO_QA",projected["question_answer_evidence"])):
            case_id="P70FULL_"+digest([row["source_claim_id"],view])[:16]
            p={"case_id":case_id,"claim":row["claim"],
               "question_answer_evidence":evidence,
               "instructions":"Use only shown question/answer records; a source URL is not the visited webpage. Do not infer original label. Report incomplete evidence, temporal/referent uncertainty, and indispensable evidence."}
            public.append((view,row["source_claim_id"],p))
            sealed.append({"case_id":case_id,"claim_fingerprint":row["source_claim_id"],
                  "source_position":row["source_position"],
                  "condition":view,"packet_sha256":digest(p),
                  "available_ids":[e["evidence_id"] for e in evidence],
                  "original_label_SEALED":row["source_label"],
                  "structural_projection_hash":meta["qa_multiset_sha256"]})
    if len(public)!=8 or dict(counts)["original_questions"]!=10 or counts["projection_retained_qa"]!=8:
        raise ValueError("P70_UNEXPECTED_ORIGINAL_QA_COUNTERS")
    return public,sealed,dict(counts),receipt

def assignments(public,sealed):
    source={x["case_id"]:x for x in sealed}
    panels={}
    for condition,prefix in (("FULL_ORIGINAL_QA","F"),
                             ("PROJECTED_TWO_QA","P")):
        cases=[p for cond,cluster,p in public if cond==condition]
        if len(cases)!=4:raise ValueError("P70_BAD_CONDITION_SPLIT")
        for n in (1,2):
            assigned=list(cases);random.Random(401+n+(0 if prefix=="F" else 100)).shuffle(assigned)
            key=f"{prefix}{n}"
            panels[key]={
              "case_bundle":{"kind":"P70_MASKED_FULL_VS_PROJECTED",
                 "condition_display":"FULL_ORIGINAL" if prefix=="F" else "PROJECTED",
                 "source_label_visible":False,"peer_judgments_visible":False,
                 "model_outputs_visible":False,"cases":assigned},
              "response_template":{"role":"P70_FULL_VS_PROJECTED_INDEPENDENT_REVIEW",
                 "reviewer_id":"REPLACE_WITH_DISTINCT_REVIEWER_PSEUDONYM",
                 "independent_from_model_and_source_authors":False,
                 "judgments":[{"case_id":p["case_id"],
                   "packet_sha256":source[p["case_id"]]["packet_sha256"],
                   "verdict":None,"sufficient_evidence_ids":[],
                   "omitted_questions_material":None,
                   "time_or_referent_problem":None,
                   "source_access_limitations":[],
                   "reason":""} for p in assigned]}}
    return panels

def adjudicate(sealed,reviews=None):
    if not reviews:
        return {"verdict":"P70_FULL_VS_PROJECTED_HUMAN_REVIEW_PENDING",
           "expected_distinct_reviewers":4,"actual_reviewers":0,
           "expected_judgments":16,"actual_judgments":0,
           "original_claim_clusters":4,
           "full_original_vs_projection_semantics":"HOLD"}
    if set(reviews)!={"F1","F2","P1","P2"}:
        raise ValueError("P70_REQUIRED_TWO_REVIEWERS_PER_CONDITION")
    ids=[z.get("reviewer_id") for z in reviews.values()]
    if not all(isinstance(x,str) and len(x.strip())>2 for x in ids) or len(set(ids))!=4:
        raise ValueError("P70_NOT_FOUR_DISTINCT_HUMAN_REVIEWERS")
    known={x["case_id"]:x for x in sealed}
    counters=collections.Counter()
    outcomes={}
    for panel,submission in reviews.items():
        if submission.get("independent_from_model_and_source_authors") is not True:
            raise ValueError("P70_REVIEWER_INDEPENDENCE_NOT_ATTESTED")
        allowed={x["case_id"] for x in sealed if x["condition"]==(
            "FULL_ORIGINAL_QA" if panel.startswith("F") else "PROJECTED_TWO_QA")}
        rows=submission.get("judgments")
        if not isinstance(rows,list) or len(rows)!=4 or {x.get("case_id") for x in rows}!=allowed:
            raise ValueError("P70_INCOMPLETE_OR_WRONG_CONDITION_JUDGMENT")
        for j in rows:
            original=known[j["case_id"]]
            if j.get("packet_sha256")!=original["packet_sha256"]:
                raise ValueError("P70_REVIEW_PACKET_CHANGED")
            if j.get("verdict") not in ("SUPPORT","CONTRADICT","INSUFFICIENT","AMBIGUOUS"):
                raise ValueError("P70_REVIEW_BAD_VERDICT")
            names=j.get("sufficient_evidence_ids")
            if not isinstance(names,list) or len(names)!=len(set(names)) or not set(names).issubset(original["available_ids"]):
                raise ValueError("P70_INVALID_EVIDENCE_REFERENCE")
            if j["verdict"] in ("SUPPORT","CONTRADICT") and not names:
                raise ValueError("P70_LABEL_WITHOUT_JUSTIFICATION")
            if j.get("omitted_questions_material") not in (True,False,None):
                raise ValueError("P70_UNDECLARED_OMISSION_EFFECT")
            if j.get("time_or_referent_problem") not in (True,False):
                raise ValueError("P70_MISSING_TEMPORAL_REFERENT_REVIEW")
            if not isinstance(j.get("reason"),str) or len(j["reason"].strip())<15:
                raise ValueError("P70_UNEXPLAINED_HUMAN_DECISION")
            outcomes[(panel,j["case_id"])]=j
            counters[panel]+=1
    if any(counters[x]!=4 for x in reviews):raise ValueError("P70_BAD_REVIEW_CENSUS")
    # Submissions alone cannot validate that the four identities are
    # genuinely independent people or that condition effects are causal.
    return {"verdict":"P70_FULL_VS_PROJECTED_HUMAN_INPUT_RECEIVED_CUSTODIAN_HOLD",
       "expected_distinct_reviewers":4,"reported_reviewers":4,
       "reported_judgments":16,"external_identity_audit":"REQUIRED",
       "independent_source_page_truth":"NOT_VERIFIED",
       "projection_semantic_transport":"REQUIRES_RESOLVED_DISAGREEMENTS",
       "population_effect":"NOT_IDENTIFIED"}

def self_test():
    sealed=[]
    for v in ("FULL_ORIGINAL_QA","PROJECTED_TWO_QA"):
        for k in range(4):
            sealed.append({"case_id":v+str(k),"condition":v,
                           "packet_sha256":"f"*64,
                           "available_ids":["e0","e1"]})
    assert adjudicate(sealed)["actual_judgments"]==0
    def mock(name,view):
        return {"reviewer_id":name,"independent_from_model_and_source_authors":True,
                "judgments":[{"case_id":x["case_id"],"packet_sha256":x["packet_sha256"],
                  "verdict":"SUPPORT","sufficient_evidence_ids":["e0"],
                  "omitted_questions_material":False,
                  "time_or_referent_problem":False,"reason":"Synthetic test reviewer only; not real."}
                 for x in sealed if x["condition"]==view]}
    fake={"F1":mock("MOCK_FA","FULL_ORIGINAL_QA"),"F2":mock("MOCK_FB","FULL_ORIGINAL_QA"),
          "P1":mock("MOCK_PA","PROJECTED_TWO_QA"),"P2":mock("MOCK_PB","PROJECTED_TWO_QA")}
    assert adjudicate(sealed,fake)["reported_judgments"]==16
    fake["P2"]["reviewer_id"]="MOCK_PA"
    try:adjudicate(sealed,fake)
    except ValueError as e:assert "DISTINCT" in str(e)
    else:raise AssertionError("P70_FAKE_INDEPENDENCE_ACCEPTED")
    return "P70_FULL_VS_PROJECTED_DUAL_PANEL_SELFTEST_PASS_REAL_HUMANS_ZERO"

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source");p.add_argument("--outdir");p.add_argument("--receipt")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:print(self_test())
    else:
        if not all((a.source,a.outdir,a.receipt)):
            p.error("source+outdir+receipt required")
        public,sealed,counts,source=build(a.source)
        root=Path(a.outdir);root.mkdir(parents=True,exist_ok=True)
        for key,material in assignments(public,sealed).items():
            (root/f"{key}_masked_PRIVATE.json").write_text(
                json.dumps(material["case_bundle"],ensure_ascii=False,indent=2))
            (root/f"{key}_response_UNFILLED_PRIVATE.json").write_text(
                json.dumps(material["response_template"],ensure_ascii=False,indent=2))
        (root/"CUSTODIAN_SEALED.json").write_text(json.dumps(sealed,indent=2))
        receipt={"kind":"P70_ORIGINAL_FULL_VS_PROJECTED_COMPARISON_HANDOFF",
                 "source_sha256":source["sha256"],"underlying_claim_clusters":4,
                 "conditions":["FULL_ORIGINAL_QA","PROJECTED_TWO_QA"],
                 "original_question_census":counts,
                 "requested_additional_human_judgments":16,
                 "requested_distinct_human_reviewers":4,
                 "actual_human_judgments":0,
                 "P71_existing_16x2_human_judgments":0,
                 "license":source["license"],
                 "source_full_qa_equals_external_web_page_contents":False,
                 "semantic_transport":"NOT_IDENTIFIED",
                 "provider_calls":0}
        Path(a.receipt).parent.mkdir(parents=True,exist_ok=True)
        Path(a.receipt).write_text(json.dumps(receipt,indent=2,sort_keys=True))
        print("P70_FULL_ORIGINAL_VS_TWO_QA_HUMAN_PANEL_READY actual_human_reviews=0 calls=0")
