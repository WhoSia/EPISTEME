# EPISTEME-P77 W47 — Scientific Hypothesis Discriminability vs Converter-Specific Output: A Data-Processing Negative Control

**Date:** 2026-11-11 KST. [P77 binding strategy](../STRATEGY_P77_CURRENT.md) · [W15 original adversarial experiment contract](p77_w15_20261105_matched_rival_observability_protocol.md) · [W46 standards economic court](p77_w46_20261111_original_economic_rival_matched_equilibrium_court.md). **Status:** P77 ACTIVE, P78 HOLD, PAPER HOLD, independent TLP novelty NOT CERTIFIED.

## 1. New independently executed original calculations, but an *existing* mathematical theorem

Define two hypothetical, exactly specified scientific hypotheses about a **binary observational outcome X**:
`P(X|H0)=(3/4,1/4)`, `P(X|H1)=(1/4,3/4)`. Equal prior probabilities, a converter is a hypothesis-independent Markov kernel `K(X→Y)`. Use `TV(P,Q)=½∑|p_x−q_x|` and optimal single-observation equal-prior classification error `R*=(1−TV)/2`. **These are mathematically defined synthetic distributions, NOT distributions calibrated from real BIA microscopy images or an actually observed scientific hypothesis**.

For any fixed hypothesis-independent Markov conversion `K`, standard **data-processing inequality for total variation** yields `TV(P0 K,P1 K)≤TV(P0,P1)`. A lossy converter cannot create information for this fixed binary discrimination problem; an invertible converter preserves this TV. This is well-known information theory/decision theory, **not an EPISTEME theorem**.

Locally executed a Python standard-library `fractions.Fraction` experiment with exact rational arithmetic:
| transformation | TV | Bayes equal-prior best error |
|---|---:|---:|
| identity | 1/2 | 1/4 |
| bijective output inversion | 1/2 | 1/4 |
| symmetric 1/5 flip noise | 3/10 | 7/20 |
| constant map to one output | 0 | 1/2 |

Also **enumerated all 25 binary Markov kernels** where each row's first probability is chosen from `{0,1/4,1/2,3/4,1}`; all satisfied TV contraction. **This finite scan is not a proof of the general data-processing inequality**; the full inequality follows from the triangle inequality and stochastic row-sum unity. The exact nontrivial example and set check demonstrate pre-existing theoretical constraints to any blanket statement.

[Committed read-only Python selftest](../analysis/p77_w47_discriminability_and_preserved_alternative_control.py). A closely matching local exact-rational script was **actually run** with the output stated; the committed source has a slightly different output format and has not separately been re-downloaded and run in local Python.

## 2. Formal distinction: isolated representation quality versus available scientific tests

If one conversion path is lossy and **raw X remains scientifically valid, accessible, and affordable under unchanged permissions, expert review and time budget**, the community's best technical choice is to use the raw X and preserve the original optimum `R*=1/4` in this fixture. A newly offered constant-Y converter is then merely an extra inferior option, rather than an automatic reduction of feasible valid tests. This is a specific **negative control**: treat the set of available experiments/paths `F` as monotone only under those explicitly fixed assumptions.

However under **actual institutions**, the raw access path might become inaccessible, costs or validation capacity may change, or policies and social acceptance could alter which tests are performed or considered warranted. This is where a scientific epistemological question might lie, **but those conditions are not entailed by information loss alone** and do not provide independent novelty absent a new causal prediction and a trustworthy observational design. Even the relevance of TV as a proxy for scientific testability must be justified: real science often has composite hypotheses, nuisance parameters, multiple samples, calibration, causal identification and more than two experiment choices.

## 3. The most serious existing adversaries

- **Standard information theory** explains loss/preservation of hypothesis discriminability under fixed channel and resources.
- **Farrell–Saloner 1985, Arthur 1989 and Liu 2011** (all actual user-held publisher originals re-read in W46) already cover adoption equilibrium, network effects and endogenous converter compatibility; behavioral nonadoption must not be renamed epistemological novelty.
- **Bakeev 2026** already argues domain-specific methodological tractability determines a transferred scientific model's acceptability.
- **Kuckertz et al 2026 DataDesc/ioProc** and **Huvila et al 2026 paradata** are publisher originals held in 10_PAPERS and already discuss technical interoperability and process representation.
- **MQR** remains a stronger local lab for instrument calibration and accepted measurement claims. No independent EPISTEME theory is gained by relabeling an experiment-scale mismatch.

**To surpass these rivals**, a future experiment needs actual pre-specified scientific `H0/H1`, raw instrument/source data, permissions, source/converted measurement likelihoods with independent checking, **a version-fixed AI adapter randomly or credibly quasi-randomly assigned versus the best approved deterministic/manual adapter**, tracked peer-group standards adoption, test selection/funding/validation and all alternative source paths. A mere converted-file read-error or different LLM grader score cannot satisfy this.

## 4. Executed findings and what is still missing

- **PASS:** original exact mathematical calculation with 4 channels and enumerated 25-quarter-grid binary kernels; one unchanged raw alternative preserves optimum under assumptions.
- **NO CLAIM:** actual original scientific evidence, BIA microscopy test, biological ground truth, completed new theorem, scientific publication result or a randomized AI converter treatment.
- **NO-GO:** founding TLP full causal Z→A→T remains absent; no independent explanatory residual demonstrated beyond above known rival theories.
- **Research governance:** W46/W47 results will remain source-labeled synthetic **adversarial counterexamples**, not substitute for historical real lab evidence. P77 ACTIVE / P78 HOLD / PAPER HOLD, no automatic closure.

**Next bounded source obligation:** locate an authentic science-domain converter *rollout* with valid raw/derived calibration and lab standards choices and independent successful/failed fixed hypothesis tests, or explicitly confirm no source-supported identification path in current corpus and return to founder novelty court rather than extending synthetic examples.
