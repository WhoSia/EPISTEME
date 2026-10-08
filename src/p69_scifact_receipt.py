"""P69 provenance-only SciFact dataset receipt; never uploads dataset text or private oracle."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from p69_external_scifact import ingest,prepare,SOURCE_SCHEMA

def census(claim_path,corpus_path,archive_path,max_claims=16):
    claims=list(ingest(claim_path))
    corpus_rows=list(ingest(corpus_path))
    corpus={str(v["doc_id"]):v for v in corpus_rows if "doc_id" in v}
    packets,private=prepare(claims,corpus,max_claims)
    assert len(packets)==len(private)==8*max_claims, "SCIFACT_INSUFFICIENT_MATCHED_EXAMPLES"
    assert len({z["case_id"] for z in packets})==len(packets)
    assert all(z["needs_independent_annotation"] and z["claim_of_semantic_null"]=="NOT_AUTHORIZED" for z in private)
    assert all(z["annotation_label"] is None for z in packets)
    for k in range(0,len(packets),8):
        original=packets[k:k+8]
        a=original[0]["claim"]
        assert all(z["claim"]==a for z in original)
        visible_counts=sorted(len(z["evidence"]) for z in original)
        assert visible_counts.count(visible_counts[0])>=4
        for retained in ("gold_attested","gold_withheld"):
            subset=[packets[k+i] for i,v in enumerate(private[k:k+8])
                    if v["projected_gold_status"]==retained]
            assert len(subset)==4
            original_evidence={tuple(sorted(z["text"] for z in p["evidence"])) for p in subset}
            assert len(original_evidence)==1,"R/T_CHANGED_SEMANTICS"
    chosen=sorted({z["scifact_claim_id"] for z in private})
    return {"stage":"EPISTEME-P69","result":"EXTERNAL_SCHEMA_AND_SOURCE_CUSTODY_PASS",
            "source":"SciFact (Wadden et al. 2020)","source_schema":SOURCE_SCHEMA,
            "corpus_entries":len(corpus),"dev_claim_rows":len(claims),
            "externally_annotated_claims_selected":len(chosen),
            "source_claim_ids_sha256":hashlib.sha256(",".join(map(str,chosen)).encode()).hexdigest(),
            "generated_packet_rows":len(packets),"mode":"SCHEMA_ONLY / NOT BEHAVIORALLY VALIDATED",
            "null_claims_are": "WITHHELD_ANNOTATED_RATIONALE, NOT CERTIFIED NO-CONTRADICTION",
            "human_evidence_annotation_required":True,
            "provider_calls":0,
            "source_tar_sha256":hashlib.sha256(Path(archive_path).read_bytes()).hexdigest() if archive_path else None,
            "raw_dataset_in_artifact":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--claims",required=True)
    ap.add_argument("--corpus",required=True)
    ap.add_argument("--source-tar",default=None)
    ap.add_argument("--out",required=True)
    ap.add_argument("--max-claims",type=int,default=16)
    a=ap.parse_args()
    report=census(a.claims,a.corpus,a.source_tar,a.max_claims)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n")
    print("P69_REAL_SCIFACT_CUSTODY_PASS selected_claims="+str(report["externally_annotated_claims_selected"]))
    print("P69_SCIFACT_HUMAN_NULL_HOLD; no provider calls; raw text not uploaded")

if __name__=="__main__":main()
