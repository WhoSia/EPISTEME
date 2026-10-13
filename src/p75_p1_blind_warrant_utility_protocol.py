"""P75-P1 prospective human-warrant and switching-utility contract.

No actual human reviews, real source authentication, policy outcomes or calls
are generated. The initial roster uses SYNTHETIC reviewers, not credentials.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from fractions import Fraction as F
import hashlib
import json

ARMS=("FULL_ORIGINAL","MATCHED_PROJECTED")
CHOICES=("KEEP","SWITCH","REVIEW")
VERDICTS=("SUPPORTS","REFUTES","NOT ENOUGH INFO")

@dataclass(frozen=True)
class Assignment:
    claim_cluster:str
    condition:str
    reviewer_slot:str
    masked_packet_id:str
    simulated_only:bool=True

@dataclass(frozen=True)
class ReviewInput:
    packet_sha256:str
    claim_cluster:str
    reviewer_slot:str
    condition:str
    target_claim_verdict:str
    proposed_witness_ids:tuple[str,...]
    available_evidence_ids:tuple[str,...]
    necessary_after_removal:tuple[bool,...]
    sufficient_full_set:bool
    independently_verified_original_source:bool
    independently_verified_source_time_role:bool
    independent_external_custodian:bool
    real_human_review:bool
    choice:str
    source_access_limitations:tuple[str,...]=()
    ambiguity_flags:tuple[str,...]=()


def precommit_schedule(clusters:tuple[str,...])->tuple[Assignment,...]:
    """Each cluster: 2 raters FULL + 2 PROJECTED, crossover across clusters.

    Every reviewer sees a SINGLE arm of any claim cluster. Across 2+ clusters
    parity balances reviewers across arms. It is a scheduling contract only.
    """
    if len(clusters)<2 or len(clusters)!=len(set(clusters)):
        raise ValueError("P75_REQUIRE_DISJOINT_CLUSTERS")
    reviewers=("SIMULATED_R01","SIMULATED_R02","SIMULATED_R03","SIMULATED_R04")
    result=[]
    for j,cluster in enumerate(clusters):
        if not cluster.strip():
            raise ValueError("P75_EMPTY_CLUSTER")
        for i,reviewer in enumerate(reviewers):
            condition=ARMS[(i//2+j)%2]
            raw=f"{cluster}|{condition}|{reviewer}"
            result.append(Assignment(
                claim_cluster=cluster,condition=condition,
                reviewer_slot=reviewer,
                masked_packet_id=hashlib.sha256(raw.encode()).hexdigest()[:20]))
    assert all(len([x for x in result if x.claim_cluster==c and x.condition==a])==2
               for c in clusters for a in ARMS)
    assert len({x.masked_packet_id for x in result})==len(result)
    assert all(len({x.condition for x in result
                    if x.claim_cluster==c and x.reviewer_slot==r})==1
               for c in clusters for r in reviewers)
    return tuple(result)


def validate_review_shape(v:ReviewInput)->str:
    if (len(v.packet_sha256)!=64 or any(c not in "0123456789abcdef" for c in v.packet_sha256)):
        raise ValueError("P75_PACKET_SHA_UNTRUSTED")
    if v.condition not in ARMS or v.target_claim_verdict not in VERDICTS or v.choice not in CHOICES:
        raise ValueError("P75_INVALID_CLASS_OR_ACTION")
    if not v.claim_cluster or not v.reviewer_slot:
        raise ValueError("P75_MISSING_ASSIGNMENT")
    required=set(v.proposed_witness_ids)
    if not required or len(required)!=len(v.proposed_witness_ids):
        raise ValueError("P75_WITNESS_SET_EMPTY_OR_DUPLICATE")
    if not required.issubset(set(v.available_evidence_ids)):
        raise ValueError("P75_WITNESS_NOT_ACCESSIBLE")
    if len(v.necessary_after_removal)!=len(v.proposed_witness_ids):
        raise ValueError("P75_WITNESS_NECESSITY_INCOMPLETE")
    if any(not isinstance(x,bool) for x in v.necessary_after_removal):
        raise ValueError("P75_WITNESS_NECESSITY_BAD_TYPE")
    if not all(isinstance(x,str) for x in v.source_access_limitations+v.ambiguity_flags):
        raise ValueError("P75_REVIEW_FLAGS_BAD_TYPE")
    if (not v.sufficient_full_set or not all(v.necessary_after_removal)):
        return "P75_INDEPENDENT_MINIMAL_WARRANT_NOT_ACCEPTED"
    if (not v.real_human_review or not v.independent_external_custodian
        or not v.independently_verified_original_source
        or not v.independently_verified_source_time_role):
        return "P75_PROSPECTIVE_SCHEMA_ONLY_CUSTODY_NOT_VERIFIED"
    # This branch is still only a declaration; a genuine external custodian
    # must validate identity + proof receipts outside this code. No booleans
    # in a user-supplied object can prove real independent participation.
    return "P75_SUBMISSION_REQUIRES_OUT_OF_BAND_CUSTODIAL_CONFIRMATION"


@dataclass(frozen=True)
class UtilityPolicy:
    correct_switch_benefit:F
    incorrect_switch_harm:F
    switch_transition_cost:F
    independent_review_cost:F
    decision_delay_cost:F
    # Policy utility cannot be identified from dataset labels alone.
    externally_calibrated:bool=False


def utility_preflight(p:UtilityPolicy)->str:
    if any(type(x) is not F for x in (
        p.correct_switch_benefit,p.incorrect_switch_harm,
        p.switch_transition_cost,p.independent_review_cost,p.decision_delay_cost)):
        raise ValueError("P75_COSTS_EXACT_FRACTIONS")
    if any(x<0 for x in (
        p.correct_switch_benefit,p.incorrect_switch_harm,
        p.switch_transition_cost,p.independent_review_cost,p.decision_delay_cost)):
        raise ValueError("P75_NEGATIVE_COST_OR_BENEFIT")
    if not p.externally_calibrated:
        return "P75_SWITCH_UTILITY_EMPIRICAL_HOLD"
    return "P75_COSTS_CLAIMED_CALIBRATED_REQUIRE_EXTERNAL_RECEIPT"


def expect_error(fn,token):
    try:fn()
    except ValueError as e:assert token in str(e),str(e)
    else:raise AssertionError("P75_ACCEPTED_"+token)


def self_test():
    schedule=precommit_schedule(("CLUSTER_DEMO_A","CLUSTER_DEMO_B",
                                 "CLUSTER_DEMO_C","CLUSTER_DEMO_D"))
    assert len(schedule)==16
    assert len({x.claim_cluster for x in schedule})==4
    for r in {x.reviewer_slot for x in schedule}:
        arms=[x.condition for x in schedule if x.reviewer_slot==r]
        assert arms.count(ARMS[0])==arms.count(ARMS[1])==2
    assert all(a.simulated_only for a in schedule)
    sample=ReviewInput(
        packet_sha256=hashlib.sha256(b"P75_P1_SYNTHETIC_PACKET").hexdigest(),
        claim_cluster="CLUSTER_DEMO_A",reviewer_slot="SIMULATED_R01",
        condition=ARMS[0],target_claim_verdict="SUPPORTS",
        proposed_witness_ids=("SLOT-1",),available_evidence_ids=("SLOT-1","DECOY-1"),
        necessary_after_removal=(True,),sufficient_full_set=True,
        independently_verified_original_source=False,
        independently_verified_source_time_role=False,
        independent_external_custodian=False,real_human_review=False,
        choice="REVIEW",source_access_limitations=("NO_REAL_ORIGINAL_CERTIFICATE",))
    assert validate_review_shape(sample)=="P75_PROSPECTIVE_SCHEMA_ONLY_CUSTODY_NOT_VERIFIED"
    assert validate_review_shape(replace(sample,necessary_after_removal=(False,)))==(
        "P75_INDEPENDENT_MINIMAL_WARRANT_NOT_ACCEPTED")
    expect_error(lambda:validate_review_shape(replace(
        sample,available_evidence_ids=("DECOY-1",))),"WITNESS_NOT_ACCESSIBLE")
    expect_error(lambda:validate_review_shape(replace(
        sample,proposed_witness_ids=("SLOT-1","SLOT-1"))),"WITNESS_SET_EMPTY")
    expect_error(lambda:validate_review_shape(replace(
        sample,necessary_after_removal=())),"WITNESS_NECESSITY_INCOMPLETE")
    expect_error(lambda:precommit_schedule(("ONE",)),"REQUIRE_DISJOINT")
    assert validate_review_shape(replace(
        sample,independently_verified_original_source=True,
        independently_verified_source_time_role=True,independent_external_custodian=True,
        real_human_review=True))=="P75_SUBMISSION_REQUIRES_OUT_OF_BAND_CUSTODIAL_CONFIRMATION"
    hypothetical=UtilityPolicy(F(1),F(1),F(1,4),F(1,10),F(1,20))
    assert utility_preflight(hypothetical)=="P75_SWITCH_UTILITY_EMPIRICAL_HOLD"
    assert utility_preflight(replace(hypothetical,externally_calibrated=True))==(
        "P75_COSTS_CLAIMED_CALIBRATED_REQUIRE_EXTERNAL_RECEIPT")
    expect_error(lambda:utility_preflight(replace(
        hypothetical,incorrect_switch_harm=F(-1,4))),"NEGATIVE_COST")
    return {
        "study":"P75_P1_PROSPECTIVE_WARRANT_AND_SWITCH_UTILITY",
        "status":"SIMULATED_SCHEDULE_AND_SCHEMA_VALIDATION_PASS_ONLY",
        "hypothetical_claim_clusters":4,
        "hypothetical_review_slots":16,
        "prospective_raters_per_arm_per_cluster":2,
        "crossed_reviewer_assignments_balance_by_cluster":True,
        "same_reviewer_sees_both_arms_same_cluster":False,
        "assigned_independent_real_humans":0,
        "observed_independently_certified_minimal_warrants":0,
        "measured_real_switch_utility":0,
        "external_source_original_certificate":False,
        "reviewer_independence_verified_out_of_band":False,
        "actual_study_randomization_executed":False,
        "dataset_gold_is_not_independent_warrant":True,
        "new_paid_model_calls":0,
        "human_participant_recruitment":0,
        "preregistered_final_statistical_analysis":"NOT_SEALED_BLOCKED_ON_REAL_CLUSTER_CENSUS_AND_COSTS"
    }

if __name__=="__main__":
    print(json.dumps(self_test(),indent=2,sort_keys=True))
