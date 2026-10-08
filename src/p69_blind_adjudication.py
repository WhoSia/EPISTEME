"""P69 blinded independent-adjudication packet export (no hosted provider calls).

Outputs 72 public annotation cases; a private oracle may only be generated
locally with explicit --private-key. Never upload the private key as Action
artifact or commit it to a public repository.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,random
from pathlib import Path
from p69_task_factory import TASKS,VERTICES
from p69_retention_controls import CLASSES,VIEWS,projections
from p69_witness_enumerator import minimal_witnesses

IDENTIFIER_KEYS={"archive_id","focus_object","object_ref","trace_ref","node","from_node","to_node",
                 "trigger_ref","gate_ref","evidence_id","measurement_ref"}
def hash_id(salt,value):
    return "id-"+hashlib.sha256((salt+"|"+value).encode()).hexdigest()[:18]

def opaque_copy(packet,salt):
    p=copy.deepcopy(packet)
    identifiers=set()
    def collect(node,key=None):
        if isinstance(node,dict):
            for k,v in node.items():collect(v,k)
        elif isinstance(node,list):
            for item in node:collect(item,key)
        elif isinstance(node,str) and key in IDENTIFIER_KEYS:
            identifiers.add(node)
        elif isinstance(node,str) and key in ("trace","requires_all"):
            identifiers.add(node)
    collect(p)
    mapping={x:hash_id(salt,x) for x in sorted(identifiers)}
    assert len(set(mapping.values()))==len(mapping)
    def rewrite(node):
        if isinstance(node,dict):return {k:rewrite(v) for k,v in node.items()}
        if isinstance(node,list):return [rewrite(x) for x in node]
        if isinstance(node,str):return mapping.get(node,node)
        return node
    return rewrite(p)

def build():
    public=[];private=[]
    for ti,task in enumerate(TASKS):
        for ci,cls in enumerate(CLASSES):
            vi=(ti*5+ci*3)%len(VERTICES)
            variants=projections(task,VERTICES[vi],cls)
            for wi,view in enumerate(VIEWS):
                source=variants[view]
                case_id="PA"+hashlib.sha256(f"P69|{task}|{ci}|{wi}".encode()).hexdigest()[:14]
                anonymized=opaque_copy(source,"P69-ADJ-"+case_id)
                proofsets=minimal_witnesses(anonymized)
                assert bool(proofsets)==bool(minimal_witnesses(source))
                public.append({"case_id":case_id,"archive":anonymized,
                    "annotation":{"challenge_exists":None,"rationale_ids":None,
                        "intervention":None,"predicted_direction":None}})
                private.append({"case_id":case_id,"task":task,"class":cls,"view":view,
                    "expected_challenge":bool(proofsets),
                    "minimal_rationale_sets":[sorted(s) for s in proofsets]})
    rng=random.Random(690069)
    rng.shuffle(public)
    assert len(public)==len(private)==72
    assert len({z["case_id"] for z in public})==72
    public_ids=[z["case_id"] for z in public]
    assert not any(("class" in item or "view" in item or "expected_challenge" in item) for item in public)
    return public,private

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--public",required=True)
    ap.add_argument("--private-key",default=None)
    args=ap.parse_args()
    cases,key=build()
    path=Path(args.public);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("".join(json.dumps(c,sort_keys=True)+"\n" for c in cases))
    print("P69_BLIND_PACKET_EXPORT_PASS public_cases=72 provider_calls=0")
    if args.private_key:
        path=Path(args.private_key);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text("".join(json.dumps(c,sort_keys=True)+"\n" for c in key))
        print("PRIVATE_KEY_CREATED_LOCALLY_ONLY_DO_NOT_PUBLISH")

if __name__=="__main__":main()
