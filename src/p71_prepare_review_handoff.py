"""P71: Local-only, blinded, reviewer-separated AVeriTeC 16-packet handoff.

Usage: PYTHONPATH=src python src/p71_prepare_review_handoff.py
  --source /path/to/pinned/AVeriTeC/data/dev.json --out-dir PRIVATE_DIR

Never uploads raw evidence to a repository or CI artifact; materials remain
in the chosen local directory (user shares reviewer files separately).
"""
from __future__ import annotations
import argparse, json, os, random
from pathlib import Path
from p70_packet_adjudication import compile_review, court, FLAG_SET, ALLOWED

ORDERS={
 "A":(0,7,11,4,13,2,9,6,15,1,12,8,3,14,5,10),
 "B":(14,1,6,11,3,9,12,5,0,10,7,15,2,13,8,4),
}

def text_packet(p):
    lines=[f"CASE ID: {p['case_id']}",f"CLAIM: {p['claim']}"]
    for row in p["question_answer_evidence"]:
        lines.extend([f"Evidence ID: {row['evidence_id']}",
            f"Question: {row['question']}",f"Answer: {row['answer']}",
            f"Source URL: {row['source_url']}",""])
    return "\n".join(lines)

def form_template(case,packet_hash):
    return {
        "case_id":case["case_id"],"packet_sha256":packet_hash,
        "verdict":None,"sufficient_evidence_ids":[],
        "qa_order_semantically_safe":None,
        "flags":[],"reason":"",
    }

def build_files(packets,ledger,reviewer):
    if reviewer not in ORDERS:raise ValueError("P71_REVIEWER_UNKNOWN")
    if len(packets)!=16 or len(ledger)!=16:raise ValueError("P71_PACKETS_NOT_COMPLETE")
    if len(set(ORDERS[reviewer]))!=16:raise ValueError("P71_ORDER_DUPLICATED")
    ordered=[packets[i] for i in ORDERS[reviewer]]
    led={x["case_id"]:x for x in ledger}
    intro=[
        "EPISTEME-P71 | BLINDED INDEPENDENT EVIDENCE REVIEW",
        f"Reviewer panel: {reviewer} — PRIVATE, do not share with the other reviewer.",
        "Source: AVeriTeC (Schlichtkrull et al.), CC BY-NC 4.0. Original independent dataset.",
        "Only the presented claim and exactly two QA evidence atoms may be used.",
        "Do NOT look up original source labels, historical model runs or another reviewer's judgments.",
        "Do NOT browse external sources in this CLOSED-PACKET pass. URLs are provenance metadata.",
        "Some cases recur in modified visual order or renamed IDs; review each presentation independently.",
        "For EACH packet: verdict SUPPORT|CONTRADICT|INSUFFICIENT|AMBIGUOUS;",
        "necessary evidence IDs (from visible list only), semantic order safety YES|NO;",
        "flags temporal_scope,subject_identity,evidence_specificity,cross_qa_dependency,source_access,context_dependency,other;",
        "an auditable reason of >=12 characters.",
        "If provided evidence cannot entail a label, choose INSUFFICIENT or AMBIGUOUS, not a remembered fact.",
        "",
    ]
    for n,p in enumerate(ordered,1):
        intro.extend(["="*70,f"PACKET {n:02d} (record ID {p['case_id']})",text_packet(p),
            "VERDICT: [                                ]",
            "NECESSARY EVIDENCE IDS: [                ]",
            "ORDER SEMANTICALLY SAFE? [ YES / NO ]",
            "FLAGS: [                                  ]",
            "REASON: [                                 ]",""])
    form={"role":"INDEPENDENT_HUMAN_REVIEW","reviewer_id":None,
          "independent_from_author_and_model_outputs":None,
          "blind_to_original_gold_and_peer_judgments":None,
          "judgments":[form_template(p,led[p["case_id"]]["sha256_review_packet"]) for p in ordered]}
    return "\n".join(intro),form

def write_files(source,outdir):
    public,ledger,origin=compile_review(source)
    path=Path(outdir);path.mkdir(parents=True,exist_ok=True,mode=0o700)
    os.chmod(path,0o700)
    for reviewer in ORDERS:
        text,form=build_files(public,ledger,reviewer)
        for suffix,contents in ((".md",text),(".json",json.dumps(form,indent=2,ensure_ascii=False)+"\n")):
            p=path/("reviewer_"+reviewer+"_PRIVATE"+suffix)
            p.write_text(contents,encoding="utf-8")
            os.chmod(p,0o600)
    # Do NOT export sealed original labels, nor author-specific gold comparisons.
    return {"source_sha256":origin["sha256"],"masked_packets":len(public),
            "review_forms":2,"expected_human_ratings":32,
            "real_submitted_ratings":0,"actual_human_verdict":"P71_REVIEW_HOLD",
            "raw_review_text_uploaded":False}

def self_test():
    import tempfile
    pkts=[];ledger=[]
    for i in range(16):
        cid="S"+str(i)
        pkts.append({"case_id":cid,"claim":"Mock claim "+str(i),
                    "question_answer_evidence":[{"evidence_id":"e"+str(i),
                    "question":"Mock Q?","answer":"Mock A","source_url":"https://example.test"}]})
        ledger.append({"case_id":cid,"sha256_review_packet":"mock"+str(i)})
    a,f=build_files(pkts,ledger,"A");b,g=build_files(pkts,ledger,"B")
    assert len(f["judgments"])==len(g["judgments"])==16
    assert f["judgments"][0]["case_id"]!=g["judgments"][0]["case_id"]
    assert all(r["verdict"] is None and r["reason"]=="" for r in f["judgments"])
    assert all("source_label" not in a and "source_label" not in b for _ in (0,))
    assert len(set(r["case_id"] for r in f["judgments"]))==16
    print("P71_MASKED_REVIEW_HANDOFF_SELFTEST_PASS packets=16 panels=2 human_reviews=0 model_calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source");p.add_argument("--out-dir")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        if not a.source or not a.out_dir:p.error("--source and --out-dir required")
        print(json.dumps(write_files(a.source,a.out_dir),indent=2))
