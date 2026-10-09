"""P70 external-source independent pilot: four actual SciFact-annotated claims.

ONE independently produced scientific corpus, not four independent ecologies.
32 potential hosted model calls; all edits retain the same attested rationale.
No inferred semantic-null cases; abstention not scored as false.
Raw source text and user/model responses are not uploaded as workflow artifacts.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import os
import random
import time
from pathlib import Path

from p69_external_scifact import ingest
from p69_provider_canary import MODEL_IDS
from p69_safe_error import classify

SOURCE="SciFact original public release / claims_dev.jsonl / corpus.jsonl"
SCHEMA={"type":"object","properties":{
    "verdict":{"type":"string","enum":["SUPPORT","CONTRADICT","INSUFFICIENT"]},
    "evidence_ids":{"type":"array","items":{"type":"string"}},
    },
    "required":["verdict","evidence_ids"],"additionalProperties":False}
LABELS=("SUPPORT","CONTRADICT")
VERSIONS=("I","R","H","RH")
N_CLAIMS=4
MAX_CALLS=32


def fingerprint(value):
    if not isinstance(value,str):raise ValueError("P70_DIGEST_NEEDS_STRING")
    return hashlib.sha256(value.encode()).hexdigest()


def candidates(claims,corpus):
    buckets={k:[] for k in LABELS}
    for claim in claims:
        if not isinstance(claim.get("id"),int) or not isinstance(claim.get("claim"),str) or not claim["claim"].strip():
            continue
        annotations=[]
        for doc_id,group in claim.get("evidence",{}).items():
            doc=corpus.get(str(doc_id))
            if not doc or not isinstance(doc.get("abstract"),list):continue
            abstract=doc["abstract"]
            for ann in group:
                label=ann.get("label")
                inds=ann.get("sentences",[])
                if (label not in LABELS or not isinstance(inds,list) or not inds
                    or len(inds)>3 or not all(isinstance(i,int) and
                    0<=i<len(abstract) and isinstance(abstract[i],str) and
                    abstract[i].strip() for i in inds)):continue
                ix=tuple(sorted(set(inds)))
                choices=[k for k,v in enumerate(abstract) if k not in ix
                         and isinstance(v,str) and v.strip()]
                if not choices:continue
                # Same-document supplementary sentence is deliberately NOT
                # a semantic null and is never considered an annotation.
                decoy=min(choices,key=lambda k:(abs(len(abstract[k])-len(abstract[ix[0]])),k))
                annotations.append((label,str(doc_id),ix,decoy))
        if not annotations:continue
        unique={a[0] for a in annotations}
        if len(unique)!=1:continue
        label=next(iter(unique))
        chosen=min(annotations,key=lambda a:(a[1],a[2],a[3]))
        buckets[label].append((fingerprint(str(claim["id"])),claim,chosen))
    for label in LABELS:
        buckets[label].sort(key=lambda x:x[0])
    if any(len(buckets[x])<2 for x in LABELS):
        raise ValueError("P70_NOT_ENOUGH_REAL_ANNOTATED_CLAIMS")
    chosen=[]
    used_docs=set()
    for label in LABELS:
        taken=0
        for _,claim,ann in buckets[label]:
            if (claim["id"],ann[1]) in used_docs:continue
            chosen.append((claim,ann))
            used_docs.add((claim["id"],ann[1]))
            taken+=1
            if taken==2:break
    if len(chosen)!=4:raise ValueError("P70_INSUFFICIENT_INDEPENDENT_CLAIMS")
    return chosen


def load_source(claim_path,corpus_path):
    cp=Path(claim_path);bp=Path(corpus_path)
    claims=list(ingest(cp))
    corpus={str(row["doc_id"]):row for row in ingest(bp) if "doc_id" in row}
    selected=candidates(claims,corpus)
    source_receipt={
        "corpus_rows":len(corpus),"dev_rows":len(claims),
        "corpus_sha256":hashlib.sha256(bp.read_bytes()).hexdigest(),
        "dev_sha256":hashlib.sha256(cp.read_bytes()).hexdigest(),
        "claim_ids_sha256":fingerprint(",".join(str(cl["id"]) for cl,_ in selected)),
        "selected_claim_count":len(selected),
        "selected_original_labels":dict(collections.Counter(a[0] for _,a in selected)),
        "source":"SciFact original annotated development release",
        "source_authority":"SOURCE_LABEL_CONSISTENCY_NOT_PACKET_MINIMAL_PROOF",
    }
    return selected,corpus,source_receipt


def packet(claim,annotation,corpus,version):
    if version not in VERSIONS:raise ValueError("P70_UNKNOWN_INTERVENTION")
    label,doc,indices,decoy=annotation
    positions=list(indices)+[decoy]
    if "H" in version:positions.reverse()
    evidence=[]
    for i in positions:
        eid="e"+fingerprint("P70SCIFACT|"+str(claim["id"])+"|"+doc+"|"+str(i)+
                            ("|renamed" if "R" in version else "|base"))[:15]
        evidence.append({"evidence_id":eid,"text":corpus[doc]["abstract"][i]})
    gold={e["evidence_id"] for e,i in zip(evidence,positions) if i in indices}
    public={"claim":claim["claim"],"evidence":evidence,
            "instruction":"Use only the visible evidence to decide whether it SUPPORTS or CONTRADICTS the scientific claim, or is INSUFFICIENT. Cite provided evidence IDs. Do not rely on outside knowledge."}
    private={"claim_id":claim["id"],"doc_id":doc,"label":label,"gold_ids":sorted(gold),
             "case_id":"P70EXT-"+fingerprint(str(claim["id"])+"|"+version)[:15],
             "version":version,
             "evidence_multiset_hash":fingerprint(json.dumps(sorted(e["text"] for e in evidence),ensure_ascii=False))}
    return public,private


def prompt_for(p):
    return ("Evaluate the scientific claim using only the evidence supplied. "
            "Return exactly one JSON object with keys verdict and evidence_ids. "
            "verdict must be exactly one of SUPPORT, CONTRADICT, INSUFFICIENT. "
            "Use only evidence_id strings from the supplied records. "
            "Do not guess based on external facts.\n\n"
            +json.dumps(p,ensure_ascii=False,sort_keys=True,separators=(",",":")))


def model_call(model,prompt,client):
    if model=="gptoss120":
        result=client.chat.completions.create(
            model=MODEL_IDS[model],messages=[{"role":"user","content":prompt}],
            temperature=0.2,top_p=0.95,max_completion_tokens=1024,stream=False,
            reasoning_effort="medium",reasoning_format="hidden",
            response_format={"type":"json_schema","json_schema":{
                "name":"p70_scifact_v1","strict":True,"schema":SCHEMA}})
        return result.choices[0].message.content or "",getattr(result,"model",None)
    from google.genai import types
    result=client.models.generate_content(model=MODEL_IDS[model],contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2,top_p=0.95,
            max_output_tokens=1024,response_mime_type="application/json",
            response_json_schema=SCHEMA))
    return result.text or "",getattr(result,"model_version",None)


def make_client(model):
    if model=="gptoss120":
        from groq import Groq
        return Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=0)
    from google import genai
    from google.genai import types
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"],
        http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)))


def grade(raw,public,private):
    try:parsed=json.loads(raw)
    except (TypeError,ValueError):parsed=None
    valid=(isinstance(parsed,dict) and set(parsed)==set(SCHEMA["required"])
           and parsed.get("verdict") in SCHEMA["properties"]["verdict"]["enum"]
           and isinstance(parsed.get("evidence_ids"),list)
           and all(isinstance(v,str) for v in parsed["evidence_ids"]))
    if not valid:
        return {"format_valid":False,"label_matches_original_annotation":None,
                "rationale_ids_in_packet":None,"annotated_rationale_cited":None}
    ids=parsed["evidence_ids"]
    pool={r["evidence_id"] for r in public["evidence"]}
    cited=set(ids)
    return {
        "format_valid":True,
        "label_matches_original_annotation":parsed["verdict"]==private["label"],
        "rationale_ids_in_packet":len(ids)==len(cited) and cited<=pool,
        "annotated_rationale_cited":bool(cited & set(private["gold_ids"])),
        "model_verdict":parsed["verdict"],
    }


def run(model,selected,corpus,source_receipt,offline=False):
    if model not in MODEL_IDS:raise ValueError("P70_MODEL_UNKNOWN")
    client=None if offline else make_client(model)
    grid=[(cl,ann,v) for cl,ann in selected for v in VERSIONS]
    random.Random(701009+list(MODEL_IDS).index(model)).shuffle(grid)
    rows=[]
    for cl,ann,v in grid:
        p,private=packet(cl,ann,corpus,v)
        prompt=prompt_for(p)
        start=time.monotonic_ns()
        status="RESPONSE";error=None
        try:
            raw,reported=((json.dumps({"verdict":private["label"],
               "evidence_ids":private["gold_ids"]}),MODEL_IDS[model])
               if offline else model_call(model,prompt,client))
            evaluation=grade(raw,p,private)
        except Exception as exc:
            status="PROVIDER_FAILURE"
            error=classify(exc)
            reported=None
            evaluation=grade(None,p,private)
        rows.append({
            "case_id":private["case_id"],"claim_id":private["claim_id"],
            "version":v,"source_annotation_label":private["label"],
            "evidence_multiset_hash":private["evidence_multiset_hash"],
            "prompt_sha256":fingerprint(prompt),
            "provider_status":status,"error_diagnostic":error,
            "model_bundle":model,"model_requested":MODEL_IDS[model],
            "model_reported":reported,
            "elapsed_ms":(time.monotonic_ns()-start)/1e6,
            **evaluation,
        })
    assert len(rows)==16
    return {"stage":"EPISTEME-P70","kind":"EXTERNAL_SCIFACT_PILOT",
        "model_bundle":model,"mode":"OFFLINE_FIXTURE" if offline else "ACTUAL_PROVIDER",
        "invocation_ceiling":16,"source_receipt":source_receipt,"rows":rows,
        "authority":"FOUR EXTERNAL CLAIMS / ONE SOURCE ECOLOGY; NOT CROSS-ECOLOGY REPLICATION"}


def self_test():
    corpus={}
    claims=[]
    for i in range(4):
        label=LABELS[i//2]
        doc=str(100+i)
        corpus[doc]={"doc_id":int(doc),"abstract":[
            "Claim-oriented evidence sentence "+str(i),
            "Other same-source sentence "+str(i)]}
        claims.append({"id":i+1,"claim":"Test claim "+str(i),
            "evidence":{doc:[{"label":label,"sentences":[0]}]}})
    selected=candidates(claims,corpus)
    assert len(selected)==4
    for cl,ann in selected:
        fingerprints=set()
        for v in VERSIONS:
            public,priv=packet(cl,ann,corpus,v)
            fingerprints.add(priv["evidence_multiset_hash"])
            assert grade(json.dumps({"verdict":priv["label"],
                    "evidence_ids":priv["gold_ids"]}),public,priv)["label_matches_original_annotation"]
        assert len(fingerprints)==1
    for model in MODEL_IDS:
        report=run(model,selected,corpus,{"source":"MOCK"},offline=True)
        assert len(report["rows"])==16 and all(x["format_valid"] for x in report["rows"])
    print("P70_EXTERNAL_SOURCE_SELFTEST_PASS synthetic_claims=4 mock_slots=32 provider_calls=0")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--claims")
    parser.add_argument("--corpus")
    parser.add_argument("--model",choices=tuple(MODEL_IDS))
    parser.add_argument("--out")
    parser.add_argument("--offline",action="store_true")
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:return self_test()
    if not args.claims or not args.corpus or not args.model or not args.out:
        parser.error("claims, corpus, model and out are mandatory")
    selected,corpus,receipt=load_source(args.claims,args.corpus)
    output=run(args.model,selected,corpus,receipt,offline=args.offline)
    target=Path(args.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+"\n")
    print("P70_EXTERNAL_PILOT_SLOTS="+str(len(output["rows"])))
    print("P70_SOURCE_SHA256="+receipt["dev_sha256"])


if __name__=="__main__":main()
