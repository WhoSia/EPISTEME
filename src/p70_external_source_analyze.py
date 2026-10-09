"""P70 independent SciFact single-ecology, nonconfirmatory hosted pilot judge."""
from __future__ import annotations
import argparse
import collections
import json
import tempfile
from pathlib import Path
from p69_provider_canary import MODEL_IDS
from p70_external_source_pilot import VERSIONS,LABELS,run,candidates


def analyze(root):
    docs=[]
    for f in Path(root).rglob("*.json"):
        try:d=json.loads(f.read_text())
        except (ValueError,OSError):continue
        if d.get("kind")=="EXTERNAL_SCIFACT_PILOT":docs.append(d)
    if len(docs)!=2 or {d.get("model_bundle") for d in docs}!=set(MODEL_IDS):
        raise ValueError("P70_MISSING_OR_DUPLICATED_SOURCE_BUNDLE")
    sha=set()
    shared_cases=None
    arms={}
    for doc in docs:
        if doc["mode"]!="ACTUAL_PROVIDER" or len(doc["rows"])!=16:
            raise ValueError("P70_BAD_MODE_OR_ROWS")
        source=doc["source_receipt"]
        sha.add((source["dev_sha256"],source["corpus_sha256"],source["claim_ids_sha256"]))
        ids=collections.defaultdict(dict)
        for r in doc["rows"]:
            key=r["claim_id"]
            version=r["version"]
            if version not in VERSIONS or version in ids[key]:
                raise ValueError("P70_DUPLICATE_OR_UNDECLARED_INTERVENTION")
            if r["model_requested"]!=MODEL_IDS[doc["model_bundle"]]:
                raise ValueError("P70_MODEL_SUBSTITUTED")
            ids[key][version]=r
        if len(ids)!=4 or any(set(group)!=set(VERSIONS) for group in ids.values()):
            raise ValueError("P70_MISSING_PAIRED_CLAIM")
        corpus_identity={(str(k),group["I"]["source_annotation_label"],
            group["I"]["evidence_multiset_hash"]) for k,group in ids.items()}
        if shared_cases is not None and shared_cases!=corpus_identity:
            raise ValueError("P70_PROVIDER_SOURCE_MISMATCH")
        shared_cases=corpus_identity
        if collections.Counter(row["I"]["source_annotation_label"] for row in ids.values())!={"SUPPORT":2,"CONTRADICT":2}:
            raise ValueError("P70_SOURCE_LABEL_IMBALANCE")
        for group in ids.values():
            if len({r["evidence_multiset_hash"] for r in group.values()})!=1:
                raise ValueError("P70_R_H_CHANGED_EVIDENCE_CONTENT")
        rows=doc["rows"]
        provider=sum(r["provider_status"]=="RESPONSE" for r in rows)
        fmt=sum(r["format_valid"] is True for r in rows)
        acc=sum(r["label_matches_original_annotation"] is True for r in rows)
        grounded=sum(r["annotated_rationale_cited"] is True and
                     r["rationale_ids_in_packet"] is True for r in rows)
        correct_by_source_label={label:sum(r["label_matches_original_annotation"] is True
                                          for r in rows if r["source_annotation_label"]==label)
                                 for label in LABELS}
        # Treat absent or invalid responses as failed EXECUTION, never false latent semantics.
        executable=lambda r: int(r["label_matches_original_annotation"] is True and
                                  r["rationale_ids_in_packet"] is True)
        contrast_r=sum((executable(g["R"])-executable(g["I"]) +
                        executable(g["RH"])-executable(g["H"])) for g in ids.values())
        contrast_h=sum((executable(g["H"])-executable(g["I"]) +
                        executable(g["RH"])-executable(g["R"])) for g in ids.values())
        arms[doc["model_bundle"]]={
            "calls":16,"provider_responses":provider,"format_valid":fmt,
            "source_label_correct":acc,"annotated_evidence_cited":grounded,
            "source_label_correct_by_gold":correct_by_source_label,
            "all_call_executable_R_difference_over_eight":str(contrast_r)+"/8",
            "all_call_executable_H_difference_over_eight":str(contrast_h)+"/8",
            "technical_gate":provider==16 and fmt>=14,
            "balanced_source_label_signal":all(correct_by_source_label[v]>=1 for v in LABELS),
        }
    if len(sha)!=1:raise ValueError("P70_SOURCE_RELEASE_MISMATCH")
    technical=all(v["technical_gate"] for v in arms.values())
    signal=all(v["balanced_source_label_signal"] for v in arms.values())
    verdict=("PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE" if technical and signal
             else "TECHNICAL_EXTERNAL_HOLD" if not technical
             else "NONSELECTIVE_EXTERNAL_HOLD")
    return {"stage":"EPISTEME-P70","kind":"INDEPENDENT_SOURCE_PILOT_VERDICT",
            "verdict":verdict,"total_provider_slots":32,
            "original_source_shas":{"dev":next(iter(sha))[0],"corpus":next(iter(sha))[1]},
            "arms":arms,
            "independent_claims":4,"distinct_source_ecologies":1,
            "no_semantic_null_constructed":True,
            "claim_ceiling":"Source-original labels only, two bundles, FOUR CLAIM CLUSTERS, ONE ecology; descriptive matched R/H comparisons, no cross-ecology transfer or statistical significance.",
            "cross_ecology_replication":"NOT_PERFORMED",
            "human_independent_rescoring":"NOT_PERFORMED",
        }


def self_test():
    with tempfile.TemporaryDirectory() as td:
        corpus={}
        claims=[]
        for i in range(4):
            doc=str(1+i)
            label=LABELS[i//2]
            corpus[doc]={"doc_id":i+1,"abstract":["Realistic hypothetical evidence "+str(i),
                "Unannotated same-source sentence "+str(i)]}
            claims.append({"id":i+1,"claim":"Claim "+str(i),
                "evidence":{doc:[{"label":label,"sentences":[0]}]}})
        picked=candidates(claims,corpus)
        fake_source={"dev_sha256":"a","corpus_sha256":"b","claim_ids_sha256":"c"}
        for model in MODEL_IDS:
            d=run(model,picked,corpus,fake_source,offline=True)
            d["mode"]="ACTUAL_PROVIDER"
            Path(td,model+".json").write_text(json.dumps(d))
        x=analyze(td)
        assert x["verdict"]=="PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE"
        assert x["total_provider_slots"]==32 and x["distinct_source_ecologies"]==1
        d=json.loads(Path(td,"gemini.json").read_text())
        d["rows"][0]["evidence_multiset_hash"]="altered"
        Path(td,"gemini.json").write_text(json.dumps(d))
        try:analyze(td)
        except ValueError as e:assert "CHANGED_EVIDENCE" in str(e)
        else:raise AssertionError("P70_FAKE_EQUIVALENCE_ACCEPTED")
    print("P70_EXTERNAL_PILOT_ANALYZER_SELFTEST_PASS slots=32 invalid_bridge=REJECTED calls=0")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root")
    parser.add_argument("--out")
    parser.add_argument("--self-test",action="store_true")
    a=parser.parse_args()
    if a.self_test:return self_test()
    if not a.root or not a.out:parser.error("--root and --out required")
    report=analyze(a.root)
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+"\n")
    print("P70_"+report["verdict"])
    if report["verdict"]!="PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE":
        raise SystemExit(2)


if __name__=="__main__":main()
