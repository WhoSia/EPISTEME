"""P69 exhaustive minimal-evidence adjudicator; packet only, no task labels."""
from __future__ import annotations

def minimal_witnesses(p):
    focus=p["focus_object"]
    found=set()
    if "provenance_records" in p:
        for src in p["provenance_records"]:
            if src["object_ref"]!=focus:continue
            for rule in p["response_rules"]:
                if (rule["trace_ref"]==src["trace_ref"] and rule["intervention"]=="u1"
                    and rule["contrast"]=="different"):
                    found.add(frozenset((src["evidence_id"],rule["evidence_id"])))
    elif "transition_edges" in p:
        graph={}
        for edge in p["transition_edges"]:
            graph.setdefault(edge["from_node"],[]).append((edge["to_node"],edge["evidence_id"]))
        goals={}
        for rule in p["response_rules"]:
            if rule["intervention"]=="u1" and rule["contrast"]=="different":
                goals.setdefault(rule["node"],[]).append(rule["evidence_id"])
        count=0
        for src in p["source_records"]:
            if src["object_ref"]!=focus:continue
            node=src["node"]
            stack=[(node,frozenset((src["evidence_id"],)),frozenset((node,)))]
            while stack:
                current,eids,visited=stack.pop()
                count+=1
                if count>2048:raise ValueError("P69_PATH_ENUMERATION_LIMIT")
                for goal in goals.get(current,[]):found.add(eids|{goal})
                for nxt,edge_id in graph.get(current,()):
                    if nxt not in visited:stack.append((nxt,eids|{edge_id},visited|{nxt}))
    elif "conditional_rules" in p:
        gates={g["gate_ref"]:g for g in p["gate_states"]}
        for tr in p["trigger_records"]:
            if tr["object_ref"]!=focus:continue
            for rule in p["conditional_rules"]:
                if (tr["trigger_ref"]!=rule["trigger_ref"] or rule["intervention"]!="u1"
                    or rule["contrast"]!="different"):continue
                required=[gates.get(x) for x in rule["requires_all"]]
                if all(x is not None and x["enabled"] is True for x in required):
                    found.add(frozenset([tr["evidence_id"],rule["evidence_id"]]+[x["evidence_id"] for x in required]))
    elif "calibration_rules" in p:
        for meas in p["measurement_records"]:
            if meas["object_ref"]!=focus:continue
            for rule in p["calibration_rules"]:
                if rule["object_ref"]!=focus or rule["intervention"]!="u1":continue
                if rule.get("measurement_ref") not in (None,meas["evidence_id"]):continue
                x=meas["measurement"]
                if x*rule["gain"]+rule["offset"]!=x:
                    found.add(frozenset((meas["evidence_id"],rule["evidence_id"])))
    else:raise ValueError("P69_UNKNOWN_EVIDENCE_GRAMMAR")
    ordered=sorted(found,key=lambda a:(len(a),tuple(sorted(a))))
    return tuple(a for a in ordered if not any(b<a for b in ordered))
