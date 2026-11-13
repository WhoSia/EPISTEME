"""Recheck P77 W50 from published workbook values and printed paper statistics.

Run with Python 3. The recall rows are transcribed from Musen Lab's Zenodo v3
workbook, 'overall tissue'; each pair of strata rows is identified by matching
the values on the BioSample - GPT-4 and geo-gpt4 worksheets. See the W50 report
for source URLs, workbook labeling ambiguity, and the limits of these checks.
"""
from itertools import product
from math import exp, isclose
from statistics import mean


RECALL_ROWS = {
    "BioSample": [
        (0.042, 0.045, 0.724),
        (0.264755480607082, 0.106239460370994, 0.952782462057335),
        (0.170454545454545, 0.183441558441558, 0.99025974025974),
        (0.246753246753246, 0.246753246753246, 0.506493506493506),
        (0.0, 0.2, 0.95),
        (0.5, 0.484375, 0.78125),
    ],
    "GEO": [
        (0.0, 0.0, 0.435897435897435),
        (0.0942760942760942, 0.0, 0.646319569120287),
        (0.0, 0.122807017543859, 0.91578947368421),
        (0.0, 0.0, 0.0),
        (0.8, 0.0, 0.0),
        (0.0, 0.0, 0.642276422764227),
    ],
}
# Row order: ovary, liver, lung organ queries, then blood for the same strata.
# Column order: baseline, LLM+DD, LLM+CEDAR.


def f_upper_tail(f, denominator_df):
    """Survival probability for an F distribution with 2 numerator df."""
    return (1 + 2 * f / denominator_df) ** (-denominator_df / 2)


def repeated_measures(rows):
    """Balanced, three-condition one-way RM-ANOVA with row fixed effects."""
    columns = tuple(zip(*rows))
    method_means = tuple(map(mean, columns))
    grand_mean = mean(method_means)
    ss_method = len(rows) * sum((value - grand_mean) ** 2 for value in method_means)
    ss_error = sum(
        (value - mean(row) - method_means[j] + grand_mean) ** 2
        for row in rows
        for j, value in enumerate(row)
    )
    denominator_df = 2 * (len(rows) - 1)
    f = (ss_method / 2) / (ss_error / denominator_df)
    return f, f_upper_tail(f, denominator_df)


def friedman(rows):
    """Tie-corrected Friedman statistic and asymptotic chi-square p (2 df)."""
    blocks, methods = len(rows), len(rows[0])
    ranks = [
        [1 + sum(other < value for other in row) + (row.count(value) - 1) / 2
         for value in row]
        for row in rows
    ]
    rank_sums = tuple(map(sum, zip(*ranks)))
    tie_sum = sum(row.count(value) ** 3 - row.count(value)
                  for row in rows for value in set(row))
    statistic = 12 * sum(rank ** 2 for rank in rank_sums) / (
        blocks * methods * (methods + 1)
    ) - 3 * blocks * (methods + 1)
    correction = 1 - tie_sum / (blocks * methods * (methods ** 2 - 1))
    statistic /= correction
    return statistic, exp(-statistic / 2)


def cancer_blocks(rows):
    """Collapse the organ and blood queries within each cancer stratum."""
    return [tuple(map(mean, zip(organ, blood)))
            for organ, blood in zip(rows[:3], rows[3:])]


def sign_flip_p(differences):
    """Two-sided sensitivity calculation under block sign exchangeability."""
    observed = abs(sum(differences))
    permuted = [
        abs(sum(sign * difference for sign, difference in zip(signs, differences)))
        for signs in product((-1, 1), repeat=len(differences))
    ]
    return mean(value >= observed or isclose(value, observed, abs_tol=1e-14)
                for value in permuted)


def main():
    for name, rows in RECALL_ROWS.items():
        f, anova_p = repeated_measures(rows)
        q, friedman_p = friedman(rows)
        blocked = cancer_blocks(rows)
        blocked_f, blocked_p = repeated_measures(blocked)
        differences = [cedar - baseline for baseline, _, cedar in blocked]
        print(f"{name}: F(2,10)={f:.6f}, p={anova_p:.8f}; "
              f"Friedman Q={q:.6f}, asymptotic p={friedman_p:.8f}")
        print(f"  Cancer-stratum CEDAR minus baseline: {differences}; "
              f"F(2,4)={blocked_f:.6f}, p={blocked_p:.8f}; "
              f"two-sided sign-flip p={sign_flip_p(differences):.2f}")

    weighted = sum(n * rate for n, rate in ((421, 29.4), (116, 12.1),
                                             (56, 17.8), (41, 34.1))) / 634
    print(f"Long Table 2/3 header-count-weighted published rates: {weighted:.6f}%")
    print(f"Tail for the printed GEO F(2,10)=1.08: {f_upper_tail(1.08, 10):.8f}")


if __name__ == "__main__":
    main()
