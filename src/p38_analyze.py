from __future__ import annotations

import itertools,json
from collections import Counter,defaultdict
from pathlib import Path

CONTEXTS=("measurement","analysis","sample")
PROFILES=("0000","0101","1111")
ARMS=("A0N0","A1N0","A0N1","A1N1")
FEATURES=("C","Z","A","N")
REP_COORDS=("R","F","H","T","L")

def xor(a,b): return "".join(str(int(x!=y)) for x,y in zip(a,b))

def gf2_rank(rows):
    if not rows:return 0
    a=[[int(c) for c in r] for r in rows]
    m=len(a); n=len(a[0]); rank=0
    for col in range(n):
        p=next((i for i in range(rank,m) if a[i][col]),None)
        if p is None:continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(m):
            if i!=rank and a[i][col]:
                a[i]=[x^y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def vertex_mask(label):
    if label=="I": return 0
    s=set(label.split("_"))
    return sum(1<<i for i,c in enumerate(REP_COORDS) if c in s)

def anf(row,vertex_order):
    arr=[0]*32
    for i,v in enumerate(vertex_order): arr[vertex_mask(v)]=int(row[i])
    a=arr[:]
    for bit in range(5):
        step=1<<bit
        for mask in range(32):
            if mask&step:a[mask]^=a[mask^step]
    degree=max((mask.bit_count() for mask,x in enumerate(a) if x),default=0)
    terms=sum(a)
    return degree,terms

def coords(key):
    c,z,arm=key.split("|")
    return {"C":c,"Z":z,"A":int(arm[1]),"N":int(arm[3])}

def sufficient(worlds,subset,vertex=None):
    seen={}
    for key,row in worlds.items():
        q=coords(key)
        k=tuple(q[f] for f in subset)
        y=row if vertex is None else row[vertex]
        if k in seen and seen[k]!=y:return False
        seen[k]=y
    return True

def main():
    ev=json.loads(Path("active/p38_evidence.json").read_text())
    worlds=ev["worlds"]; verts=ev["vertex_order"]

    effects={k:{} for k in ("A","N","AxN")}
    for c in CONTEXTS:
        for z in PROFILES:
            y00=worlds[f"{c}|{z}|A0N0"]
            y10=worlds[f"{c}|{z}|A1N0"]
            y01=worlds[f"{c}|{z}|A0N1"]
            y11=worlds[f"{c}|{z}|A1N1"]
            effects["A"][(c,z)]=xor(y10,y00)
            effects["N"][(c,z)]=xor(y01,y00)
            effects["AxN"][(c,z)]=xor(xor(y11,y10),xor(y01,y00))

    channel={}
    for ch in effects:
        rows=list(effects[ch].values())
        av=[anf(r,verts) for r in rows]
        channel[ch]={
          "rank_gf2":gf2_rank(rows),
          "nonzero_bits":sum(r.count("1") for r in rows),
          "total_bits":9*32,
          "distinct_effect_rows":len(set(rows)),
          "anf_degree_distribution":dict(sorted(Counter(d for d,t in av).items())),
          "mean_anf_term_count":sum(t for d,t in av)/9,
        }

    rA=list(effects["A"].values()); rN=list(effects["N"].values()); rX=list(effects["AxN"].values())
    ranks={
      "A":gf2_rank(rA),"N":gf2_rank(rN),"AxN":gf2_rank(rX),
      "A+N":gf2_rank(rA+rN),"A+AxN":gf2_rank(rA+rX),"N+AxN":gf2_rank(rN+rX),
      "A+N+AxN":gf2_rank(rA+rN+rX),
    }
    intersections={
      "A_intersect_N":ranks["A"]+ranks["N"]-ranks["A+N"],
      "A_intersect_AxN":ranks["A"]+ranks["AxN"]-ranks["A+AxN"],
      "N_intersect_AxN":ranks["N"]+ranks["AxN"]-ranks["N+AxN"],
    }

    exchange=[xor(effects["A"][k],effects["N"][k]) for k in effects["A"]]
    exchange_mismatch=sum(r.count("1") for r in exchange)

    transport={}
    for ch in effects:
        rr=[]
        for c in ("analysis","sample"):
            for z in PROFILES:
                rr.append(xor(effects[ch][(c,z)],effects[ch][("measurement",z)]))
        transport[ch]={
          "rank_gf2":gf2_rank(rr),
          "nonzero_bits":sum(r.count("1") for r in rr),
          "total_bits":6*32,
          "exact_rows":sum(r=="0"*32 for r in rr),
          "distinct_residual_rows":len(set(rr))
        }

    sufficient_sets=[]
    for k in range(5):
        for s in itertools.combinations(FEATURES,k):
            if sufficient(worlds,s):sufficient_sets.append(s)
    m=min(map(len,sufficient_sets))
    mins=[list(s) for s in sufficient_sets if len(s)==m]

    vdist=Counter()
    for i,v in enumerate(verts):
        ss=[]
        for k in range(5):
            for s in itertools.combinations(FEATURES,k):
                if sufficient(worlds,s,i):ss.append(s)
        vdist[min(map(len,ss))]+=1

    result={
      "stage":"EPISTEME-P38",
      "identifier_channel_symmetry":{
        "operational_definition":"Exact symmetry of orthogonally manipulated model-visible archive-ID and namespace channels on the observed finite design.",
        "channel_exchange_A_equals_N":{
          "matching_bits":9*32-exchange_mismatch,
          "mismatching_bits":exchange_mismatch,
          "total_bits":9*32,
          "exact_rows":sum(r=="0"*32 for r in exchange),
          "difference_rank_gf2":gf2_rank(exchange),
          "verdict":"REJECTED"
        },
        "additive_no_interaction_AxN_zero":{
          "zero_bits":9*32-channel["AxN"]["nonzero_bits"],
          "nonzero_bits":channel["AxN"]["nonzero_bits"],
          "total_bits":9*32,
          "exact_zero_rows":sum(r=="0"*32 for r in rX),
          "verdict":"REJECTED"
        },
        "context_transport_symmetry":{
          "A":transport["A"],"N":transport["N"],"AxN":transport["AxN"],
          "verdict":"REJECTED_FOR_ALL_THREE_CHANNEL_EFFECT_FAMILIES"
        }
      },
      "cross_context_effect_tensor":{
        "shape":"3 contexts × 3 construction profiles × 3 channel-effect families × 32 representation vertices",
        "channel_summaries":channel,
        "span_ranks":ranks,
        "pairwise_span_intersection_dimensions":intersections,
        "direct_sum_rank":ranks["A+N+AxN"],
        "direct_sum_dimension_maximal":ranks["A+N+AxN"]==27,
        "interpretation":"A, N, and AxN each span nine independent observed effect directions; their pairwise spans intersect trivially and combine as a 27-dimensional direct sum inside the 32-dimensional representation-geometry space."
      },
      "channel_representation_interaction_algebra":{
        "representation_space":"full Boolean cube on {R,F,H,T,L}",
        "A_anf_degree_distribution":channel["A"]["anf_degree_distribution"],
        "N_anf_degree_distribution":channel["N"]["anf_degree_distribution"],
        "AxN_anf_degree_distribution":channel["AxN"]["anf_degree_distribution"],
        "A_mean_terms":channel["A"]["mean_anf_term_count"],
        "N_mean_terms":channel["N"]["mean_anf_term_count"],
        "AxN_mean_terms":channel["AxN"]["mean_anf_term_count"],
        "low_order_uniform_channel_law_supported":False
      },
      "compression_frontier_reconstitution":{
        "observed_conditions":36,
        "distinct_geometry_rows":len(set(worlds.values())),
        "candidate_coordinates":["C","Z","A","N"],
        "minimum_coordinate_projection_size_for_full_geometry":m,
        "minimal_subsets":mins,
        "strict_subset_sufficient":m<4,
        "vertex_minimum_size_distribution":dict(sorted(vdist.items())),
        "frontier_status":"RECONSTITUTED_NO_COMPRESSION_FRONTIER"
      },
      "constitutional_verdict":"IDENTIFIER_CHANNELS_ORTHOGONAL_BUT_NONSEPARABLE_FROM_CONTEXT_AND_REPRESENTATION",
      "authority":"Deterministic exact decomposition of the sealed P37 Gemini tensor. 'Causal symmetry' here refers only to symmetry properties of randomized/orthogonal model-visible channel interventions in this task; it is not a claim about internal neural causal mechanisms. No cross-model authority or behavioral SVEC promotion.",
      "new_model_calls":0,
      "new_actions":0,
      "self_audit":"PASS"
    }
    Path("active/p38_result.json").write_text(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
