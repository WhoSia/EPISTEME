"""EPISTEME P77 W22: finite, SYNTHETIC negative identification witness.

Not an empirical science experiment or a new theorem. Market adoption is
observationally equivalent in all scenarios; scientific test admissibility is not.
An available manual reference route defeats the apparent adapter-caused loss.
"""
from dataclasses import dataclass
from itertools import product

@dataclass(frozen=True)
class World:
    label: str
    ai_semantic_fidelity: bool
    ai_provenance_verified: bool
    trusted_manual_feasible: bool
    scientific_budget: int = 3
    manual_cost: int = 4
    adopter_count: int = 10
    adopted_challenger: int = 4
    public_numeric_output: tuple = (5, 8, 13)

    def market_observables(self):
        return (self.adopter_count, self.adopted_challenger, self.public_numeric_output)

    def ai_provides_admissible_test(self):
        return self.ai_semantic_fidelity and self.ai_provenance_verified

    def manual_provides_admissible_test(self):
        return self.trusted_manual_feasible and self.manual_cost <= self.scientific_budget

    def scientific_test_available(self):
        return self.ai_provides_admissible_test() or self.manual_provides_admissible_test()


def run():
    verified = World("verified conversion", True, True, False)
    silent_error = World("unverified conversion", True, False, False)
    manual_rescue = World("manual alternative in budget", True, False, True,
                          scientific_budget=5, manual_cost=4)
    common_obs = verified.market_observables()
    for w in [verified, silent_error, manual_rescue]:
        assert w.market_observables() == common_obs
    assert verified.scientific_test_available()
    assert not silent_error.scientific_test_available()
    assert manual_rescue.scientific_test_available()
    assert common_obs[:2] == (10, 4)
    print("PASS: identical 4/10 adoption + numeric output in 3 latent worlds")
    print("PASS: admissible test = 1, 0, 1; trusted affordable manual route rescues")
    all_worlds = [World(f"{f}-{p}-{m}-{b}", f, p, m, scientific_budget=b)
                  for f,p,m,b in product([False, True], [False, True], [False, True], [3, 5])]
    outcomes = {w.scientific_test_available() for w in all_worlds}
    assert len(all_worlds) == 16 and outcomes == {False, True}
    print("PASS: exhaustive 16-state sensitivity set has both Y=0 and Y=1 at same market observables")
    print("WARNING: purely synthetic; no real study, no estimated treatment effect, no novelty claim")


if __name__ == "__main__":
    run()
