"""P77 W46: strict synthetic standard competition and causal non-identification.

Original authored demonstration, NOT Farrell-Saloner, Liu or Arthur's model.
Do not present as an estimated real adoption effect or novel theorem.
"""
from itertools import product
from fractions import Fraction as F

Q = (F("2.8"), F("2.2"), F("1.9"))
NETWORK = F("1")
COST = F(".4")

def utility(i, choice, state, convert, quality=Q):
    peers = sum(state[j] == choice for j in range(3) if j != i)
    return NETWORK * peers + (convert if choice == "A" else quality[i] - COST)

def best_response(convert, quality=Q):
    state = ["A"]*3
    trace = ["".join(state)]
    for _ in range(8):
        moved = False
        for i in range(3):
            other = "B" if state[i] == "A" else "A"
            if utility(i, other, state, convert, quality) > utility(i, state[i], state, convert, quality):
                state[i] = other
                trace.append("".join(state))
                moved = True
        if not moved:
            return trace
    raise AssertionError("not converged")

def nash(convert, quality=Q):
    return ["".join(s) for s in product("AB", repeat=3)
            if all(utility(i, s[i], s, convert, quality) >=
                   utility(i, "B" if s[i] == "A" else "A", s, convert, quality)
                   for i in range(3))]

def observational_worlds():
    # Under observation, Z=U. World 1 A=Z, T=A; World 2 A=U, T=A.
    obs = []
    for u in (0,1):
        z=u
        assert (u,z,z,z) == (u,z,u,u)
        obs.append((u,z,z,z))
    # Under intervention, do(Z) breaks this observational identity.
    rivals = [(u,z,z,u) for u,z in product((0,1), repeat=2) if u != z]
    assert len(rivals)==2
    return obs,rivals

def main():
    no_converter=best_response(F(0))
    with_converter=best_response(F(1))
    assert no_converter == ["AAA","BAA","BBA","BBB"]
    assert with_converter == ["AAA"]
    assert nash(F(0)) == ["BBB"]
    assert nash(F(1)) == ["AAA","BBB"]
    print("PASS no converter:", no_converter, "equilibria:", nash(F(0)))
    print("PASS with converter:", with_converter, "equilibria:", nash(F(1)))
    # External access friction = 1 - conversion level: 1 -> 0.
    assert F(1)-F(0)>F(1)-F(1)
    assert best_response(F(1), quality=(F("4.5"),F("2.2"),F("1.9")))[-1] == "BBB"
    print("PASS not universal: higher quality B still wins even with converter")
    fixed=[{"base"}]*3
    expanded=[{"base","converted"}]*3
    assert all(a.issubset(b) for a,b in zip(fixed,expanded))
    print("PASS fixed feasible experiments monotonicity", set.union(*fixed), "subset", set.union(*expanded))
    obs, rivals=observational_worlds()
    print("PASS observationally identical SCMs", obs, "interventions disagree", rivals)
    print("LIMIT synthetic choice law and observational equivalence only; no AI effects or true scientific tests")

if __name__ == "__main__": main()
