from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

COORDS=("R","F","H","T","L")
SEMANTICS=("valid","null")
SEED=20260924
TAG="P30-BALANCED-CROSSING"

@dataclass(frozen=True)
class ProspectiveWorld:
    world_id:str
    skin:str
    intervention:str
    history_a:str
    history_b:str
    terminal_claim:str="The retained terminal summary is sufficient to predict the challenge response."

PROSPECTIVE_WORLDS=(
    ProspectiveWorld("P30W01","measurement-pipeline","u2","p30h1a","p30h1b"),
    ProspectiveWorld("P30W02","measurement-pipeline","u3","p30h2a","p30h2b"),
    ProspectiveWorld("P30W03","analysis-pipeline","u3","p30h3a","p30h3b"),
    ProspectiveWorld("P30W04","analysis-pipeline","u4","p30h4a","p30h4b"),
    ProspectiveWorld("P30W05","sample-handling","u1","p30h5a","p30h5b"),
    ProspectiveWorld("P30W06","sample-handling","u4","p30h6a","p30h6b"),
)

def all_vertices():
    return tuple(frozenset(c) for n in range(6) for c in itertools.combinations(COORDS,n))

def label(v:frozenset[str])->str:
    return "I" if not v else "_".join(c for c in COORDS if c in v)

VERTICES=all_vertices()
VERTEX_ORDER=tuple(label(v) for v in VERTICES)

def _xor(a,b): return [x^y for x,y in zip(a,b)]

def additive_prediction_rows():
    recon=json.loads(Path("active/p29_reconstruction.json").read_text(encoding="utf-8"))
    assert tuple(recon["vertex_order"])==VERTEX_ORDER
    y={w:[int(b) for b in recon["worlds"][w]["row"]] for w in ("W01","W02","W03","W04","W05","W06")}
    zero=[0]*32
    a_m=zero
    b_u1=y["W01"]
    b_u4=y["W04"]
    a_a=_xor(y["W05"],b_u1)
    b_u2=_xor(y["W02"],a_a)
    a_s=_xor(y["W06"],b_u2)
    b_u3=_xor(y["W03"],a_s)
    rows={
      "P30W01":_xor(a_m,b_u2),
      "P30W02":_xor(a_m,b_u3),
      "P30W03":_xor(a_a,b_u3),
      "P30W04":_xor(a_a,b_u4),
      "P30W05":_xor(a_s,b_u1),
      "P30W06":_xor(a_s,b_u4),
    }
    return {w:"".join(map(str,row)) for w,row in rows.items()}

PREDICTED_FAILURE_ROWS=additive_prediction_rows()

def oid(world_id:str,vertex:frozenset[str],semantic:str)->str:
    return hashlib.sha256(f"{SEED}:{TAG}:{world_id}:{label(vertex)}:{semantic}".encode()).hexdigest()[:12]

def build_packet(w:ProspectiveWorld,vertex:frozenset[str],semantic:str)->dict[str,Any]:
    renamed="R" in vertex
    filler_renamed="F" in vertex
    reverse_histories="H" in vertex
    witness_last="T" in vertex
    reverse_relations="L" in vertex
    key=f"zeta30-{w.world_id.lower()}" if renamed else f"k30-{w.world_id.lower()}c"
    alt=f"{key}-alt"
    fillers=["q9","q4"] if filler_renamed else ["p2","p3"]
    def trace(token):
        return [*fillers,token] if witness_last else [token,*fillers]
    ha={"history":w.history_a,"trace":trace(key)}
    hb={"history":w.history_b,"trace":trace(alt)}
    histories=[hb,ha] if reverse_histories else [ha,hb]
    target={
      "source":key,
      "intervention":w.intervention,
      "response_link":"history-sensitive" if semantic=="valid" else "history-invariant",
    }
    distractor={"source":"decoy-z" if renamed else "distractor-c","intervention":"uX","response_link":"irrelevant"}
    relations=[distractor,target] if reverse_relations else [target,distractor]
    return {
      "archive_id":oid(w.world_id,vertex,semantic),
      "claim":w.terminal_claim,
      "terminal_observation":{w.history_a:"T=stable",w.history_b:"T=stable"},
      "available_interventions":[w.intervention,"uX","uY"],
      "instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.",
      "surface_domain":w.skin,
      "retained_history":histories,
      "relation_notes":relations,
    }

def blinded_packets():
    rows=[]
    for w in PROSPECTIVE_WORLDS:
        for v in VERTICES:
            for sem in SEMANTICS:
                rows.append({"packet_id":oid(w.world_id,v,sem),"packet":build_packet(w,v,sem)})
    import random
    random.Random(SEED+30).shuffle(rows)
    return rows

def hidden_key():
    out={}
    for w in PROSPECTIVE_WORLDS:
        pred=PREDICTED_FAILURE_ROWS[w.world_id]
        for i,v in enumerate(VERTICES):
            for sem in SEMANTICS:
                out[oid(w.world_id,v,sem)]={
                  "world_id":w.world_id,
                  "skin":w.skin,
                  "intervention_context":w.intervention,
                  "vertex":label(v),
                  "semantic_class":sem,
                  "expected_specific_criticism":sem=="valid",
                  "oracle_intervention":w.intervention,
                  "oracle_direction":"different",
                  "predicted_additive_selective_pass":pred[i]=="0",
                }
    return out

def self_audit():
    observed={
      ("measurement-pipeline","u1"),("measurement-pipeline","u4"),
      ("analysis-pipeline","u2"),("analysis-pipeline","u1"),
      ("sample-handling","u3"),("sample-handling","u2"),
    }
    fresh={(w.skin,w.intervention) for w in PROSPECTIVE_WORLDS}
    full={(s,u) for s in ("measurement-pipeline","analysis-pipeline","sample-handling") for u in ("u1","u2","u3","u4")}
    assert observed|fresh==full and not observed&fresh
    assert len(PREDICTED_FAILURE_ROWS)==6
    assert all(len(x)==32 for x in PREDICTED_FAILURE_ROWS.values())
    assert len(blinded_packets())==384
    return True
