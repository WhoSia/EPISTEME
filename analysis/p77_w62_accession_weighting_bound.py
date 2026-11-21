"""W62: *counterfactual weighting-only* bound for repeated accession rows.

For a bounded, accession-level score f(accession) in [0,1] that is the same
for all repeated rows of that accession, the maximum absolute difference between
the row-weighted and unique-accession unweighted means equals total variation
distance of their empirical accession weight vectors.
This is NOT a bound on precision/F1 or the authors' actual data with conflicting
row-level predictions. See W62 research judgment before interpretation.
"""
from collections import Counter


def bound(accessions):
    if not accessions or any(not isinstance(x, str) or not x for x in accessions):
        raise ValueError("Accessions must be nonempty strings")
    counts = Counter(accessions)
    n, unique = len(accessions), len(counts)
    tv = 0.5 * sum(abs(count / n - 1 / unique) for count in counts.values())
    max_leverage = max(counts.values()) * unique / n
    return {
        "row_count": n,
        "distinct_accession_count": unique,
        "total_variation_weight_shift": tv,
        "upper_bound_mean_score_difference_percentage_points": 100 * tv,
        "maximum_accession_row_weight_ratio_to_unique_weight": max_leverage,
        "assumptions": [
            "bounded score in [0,1]",
            "one fixed score for every accession",
            "no cross-accession sample dependence",
            "the same fixed set of accession IDs in row and unique analyses",
        ],
        "exclusions": [
            "not an estimate of real evaluation bias",
            "not a general bound on precision, recall or F1 ratios",
            "not applicable unchanged to disagreements between duplicate predictions",
            "not evidence of biological or institutional causal effects",
        ],
    }
