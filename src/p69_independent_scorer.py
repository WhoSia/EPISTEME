"""P69 independent deterministic scorer: reconstructs a witness from visible evidence only."""
import json
from collections import deque

FIELDS={"challenge","intervention","predicted_direction","rationale_ids"}

def proof(packet):
    focus=packet["focus_object"]
    if "provenance_records" in packet:
        targets={r["trace_ref"]:r["evidence_id"] for r in packet["provenance_records"] if r["object_ref"]==focus}
        for r in packet["response_rules"]:
            if r["trace_ref"] in targets and r["intervention"]=="u1" and r["contrast"]=="different":
                return {targets[r["trace_ref"]],r["evidence_id"]}
        return None
    if "transition_edges" in packet:
        start=[(r["node"],{r["evidence_id"]}) for r in packet["source_records"] if r["object_ref"]==focus]
        graph={}
        for e in packet["transition_edges"]:
            graph.setdefault(e["from_node"],[]).append((e["to_node"],e["evidence_id"]))
        queue=deque(start);seen=set()
        while queue:
            node,evidence=queue.popleft()
            if node in seen:continue
            seen.add(node)
            for r in packet["response_rules"]:
                if r["node"]==node and r["intervention"]=="u1" and r["contrast"]=="different":
                    return evidence|{r["evidence_id"]}
            for dest,eid in graph.get(node,[]):queue.append((dest,evidence|{eid}))
        return None
    if "conditional_rules" in packet:
        triggers={r["trigger_ref"]:r["evidence_id"] for r in packet["trigger_records"] if r["object_ref"]==focus}
        gates={r["gate_ref"]:r for r in packet["gate_states"]}
        for r in packet["conditional_rules"]:
            if r["trigger_ref"] not in triggers or r["intervention"]!="u1" or r["contrast"]!="different":continue
            required=[gates.get(g) for g in r["requires_all"]]
            if all(g is not None and g["enabled"] is True for g in required):
                return {triggers[r["trigger_ref"]],r["evidence_id"]}|{g["evidence_id"] for g in required}
        return None
    if "calibration_rules" in packet:
        for measurement in packet["measurement_records"]:
            if measurement["object_ref"]!=focus:continue
            for rule in packet["calibration_rules"]:
                if rule["object_ref"]!=focus or rule["intervention"]!="u1":continue
                x=measurement["measurement"]
                if x*rule["gain"]+rule["offset"]!=x:
                    return {measurement["evidence_id"],rule["evidence_id"]}
        return None
    raise ValueError("unknown evidence grammar")

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
    obj=parse(raw)
    if obj is None:
        return {"format_valid":False,"semantic_correct":None,"executable_correct":False,"reason":"FORMAT_UNOBSERVED"}
    expected=proof(packet)
    abstain=obj["challenge"] is None or obj["challenge"].strip().upper()=="NONE"
    if expected is None:
        ok=(abstain and obj["intervention"] is None and obj["predicted_direction"] is None and not obj["rationale_ids"])
    else:
        ids=set(obj["rationale_ids"])
        ok=(not abstain and obj["intervention"]=="u1" and obj["predicted_direction"]=="different" and
            set(expected).issubset(ids) and ids.issubset(all_evidence_ids(packet)))
    return {"format_valid":True,"semantic_correct":bool(ok),"executable_correct":bool(ok),
            "reason":"SUPPORTED_OR_CORRECT_ABSTENTION" if ok else "UNSUPPORTED_OR_INCONSISTENT"}

def oracle_response(packet):
    evidence=proof(packet)
    if evidence is None:
        return json.dumps({"challenge":"NONE","intervention":None,"predicted_direction":None,"rationale_ids":[]})
    return json.dumps({"challenge":"counterexample","intervention":"u1","predicted_direction":"different","rationale_ids":sorted(evidence)})
