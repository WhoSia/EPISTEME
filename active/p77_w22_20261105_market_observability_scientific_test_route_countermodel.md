# EPISTEME-P77 W22 — Market-Observability Countermodel and Scientific-Test Route Control

**Date:** 2026-11-05 KST  
**Governance:** [P77 binding strategy](../STRATEGY_P77_CURRENT.md) · [official Notion](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53)  
**Status:** P77 ACTIVE / P78 HOLD / PAPER HOLD / theory novelty NOT CERTIFIED  
**Precedent:** [W21 authentic 89×464 CRI table audit](p77_w21_20261105_real_cri_team_csv_grain_and_positivity_court.md).  
**Download aid:** [W22 official source acquisition and permissions guide](p77_w22_20261105_cri_issp_acquisition_guide.md).

## 1. Research return to founding question

The founding TLP asks whether AI-mediated adapters can reduce personal switching friction but change community standard lock-in, and whether this changes **which distinct scientific hypotheses can be genuinely tested**, not merely market share or result values. W15–W21 already found fatal antecedents to pure converter-network effects (Farrell–Saloner, Arthur, Liu, Heinrich, Rosero), agent-layer lock-in (Marro–Torr), scientific data/method portability (Bakeev, Janssen, NCSA, Pritchard–Wicenec), and causal-evidence disagreement (Reijula–Blanco Sequeiros, Blanco Sequeiros, Breznau). **Do not rename an elementary three-layer model as new theory.**

## 2. A synthetic 16-world intervention-adjacent *negative* witness (actually executed)

Committed source: [analysis/p77_w22_market_observation_vs_scientific_test_countermodel.py](../analysis/p77_w22_market_observation_vs_scientific_test_countermodel.py).

**Observables held constant:** an incumbent/challenger market with 10 adopters, 4 recorded as using the challenger, and an identical public numeric output `(5,8,13)`. An unobserved scientific-test validity channel depends on (i) adapter semantic fidelity, (ii) adapter provenance validation, (iii) whether a **trusted non-AI manual route** is feasible at the relevant independent scientific workflow budget.

Define `T_A = semantic_fidelity AND provenance_verified`; `T_M = trusted_manual AND (manual_cost <= scientific_budget)`; `Y = T_A OR T_M`. `Y` is a **stipulated synthetic Boolean marker for the existence of one admissible discriminating route**. In actual science, fidelity, institutional acceptance, experimental admissibility and evidence warrant are much richer and cannot be reduced without independent justification to these Booleans.

Under the same observable market and exact same published numerical output:
- World A: semantic fidelity and provenance validation both succeed; `Y=1`.
- World B: semantic fidelity succeeds but provenance validation does not, no affordable trusted manual route; `Y=0`.
- World C: provenance validation of the adapter fails, but an independent trusted manual comparator is feasible under a larger science-specific budget; `Y=1`.

**Executed local Python output** (not just authored):
```
PASS: identical 4/10 adoption + numeric output in 3 latent worlds
PASS: admissible test = 1, 0, 1; trusted affordable manual route rescues
PASS: exhaustive 16-state sensitivity set has both Y=0 and Y=1 at same market observables
WARNING: purely synthetic; no real study, no estimated treatment effect, no novelty claim
```
Enumerated 2×2×2×2=16 Boolean/budget states: Y has both 0 and 1 although public market observables stay fixed.

**Mathematical reading:** With `O=(adoption,numeric_output)`, there exist `w_1,w_2` with `O(w_1)=O(w_2)` but `Y(w_1) != Y(w_2)`. Therefore Y is **not an identified function of O alone** on this constructed set. This is a *standard non-injectivity/countermodel*, not a novel theorem. The choice of Y is stipulated; it is not a scientifically measured fact or empirical causal effect.

