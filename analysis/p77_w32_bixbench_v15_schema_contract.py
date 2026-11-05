"""W32: BixBench v1.5 dataset->CLI evaluator mode contract (synthetic fixtures).

Source inspection (2026-11-05):
- Hugging Face futurehouse/BixBench dataset viewer: eval_mode
- Future-House/BixBench grade_outputs.py: row.get("evaluation_mode", "llm_verifier")
Only a *hypothetical direct CSV flow* is tested; the official pipeline might
map columns elsewhere. No real benchmark questions, answers, or canary tokens
are included. A green test is NOT a verified biological inference or TLP effect.
"""
from collections.abc import Mapping

ALLOWED = frozenset({"llm_verifier", "str_verifier", "range_verifier"})


def direct_cli_mode(row: Mapping[str, str]) -> str:
    """Exact source default expression, not the grader itself."""
    return row.get("evaluation_mode", "llm_verifier")


def normalized_cli_fields(row: Mapping[str, str]) -> dict[str, str]:
    """Lossless explicit schema adapter; fails closed on ambiguity."""
    if "eval_mode" not in row:
        raise KeyError("Expected v1.5 dataset field eval_mode")
    mode = row["eval_mode"]
    if mode not in ALLOWED:
        raise ValueError(f"Unknown evaluation mode {mode!r}")
    if "evaluation_mode" in row and row["evaluation_mode"] != mode:
        raise ValueError("Contradictory eval_mode/evaluation_mode fields")
    return {"evaluation_mode": mode}


def self_test() -> None:
    synthetic = [
        {"id": "fixture_a", "eval_mode": "llm_verifier"},
        {"id": "fixture_b", "eval_mode": "str_verifier"},
        {"id": "fixture_c", "eval_mode": "range_verifier"},
    ]
    mismatches = [row["id"] for row in synthetic
                  if direct_cli_mode(row) != row["eval_mode"]]
    assert mismatches == ["fixture_b", "fixture_c"]
    assert all(
        direct_cli_mode(normalized_cli_fields(row)) == row["eval_mode"]
        for row in synthetic
    )
    for bad in [
        {"id": "missing"},
        {"id": "bad", "eval_mode": "unsupported"},
        {"eval_mode": "range_verifier", "evaluation_mode": "llm_verifier"},
    ]:
        try:
            normalized_cli_fields(bad)
        except (KeyError, ValueError):
            continue
        raise AssertionError("Unvalidated benchmark schema admitted")
    print("PASS: invented 3-mode cases; naive direct input mismatches in 2 modes")
    print("PASS: explicit alias adapter preserves all 3 modes")
    print("PASS: missing/invalid/contradictory mode aliases rejected")
    print("SCOPE: synthetic schema test; official pipeline not run; no performance result")


if __name__ == "__main__":
    self_test()
