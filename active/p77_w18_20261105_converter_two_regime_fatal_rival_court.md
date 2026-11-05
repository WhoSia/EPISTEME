# EPISTEME-P77 W18 — Converter-Induced Choice Sign Reversal Is Prior Art; The Scientific-Test Residual Remains Unidentified

**Date:** 2026-11-05 KST  
**Authority:** [Official P77 Notion strategy](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53) · [binding director charter](../STRATEGY_P77_CURRENT.md)  
**Status:** P77 PHASE 1 / NON-NOVEL ECONOMIC BASELINE / P78 HOLD / PAPER HOLD  
**Previous:** [W17 non-identification court](p77_w17_20261105_acquisition_identity_and_hdf_identifiability_court.md)

## 1. Rival sources actually consulted in W18

The following **already-held Google Drive originals** were fetched and matched to relevant abstract/argument/results passages:

- [Farrell & Saloner (1985), *Standardization, Compatibility, and Innovation*](https://drive.google.com/file/d/1B1upRm8FEh87y_EcCyDHOc0DDkj62Gef/view), RAND Journal of Economics 16(1). The abstract distinguishes complete information/identical preferences (no excess inertia in their investigated case) from incomplete information, where excess inertia may occur and communication matters. Do not universalize either result outside its stated assumptions.
- [Arthur (1989), *Competing Technologies, Increasing Returns, and Lock-In by Historical Events*](https://drive.google.com/file/d/1devRTYAr9TJHJ4A01V-nYPqKAv3LQXzM/view), Economic Journal 99. Adoption-generated increasing returns and historical lock-in can be path-inefficient. Do not claim a new path-dependence theory.
- [Liu, Gal-Or, Kemerer & Smith (2011), *Compatibility and Proprietary Standards: The Impact of Conversion Technologies in IT Markets with Network Effects*](https://drive.google.com/file/d/1Lbbe1LJz_gN_0tzGBbmpYY-2Ba-bcOni/view), Information Systems Research 22(1), DOI 10.1287/isre.1090.0255. Endogenous converter provision and extent of conversion in sequential market competition; in part of the parameter range joint converter agreements soften product price competition and lift firms' product and converter revenues. Elsewhere comparative statics vary with network effects and market shares. This is **direct fatal prior art** for simplistic TLP claims.
- [Heinrich (2014), *Standard Wars, Tied Standards, and Network Externality Induced Path Dependence in the ICT Sector*](https://drive.google.com/file/d/13-FVE8iccVpnjgTqusR0gY-_spqErjqw/view). Inter-sector standard tying, reinforced lock-in and agent/replicator models.
- [Marro & Torr (2026), *Position: LLM Agents Are the Antidote to Walled Gardens*](https://drive.google.com/file/d/1oj1sQq0CWf_Z93_H0jFclL8DWXtpPOCR/view), ICML/PMLR 306, **position paper**; proposes AI adapters reduce service lock-in but explicitly anticipates new agent-framework lock-in and security/mapping error. No observed scientific-adoption effect follows from the position.

No claims of full exhaustive section-by-section literature review or novel empirical data. The five PDFs were held before W18; no Drive rename/move in this turn.

## 2. Small falsifiable-looking model that existing economics easily explains

**One prospective adopter** faces an incumbent I and challenger R, with the incumbent user base fixed. Let adapter intensity t be in [0,1], q the intrinsic advantage of R, c0 the no-adapter switching cost, k the incumbent's network benefit, r >= 0 the adapter's direct switch-cost relief, and h >= 0 the incumbent's adapter-enabled benefit of accessing R functionality **without leaving incumbent I**. The adopter's payoff difference is

D(t) = U_R(t) - U_I(t) = q - c0 - k + (r-h)t.

For stochastic logistic choice with positive temperature tau,

P(R | t) = 1/(1+exp(-D(t)/tau)).

Then sign(dP/dt) = sign(r-h) when tau > 0. A fixed reduction in switching cost can correspond to either a higher or lower propensity to migrate depending on the retention-side compatibility benefit h. This is not a surprising new theorem. It is an elementary choice-response illustration consistent with long-standing conversion/network economics.

Parameters are **dimensionless arbitrary utility units**, not estimates:
q = 0.5, c0 = 0.2, k = 0.6, r = 0.6, tau = 0.1.
At t=0, D=-0.3 and P(R)=0.047426 for both models.
- Case A (h=0): at t=1, D=+0.3, P(R)=0.952574.
- Case B (h=0.9): at t=1, D=-0.6, P(R)=0.002473.

**Actually run:** a local Python script printed these four values, passed the sign-reversal asserts and warned that this is a fixed-installed-base one-adopter comparison, not an equilibrium or field experiment. Committed source: [analysis/p77_w18_converter_two_regime_baseline.py](../analysis/p77_w18_converter_two_regime_baseline.py).

### Interpretation guardrails

1. Calling the Case B result "more lock-in" is, at most, lower one-step *migration propensity* under a fixed installed base. It is **not** a measured market share, a Nash equilibrium, an evolutionary absorbing state, or a long-run aggregate path.
2. The adapter raises direct individual ability to switch through r>0 in both cases, but in Case B the value of staying rises by more. The difference r-h is a **behavioral payoff comparison**, not a demonstrated inability to translate a scientific claim.
3. New technology could alter q, k, agent-framework costs, costs of scientific validation and the network itself. Such endogeneity is not modeled, yet it is the central question studied in the stronger economic prior art.
4. The model **does not contain an epistemic-test-production function** or a physical experimental task. It cannot infer any effect on the set of discriminating experiments. Tests may remain feasible even if the observed propensity to migrate falls.
5. This is not a formal reproduction of the Farrell–Saloner / Liu et al. equilibrium or numerical estimates.

## 3. The residual identification question

The founder's TLP has two stages:

**Stage A (covered):** adapter provision/translation -> switching/compatibility incentives -> individual/collective standard selection. Already extensively covered by Farrell–Saloner, Arthur, Liu et al., Heinrich and the new Marro position.

**Stage B (NOT SHOWN):** selection of standards/infrastructures -> loss, gain or modification of actually executable scientific discriminating tests (conditional on resources, skills, access to data, alternative validation pipelines, and historical evidence standards).

The presence of Stage A alone cannot prove Stage B. If Stage B is only ordinary resource allocation, domain tractability, data lineage, measurement calibration or community practice, it too is likely covered by Bakeev, McGrath/NCSA, Beauchemin–Staley, Leonelli and MQR.

A strong program must provide a **particular comparison**: given an H0/H1 scientific question and matched resources, do two routes produce different attainable evidence quality or test availability, after controlling for actual standard adoption, effective compatibility and an alternate known converter? Without a real observation to differentiate the existing theory, do not claim an independent explanation.

## 4. Attack matrix

| Candidate P77 claim | Existing competitor | Disposition |
|---|---|---|
| Lower adapter switching costs always erode incumbent standard | Elementary model plus converter economics | FALSE IN GENERAL under retained incumbent compatibility benefits |
| Lower adapter switching costs can reinforce incumbent retention | Liu-style conversion effects, network/compatibility economics | NOT ORIGINAL |
| Additional layer of agent/framework lock-in may replace platform lock-in | Marro & Torr (2026) | DIRECTLY ANTICIPATED |
| HDF data conversion keeps counts but changes storage reference identity | Prior P76 receipts, NCSA 2000 | BOUNDED TECHNICAL FACT, NO NEW EPISTEMIC LAW |
| Historical standards can suppress discrimination of competing physical theories beyond these accounts | Need a source-backed H0/H1 and real tests | UNIDENTIFIED / NOT ESTABLISHED |
| TLP is a completely new theory in 2026 | Multiple direct fatal rivals | REJECTED |

## 5. Research director decision and next W19

**Do not spend another week refining elementary converter-equilibrium toy models.** Treat these as completed *negative* baseline and use the time to identify an empirically grounded *scientific practice* case where **different hypothesis-discriminating tests** are actually attempted and their ability to survive standard/adapter transition can be compared.

W19 choice discipline: first read held originals about specific scientific workflow/cross-format conversion or genuine experimental model-transfer; specify the physical or statistical H0/H1, source bytes or accepted published dataset, comparator, measurement. If no actual distinguishable test exists, register **SCIENTIFIC-TEST MECHANISM NOT FOUND** and retain P77 Phase 1 without renaming market incentives as new epistemology.

No P78, no paper. No automatic research-lab closure; 12-week plan stays bounded, not an assurance of innovation. Protect Notion semantics / human-authored Git history / Drive byte custody / github-actions[bot] ban.

## 6. Drive missing list

Rosero Abad, Bekkers & Raiteri (2026), *Open Standards, Closed Standards or Vertical Integration?* DOI https://doi.org/10.59490/jos.2026.8038 — PDF NOT verified held.
Janssen et al. (2026), *Toward Full Interoperability in Materials Science*, DOI https://doi.org/10.1002/adem.71258 — PDF NOT verified held.
CERN Management Board 2000-12-07 original minutes — not held.
LEPC 2000-11-03 / Research Board 2000-11-07 original decision minutes — not held.
