"""P69 no-provider retention projections for construct controls.
Not in the frozen 8192-call main lattice. Sham uses truthful decoy reserve.
"""
from __future__ import annotations
import copy,hashlib,json
from p69_task_factory import TASKS,VERTICES,build
from p69_witness_enumerator import minimal_witnesses

CLASSES=("critical","recoverable","null")
VIEWS=("rich","coarse","sham_rich")

def seal(*items):
    return "r"+hashlib.sha256(("P69RETENTION|"+"|".join(map(str,items))).encode()).hexdigest()[:12]

def rule_key(p):
    if "conditional_rules" in p:return "conditional_rules"
    if "calibration_rules" in p:return "calibration_rules"
    return "response_rules"

def second_witness(packet,task,vertex):
    p=copy.deepcopy(packet)
    focus=p["focus_object"]
    stub=seal(task,"secondary")
    eid=lambda name:stub+":ev:"+name
    trace=lambda x:([seal(task,"auxA"),seal(task,"auxB"),x] if "T" in vertex
                    else [x,seal(task,"auxA"),seal(task,"auxB")])
    if "provenance_records" in p:
        t=stub+":focus_trace"
        p["provenance_records"].append(dict(object_ref=focus,trace_ref=t,evidence_id=eid("source"),trace=trace(t)))
        p["response_rules"].append(dict(trace_ref=t,intervention="u1",contrast="different",evidence_id=eid("rule")))
    elif "transition_edges" in p:
        a,b,c=(stub+":source",stub+":middle",stub+":sink")
        p["source_records"].append(dict(object_ref=focus,node=a,evidence_id=eid("source"),trace=trace(a)))
        p["transition_edges"].extend([dict(from_node=a,to_node=b,evidence_id=eid("edge0")),
                                      dict(from_node=b,to_node=c,evidence_id=eid("edge1"))])
        p["response_rules"].append(dict(node=c,intervention="u1",contrast="different",evidence_id=eid("rule")))
    elif "conditional_rules" in p:
        a,g=stub+":trigger",stub+":gate"
        p["trigger_records"].append(dict(object_ref=focus,trigger_ref=a,evidence_id=eid("source"),trace=trace(a)))
        p["gate_states"].append(dict(gate_ref=g,enabled=True,evidence_id=eid("gate")))
        p["conditional_rules"].append(dict(trigger_ref=a,intervention="u1",contrast="different",
                                            requires_all=[g],evidence_id=eid("rule")))
    else:
        m=next(x for x in p["measurement_records"] if x["object_ref"]==focus)
        for r in p["calibration_rules"]:
            if r["object_ref"]==focus and r["intervention"]=="u1":
                r["measurement_ref"]=m["evidence_id"]
        p["measurement_records"].append(dict(object_ref=focus,measurement=11,evidence_id=eid("measurement"),trace=trace(focus)))
        p["calibration_rules"].append(dict(object_ref=focus,intervention="u1",gain=1,offset=5,
                                           measurement_ref=eid("measurement"),evidence_id=eid("calibration")))
    assert len(minimal_witnesses(p))>=2
    return p

def decoy_reserve(p,task,count):
    template=next(r for r in p[rule_key(p)] if r["intervention"]=="uX")
    reserve=[]
    for i in range(count):
        r=copy.deepcopy(template)
        r["evidence_id"]=seal(task,"decoy_true",i)
        reserve.append(r)
    return reserve

def facts(p):
    keys=("provenance_records","source_records","trigger_records","measurement_records",
          "response_rules","conditional_rules","calibration_rules","transition_edges","gate_states","irrelevant_records")
    return {(k,json.dumps(row,sort_keys=True)) for k in keys for row in p.get(k,())}

def projections(task,vertex,world_class):
    if task not in TASKS or vertex not in VERTICES or world_class not in CLASSES:raise ValueError("unknown cell")
    rich=build(task,vertex,"null" if world_class=="null" else "valid")
    if world_class=="recoverable":rich=second_witness(rich,task,vertex)
    key=rule_key(rich)
    reserve=decoy_reserve(rich,task,len(rich[key])+2)
    latent=copy.deepcopy(rich)
    latent[key].extend(copy.deepcopy(reserve))
    if world_class!="null":
        primary=minimal_witnesses(build(task,vertex,"valid"))[0]
        primary_id=next(r["evidence_id"] for r in rich[key] if r["evidence_id"] in primary)
    else:
        primary_id=next(r["evidence_id"] for r in rich[key] if r["intervention"]=="u1")
    coarse=copy.deepcopy(rich)
    coarse[key]=[r for r in coarse[key] if r["evidence_id"]!=primary_id]
    sham=copy.deepcopy(rich)
    target_rules=[r for r in sham[key] if r["intervention"]=="u1"]
    sham[key]=[r for r in sham[key] if r["intervention"]!="u1"]
    sham[key].extend(copy.deepcopy(reserve[:len(target_rules)]))
    assert len(facts(rich))==len(facts(sham))
    assert facts(coarse).issubset(facts(rich))
    assert facts(sham).issubset(facts(latent))
    views={"rich":rich,"coarse":coarse,"sham_rich":sham}
    for view,p in views.items():
        p["archive_id"]=seal(task,"".join(vertex),world_class,view)
        assert not any(k in p for k in ("semantic","expected","world_class","view","retention_class"))
    actual=tuple(bool(minimal_witnesses(views[v])) for v in VIEWS)
    expected={"critical":(True,False,False),"recoverable":(True,True,False),
              "null":(False,False,False)}[world_class]
    assert actual==expected,(task,vertex,world_class,actual)
    return views

def census():
    count=0
    for task in TASKS:
        for v in VERTICES:
            for cls in CLASSES:
                assert set(projections(task,v,cls))==set(VIEWS)
                count+=3
    assert count==1152
    print("P69_RETENTION_CONSTRUCT_PASS packets=1152 latent_worlds=384 provider_calls=0")

if __name__=="__main__":census()
