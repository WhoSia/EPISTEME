"""P69 human adjudication exporter; preview is NOT a cryptographic blind.

Production export requires a secret high-entropy local hex key, kept off GitHub.
The sealed answer key is written only when --private-key is used locally.
Never upload the sealed key to a public GitHub Actions artifact.
"""
from __future__ import annotations
import argparse,copy,hashlib,hmac,json,random
from pathlib import Path
from p69_task_factory import TASKS,VERTICES
from p69_retention_controls import CLASSES,VIEWS,projections
from p69_witness_enumerator import minimal_witnesses

IDENTIFIER_KEYS={"archive_id","focus_object","object_ref","trace_ref","node","from_node","to_node",
                 "trigger_ref","gate_ref","evidence_id","measurement_ref"}

def pseudonym(key,salt,value):
    message=(salt+"|"+value).encode()
    digest=(hmac.new(key,message,hashlib.sha256).hexdigest() if key is not None
            else hashlib.sha256(("PREVIEW|"+salt+"|"+value).encode()).hexdigest())
    return "id-"+digest[:22]

def opaque_copy(packet,salt,key):
    p=copy.deepcopy(packet)
    ids=set()
    def collect(node,field=None):
        if isinstance(node,dict):
            for k,v in node.items():collect(v,k)
        elif isinstance(node,list):
            for v in node:collect(v,field)
        elif isinstance(node,str) and field in IDENTIFIER_KEYS|{"trace","requires_all"}:
            ids.add(node)
    collect(p)
    mapping={v:pseudonym(key,salt,v) for v in sorted(ids)}
    assert len(set(mapping.values()))==len(mapping)
    def rewrite(node):
        if isinstance(node,dict):return {k:rewrite(v) for k,v in node.items()}
        if isinstance(node,list):return [rewrite(x) for x in node]
        if isinstance(node,str):return mapping.get(node,node)
        return node
    return rewrite(p)

def build(*,key=None,preview=False):
    if (key is None)==(not preview):raise ValueError("choose exactly one of secret key and preview")
    if key is not None and len(key)<32:raise ValueError("at least 32 secret random bytes needed")
    public=[];private=[]
    for ti,task in enumerate(TASKS):
        for ci,cls in enumerate(CLASSES):
            vi=(ti*5+ci*3)%len(VERTICES)
            variants=projections(task,VERTICES[vi],cls)
            for wi,view in enumerate(VIEWS):
                raw=f"P69|{task}|{ci}|{wi}"
                case_id="P69"+(hmac.new(key,raw.encode(),hashlib.sha256).hexdigest()[:20]
                    if key is not None else "PRE"+hashlib.sha256(raw.encode()).hexdigest()[:20])
                packet=opaque_copy(variants[view],"CASE-"+case_id,key)
                proofs=minimal_witnesses(packet)
                assert bool(proofs)==bool(minimal_witnesses(variants[view]))
                public.append({"case_id":case_id,"archive":packet,
                    "annotation":{"challenge_exists":None,"rationale_ids":None,
                        "intervention":None,"predicted_direction":None}})
                private.append({"case_id":case_id,"task":task,"class":cls,"view":view,
                    "expected_challenge":bool(proofs),
                    "minimal_rationale_sets":[sorted(s) for s in proofs]})
    # In production the public shuffle also depends on a secret; the preview
    # is deliberately reproducible but MUST NOT be called blinded evidence.
    order_seed=int.from_bytes(hmac.new(key,b"ORDER",hashlib.sha256).digest()[:8],"big") if key else 690069
    random.Random(order_seed).shuffle(public)
    assert len(public)==len(private)==72
    assert len({r["case_id"] for r in public})==72
    assert not any({"class","view","expected_challenge","minimal_rationale_sets"}&set(r) for r in public)
    return public,private

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--public",required=True)
    ap.add_argument("--preview",action="store_true",help="deterministic public PREVIEW, not blinded evaluation")
    ap.add_argument("--secret-file",default=None,help="private file containing >=32 random bytes as hex")
    ap.add_argument("--private-key",default=None,help="sealed matching ground truth; local use ONLY")
    args=ap.parse_args()
    if args.preview==bool(args.secret_file):ap.error("specify exactly --preview or --secret-file")
    if args.preview and args.private_key:ap.error("private evaluation keys require --secret-file")
    key=None
    if args.secret_file:
        key=bytes.fromhex(Path(args.secret_file).read_text().strip())
        if len(key)<32:ap.error("insufficient key entropy length")
    cases,groundtruth=build(key=key,preview=args.preview)
    p=Path(args.public);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text("".join(json.dumps(c,sort_keys=True)+"\n" for c in cases))
    print(("P69_PREVIEW_ONLY_PASS" if args.preview else "P69_SECRET_BLIND_PACK_PASS")
          +" cases=72 provider_calls=0")
    if args.private_key:
        p=Path(args.private_key);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in groundtruth))
        print("PRIVATE_GROUND_TRUTH_WRITTEN_LOCAL_ONLY")

if __name__=="__main__":main()
