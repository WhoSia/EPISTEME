from __future__ import annotations
import argparse,json
from collections import defaultdict
from pathlib import Path
from p32_design import FRESH_WORLDS,VERTICES,VERTEX_ORDER,CANONICAL_ROWS,hidden_key,label

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip(); return "NONE" if t.upper()=="NONE" else t

def correct(row,a):
    if row.get("status")!="OK": return False
    ans=row.get("parsed_response") or {}; ch=norm(ans.get("challenge"))
    if not a["expected_specific_criticism"]: return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")==a["oracle_intervention"] and ans.get("predicted_direction")==a["oracle_direction"]

def gf2_rank(rows):
    a=[r[:] for r in rows]
    if not a:return 0
    m=len(a); n=len(a[0]); rank=0
    for col in range(n):
        p=next((i for i in range(rank,m) if a[i][col]),None)
        if p is None: continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(m):
            if i!=rank and a[i][col]:
                a[i]=[x^y for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==m:break
    return rank

def hamming(a,b): return sum(x!=y for x,y in zip(a,b))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--gemini",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    receipt=json.loads(Path(a.gemini).read_text(encoding="utf-8"))
    key=hidden_key(); grouped=defaultdict(list)
    for r in receipt["rows"]: grouped[r["packet_id"]].append(r)

    packets={}; technical=True; format_failures=0
    for pid,reps in grouped.items():
        audit=key[pid]
        ok=sum(r.get("status")=="OK" for r in reps)
        votes=sum(correct(r,audit) for r in reps)
        technical &= ok>=2
        format_failures += sum(r.get("status")!="OK" for r in reps)
        packets[pid]={**audit,"ok_replicates":ok,"packet_correct":votes>=2}

    context_rows={"|".join(k):v for k,v in CANONICAL_ROWS.items()}
    fresh_rows={}
    residual_rows=[]
    cells={}
    exact_cells=0
    identity_correct=0

    for w in FRESH_WORLDS:
        observed=[]
        for v in VERTICES:
            name=label(v)
            vr=next(x for x in packets.values() if x["world_id"]==w.world_id and x["vertex"]==name and x["semantic_class"]=="valid")
            nr=next(x for x in packets.values() if x["world_id"]==w.world_id and x["vertex"]==name and x["semantic_class"]=="null")
            observed_pass=vr["packet_correct"] and nr["packet_correct"]
            observed.append("0" if observed_pass else "1")
        row="".join(observed)
        canonical=CANONICAL_ROWS[(w.skin,w.intervention)]
        residual=[int(x!=y) for x,y in zip(row,canonical)]
        residual_rows.append(residual)
        dists={k:hamming(row,v) for k,v in context_rows.items()}
        best=min(dists.values())
        winners=sorted(k for k,d in dists.items() if d==best)
        own=f"{w.skin}|{w.intervention}"
        exact=row==canonical
        unique_own=winners==[own]
        exact_cells+=int(exact); identity_correct+=int(unique_own)
        fresh_rows[w.world_id]=row
        cells[w.world_id]={
          "context":own,
          "canonical_row":canonical,
          "fresh_row":row,
          "hamming_to_own":hamming(row,canonical),
          "exact_geometry_match":exact,
          "nearest_canonical_distance":best,
          "nearest_canonical_cells":winners,
          "own_cell_unique_nearest":unique_own,
          "identity_margin":(sorted(dists.values())[1]-best) if len(dists)>1 else None,
        }

    residual_signature_classes=defaultdict(list)
    stable_vertices=[]
    persistent_flip_vertices=[]
    for i,v in enumerate(VERTEX_ORDER):
        sig="".join(str(residual_rows[j][i]) for j in range(12))
        residual_signature_classes[sig].append(v)
        if sig=="0"*12: stable_vertices.append(v)
        if sig=="1"*12: persistent_flip_vertices.append(v)

    residual_rank=gf2_rank(residual_rows)
    if not technical:
        verdict="TECHNICAL_HOLD"
    elif exact_cells==12:
        verdict="EXACT_CELL_GEOMETRY_REPRODUCIBLE"
    elif identity_correct==12:
        verdict="CELL_IDENTITY_REPRODUCIBLE_WITH_WORLD_SPECIFIC_RESIDUAL"
    else:
        verdict="CELL_IDENTITY_NOT_REPRODUCIBLE_WORLD_INSTANCE_EFFECT"

    result={
      "stage":"EPISTEME-P32",
      "model":"gemini",
      "arm_evaluable":technical,
      "fresh_worlds":12,
      "geometry_cells":384,
      "cell_results":cells,
      "exact_cell_geometry_matches":exact_cells,
      "unique_nearest_own_cell":identity_correct,
      "world_specific_residual":{
        "shape":[12,32],
        "gf2_rank":residual_rank,
        "full_context_residual_rank":residual_rank==12,
        "nonzero_bits":sum(sum(r) for r in residual_rows),
        "stable_representation_vertices":stable_vertices,
        "persistent_flip_vertices":persistent_flip_vertices,
        "residual_signature_class_count":len(residual_signature_classes),
        "residual_signature_classes":dict(sorted(residual_signature_classes.items())),
      },
      "program_verdict":verdict,
      "format_or_api_failures":format_failures,
      "authority":"Prospective within-cell replication of the sealed P31 12-cell geometry. Exact matching licenses cell-level reproducibility only on this symbolic task/model; nearest-cell recovery without exact matching licenses cell identity but not exact geometry. Failure of own-cell identification rejects treating skin×intervention cell identity as sufficient. No causal-law or behavioral-SVEC promotion."
    }
    Path(a.out).write_text(json.dumps(result,indent=2),encoding="utf-8")

if __name__=="__main__": main()
