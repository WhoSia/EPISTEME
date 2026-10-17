"""EPISTEME-P75 P0: preregistered warrant-conditioned switch admission court.

This is an offline DESIGN and synthetic decision-counterexample validator.
It does not adjudicate humans, authenticate actual sources, evaluate models,
estimate causal effects, or measure real utility. Exact Fraction arithmetic.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from typing import Literal
import hashlib
import json

Action = Literal["KEEP", "SWITCH", "REVIEW"]


@dataclass(frozen=True)
class StudyCell:
    condition_id: str
    contract: str
    evidence_view: str
    authority_state: str
    ecology: str
    source_claim_group: str
    independent_external_warrant: bool = False
    human_judgments: int = 0
    real_source_time_certificate: bool = False
    model_responses: int = 0


@dataclass(frozen=True)
class DecisionDossier:
    packet_id: str
    claim_group_id: str
    task_ecology: str
    evidence_sha256: str
    source_access_cutoff: str
    net_gain_lower: F
    net_gain_upper: F
    output_correctness_A: bool
    output_correctness_B: bool
    source_original_authenticated: bool
    role_and_time_certified: bool
    minimal_sufficient_warrant_independently_adjudicated: bool
    independent_reviewers: int
    reviewer_identity_external_custodian_verified: bool
    switch_utility_empirically_validated: bool
    # Optional, machine-checkable route. Booleans are assertions, NOT proof receipts.
    independent_formal_certificate_replayed: bool = False
    source_claim_scope_mechanically_checked: bool = False
    target_is_conditional_model_decision: bool = False


CONTRACTS = ("strict_schema", "json_object")
EVIDENCE = ("FULL_SOURCE", "PROJECTED_SOURCE")
TEMPORAL = ("EFFECTIVE_AT_DECISION", "WITHDRAWN_BEFORE_DECISION",
            "SOURCE_TIME_UNRESOLVED")
ECOLOGIES = ("SCIFACT_HISTORICAL", "AVERITEC_HISTORICAL",
             "NEW_INDEPENDENT_MECHANISM_NOT_ACQUIRED")


def prospective_design() -> tuple[StudyCell, ...]:
    cells = []
    for c, e, t, x in product(CONTRACTS, EVIDENCE, TEMPORAL, ECOLOGIES):
        raw = "|".join((c, e, t, x))
        ident = hashlib.sha256(raw.encode()).hexdigest()[:16]
        cells.append(StudyCell(ident, c, e, t, x, "UNASSIGNED_HELDOUT_CLAIM_GROUP"))
    return tuple(cells)


def classical_minimax_regret(lower: F, upper: F) -> Action:
    if type(lower) is not F or type(upper) is not F or lower > upper:
        raise ValueError("P75_BAD_INTERVAL")
    r_switch = max(F(0), -lower)
    r_keep = max(F(0), upper)
    if r_switch < r_keep:
        return "SWITCH"
    if r_keep < r_switch:
        return "KEEP"
    return "REVIEW"  # equal regrets: a tie, not evidence that review adds value


def warrant_admission(dossier: DecisionDossier) -> tuple[Action, str]:
    """Conservative normative admission rule, not an empirically validated policy.

    REVIEW is only a proposed next action, not a completed human study.
    Classical regret baseline can switch without proof, a different *objective*.
    """
    if type(dossier.net_gain_lower) is not F or type(dossier.net_gain_upper) is not F:
        raise ValueError("P75_GAIN_MUST_BE_EXACT_FRACTION")
    if dossier.net_gain_lower > dossier.net_gain_upper:
        raise ValueError("P75_REVERSED_GAIN_INTERVAL")
    if not isinstance(dossier.evidence_sha256, str) or len(dossier.evidence_sha256) != 64:
        raise ValueError("P75_SOURCE_HASH_NOT_SHA256_LENGTH")
    if any(c not in "0123456789abcdef" for c in dossier.evidence_sha256):
        raise ValueError("P75_SOURCE_HASH_NOT_HEX")
    if dossier.independent_reviewers < 0:
        raise ValueError("P75_NEGATIVE_REVIEWER_COUNT")
    if not dossier.packet_id or not dossier.claim_group_id or not dossier.task_ecology:
        raise ValueError("P75_MISSING_PACKET_GROUP_OR_ECOLOGY")
    if not dossier.source_access_cutoff:
        raise ValueError("P75_MISSING_DECISION_CUTOFF")
    # Intentional strictness: an author-written Boolean or source URL is not
    # a third-party certificate. In real submissions custody must be external.
    # A mechanical proof/certificate replay is a separate admissible route
    # for a CONDITIONAL MODEL-RELATIVE decision, no human rater required.
    # An observational HUMAN PREFERENCE estimand is a different project and
    # cannot be inferred from a proof or from simulated participant responses.
    nonhuman = (dossier.target_is_conditional_model_decision
                and dossier.independent_formal_certificate_replayed
                and dossier.source_claim_scope_mechanically_checked)
    optional_human = (dossier.independent_reviewers >= 2
                      and dossier.reviewer_identity_external_custodian_verified
                      and not dossier.target_is_conditional_model_decision)
    certified = (
        dossier.source_original_authenticated
        and dossier.role_and_time_certified
        and dossier.minimal_sufficient_warrant_independently_adjudicated
        and (nonhuman or optional_human)
        and (dossier.target_is_conditional_model_decision
             or dossier.switch_utility_empirically_validated)
    )
    if not certified:
        return "REVIEW", "P75_CERTIFICATION_AND_UTILITY_HOLD"
    if dossier.net_gain_lower > 0:
        return "SWITCH", "HYPOTHETICAL_ALL_GATES_AND_ROBUST_GAIN"
    if dossier.net_gain_upper < 0:
        return "KEEP", "HYPOTHETICAL_ALL_GATES_AND_ROBUST_LOSS"
    return "REVIEW", "HYPOTHETICAL_CERTIFIED_BUT_GAIN_SIGN_UNIDENTIFIED"


def test_no_conclusion_promotion() -> dict:
    cells = prospective_design()
    assert len(cells) == 36 and len({c.condition_id for c in cells}) == 36
    assert all(c.human_judgments == c.model_responses == 0 for c in cells)
    assert all(not c.independent_external_warrant and not c.real_source_time_certificate for c in cells)
    assert len({(c.contract,c.evidence_view,c.authority_state,c.ecology) for c in cells}) == 36
    # Intentional incomplete mechanism coverage: the third label is a future
    # condition, NOT a new ecology we have actually obtained.
    assert sum(c.ecology == ECOLOGIES[2] for c in cells) == 12

    sha = hashlib.sha256(b"P75_SYNTHETIC_FIXED_PLACEHOLDER_NOT_SOURCE_BYTES").hexdigest()
    sample = DecisionDossier(
        packet_id="MOCK-C1", claim_group_id="MOCK-CLUSTER-1",
        task_ecology="MOCK_ECOLOGY", evidence_sha256=sha,
        source_access_cutoff="2026-10-11",
        net_gain_lower=F(1, 4), net_gain_upper=F(3, 4),
        output_correctness_A=True, output_correctness_B=True,
        source_original_authenticated=False, role_and_time_certified=False,
        minimal_sufficient_warrant_independently_adjudicated=False,
        independent_reviewers=0, reviewer_identity_external_custodian_verified=False,
        switch_utility_empirically_validated=False,
    )
    # Same surface correctness: a seemingly profitable robust switch is not
    # permitted under a proof-bearing policy without independent warrant.
    assert classical_minimax_regret(sample.net_gain_lower,sample.net_gain_upper) == "SWITCH"
    action, reason = warrant_admission(sample)
    assert (action,reason) == ("REVIEW","P75_CERTIFICATION_AND_UTILITY_HOLD")

    # The next examples are counterfactual toy dossiers. Marking author booleans
    # true proves ONLY that the branch behaves as designed; NO real certification.
    hypothetical = DecisionDossier(
        **{**sample.__dict__,
           "source_original_authenticated":True, "role_and_time_certified":True,
           "minimal_sufficient_warrant_independently_adjudicated":True,
           "independent_reviewers":2,
           "reviewer_identity_external_custodian_verified":True,
           "switch_utility_empirically_validated":True}
    )
    assert warrant_admission(hypothetical) == (
        "SWITCH","HYPOTHETICAL_ALL_GATES_AND_ROBUST_GAIN")
    revocable = DecisionDossier(**{**hypothetical.__dict__,
                                   "role_and_time_certified":False})
    assert warrant_admission(revocable)[0] == "REVIEW"
    lost_witness = DecisionDossier(**{**hypothetical.__dict__,
        "minimal_sufficient_warrant_independently_adjudicated":False})
    assert warrant_admission(lost_witness)[0] == "REVIEW"
    single_reviewer = DecisionDossier(**{**hypothetical.__dict__,
                                         "independent_reviewers":1})
    assert warrant_admission(single_reviewer)[0] == "REVIEW"
    # Non-human structural warrant: independent replay is REQUIRED, human
    # count = 0 is entirely acceptable for a CONDITIONAL model conclusion.
    model_conditional = DecisionDossier(**{**hypothetical.__dict__,
        "independent_reviewers":0,
        "reviewer_identity_external_custodian_verified":False,
        "switch_utility_empirically_validated":False,
        "independent_formal_certificate_replayed":True,
        "source_claim_scope_mechanically_checked":True,
        "target_is_conditional_model_decision":True})
    assert warrant_admission(model_conditional)[0] == "SWITCH"
    assert warrant_admission(DecisionDossier(**{**model_conditional.__dict__,
        "independent_formal_certificate_replayed":False}))[0] == "REVIEW"
    assert warrant_admission(DecisionDossier(**{**model_conditional.__dict__,
        "source_claim_scope_mechanically_checked":False}))[0] == "REVIEW"
    assert warrant_admission(DecisionDossier(**{**model_conditional.__dict__,
        "target_is_conditional_model_decision":False}))[0] == "REVIEW"
    no_utility = DecisionDossier(**{**hypothetical.__dict__,
                                    "switch_utility_empirically_validated":False})
    assert warrant_admission(no_utility)[0] == "REVIEW"
    gain_uncertain = DecisionDossier(**{**hypothetical.__dict__,
        "net_gain_lower":F(-1,4),"net_gain_upper":F(3,4)})
    assert warrant_admission(gain_uncertain)[0] == "REVIEW"

    # Standard minimax regret chooses SWITCH for a broad interval, whereas
    # robust dominance and warrant admission refuse: distinct objectives,
    # no claim that author-designed policy beats standard decision theory.
    assert classical_minimax_regret(F(-1, 4),F(3, 4)) == "SWITCH"

    try: warrant_admission(DecisionDossier(
        **{**sample.__dict__,"evidence_sha256":"0"*63}))
    except ValueError as err: assert "SOURCE_HASH" in str(err)
    else: raise AssertionError("P75_INVALID_HASH_ACCEPTED")
    try: warrant_admission(DecisionDossier(
        **{**sample.__dict__,"independent_reviewers":-1}))
    except ValueError as err: assert "NEGATIVE_REVIEWER" in str(err)
    else: raise AssertionError("P75_INVALID_REVIEWER_COUNT_ACCEPTED")

    return {
        "stage":"EPISTEME_P75_P0_AUTHORIZED_DESIGN_ONLY",
        "status":"SYNTHETIC_GATE_AND_FACTORIAL_PRECOMMIT_PASS",
        "prospective_factorial_cells":len(cells),
        "factorial_structure":"2 contract x 2 evidence x 3 time x 3 ecology",
        "third_heldout_ecology_acquired":False,
        "claim_clusters_assigned":0,
        "blinded_independent_gold_labels_obtained":0,
        "actual_P69_human_judgments":0,
        "actual_P70_human_judgments":0,
        "actual_P71_human_judgments":0,
        "new_model_responses":0,
        "new_provider_calls":0,
        "real_field_studies":0,
        "real_switch_utility_outcomes":0,
        "hypothetical_classical_minimax_prefers_switch":True,
        "p75_uncertified_counterexample_policy":"REVIEW",
        "p75_hypothetically_fully_certified_positive_policy":"SWITCH",
        "human_raters_required_for_conditional_model_warrant":False,
        "nonhuman_certificate_route_synthetic_only":True,
        "human_preference_effect_measured":False,
        "independent_warrant_established":False,
        "causal_switch_improvement_identified":False,
        "novel_behavioral_effect":False,
        "classical_rival_advantage_falsified":False,
        "actual_heldout_empirical_test":"BLOCKED_REQUIRED_INPUTS_MISSING"
    }


if __name__ == "__main__":
    print(json.dumps(test_no_conclusion_promotion(),ensure_ascii=False,sort_keys=True,indent=2))
