"""P71 end-to-end REAL source admission, dual-tool equivalence & provenance audit.

The sole original AVeriTeC data blob is pinned by p70 source_checks.
All annotation rows in this module are TEST FIXTURES, not actual human votes.
No source claim/answer is printed, published or uploaded as an artifact.
"""
from __future__ import annotations
import argparse, copy, json, os, stat, tempfile
from pathlib import Path
from p70_packet_adjudication import compile_review
from p71_review_handoff import build_handoff,analyze_reviews
from p71_prepare_review_handoff import build_files
from p71_review_disagreement_court import run as canonical_court
from p71_review_html import render

def verify(source):
    public,ledger,origin=compile_review(source)
    assert len(public)==len(ledger)==16
    expected={v["case_id"] for v in public}
    seal={v["case_id"]:v for v in ledger}
    with tempfile.TemporaryDirectory(prefix="p71-private-") as tmp:
        root=Path(tmp)/"private"
        receipt=build_handoff(source,root)
        assert receipt["actual_human_reviews_received"]==0
        assert receipt["expected_independent_human_judgments"]==32
        assert stat.S_IMODE(root.stat().st_mode)==0o700
        order={}
        for reviewer in ("A","B"):
            masked=root/("reviewer_"+reviewer+"_masked.json")
            template=root/("reviewer_"+reviewer+"_response_TEMPLATE.json")
            assert stat.S_IMODE(masked.stat().st_mode)==0o600
            assert stat.S_IMODE(template.stat().st_mode)==0o600
            bundle=json.loads(masked.read_text())
            form=json.loads(template.read_text())
            assert bundle["source_labels_or_justifications_visible"] is False
            assert bundle["model_responses_visible"] is False
            assert form["independent_from_author_and_model_outputs"] is False
            assert form["blind_to_original_gold_and_peer_judgments"] is False
            assert {x["case_id"] for x in bundle["cases"]}==expected
            assert {x["case_id"] for x in form["judgments"]}==expected
            assert all(x["packet_sha256"]==seal[x["case_id"]]["sha256_review_packet"]
                       for x in form["judgments"])
            assert not any("source_label" in x or "justification" in x for x in bundle["cases"])
            order[reviewer]=tuple(x["case_id"] for x in bundle["cases"])
            legacy_txt,legacy_form=build_files(public,ledger,reviewer)
            assert {x["case_id"] for x in legacy_form["judgments"]}==expected
            assert {x["case_id"]:x["packet_sha256"] for x in legacy_form["judgments"]}=={
                x["case_id"]:x["packet_sha256"] for x in form["judgments"]}
            assert "original source label" not in legacy_txt.lower()
            html=render(bundle,form)
            assert len(html)>10000 and "blind_to_original_gold_and_peer_judgments:true" in html
            # Review information flows into masked HTML, not into workflow artifacts.
            assert "source_label_SEALED" not in html
            assert "CUSTODIAN_ONLY" not in html
        assert order["A"]!=order["B"]
        assert stat.S_IMODE((root/"CUSTODIAN_ONLY_sealed_ledger.json").stat().st_mode)==0o600
    assert canonical_court(ledger)["received_reviews"]==0
    assert analyze_reviews(public,ledger)["actual_judgments"]==0
    # Deliberately synthetic full responses use ONLY the original packet hash;
    # they are not evidence of independent human observations.
    def fixture(alias):
        return {"role":"INDEPENDENT_HUMAN_REVIEW","reviewer_id":"MOCK_"+alias,
          "independent_from_author_and_model_outputs":True,
          "blind_to_original_gold_and_peer_judgments":True,
          "judgments":[{
            "case_id":x["case_id"],
            "packet_sha256":x["sha256_review_packet"],
            "verdict":"INSUFFICIENT",
            "sufficient_evidence_ids":[],
            "flags":[],
            "qa_order_semantically_safe":True,
            "reason":"Explicit artificial fixture; never a human review"
          } for x in ledger]}
    a,b=fixture("A"),fixture("B")
    orig=canonical_court(ledger,a,b)
    parallel=analyze_reviews(public,ledger,a,b)
    assert orig["pairwise_disagreements"]==parallel["disagreement_count"]==0
    assert orig["semantic_bridge"]==parallel["semantic_bridge"]=="HOLD"
    b["judgments"][0]["verdict"]="AMBIGUOUS"
    orig=canonical_court(ledger,a,b)
    parallel=analyze_reviews(public,ledger,a,b)
    assert orig["pairwise_disagreements"]==parallel["disagreement_count"]==1
    arb={"role":"THIRD_HUMAN_DISPUTE_ADJUDICATOR",
         "adjudicator_id":"MOCK_C","blind_to_source_gold":True,
         "resolved_cases":[{
           "case_id":ledger[0]["case_id"],
           "packet_sha256":ledger[0]["sha256_review_packet"],
           "verdict":"AMBIGUOUS","sufficient_evidence_ids":[],
           "rationale":"Explicit mock third-party uncertainty, no human evidence."}]}
    assert canonical_court(ledger,a,b,arb)["semantic_bridge"]=="HOLD"
    assert analyze_reviews(public,ledger,a,b,arb)["semantic_bridge"]=="HOLD"
    malformed=copy.deepcopy(b)
    malformed["blind_to_original_gold_and_peer_judgments"]=False
    for func,args in ((canonical_court,(ledger,a,malformed)),
                      (analyze_reviews,(public,ledger,a,malformed))):
        try:func(*args)
        except ValueError:pass
        else:raise AssertionError("P71_UNBLINDED_REVIEW_ACCEPTED")
    malformed=copy.deepcopy(b)
    malformed["judgments"][0]["packet_sha256"]="WRONG_SOURCE"
    for func,args in ((canonical_court,(ledger,a,malformed)),
                      (analyze_reviews,(public,ledger,a,malformed))):
        try:func(*args)
        except ValueError:pass
        else:raise AssertionError("P71_WRONG_PACKET_HASH_ACCEPTED")
    return {"kind":"P71_EXACT_ORIGINAL_ECOLOGY_INTEGRATION_COURT",
            "status":"ADMISSION_CI_PASS_REVIEW_NOT_RUN",
            "source_sha256":origin["sha256"],
            "source_records":origin["records"],
            "original_claim_clusters":4,
            "distinct_masked_packets":16,
            "actual_independent_human_judgments":0,
            "actual_independent_human_reviewers":0,
            "synthetic_mock_adjudicator_count":3,
            "parallel_court_fixture_agreement":"PASS",
            "source_packet_hash_integrity":"PASS",
            "private_posix_permissions":"PASS",
            "offline_form_schema":"PASS",
            "source_text_in_receipt":False,
            "model_provider_calls":0}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--receipt",required=True)
    a=ap.parse_args()
    outcome=verify(a.source)
    p=Path(a.receipt);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(outcome,indent=2)+"\n")
    print("P71_ORIGINAL_SOURCE_INTEROPERABILITY_PASS real_human_reviews=0 model_calls=0 bot_commits=0")
