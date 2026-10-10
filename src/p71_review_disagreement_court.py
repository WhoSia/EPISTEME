"""P71: dual blinded human-rating and dispute escalation court.

No score is imputed. Identical labels on 16 repeated packets do not create
16 independent scientific units: only four underlying claims are sampled.
"""
from __future__ import annotations
import argparse, json, collections
from pathlib import Path
from p70_packet_adjudication import check_review, ALLOWED

def run(ledger, a=None, b=None, c=None):
    if len(ledger)!=16 or len({x["case_id"] for x in ledger})!=16:
        raise ValueError("P71_MISSING_OR_DUPLICATED_16_CASE_LEDGER")
    if a is None or b is None:
        return {"verdict":"P71_INDEPENDENT_HUMAN_REVIEW_HOLD",
                "required_reviews":32,"received_reviews":0 if a is None and b is None else 16,
                "independent_claim_clusters":4,"packets":16,
                "third_party_adjudication":"NOT_STARTED",
                "source_labels_used":False}
    aid,ar=check_review(a,ledger);bid,br=check_review(b,ledger)
    if aid==bid:raise ValueError("P71_NOT_DISTINCT_HUMAN_REVIEWERS")
    if not all(r.get("independent_from_author_and_model_outputs") is True and
               r.get("blind_to_original_gold_and_peer_judgments") is True for r in (a,b)):
        raise ValueError("P71_REVIEWER_BLINDING_OR_INDEPENDENCE_UNATTESTED")
    diffs=[]
    agreement=0
    for record in ledger:
        cid=record["case_id"];x,y=ar[cid],br[cid]
        same=(x["verdict"]==y["verdict"] and
              set(x["sufficient_evidence_ids"])==set(y["sufficient_evidence_ids"]) and
              x["qa_order_semantically_safe"]==y["qa_order_semantically_safe"] and
              set(x["flags"])==set(y["flags"]))
        if same:agreement+=1
        else:diffs.append({"case_id":cid,"claim_fingerprint":record["claim_fingerprint"],
             "reason":"BLINDED_JUDGMENT_OR_WITNESS_DISAGREEMENT"})
    if c is None:
        state="P71_HUMAN_DISAGREEMENT_ADJUDICATION_HOLD" if diffs else "P71_DUAL_REVIEW_COMPLETE_BRIDGE_NOT_CERTIFIED"
        return {"verdict":state,"received_reviews":32,"packets":16,
                "independent_claim_clusters":4,"pairwise_exact_agreements":agreement,
                "pairwise_disagreements":len(diffs),"dispute_queue":diffs,
                "third_party_adjudication":"PENDING" if diffs else "NOT_REQUIRED",
                "semantic_bridge":"HOLD","source_labels_used":False,
                "claim_ceiling":"HUMAN_LABELS_NOT_CAUSAL_TRANSPORT"}
    if not isinstance(c,dict) or c.get("role")!="THIRD_HUMAN_DISPUTE_ADJUDICATOR":
        raise ValueError("P71_THIRD_PARTY_ROLE_MISSING")
    if c.get("adjudicator_id") in (None,"",aid,bid) or c.get("blind_to_source_gold") is not True:
        raise ValueError("P71_THIRD_REVIEWER_NOT_INDEPENDENT")
    submissions=c.get("resolved_cases",[])
    if len(submissions)!=len(diffs) or {r.get("case_id") for r in submissions}!={d["case_id"] for d in diffs}:
        raise ValueError("P71_THIRD_ADJUDICATION_DISPUTE_CENSUS_INCOMPLETE")
    for r in submissions:
        if r.get("verdict") not in ALLOWED:
            raise ValueError("P71_THIRD_UNDECLARED_VERDICT")
        if not isinstance(r.get("rationale"),str) or len(r["rationale"].strip())<20:
            raise ValueError("P71_THIRD_ADJUDICATION_REASON_MISSING")
        allowed=next(x for x in ledger if x["case_id"]==r["case_id"])
        if r.get("packet_sha256")!=allowed["sha256_review_packet"]:
            raise ValueError("P71_THIRD_WRONG_SOURCE_PACKET_HASH")
        if r.get("verdict") in ("SUPPORT","CONTRADICT"):
            refs=r.get("sufficient_evidence_ids",[])
            if not refs or not set(refs)<=set(allowed["evidence_ids"]):
                raise ValueError("P71_THIRD_NO_EVIDENCE_WITNESS")
    return {"verdict":"P71_THIRD_PARTY_DISPUTE_PROCESS_COMPLETED",
            "received_reviews":32,"third_adjudications":len(diffs),
            "unresolved_disputes":0,"semantic_bridge":"HOLD",
            "claim_ceiling":"REVIEW_RECORD_COMPLETE; PROOF_MAP_STILL_SEPARATE",
            "reviewer_identity_verified_outside_code":False}

