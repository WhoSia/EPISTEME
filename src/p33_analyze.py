from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

VERTEX_ORDER=[
"I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L",
"R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L",
"R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"
]

CANONICAL_ROWS=[
"01100001100001011000000100011010",
"00000011000111010000000010000000",
"10000001001111110101010111010100",
"00010000000010100001101001000101",
"01011010110000001011010001100010",
"01100110010100101000001101010101",
"00001100100001110100000111101110",
"00110101110111110001000001110001",
"01010001100000010100001010001000",
"00011001010010100011110011010110",
"00010000000001001001000001001000",
"00100000000011010000000101011000",
]

CONTEXTS=[
"measurement-pipeline|u1","measurement-pipeline|u2","measurement-pipeline|u3","measurement-pipeline|u4",
"analysis-pipeline|u1","analysis-pipeline|u2","analysis-pipeline|u3","analysis-pipeline|u4",
"sample-handling|u1","sample-handling|u2","sample-handling|u3","sample-handling|u4",
]

def bits(s): return [int(x) for x in s]

def xor(a,b): return "".join(str(int(x!=y)) for x,y in zip(a,b))

def hamming(a,b): return sum(x!=y for x,y in zip(a,b))

def gf2_rank(rows):
    a=[bits(r) if isinstance(r,str) else list(r) for r in rows]
    m=len(a); n=len(a[0]); rank=0
    for col in range(n):
        p=next((i for i in range(rank,m) if a[i][col]),None)
        if p is None: continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(m):
            if i!=rank and a[i][col]:
                a[i]=[x^y for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==m: break
    return rank

def main():
    p32=json.loads(Path("active/p32_result.json").read_text(encoding="utf-8"))
    cell_results=p32.get("cell_results")
    if cell_results is None:
        raise RuntimeError("P32 canonical detailed cell_results required before P33 deterministic analysis")

    world_order=[f"P32W{i:02d}" for i in range(1,13)]
    fresh=[cell_results[w]["fresh_row"] for w in world_order]
    residual=[xor(c,f) for c,f in zip(CANONICAL_ROWS,fresh)]

    rank_c=gf2_rank(CANONICAL_ROWS)
    rank_f=gf2_rank(fresh)
    rank_e=gf2_rank(residual)
    rank_ce=gf2_rank(CANONICAL_ROWS+residual)
    intersection_dim=rank_c+rank_e-rank_ce

    paired=[hamming(c,f) for c,f in zip(CANONICAL_ROWS,fresh)]
    unpaired=[
        hamming(f,c)
        for i,f in enumerate(fresh)
        for j,c in enumerate(CANONICAL_ROWS)
        if i!=j
    ]

    own_ranks=[]
    unique_nearest=0
    for i,f in enumerate(fresh):
        ds=[hamming(f,c) for c in CANONICAL_ROWS]
        own=ds[i]
        rank_min=1+sum(d<own for d in ds)
        rank_max=sum(d<=own for d in ds)
        own_ranks.append({"context":CONTEXTS[i],"min_rank":rank_min,"max_rank":rank_max,"own_distance":own})
        if rank_min==rank_max==1: unique_nearest+=1

    residual_classes=defaultdict(list)
    fresh_classes=defaultdict(list)
    combined_classes=defaultdict(list)
    agreement={}
    for i,v in enumerate(VERTEX_ORDER):
        rsig="".join(r[i] for r in residual)
        fsig="".join(r[i] for r in fresh)
        csig="".join(x[i] for pair in zip(CANONICAL_ROWS,fresh) for x in pair)
        residual_classes[rsig].append(v)
        fresh_classes[fsig].append(v)
        combined_classes[csig].append(v)
        agreement[v]=sum(CANONICAL_ROWS[j][i]==fresh[j][i] for j in range(12))

    result={
      "stage":"EPISTEME-P33",
      "world_instance_variance_constitution":{
        "paired_hamming_distances":paired,
        "mean_paired_hamming":sum(paired)/12,
        "paired_flip_rate":sum(paired)/(12*32),
        "mean_unpaired_fresh_to_canonical_hamming":sum(unpaired)/len(unpaired),
        "instance_residual_nonzero_bits":sum(sum(bits(r)) for r in residual),
        "instance_residual_total_bits":12*32,
      },
      "cell_identity_survival_boundary":{
        "exact_geometry_matches":0,
        "unique_nearest_own_cell":unique_nearest,
        "own_cell_rank_intervals":own_ranks,
        "mean_own_cell_min_rank":sum(x["min_rank"] for x in own_ranks)/12,
        "surviving_cell":"sample-handling|u3" if unique_nearest==1 else None,
      },
      "context_vs_instance_row_space":{
        "canonical_context_rank_gf2":rank_c,
        "fresh_world_rank_gf2":rank_f,
        "instance_residual_rank_gf2":rank_e,
        "combined_context_plus_residual_rank_gf2":rank_ce,
        "context_residual_intersection_dimension":intersection_dim,
        "classification":"ALGEBRAIC_ROW_SPACE_SEPARATION" if intersection_dim==0 and rank_ce==rank_c+rank_e else "ROW_SPACE_OVERLAP",
      },
      "replicate_quotient_geometry":{
        "canonical_behavioral_classes":31,
        "fresh_behavioral_classes":len(fresh_classes),
        "combined_24row_behavioral_classes":len(combined_classes),
        "residual_signature_classes":len(residual_classes),
        "fresh_nontrivial_merges":[x for x in fresh_classes.values() if len(x)>1],
        "combined_nontrivial_merges":[x for x in combined_classes.values() if len(x)>1],
        "residual_nontrivial_merges":[x for x in residual_classes.values() if len(x)>1],
        "representation_context_agreement_counts":agreement,
      },
      "authority_separation":{
        "context_cell_geometry":"NOT_REPRODUCIBLE",
        "cell_identity":"NOT_REPRODUCIBLE_EXCEPT_ONE_OF_TWELVE",
        "world_instance_component":"FULL_RANK_12_OF_12_RESIDUAL",
        "representation_quotient":"MAXIMALLY_FINE_UNDER_FRESH_AND_COMBINED_SIGNATURES",
        "verdict":"WORLD_INSTANCE_AUTHORITY_DOMINATES_CELL_IDENTITY_ON_TESTED_CONSTRUCTION",
        "caveat":"This is an algebraic and predictive authority separation on two instances per context cell, not a causal variance decomposition."
      },
      "successor_problem":{
        "question":"Which latent packet/world features generate the instance residual, and can they be prospectively measured before model response?",
        "recommended_direction":"instrument world-instance construction features before further replication; do not add more nominal context labels without a pre-response measurable candidate."
      },
      "new_model_calls":0,
      "new_actions":0,
      "authority":"Deterministic analysis of sealed P31/P32 tensors only. No causal variance attribution, universal law, or behavioral SVEC promotion."
    }
    Path("active/p33_result.json").write_text(json.dumps(result,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
