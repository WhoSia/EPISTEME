from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

VERTEX_ORDER=[
"I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L",
"R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L",
"R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"
]
CONTEXT_ORDER=[
("measurement-pipeline","u1"),("measurement-pipeline","u2"),("measurement-pipeline","u3"),("measurement-pipeline","u4"),
("analysis-pipeline","u1"),("analysis-pipeline","u2"),("analysis-pipeline","u3"),("analysis-pipeline","u4"),
("sample-handling","u1"),("sample-handling","u2"),("sample-handling","u3"),("sample-handling","u4"),
]
ROWS={
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

def gf2_rank(rows):
    a=[r[:] for r in rows]
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
    assert all(len(r)==32 for r in ROWS.values())
    mat=[[int(b) for b in ROWS[c]] for c in CONTEXT_ORDER]
    full_rank=gf2_rank(mat)

    m="measurement-pipeline"; a="analysis-pipeline"; s="sample-handling"; u1="u1"
    cycles=[(a,"u2"),(a,"u3"),(a,"u4"),(s,"u2"),(s,"u3"),(s,"u4")]
    residual=[]
    for sk,u in cycles:
        bits=[]
        for i in range(32):
            bits.append(
                int(ROWS[(sk,u)][i]) ^
                int(ROWS[(sk,u1)][i]) ^
                int(ROWS[(m,u)][i]) ^
                int(ROWS[(m,u1)][i])
            )
        residual.append(bits)

    cycle_weights={f"{sk}|{u}":sum(bits) for (sk,u),bits in zip(cycles,residual)}
    interaction_rank=gf2_rank(residual)
    interaction_nonzero=sum(sum(x) for x in residual)

    interaction_classes=defaultdict(list)
    full_classes=defaultdict(list)
    vertex_weights={}
    for i,v in enumerate(VERTEX_ORDER):
        isig="".join(str(residual[j][i]) for j in range(6))
        fsig="".join(ROWS[c][i] for c in CONTEXT_ORDER)
        interaction_classes[isig].append(v)
        full_classes[fsig].append(v)
        vertex_weights[v]=sum(residual[j][i] for j in range(6))

    additive_vertices=sorted(v for v,w in vertex_weights.items() if w==0)

    result={
      "stage":"EPISTEME-P31",
      "balanced_factor_tensor":{
        "shape":[3,4,32],
        "binary_encoding":"1=FAIL,0=PASS",
        "context_row_rank_gf2":full_rank,
        "context_rows_linearly_independent":full_rank==12,
      },
      "prospective_additive_law":{
        "status":"DEFEATED",
        "presealed_cells":192,
        "matches":93,
        "mismatches":99,
        "match_rate":93/192,
        "exact_rows":0,
      },
      "interaction_residual_geometry":{
        "basis":"six independent 2x2 GF(2) cycle contrasts relative to measurement-pipeline/u1",
        "basis_cells":[f"{sk}|{u}" for sk,u in cycles],
        "cycle_nonzero_weights":cycle_weights,
        "nonzero_residual_bits":interaction_nonzero,
        "total_residual_bits":192,
        "interaction_rank_gf2":interaction_rank,
        "full_interaction_dimension_required":interaction_rank==6,
        "interaction_signature_class_count":len(interaction_classes),
        "interaction_signature_classes":dict(sorted(interaction_classes.items())),
        "purely_additive_vertices":additive_vertices,
        "purely_additive_vertex_count":len(additive_vertices),
        "vertex_interaction_weights":vertex_weights,
      },
      "exact_behavioral_compression":{
        "full_12_context_signature_class_count":len(full_classes),
        "classes":dict(sorted(full_classes.items())),
        "only_nontrivial_merge":[vs for vs in full_classes.values() if len(vs)>1],
        "compression_ratio":"32 representations -> 31 exact behavioral classes",
      },
      "context_law_authority":{
        "M0":"DEFEATED",
        "M_S":"DEFEATED",
        "M_U":"DEFEATED",
        "M_S+U":"PROSPECTIVELY_DEFEATED",
        "M_SxU":"SATURATED_CEILING_ONLY",
        "verdict":"NO_CONTEXT_FEATURE_SUFFICIENCY / FULL_SKIN×INTERVENTION_INTERACTION_REQUIRED_ON_TESTED_GRID",
        "interpretation":"The complete balanced grid requires all six independent interaction contrasts over GF(2); neither main effects nor a lower-rank interaction residual explain the observed tensor exactly."
      },
      "successor_identifiability_problem":{
        "question":"Are the 12 context-cell geometries reproducible properties of skin×intervention cells, or idiosyncratic to particular world instantiations?",
        "recommended_design":"fresh within-cell replication over all 12 balanced cells before introducing any new context feature or claiming cell-level law"
      },
      "authority":"Exact deterministic decomposition of the sealed P30 3x4x32 Gemini tensor. No new model calls, no causal context-law claim, and no behavioral SVEC promotion."
    }
    Path("active/p31_result.json").write_text(json.dumps(result,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
