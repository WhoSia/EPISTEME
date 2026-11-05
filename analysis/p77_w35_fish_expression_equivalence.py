"""W35 source-grounded BLADE annotation expression-equivalence diagnostic.

Pinned dataset via W34 auditor; compare two ORIGINAL annotated expressions:
  fish / (hours * (persons + child))
  (fish / hours) / (persons + child)
No science oracle, AI translator, or community adoption result is inferred.
"""
from pathlib import Path
import math
import sys

from p77_w34_fish_source_estimand_audit import load


def equivalence(rows):
    n_float_unequal = 0
    maximum_difference = 0.0
    for r in rows:
        group_size = r["persons"] + r["child"]
        expr_a = r["fish_caught"] / (r["hours"] * group_size)
        expr_b = (r["fish_caught"] / r["hours"]) / group_size
        n_float_unequal += (expr_a != expr_b)
        maximum_difference = max(maximum_difference, abs(expr_a - expr_b))
        assert math.isclose(expr_a, expr_b, rel_tol=0, abs_tol=1e-12)
    return {"rows": len(rows), "float_inequality_count": n_float_unequal,
            "maximum_abs_diff": maximum_difference,
            "numerical_equivalence_at_abs_1e_12": True,
            "limit": "Equivalence of numerical expressions only, not causal scientific validity"}


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        print(equivalence([{"fish_caught": 7.0, "hours": .125,
                            "persons": 3.0, "child": 2.0}]))
        print("PASS: synthetic expression selftest")
    elif len(sys.argv) == 2:
        print(equivalence(load(Path(sys.argv[1]))))
    else:
        raise SystemExit("Usage: python p77_w35_fish_expression_equivalence.py --selftest | SOURCE.csv")
