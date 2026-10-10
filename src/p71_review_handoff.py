"""P71-P0: independent human review handoff and non-destructive disagreement court.

Never simulate a human reviewer. Mock fixture self-tests have zero authority.
Source AVeriTeC license CC BY-NC 4.0: external noncommercial review only.
Distribution packs contain source claim/QA text and must NOT be uploaded to
public GitHub Actions artifacts. Only status/hash/census receipts may be shared.
"""
from __future__ import annotations
import argparse, hashlib, json, random
from collections import Counter, defaultdict
from pathlib import Path

from p70_packet_adjudication import compile_review, check_review

LICENSE = "AVeriTeC original source: Schlichtkrull et al. (2023), CC BY-NC 4.0"
SOURCE = "https://github.com/MichSchli/AVeriTeC"
FIELDS = ("verdict", "sufficient_evidence_ids", "flags",
          "qa_order_semantically_safe", "reason")

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()

def build_handoff(original_source, destination, seed=71001):
    """Produce two truly source-label-blind packs and empty human templates.

    Calling this function is data *preparation*, not review participation.
    Reviewers get different randomized packet orders; no model answers/labels.
    """
    public, sealed, source_receipt = compile_review(original_source)
    out = Path(destination)
    out.mkdir(parents=True, exist_ok=True)
    by_id = {p["case_id"]: p for p in public}
    seal = {p["case_id"]: p for p in sealed}
    if len(by_id) != 16 or len(seal) != 16:
        raise ValueError("P71_NOT_SIXTEEN_UNIQUE_CASES")
    for reviewer, offset in (("A", 11), ("B", 29)):
        cases = list(public)
        random.Random(seed + offset).shuffle(cases)
        packet_output = {
            "kind": "P71_BLIND_EVIDENCE_PACKET_BUNDLE",
            "version": "P71-P0-1",
            "assignment": reviewer,
            "license": LICENSE,
            "attribution_url": SOURCE,
            "source_labels_or_justifications_visible": False,
            "model_responses_visible": False,
            "rules": ("Judge ONLY the text inside each claim/QA packet. "
                      "First pass: do not browse original fact-checkers or seek "
                      "outside facts. Rate support, contradiction, insufficiency, "
                      "or ambiguity. Cite the indispensable evidence IDs and "
                      "note temporal, referent, context and QA-order objections. "
                      "Do not discuss answers with another reviewer."),
            "cases": cases,
        }
        if any("source_label" in json.dumps(p) or "justification" in p
               for p in cases):
            raise ValueError("P71_SOURCE_LABEL_LEAK")
        (out / ("reviewer_" + reviewer + "_masked.json")).write_text(
            json.dumps(packet_output, ensure_ascii=False, indent=2) + "\n"
        )
        template = {
            "role": "INDEPENDENT_HUMAN_REVIEW",
            "reviewer_id": "REPLACE_WITH_PRIVATE_DISTINCT_PSEUDONYM",
            "independent_from_author_and_model_outputs": False,
            "instructions": "Do not submit until all 16 entries are completed, and the independence attestation is true.",
            "judgments": [{
                "case_id": p["case_id"],
                "packet_sha256": seal[p["case_id"]]["sha256_review_packet"],
                "verdict": None,
                "sufficient_evidence_ids": [],
                "flags": [],
                "qa_order_semantically_safe": None,
                "reason": "",
            } for p in cases],
        }
        (out / ("reviewer_" + reviewer + "_response_TEMPLATE.json")).write_text(
            json.dumps(template, ensure_ascii=False, indent=2) + "\n"
        )
    # The sealed file MUST NOT be circulated to reviewers. IDs, gold, roles
    # and source-control metadata are exclusively custodian-side.
    sealed_output = {
        "source_sha256": source_receipt["sha256"],
        "truth_authority": "ORIGINAL_SOURCE_LABELS_NOT_PACKET_GOLD",
        "cases": sealed,
    }
    (out / "CUSTODIAN_ONLY_sealed_ledger.json").write_text(
        json.dumps(sealed_output, ensure_ascii=False, indent=2) + "\n"
    )
    return {"kind": "P71_BLIND_HANDOFF_RECEIPT",
            "source_sha256": source_receipt["sha256"],
            "case_count": 16, "reviewer_assignments": 2,
            "actual_human_reviews_received": 0,
            "expected_independent_human_judgments": 32,
            "prepared_bundles": ["A", "B"],
            "status": "PACKETS_PREPARED_HUMAN_REVIEWS_PENDING",
            "license": LICENSE, "provider_calls": 0}

def _qa_role_map(masked_packets):
    roles = {}
    for p in masked_packets:
        cid=p["case_id"]
        mapping={}
        for row in p["question_answer_evidence"]:
            role = canonical_hash([row["question"], row["answer"],
                                   row["source_url"]])
            if role in mapping.values():
                raise ValueError("P71_DUPLICATE_QA_ROLE")
            mapping[row["evidence_id"]]=role
        roles[cid]=mapping
    return roles

