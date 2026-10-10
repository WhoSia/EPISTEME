"""P74-P2: source-record time, valid time, withdrawal and proof-role court.

Three *real published document identifiers and dates* are desk-checked against
Federal Register public records (original/correction/withdrawal). The mapping,
role judgments and all counterexample mutations are our reconstruction.
No downloaded official PDF hashes, independently timestamped capture, present
legal opinion, audit-induced causation, provider calls or human ratings.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
import json

DOCKET = "FDA-2024-N-3654"
ORIGINAL = "2024-21231"
CORRECTION = "2024-24100"
WITHDRAWAL = "2025-01145"

# This is human-transcribed metadata, not raw document bytes.
DOC_URLS = {
    ORIGINAL: "https://www.federalregister.gov/documents/2024/09/20/2024-21231/regulatory-hearing-before-the-food-and-drug-administration-general-provisions-amendments",
    CORRECTION: "https://www.govinfo.gov/content/pkg/FR-2024-10-18/pdf/2024-24100.pdf",
    WITHDRAWAL: "https://www.federalregister.gov/documents/2025/01/17/2025-01145/regulatory-hearing-before-the-food-and-drug-administration-general-provisions-amendments-withdrawal",
}


@dataclass(frozen=True)
class Event:
    doc: str
    kind: str
    publication: str
    docket: str
    source: str
    target_doc: str | None = None
    signed: str | None = None
    filed: str | None = None
    effective: str | None = None
    special_instruction_effective: str | None = None
    proof_role: str = "DOCUMENTARY_PUBLICATION_RECORD"
    source_verification: str = "PUBLIC_INDEX_AND_TEXT_DESK_REVIEW"
    # Publication date is observed; database commit/transaction timestamp is not.
    independently_verified_transaction_at: str | None = None


def events() -> tuple[Event, ...]:
    return (
        Event(ORIGINAL, "DIRECT_FINAL_RULE", "2024-09-20", DOCKET,
              DOC_URLS[ORIGINAL], effective="2025-02-03",
              # The special effective date was omitted, per correction.
              special_instruction_effective=None,
              proof_role="PROPOSED_FUTURE_NORMATIVE_EFFECT"),
        Event(CORRECTION, "CORRECTION", "2024-10-18", DOCKET,
              DOC_URLS[CORRECTION], target_doc=ORIGINAL,
              effective="2025-02-03",
              special_instruction_effective="2025-12-18",
              proof_role="CORRECTION_OF_EFFECTIVE_DATE"),
        Event(WITHDRAWAL, "WITHDRAWAL", "2025-01-17", DOCKET,
              DOC_URLS[WITHDRAWAL], target_doc=ORIGINAL,
              signed="2025-01-13", filed="2025-01-16",
              effective="2025-01-17",
              proof_role="WITHDRAWAL_OF_ORIGINAL_RULE"),
    )


def day(s: str) -> date:
    if not isinstance(s, str):
        raise ValueError("P74_DATE_REQUIRED")
    try:
        return date.fromisoformat(s)
    except ValueError as e:
        raise ValueError("P74_INVALID_DATE") from e


def validate(court: tuple[Event, ...]) -> None:
    if len(court) != 3 or {x.doc for x in court} != {ORIGINAL, CORRECTION, WITHDRAWAL}:
        raise ValueError("P74_SOURCE_DOCUMENT_CENSUS")
    indexed = {x.doc: x for x in court}
    for doc, event in indexed.items():
        if event.docket != DOCKET or event.source != DOC_URLS[doc]:
            raise ValueError("P74_SOURCE_DOCKET_OR_LOCATOR_DRIFT")
        if event.independently_verified_transaction_at is not None:
            raise ValueError("P74_UNVERIFIED_DB_TRANSACTION_TIME_PROMOTION")
        if event.source_verification != "PUBLIC_INDEX_AND_TEXT_DESK_REVIEW":
            raise ValueError("P74_FALSE_AUTHENTICATED_PDF_PROMOTION")
        if event.signed and day(event.signed) > day(event.publication):
            raise ValueError("P74_SIGNED_AFTER_PUBLICATION")
        if event.filed and day(event.filed) > day(event.publication):
            raise ValueError("P74_FILED_AFTER_PUBLICATION")
        if event.signed and event.filed and day(event.signed) > day(event.filed):
            raise ValueError("P74_SIGNED_AFTER_FILED")
    original, fix, retraction = (indexed[k] for k in (ORIGINAL, CORRECTION, WITHDRAWAL))
    if [original.kind, fix.kind, retraction.kind] != [
        "DIRECT_FINAL_RULE", "CORRECTION", "WITHDRAWAL"]:
        raise ValueError("P74_DOCUMENT_ACTION_MISMATCH")
    if (original.target_doc is not None or fix.target_doc != ORIGINAL
        or retraction.target_doc != ORIGINAL):
        raise ValueError("P74_RELATIONSHIP_NOT_DOCUMENT_GROUNDED")
    if not (day(original.publication) < day(fix.publication) <
            day(retraction.publication) == day(retraction.effective)):
        raise ValueError("P74_SOURCE_CHAIN_TEMPORAL_DISORDER")
    if not (day(original.publication) < day(retraction.effective)
            < day(original.effective)):
        raise ValueError("P74_WITHDRAWN_BEFORE_PLANNED_EFFECT_GUARD")
    if (original.special_instruction_effective is not None or
        fix.special_instruction_effective != "2025-12-18" or
        fix.effective != original.effective):
        raise ValueError("P74_UNGROUNDED_SPECIAL_DATE")
    if (original.proof_role != "PROPOSED_FUTURE_NORMATIVE_EFFECT" or
        fix.proof_role != "CORRECTION_OF_EFFECTIVE_DATE" or
        retraction.proof_role != "WITHDRAWAL_OF_ORIGINAL_RULE"):
        raise ValueError("P74_WRONG_SOURCE_PROOF_ROLE")


def known_at(court: tuple[Event, ...], record_date: str) -> tuple[Event, ...]:
    validate(court)
    return tuple(x for x in sorted(court, key=lambda y: y.publication)
                 if day(x.publication) <= day(record_date))


def rule_state(court: tuple[Event, ...], *, target_date: str,
               record_date: str, scope: str = "MAIN") -> str:
    """A document-level retrospective/conditional status, NOT legal advice.

    record_date is public publication knowledge cutoff, NOT database tx time.
    target_date is the sought calendar time for the rule's *planned* effect.
    """
    if scope not in ("MAIN", "SPECIAL_INSTRUCTION_3"):
        raise ValueError("P74_UNKNOWN_PROOF_SCOPE")
    visible = known_at(court, record_date)
    if not visible:
        return "NO_PUBLIC_DOCUMENT_AS_OF_RECORD_DATE"
    original = next(x for x in visible if x.kind == "DIRECT_FINAL_RULE")
    withdrawal = next((x for x in visible if x.kind == "WITHDRAWAL"), None)
    corrected = next((x for x in visible if x.kind == "CORRECTION"), None)
    target = day(target_date)
    if withdrawal and day(withdrawal.effective) <= target:
        return "WITHDRAWN_BEFORE_ORIGINAL_EFFECTIVE_DATE"
    effective = (corrected.special_instruction_effective if corrected else
                 original.special_instruction_effective) if scope == "SPECIAL_INSTRUCTION_3" else original.effective
    if effective is None:
        return "SPECIAL_EFFECTIVE_DATE_UNSPECIFIED_AT_THIS_RECORD_DATE"
    # A past as-of record cannot certify a future legal effectiveness.
    if target > day(record_date):
        return ("PROJECTED_EFFECTIVE_CONDITIONAL_ON_NO_FUTURE_WITHDRAWAL"
                if target >= day(effective) else "SCHEDULED_NOT_YET_EFFECTIVE")
    if target < day(effective):
        return "PUBLISHED_BUT_NOT_YET_EFFECTIVE"
    return "EFFECTIVE_ACCORDING_TO_RECORDED_DOCUMENTS"


def proof_role(court: tuple[Event, ...], *, doc: str, role: str,
               target_date: str, record_date: str) -> str:
    indexed = {x.doc: x for x in known_at(court, record_date)}
    if doc not in indexed:
        return "DOCUMENT_UNAVAILABLE_AS_OF_RECORD_DATE"
    if role == "HISTORICAL_PUBLICATION":
        return "DOCUMENTARY_EVENT_SUPPORTED"
    if role == "CURRENT_ENFORCEABLE_AMENDMENT":
        if doc != ORIGINAL:
            return "CORRECTION_OR_WITHDRAWAL_IS_NOT_ORIGINAL_AMENDMENT"
        return rule_state(court, target_date=target_date, record_date=record_date)
    return "ROLE_NOT_ADJUDICATED"


def test_rejection(fn, token):
    try:
        fn()
    except ValueError as exc:
        assert token in str(exc), (token, str(exc))
    else:
        raise AssertionError("P74_FAILED_TO_REJECT_" + token)


def self_test() -> dict:
    court = events()
    validate(court)
    assert [x.doc for x in known_at(court, "2024-09-30")] == [ORIGINAL]
    assert [x.doc for x in known_at(court, "2024-11-01")] == [ORIGINAL, CORRECTION]
    assert len(known_at(court, "2025-01-20")) == 3
    pre = rule_state(court, target_date="2025-02-04",
                     record_date="2024-11-01")
    post = rule_state(court, target_date="2025-02-04",
                      record_date="2025-01-20")
    assert pre == "PROJECTED_EFFECTIVE_CONDITIONAL_ON_NO_FUTURE_WITHDRAWAL"
    assert post == "WITHDRAWN_BEFORE_ORIGINAL_EFFECTIVE_DATE"
    assert rule_state(court, target_date="2025-02-04", record_date="2024-09-30",
                      scope="SPECIAL_INSTRUCTION_3") == "SPECIAL_EFFECTIVE_DATE_UNSPECIFIED_AT_THIS_RECORD_DATE"
    assert rule_state(court, target_date="2025-02-04", record_date="2024-11-01",
                      scope="SPECIAL_INSTRUCTION_3") == "SCHEDULED_NOT_YET_EFFECTIVE"
    assert proof_role(court, doc=ORIGINAL, role="HISTORICAL_PUBLICATION",
                      target_date="2026-01-01", record_date="2026-01-01") == "DOCUMENTARY_EVENT_SUPPORTED"
    assert proof_role(court, doc=ORIGINAL, role="CURRENT_ENFORCEABLE_AMENDMENT",
                      target_date="2026-01-01", record_date="2026-01-01") == post
    assert proof_role(court, doc=CORRECTION, role="CURRENT_ENFORCEABLE_AMENDMENT",
                      target_date="2026-01-01", record_date="2026-01-01") == "CORRECTION_OR_WITHDRAWAL_IS_NOT_ORIGINAL_AMENDMENT"
    assert proof_role(court, doc=WITHDRAWAL, role="HISTORICAL_PUBLICATION",
                      target_date="2026-01-01", record_date="2024-11-01") == "DOCUMENT_UNAVAILABLE_AS_OF_RECORD_DATE"

    orig, fix, withdrawn = court
    test_rejection(lambda: validate((replace(orig, docket="FAKE"), fix, withdrawn)),
                   "SOURCE_DOCKET_OR_LOCATOR_DRIFT")
    test_rejection(lambda: validate((orig, replace(fix, publication="2024-09-01"), withdrawn)),
                   "SOURCE_CHAIN_TEMPORAL_DISORDER")
    test_rejection(lambda: validate((orig, fix, replace(withdrawn,
              signed="2025-01-20"))), "SIGNED_AFTER_PUBLICATION")
    test_rejection(lambda: validate((orig, replace(fix,
              special_instruction_effective="2025-02-03"), withdrawn)),
                   "UNGROUNDED_SPECIAL_DATE")
    test_rejection(lambda: validate((orig, fix, replace(withdrawn,
              source_verification="OFFICIAL_PDF_SHA_VERIFIED"))),
                   "FALSE_AUTHENTICATED_PDF_PROMOTION")
    test_rejection(lambda: validate((orig, replace(fix,
              proof_role="CURRENT_ENFORCEABLE_AMENDMENT"), withdrawn)),
                   "WRONG_SOURCE_PROOF_ROLE")
    test_rejection(lambda: validate((replace(orig,
              independently_verified_transaction_at="2024-09-20"), fix, withdrawn)),
                   "UNVERIFIED_DB_TRANSACTION_TIME_PROMOTION")
    test_rejection(lambda: rule_state(court, target_date="2025-02-04",
              record_date="2025-01-20", scope="UNKNOWN"),
                   "UNKNOWN_PROOF_SCOPE")

    return {
        "stage": "EPISTEME_P74_P2_REAL_PUBLIC_DOCUMENT_METADATA_DESK_COURT",
        "status": "DOCUMENTARY_TIMELINE_AND_SYNTHETIC_NEGATIVE_TEST_PASS",
        "docket": DOCKET,
        "actual_original_documents": [e.doc for e in court],
        "publication_dates": {e.doc:e.publication for e in court},
        "withdrawal_signed_file_pub": [
            withdrawn.signed, withdrawn.filed, withdrawn.publication],
        "original_general_effective_was_scheduled": orig.effective,
        "corrected_special_instruction_effective_was_scheduled":
            fix.special_instruction_effective,
        "earlier_projection": pre,
        "retrospective_outcome": post,
        "historical_event_evidence_survives_withdrawal": True,
        "normative_effectiveness_not_equivalent_to_publication": True,
        "record_time_is_publication_date_NOT_verified_database_transaction_time": True,
        "historical_official_pdf_byte_hashes": "NOT_OBTAINED",
        "original_valid_time_adjudication": "DOCUMENTARY_ONLY",
        "actual_audit_notice_effect": "NOT_IDENTIFIED",
        "legal_authority_of_any_current_regulation": "NOT_ADJUDICATED",
        "human_semantic_review": 0,
        "paid_model_calls": 0,
        "novel_theorem": False
    }


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2, ensure_ascii=False, sort_keys=True))
