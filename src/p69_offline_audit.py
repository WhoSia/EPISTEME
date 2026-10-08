"""P69 hosted-provider-free integration court. All checks are deterministic."""
import copy,hashlib,itertools,json,random
from p69_task_factory import TASKS,PILOT_TASKS,VERTICES,SEMANTICS,build,canonical_json
from p69_independent_scorer import proof,score,oracle_response

def run():
    assert len(TASKS)==8 and len(VERTICES)==16 and len(set(VERTICES))==16
    assert not set(TASKS)&set(PILOT_TASKS)
    assert len({f for f,_ in (t.rsplit('_',1) for t in TASKS)})==4
    assertions=0
    for task in TASKS+PILOT_TASKS:
        for v in VERTICES:
            for sem in SEMANTICS:
                p=build(task,v,sem)
                assert ('semantic' not in p and 'expected' not in p and task not in canonical_json(p))
                found=proof(p);assert (found is not None)==(sem=="valid")
                assert score(p,oracle_response(p))["semantic_correct"] is True
                assert score(p,"NONE")["semantic_correct"] is None
                alt=copy.deepcopy(p)
                for value in alt.values():
                    if isinstance(value,list) and value and isinstance(value[0],dict):
                        random.Random(6900+len(task)+len(v)).shuffle(value)
                assert (proof(alt) is not None)==(found is not None)
                assert score(alt,oracle_response(alt))["semantic_correct"]
                assertions+=1
                if task not in TASKS or sem!="valid":continue
                # Remove one indispensable step and require loss of admissibility.
                family=task.rsplit("_",1)[0]
                if family=="provenance":
                    for rule in alt["response_rules"]:
                        if rule["intervention"]=="u1":rule["contrast"]="same"
                elif family=="composition":
                    alt["transition_edges"]=[edge for edge in alt["transition_edges"] if edge["evidence_id"] not in found]
                elif family=="guarded":
                    for gate in alt["gate_states"]:
                        if gate["evidence_id"] in found:gate["enabled"]=False
                else:
                    for rule in alt["calibration_rules"]:
                        if rule["intervention"]=="u1":rule["gain"]=1;rule["offset"]=0
                assert proof(alt) is None,(task,v)
                assert not score(alt,oracle_response(p))["semantic_correct"]
                fabricated=json.loads(oracle_response(p))
                fabricated["rationale_ids"]=["outside_oracle"]
                assert score(p,json.dumps(fabricated))["semantic_correct"] is False
    assert assertions==320
    for op in ("R","T"):
        pairs=0;universe=set(VERTICES)
        for v in VERTICES:
            if op not in v and tuple(x for x in "RFHTL" if x in set(v)|{op}) in universe:
                pairs+=1
        assert pairs==8,(op,pairs)
    size=2*8*16*2*2*8
    assert size==8192
    hashes={canonical_json(build(t,v,s)) for t,v,s in itertools.product(TASKS,VERTICES,SEMANTICS)}
    assert len(hashes)==256
    print("P69_INDEPENDENT_SCORER_AND_FACTORY_PASS")
    print("main=256 packet oracles; pilot=64 separate packet oracles")
    print("oracle tamper controls=128; fake evidence controls=128")
    print("R_pairs=8 T_pairs=8 planned_hosted_requests=8192 provider_calls=0")
if __name__=="__main__":
    run()
    from p69_retention_selftest import run as run_retention_court
    run_retention_court()

