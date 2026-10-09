"""Redacted provider error categories; never publish exception text or API secrets."""
from __future__ import annotations
import re
CODES={400,401,402,403,404,408,409,429,500,502,503,504}
def classify(exc):
    status=None
    for obj in (exc,getattr(exc,"response",None)):
        if obj is None:continue
        for field in ("status_code","code"):
            value=getattr(obj,field,None)
            try:
                if value is not None and int(value) in CODES:status=int(value);break
            except (TypeError,ValueError):pass
        if status is not None:break
    # Provider message is used in-memory for allowlisted classification ONLY.
    msg=str(getattr(exc,"message","") or "")
    patterns=[
        ("API_KEY_INVALID",r"api[_ -]?key[_ -]?invalid|invalid api key|api key not valid"),
        ("MODEL_UNAVAILABLE",r"model.*(not found|not supported|not available)|not found for api version"),
        ("SCHEMA_UNSUPPORTED",r"(unsupported|invalid).*(schema|response_json_schema|response_format)|schema.*(invalid|unsupported)"),
        ("QUOTA_EXHAUSTED",r"quota|rate limit|resource.exhausted"),
        ("PERMISSION_DENIED",r"permission|forbidden|restricted|not authorized"),
        ("BILLING_REQUIRED",r"billing|payment|credit|plan limitation"),
        ("INVALID_ARGUMENT",r"invalid.argument|invalid parameter|bad request"),
    ]
    tag=next((key for key,pattern in patterns if re.search(pattern,msg,re.I)),"UNKNOWN")
    if tag=="UNKNOWN":tag={401:"AUTH_OR_PERMISSION",403:"AUTH_OR_PERMISSION",404:"MODEL_OR_ENDPOINT_UNAVAILABLE",402:"BILLING_REQUIRED",429:"RATE_OR_QUOTA",400:"INVALID_REQUEST_UNCLASSIFIED",500:"SERVER_TEMPORARY",502:"SERVER_TEMPORARY",503:"SERVER_TEMPORARY",504:"SERVER_TEMPORARY"}.get(status,"UNKNOWN")
    return {"exception_type":type(exc).__name__,"http_status":status,"failure_category":tag}

def self_test():
    class Sample(Exception):
        code=400
        message="API key not valid: private_secret_must_never_appear"
    result=classify(Sample("opaque"))
    assert result=={"exception_type":"Sample","http_status":400,"failure_category":"API_KEY_INVALID"}
    assert "private_secret" not in str(result)
    class Missing(Exception):status_code=404
    assert classify(Missing())["failure_category"]=="MODEL_OR_ENDPOINT_UNAVAILABLE"
    class Payment(Exception): status_code=402
    payment=classify(Payment())
    assert payment["http_status"]==402 and payment["failure_category"]=="BILLING_REQUIRED"
    print("P69_REDACTED_ERROR_SELFTEST_PASS billing_402=PASS")
if __name__=="__main__":self_test()