def self_test():
    ledger=[{"case_id":f"q{k}","claim_fingerprint":f"g{k//4}",
             "sha256_review_packet":f"sha{k}","evidence_ids":["x","y"]}
            for k in range(16)]
    assert run(ledger)["verdict"]=="P71_INDEPENDENT_HUMAN_REVIEW_HOLD"
    def reviewer(alias):
        return {"role":"INDEPENDENT_HUMAN_REVIEW","reviewer_id":alias,
          "independent_from_author_and_model_outputs":True,
          "blind_to_original_gold_and_peer_judgments":True,
          "judgments":[{"case_id":e["case_id"],"packet_sha256":e["sha256_review_packet"],
            "verdict":"SUPPORT","sufficient_evidence_ids":["x"],
            "qa_order_semantically_safe":True,"flags":[],"reason":"Synthetic test only, never an actual review"} for e in ledger]}
    a=reviewer("test_a");b=reviewer("test_b")
    assert run(ledger,a,b)["verdict"]=="P71_DUAL_REVIEW_COMPLETE_BRIDGE_NOT_CERTIFIED"
    b["judgments"][0]["verdict"]="INSUFFICIENT"
    q=run(ledger,a,b)
    assert q["pairwise_disagreements"]==1 and q["verdict"]=="P71_HUMAN_DISAGREEMENT_ADJUDICATION_HOLD"
    third={"role":"THIRD_HUMAN_DISPUTE_ADJUDICATOR","adjudicator_id":"test_c",
           "blind_to_source_gold":True,
           "resolved_cases":[{"case_id":"q0","packet_sha256":"sha0","verdict":"AMBIGUOUS",
                              "sufficient_evidence_ids":[],"rationale":"A synthetic disagreement case with no warranted entailment"}]}
    assert run(ledger,a,b,third)["verdict"]=="P71_THIRD_PARTY_DISPUTE_PROCESS_COMPLETED"
    third["adjudicator_id"]="test_a"
    try:run(ledger,a,b,third)
    except ValueError:pass
    else:raise AssertionError("P71_SAME_PERSON_THIRD_REVIEW_ACCEPTED")
    # No null case may pass by simply omitting one real reviewer.
    assert run(ledger,a,None)["verdict"]=="P71_INDEPENDENT_HUMAN_REVIEW_HOLD"
    print("P71_DISAGREEMENT_COURT_SELFTEST_PASS toy_agreement_dispute_and_third=PASS genuine_human_reviews=0 provider_calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--ledger");p.add_argument("--review-a");p.add_argument("--review-b")
    p.add_argument("--review-c");p.add_argument("--out")
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    if args.self_test:self_test()
    else:
        if not args.ledger or not args.out:p.error("--ledger and --out required")
        load=lambda s:json.loads(Path(s).read_text()) if s else None
        result=run(load(args.ledger),load(args.review_a),load(args.review_b),load(args.review_c))
        dst=Path(args.out);dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
        print("P71_REVIEW_COURT="+result["verdict"])
