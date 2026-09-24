from __future__ import annotations

import hashlib
import itertools
import random
from dataclasses import dataclass
from typing import Any

SEED=20260924
TAG="P34-PROSPECTIVE-WORLD-INSTANCE-INSTRUMENTATION"
COORDS=("R","F","H","T","L")
SEMANTICS=("valid","null")
INSTANCE_FACTORS=("S","P","L","D")

ANCHOR_CONTEXT=("measurement-pipeline","u1")
ANCHOR_ROW="01100001100001011000000100011010"

VERTEX_ORDER=[
"I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L",
"R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L",
"R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"
]

# Holdout chosen prospectively. The remaining 12 points have full GF(2)
# rank 11 under the complete quadratic feature map [1, four mains, six pairs].
HOLDOUT_PROFILES={
    (0,0,0,0),
    (0,0,1,1),
    (0,1,0,1),
    (1,1,1,0),
}

@dataclass(frozen=True)
class InstrumentedWorld:
    world_id:str
    profile:tuple[int,int,int,int]
    skin:str
    intervention:str
    separator:str
    nonce:str
    key_core:str
    history_a:str
    history_b:str
    terminal_claim:str="The retained terminal summary is sufficient to predict the challenge response."

def make_world(i:int, profile:tuple[int,int,int,int])->InstrumentedWorld:
    S,P,L,D=profile
    sep="_" if D else "-"
    nonce=("q7v4m9p2" if L else "q7")

    # S: source/history-A shared stem.
    key_core=(f"nexus{sep}{nonce}" if S else f"source{sep}{nonce}")

    # P: history-pair prefix overlap. S is implemented independently by
    # inserting the source stem only into history A.
    if P:
        common=f"hist{sep}{nonce}"
        ha=f"{common}{sep}a" + (f"{sep}nexus" if S else "")
        hb=f"{common}{sep}b{sep}omega"
    else:
        ha=f"alpha{sep}{nonce}" + (f"{sep}nexus" if S else "")
        hb=f"omega{sep}{nonce}{sep}b"

    return InstrumentedWorld(
        world_id=f"P34W{i:02d}",
        profile=profile,
        skin=ANCHOR_CONTEXT[0],
        intervention=ANCHOR_CONTEXT[1],
        separator=sep,
        nonce=nonce,
        key_core=key_core,
        history_a=ha,
        history_b=hb,
    )

PROFILES=tuple(itertools.product((0,1),repeat=4))
WORLDS=tuple(make_world(i+1,p) for i,p in enumerate(PROFILES))
TRAIN_WORLDS=tuple(w for w in WORLDS if w.profile not in HOLDOUT_PROFILES)
HOLDOUT_WORLDS=tuple(w for w in WORLDS if w.profile in HOLDOUT_PROFILES)

def vertices():
    return tuple(frozenset(c) for n in range(6) for c in itertools.combinations(COORDS,n))
VERTICES=vertices()

def label(v:frozenset[str])->str:
    return "I" if not v else "_".join(c for c in COORDS if c in v)
assert [label(v) for v in VERTICES]==VERTEX_ORDER

def oid(world_id:str,v:frozenset[str],semantic:str)->str:
    return hashlib.sha256(f"{SEED}:{TAG}:{world_id}:{label(v)}:{semantic}".encode()).hexdigest()[:12]

def build_packet(w:InstrumentedWorld,v:frozenset[str],semantic:str)->dict[str,Any]:
    renamed="R" in v
    filler_renamed="F" in v
    reverse_histories="H" in v
    witness_last="T" in v
    reverse_relations="L" in v

    rep_prefix="zeta34" if renamed else "k34"
    key=f"{rep_prefix}{w.separator}{w.key_core}"
    alt=f"{key}{w.separator}alt"
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
    for w in WORLDS:
        for v in VERTICES:
            for sem in SEMANTICS:
                rows.append({"packet_id":oid(w.world_id,v,sem),"packet":build_packet(w,v,sem)})
    random.Random(SEED+34).shuffle(rows)
    return rows

def _common_prefix_len(a:str,b:str)->int:
    n=0
    for x,y in zip(a,b):
        if x!=y: break
        n+=1
    return n

def _tokens(s:str)->set[str]:
    return set(s.replace("_","-").split("-"))

def feature_census():
    out={}
    for w in WORLDS:
        # census is entirely response-blind and computed from emitted identifiers.
        source=f"k34{w.separator}{w.key_core}"
        ha, hb=w.history_a,w.history_b
        out[w.world_id]={
          "profile":{"S":w.profile[0],"P":w.profile[1],"L":w.profile[2],"D":w.profile[3]},
          "split":"holdout" if w.profile in HOLDOUT_PROFILES else "train",
          "source_id":source,
          "history_a":ha,
          "history_b":hb,
          "source_length":len(source),
          "history_a_length":len(ha),
          "history_b_length":len(hb),
          "history_common_prefix_chars":_common_prefix_len(ha,hb),
          "source_history_a_token_overlap":len(_tokens(source)&_tokens(ha)),
          "source_history_b_token_overlap":len(_tokens(source)&_tokens(hb)),
          "separator":w.separator,
        }
    return out

def quadratic_features(profile):
    S,P,L,D=profile
    xs=(S,P,L,D)
    return [1,*xs,*[xs[i]*xs[j] for i in range(4) for j in range(i+1,4)]]

def main_features(profile):
    return [1,*profile]

def gf2_rank(rows):
    a=[list(r) for r in rows]
    m=len(a); n=len(a[0]); rank=0
    for col in range(n):
        p=next((i for i in range(rank,m) if a[i][col]),None)
        if p is None: continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(m):
            if i!=rank and a[i][col]:
                a[i]=[x^y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def self_audit():
    assert len(WORLDS)==16 and len(TRAIN_WORLDS)==12 and len(HOLDOUT_WORLDS)==4
    assert len(blinded_packets())==16*32*2
    assert gf2_rank([quadratic_features(w.profile) for w in TRAIN_WORLDS])==11
    assert gf2_rank([main_features(w.profile) for w in TRAIN_WORLDS])==5
    c=feature_census()
    assert len(c)==16
    return True
