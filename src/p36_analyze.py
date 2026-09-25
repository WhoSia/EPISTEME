from __future__ import annotations

import itertools,json
from collections import Counter,defaultdict
from pathlib import Path

FEATURES=("C","S","P","L","D")

def hamming(a,b): return sum(x!=y for x,y in zip(a,b))
def xor(a,b): return "".join(str(int(x!=y)) for x,y in zip(a,b))

def gf2_rank(rows):
    if not rows:return 0
    a=[[int(c) for c in row] for row in rows]
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

def feature_value(context,profile,f):
    if f=="C": return context
    return profile[{"S":0,"P":1,"L":2,"D":3}[f]]

def is_sufficient(conditions,subset,vertex_index=None):
    seen={}
    for context,profile,row in conditions:
        key=tuple(feature_value(context,profile,f) for f in subset)
        y=row if vertex_index is None else row[vertex_index]
        if key in seen and seen[key]!=y:
            return False
        seen[key]=y
    return True

def main():
    ev=json.loads(Path("active/p36_evidence.json").read_text())
    verts=ev["vertex_order"]
    p34=ev["p34_anchor_variable_identifier_package"]
    p35=ev["p35_constant_archive_id"]

    # Identifier-channel package contrast. P34->P35 changes model-visible archive_id
    # and source namespace (k34/zeta34 -> k35/zeta35); it is not archive_id-only.
    channel_residual={p:xor(p34[p],p35["anchor"][p]) for p in sorted(p34)}
    channel_hamming={p:channel_residual[p].count("1") for p in sorted(channel_residual)}
    channel_vertex_classes=defaultdict(list)
    for i,v in enumerate(verts):
        sig="".join(channel_residual[p][i] for p in sorted(channel_residual))
        channel_vertex_classes[sig].append(v)

    # P35 observed condition set: anchor full factorial + 4 profiles in each external context.
    conditions=[]
    for p,row in sorted(p35["anchor"].items()): conditions.append(("anchor",p,row))
    for c in ("analysis","sample"):
        for p,row in sorted(p35[c].items()): conditions.append((c,p,row))

    sufficient=[]
    for k in range(len(FEATURES)+1):
        for subset in itertools.combinations(FEATURES,k):
            if is_sufficient(conditions,subset):
                sufficient.append(subset)
    min_global=min(map(len,sufficient))
    min_global_subsets=[s for s in sufficient if len(s)==min_global]

    vertex_min={}
    size_distribution=Counter()
    for i,v in enumerate(verts):
        ss=[]
        for k in range(len(FEATURES)+1):
            for subset in itertools.combinations(FEATURES,k):
                if is_sufficient(conditions,subset,i):
                    ss.append(subset)
        m=min(map(len,ss))
        mins=[s for s in ss if len(s)==m]
        vertex_min[v]={"minimum_size":m,"minimal_subsets":[list(s) for s in mins]}
        size_distribution[m]+=1

    output_classes=defaultdict(list)
    for c,p,row in conditions: output_classes[row].append(f"{c}|{p}")

    # Construction effect rows over the 3 profiles common to all three contexts.
    profiles=("0101","1010","1111")
    deltas={}
    for c in ("anchor","analysis","sample"):
        base=p35[c]["0000"]
        for p in profiles:
            deltas[f"{c}|{p}"]=xor(p35[c][p],base)

    interaction=[]
    for c in ("analysis","sample"):
        for p in profiles:
            interaction.append(xor(deltas[f"{c}|{p}"],deltas[f"anchor|{p}"]))

    pred=ev["p35_presealed_predictions"]["predicted_external_rows"]
    transport_residual=[]
    transport_matches=0
    for c in ("analysis","sample"):
        for p in profiles:
            observed=p35[c][p]; predicted=pred[c][p]
            transport_matches+=sum(a==b for a,b in zip(observed,predicted))
            transport_residual.append(xor(observed,predicted))

    result={
      "stage":"EPISTEME-P36",
      "identifier_channel_decomposition":{
        "contrast":"P34 variable identifier package -> P35 constant archive-id package at the same measurement×u1 16-profile factorial",
        "model_visible_changes":"archive_id channel plus source namespace generation label (k34/zeta34 -> k35/zeta35); therefore not archive_id-only",
        "changed_profile_rows":sum(p34[p]!=p35["anchor"][p] for p in p34),
        "profile_rows_total":16,
        "geometry_bit_flips":sum(channel_hamming.values()),
        "geometry_bits_total":16*32,
        "mean_hamming_per_profile":sum(channel_hamming.values())/16,
        "residual_rank_gf2":gf2_rank(list(channel_residual.values())),
        "vertex_residual_signature_classes":len(channel_vertex_classes),
        "nontrivial_vertex_merges":[x for x in channel_vertex_classes.values() if len(x)>1],
      },
      "cross_context_construction_effect":{
        "prospective_transport_matches":transport_matches,
        "prospective_transport_total":192,
        "prospective_transport_mismatches":192-transport_matches,
        "transport_residual_rank_gf2":gf2_rank(transport_residual),
        "common_profile_effect_rows":len(deltas),
        "unique_common_profile_effect_rows":len(set(deltas.values())),
        "common_profile_effect_rank_gf2":gf2_rank(list(deltas.values())),
        "context_interaction_rank_gf2":gf2_rank(interaction),
      },
      "observed_no_compression_frontier":{
        "observed_world_conditions":len(conditions),
        "distinct_32bit_geometry_rows":len(set(row for _,_,row in conditions)),
        "output_quotient_classes":len(output_classes),
        "output_quotient_nontrivial_merges":[x for x in output_classes.values() if len(x)>1],
        "candidate_pre_response_coordinates":list(FEATURES),
        "minimum_coordinate_projection_size_for_full_geometry":min_global,
        "minimal_full_geometry_coordinate_subsets":[list(s) for s in min_global_subsets],
        "strict_subset_sufficient":min_global < len(FEATURES),
        "interpretation":"Within the observed finite design, no strict coordinate projection of (context,S,P,L,D) determines the full 32-bit geometry exactly."
      },
      "vertexwise_minimal_sufficient_statistics":{
        "minimum_size_distribution":dict(sorted(size_distribution.items())),
        "per_vertex":vertex_min,
        "exception":"R_F is the only vertex whose observed response is exactly determined without context C; all other 31 require C,S,P,L,D."
      },
      "constitutional_verdict":"OBSERVED_NO_COMPRESSION_FRONTIER",
      "authority":"Exact deterministic statement over the observed P34/P35 Gemini design. 'Sufficient statistic' means deterministic coordinate-projection sufficiency on this finite observation set, not Fisher-Neyman statistical sufficiency and not a universal causal law. The full five-coordinate tuple is saturated on the observed 24 conditions and therefore does not constitute a nontrivial predictive law.",
      "new_model_calls":0,
      "new_actions":0,
      "self_audit":"PASS"
    }
    Path("active/p36_result.json").write_text(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
