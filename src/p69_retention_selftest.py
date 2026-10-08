"""P69 adversarial grading and retention projection court. Zero provider calls."""
from __future__ import annotations
import json
from p69_task_factory import TASKS,VERTICES,build
from p69_independent_scorer import proof,score,oracle_response
from p69_witness_enumerator import minimal_witnesses
from p69_retention_controls import CLASSES,VIEWS,projections,census

def reference_exists(p):
    """Separate rule evaluator; does not call or reuse witness enumeration."""
    focus=p["focus_object"]
    if "provenance_records" in p:
        owned={r["trace_ref"] for r in p["provenance_records"] if r["object_ref"]==focus}
        return any(r["trace_ref"] in owned and r["intervention"]=="u1" and r["contrast"]=="different"
                   for r in p["response_rules"])
    if "transition_edges" in p:
        frontier={r["node"] for r in p["source_records"] if r["object_ref"]==focus}
        for _ in range(len(p["transition_edges"])+2):
            new=frontier|{e["to_node"] for e in p["transition_edges"] if e["from_node"] in frontier}
            if new==frontier:break
            frontier=new
        return any(r["node"] in frontier and r["intervention"]=="u1" and r["contrast"]=="different"
                   for r in p["response_rules"])
    if "conditional_rules" in p:
        owned={r["trigger_ref"] for r in p["trigger_records"] if r["object_ref"]==focus}
        enabled={r["gate_ref"] for r in p["gate_states"] if r["enabled"] is True}
        return any(r["trigger_ref"] in owned and r["intervention"]=="u1" and r["contrast"]=="different"
                   and set(r["requires_all"]).issubset(enabled) for r in p["conditional_rules"])
    if "calibration_rules" in p:
        measurements=[r for r in p["measurement_records"] if r["object_ref"]==focus]
        for rule in p["calibration_rules"]:
            if rule["object_ref"]!=focus or rule["intervention"]!="u1":continue
            for m in measurements:
                if rule.get("measurement_ref") not in (None,m["evidence_id"]):continue
                if rule["gain"]*m["measurement"]+rule["offset"]!=m["measurement"]:return True
        return False
    raise ValueError("unknown grammar")

def all_visible_ids(packet):
    out=set()
    def walk(x):
        if isinstance(x,dict):
            if isinstance(x.get("evidence_id"),str):out.add(x["evidence_id"])
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk(packet)
    return out

def run():
    main_good=0;shotguns=0;duplicates=0;alternative=0;controls=0;independent=0
    for task in TASKS:
        for v in VERTICES:
            for semantic in ("valid","null"):
                packet=build(task,v,semantic)
                oracle=oracle_response(packet)
                assert score(packet,oracle)["semantic_correct"] is True
                assert reference_exists(packet)==(semantic=="valid")
                main_good+=1
                if semantic=="valid":
                    reply=json.loads(oracle)
                    extras=sorted(all_visible_ids(packet)-set(reply["rationale_ids"]))
                    assert extras
                    reply["rationale_ids"].append(extras[0])
                    audit=score(packet,json.dumps(reply))
                    assert audit["semantic_correct"] is False
                    assert audit["answer_correct"] is True and audit["rationale_minimal"] is False
                    shotguns+=1
                    reply=json.loads(oracle)
                    reply["rationale_ids"].append(reply["rationale_ids"][0])
                    assert score(packet,json.dumps(reply))["semantic_correct"] is False
                    duplicates+=1
            for cls in CLASSES:
                pp=projections(task,v,cls)
                for view in VIEWS:
                    pkt=pp[view]
                    yes=bool(minimal_witnesses(pkt))
                    assert reference_exists(pkt)==yes,(task,v,cls,view)
                    assert score(pkt,oracle_response(pkt))["semantic_correct"] is True
                    controls+=1;independent+=1
                if cls=="recoverable":
                    proofs=minimal_witnesses(pp["rich"])
                    assert len(proofs)>=2
                    for candidate in proofs:
                        reply={"challenge":"counterexample","intervention":"u1","predicted_direction":"different",
                               "rationale_ids":sorted(candidate)}
                        assert score(pp["rich"],json.dumps(reply))["semantic_correct"] is True
                        alternative+=1
    assert (main_good,shotguns,duplicates,controls,independent)==(256,128,128,1152,1152)
    assert alternative>=256
    census()
    print("P69_SCORER_RIVAL_COURT_PASS main=256 shotgun_rejected=128 duplicates_rejected=128")
    print("independent_decision_agreement=1152 alternative_valid_proofs="+str(alternative)+" provider_calls=0")

if __name__=="__main__":run()
