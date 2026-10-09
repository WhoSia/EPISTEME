"""EPISTEME P69/P70: fail-closed, source-receipt-bounded transition court.

CLOSE an executed experiment or source-audit phase without falsely closing a
manuscript, an unrun human adjudication or a transport identification claim.
"""
from __future__ import annotations
import argparse,json,copy
from pathlib import Path

NEED={
"p69_pilot":("INSTRUMENT_PILOT_VERDICT","TECHNICAL_PILOT_HOLD"),
"p69_r1":("PAIRED_MEASUREMENT_REPAIR_VERDICT","REPAIR_MEASUREMENT_HOLD"),
"p70_scifact":("INDEPENDENT_SOURCE_PILOT_VERDICT","PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE"),
}

def read(path):
    p=Path(path)
    x=json.loads(p.read_text())
    if not isinstance(x,dict):raise ValueError("EPISTEME_BAD_RECEIPT")
    return x

def adjudicate(p69_pilot,p69_r1,p70_scifact,review,bridge):
    for key,actual in (("p69_pilot",p69_pilot),("p69_r1",p69_r1),("p70_scifact",p70_scifact)):
        kind,verdict=NEED[key]
        if actual.get("kind")!=kind or actual.get("verdict")!=verdict:
            raise ValueError("EPISTEME_SOURCE_OR_VERDICT_NOT_FROZEN_"+key)
    if p69_pilot.get("provider_invocation_slots")!=192:
        raise ValueError("EPISTEME_P69_PILOT_NOT_192")
    if p69_r1.get("provider_slots")!=64:
        raise ValueError("EPISTEME_P69_R1_NOT_64")
    if p70_scifact.get("total_provider_slots")!=32 or p70_scifact.get("distinct_source_ecologies")!=1:
        raise ValueError("EPISTEME_P70_SCI_NOT_SINGLE_ECOLOGY")
    if review.get("verdict")!="P70_PACKET_HUMAN_ADJUDICATION_HOLD" or review.get("reviewers_completed")!=0:
        raise ValueError("EPISTEME_REVIEW_STATUS_MISREPRESENTED")
    if review.get("packets")!=16:
        raise ValueError("EPISTEME_PACKET_GRID_MISSING")
    if bridge.get("kind")!="SCIFACT_AVERITEC_INDEPENDENT_ORIGINAL_SOURCE_PARTIAL_BRIDGE":
        raise ValueError("EPISTEME_BRIDGE_RECEIPT_MISSING")
    if bridge.get("same_polarity_candidate_pairs")!=8 or bridge.get("semantic_bridge")!="HOLD":
        raise ValueError("EPISTEME_FABRICATED_SEMANTIC_BRIDGE")
    if bridge.get("cross_ecology_effect")!="NOT_IDENTIFIED":
        raise ValueError("EPISTEME_FABRICATED_TRANSPORT")
    if bridge.get("provider_calls")!=0:
        raise ValueError("EPISTEME_UNAUTHORIZED_PROVIDER_CALLS")
    return {
       "stage":"EPISTEME-P69/P70",
       "kind":"SCOPE_BOUND_TRANSITION_COURT",
       "verdict":"SCOPED_NEGATIVE_AND_PARTIAL_PHASES_CLOSED_WITH_SCIENCE_HOLDS",
       "evidence":{
           "p69_instrumentation":"192_CALL_NEGATIVE_MEASUREMENT_PHASE_CLOSED",
           "p69_r1_calibration":"64_CALL_NEGATIVE_CALIBRATION_PHASE_CLOSED",
           "p70_scifact":"32_CALL_SINGLE_ECOLOGY_CALIBRATION_PHASE_CLOSED",
           "p70_ecology2":"500_SOURCE_RECORDS_AND_16_PACKET_COMPILATION_CLOSED",
           "p70_typed_bridge":"8_CANDIDATE_PAIRS_PROVENANCE_POLARITY_ONLY",
       },
       "not_closed":{
           "p69_manuscript":"PAPER_CONSTRUCT_HOLD",
           "p69_claim_of_transport":"NOT_ESTABLISHED",
           "p70_blind_human_packet_judgments":"0_OF_32_RECEIVED",
           "p70_warrant_and_dependency_bridge":"SEMANTIC_HOLD",
           "p70_prospective_cross_ecology_model_effect":"NOT_RUN_NOT_IDENTIFIED",
       },
       "p71_status":"TITLE_PROPOSED_NOT_EMPIRICALLY_OPEN",
       "future_model_call_budget_authorized":0,
       "research_authority":"EPISTEME_POSITIVE_THEORY_AND_NEGATIVE_EXPERIMENTS_NOT_FULL_PAPER_CLOSURE",
       "historic_workflows_are_immutable":True
    }

def self_test():
    a={"kind":NEED["p69_pilot"][0],"verdict":NEED["p69_pilot"][1],
       "provider_invocation_slots":192}
    b={"kind":NEED["p69_r1"][0],"verdict":NEED["p69_r1"][1],"provider_slots":64}
    c={"kind":NEED["p70_scifact"][0],"verdict":NEED["p70_scifact"][1],
       "total_provider_slots":32,"distinct_source_ecologies":1}
    d={"verdict":"P70_PACKET_HUMAN_ADJUDICATION_HOLD","reviewers_completed":0,"packets":16}
    e={"kind":"SCIFACT_AVERITEC_INDEPENDENT_ORIGINAL_SOURCE_PARTIAL_BRIDGE",
       "same_polarity_candidate_pairs":8,"semantic_bridge":"HOLD",
       "cross_ecology_effect":"NOT_IDENTIFIED","provider_calls":0}
    result=adjudicate(a,b,c,d,e)
    assert result["not_closed"]["p69_manuscript"]=="PAPER_CONSTRUCT_HOLD"
    assert result["future_model_call_budget_authorized"]==0
    for idx,field,val in ((0,"verdict","MEASUREMENT_PILOT_READY"),
                          (1,"verdict","CALIBRATION_SIGNAL_PRESENT"),
                          (2,"distinct_source_ecologies",2),
                          (3,"reviewers_completed",2),
                          (4,"semantic_bridge","PASS")):
        inputs=[copy.deepcopy(x) for x in (a,b,c,d,e)]
        inputs[idx][field]=val
        try:adjudicate(*inputs)
        except ValueError:pass
        else:raise AssertionError("EPISTEME_FALSE_SCIENCE_CLOSURE_ACCEPTED "+field)
    print("EPISTEME_P69_P70_SCOPED_CLOSURE_SELFTEST_PASS adversarial_statuses=5 calls=0")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for key in ("p69-pilot","p69-r1","p70-scifact","eco2-review","bridge","out"):
        p.add_argument("--"+key)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:self_test()
    else:
        vals=[getattr(a,k.replace("-","_")) for k in
              ("p69-pilot","p69-r1","p70-scifact","eco2-review","bridge","out")]
        if not all(vals):p.error("all six paths mandatory")
        report=adjudicate(*(read(v) for v in vals[:5]))
        out=Path(vals[-1]);out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
        print("EPISTEME_P69_P70_SCOPED_PHASE_CLOSURE_PASS paper_closure=HOLD human_review=HOLD model_calls=0")
