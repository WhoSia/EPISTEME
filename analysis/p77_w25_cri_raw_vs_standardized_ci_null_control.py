"""P77 W25 read-only negative control: original-vs-standardized CI classification.

Run against the user's authentic, publicly derived CRI-master.zip (or data/cri_str.csv
extracted unchanged). NOT a test of AI translation, instrument validity or originality.
"""
import argparse
import csv
from pathlib import Path
from collections import Counter

def number(s):
    s=(s or "").strip()
    if s.upper() in ("NA","NAN",""):return None
    return float(s)
def category(est,lower,upper):
    if est<0 and upper<0:return "negative"
    if est>0 and lower>0:return "positive"
    return "includes_zero"
def check(path):
    with open(path,encoding="cp1252",newline="") as f:
        data=list(csv.DictReader(f))
    assert len(data)==1309
    changed=[]
    kept=[]
    for r in data:
        if r["u_teamid"]=="0": continue
        columns=["AME","lower","upper","AME_Z","lower_Z","upper_Z"]
        values=[number(r[x]) for x in columns]
        if any(x is None for x in values): continue
        a,lo,hi,az,lz,uz=values
        x,y=category(a,lo,hi),category(az,lz,uz)
        kept.append((r["id"],x,y))
        if x!=y:changed.append((r["id"],x,y))
    assert len(kept)==1252
    assert changed==[],changed[:10]
    groups=Counter(y for _,_,y in kept)
    assert groups=={"negative":244,"includes_zero":806,"positive":202}
    print("PASS: 1252 original/standardized paired CIs; 0 category changes")
    print("COUNTS",dict(groups))
    print("LIMIT: positive-rescaling/sign classifications only, not equal scientific meaning")
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("original_cri_str_csv");args=ap.parse_args()
    check(Path(args.original_cri_str_csv))
