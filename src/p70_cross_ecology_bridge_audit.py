"""P70: actual-source SciFact ↔ AVeriTeC *partial structural* bridge audit.

No hosted model calls. A source annotation is not the semantic oracle for a
two-QA AVeriTeC projection. The only cross-source shared objects certified
here are polarity vocabulary and explicit evidence provenance roles.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from p69_external_scifact import ingest
from p70_ecology_averitec import source_checks,select as choose_averitec
from p70_partial_mechanism_bridge import EvidenceAtom,classify,BridgeHold

SCIFACT_DEV_SHA="86f0435d08fdb65d1aa41d1472684f57e6e71930626497bdf4d7a9ec1a632217"
SCIFACT_CORPUS_SHA="b8d6c89624cb2ed74dee8938effc4f5d8bd2086887880af8110d64be4ceade62"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read_scifact(claims_path,corpus_path):
    if digest(Path(claims_path).read_bytes())!=SCIFACT_DEV_SHA:
        raise ValueError("P70_BRIDGE_SCIFACT_DEV_DIGEST_DRIFT")
    if digest(Path(corpus_path).read_bytes())!=SCIFACT_CORPUS_SHA:
        raise ValueError("P70_BRIDGE_SCIFACT_CORPUS_DIGEST_DRIFT")
    claims=list(ingest(claims_path))
    corpus={str(d["doc_id"]):d for d in ingest(corpus_path)}
    pools={"SUPPORT":[],"CONTRADICT":[]}
    for claim in claims:
        if not isinstance(claim.get("id"),int):continue
        text=claim.get("claim")
        if not isinstance(text,str) or not text.strip():continue
        possible=[]
        for doc_id,annotations in claim.get("evidence",{}).items():
            row=corpus.get(str(doc_id))
            if not row:continue
            abstract=row.get("abstract",[])
            for ann in annotations:
                label=ann.get("label")
                ids=ann.get("sentences",[])
                if label not in pools or not isinstance(ids,list) or not ids:
                    continue
                if not all(isinstance(i,int) and 0<=i<len(abstract) and
                     isinstance(abstract[i],str) and abstract[i].strip() for i in ids):continue
                possible.append((label,str(doc_id),tuple(sorted(set(ids)))))
        if len({a[0] for a in possible})!=1:continue
        label,doc,indices=min(possible,key=lambda t:(t[1],t[2]))
        atom=EvidenceAtom("SCIFACT_SENTENCE",role="scifact_rationale",
            text=corpus[doc]["abstract"][indices[0]],polarity=label,
            source_reference="SciFact:"+doc+":"+str(indices[0]))
        pools[label].append((hashlib.sha256(str(claim["id"]).encode()).hexdigest(),atom))
    if any(len(pools[k])<2 for k in pools):raise ValueError("P70_BRIDGE_SCIFACT_NOT_ENOUGH")
    return [a for label in pools for _,a in sorted(pools[label],key=lambda x:x[0])[:2]]

def bridge_audit(sf_atoms,averitec_selected):
    av_atoms=[]
    labelmap={"SUPPORT":"SUPPORT","CONTRADICT":"CONTRADICT"}
    for source in averitec_selected:
        claim, (label,doc,indices,decoy) = source if isinstance(source,tuple) and len(source)==2 else (None,None)
        # Cross-source code consumes AVeriTeC select() output in a separate path.
        raise ValueError("P70_BRIDGE_WRONG_AVERITEC_ADAPTER")

def project_averitec(selected):
    atoms=[]
    for src in selected:
        if src["source_label"] not in ("SUPPORT","CONTRADICT"):
            raise BridgeHold("P70_BRIDGE_UNSUPPORTED_POLARITY")
        qa=src["qa"]
        if len(qa)!=2:raise BridgeHold("P70_BRIDGE_QA_COUNT")
        # No inherent order-invariance is presumed. Use first atom only to
        # check a shared typed provenance+polarity quotient; not entailment.
        first=qa[0]
        atom=EvidenceAtom("AVERITEC_QA",role="averitec_qa",
            text=first["question"]+" "+first["answer"],
            polarity=src["source_label"],source_reference=first["source_url"],
            needs_external_context=True)
        atoms.append(atom)
    return atoms

def court(scifact_atoms,averitec_atoms):
    if len(scifact_atoms)!=len(averitec_atoms)!=4:
        raise ValueError("P70_BRIDGE_EXPECT_FOUR_EACH")
    if len(scifact_atoms)!=4 or len(averitec_atoms)!=4:
        raise ValueError("P70_BRIDGE_NOT_FOUR")
    pairs=[]
    for s in scifact_atoms:
        for t in averitec_atoms:
            if s.polarity!=t.polarity:continue
            r=classify(s,t)
            if r["verdict"]!="SHARED_POLARITY_AND_PROVENANCE_QUOTIENT_ONLY":
                raise BridgeHold("P70_BRIDGE_FALSE_SEMANTIC_PROMOTION")
            pairs.append({"source_label":s.polarity,
                "target_label":t.polarity,
                "verdict":r["verdict"],
                "packet_truth":"UNADJUDICATED",
                "proof_bijection":"NOT_PROVEN"})
    if len(pairs)!=8:
        raise BridgeHold("P70_BRIDGE_UNBALANCED_SUPPORT")
    return {"stage":"EPISTEME-P70",
        "kind":"SCIFACT_AVERITEC_INDEPENDENT_ORIGINAL_SOURCE_PARTIAL_BRIDGE",
        "source_claims":4,"target_claims":4,
        "same_polarity_candidate_pairs":len(pairs),
        "structural_bridge":"POLARITY_AND_PROVENANCE_ROLE_QUOTIENT_ONLY",
        "semantic_bridge":"HOLD",
        "proof_witness_family_bijection":"NOT_PROVEN",
        "QA_dependency_invariance":"NOT_PROVEN",
        "temporal_scope_alignment":"NOT_PROVEN",
        "cross_ecology_effect":"NOT_IDENTIFIED",
        "provider_calls":0,
        "pairs":pairs,
        "paper_claim_authority":"NONE_BEYOND_STRUCTURAL_SOURCE_QUOTIENT"}

def self_test():
    def atom(o,p):
        return EvidenceAtom(o,o,p,p,"mock:reference",needs_external_context=o=="AVERITEC_QA")
    sf=[atom("SCIFACT_SENTENCE",p) for p in ("SUPPORT","SUPPORT","CONTRADICT","CONTRADICT")]
    av=[atom("AVERITEC_QA",p) for p in ("SUPPORT","SUPPORT","CONTRADICT","CONTRADICT")]
    r=court(sf,av)
    assert r["same_polarity_candidate_pairs"]==8 and r["semantic_bridge"]=="HOLD"
    assert r["cross_ecology_effect"]=="NOT_IDENTIFIED"
    try:court(sf[:3],av)
    except ValueError:pass
    else:raise AssertionError("P70_MISSING_SOURCE_CASE_PROMOTED")
    print("P70_CROSS_ECOLOGY_PARTIAL_BRIDGE_SELFTEST_PASS synthetic_pairs=8 model_calls=0")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--scifact-claims");ap.add_argument("--scifact-corpus")
    ap.add_argument("--averitec-dev");ap.add_argument("--out")
    ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:self_test()
    else:
        if not all((a.scifact_claims,a.scifact_corpus,a.averitec_dev,a.out)):
            ap.error("source files and --out required")
        sf=read_scifact(a.scifact_claims,a.scifact_corpus)
        data,origin=source_checks(a.averitec_dev)
        av=project_averitec(choose_averitec(data))
        receipt=court(sf,av)
        receipt["scifact_claims_sha256"]=SCIFACT_DEV_SHA
        receipt["scifact_corpus_sha256"]=SCIFACT_CORPUS_SHA
        receipt["averitec_sha256"]=origin["sha256"]
        output=Path(a.out);output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(receipt,indent=2)+"\n")
        print("P70_SCIFACT_AVERITEC_PARTIAL_BRIDGE_PASS source_claims=4 target_claims=4 candidate_pairs=8 semantic_bridge=HOLD model_calls=0")
