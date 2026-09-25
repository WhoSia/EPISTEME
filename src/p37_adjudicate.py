from __future__ import annotations

import argparse,itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from p37_design import PROFILES,ARMS,BASE_ARM,VERTEX_ORDER,profile_label,arm_label

FEATURES=("C","Z","A","N")

def norm(v):
    if v is None:return "NONE"
    t=str(v).strip()
    return "NONE" if t.upper()=="NONE" else t

def correct(r):
    if r.get("status")!="OK": return False
    ans=r.get("parsed_response") or {}
    ch=norm(ans.get("challenge"))
    if r["semantic_class"]=="null": return ch=="NONE"
    return ch!="NONE" and ans.get("intervention")=="u1" and ans.get("predicted_direction")=="different"

def aggregate(rows):
    g=defaultdict(list)
    for r in rows:
        g[(r["context"],r["profile"],r["arm"],r["vertex"],r["semantic_class"])].append(r)
    worlds={}; technical=True
    for c,p,a in sorted({(k[0],k[1],k[2]) for k in g}):
        bits=[]
        for v in VERTEX_ORDER:
            vr=g[(c,p,a,v,"valid")]; nr=g[(c,p,a,v,"null")]
            vok=sum(x["status"]=="OK" for x in vr); nok=sum(x["status"]=="OK" for x in nr)
            technical &= vok>=2 and nok>=2
            vp=sum(correct(x) for x in vr)>=2
            np=sum(correct(x) for x in nr)>=2
            bits.append("0" if vp and np else "1")
        worlds[(c,p,a)]="".join(bits)
    return worlds,technical

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

def coords(key):
    c,p,a=key
    A=1 if a.startswith("A1") else 0
    N=1 if a.endswith("N1") else 0
    return {"C":c,"Z":p,"A":A,"N":N}

def sufficient(worlds,subset,vertex=None):
    seen={}
    for key,row in worlds.items():
        z=coords(key)
        k=tuple(z[f] for f in subset)
        y=row if vertex is None else row[vertex]
        if k in seen and seen[k]!=y:return False
        seen[k]=y
    return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--receipt",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    receipt=json.loads(Path(a.receipt).read_text(encoding="utf-8"))
    worlds,technical=aggregate(receipt["rows"])
    pre=receipt["preseal"]

    target_arms=[arm_label(x) for x in ARMS if x!=BASE_ARM]
    matches=0; total=0; residual_rows=[]; details=[]
    for c in ("analysis","sample"):
        for p in PROFILES:
            pl=profile_label(p)
            for al in target_arms:
                obs=worlds[(c,pl,al)]
                pred=pre["predicted_external_rows"][c][pl][al]
                resid=xor(obs,pred)
                m=sum(x==y for x,y in zip(obs,pred))
                matches+=m; total+=32; residual_rows.append(resid)
                details.append({"context":c,"profile":pl,"arm":al,"matches":m,"n":32,"exact":m==32,"residual":resid})

    # Anchor factorial decomposition: A, N, and A×N contrasts.
    contrast_rows={"A":[],"N":[],"AxN":[]}
    per_profile={}
    for p in PROFILES:
        pl=profile_label(p)
        y00=worlds[("measurement",pl,"A0N0")]
        y10=worlds[("measurement",pl,"A1N0")]
        y01=worlds[("measurement",pl,"A0N1")]
        y11=worlds[("measurement",pl,"A1N1")]
        dA=xor(y10,y00); dN=xor(y01,y00); dAN=xor(xor(y11,y10),xor(y01,y00))
        contrast_rows["A"].append(dA); contrast_rows["N"].append(dN); contrast_rows["AxN"].append(dAN)
        per_profile[pl]={
          "A_nonzero":dA.count("1"),
          "N_nonzero":dN.count("1"),
          "AxN_nonzero":dAN.count("1")
        }

    # Observed 3×3×2×2 full factorial exact sufficiency reopening.
    suff=[]
    for k in range(len(FEATURES)+1):
        for s in itertools.combinations(FEATURES,k):
            if sufficient(worlds,s):suff.append(s)
    m=min(map(len,suff))
    mins=[list(s) for s in suff if len(s)==m]

    vdist=Counter(); vmins={}
    for i,v in enumerate(VERTEX_ORDER):
        ss=[]
        for k in range(len(FEATURES)+1):
            for s in itertools.combinations(FEATURES,k):
                if sufficient(worlds,s,i):ss.append(s)
        vm=min(map(len,ss)); vdist[vm]+=1
        vmins[v]={"minimum_size":vm,"minimal_subsets":[list(s) for s in ss if len(s)==vm]}

    unique_rows=len(set(worlds.values()))
    exact_transport=technical and matches==576
    verdict="TECHNICAL_HOLD" if not technical else ("IDENTIFIER_CHANNEL_TRANSPORT_SURVIVES" if exact_transport else "IDENTIFIER_CHANNEL_CONTEXT_INTERACTION")

    result={
      "stage":"EPISTEME-P37",
      "arm_evaluable":technical,
      "orthogonal_identifier_factorial":{
        "contexts":3,"profiles":3,"archive_levels":2,"namespace_levels":2,
        "observed_conditions":len(worlds),
        "distinct_geometry_rows":unique_rows,
        "anchor_contrast_rank_gf2":{
          "A":gf2_rank(contrast_rows["A"]),
          "N":gf2_rank(contrast_rows["N"]),
          "AxN":gf2_rank(contrast_rows["AxN"])
        },
        "anchor_contrast_nonzero_bits":{
          "A":sum(r.count("1") for r in contrast_rows["A"]),
          "N":sum(r.count("1") for r in contrast_rows["N"]),
          "AxN":sum(r.count("1") for r in contrast_rows["AxN"])
        },
        "per_profile":per_profile
      },
      "prospective_context_transport":{
        "preseal_sha256":pre["sha256"],
        "target_cells":576,
        "matching_cells":matches,
        "mismatches":576-matches,
        "match_rate":matches/576,
        "exact_rows":sum(x["exact"] for x in details),
        "total_rows":18,
        "transport_residual_rank_gf2":gf2_rank(residual_rows),
        "details":details
      },
      "sufficient_statistic_reopening":{
        "coordinates":["C","Z","A","N"],
        "minimum_projection_size_for_full_geometry":m,
        "minimal_subsets":mins,
        "strict_subset_sufficient":m<4,
        "vertex_minimum_size_distribution":dict(sorted(vdist.items())),
        "per_vertex":vmins
      },
      "program_verdict":verdict,
      "format_or_api_failures":sum(r["status"]!="OK" for r in receipt["rows"]),
      "authority":"Orthogonal archive-regime × namespace-regime attribution and prospective transport over three fixed construction profiles and three contexts at u1. A/N factors are model-visible lexical channels, not causal mechanisms beyond this task. Sufficiency is finite-design deterministic coordinate-projection sufficiency only; no behavioral SVEC promotion."
    }
    Path(a.out).write_text(json.dumps(result,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