def normalized_witness(j, role_map):
    evidence=j["sufficient_evidence_ids"]
    if any(e not in role_map for e in evidence):
        raise ValueError("P71_UNKNOWN_WITNESS_ROLE")
    return tuple(sorted(role_map[e] for e in evidence))

def analyze_reviews(masked_packets, sealed, reviewer_a=None,
                    reviewer_b=None, arbitration=None):
    if len(masked_packets)!=16 or len(sealed)!=16:
        raise ValueError("P71_IMPROPER_PACKET_COUNT")
    case_ids={p["case_id"] for p in masked_packets}
    if len(case_ids)!=16 or case_ids!={s["case_id"] for s in sealed}:
        raise ValueError("P71_PACKET_AND_SEAL_ID_MISMATCH")
    for p,s in zip(masked_packets,sealed):
        if p["case_id"]!=s["case_id"]:
            raise ValueError("P71_PACKET_SEALED_ORDER_MISMATCH")
        if canonical_hash(p)!=s["sha256_review_packet"]:
            # Legacy P70 digest uses JSON sort_keys+ensure_ascii without
            # compact separators. Verify that hash rather than this canonical
            # helper for backward-compatible source-custody.
            old_hash=hashlib.sha256(json.dumps(
                p, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if old_hash!=s["sha256_review_packet"]:
                raise ValueError("P71_PACKET_SHA_DRIFT")
    if reviewer_a is None or reviewer_b is None:
        return {"kind": "P71_ADJUDICATION_COURT",
                "verdict": "INDEPENDENT_HUMAN_REVIEW_HOLD",
                "case_count": 16, "actual_reviewers": 0,
                "actual_judgments": 0, "disagreement_count": None,
                "adjudication_complete": False,
                "semantic_bridge": "HOLD", "model_calls": 0}
    ida,a=check_review(reviewer_a,sealed)
    idb,b=check_review(reviewer_b,sealed)
    if ida==idb or not all(
        x.get("independent_from_author_and_model_outputs") is True
        for x in (reviewer_a,reviewer_b)):
        raise ValueError("P71_HUMAN_REVIEW_INDEPENDENCE_NOT_ATTESTED")
    roles=_qa_role_map(masked_packets)
    disputes=[]
    unanimous=[]
    for p in masked_packets:
        cid=p["case_id"]
        ja,jb=a[cid],b[cid]
        mismatch=[]
        if ja["verdict"]!=jb["verdict"]:mismatch.append("VERDICT")
        if normalized_witness(ja,roles[cid])!=normalized_witness(jb,roles[cid]):
            mismatch.append("WITNESS_ROLE")
        if sorted(ja["flags"])!=sorted(jb["flags"]):mismatch.append("EVIDENCE_FLAGS")
        if ja["qa_order_semantically_safe"]!=jb["qa_order_semantically_safe"]:
            mismatch.append("QA_ORDER_DEPENDENCY")
        if mismatch:
            disputes.append({"case_id":cid,"issues":mismatch,
                "review_a_verdict":ja["verdict"],"review_b_verdict":jb["verdict"]})
        else:unanimous.append(cid)
    # Never collapse repeated I/R/H/RH prompts into four independent human
    # samples. Those are four source claim clusters, 16 displayed packets.
    group = defaultdict(list)
    for item in sealed:
        group[item["claim_fingerprint"]].append(item["case_id"])
    if len(group)!=4 or any(len(v)!=4 for v in group.values()):
        raise ValueError("P71_ORIGINAL_CLAIM_CLUSTERS_NOT_FOUR")
    arbitration_status="NOT_NEEDED" if not disputes else "THIRD_REVIEW_REQUIRED"
    if arbitration is not None:
        if arbitration.get("role")!="THIRD_INDEPENDENT_HUMAN_ADJUDICATOR":
            raise ValueError("P71_FORGED_ARBITER_ROLE")
        cid_set={d["case_id"] for d in disputes}
        if arbitration.get("reviewer_id") in (ida,idb) or not arbitration.get("independent_from_original_reviewers"):
            raise ValueError("P71_NOT_INDEPENDENT_ARBITER")
        adjudicated=arbitration.get("judgments")
        if not isinstance(adjudicated,list) or {x.get("case_id") for x in adjudicated}!=cid_set or len(adjudicated)!=len(cid_set):
            raise ValueError("P71_ARBITRATION_NOT_EXACT_DISPUTE_SET")
        for item in adjudicated:
            if item.get("verdict") not in ("SUPPORT","CONTRADICT","INSUFFICIENT","AMBIGUOUS") or len(str(item.get("reason","")).strip())<12:
                raise ValueError("P71_ARBITRATION_INCOMPLETE")
        arbitration_status="THIRD_REVIEW_SUBMITTED_CUSTODY_UNVERIFIED"
    return {"kind": "P71_ADJUDICATION_COURT",
            "verdict": "CONSENSUS_CANDIDATE_CUSTODIAN_HOLD"
                if not disputes else "DISAGREEMENT_ADJUDICATION_HOLD",
            "case_count": 16,"claim_clusters":4,
            "actual_reviewers":2,"actual_judgments":32,
            "unanimous_packet_count":len(unanimous),
            "disagreement_count":len(disputes),
            "disputes":disputes, "adjudication_status":arbitration_status,
            "custodian_identity_verification":"REQUIRED",
            "cross_variant_warrant_bijection":"NOT_PROVEN",
            "semantic_bridge":"HOLD","model_calls":0}

def self_test():
    """No model/real reviewers. Tests only on explicitly artificial fixtures."""
    public=[];sealed=[]
    for claim in range(4):
        for v in ("I","R","H","RH"):
            cid=f"MOCK_{claim}_{v}"
            p={"case_id":cid,"claim":"Synthetic label "+str(claim),
               "question_answer_evidence":[
                 {"evidence_id":"e1"+v,"question":"Q1","answer":"A1","source_url":"https://x.test/1"},
                 {"evidence_id":"e2"+v,"question":"Q2","answer":"A2","source_url":"https://x.test/2"}]}
            public.append(p)
            sealed.append({"case_id":cid,"claim_fingerprint":str(claim),
              "vertex":v,"sha256_review_packet":
              hashlib.sha256(json.dumps(p,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
              "evidence_ids":["e1"+v,"e2"+v]})
    assert analyze_reviews(public,sealed)["verdict"]=="INDEPENDENT_HUMAN_REVIEW_HOLD"
    def fixture(name):
        return {"role":"INDEPENDENT_HUMAN_REVIEW","reviewer_id":name,
          "independent_from_author_and_model_outputs":True,
          "judgments":[{"case_id":p["case_id"],"packet_sha256":s["sha256_review_packet"],
             "verdict":"SUPPORT","sufficient_evidence_ids":[p["question_answer_evidence"][0]["evidence_id"]],
             "flags":[],"qa_order_semantically_safe":True,
             "reason":"Explicit synthetic reason to test the protocol."}
             for p,s in zip(public,sealed)]}
    ra,rb=fixture("MOCK_A"),fixture("MOCK_B")
    green=analyze_reviews(public,sealed,ra,rb)
    assert green["unanimous_packet_count"]==16
    assert green["semantic_bridge"]=="HOLD"
    rb["judgments"][0]["sufficient_evidence_ids"]=["e2I"]
    red=analyze_reviews(public,sealed,ra,rb)
    assert red["disagreement_count"]==1
    assert "WITNESS_ROLE" in red["disputes"][0]["issues"]
    try:analyze_reviews(public,sealed,ra,ra)
    except ValueError as e:assert "INDEPENDENCE" in str(e)
    else:raise AssertionError("P71_REPEATED_REVIEWER_PASSED")
    arb={"role":"THIRD_INDEPENDENT_HUMAN_ADJUDICATOR","reviewer_id":"MOCK_C",
         "independent_from_original_reviewers":True,"judgments":[{
           "case_id":public[0]["case_id"],"verdict":"AMBIGUOUS",
           "reason":"Real-world context is not present in synthetic case."}]}
    end=analyze_reviews(public,sealed,ra,rb,arb)
    assert end["adjudication_status"]=="THIRD_REVIEW_SUBMITTED_CUSTODY_UNVERIFIED"
    assert end["semantic_bridge"]=="HOLD"
    print("P71_HUMAN_REVIEW_CONTRACT_SELFTEST_PASS packets=16 mock_annotators_not_real=3 provider_calls=0")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source");ap.add_argument("--outdir")
    ap.add_argument("--review-a");ap.add_argument("--review-b");ap.add_argument("--arbitration")
    ap.add_argument("--out");ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:self_test()
    else:
        if not a.source or not a.outdir:ap.error("--source and --outdir required")
        receipt=build_handoff(a.source,a.outdir)
        if a.out:
            p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
            if a.review_a or a.review_b or a.arbitration:
                if not a.review_a or not a.review_b:
                    ap.error("both first reviewers required before arbitration")
                public,sealed,_=compile_review(a.source)
                verdict=analyze_reviews(public,sealed,
                    json.loads(Path(a.review_a).read_text()),
                    json.loads(Path(a.review_b).read_text()),
                    json.loads(Path(a.arbitration).read_text()) if a.arbitration else None)
                p.write_text(json.dumps(verdict,indent=2)+"\n")
                print("P71_"+verdict["verdict"])
            else:
                p.write_text(json.dumps(receipt,indent=2)+"\n")
                print("P71_BLIND_HANDOFF_READY actual_human_reviews=0 provider_calls=0")
