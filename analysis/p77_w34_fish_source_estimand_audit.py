"""W34 source-pinned BLADE fish visit-rate vs population/measurement audit.

Run: python analysis/p77_w34_fish_source_estimand_audit.py original_fish_data.csv
For original data use the upstream path:
  behavioral-data/BLADE/blob/6118fa8d5007b91aa8c91c518182db82446a4547/
  blade_bench/datasets/fish/data.csv
This reports aggregated observational estimates; no AI translator or causal effects.
"""
import csv
import hashlib
import math
import random
import sys
from pathlib import Path

PINNED_GIT_BLOB = "a590e5b1a92029adc2db4915e48295ed60833430"
HEADER = ("fish_caught", "livebait", "camper", "persons", "child", "hours")


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load(path):
    raw = Path(path).read_bytes()
    assert git_blob(raw) == PINNED_GIT_BLOB, "Source differs from original Git blob"
    reader = csv.DictReader(raw.decode("utf8").splitlines())
    assert tuple(reader.fieldnames) == HEADER
    rows = [{k: float(row[k]) for k in HEADER} for row in reader]
    assert len(rows) == 250 and all(
        all(math.isfinite(v) for v in row.values())
        and row["hours"] > 0 and row["persons"] + row["child"] > 0
        and row["fish_caught"] >= 0 for row in rows
    )
    return rows


def estimates(rows):
    catches = math.fsum(r["fish_caught"] for r in rows)
    hours = math.fsum(r["hours"] for r in rows)
    personhours = math.fsum(
        r["hours"] * (r["persons"] + r["child"]) for r in rows
    )
    visit_rate = math.fsum(r["fish_caught"] / r["hours"] for r in rows) / len(rows)
    person_visit_rate = math.fsum(
        r["fish_caught"] / (r["hours"] * (r["persons"] + r["child"]))
        for r in rows
    ) / len(rows)
    return {
        "visits": len(rows), "total_fish": catches, "total_park_hours": hours,
        "total_person_park_hours": personhours,
        "pooled_fish_per_park_hour": catches / hours,
        "equal_visit_mean_fish_per_park_hour": visit_rate,
        "pooled_fish_per_person_park_hour": catches / personhours,
        "equal_visit_mean_fish_per_person_park_hour": person_visit_rate,
    }


def poisson_check(rows):
    rate = estimates(rows)["pooled_fish_per_park_hour"]
    dispersion = math.fsum(
        (r["fish_caught"] - rate * r["hours"]) ** 2 / (rate * r["hours"])
        for r in rows
    ) / (len(rows) - 1)
    expected_zeros = math.fsum(math.exp(-rate * r["hours"]) for r in rows)
    return {
        "observed_zero_fish": sum(r["fish_caught"] == 0 for r in rows),
        "expected_zero_fish_if_constant_rate_poisson": expected_zeros,
        "pearson_dispersion_if_constant_rate_poisson": dispersion,
    }


def quantile(samples, p):
    values = sorted(samples)
    pos = p * (len(values) - 1)
    index = int(pos)
    return values[index] + (pos - index) * (
        values[min(index + 1, len(values) - 1)] - values[index]
    )


def bootstrap(rows, draws=3000, seed=20261105):
    rng = random.Random(seed)
    pooled, visits, difference = [], [], []
    for _ in range(draws):
        sample = rng.choices(rows, k=len(rows))
        e = estimates(sample)
        x, y = e["pooled_fish_per_park_hour"], e["equal_visit_mean_fish_per_park_hour"]
        pooled.append(x)
        visits.append(y)
        difference.append(y - x)
    return {
        "seed": seed, "draws": draws,
        "pooled_percentile_95": [quantile(pooled, .025), quantile(pooled, .975)],
        "equal_visit_percentile_95": [quantile(visits, .025), quantile(visits, .975)],
        "difference_percentile_95": [quantile(difference, .025), quantile(difference, .975)],
        "scope": "illustrative iid-visit resampling, not validated population confidence coverage",
    }


def audit(rows):
    e = estimates(rows)
    assert e["visits"] == 250 and e["total_fish"] == 824
    assert math.isclose(e["total_park_hours"], 1381.495, abs_tol=1e-9)
    assert math.isclose(e["pooled_fish_per_park_hour"], .5964552893785353, abs_tol=1e-12)
    assert math.isclose(e["equal_visit_mean_fish_per_park_hour"], 1.1073814569241494, abs_tol=1e-12)
    print("SOURCE_COHORT", e)
    print("POISSON_DIAGNOSTIC", poisson_check(rows))
    print("SENSITIVITY", [
        {"min_park_hours": t, **estimates(subset)} for t in (0, .01, .1, .5, 1)
        if (subset := [r for r in rows if r["hours"] >= t])
    ])
    print("DESCRIPTIVE_RESAMPLING", bootstrap(rows))
    print("NO AI CONVERSION OR RESEARCH-COMMUNITY ADOPTION DATA; NO TLP EFFECT")


def selftest():
    a = [
        dict(fish_caught=1., hours=1., persons=1., child=0.),
        dict(fish_caught=3., hours=3., persons=1., child=1.),
    ]
    e = estimates(a)
    assert e["pooled_fish_per_park_hour"] == 1.0
    assert e["equal_visit_mean_fish_per_park_hour"] == 1.0
    assert math.isclose(e["pooled_fish_per_person_park_hour"], 4/7)
    assert math.isclose(e["equal_visit_mean_fish_per_person_park_hour"], .75)
    print("PASS synthetic 2-record formula selftest; not original source replay")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python p77_w34_fish_source_estimand_audit.py DATA.csv OR --selftest")
    if sys.argv[1] == "--selftest":
        selftest()
    else:
        audit(load(sys.argv[1]))
