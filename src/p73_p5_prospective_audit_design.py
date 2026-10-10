"""P73-P5: prospective audit-announcement effect vs external time/authority drift.

This is a preregistration-quality design validator + synthetic diagnostics,
NOT an experiment on an institution and NOT an independent causal estimate.
It never reaches out to mutable institutions, recruits humans or makes calls.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations
import json

@dataclass(frozen=True)
class Snapshot:
    source_id:str
    arm:str # announced-audit versus contemporaneous control
    wave:str # pre/post
    read_at:str
    source_sha:str
    source_role:str
    authorization:str
    authority_effective_from:str
    source_updated_at:str
    certified_external_page_capture:bool
    measured_outcome:int
    independent_collector_id:str

def _time(s):
    v=datetime.fromisoformat(s.replace("Z","+00:00"))
    if v.utcoffset() is None:raise ValueError("P73_TIME_MUST_BE_OFFSET_AWARE")
    return v.astimezone(timezone.utc)

def validate(rows:list[Snapshot],announcement_at:str, *,
             preregistered:bool,consent_and_legal_review:bool):
    if not preregistered or not consent_and_legal_review:
        raise ValueError("P73_P5_UNAUTHORIZED_PROSPECTIVE_FIELD_INTERVENTION")
    assert all(r.wave in ("pre","post") and r.arm in ("audit_notice","control") for r in rows)
    if len(rows)<8:raise ValueError("P73_P5_INSUFFICIENT_SOURCE_PANEL")
    groups={}
    announcement=_time(announcement_at)
    for row in rows:
        key=(row.arm,row.source_id)
        groups.setdefault(key,{})
        if row.wave in groups[key]:raise ValueError("P73_DUPLICATE_SOURCE_WAVE")
        groups[key][row.wave]=row
        if row.measured_outcome not in (0,1):raise ValueError("P73_NONBINARY_PREDECLARED_OUTCOME")
        if not row.source_sha or len(row.source_sha)!=64 or not row.source_role:
            raise ValueError("P73_MISSING_SOURCE_PROVENANCE")
        if not row.authorization or not row.independent_collector_id:
            raise ValueError("P73_MISSING_AUTHORITY_COLLECTOR")
        if not row.certified_external_page_capture:
            raise ValueError("P73_CUSTODIAN_EXTERNAL_CAPTURE_NOT_CERTIFIED")
        instant=_time(row.read_at)
        if (row.wave=="pre" and instant>=announcement) or (
            row.wave=="post" and instant<=announcement):
            raise ValueError("P73_PRE_POST_EVENT_TIME_MISALIGNED")
        if _time(row.source_updated_at)>instant or _time(row.authority_effective_from)>instant:
            raise ValueError("P73_FUTURE_DATED_EVIDENCE_OR_AUTHORITY")
    counts={"audit_notice":0,"control":0}
    for (arm,sid),waves in groups.items():
        if set(waves)!={"pre","post"}:raise ValueError("P73_MISSING_PANEL_WAVE")
        pre,post=waves["pre"],waves["post"]
        if pre.authorization!=post.authorization or pre.source_role!=post.source_role:
            # A real source-authority change is reported, not silently used
            # to claim that the observed outcome shift was caused by auditing.
            raise ValueError("P73_CHANGING_ROLE_OR_AUTHORITY_CONFOUND")
        if pre.independent_collector_id==post.independent_collector_id:
            # Independent snapshot collectors are a stronger design request.
            raise ValueError("P73_SAME_COLLECTOR_FOR_BOTH_TIMES")
        counts[arm]+=1
    if min(counts.values())<2:raise ValueError("P73_TOO_FEW_CONTROL_OR_TREATED_SOURCES")
    # Public notice itself may spill over to control sources; no-interference
    # cannot be inferred from this mechanical validator.
    means={}
    for arm in counts:
        for wave in ("pre","post"):
            values=[v[wave].measured_outcome for (a,_),v in groups.items() if a==arm]
            means[arm,wave]=F(sum(values),len(values))
    did=(means["audit_notice","post"]-means["audit_notice","pre"]
         -means["control","post"]+means["control","pre"])
    return {"kind":"P73_P5_PROSPECTIVE_TIME_AND_AUTHORITY_AUDIT_COURT",
       "panel_sources":len(groups),"audit_notice_sources":counts["audit_notice"],
       "contemporaneous_controls":counts["control"],
       "conditional_difference_in_differences":str(did),
       "estimation_scale":"BINARY_PREDECLARED_OUTCOME",
       "comparison":"SOURCE_PANEL_PREPOST_AUDIT_NOTICE_VS_CONTROL",
       "source_and_role_time_gate":"VALIDATED_FOR_SUPPLIED_FIXTURE",
       "individual_source_update_separated_from_audit":"NOT_CAUSALLY_IDENTIFIED",
       "assumption_parallel_trends":"NOT_IDENTIFIED_BY_TWO_WAVES",
       "assumption_no_spillover":"NOT_IDENTIFIED",
       "arm_allocation_randomization":"NOT_VERIFIED",
       "certified_really_external_authority":"NOT_VERIFIED_BY_BOOLEAN",
       "causal_effect":"HOLD_FIELD_STUDY_NOT_CONDUCTED"}

def fixture():
    rows=[]
    # Purely artificial binary outcomes; no persons, websites or real entities.
    for arm in ("audit_notice","control"):
        for j in range(2):
            for wave in ("pre","post"):
                rows.append(Snapshot(
                    source_id=f"{arm}_synthetic_{j}",arm=arm,wave=wave,
                    read_at="2026-10-01T10:00:00+09:00" if wave=="pre" else "2026-10-03T10:00:00+09:00",
                    source_sha="a"*64 if wave=="pre" else "b"*64,
                    source_role="CLAIM_WARRANT",authorization="TEST_ONLY",
                    authority_effective_from="2026-09-01T00:00:00+09:00",
                    source_updated_at="2026-09-30T00:00:00+09:00",
                    certified_external_page_capture=True,
                    measured_outcome=1 if wave=="post" and arm=="audit_notice" else 0,
                    independent_collector_id=f"SYNTHETIC_{wave}"))
    return rows

def self_test():
    rows=fixture();time="2026-10-02T10:00:00+09:00"
    res=validate(rows,time,preregistered=True,consent_and_legal_review=True)
    assert res["conditional_difference_in_differences"]=="1"
    assert res["causal_effect"].startswith("HOLD")
    def must_reject(mutator,reason):
        modified=mutator(list(rows))
        try:validate(modified,time,preregistered=True,consent_and_legal_review=True)
        except ValueError as err:
            assert reason in str(err),(reason,str(err))
        else:raise AssertionError("P73_FALSE_CERTIFICATION_"+reason)
    from dataclasses import replace
    must_reject(lambda r:r[:-1],"MISSING_PANEL_WAVE")
    must_reject(lambda r:[replace(x,source_role="WRONG_ROLE") if i==1 else x
                          for i,x in enumerate(r)],"CHANGING_ROLE")
    must_reject(lambda r:[replace(x,read_at="2026-10-04T10:00:00+09:00") if i==0 else x
                          for i,x in enumerate(r)],"MISALIGNED")
    must_reject(lambda r:[replace(x,source_updated_at="2026-11-01T00:00:00+09:00") if i==0 else x
                          for i,x in enumerate(r)],"FUTURE_DATED")
    must_reject(lambda r:[replace(x,certified_external_page_capture=False) if i==0 else x
                          for i,x in enumerate(r)],"NOT_CERTIFIED")
    try:validate(rows,time,preregistered=False,consent_and_legal_review=True)
    except ValueError as e:assert "UNAUTHORIZED" in str(e)
    else:raise AssertionError("P73_MISSING_PRE_REG_APPROVED")
    res.update({"real_field_sources":0,"real_audit_interventions":0,
                "actual_human_reviews":0,"paid_model_calls":0,
                "synthetic_demonstration_only":True})
    return res

if __name__=="__main__":
    print("P73_P5_PROSPECTIVE_PANEL_CONTRACT_PASS causal_effect=HOLD real_interventions=0")
    print(json.dumps(self_test(),indent=2,sort_keys=True))
