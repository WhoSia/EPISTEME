from __future__ import annotations

import hashlib
import itertools
import random
from dataclasses import dataclass
from typing import Any

SEED=20260924
TAG="P35-CONFOUND-STRIPPED-CONSTRUCTION-TRANSPORT"
COORDS=("R","F","H","T","L")
SEMANTICS=("valid","null")
PROFILES=tuple(itertools.product((0,1),repeat=4))
EXTERNAL_TEST_PROFILES=((0,1,0,1),(1,0,1,0),(1,1,1,1))
BASELINE_PROFILE=(0,0,0,0)
CONSTANT_ARCHIVE_ID="P35-CONSTANT-ARCHIVE"

VERTEX_ORDER=[
"I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L",
"R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L",
"R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"
]

@dataclass(frozen=True)
class Context:
    name:str
    skin:str
    intervention:str="u1"

ANCHOR=Context("anchor","measurement-pipeline")
EXTERNAL=(Context("analysis","analysis-pipeline"),Context("sample","sample-handling"))

def vertices():
    return tuple(frozenset(c) for n in range(6) for c in itertools.combinations(COORDS,n))
VERTICES=vertices()

def label(v:frozenset[str])->str:
    return "I" if not v else "_".join(c for c in COORDS if c in v)
assert [label(v) for v in VERTICES]==VERTEX_ORDER

def profile_label(p): return "".join(map(str,p))

def identifiers(profile:tuple[int,int,int,int], renamed:bool):
    S,P,L,D=profile
    sep="_" if D else "-"
    nonce="q7v4m9p2" if L else "q7"
    stem="nexus" if S else "source"
    rep="zeta35" if renamed else "k35"
    key=f"{rep}{sep}{stem}{sep}{nonce}"
    alt=f"{key}{sep}alt"
    if P:
        common=f"hist{sep}{nonce}"
        ha=f"{common}{sep}a" + (f"{sep}nexus" if S else "")
        hb=f"{common}{sep}b{sep}omega"
    else:
        ha=f"alpha{sep}{nonce}" + (f"{sep}nexus" if S else "")
        hb=f"omega{sep}{nonce}{sep}b"
    return key,alt,ha,hb,sep

def tracking_id(context:Context,profile,v,semantic):
    raw=f"{SEED}:{TAG}:{context.name}:{profile_label(profile)}:{label(v)}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:14]

def build_packet(context:Context,profile,v,semantic)->dict[str,Any]:
    renamed="R" in v
    filler_renamed="F" in v
    reverse_histories="H" in v
    witness_last="T" in v
    reverse_relations="L" in v
    key,alt,ha_id,hb_id,sep=identifiers(profile,renamed)
    fillers=["q9","q4"] if filler_renamed else ["p2","p3"]
    def trace(token):
        return [*fillers,token] if witness_last else [token,*fillers]
    ha={"history":ha_id,"trace":trace(key)}
    hb={"history":hb_id,"trace":trace(alt)}
    histories=[hb,ha] if reverse_histories else [ha,hb]
    target={
      "source":key,
      "intervention":context.intervention,
      "response_link":"history-sensitive" if semantic=="valid" else "history-invariant",
    }
    distractor={
      "source":"decoy-z" if renamed else "distractor-c",
      "intervention":"uX",
      "response_link":"irrelevant",
    }
    relations=[distractor,target] if reverse_relations else [target,distractor]
    return {
      "archive_id":CONSTANT_ARCHIVE_ID,
      "claim":"The retained terminal summary is sufficient to predict the challenge response.",
      "terminal_observation":{ha_id:"T=stable",hb_id:"T=stable"},
      "available_interventions":[context.intervention,"uX","uY"],
      "instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.",
      "surface_domain":context.skin,
      "retained_history":histories,
      "relation_notes":relations,
    }

def packets_for(context:Context,profiles):
    rows=[]
    for p in profiles:
        for v in VERTICES:
            for sem in SEMANTICS:
                rows.append({
                  "packet_id":tracking_id(context,p,v,sem),
                  "context":context.name,
                  "profile":profile_label(p),
                  "vertex":label(v),
                  "semantic_class":sem,
                  "packet":build_packet(context,p,v,sem),
                })
    return rows

def phase_a_packets():
    rows=packets_for(ANCHOR,PROFILES)
    random.Random(SEED+351).shuffle(rows)
    return rows

def phase_b_packets():
    rows=[]
    for c in EXTERNAL: rows.extend(packets_for(c,(BASELINE_PROFILE,)))
    random.Random(SEED+352).shuffle(rows)
    return rows

def phase_c_packets():
    rows=[]
    for c in EXTERNAL: rows.extend(packets_for(c,EXTERNAL_TEST_PROFILES))
    random.Random(SEED+353).shuffle(rows)
    return rows

def self_audit():
    assert len(phase_a_packets())==16*32*2
    assert len(phase_b_packets())==2*32*2
    assert len(phase_c_packets())==2*3*32*2
    # Same construction profile is byte-identical across contexts except surface_domain.
    p=(1,0,1,0); v=frozenset({"R","H"})
    a=build_packet(ANCHOR,p,v,"valid")
    b=build_packet(EXTERNAL[0],p,v,"valid")
    diffs={k for k in a if a[k]!=b[k]}
    assert diffs=={"surface_domain"}
    assert all(build_packet(ANCHOR,p,frozenset(),"valid")["archive_id"]==CONSTANT_ARCHIVE_ID for p in PROFILES)
    return True
