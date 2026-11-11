"""EPISTEME P77 W47: information-theoretic discriminability negative control.

SYNTHETIC binary hypotheses, identical prior and a hypothesis-independent
conversion channel. Uses standard total variation/data-processing inequality.
No scientific image, true physical measurement, BIA converter or new theorem.
"""
from fractions import Fraction as F
from itertools import product

H0=(F(3,4),F(1,4))
H1=(F(1,4),F(3,4))

def transform(p,k):
    assert all(sum(row)==1 and all(0<=v<=1 for v in row) for row in k)
    return tuple(sum(p[x]*k[x][y] for x in range(len(p))) for y in range(len(k[0])))

def tv(a,b):
    return sum(abs(x-y) for x,y in zip(a,b))/2

def bayes_error(a,b):
    return (1-tv(a,b))/2

def main():
    maps=[
      ("identity",((F(1),F(0)),(F(0),F(1))),F(1,2)),
      ("invertible",((F(0),F(1)),(F(1),F(0))),F(1,2)),
      ("noisy",((F(4,5),F(1,5)),(F(1,5),F(4,5))),F(3,10)),
      ("constant",((F(1),F(0)),(F(1),F(0))),F(0))
    ]
    assert tv(H0,H1)==F(1,2)
    for name,k,expected in maps:
        p,q=transform(H0,k),transform(H1,k)
        assert tv(p,q)==expected
        assert tv(p,q)<=tv(H0,H1)
        print(name, "TV",str(tv(p,q)),"Bayes_equal_prior_error",str(bayes_error(p,q)))
    for a,b in product(range(5),repeat=2):
        k=((F(a,4),1-F(a,4)),(F(b,4),1-F(b,4)))
        assert tv(transform(H0,k),transform(H1,k))<=tv(H0,H1)
    assert min(bayes_error(H0,H1),bayes_error(transform(H0,maps[-1][1]),
             transform(H1,maps[-1][1])))==F(1,4)
    print("PASS all 25 binary stochastic channels on quarter grid: TV nonincrease")
    print("PASS if raw original remains valid and available, optional lossy representation does not force loss of best achievable test")
    print("LIMIT standard information theory, synthetic hypotheses, no AI or scientific-community effects")

if __name__=="__main__":
    main()
