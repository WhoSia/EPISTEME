"""EPISTEME P77 W24 — CRI author-derived Fig1 independent source-table replay.
Input: user's unmodified CRI-master.zip (SHA256 sealed in W23).
Reproduces plotted category percentages, NOT original ISSP regression estimates.
"""
import argparse, csv, hashlib, io, json, math, zipfile
from collections import Counter
SHA = "64756bfe62b25cdd7dbea57d2b063cb0f564225751d1f0251b4879f426894098"
def number(x):
    x=(x or "").strip()
    return None if not x or x.upper() in ("NA","NAN") else float(x)
def audit(path):
    digest=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): digest.update(chunk)
    assert digest.hexdigest()==SHA
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        with z.open("CRI-master/data/cri_str.csv") as f:
            rows=list(csv.DictReader(io.TextIOWrapper(f,encoding="cp1252",newline="")))
        with z.open("CRI-master/data/cri.csv") as f:
            models=list(csv.DictReader(io.TextIOWrapper(f,encoding="cp1252",newline="")))
    assert len(rows)==len(models)==1309
    sample=[r for r in rows if r["u_teamid"]!="0"]
    assert len(sample)==1261
    ame=[r for r in sample if number(r["AME_Z"]) is not None]
    assert len(ame)==1253
    usable=[r for r in ame if number(r["lower_Z"]) is not None]
    assert len(usable)==1252 and all(number(r["upper_Z"]) is not None for r in usable)
    cat=Counter(); wcat=Counter()
    for r in usable:
        est=number(r["AME_Z"]);lo=number(r["lower_Z"]);hi=number(r["upper_Z"])
        if -1e-8 < lo < 1e-8: lo=-.0001
        if -1e-8 < hi < 1e-8: hi=.0001
        lo=max(lo,-.75);hi=min(hi,.75)
        if hi<-.75: hi=-.745
        est=max(-.747,min(.747,est))
        est,lo,hi=round(est,6),round(lo,6),round(hi,6)
        key="negative" if est<0 and hi<0 else ("positive" if est>0 and lo>0 else "nonsignificant")
        cat[key]+=1
        weight=number(r["inv_weight"])
        assert weight is not None and weight>0
        wcat[key]+=weight
    denom=sum(wcat.values())
    weighted={k:round(100*round(wcat[k]/denom,3),1) for k in ("negative","nonsignificant","positive")}
    assert weighted=={"negative":25.4,"nonsignificant":57.7,"positive":16.9}
    assert cat==Counter(negative=244,nonsignificant=806,positive=202)
    near=sum(abs(number(r["AME_Z"]))<=.037 for r in ame)
    assert near==1126
    return {"source_zip_sha256":SHA,"cohort":{"submitted":1261,"nonmissing_ame_z":1253,"ci_complete":1252},
        "categories_unweighted_counts":dict(cat),
        "categories_unweighted_percent":{k:round(100*cat[k]/1252,3) for k in weighted},
        "categories_inverse_team_weighted_percent":weighted,
        "sum_inv_weight_after_ci_filter":round(denom,9),
        "small_effect":{"abs_ame_z_le_0_037":near,"denominator":1253,"percent":round(100*near/1253,3)},
        "scope":"Published derived data; original regression models NOT rerun; no AI treatment/adoption."}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("original_zip");a=p.parse_args()
    print(json.dumps(audit(a.original_zip),indent=2))
    print("PASS: original author Fig1 category proportions, and effect-size critique cross-check")
