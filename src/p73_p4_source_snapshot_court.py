"""P73-P4 original AVeriTeC snapshot and P70 cross-ecology source court.

Two downloads of a pinned file establish byte stability, NOT non-interference.
No raw claim text, URLs or licensed QA exported to receipts.
"""
import argparse,hashlib,json,collections
from pathlib import Path
from p70_ecology_averitec import source_checks,select,packet,VERTICES
from p70_external_source_pilot import load_source

def audit(before,after,claims,corpus):
    raw=Path(before).read_bytes()
    if raw!=Path(after).read_bytes():
        raise ValueError("P73_SOURCE_CHANGED_AFTER_SECOND_READ")
    data,receipt=source_checks(before)
    sel=select(data)
    chosen,_,sci=load_source(claims,corpus)
    if len(sel)!=4 or len(chosen)!=4:
        raise ValueError("P73_UNEXPECTED_SOURCE_SELECTION")
    counts=collections.Counter()
    for item in sel:
        views=[packet(item,v) for v in VERTICES]
        if len({meta["qa_multiset_sha256"] for _,meta in views})!=1:
            raise ValueError("P73_CONTENT_MODIFIED_BY_RENAMING_ORDER")
        counts["retained_qa"]+=len(item["qa"])
        counts["source_original_questions"]+=item["original_question_count"]
        counts["omitted_questions"]+=max(0,item["original_question_count"]-2)
    a=collections.Counter(row["source_label"] for row in sel)
    b=collections.Counter(annotation[0] for _,annotation in chosen)
    if a!=b or a!={"SUPPORT":2,"CONTRADICT":2}:
        raise ValueError("P70_SOURCE_POLARITY_GRID_NOT_MATCHED")
    pair_count=sum(x["source_label"]==annotation[0]
                   for x in sel for _,annotation in chosen)
    if pair_count!=8:raise ValueError("P70_CANDIDATE_PAIR_DRIFT")
    return {"kind":"P73_P4_REAL_SOURCE_SNAPSHOT_AND_P70_PARTIAL_BRIDGE",
       "averitec_source_sha256":receipt["sha256"],
       "averitec_pinned_revision":receipt["source_revision"],
       "scifact_original_dev_sha256":sci["dev_sha256"],
       "scifact_original_corpus_sha256":sci["corpus_sha256"],
       "real_original_claim_clusters_each_ecology":4,
       "real_averitec_review_variants":16,
       "matched_polarity_candidates":pair_count,
       "actual_original_question_count":dict(counts),
       "R_H_original_qa_content_preserved":True,
       "source_snapshot_repeated_bytes_identical":True,
       "source_url_is_not_source_contents":True,
       "question_answer_packet_truth":"INDEPENDENT_HUMAN_REVIEW_HOLD",
       "time_scoped_citation_validity":"NOT_INDEPENDENTLY_CERTIFIED",
       "cross_ecology_warrant_role_bijection":"UNIDENTIFIED",
       "behavioral_cross_ecology_transport":"NOT_IDENTIFIED",
       "real_world_audit_noninterference":"NOT_IDENTIFIED_BY_TWO_IDENTICAL_READS",
       "new_model_calls":0,"actual_human_reviews":0}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for a in ("before","after","claims","corpus","out"):
        p.add_argument("--"+a,required=True)
    args=p.parse_args()
    r=audit(args.before,args.after,args.claims,args.corpus)
    out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("P73_P4_ORIGINAL_SOURCE_SNAPSHOT_PASS qa_semantic_HOLD cross_ecology_HOLD calls=0")
