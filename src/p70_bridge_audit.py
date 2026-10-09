"""P70 bridge audit of the actual P69 synthetic instrument, with adversaries.

Tests witness-role invariance and trace-order commutation; it is NOT a
cross-ecology behavioral equivalence or causal-effect validation.
"""
from __future__ import annotations
from copy import deepcopy

from p69_task_factory import TASKS, SEMANTICS, FHL_CONTEXTS, build
from p69_witness_enumerator import minimal_witnesses


class BridgeFailure(AssertionError):
    pass


def role(evidence_id: str) -> str:
    left, sep, right = evidence_id.partition(":ev:")
    if not sep or not left or not right:
        raise BridgeFailure("P70_MISSING_EVIDENCE_ROLE")
    return right


def witness_signature(packet: dict) -> tuple:
    return tuple(sorted(tuple(sorted(role(i) for i in w))
                        for w in minimal_witnesses(packet)))


ROW_KEYS=("provenance_records","source_records","trigger_records","measurement_records")


def trace_index(packet: dict) -> dict:
    result={}
    for key in ROW_KEYS:
        for row in packet.get(key,()):
            name=(key,role(row["evidence_id"]))
            if name in result:
                raise BridgeFailure("P70_DUPLICATE_ROW_ROLE")
            result[name]=tuple(row["trace"])
    return result


def check_T(base: dict, transformed: dict) -> None:
    """Within same task, R and nuisance context, T reverses EACH trace."""
    aa=trace_index(base)
    bb=trace_index(transformed)
    if set(aa)!=set(bb) or any(bb[k]!=tuple(reversed(aa[k])) for k in aa):
        raise BridgeFailure("P70_T_COMMUTATION_FAILURE")


def lattice_court() -> dict:
    cases=0
    comparisons=0
    commutations=0
    for task in TASKS:
        for semantic in SEMANTICS:
            for f,h,l in FHL_CONTEXTS:
                nuisance={k for k,bit in zip("FHL",(f,h,l)) if bit}
                packets={}
                for r in (False,True):
                    for t in (False,True):
                        vertex=tuple(x for x in "RFHTL"
                                     if (x in nuisance or (x=="R" and r) or (x=="T" and t)))
                        packets[(r,t)]=build(task,vertex,semantic)
                        cases+=1
                anchor=witness_signature(packets[(False,False)])
                for key,packet in packets.items():
                    if witness_signature(packet)!=anchor:
                        raise BridgeFailure("P70_WITNESS_BIJECTION_FAILURE")
                    comparisons+=1
                for r in (False,True):
                    check_T(packets[(r,False)],packets[(r,True)])
                    commutations+=1
    assert cases==len(TASKS)*len(SEMANTICS)*len(FHL_CONTEXTS)*4==256
    assert comparisons==256 and commutations==128
    return {"synthetic_packets_audited":cases,
            "witness_role_matches":comparisons,"trace_commutations":commutations,
            "claim_ceiling":"SYNTHETIC_WITHIN_COMPILER_EQUIVARIANCE_ONLY"}


def adversarial_court() -> dict:
    source=build("provenance_2",(),"valid")
    first=deepcopy(source)
    for row in first["response_rules"]:
        if role(row["evidence_id"])=="alternate_rule":
            row["contrast"]="different"
    second=deepcopy(first)
    second["provenance_records"]=[
        x for x in second["provenance_records"]
        if role(x["evidence_id"])!="alternate_origin"]
    before=witness_signature(first)
    after=witness_signature(second)
    assert len(before)==2 and len(after)==1
    assert bool(before)==bool(after)  # unchanged truth/answer
    assert before!=after              # proof-witness loss
    base=build("provenance_1",(),"valid")
    honest_t=build("provenance_1",("T",),"valid")
    check_T(base,honest_t)
    impostor=deepcopy(base)
    impostor["provenance_records"].reverse()  # H-like row order, mislabeled as T
    try:check_T(base,impostor)
    except BridgeFailure:pass
    else:raise AssertionError("P70_WRONG_OPERATOR_BRIDGE_ACCEPTED")
    return {"answer_preserving_proof_loss":True,
            "same_label_different_operation_rejected":True,
            "claim_ceiling":"SYNTHETIC_ADVERSARIAL_CONSTRUCTION_ONLY"}


def self_test():
    a=lattice_court()
    b=adversarial_court()
    assert a["synthetic_packets_audited"]==256
    assert all((b["answer_preserving_proof_loss"],b["same_label_different_operation_rejected"]))
    print("P70_BRIDGE_COURT_PASS packets=256 witness_matches=256 trace_commutations=128 counterexamples=2 provider_calls=0")


if __name__=="__main__":
    self_test()
