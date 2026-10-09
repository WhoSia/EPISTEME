"""P70 ECO2: blind packet-review compiler and conservative two-reviewer court.

Source annotations are *not* projected packet labels. A model's self-grading
and a synthetic test fixture are not independent human adjudication.
No hosted providers, no storage/upload of copyrighted QA text in CI artifacts.
"""
from __future__ import annotations
import argparse, collections, hashlib, json
from pathlib import Path
from p70_ecology_averitec import (source_checks,select,packet,VERTICES,
                                  FROZEN_SOURCE_SHA256)

ALLOWED=("SUPPORT","CONTRADICT","INSUFFICIENT","AMBIGUOUS")
FLAG_SET=("temporal_scope","subject_identity","evidence_specificity",
          "cross_qa_dependency","source_access","context_dependency",
          "other")

def digest(s):
    return hashlib.sha256(s.encode()).hexdigest()

def compile_review(source):
    data,origin=source_checks(source)
    if origin["sha256"]!=FROZEN_SOURCE_SHA256:raise ValueError("P70_REVIEW_SOURCE_DRIFT")
    selected=select(data)
    public=[];ledger=[]
    for s in selected:
        for vertex in VERTICES:
            visible,meta=packet(s,vertex)
            # Original label, source doc position and prior justification are
            # NEVER present in the review packet.
            if any(x in visible for x in ("label","source_label","justification")):
                raise ValueError("P70_REVIEW_UNBLINDING")
            public.append(visible)
            ledger.append({
                "case_id":visible["case_id"],"claim_fingerprint":meta["source_claim_id"],
                "vertex":vertex,"source_label_SEALED":meta["source_label"],
                "sha256_review_packet":digest(json.dumps(visible,sort_keys=True,ensure_ascii=False)),
                "evidence_ids":sorted(x["evidence_id"] for x in visible["question_answer_evidence"]),
                "evidence_multiset_sha256":meta["qa_multiset_sha256"],
                "truth_authority":"INDEPENDENT_REVIEW_PENDING",
            })
    if len(public)!=16 or len(ledger)!=16:raise ValueError("P70_REVIEW_INCOMPLETE")
    return public,ledger,origin

def check_review(data,ledger):
    if not isinstance(data,dict) or data.get("role")!="INDEPENDENT_HUMAN_REVIEW":
        raise ValueError("P70_NOT_AN_INDEPENDENT_HUMAN_REVIEW")
    reviewer=data.get("reviewer_id")
    if not isinstance(reviewer,str) or not reviewer.strip():
        raise ValueError("P70_MISSING_REVIEWER_ID")
    judgments=data.get("judgments")
    if not isinstance(judgments,list) or len(judgments)!=len(ledger):
        raise ValueError("P70_REVIEW_MISSING_CASES")
    allowed={r["case_id"]:r for r in ledger}
    output={}
    for row in judgments:
        if not isinstance(row,dict):raise ValueError("P70_MALFORMED_REVIEW")
        cid=row.get("case_id")
        if cid not in allowed or cid in output:raise ValueError("P70_WRONG_OR_DUPLICATE_CASE")
        if row.get("packet_sha256")!=allowed[cid]["sha256_review_packet"]:
            raise ValueError("P70_REVIEWED_PACKET_HASH_MISMATCH")
        if row.get("verdict") not in ALLOWED:
            raise ValueError("P70_UNDECLARED_REVIEW_VERDICT")
        evidence=row.get("sufficient_evidence_ids")
        if not isinstance(evidence,list) or len(evidence)!=len(set(evidence)) or not all(
                isinstance(e,str) and e in allowed[cid]["evidence_ids"] for e in evidence):
            raise ValueError("P70_REVIEW_EVIDENCE_NOT_AVAILABLE")
        flags=row.get("flags")
        if not isinstance(flags,list) or any(v not in FLAG_SET for v in flags):
            raise ValueError("P70_BAD_REVIEW_FLAGS")
        # Grounding requires explicit subset; unsupported/ambiguous cases
        # are review outcomes, not invented factual negatives.
        if row["verdict"] in ("SUPPORT","CONTRADICT") and not evidence:
            raise ValueError("P70_POSITIVE_OR_NEGATIVE_WITHOUT_WITNESS")
        if row.get("qa_order_semantically_safe") not in (True,False):
            raise ValueError("P70_NO_ORDER_DEPENDENCE_DECISION")
        if not isinstance(row.get("reason"),str) or len(row["reason"].strip())<12:
            raise ValueError("P70_REVIEW_REASON_NOT_AUDITABLE")
        output[cid]=row
    return reviewer,output

