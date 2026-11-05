"""P77 W29 authentic CRI hierarchy audit. Descriptive only; NO causal/epistemic attribution.
Usage: python analysis/p77_w29_cri_variance_hierarchy.py /path/to/CRI-master.zip
Requires pandas/numpy. Original respondent rows are never exported.
"""
from pathlib import Path
from zipfile import ZipFile
import io, json, sys
import pandas as pd
import numpy as np

def load(zip_path):
    with ZipFile(zip_path) as z:
        assert z.testzip() is None
        with z.open("CRI-master/data/cri_str.csv") as f:
            frame=pd.read_csv(io.BytesIO(f.read()),encoding="cp1252",low_memory=False)
    assert len(frame)==1309
    frame=frame[(frame.u_teamid!=0)&frame.AME_Z.notna()].copy()
    assert len(frame)==1253 and frame.u_teamid.nunique()==71
    return frame

def hierarchy(d):
    d=d.copy()
    d["iv_type"]=np.select([d.Stock.eq("Stock"),d.Flow.eq("Flow")],["Stock","Flow"],default="Other")
    y=d.AME_Z;means=[pd.Series(y.mean(),index=d.index)]
    for level in [["u_teamid"],["u_teamid","dv_type"],["u_teamid","dv_type","iv_type"]]:
        means.append(d.groupby(level,dropna=False).AME_Z.transform("mean"))
    means.append(y)
    var=float(y.var(ddof=0))
    parts=[float(((means[i+1]-means[i])**2).mean()) for i in range(4)]
    assert np.isclose(sum(parts),var,rtol=1e-11)
    return {"n":len(d),"n_teams":d.u_teamid.nunique(),"n_team_outcome_exposure_groups":d.groupby(["u_teamid","dv_type","iv_type"],dropna=False).ngroups,
            "variance":var,"between_team_share":parts[0]/var,
            "within_team_between_outcome_share":parts[1]/var,
            "within_team_outcome_between_exposure_share":parts[2]/var,
            "within_team_outcome_exposure_share":parts[3]/var}

def simple_team(d):
    y=d.AME_Z
    tmean=d.groupby("u_teamid").AME_Z.transform("mean")
    total=float(y.var(ddof=0))
    w=float(((y-tmean)**2).mean())
    groups=d.groupby("u_teamid").AME_Z
    mm=groups.mean();vv=groups.var(ddof=0).fillna(0)
    within_eq=vv.mean();between_eq=((mm-mm.mean())**2).mean()
    return {"n":len(d),"n_teams":groups.ngroups,"within_share_model_weighted":w/total,
            "within_share_equal_team":within_eq/(within_eq+between_eq)}

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("python p77_w29_cri_variance_hierarchy.py original.zip")
    d=load(Path(sys.argv[1]))
    a=simple_team(d)
    assert np.isclose(a["within_share_model_weighted"],.8639918954905882,atol=1e-10)
    assert np.isclose(a["within_share_equal_team"],.7951031412536741,atol=1e-10)
    h=hierarchy(d)
    assert np.isclose(h["within_team_outcome_exposure_share"],.153582480,atol=1e-7)
    r={"primary_model_weighted":a,"hierarchy":h,
       "sensitivity":{name:simple_team(v) for name,v in {
          "exclude_abs_ame_gt_0_75":d[d.AME_Z.abs()<=.75],
          "exclude_abs_ame_gt_0_20":d[d.AME_Z.abs()<=.20],
          "winsorize_ame_at_0_10":d.assign(AME_Z=d.AME_Z.clip(-.1,.1))}.items()}}
    print(json.dumps(r,ensure_ascii=False,indent=2))
    print("PASS: finite dataset orthogonal decomposition; NOT causation, common estimand or original R rerun")
