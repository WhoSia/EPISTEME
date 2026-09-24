from __future__ import annotations

import argparse,json
from collections import Counter,defaultdict
from pathlib import Path

from p35_design import VERTEX_ORDER,EXTERNAL_TEST_PROFILES,profile_label

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

def aggregate(rows,phase=None):
    g=defaultdict(list)
    for r in rows:
        if phase and r["phase"]!=phase: continue
        g[(r["context"],r["profile"],r["vertex"],r["semantic_class"])].append(r)
    worlds={}; technical=True
    for c,p in sorted({(k[0],k[1]) for k in g}):
        bits=[]
        for v in VERTEX_ORDER:
            vr=g[(c,p,v,"valid")]; nr=g[(c,p,v,"null")]
            vok=sum(x["status"]=="OK" for x in vr); nok=sum(x["status"]=="OK" for x in nr)
            technical &= vok>=2 and nok>=2
            vp=sum(correct(x) for x in vr)>=2
            np=sum(correct(x) for x in nr)>=2
            bits.append("0" if vp and np else "1")
        worlds[(c,p)]="".join(bits)
    return worlds,technical

def anf_degree(vals_by_profile):
    # Full 4-bit Mobius transform; profile labels are SP LD in binary order.
    arr=[0]*16
    for lab,val in vals_by_profile.items():
        idx=int(lab,2); arr[idx]=val
    a=arr[:]
    for bit in range(4):
        step=1<<bit
        for mask in range(16):
            if mask&step: a[mask]^=a[mask^step]
    degree=max((mask.bit_count() for mask,c in enumerate(a) if c),default=0)
    return degree,sum(a)

def gf2_rank(rows):
    if not rows:return 0
    a=[[int(x) for x in r] for r in rows]
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

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--receipt",required=True); ap.add_argument("--out",required=True); a=ap.parse_args()
    receipt=json.loads(Path(a.receipt).read_text(encoding="utf-8"))
    worlds,technical=aggregate(receipt["rows"])
    pre=receipt["preseal"]

    matches=0; total=0; context_matches=Counter()
    residual_rows=[]
    cell_details=[]
    for c in ("analysis","sample"):
        for p in EXTERNAL_TEST_PROFILES:
            lab=profile_label(p)
            obs=worlds[(c,lab)]
            pred=pre["predicted_external_rows"][c][lab]
            resid="".join(str(int(x!=y)) for x,y in zip(obs,pred))
            residual_rows.append(resid)
            m=sum(x==y for x,y in zip(obs,pred))
            matches+=m; total+=32; context_matches[c]+=m
            cell_details.append({"context":c,"profile":lab,"matches":m,"n":32,"exact":m==32,"residual":resid})

    # Anchor exact ANF localization after archive-id confound removal.
    degree_dist=Counter(); term_counts=[]
    for j,v in enumerate(VERTEX_ORDER):
        vals={}
        for i in range(16):
            lab=f"{i:04b}"
            vals[lab]=int(worlds[("anchor",lab)][j])
        d,t=anf_degree(vals); degree_dist[d]+=1; term_counts.append(t)

    exact=technical and matches==192
    if not technical:
        verdict="TECHNICAL_HOLD"
    elif exact:
        verdict="CONSTRUCTION_EFFECT_TRANSPORT_SURVIVES"
    else:
        verdict="CONSTRUCTION_EFFECT_CONTEXT_INTERACTION"

    result={
      "stage":"EPISTEME-P35",
      "arm_evaluable":technical,
      "p34_inherited_verdict":"NO_LOW_ORDER_INSTANCE_LAW",
      "confound_stripped_anchor":{
        "constant_archive_id":True,
        "full_factorial_profiles":16,
        "exact_anf_degree_distribution":dict(sorted(degree_dist.items())),
        "mean_anf_term_count":sum(term_counts)/32,
      },
      "prospective_cross_context_transport":{
        "preseal_sha256":pre["sha256"],
        "target_cells":192,
        "matching_cells":matches,
        "match_rate":matches/192,
        "analysis_matches":context_matches["analysis"],
        "sample_matches":context_matches["sample"],
        "exact_profile_rows":sum(x["exact"] for x in cell_details),
        "total_profile_rows":6,
        "cell_details":cell_details,
        "transport_residual_rank_gf2":gf2_rank(residual_rows),
      },
      "program_verdict":verdict,
      "format_or_api_failures":sum(r["status"]!="OK" for r in receipt["rows"]),
      "authority":"P35 isolates the S/P/L/D construction profiles from archive-id variation and prospectively tests whether their anchor-context effect deltas transport to analysis and sample contexts at fixed u1. Exact survival licenses only this construction-effect transport family; failure implies context-dependent construction effects. No causal or behavioral-SVEC promotion."
    }
    Path(a.out).write_text(json.dumps(result,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
