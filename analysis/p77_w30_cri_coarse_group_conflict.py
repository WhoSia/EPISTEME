"""EPISTEME P77 W30: authentic CRI source-table coarse grouping and CI disagreement.
Read-only; no AI intervention, and matching team/outcome/exposure does not ensure common estimand.
Requirements pandas, numpy; run: python p77_w30_cri_coarse_group_conflict.py CRI-master.zip
"""
import io, json, sys, zipfile
import numpy as np
import pandas as pd

def audit(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        with z.open("CRI-master/data/cri_str.csv") as f:
            d=pd.read_csv(io.BytesIO(f.read()),encoding="cp1252",low_memory=False)
    d=d[(d.u_teamid!=0)&d.AME_Z.notna()&d.lower_Z.notna()&d.upper_Z.notna()].copy()
    assert len(d)==1252
    d["exposure"]=np.select([d.Stock.eq("Stock"),d.Flow.eq("Flow")],["Stock","Flow"],default="Other")
    d["category"]=np.where((d.AME_Z<0)&(d.upper_Z<0),"negative",
                    np.where((d.AME_Z>0)&(d.lower_Z>0),"positive","includes_zero"))
    g=d.groupby(["u_teamid","dv_type","exposure"],dropna=False)
    counts=g.size(); categories=g.category.nunique()
    both=g.category.agg(lambda x:{"negative","positive"}.issubset(set(x)))
    result={"models_ci_complete":len(d),"coarse_groups":g.ngroups,
       "groups_with_multiple_models":int((counts>1).sum()),
       "groups_with_mixed_ci_categories":int((categories>1).sum()),
       "models_in_mixed_groups":int(counts[categories>1].sum()),
       "groups_with_both_significant_directions":int(both.sum()),
       "row_categories":d.category.value_counts().to_dict()}
    expected={"models_ci_complete":1252,"coarse_groups":531,
       "groups_with_multiple_models":238,"groups_with_mixed_ci_categories":89,
       "models_in_mixed_groups":400,"groups_with_both_significant_directions":15,
       "row_categories":{"includes_zero":806,"negative":244,"positive":202}}
    assert result==expected,(result,expected)
    return result
if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("Pass original CRI-master.zip")
    print(json.dumps(audit(sys.argv[1]),indent=2))
    print("PASS: source-data summary only; NOT an AI effect, fixed estimand, nor new epistemic theorem")
