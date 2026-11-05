"""W18: elementary, SYNTHETIC network-economics comparative statics.

Not a calibrated Farrell-Saloner / Liu structural model. Not empirical science.
"""
from dataclasses import dataclass
from math import exp

@dataclass(frozen=True)
class Regime:
    name: str
    rival_quality_advantage: float = 0.5
    initial_switch_cost: float = 0.2
    incumbent_network_advantage: float = 0.6
    switch_cost_relief_per_adapter: float = 0.6
    incumbent_compatibility_benefit_per_adapter: float = 0.0
    choice_temperature: float = 0.1

    def utility_difference(self, adapter: float) -> float:
        """Utility of migrating to R minus remaining on incumbent I.

        Fixed installed base and single prospective adopter; not a dynamic equilibrium.
        """
        assert 0.0 <= adapter <= 1.0
        return (self.rival_quality_advantage - self.initial_switch_cost
                - self.incumbent_network_advantage
                + adapter * (self.switch_cost_relief_per_adapter
                             - self.incumbent_compatibility_benefit_per_adapter))

    def migration_probability(self, adapter: float) -> float:
        z = self.utility_difference(adapter) / self.choice_temperature
        return 1.0 / (1.0 + exp(-z))


def test():
    weakening = Regime(name="migration-facilitating", incumbent_compatibility_benefit_per_adapter=0.0)
    reinforcing = Regime(name="incumbent-complementary", incumbent_compatibility_benefit_per_adapter=0.9)
    for regime in [weakening, reinforcing]:
        a, b = regime.migration_probability(0), regime.migration_probability(1)
        print(f"{regime.name}: delta0={regime.utility_difference(0):+.3f}, delta1={regime.utility_difference(1):+.3f}, Pmigrate0={a:.6f}, Pmigrate1={b:.6f}")
    assert weakening.migration_probability(1) > weakening.migration_probability(0)
    assert reinforcing.migration_probability(1) < reinforcing.migration_probability(0)
    assert weakening.switch_cost_relief_per_adapter > 0 and reinforcing.switch_cost_relief_per_adapter > 0
    # Feasible tests are fixed exogenously; this calculation cannot prove
    # a change in the physically/institutionally feasible set.
    print("PASS: sign reversal in single-agent choice under equal initial utility and switch-cost relief")
    print("LIMIT: choices are conditional on fixed installed base, no strategic equilibrium or field evidence")

if __name__ == '__main__':
    test()