def court(ledger,review_a=None,review_b=None):
    """Fail closed: independent reviewer *identity* and external provenance
    are process assertions verified by study custodian, not cryptographic proof.
    """
    if review_a is None or review_b is None:
        return {"verdict":"P70_PACKET_HUMAN_ADJUDICATION_HOLD",
                "reviewers_completed":0,"packets":len(ledger),
                "R_semantic_bridge":"HOLD","H_semantic_bridge":"HOLD",
                "claim_ceiling":"STRUCTURAL_PACKET_COMPILER_ONLY"}
    a_id,a=check_review(review_a,ledger)
    b_id,b=check_review(review_b,ledger)
    if a_id==b_id:raise ValueError("P70_NOT_TWO_DISTINCT_REVIEWERS")
    if not all(review.get("independent_from_author_and_model_outputs") is True
               for review in (review_a,review_b)):
        raise ValueError("P70_REVIEWER_INDEPENDENCE_UNATTESTED")
    disagreements=[]
    bygroup=collections.defaultdict(list)
    for case in ledger:
        cid=case["case_id"]
        aa,bb=a[cid],b[cid]
        # Acceptable human interpretation requires dual unanimity, including
        # witness ID role sets and no ambiguity flags or unsafe order.
        if (aa["verdict"]!=bb["verdict"] or
            aa["sufficient_evidence_ids"]!=bb["sufficient_evidence_ids"] or
            aa["qa_order_semantically_safe"]!=bb["qa_order_semantically_safe"] or
            aa["flags"]!=bb["flags"]):
            disagreements.append(cid)
        bygroup[case["claim_fingerprint"]].append((case,aa,bb))
    issues=[]
    for claim, group in bygroup.items():
        # Role remap MUST be externally verified. Different evidence_id bytes
        # at R/RH are expected; never naively compare their literal strings.
        unique={aa["verdict"] for _,aa,bb in group}
        if len(unique)!=1 or any(aa["flags"] or not aa["qa_order_semantically_safe"]
                              for _,aa,bb in group):
            issues.append(claim)
        if any(aa["verdict"]=="AMBIGUOUS" or aa["verdict"]=="INSUFFICIENT"
               for _,aa,bb in group):
            issues.append(claim)
    eligible=not disagreements and not issues
    # Even unanimous two-reviewer packet judgments do NOT certify dependency
    # graph homomorphism across SciFact and AVeriTeC or independence of reviews.
    return {"verdict":"P70_PACKET_PRELIMINARY_DUAL_REVIEW_PASS" if eligible
                         else "P70_PACKET_REVIEW_HOLD",
            "packets":len(ledger),"reviewers_completed":2,
            "disagreement_count":len(disagreements),"flagged_claim_groups":len(set(issues)),
            "R_semantic_bridge":"REQUIRES_ROLE_ISOMORPHISM_AND_CUSTODIAN_AUDIT",
            "H_semantic_bridge":"REQUIRES_DEPENDENCY_GRAPH_CERTIFICATE",
            "cross_ecology_transport":"NOT_IDENTIFIED",
            "reviewer_independence":"ATTESTED_BY_SUBMISSION_NOT_EXTERNALLY_VERIFIED"}

def self_test():
    # Contract-only mock ledger: synthetic reviews never gain human authority.
    ledger=[]
    for c in range(4):
        for v in VERTICES:
            pid="p"+str(c)+"_"+v
            ledger.append({"case_id":pid,"claim_fingerprint":"c"+str(c),
             "vertex":v,"sha256_review_packet":digest(pid),
             "evidence_ids":["e1","e2"],"source_label_SEALED":"SUPPORT"})
    assert court(ledger)["verdict"]=="P70_PACKET_HUMAN_ADJUDICATION_HOLD"
    def mock(rid):
        return {"role":"INDEPENDENT_HUMAN_REVIEW","reviewer_id":rid,
            "independent_from_author_and_model_outputs":True,
            "judgments":[{"case_id":p["case_id"],
                "packet_sha256":p["sha256_review_packet"],"verdict":"SUPPORT",
                "sufficient_evidence_ids":["e1"],"flags":[],
                "qa_order_semantically_safe":True,
                "reason":"Independent MOCK witness for contract-only test"}
                for p in ledger]}
    a=mock("test_a");b=mock("test_b")
    result=court(ledger,a,b)
    assert result["verdict"]=="P70_PACKET_PRELIMINARY_DUAL_REVIEW_PASS"
    assert result["R_semantic_bridge"]!="PASS"
    b["judgments"][0]["verdict"]="AMBIGUOUS"
    assert court(ledger,a,b)["verdict"]=="P70_PACKET_REVIEW_HOLD"
    b=mock("test_a")
    try:court(ledger,a,b)
    except ValueError as e:assert "TWO_DISTINCT" in str(e)
    else:raise AssertionError("P70_DUPLICATE_REVIEWER_ADMITTED")
    print("P70_ECO2_PACKET_REVIEW_SELFTEST_PASS toy_cases=16 independent_actual_reviews=0 paid_calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source");p.add_argument("--public");p.add_argument("--sealed")
    p.add_argument("--review-a");p.add_argument("--review-b")
    p.add_argument("--verdict");p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not all((a.source,a.public,a.sealed,a.verdict)):
            p.error("source, public, sealed, verdict required")
        public,ledger,orig=compile_review(a.source)
        Path(a.public).parent.mkdir(parents=True,exist_ok=True)
        Path(a.public).write_text(json.dumps(public,indent=2,ensure_ascii=False))
        Path(a.sealed).write_text(json.dumps(ledger,indent=2,ensure_ascii=False))
        review_a=json.loads(Path(a.review_a).read_text()) if a.review_a else None
        review_b=json.loads(Path(a.review_b).read_text()) if a.review_b else None
        report=court(ledger,review_a,review_b)
        report["origin_sha256"]=orig["sha256"]
        Path(a.verdict).write_text(json.dumps(report,indent=2))
        print("P70_ECO2_PACKET_REVIEW_"+report["verdict"]+" provider_calls=0")
