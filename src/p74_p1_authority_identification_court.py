"""EPISTEME P74-P1: authority-time admissibility != counterfactual identification.

All witnesses and issuer identities in this module are SYNTHETIC / UNVERIFIED.
No real external certificates, institutions, human reviews, API or model calls.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
import hashlib
import json

from p74_p0_observational_equivalence import (
    SourceUnit, fixture, observed_trace, potential_world, average_effect
)


@dataclass(frozen=True)
class AuthorityWitness:
    source_id: str
    observed_sha256: str
    source_owner: str
    issuer: str
    collector: str
    source_role: str
    referent: str
    effective_from: str
    effective_until: str  # half-open [from, until)
    revoked_from: str | None
    signed_at: str
    synthetic_only: bool = True


@dataclass(frozen=True)
class CounterfactualBridge:
    source_id: str
    action: int
    asserted_outcome: int
    scope: str = "HYPOTHETICAL_CROSSWORLD_STRUCTURAL_ASSUMPTION"


def utc(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.utcoffset() is None:
        raise ValueError("P74_NAIVE_TIME_FORBIDDEN")
    return result.astimezone(timezone.utc)


def evidence_witnesses(rows: tuple[SourceUnit, ...]) -> tuple[AuthorityWitness, ...]:
    trace = observed_trace(rows, potential_world(rows, "positive"))
    records = []
    for row, observed in zip(rows, trace):
        records.append(AuthorityWitness(
            source_id=row.unit_id,
            observed_sha256=observed["source_snapshot_sha256"],
            source_owner="SYNTHETIC_SOURCE_OWNER",
            issuer="SYNTHETIC_SEPARATE_ISSUER",
            collector="SYNTHETIC_DISTINCT_COLLECTOR",
            source_role=row.source_role,
            referent="SYNTHETIC_REFERENT",
            effective_from="2026-09-01T00:00:00+00:00",
            effective_until="2026-11-01T00:00:00+00:00",
            revoked_from="2026-10-02T00:00:00+00:00"
                if row.unit_id == "artificial_0_0" else None,
            signed_at="2026-10-03T00:00:00+00:00",
        ))
    return tuple(records)


def validate_witnesses(
    rows: tuple[SourceUnit, ...],
    witnesses: tuple[AuthorityWitness, ...],
) -> dict[str, bool]:
    if len(witnesses) != len(rows) or len({w.source_id for w in witnesses}) != len(witnesses):
        raise ValueError("P74_AUTHORITY_WITNESS_CENSUS_OR_DUPLICATE")
    by_id = {w.source_id: w for w in witnesses}
    trace = {r["source_id"]: r for r in observed_trace(rows, potential_world(rows, "negative"))}
    if set(by_id) != set(trace):
        raise ValueError("P74_WITNESS_SOURCE_SET_MISMATCH")
    result = {}
    for row in rows:
        w = by_id[row.unit_id]
        capture = utc(row.observation_epoch)
        start, end, signed = utc(w.effective_from), utc(w.effective_until), utc(w.signed_at)
        if not start < end:
            raise ValueError("P74_INVALID_AUTHORITY_INTERVAL")
        if signed > capture:
            raise ValueError("P74_FUTURE_SIGNED_ATTESTATION")
        if not (start <= signed <= capture):
            raise ValueError("P74_ATTESTATION_BEFORE_EFFECTIVE_AUTHORITY")
        if len({w.source_owner, w.issuer, w.collector}) != 3:
            raise ValueError("P74_ATTESTATION_ACTOR_NOT_SEPARATE")
        if w.source_role != row.source_role or w.referent != "SYNTHETIC_REFERENT":
            raise ValueError("P74_PROOF_ROLE_OR_REFERENT_MISMATCH")
        if w.observed_sha256 != trace[row.unit_id]["source_snapshot_sha256"]:
            raise ValueError("P74_CERTIFIED_CONTENT_HASH_MISMATCH")
        if not w.synthetic_only:
            # A Boolean claim of independent certification cannot authenticate.
            raise ValueError("P74_FALSE_REAL_CERTIFICATE_PROMOTION")
        if w.revoked_from is not None:
            revocation = utc(w.revoked_from)
            if revocation < start:
                raise ValueError("P74_REVOCATION_BEFORE_AUTHORITY")
            result[row.unit_id] = start <= capture < min(end, revocation)
        else:
            result[row.unit_id] = start <= capture < end
    return result


def identification_set(
    rows: tuple[SourceUnit, ...],
    bridges: tuple[CounterfactualBridge, ...] = (),
    *,
    explicitly_assume_crossworld_bridge: bool = False,
) -> tuple[set[Fraction], int]:
    if bridges and not explicitly_assume_crossworld_bridge:
        raise ValueError("P74_NO_CAUSAL_BRIDGE_FROM_AUTHORITY_METADATA")
    admissible_ids = {row.unit_id: row for row in rows}
    constraints = {}
    for bridge in bridges:
        if (bridge.source_id not in admissible_ids
            or bridge.action not in (0, 1)
            or bridge.asserted_outcome not in (0, 1)
            or bridge.scope != "HYPOTHETICAL_CROSSWORLD_STRUCTURAL_ASSUMPTION"):
            raise ValueError("P74_INVALID_CROSSWORLD_BRIDGE")
        row = admissible_ids[bridge.source_id]
        if row.notice == bridge.action:
            raise ValueError("P74_OBSERVED_OUTCOME_NOT_MISSING_COUNTERFACTUAL")
        key = (bridge.source_id, bridge.action)
        if key in constraints:
            raise ValueError("P74_DUPLICATE_CROSSWORLD_CONSTRAINT")
        constraints[key] = bridge.asserted_outcome

    effects, count = set(), 0
    for unseen in product((0, 1), repeat=len(rows)):
        world = {}
        for row, missing in zip(rows, unseen):
            world[row.unit_id] = (
                (row.recorded_post_change, missing) if row.notice == 0
                else (missing, row.recorded_post_change)
            )
        if any(world[sid][action] != value for (sid, action), value in constraints.items()):
            continue
        effects.add(average_effect(world))
        count += 1
    if not effects:
        raise ValueError("P74_EMPTY_COUNTERFACTUAL_MODEL_CLASS")
    return effects, count


def assert_rejected(fn, marker):
    try:
        fn()
    except ValueError as err:
        assert marker in str(err), (marker, err)
    else:
        raise AssertionError("P74_FALSE_ACCEPTANCE_" + marker)


def self_test():
    rows = fixture()
    witnesses = evidence_witnesses(rows)
    authority = validate_witnesses(rows, witnesses)
    assert len(authority) == 8 and sum(authority.values()) == 7
    baseline, n_base = identification_set(rows)
    # Adding independently-themed authority metadata alone does not constrain
    # a potential outcome under another treatment assignment.
    _ = validate_witnesses(rows, witnesses)
    after_metadata, n_same = identification_set(rows)
    assert n_base == n_same == 256 and after_metadata == baseline
    assert (min(baseline), max(baseline)) == (Fraction(-1, 4), Fraction(3, 4))

    treated = [row for row in rows if row.notice == 1]
    bridges_two = tuple(CounterfactualBridge(row.unit_id, 0, 0) for row in treated[:2])
    bridges_all = tuple(CounterfactualBridge(row.unit_id, 0, 0) for row in treated)
    assert_rejected(lambda: identification_set(rows, bridges_two),
                    "NO_CAUSAL_BRIDGE_FROM_AUTHORITY_METADATA")
    weak, n_weak = identification_set(
        rows, bridges_two, explicitly_assume_crossworld_bridge=True)
    strong, n_strong = identification_set(
        rows, bridges_all, explicitly_assume_crossworld_bridge=True)
    assert (n_weak, n_strong) == (64, 16)
    assert (min(weak), max(weak)) == (Fraction(0), Fraction(3, 4))
    assert (min(strong), max(strong)) == (Fraction(1, 4), Fraction(3, 4))
    assert strong.issubset(weak) and weak.issubset(baseline)
    assert Fraction(0) in weak and Fraction(0) not in strong
    assert_rejected(lambda: identification_set(rows, bridges_all + bridges_all,
        explicitly_assume_crossworld_bridge=True), "DUPLICATE_CROSSWORLD_CONSTRAINT")

    first = witnesses[0]
    def altered(**kwargs):
        return (replace(first, **kwargs),) + witnesses[1:]
    assert_rejected(lambda: validate_witnesses(rows, altered(
        issuer=first.source_owner)), "ATTESTATION_ACTOR_NOT_SEPARATE")
    assert_rejected(lambda: validate_witnesses(rows, altered(
        signed_at="2026-10-04T00:00:00+00:00")), "FUTURE_SIGNED_ATTESTATION")
    assert_rejected(lambda: validate_witnesses(rows, altered(
        source_role="UNAUTHORIZED_PROOF_ROLE")), "PROOF_ROLE_OR_REFERENT_MISMATCH")
    assert_rejected(lambda: validate_witnesses(rows, altered(
        observed_sha256="0" * 64)), "CERTIFIED_CONTENT_HASH_MISMATCH")
    assert_rejected(lambda: validate_witnesses(rows, altered(
        effective_until="2026-08-01T00:00:00+00:00")), "INVALID_AUTHORITY_INTERVAL")
    assert_rejected(lambda: validate_witnesses(rows, altered(
        synthetic_only=False)), "FALSE_REAL_CERTIFICATE_PROMOTION")
    assert_rejected(lambda: validate_witnesses(rows, (first,) + witnesses),
                    "AUTHORITY_WITNESS_CENSUS_OR_DUPLICATE")

    return {
        "study": "EPISTEME_P74_P1_AUTHORITY_VS_CAUSAL_IDENTIFICATION",
        "verdict": "SYNTHETIC_SEPARATION_PASS_REAL_AUTHORITY_HOLD",
        "input_source_count": 8,
        "synthetic_authority_admissible_at_observation": sum(authority.values()),
        "synthetic_revoked_at_observation": 1,
        "metadata_only_ACE_bounds": [str(min(after_metadata)), str(max(after_metadata))],
        "metadata_only_models": n_same,
        "two_explicit_hypothetical_crossworld_assumptions_bounds":
            [str(min(weak)), str(max(weak))],
        "two_assumption_models": n_weak,
        "four_explicit_hypothetical_crossworld_assumptions_bounds":
            [str(min(strong)), str(max(strong))],
        "four_assumption_models": n_strong,
        "authority_time_admissibility_separate_from_causal_ACE": True,
        "warrant_validity_beyond_issuer_authority": "NOT_CERTIFIED",
        "counterfactual_bridges_empirically_justified": False,
        "independent_real_external_authentication_count": 0,
        "actual_field_interventions": 0,
        "human_adjudications": 0,
        "paid_model_calls": 0,
        "novel_theorem": False,
    }


if __name__ == "__main__":
    print(json.dumps(self_test(), ensure_ascii=False, indent=2, sort_keys=True))
