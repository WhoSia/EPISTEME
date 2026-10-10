"""EPISTEME P74-P0: synthetic observational equivalence vs causal effect.

Finite artificial population only. Classical missing-potential-outcome example.
No real sources, audit interventions, warrant certificates, people or model calls.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import hashlib
import json


@dataclass(frozen=True)
class SourceUnit:
    unit_id: str
    notice: int
    recorded_post_change: int
    pre_history: tuple[int, int] = (0, 0)
    source_role: str = "SYNTHETIC_WARRANT_SOURCE"
    authority_epoch: str = "2026-09-01T00:00:00+00:00"
    observation_epoch: str = "2026-10-03T00:00:00+00:00"


def fixture() -> tuple[SourceUnit, ...]:
    # Unrandomized notice; observed post rates: control 1/4, notice 3/4.
    return tuple(
        SourceUnit(f"artificial_{arm}_{j}", arm, outcome)
        for arm, outcomes in ((0, (1, 0, 0, 0)), (1, (1, 1, 1, 0)))
        for j, outcome in enumerate(outcomes)
    )


def potential_world(rows: tuple[SourceUnit, ...], kind: str):
    if kind not in ("positive", "negative"):
        raise ValueError("P74_UNKNOWN_WORLD")
    world = {}
    for row in rows:
        # Consistency holds; only the unseen counterfactual differs.
        if row.notice == 0:
            y0, y1 = row.recorded_post_change, int(kind == "positive")
        else:
            y0, y1 = int(kind == "negative"), row.recorded_post_change
        world[row.unit_id] = (y0, y1)
    return world


def observed_trace(rows: tuple[SourceUnit, ...], world: dict):
    trace = []
    for row in rows:
        y0, y1 = world[row.unit_id]
        actual = (y0, y1)[row.notice]
        assert actual == row.recorded_post_change
        trace.append({
            "source_id": row.unit_id,
            "notice_exposure": row.notice,
            "pre_history": list(row.pre_history),
            "observed_post_source_change": actual,
            "source_role": row.source_role,
            "authority_epoch": row.authority_epoch,
            "observation_epoch": row.observation_epoch,
            "source_snapshot_sha256": hashlib.sha256(
                (row.unit_id + ":" + str(actual)).encode()
            ).hexdigest(),
        })
    return trace


def average_effect(world: dict) -> Fraction:
    return sum((pair[1] - pair[0] for pair in world.values()), 0) / Fraction(len(world))


def observed_did(rows: tuple[SourceUnit, ...]) -> Fraction:
    means = {}
    for arm in (0, 1):
        group = [r for r in rows if r.notice == arm]
        means[arm] = Fraction(
            sum(r.recorded_post_change - r.pre_history[-1] for r in group),
            len(group)
        )
    return means[1] - means[0]


def sharp_completion_set(rows: tuple[SourceUnit, ...]) -> set[Fraction]:
    # 2^8 completions, each free missing potential binary outcome.
    effects = set()
    for unseen in product((0, 1), repeat=len(rows)):
        model = {}
        for row, missing in zip(rows, unseen):
            model[row.unit_id] = (
                (row.recorded_post_change, missing)
                if row.notice == 0 else (missing, row.recorded_post_change)
            )
        effects.add(average_effect(model))
    return effects


def self_test():
    rows = fixture()
    plus = potential_world(rows, "positive")
    minus = potential_world(rows, "negative")
    observed_plus = observed_trace(rows, plus)
    observed_minus = observed_trace(rows, minus)
    assert observed_plus == observed_minus
    assert len(observed_plus) == len({r["source_id"] for r in observed_plus}) == 8
    assert all(r["pre_history"] == [0, 0] for r in observed_plus)
    did = observed_did(rows)
    assert did == Fraction(1, 2)
    positive_ace = average_effect(plus)
    negative_ace = average_effect(minus)
    assert positive_ace == Fraction(3, 4)
    assert negative_ace == Fraction(-1, 4)
    feasible = sharp_completion_set(rows)
    assert (min(feasible), max(feasible)) == (negative_ace, positive_ace)
    assert Fraction(0) in feasible and len(feasible) == 9
    assert did != positive_ace and did != negative_ace
    return {
        "study": "EPISTEME_P74_P0_OBSERVATIONAL_EQUIVALENCE",
        "status": "SYNTHETIC_NONIDENTIFICATION_PASS",
        "units": len(rows),
        "pre_periods": 2,
        "observed_traces_identical": True,
        "observed_did": str(did),
        "positive_world_finite_population_ace": str(positive_ace),
        "negative_world_finite_population_ace": str(negative_ace),
        "sharp_unrestricted_binary_ace_bounds": [str(min(feasible)), str(max(feasible))],
        "feasible_finite_population_ace_values": len(feasible),
        "randomization": "NOT_ASSUMED",
        "parallel_counterfactual_trends": "NOT_ASSUMED",
        "no_interference": "ASSUMED_FOR_THIS_COUNTEREXAMPLE_ONLY",
        "audit_notice_not_same_as_audit_collection": True,
        "external_authority_certificates": 0,
        "actual_field_units": 0,
        "human_adjudications": 0,
        "paid_model_calls": 0,
        "actual_audit_effect": "NOT_IDENTIFIED",
        "epistemic_warrant_validity": "NOT_CERTIFIED",
        "novel_theorem": False,
    }


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2, sort_keys=True))
