from __future__ import annotations

import hashlib,itertools,random
from dataclasses import dataclass
from typing import Any

SEED=20260925
TAG="P37-ORTHOGONAL-IDENTIFIER-CHANNEL"
COORDS=("R","F","H","T","L")
SEMANTICS=("valid","null")
PROFILES=((0,0,0,0),(0,1,0,1),(1,1,1,1))
BASE_ARM=(0,0)
ARMS=((0,0),(1,0),(0,1),(1,1))

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

ANCHOR=Context("measurement","measurement-pipeline")
EXTERNAL=(Context("analysis","analysis-pipeline"),Context("sample","sample-handling"))

def vertices():
    return tuple(frozenset(c) for n in range(6) for c in itertools.combinations(COORDS,n))
VERTICES=vertices()

def label(v:frozenset[str])->str:
    return "I" if not v else "_".join(c for c in COORDS if c in v)
assert [label(v) for v in VERTICES]==VERTEX_ORDER

def profile_label(p): return "".join(map(str,p))
def arm_label(a): return f"A{a[0]}N{a[1]}"

def construction_ids(profile,renamed,namespace_arm):
    S,P,L,D=profile
    sep="_" if D else "-"
    nonce="q7v4m9p2" if L else "q7"
    stem="nexus" if S else "source"
    # Matched-length namespace families. R changes k/z, N changes a/b.
    fam="b" if namespace_arm else "a"
    rep=("z" if renamed else "k")+fam+"37"
    key=f"{rep}{sep}{stem}{sep}{nonce}"
    alt=f"{key}{sep}alt"
    if P:
        common=f"hist{sep}{nonce}"
        ha=f"{common}{sep}a" + (f"{sep}nexus" if S else "")
        hb=f"{common}{sep}b{sep}omega"
    else:
        ha=f"alpha{sep}{nonce}" + (f"{sep}nexus" if S else "")
        hb=f"omega{sep}{nonce}{sep}b"
    return key,alt,ha,hb

def archive_id(profile,v,semantic,archive_arm):
    # Both arms have equal visible length. A1 varies by matched packet but NOT by context.
    if archive_arm==0:
        return "ar37-000000000000"
    raw=f"{TAG}:{profile_label(profile)}:{label(v)}:{semantic}".encode()
    return "ar37-"+hashlib.sha256(raw).hexdigest()[:12]

def tracking_id(context,profile,arm,v,semantic):
    raw=f"{SEED}:{TAG}:{context.name}:{profile_label(profile)}:{arm_label(arm)}:{label(v)}:{semantic}".encode()
    return hashlib.sha256(raw).hexdigest()[:14]

def build_packet(context:Context,profile,arm,v,semantic)->dict[str,Any]:
    A,N=arm
    renamed="R" in v
    filler_renamed="F" in v
    reverse_histories="H" in v
    witness_last="T" in v
    reverse_relations="L" in v

    key,alt,ha_id,hb_id=construction_ids(profile,renamed,N)
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
      "archive_id":archive_id(profile,v,semantic,A),
      "claim":"The retained terminal summary is sufficient to predict the challenge response.",
      "terminal_observation":{ha_id:"T=stable",hb_id:"T=stable"},
      "available_interventions":[context.intervention,"uX","uY"],
      "instructions":"Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.",
      "surface_domain":context.skin,
      "retained_history":histories,
      "relation_notes":relations,
    }

def packets_for(context,profiles,arms):
    rows=[]
    for p in profiles:
        for arm in arms:
            for v in VERTICES:
                for sem in SEMANTICS:
                    rows.append({
                      "packet_id":tracking_id(context,p,arm,v,sem),
                      "context":context.name,
                      "profile":profile_label(p),
                      "arm":arm_label(arm),
                      "vertex":label(v),
                      "semantic_class":sem,
                      "packet":build_packet(context,p,arm,v,sem),
                    })
    return rows

def phase_a_packets():
    rows=packets_for(ANCHOR,PROFILES,ARMS)
    random.Random(SEED+371).shuffle(rows)
    return rows

def phase_b_packets():
    rows=[]
    for c in EXTERNAL:
        rows.extend(packets_for(c,PROFILES,(BASE_ARM,)))
    random.Random(SEED+372).shuffle(rows)
    return rows

def phase_c_packets():
    target_arms=tuple(a for a in ARMS if a!=BASE_ARM)
    rows=[]
    for c in EXTERNAL:
        rows.extend(packets_for(c,PROFILES,target_arms))
    random.Random(SEED+373).shuffle(rows)
    return rows

def self_audit():
    assert len(phase_a_packets())==3*4*32*2
    assert len(phase_b_packets())==2*3*1*32*2
    assert len(phase_c_packets())==2*3*3*32*2

    # Orthogonality checks: A changes archive_id only; N changes namespace-bearing content only.
    p=PROFILES[1]; v=frozenset({"R","H"})
    x00=build_packet(ANCHOR,p,(0,0),v,"valid")
    x10=build_packet(ANCHOR,p,(1,0),v,"valid")
    diffa={k for k in x00 if x00[k]!=x10[k]}
    assert diffa=={"archive_id"}

    x01=build_packet(ANCHOR,p,(0,1),v,"valid")
    diffn={k for k in x00 if x00[k]!=x01[k]}
    assert diffn=={"retained_history","relation_notes"}

    # Matched packet across contexts differs only by surface_domain for every arm.
    for arm in ARMS:
        a=build_packet(ANCHOR,p,arm,v,"valid")
        b=build_packet(EXTERNAL[0],p,arm,v,"valid")
        assert {k for k in a if a[k]!=b[k]}=={"surface_domain"}

    # Archive A1 value is matched across contexts.
    for arm in ARMS:
        assert build_packet(ANCHOR,p,arm,v,"valid")["archive_id"]==build_packet(EXTERNAL[1],p,arm,v,"valid")["archive_id"]
    return True
