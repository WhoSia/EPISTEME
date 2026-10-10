# P71 Paper Candidate Court — Rival Literature, Reusable Negative Evidence, and a Publishable-Claim Ladder

**Stage:** paper-idea triage and analysis plan; **not** acceptance, newness confirmation, independent-human-review completion, or a frozen confirmatory trial.

## Sources checked in the user's original canonical Google Drive

1. **Baan, Aziz, Plank & Fernández (2022), *Stop Measuring Calibration When Humans Disagree***. [Original PDF in Drive](https://drive.google.com/file/d/1almvYH7czW2Db-uDvspOZTxAFBSWSCYu/view). [Original authors' claim] Calibration to majority-vote ground truth is problematic in the presence of inherent human disagreement; propose instance-level measures based on distributions of human judgments, rather than treating the majority label as an unambiguous oracle. [Our implication] Do not force every AVeriTeC projected packet to inherit a single source gold label or erase both raters' genuine ambiguity. **Do not pretend two raters estimate a full population judgment distribution**.
2. **Mani, Liang & Lipton (2024), *Fast Evidence Extraction for Grounded Language Model Outputs***. [Original FEVER-workshop paper in Drive](https://drive.google.com/file/d/1yU-Pqxkg5PFvvU7ZYqbXu-Y0yxdUFhqx/view). [Original authors' claim] Evidence span extraction can reduce the human effort of verifying grounded generated outputs, and paper studies architectures/efficiency. [Our implication] Separately measure time/effort to *locate* warrant and *decide* whether cited warrant suffices. Automated evidence retrieval does not automatically confer packet-level support.
3. **Blackwell (1951), *Comparison of Experiments***. [Original PDF in Drive](https://drive.google.com/file/d/1AabK3bac9aNuX5ASeEqkRDRucQSDZ7JB/view). [Original authors' claim] Compare information-gathering experiments by attainable risk profiles across decision problems. [Our implication] A representation is not superior merely because one accuracy point is higher; ask whether its information admits better downstream decisions. P71's simple cost interval is **not** newly invented decision theory and should not be sold as such.
4. **Angelopoulos, Bates, Candès, Jordan & Lei (2025), *Learn Then Test: Calibrating Predictive Algorithms to Achieve Risk Control***. [Original journal PDF in Drive](https://drive.google.com/file/d/1OC0CSHbj6DeFNeNiop81QDUHc9pduzTy/view). [Original authors' claim] Finite-sample risk control via calibrated learning/testing and multiple-hypothesis testing under specified assumptions. [Our implication] An empirical risk certificate requires a justified sampling structure and a real risk-calibration set. Hand-entering a cross-ecology shift epsilon is NOT a finite-sample risk guarantee.
5. **Schlichtkrull, Guo & Vlachos (2023), *AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web***. The original paper and source data underpin ECO2: [original author manuscript PDF](https://arxiv.org/pdf/2305.13117), [dataset source](https://github.com/MichSchli/AVeriTeC). **Drive 미확보(색인 검색 기준)** on exact title/author bounded query; direct arXiv PDF verified. Do not imply this source is absent from the world or that a title search establishes novelty.

**Priority:** original Drive papers were found and directly read (abstract and relevant introductory/methodological passages); this is a bounded, not exhaustive, state-of-the-art review. Novelty must be challenged with more targeted searches before submission.

## Candidate comparison

| Rank | Candidate paper question / tentative title | Present strongest evidence | Fatal deficiency right now | Publishability trajectory |
|---|---|---|---|---|
| **A1** | **When the Output Contract Changes the Verdict: Measurement Validity of Evidence-Grounded LLM Evaluation** | P69 exact source-locked 192-call negative instrument pilot; P69-R1 4+64 exploratory calibration, positive Gemini strict 0/4 vs JSON 4/4 under identical task prompts; P70 single external SciFact 32-call metadata | Two authored tasks, two draws; cannot infer causal internal schema mechanisms or generalize to other model providers. No independently adjudicated P69 task oracle | **Strongest immediate methods/negative-result short-paper candidate**, but label every present claim exploratory and add held-out task clusters plus independent oracle before full-length empirics |
| **A2** | **Warrant-Preserving Representation Migration: Partial Semantic Bridges and Refusal under Evidence-Ecology Shift** | P70 conditional bound/nonidentification, 256 compiler checks, SciFact vs AVeriTeC real-source data and 8 metadata-level same-polarity links; P71 typed review admission and bridge court | 0/32 independent packet judgments, no verified witness bijection, no live AVeriTeC model ecology, no novel nontrivial transport theorem | **Potentially most scientifically important theory+empirics paper after new evidence**, not a present empirical paper |
| **A3** | **Certified Abstention Before Migration: Contract-Robust Switching with Warrant and Audit Costs** | P71 synthetic conditional cost threshold, original Blackwell/Risk-Control rival grounding | Theoretical rule is a straightforward inequality; no real counterfactual migration costs, no comparative policy evaluation | **Possible application/decision paper** only after nontrivial new theorem or real switching policy/regret experiment. Do not advertise current arithmetic as novel theory |

## Primary recommendation

Work **A1 as an explicitly exploratory falsification/methodological note**, while developing **A2 as the central P71 long-term paper**. A1 must not claim P69 reached its originally specified held-out multi-ecology manuscript gate. P69 R1 itself is a negative calibration and its post-hoc discoveries must be treated as hypothesis-generating.

### A1 falsifiable predictions (prospective; not retroactive p-values)

- H_contract: with byte-identical prompt and independently judged positive warranted claim, strict and JSON execution envelopes yield different positive-response rates. Hold provider, exact model version, source case, decoding and output content constant to the feasible extent; randomize call blocks, log finish reason and schema details.
- H_selection: differences caused only by format loss vanish when comparing all responses through a contract-neutral, independently reviewed answer-direction extractor. Invalid JSONs are MISSING for latent semantics, not all wrong by definition.
- H_prompt×contract: procedural evidence-tracing prompt's contrast varies by response envelope even when schema validity is complete (Gemini observed only on four positives). Null false-positive and evidence precision endpoints are required.
- Strong rival: apparent contrast is idiosyncratic to these two synthetic cases, a historical provider snapshot, a scorer error or correlated generation draws. New independent task topology and masked human audit are mandatory before scaling.

### A2 pre-registered adversaries

- **Projected-packet label noninheritance:** Does the full-original AVeriTeC label survive a two-QA projection, *as judged blindly*? If not, STOP using source label as gold. Do not exclude failed projections after model results.
- **Witness-graph equivalence:** Can role/proof/warrant bijections and temporal reference maps be certified across a science-abstract sentence and a web-QA chain? If no, record *incomparable* not *transport failed*.
- **R/H operator non-equivalence:** R is evidence-ID alpha-renaming; H is row order reversal. If QA depends on another QA's referent, H cannot be assumed semantically harmless. A paper about **the boundary of safe representation change**, even if all cross-ecology effect extrapolations fail, is still a valuable methods result if independently reproduced.
- **Behavioral bridge falsification:** Freeze `phi`, historical source-effect estimate and target mechanisms before calling target providers; if target observed effects fall outside sensitivity bounds with valid CI, reject the shift assumption or mechanism grouping. Avoid tuning epsilon retrospectively until it contains the target.
- **Partial-bridge selectivity:** Do strictly certified bridge cases support more accurate transport intervals than a metadata-only comparator, controlling for sample size and abstention selection? If not, the added proof-certificate effort fails to improve decisions.

### A3 decision validity adversaries

- Does the SWITCH/RETAIN/HOLD policy lower target *total* decision loss after independent human audit costs and migration/reversal costs, compared with always-retain, point-estimate-switch and metadata-only rules?
- What is the lost opportunity when insisting on a proof certificate? Report unnecessary review and foregone beneficial migrations, not merely reduced unsafe switches.
- Blackwell risk-order and classic cost-sensitive selective decision rules are serious **rival theories**, not straw men. The paper needs an identifiable new regime or higher independent decision utility.

## Quantitative methodology and unit controls

- **Current P69 positive Gemini interaction:** `(JSON_v1−JSON_v0)−(Strict_v1−Strict_v0)=(4−0−(0−2))/4=1.5`, a difference of changes in fractions. The value is not a 150% relative improvement, population average effect, or statistically reliable p-value.
- **Current P70 SciFact:** two providers × four original claim clusters × four transformations = 32 calls; a zero observed all-call R/H contrast on four cases cannot establish universal invariance.
- **Current ECO2 16 variants:** exactly FOUR independent underlying claim items, not 16 independent sampled semantic worlds. Two human raters each assessing 16 yield 32 **judgments**, but only 4 source claim clusters. Third-party arbitration resolving disagreements cannot turn 4 source claim clusters into 32 independent research observations.
- **Future full study (not approved):** sample many independent claims across two or more source ecologies and source fact-checking organizations; stratify dependencies, temporal qualifiers and referent shifts **before** treatment responses. Treat source organizations and claim clusters as grouping units, use cluster-aware uncertainty, and report effective sample size/power based on a separate preregistration. Do not hardcode a significance claim based on n=4.
- Binary all-call execution correctness and explicit missing-format indicators remain independent endpoints. Do not condition on format success and then present the conditional estimate as an all-call causal effect.
- P71 robust switching interval requires *external* human review, source support, shift bounds, cost measurements, model contract coverage and prospective protocol. No current data meet every warrant; present-only output must be HOLD.

## Writing and replication deliverables

Suggested paper skeleton A1: motivation/matched historical instrument; noncausal exploratory R1 result; explicit formatted and semantic endpoints; negative provenance and schema effect hypotheses; historical failure/repair reproducibility; independent held-out validation and limitations. Avoid cherry-picking Groq successful arms while suppressing Gemini strict.

Suggested paper skeleton A2: formal partial witness map definition; counterexamples (temporal, object identity and QA order); independent masked packet study; certified vs metadata-only bridge competing predictors; preregistered held-out ecology transport experiments; cost-sensitive migration implication and negative cases.

**Stop rule:** if independent human packet truth or held-out scientific source equivalence cannot be established, publish an appropriately scoped methods warning or leave paper HOLD. Never extrapolate a universal representation law from source labels and JSON-only success.
