"""P69 packet-only scorer requiring EXACT inclusion-minimal sound proof IDs."""
import json
from p69_witness_enumerator import minimal_witnesses

FIELDS={"challenge","intervention","predicted_direction","rationale_ids"}

def proof(packet):
    """Canonical first minimal witness for deterministic oracle generation."""
    witnesses=minimal_witnesses(packet)
    return witnesses[0] if witnesses else None

def parse(raw):
    try:out=json.loads(raw)
    except (TypeError,ValueError):return None
    if not isinstance(out,dict) or set(out)!=FIELDS:return None
    if out["challenge"] is not None and not isinstance(out["challenge"],str):return None
    if out["intervention"] is not None and not isinstance(out["intervention"],str):return None
    if out["predicted_direction"] not in (None,"same","different"):return None
    if not isinstance(out["rationale_ids"],list) or not all(isinstance(x,str) for x in out["rationale_ids"]):return None
    return out

def all_evidence_ids(obj):
    refs=set()
    def walk(x):
        if isinstance(x,dict):
            if isinstance(x.get("evidence_id"),str):refs.add(x["evidence_id"])
            for val in x.values():walk(val)
        elif isinstance(x,list):
            for val in x:walk(val)
    walk(obj)
    return refs

def score(packet,raw):
    """Separate answer-direction validity from minimal evidence grounding.

    'semantic_correct' retains the historical API name but represents the
    STRICT grounded endpoint. 'answer_correct' is the direction/abstention
    endpoint and MUST be reported separately in future P69 model experiments.
    """
    obj=parse(raw)
    if obj is None:
        return {"format_valid":False,"answer_correct":None,"rationale_minimal":None,
                "semantic_correct":None,"executable_correct":False,
                "reason":"FORMAT_UNOBSERVED","scorer_version":"P69_SCORER_V2"}
    proofs=minimal_witnesses(packet)
    abstain=obj["challenge"] is None or obj["challenge"].strip().upper()=="NONE"
    if not proofs:
        answer=(abstain and obj["intervention"] is None and obj["predicted_direction"] is None)
        grounded=(len(obj["rationale_ids"])==0)
    else:
        answer=(not abstain and obj["intervention"]=="u1" and obj["predicted_direction"]=="different")
        claimed=obj["rationale_ids"]
        grounded=(len(claimed)==len(set(claimed)) and frozenset(claimed) in proofs)
    ok=bool(answer and grounded)
    return {"format_valid":True,"answer_correct":bool(answer),"rationale_minimal":bool(grounded),
            "semantic_correct":ok,"executable_correct":ok,
            "reason":"MINIMAL_GROUNDED" if ok else "ANSWER_WRONG" if not answer else "NONMINIMAL_OR_WRONG_WITNESS",
            "scorer_version":"P69_SCORER_V2"}

def oracle_response(packet):
    evidence=proof(packet)
    if evidence is None:
        return json.dumps({"challenge":"NONE","intervention":None,"predicted_direction":None,"rationale_ids":[]})
    return json.dumps({"challenge":"counterexample","intervention":"u1","predicted_direction":"different","rationale_ids":sorted(evidence)})
