"""EPISTEME-P64 frozen source validation, no provider access."""
from collections import Counter

def verify_counts(rows):
    counts=Counter(r["status"] for r in rows)
    assert len(rows)==49152
    assert counts["OK"]==48849
    assert counts["TECHNICAL_FAIL"]==303
    return {"total":len(rows),"ok":counts["OK"],"failed":counts["TECHNICAL_FAIL"]}
