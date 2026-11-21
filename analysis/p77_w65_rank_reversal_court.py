"""W65: find strict sign reversals from a conditional parser comparison receipt.

Compares original-source BioSample vs each model output within one cohort,
query, and released heuristic-label dataset. Sign reversals are not causal,
statistical-significance results, or author manuscript ranking estimates.
"""
import json
import sys
from pathlib import Path

EXACT = "author_exact_tissue"
NORMALIZED = "alias_casefold_strip"


def sign(a, b, tolerance=1e-12):
    if abs(a - b) <= tolerance:
        return 0
    return 1 if a > b else -1


def audit(receipt):
    if not isinstance(receipt.get("results"), dict):
        raise ValueError("Missing conditional source results")
    comparisons = []
    for cancer, c in receipt["results"].items():
        for model, layers in c["models"].items():
            if "BioSample" not in layers:
                continue
            for layer in ("LLM", "LLM+CEDAR"):
                if layer not in layers:
                    continue
                for query, source_scores in layers["BioSample"].items():
                    if query not in layers[layer]:
                        raise ValueError("Model and BioSample queries diverge")
                    model_scores = layers[layer][query]
                    for metric in ("precision", "recall", "f1"):
                        a0, a1 = source_scores[EXACT][metric], model_scores[EXACT][metric]
                        b0, b1 = source_scores[NORMALIZED][metric], model_scores[NORMALIZED][metric]
                        before, after = sign(a1, a0), sign(b1, b0)
                        comparisons.append({
                            "cancer": cancer, "model": model, "layer": layer,
                            "query": query, "metric": metric,
                            "source_exact": a0, "model_exact": a1,
                            "source_normalized": b0, "model_normalized": b1,
                            "rank_exact": before, "rank_normalized": after,
                            "strict_reversal": before * after == -1,
                        })
    reversals = [r for r in comparisons if r["strict_reversal"]]
    return {
        "pairwise_metric_comparisons": len(comparisons),
        "strict_rank_reversals": len(reversals),
        "reversals": reversals,
        "qualification": "Row-position pairing; original labels are heuristic. No author production run, independent biological labels or causal effect.",
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: p77_w65_rank_reversal_court.py w65_parser_receipt.json")
    print(json.dumps(audit(json.loads(Path(sys.argv[1]).read_text())),
                     ensure_ascii=False, indent=2))
