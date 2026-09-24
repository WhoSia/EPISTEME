from __future__ import annotations
import argparse,json
from collections import defaultdict
from pathlib import Path
from p34_design import WORLDS,TRAIN_WORLDS,HOLDOUT_WORLDS,VERTICES,VERTEX_ORDER,ANCHOR_ROW,hidden_key if False else label
from p34_design import oid,main_features,quadratic_features

# hidden key is reconstructed locally to avoid exporting any outcome-derived object.
def audit_key():
    out={}
    for w in WORLDS:
        for v in VERTICES:
            for sem in ("valid","null"):
                out[oid(w.world_id,v,sem)]={
                  "world_id":w.world_id,
                  "profile":w.profile,
                  "vertex":label(v),
                  "semantic_class":sem,
                  "expected_specific_criticism":sem=="valid",
                  "oracle_intervention":w.intervention,
                  "oracle_direction":"different",
                }
    return out

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip(); return "NONE" if t.upper()=="NONE" else t

def correct(row,a):
    if row.get("status")!="OK": return False
    ans=row.get("parsed_response") or {}; ch=norm(ans.get("challenge"))
    if not a["expected_specific_criticism"]: return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")==a["oracle_intervention"] and ans.get("predicted_direction")==a["oracle_direction"]

def solve_gf2(X,y):
    # Return one exact solution if consistent and uniquely identified for the columns.
    a=[list(r)+[yy] for r,yy in zip(X,y)]
    m=len(a); n=len(X[0]); rank=0; piv=[]
    for col in range(n):
        p=next((i for i in range(rank,m) if a[i][col]),None)
        if p is None: continue
        a[rank],a[p]=a[p],a[rank]
        for i in range(m):
            if i!=rank and a[i][col]:
                a[i]=[x^y for x,y in zip(a[i],a[rank])]
        piv.append(col); rank+=1
    for row in a:
        if not any(row[:n]) and row[n]:
            return None
    if rank<n:
        return None
    beta=[0]*n
    for i,col in enumerate(piv[:n]):
        beta[col]=a[i][n]
    return beta

def predict(beta,x):
    return sum(b*z for b,z in zip(beta,x))%2

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--gemini",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    receipt=json.loads(Path(a.gemini).read_text(encoding="utf-8"))
    key=audit_key(); grouped=defaultdict(list)
    for r in receipt["rows"]: grouped[r["packet_id"]].append(r)

    packets={}; technical=True; failures=0
    for pid,reps in grouped.items():
        au=key[pid]; ok=sum(r.get("status")=="OK" for r in reps); votes=sum(correct(r,au) for r in reps)
        technical &= ok>=2; failures += sum(r.get("status")!="OK" for r in reps)
        packets[pid]={**au,"ok_replicates":ok,"packet_correct":votes>=2}

    rows={}
    for w in WORLDS:
        bits=[]
        for v in VERTICES:
            name=label(v)
            vr=next(x for x in packets.values() if x["world_id"]==w.world_id and x["vertex"]==name and x["semantic_class"]=="valid")
            nr=next(x for x in packets.values() if x["world_id"]==w.world_id and x["vertex"]==name and x["semantic_class"]=="null")
            passed=vr["packet_correct"] and nr["packet_correct"]
            bits.append("0" if passed else "1")
        rows[w.world_id]="".join(bits)

    models={}
    for degree,feat in ((1,main_features),(2,quadratic_features)):
        train_exact_vertices=0
        holdout_matches=0
        holdout_total=4*32
        per_vertex={}
        for j,v in enumerate(VERTEX_ORDER):
            X=[feat(w.profile) for w in TRAIN_WORLDS]
            y=[int(rows[w.world_id][j]) for w in TRAIN_WORLDS]
            beta=solve_gf2(X,y)
            exact=beta is not None
            if exact: train_exact_vertices+=1
            vmatches=0
            if exact:
                for w in HOLDOUT_WORLDS:
                    pred=predict(beta,feat(w.profile))
                    obs=int(rows[w.world_id][j])
                    vmatches += int(pred==obs)
                    holdout_matches += int(pred==obs)
            per_vertex[v]={"train_exact":exact,"holdout_matches":vmatches if exact else None,"holdout_n":4 if exact else None}
        models[f"degree_{degree}"]={
          "train_exact_vertices":train_exact_vertices,
          "train_total_vertices":32,
          "holdout_matching_cells":holdout_matches,
          "holdout_total_cells":holdout_total,
          "all_vertices_train_exact":train_exact_vertices==32,
          "all_holdout_cells_exact":holdout_matches==holdout_total and train_exact_vertices==32,
          "per_vertex":per_vertex,
        }

    residual_rows={
      w.world_id:"".join(str(int(a!=b)) for a,b in zip(rows[w.world_id],ANCHOR_ROW))
      for w in WORLDS
    }

    if not technical:
        verdict="TECHNICAL_HOLD"
    elif models["degree_1"]["all_holdout_cells_exact"]:
        verdict="INSTANCE_MAIN_EFFECT_LAW_SURVIVES"
    elif models["degree_2"]["all_holdout_cells_exact"]:
        verdict="INSTANCE_QUADRATIC_LAW_SURVIVES"
    else:
        verdict="NO_LOW_ORDER_INSTANCE_LAW"

    result={
      "stage":"EPISTEME-P34",
      "model":"gemini",
      "arm_evaluable":technical,
      "anchor_context":"measurement-pipeline|u1",
      "instance_factorization":{
        "factors":["S:source/history-A shared stem","P:history-pair prefix overlap","L:identifier length","D:separator morphology"],
        "factorial_worlds":16,
        "training_profiles":12,
        "holdout_profiles":4,
      },
      "world_rows":rows,
      "anchor_residual_rows":residual_rows,
      "prospective_law_tests":models,
      "program_verdict":verdict,
      "format_or_api_failures":failures,
      "authority":"Prospective identification/holdout test of pre-response opaque-identifier construction features within one fixed context cell. Survival licenses only that local instance law; failure rules out these low-order feature laws, not all measurable instance features. No causal or behavioral-SVEC promotion."
    }
    Path(a.out).write_text(json.dumps(result,indent=2),encoding="utf-8")

if __name__=="__main__": main()