**Important matched-budget caveat:** Worlds B and C deliberately vary the independent science-testing budget to exhibit the *manual route rescue condition*; hence their difference is **NOT** an equal-budget estimator of an AI adapter effect. For an equal-budget comparison, fix the science budget and manipulate only one adapter property or the availability of the same-cost verified method. If the trusted manual alternative was already within budget in all relevant historical configurations, the alleged converter-imposed loss is false. This is an adversarial negative control, not a convenient handwaving objection.

## 3. Distinguish five targets, not one metric

1. **Direct translation/switching cost**, with semantic and validation effort priced.
2. **Individual migration choice** (W18): a payoff response not equivalent to adoption equilibrium.
3. **Collective equilibrium standard allocation**: requires interactions and converter ownership/provision, already studied in economics.
4. **Feasible route to an actual H0/H1 discriminating test**: independent source/algorithm/instrument path and alternative routes, cost, failure/reliability.
5. **Accepted evidence/warrant**: historical validity criteria and provenance uncertainty, already treated in HPS/metadata literature.

A causal claim chaining 1→2→3→4→5 requires **measuring or intervening on each distinct link** and controlling shared alternative explanations. Even a reliable effect on 4 would not itself show that 3 caused it or that the theory is novel.

## 4. Cross-source concrete identification gates (W23 continuation)

The public CRI data are real and scientifically useful for *analytical variation* and method-specific test judgments. However:
- The original 2022 cohort received no assigned AI translation treatment. One cannot retrospectively identify E[Y(1)-Y(0)] for the modern AI intervention; no observed Z=1 in original design (positivity failure).
- W21 actually parsed 89×464 `data/cri_team.csv` (72 distinct model-submitting IDs plus original reference Team0; 16 IDs had double team–hypothesis judgments). This supports secondary-data structure checks, **not an LLM causal experiment**.
- New source inspection of the original ISSP repository establishes five possible *Role of Government* waves 1985/1990/1996/2006/2016, with current GESIS versions requiring a registered account. These five files cannot necessarily reconstruct the original 2022 input exactly without the historical wave/harmonization, migration predictor inputs from World Bank/UN/OECD, code/version and sample restrictions.
- Original CRI author data on [GitHub](https://github.com/nbreznau/CRI) and [Harvard Dataverse](https://doi.org/10.7910/DVN/UUP8CX) (both cited by PNAS). GitHub code and derived CRI model-output CSV are already available; **the raw individual-level ISSP inputs are a separate acquisition and licensing step**.
- W22 executed *only synthetic code*, not a real AI-adapter A/B test, not original R model replication, and did not download the ISSP/Harvard dataset under the user's authenticated account.

### Possible future falsifiable design, not an executed claim

Fix a documented scientific H0/H1 and a set of authentic transformation tasks under the same source/data-usage terms. Randomly assign *conversion methods*, not arbitrary "LLM access" labels, between a strong official manual/deterministic method and a versioned AI-assisted method, while controlling validated resource use and providing an independent verifier. Evaluate:
- exact original scientific inferential object reproduced (including standard errors, appropriate contrast, missingness, code trace, units, source data/version);
- ability to perform a **predefined discriminating test** with justified uncertainty, even when numeric output matches;
- whether alternative valid routes rescue the test;
- if claiming collective lock-in, separate community-level adoption observations under credible units/time horizon and interference controls.

**Stop rule:** if a tested difference is explained by ordinary translation errors, workflow provenance, resource differences, methods variation or known converter network economics, label it established engineering/social-scientific effects; do not elevate P78.

## 5. Current W22 decision

**Completed:** actual run of 16-world synthetic negative identification witness; verified official ISSP five-wave acquisition route and three copies/source types; documented *where* strong controls would be needed.
**Not completed:** baseline R re-execution, individual-level ISSP/version authentication, matching AI+manual interventions, publication-level novel empirical explanation. **P77 remains active**; EPISTEME need not close or fall back into LEP case accumulation.
**Next W23:** use authentic accessible published result or explicit test case with named H0/H1 and at least one reliable non-AI conversion baseline, and try to *falsify* the hypothesized link; record a definite no-go if not feasible. Continue foundational theory inquiry, not dataset gardening.
