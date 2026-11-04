"""P77: illustrative structural-identifiability court for solar neutrino fluxes.
DO NOT treat this toy linear response as SNO statistical analysis or a discovery.
Primary studies: H.H. Chen PRL 55, 1534 (1985); SNO PRL 87, 071301 (2001);
SNO PRL 89, 011301 (2002).
"""
from __future__ import annotations
import json
import numpy as np

def design_matrices(r: float = 1/6.5) -> dict[str, np.ndarray]:
    if not (0 < r < 1):
        raise ValueError("effective elastic-scattering ratio must be in (0, 1)")
    return {
        "CC_only": np.array([[1., 0.]]),
        "CC_plus_ES": np.array([[1., 0.], [1., r]]),
        "CC_plus_NC": np.array([[1., 0.], [1., 1.]]),
    }

def diagnose(a: np.ndarray) -> dict:
    rank = int(np.linalg.matrix_rank(a))
    return {
        "rank": rank,
        "identifies_two_active_flux_components": rank == 2,
        "singular_values": np.linalg.svd(a, compute_uv=False).tolist(),
        "condition_number_2": (float(np.linalg.cond(a)) if a.shape == (2, 2) else None),
    }

def main() -> None:
    r = 1/6.5  # rough illustrative ES flavor response; not an exact energy-folded detector calibration
    results = {name: diagnose(a) for name, a in design_matrices(r).items()}
    assert results["CC_only"]["rank"] == 1
    assert results["CC_plus_ES"]["rank"] == 2
    assert results["CC_plus_NC"]["rank"] == 2
    assert results["CC_plus_ES"]["condition_number_2"] > results["CC_plus_NC"]["condition_number_2"]
    for q in (1/7, 1/6, 0.1, 0.3):
        assert int(np.linalg.matrix_rank(design_matrices(q)["CC_plus_ES"])) == 2
    print(json.dumps({
        "assumed_ES_ratio": r,
        "designs": results,
        "warning": "No covariance, background, threshold, energy shape, shared systematics, or source-model assumptions. No inferential p-value or historical counterfactual inferred."
    }, indent=2))

if __name__ == "__main__":
    main()
