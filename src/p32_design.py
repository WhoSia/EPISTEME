from __future__ import annotations

import hashlib
import itertools
import random
from dataclasses import dataclass
from typing import Any

SEED=20260924
TAG="P32-BALANCED-CELL-FRESH-WORLD-REPLICATION"
COORDS=("R","F","H","T","L")
SEMANTICS=("valid","null")

VERTEX_ORDER=[
"I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L",
"R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L",
"R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"
]

CANONICAL_ROWS={
("measurement-pipeline","u1"):"01100001100001011000000100011010",
("measurement-pipeline","u2"):"00000011000111010000000010000000",
("measurement-pipeline","u3"):"10000001001111110101010111010100",
("measurement-pipeline","u4"):"00010000000010100001101001000101",
("analysis-pipeline","u1"):"01011010110000001011010001100010",
("analysis-pipeline","u2"):"01100110010100101000001101010101",
("analysis-pipeline","u3"):"00001100100001110100000111101110",
("analysis-pipeline","u4"):"00110101110111110001000001110001",
("sample-handling","u1"):"01010001100000010100001010001000",
("sample-handling","u2"):"00011001010010100011110011010110",
("sample-handling","u3"):"00010000000001001001000001001000",
("sample-handling","u4"):"00100000000011010000000101011000",
}

@dataclass(frozen=True)
class FreshWorld:
    world_id:str
    skin:str
    intervention:str
    history_a:str
    history_b:str
    terminal_claim:str="The retained terminal summary is sufficient to predict the challenge response."

FRESH_WORLDS=(
 FreshWorld("P32W01","measurement-pipeline","u1","p32h01a","p32h01b"),
 FreshWorld("P32W02","measurement-pipeline","u2","p32h02a","p32h02b"),
 FreshWorld("P32W03","measurement-pipeline","u3","p32h03a","p32h03b"),
 FreshWorld("P32W04","measurement-pipeline","u4","p32h04a","p32h04b"),
 FreshWorld("P32W05","analysis-pipeline","u1","p32h05a","p32h05b"),
 FreshWorld("P32W06","analysis-pipeline","u2","p32h06a","p32h06b"),
 FreshWorld("P32W07","analysis-pipeline","u3","p32h07a","p32h07b"),
 FreshWorld("P32W08","analysis-pipeline","u4","p32h08a","p32h08b"),
 FreshWorld("P32W09","sample-handling","u1","p32h09a","p32h09b"),
 FreshWorld("P32W10","sample-handling","u2","p32h10a","p32h10b"),
 FreshWorld("P32W11","sample-handling","u3","p32h11a","p32h11b"),
 FreshWorld("P32W12","sample-handling","u4","p32h12a","p32h12b"),
)

def vertices():
    return tuple(frozenset(c) for n in range(6) for c in itertools.combinations(COORDS,n))

VERTICES=vertices()

def label(v:frozenset[str])->str:
    return "I" if not v else "_".join(c for c in COORDS if c in v)

assert [label(v) for v in VERTICES]==VERTEX_ORDER

def oid(world_id:str,v:frozenset[str],semantic:str)->str:
    return hashlib.sha256(f"{SEED}:{TAG}:{world_id}:{label(v)}:{semantic}".encode()).hexdigest()[:12]

def build_packet(w:FreshWorld,v:frozenset[str],semantic:str)->dict[str,Any]:
    renamed="R" in v
    filler_renamed="F" in v
    reverse_histories="H" in v
    witness_last="T" in v
    reverse_relations="L" in v

    key=f"zeta32-{w.world_id.lower()}" if renamed else f"k32-{w.world_id.lower()}c"
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
    distractor={
      "source":"decoy-z" if renamed else "distractor-c",
      "intervention":"uX",
      "response_link":"irrelevant",
    }
    relations=[distractor,target] if reverse_relations else [target,distractor]

    return {
      "archive_id":oid(w.world_id,v,semantic),
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
    for w in FRESH_WORLDS:
        for v in VERTICES:
            for sem in SEMANTICS:
                rows.append({"packet_id":oid(w.world_id,v,sem),"packet":build_packet(w,v,sem)})
    random.Random(SEED+32).shuffle(rows)
    return rows

def hidden_key():
    out={}
    for w in FRESH_WORLDS:
        expected=CANONICAL_ROWS[(w.skin,w.intervention)]
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
                  "canonical_cell_pass":expected[i]=="0",
                }
    return out

def self_audit():
    assert len(FRESH_WORLDS)==12
    assert len(CANONICAL_ROWS)==12
    assert len(blinded_packets())==12*32*2
    assert all(len(r)==32 and set(r)<=set("01") for r in CANONICAL_ROWS.values())
    assert {(w.skin,w.intervention) for w in FRESH_WORLDS}==set(CANONICAL_ROWS)
    return True
