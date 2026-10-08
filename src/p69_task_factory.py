"""P69 task compiler. Synthetic instrument only; no provider or scoring oracle calls."""
from __future__ import annotations
import hashlib,itertools,json

FAMILIES=("provenance","composition","guarded","transformation")
TASKS=tuple(f"{f}_{i}" for f in FAMILIES for i in (1,2))
PILOT_TASKS=("provenance_0","transformation_0")
FHL_CONTEXTS=((0,0,0),(0,1,1),(1,0,1),(1,1,0))
VERTICES=tuple(tuple(k for k,v in zip("RFHTL",(r,f,h,t,l)) if v)
               for f,h,l in FHL_CONTEXTS for r,t in itertools.product((0,1),repeat=2))
SEMANTICS=("valid","null")

def tag(*parts):
    return "k"+hashlib.sha256(("P69|"+"|".join(map(str,parts))).encode()).hexdigest()[:9]

def build(task,vertex,semantic):
    if task not in TASKS+PILOT_TASKS or vertex not in VERTICES or semantic not in SEMANTICS:
        raise ValueError("bad task cell")
    family,instance=task.rsplit("_",1);inst=int(instance);op=set(vertex)
    stem=tag(task,"renamed" if "R" in op else "base")
    focus=stem+":focus";decoy=stem+":decoy";src=stem+":source";mid=stem+":middle";other=stem+":alternate"
    def ev(name):return stem+":ev:"+name
    pkt={"archive_id":tag(task,"".join(vertex),semantic),
         "focus_object":focus,
         "terminal_observation":{"focus":"stable","counterpart":"stable"},
         "incumbent_claim":"The retained terminal observation suffices to predict the focus-object response to u1.",
         "available_interventions":["u1","uX"],
         "surface_domain":family,
         "instructions":"Using only the retained evidence, propose one justified counterexample against the focus claim under u1, or NONE if unjustified. Include each indispensable evidence_id in rationale_ids. A decoy-only contrast is not a focus-object refutation."}
    if family=="provenance":
        records=[{"object_ref":focus,"trace_ref":src,"evidence_id":ev("origin")},
                 {"object_ref":decoy,"trace_ref":other,"evidence_id":ev("decoy_origin")}]
        rules=[{"trace_ref":src,"intervention":"u1","contrast":"different" if semantic=="valid" else "same","evidence_id":ev("target_rule")},
               {"trace_ref":other,"intervention":"uX","contrast":"different","evidence_id":ev("decoy_rule")}]
        if inst==2:
            records.append({"object_ref":focus,"trace_ref":mid,"evidence_id":ev("alternate_origin")})
            rules.append({"trace_ref":mid,"intervention":"u1","contrast":"same","evidence_id":ev("alternate_rule")})
        pkt.update(provenance_records=records,response_rules=rules)
    elif family=="composition":
        records=[{"object_ref":focus,"node":src,"evidence_id":ev("source")},
                 {"object_ref":decoy,"node":other,"evidence_id":ev("decoy_source")}]
        edges=[{"from_node":src,"to_node":mid if semantic=="valid" else other,"evidence_id":ev("hop1")},
               {"from_node":mid,"to_node":stem+":sink","evidence_id":ev("hop2")}]
        if inst==2:
            edges.extend([{"from_node":other,"to_node":stem+":decoy_sink","evidence_id":ev("decoy_hop")},
                          {"from_node":stem+":decoy_sink","to_node":other,"evidence_id":ev("decoy_cycle")}])
        rules=[{"node":stem+":sink","intervention":"u1","contrast":"different","evidence_id":ev("rule")},
               {"node":stem+":decoy_sink","intervention":"uX","contrast":"different","evidence_id":ev("decoy_rule")}]
        pkt.update(source_records=records,transition_edges=edges,response_rules=rules)
    elif family=="guarded":
        records=[{"object_ref":focus,"trigger_ref":src,"evidence_id":ev("source")},
                 {"object_ref":decoy,"trigger_ref":other,"evidence_id":ev("decoy_source")}]
        gates=(stem+":gate0",) if inst in (0,1) else (stem+":gate0",stem+":gate1")
        states=[{"gate_ref":g,"enabled":bool(semantic=="valid" or (inst==2 and idx==1)),"evidence_id":ev(f"gate{idx}")} for idx,g in enumerate(gates)]
        rules=[{"trigger_ref":src,"intervention":"u1","contrast":"different","requires_all":list(gates),"evidence_id":ev("rule")},
               {"trigger_ref":other,"intervention":"uX","contrast":"different","requires_all":[],"evidence_id":ev("decoy_rule")}]
        pkt.update(trigger_records=records,gate_states=states,conditional_rules=rules)
    else:
        baseline=4 if inst==1 else 7
        records=[{"object_ref":focus,"measurement":baseline,"evidence_id":ev("measurement")},
                 {"object_ref":decoy,"measurement":1,"evidence_id":ev("decoy_measurement")}]
        gain=((3 if inst==0 else 2) if semantic=="valid" else 1) if inst in (0,1) else 1
        offset=3 if inst==2 and semantic=="valid" else 0
        rules=[{"object_ref":focus,"intervention":"u1","gain":gain,"offset":offset,"evidence_id":ev("calibration")},
               {"object_ref":decoy,"intervention":"uX","gain":3,"offset":0,"evidence_id":ev("decoy_calibration")}]
        pkt.update(measurement_records=records,calibration_rules=rules,
                   contrast_rule="A focus u1 counterexample requires the transformed value to differ from the retained baseline.")
    row_keys=("provenance_records","source_records","trigger_records","measurement_records")
    # T is uniformly the within-trace ordering of one relevant and two irrelevant tokens.
    for key in row_keys:
        if key in pkt:
            for row in pkt[key]:
                basis=row.get("trace_ref",row.get("node",row.get("trigger_ref",row.get("object_ref"))))
                row["trace"]=[basis,tag(task,stem,"aux-left"),tag(task,stem,"aux-right")]
    if "F" in op:
        pkt["irrelevant_records"]=[{"object_ref":stem+f":noise{i}","note":"unrelated","evidence_id":ev(f"filler{i}")} for i in range(3)]
    if "H" in op:
        for key in row_keys:
            if key in pkt:pkt[key].reverse()
    if "T" in op:
        for key in row_keys:
            if key in pkt:
                for row in pkt[key]:row["trace"].reverse()
    if "L" in op:
        for key in ("response_rules","conditional_rules","calibration_rules"):
            if key in pkt:pkt[key].reverse()
    return pkt

def canonical_json(packet):
    return json.dumps(packet,sort_keys=True,ensure_ascii=False,separators=(",",":"))

def lattice():
    for task in TASKS:
        for vertex in VERTICES:
            for semantic in SEMANTICS:yield task,vertex,semantic,build(task,vertex,semantic)

if __name__=="__main__":
    print("P69_PACKET_COMPILER_PASS",len(list(lattice())))
