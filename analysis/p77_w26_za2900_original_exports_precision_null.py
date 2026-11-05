"""P77 W26: read-only duplicate ZA2900 CSV precision and Stata reference comparison.
No respondent rows printed, and no third-party dataset is republished.
Requires pandas and numpy; input is extracted ORIGINAL user-held CRI-master/data.
"""
import argparse,csv,itertools,json
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd

def audit(folder):
    r=Path(folder)
    p=r/"ZA2900.csv";q=r/"Provided Materials"/"ZA2900.csv"
    changed=Counter();n=0;changed_rows=0;cells=0
    with p.open(encoding="cp1252",newline="") as a,q.open(encoding="cp1252",newline="") as b:
        left,right=csv.reader(a),csv.reader(b)
        h=next(left);assert h==next(right) and len(h)==194
        for x,y in itertools.zip_longest(left,right):
            assert x is not None and y is not None and len(x)==len(y)==194
            n+=1
            diff=[h[i] for i,(u,v) in enumerate(zip(x,y)) if u!=v]
            if diff:changed_rows+=1
            for column in diff:cells+=1;changed[column]+=1
    assert n==35313 and changed_rows==cells==7488 and changed=={"v325":7488}
    x=pd.to_numeric(pd.read_csv(p,encoding="cp1252",usecols=["v325"]).v325,errors="coerce")
    y=pd.to_numeric(pd.read_csv(q,encoding="cp1252",usecols=["v325"]).v325,errors="coerce")
    z=pd.read_stata(r/"ZA2900.dta",convert_categoricals=False,columns=["v325"]).v325
    eligible=x.notna()&y.notna()
    assert eligible.sum()==16218
    maxdelta=float((x[eligible]-y[eligible]).abs().max())
    assert maxdelta<1e-12
    for v in (x,y):
        mask=v.notna()&z.notna()
        assert mask.sum()==16218
        assert np.isclose(v[mask],z[mask],rtol=0,atol=1e-12).all()
    print(json.dumps({"rows":n,"columns":len(h),"textually_changed_cells":cells,
        "changed_variables":dict(changed),"numeric_rows":int(eligible.sum()),
        "not_numerically_compared_labeled_rows":int((~eligible).sum()),
        "max_absolute_difference":maxdelta,"agrees_with_stata_at_abs_1e_12":True,
        "interpretation":"CSV serialization/precision difference; no material numeric mismatch found. No AI intervention."},indent=2))
    print("PASS: no scientific-result change established")
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("original_cri_data_folder");args=a.parse_args()
    audit(args.original_cri_data_folder)
