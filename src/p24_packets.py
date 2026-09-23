from __future__ import annotations
import hashlib, random
from typing import Any
from p16_packets import worlds

SEED=20260924
TAG="P24-BOUNDARY-NORMAL-FORMS"
FAMILIES=("filler_only","rename_plus_filler","rename_plus_history","rename_plus_trace","rename_plus_relation")
SEMANTICS=("valid","null")

def oid(wid,fam,sem):
    return hashlib.sha256(f"{SEED}:{TAG}:{wid}:{fam}:{sem}".encode()).hexdigest()[:12]

def selected_worlds():
    return worlds()[:3]

def base(w):
    return {
        "claim":w.terminal_claim,
        "terminal_observation":{w.history_a:"T=stable",w.history_b:"T=stable"},
        "available_interventions":[w.intervention,"uX","uY"],
        "instructions":(
            "Using only this archive, propose the single strongest admissible experiment "
            "that could falsify the claim. If the archive does not justify a specific "
            "counterexample test, answer NONE. Do not speculate beyond retained evidence."
        ),
        "surface_domain":w.skin,
    }

def build(w,fam,sem):
    renamed=fam!="filler_only"
    key=(f"zeta24-{w.world_id.lower()}" if renamed else f"k24-{w.world_id.lower()}c")
    alt=f"{key}-alt"
    fillers=(["q9","q4"] if fam in {"filler_only","rename_plus_filler"} else ["p2","p3"])
    hA={"history":w.history_a,"trace":[key,*fillers]}
    hB={"history":w.history_b,"trace":[alt,*fillers]}
    target={
        "source":key,
        "intervention":w.intervention,
        "response_link":"history-sensitive" if sem=="valid" else "history-invariant",
    }
    distractor={
        "source":"decoy-z" if renamed else "distractor-c",
        "intervention":"uX","response_link":"irrelevant",
    }

    if fam=="rename_plus_history":
        histories=[hB,hA]
    elif fam=="rename_plus_trace":
        histories=[
            {"history":w.history_a,"trace":[*fillers,key]},
            {"history":w.history_b,"trace":[*fillers,alt]},
        ]
    else:
        histories=[hA,hB]

    relations=[target,distractor]
    if fam=="rename_plus_relation":
        relations=[distractor,target]

    p=base(w)
    p["retained_history"]=histories
    p["relation_notes"]=relations
    p["archive_id"]=oid(w.world_id,fam,sem)
    return p

def blinded_packets():
    rows=[]
    for w in selected_worlds():
        for fam in FAMILIES:
            for sem in SEMANTICS:
                rows.append({"packet_id":oid(w.world_id,fam,sem),"packet":build(w,fam,sem)})
    random.Random(SEED+24).shuffle(rows)
    return rows

def hidden_key():
    return {
        oid(w.world_id,fam,sem):{
            "world_id":w.world_id,
            "family":fam,
            "semantic_class":sem,
            "expected_specific_criticism":sem=="valid",
            "oracle_intervention":w.intervention,
            "oracle_direction":"different",
        }
        for w in selected_worlds() for fam in FAMILIES for sem in SEMANTICS
    }
