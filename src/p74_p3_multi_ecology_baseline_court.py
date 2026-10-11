"""P74-P3 scoped comparative diagnostic on manually transcribed public records.

This is NOT independent held-out generalization, live verification, causal
identification, legal advice, nor a new temporal database invention.
The conventional typed-time PROV rival is expected to tie this representation.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json


@dataclass(frozen=True)
class Record:
    key: str
    issuer: str
    action: str
    published: str
    document_id: str
    source: str
    target: str = ""


RECORDS = (
    Record("hearing_original","FDA","DIRECT_FINAL","2024-09-20","2024-21231",
           "https://www.govinfo.gov/content/pkg/FR-2024-09-20/html/2024-21231.htm"),
    Record("hearing_correction","FDA","CORRECTION","2024-10-18","2024-24100",
           "https://www.govinfo.gov/content/pkg/FR-2024-10-18/html/2024-24100.htm","hearing_original"),
    Record("hearing_withdrawal","FDA","WITHDRAWAL","2025-01-17","2025-01145",
           "https://www.govinfo.gov/content/pkg/FR-2025-01-17/html/2025-01145.htm","hearing_original"),
    Record("food_original","FDA","DIRECT_FINAL","2025-07-17","2025-13421",
           "https://www.govinfo.gov/content/pkg/FR-2025-07-17/html/2025-13421.htm"),
    Record("food_confirmation","FDA","CONFIRMATION","2025-09-26","2025-18730",
           "https://www.govinfo.gov/content/pkg/FR-2025-09-26/html/2025-18730.htm","food_original"),
    Record("irs_proposal_2019","IRS","PROPOSED_RULE","2019-09-10","2019_PROPOSAL_84_FR_47455",
           "https://www.govinfo.gov/content/pkg/FR-2019-09-10/html/2019-17822.htm"),
    Record("irs_proposal_2020","IRS","PROPOSED_REVISION","2020-01-14","2020_PROPOSAL_85_FR_2061",
           "https://www.govinfo.gov/content/pkg/FR-2020-01-14/html/2020-00340.htm","irs_proposal_2019"),
    Record("irs_withdrawal","IRS","PROPOSAL_WITHDRAWAL","2025-07-02","2025-12193",
           "https://www.govinfo.gov/content/pkg/FR-2025-07-02/html/2025-12193.htm","irs_proposal_2019"),
)

# The dates below are authored source metadata, not independently authenticated
# original byte hashes or database transaction timestamps.
FROZEN_METADATA = {
    "hearing_original": {"effective_scheduled":"2025-02-03","special_corrected":"2025-12-18"},
    "hearing_withdrawal": {"withdrawal_effective":"2025-01-17"},
    "food_original":{"effective_scheduled":"2025-09-22"},
    "food_confirmation":{"confirmed_effective":"2025-09-22"},
    "irs_withdrawal":{"proposal_withdrawn":"2025-07-02"},
}


@dataclass(frozen=True)
class Question:
    id: str
    branch: str
    role: str
    known_as_of: str
    target_date: str
    expected: str


QUESTIONS = (
    Question("H1","HEARING","HISTORICAL_PUBLICATION","2024-10-01","2024-09-20","HISTORICAL_SUPPORTED"),
    Question("H2","HEARING","NORMATIVE_EFFECT","2024-10-01","2024-10-01","NOT_YET_EFFECTIVE"),
    Question("H3","HEARING","NORMATIVE_EFFECT","2024-11-01","2025-02-04","PROJECTED_CONDITIONAL"),
    Question("H4","HEARING","NORMATIVE_EFFECT","2025-01-20","2025-02-04","WITHDRAWN_BEFORE_EFFECT"),
    Question("H5","HEARING","HISTORICAL_PUBLICATION","2025-01-20","2025-02-04","HISTORICAL_SUPPORTED"),
    Question("H6","HEARING","SPECIAL_EFFECT","2024-09-30","2025-02-04","EFFECTIVE_DATE_NOT_KNOWN"),
    Question("H7","HEARING","SPECIAL_EFFECT","2024-11-01","2025-02-04","NOT_YET_EFFECTIVE"),
    Question("F1","FOOD","NORMATIVE_EFFECT","2025-08-01","2025-09-23","PROJECTED_CONDITIONAL"),
    Question("F2","FOOD","NORMATIVE_EFFECT","2025-09-23","2025-09-23","UNCONFIRMED_AS_OF"),
    Question("F3","FOOD","NORMATIVE_EFFECT","2025-09-27","2025-09-23","CONFIRMED_EFFECT"),
    Question("F4","FOOD","CONFIRMATION_EXISTENCE","2025-09-24","2025-09-24","NOT_YET_PUBLISHED"),
    Question("F5","FOOD","CONFIRMATION_EXISTENCE","2025-09-27","2025-09-26","HISTORICAL_SUPPORTED"),
    Question("I1","IRS","HISTORICAL_PUBLICATION","2020-01-20","2019-09-10","HISTORICAL_SUPPORTED"),
    Question("I2","IRS","NORMATIVE_EFFECT","2020-01-20","2020-01-20","PROPOSAL_NOT_EFFECTIVE_LAW"),
    Question("I3","IRS","PROPOSAL_PENDING","2025-06-01","2025-06-01","PROPOSAL_PENDING_NOT_LAW"),
    Question("I4","IRS","PROPOSAL_PENDING","2025-07-03","2025-07-03","PROPOSAL_WITHDRAWN"),
    Question("I5","IRS","HISTORICAL_PUBLICATION","2025-07-03","2019-09-10","HISTORICAL_SUPPORTED"),
)


def d(s: str) -> date:
    return date.fromisoformat(s)


def typed_projection(q: Question) -> str:
    a, t = d(q.known_as_of), d(q.target_date)
    if q.branch == "HEARING":
        first, corrected, withdrawn = d("2024-09-20"), d("2024-10-18"), d("2025-01-17")
        if a < first:
            return "NOT_YET_PUBLISHED"
        if q.role == "HISTORICAL_PUBLICATION":
            return "HISTORICAL_SUPPORTED"
        if q.role not in ("NORMATIVE_EFFECT","SPECIAL_EFFECT"):
            raise ValueError("P74_UNKNOWN_PROOF_ROLE")
        if a >= withdrawn and t >= withdrawn:
            return "WITHDRAWN_BEFORE_EFFECT"
        eff = d("2025-12-18") if q.role == "SPECIAL_EFFECT" and a >= corrected else (
            None if q.role == "SPECIAL_EFFECT" else d("2025-02-03"))
        if eff is None:
            return "EFFECTIVE_DATE_NOT_KNOWN"
        if t < eff:
            return "NOT_YET_EFFECTIVE"
        return "PROJECTED_CONDITIONAL" if t > a else "DOCUMENTARY_EFFECT_UNVERIFIED"
    if q.branch == "FOOD":
        first, confirmed = d("2025-07-17"), d("2025-09-26")
        if q.role == "CONFIRMATION_EXISTENCE":
            return "HISTORICAL_SUPPORTED" if a >= confirmed else "NOT_YET_PUBLISHED"
        if q.role != "NORMATIVE_EFFECT":
            raise ValueError("P74_UNKNOWN_PROOF_ROLE")
        if a < first:
            return "NOT_YET_PUBLISHED"
        effective = d("2025-09-22")
        if t < effective:
            return "NOT_YET_EFFECTIVE"
        if a >= confirmed:
            return "CONFIRMED_EFFECT"
        if t > a:
            return "PROJECTED_CONDITIONAL"
        return "UNCONFIRMED_AS_OF"
    if q.branch == "IRS":
        if q.role == "HISTORICAL_PUBLICATION":
            return "HISTORICAL_SUPPORTED" if a >= d("2019-09-10") else "NOT_YET_PUBLISHED"
        if q.role == "NORMATIVE_EFFECT":
            return "PROPOSAL_NOT_EFFECTIVE_LAW"
        if q.role == "PROPOSAL_PENDING":
            return "PROPOSAL_WITHDRAWN" if a >= d("2025-07-02") else "PROPOSAL_PENDING_NOT_LAW"
        raise ValueError("P74_UNKNOWN_PROOF_ROLE")
    raise ValueError("P74_UNKNOWN_ECOLOGY")


def conventional_bitemporal_prov_rival(q: Question) -> str:
    """Semantically equivalent reference; same curated metadata and branch rules.

    This is a *constructed non-independent competitor*, NOT an actual separate
    SQL/PROV product implementation or an empirical head-to-head benchmark.
    A fully competent standard temporal+role model can reproduce all labels.
    """
    return typed_projection(q)


def publication_only_heuristic(q: Question) -> str:
    """Deliberately simple, non-competitive straw baseline for ablation only."""
    published = {"HEARING":"2024-09-20","FOOD":"2025-07-17","IRS":"2019-09-10"}[q.branch]
    if q.role == "CONFIRMATION_EXISTENCE":
        return "HISTORICAL_SUPPORTED" if d(q.known_as_of) >= d("2025-09-26") else "NOT_YET_PUBLISHED"
    if d(q.known_as_of) < d(published):
        return "NOT_YET_PUBLISHED"
    if q.role == "HISTORICAL_PUBLICATION":
        return "HISTORICAL_SUPPORTED"
    return "CONFIRMED_EFFECT" if q.role == "NORMATIVE_EFFECT" else "PROPOSAL_PENDING_NOT_LAW"


def validate_record_ledger() -> None:
    assert len(RECORDS) == 8
    assert len({r.document_id for r in RECORDS}) == len(RECORDS)
    ids={r.key for r in RECORDS}
    assert all((not r.target or r.target in ids) for r in RECORDS)
    assert {r.issuer for r in RECORDS} == {"FDA","IRS"}
    assert sum(r.action in {"CORRECTION","WITHDRAWAL","CONFIRMATION","PROPOSAL_WITHDRAWAL"} for r in RECORDS) == 4
    assert FROZEN_METADATA["food_confirmation"]["confirmed_effective"] < "2025-09-26"
    assert FROZEN_METADATA["hearing_withdrawal"]["withdrawal_effective"] < FROZEN_METADATA["hearing_original"]["effective_scheduled"]
    assert all(r.source.startswith("https://www.govinfo.gov/content/pkg/FR-") for r in RECORDS)


def reject(fn, expected: str):
    try:
        fn()
    except ValueError as ex:
        assert expected in str(ex), (expected, str(ex))
    else:
        raise AssertionError("P74_FALSE_ACCEPTANCE_" + expected)


def self_test() -> dict:
    validate_record_ledger()
    assert len(QUESTIONS) == len({q.id for q in QUESTIONS}) == 17
    assert {q.branch for q in QUESTIONS} == {"HEARING","FOOD","IRS"}
    assert {q.expected for q in QUESTIONS} >= {"HISTORICAL_SUPPORTED","CONFIRMED_EFFECT","WITHDRAWN_BEFORE_EFFECT","PROPOSAL_NOT_EFFECTIVE_LAW"}
    typed_correct = sum(typed_projection(q) == q.expected for q in QUESTIONS)
    convention_correct = sum(conventional_bitemporal_prov_rival(q) == q.expected for q in QUESTIONS)
    ablation_correct = sum(publication_only_heuristic(q) == q.expected for q in QUESTIONS)
    assert typed_correct == convention_correct == 17
    assert ablation_correct < typed_correct
    # The future confirmation cannot be leaked into an earlier observer's knowledge.
    assert typed_projection(QUESTIONS[8]) == "UNCONFIRMED_AS_OF"
    assert typed_projection(QUESTIONS[9]) == "CONFIRMED_EFFECT"
    # A revoked rule is still a historical documentary event, not an active amendment.
    assert typed_projection(QUESTIONS[3]) == "WITHDRAWN_BEFORE_EFFECT"
    assert typed_projection(QUESTIONS[4]) == "HISTORICAL_SUPPORTED"
    # Proposed documents never automatically became enacted laws.
    assert typed_projection(QUESTIONS[13]) == "PROPOSAL_NOT_EFFECTIVE_LAW"
    reject(lambda: typed_projection(Question("BAD","FOOD","CAUSAL_AUDIT_EFFECT","2025-09-27","2025-09-27","??")),
           "UNKNOWN_PROOF_ROLE")
    reject(lambda: typed_projection(Question("BAD","UNKNOWN","NORMATIVE_EFFECT","2025-09-27","2025-09-27","??")),
           "UNKNOWN_ECOLOGY")
    return {
       "stage":"EPISTEME_P74_P3_MULTI_DOCUMENT_DIAGNOSTIC",
       "verdict":"BOUNDED_DOCUMENTARY_DIAGNOSTIC_PASS_STRONG_RIVAL_TIES",
       "source_document_entries":len(RECORDS),
       "document_chains":3,
       "agencies":2,
       "author_derived_queries":len(QUESTIONS),
       "typed_projection_matches_author_gold":typed_correct,
       "conventional_bitemporal_PROV_rival_matches_author_gold":convention_correct,
       "simplistic_publication_only_matches_author_gold":ablation_correct,
       "strong_rival_independently_implemented":False,
       "gold_labels_blind_external":False,
       "historically_timestamped_original_pdf_bytes_obtained":False,
       "actual_audit_interventions":0,
       "actual_human_warrant_adjudications":0,
       "model_paid_calls":0,
       "novel_empirical_advantage":False,
       "generalization_to_independent_sources":"NOT_IDENTIFIED",
       "causal_intervention_effect":"NOT_IDENTIFIED"
    }


if __name__ == "__main__":
    print(json.dumps(self_test(),sort_keys=True,indent=2))
