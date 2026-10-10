# EPISTEME

Active execution surface for the EPISTEME research program.

## P70 full-evidence implementation strengthened — all original answer records (2026-10-10)

Initial full-QA handoff correctly preserved all ten original question positions but selected only one usable answer per question. The implementation has now been strengthened to retain **every original answer record** (including unusable answers with explicit status) and to reject missing original question positions. The source-locked actual four-claim sample had **10 original question records and 10 original answer records**, 8 retained complete-QA projection atoms, 2 original questions outside the projection and 1 original question lacking an eligible source answer. Human reviewers may cite only source-authorized, eligible answer records, not an empty or unusable answer entry. **This is still only the original dataset's answers, not a live independent crawl of cited web pages.**

[Exact latest G-001 three-job CI #38044892498](https://github.com/WhoSia/EPISTEME/actions/runs/38044892498) **SUCCESS**; all P73/P69/P70 jobs passed after the strengthened full-answer compiler. [Verified canonical v2 P70 counts-only receipt](https://drive.google.com/file/d/1eTBqqRl27Okoji06bdNLEAmJorgisCUI/view). Earlier v1 receipt is preserved as prior code history but **v2 supersedes it for complete original-answer handling**. Reviewer outcomes remain 0/16; P71 old packet review 0/32.


## P73-P5 × P69 × P70 — independently sourced review and source-time audit design (2026-10-10)

**Canonical [joint protocol and actual source checks](active/p73_p5_p69_p70_independent_validation.md)**. [G-001 read-only original-source three-job CI #38044552352](https://github.com/WhoSia/EPISTEME/actions/runs/38044552352) PASS: P73-P5 notice-vs-control prospective audit design has **zero actual interventions and causal HOLD**; P69 source-authored SciFact holdout has **8 previously unused claims/8 different documents with no overlap with P70's 4 selected claims/documents**, but is still **one SciFact ecology**, and blinded independent scorers **0/16**; P70 compares **10 original AVeriTeC question records vs 8 retained QA atoms**, with 2 omitted and 1 question lacking a usable original answer; four human full-vs-projected raters **0/16**. Existing P71 16-variant dual human review **0/32**, P69 paper construct HOLD, P70 semantics/behavioral transport HOLD. **No new API calls or human participation.**

**Verified Drive receipts:** [P73 design](https://drive.google.com/file/d/1bd-ELHsF801hNuH_da78xSAI9gnJammg/view) · [P69 scorer-ready holdout](https://drive.google.com/file/d/1j4psNjZi6xcS7Ob6gy6UE3wn8LDk1alc/view) · [P70 full-vs-projected panels](https://drive.google.com/file/d/1OCllIKsyZmUmvjnlCLzDom0EuL_buYjs/view). Only hashed counts and HOLDs are uploaded; private licensed claim/reviewer packets are deleted from CI runner.


## Repository doctrine

- `main` is the working line; do not create routine per-stage branches.
- Keep only code needed by the **active executable stage and its transitive imports**. Do not delete an older module merely because its P-number is lower: resolve backreferences first.
- Before retiring code: generate exact Git blob/commit SHA manifest, dependency and workflow reference matrix, upload a byte-identical archive with checksum to Google Drive, verify readback, and only then remove the retired source files from `main`.
- Research receipts, historical packets, large result ledgers, literature custody, and superseded artifacts belong in Google Drive / Notion, not this repository.
- Git history is not the scientific archive.
- Argument comes first; literature and code are pressure, falsification, or execution instruments rather than sources of authority.
- GitHub Actions may compute, test, validate, and upload artifacts, but `github-actions[bot]` must not write repository history. Workflows default to `contents: read`.

## Parallel current work — EPISTEME-P69 (paper HOLD) & EPISTEME-P70 (theory OPEN)

**Live custody update, 2026-10-09 KST:** P69 [4-slot canary #37917857783](https://github.com/WhoSia/EPISTEME/actions/runs/37917857783) passed `MEASUREMENT_CONTRACT_READY` at HEAD `18cb018c`. The [192-slot actual hosted pilot #37925719478](https://github.com/WhoSia/EPISTEME/actions/runs/37925719478) completed 192/192 provider responses but its scientific/measurement artifact is **`TECHNICAL_PILOT_HOLD`**, although GitHub's `analyze` job was green. Strict schema: Gemini 48/48 format-valid, Groq 48/48. JSON object: Gemini 47/48 format-valid but 0 strictly grounded valid-positive cases; Groq 34/48 format-valid, below the 36/48 technical threshold. Original result artifact: [pilot verdict](https://github.com/WhoSia/EPISTEME/actions/runs/37925719478/artifacts/11613872997). Pilot aggregator is repaired prospectively to exit nonzero on HOLD; historical green run is not relabeled. No further paid run or main 8,192-call study authorized; P69 paper claims remain OPEN/HOLD.

**P70 now separately THEORY-OPEN, no P70 provider calls.** [Formal theory and countermodels](active/p70_theory_program.md) · [finite exact-rational checker](src/p70_transport.py) · [native 256-packet witness/trace bridge audit](src/p70_bridge_audit.py) · [read-only P70 CI](.github/workflows/p70_theory.yml) · [P70 Notion](https://app.notion.com/p/3f4ef561cf9281698d75db449586b606). P70 is a parallel conceptual program, not retroactive P69 manuscript closure.

## P73-P1/P2 — Four New Original Decision-Tree Sources and History-Safe Winning Beliefs (2026-10-10)

**Four user-supplied Drive PDFs have been read, renamed, moved from `00_INTAKE` into `10_PAPERS`, and parent-folder readback verified:** [Hyafil & Rivest (1976)](https://drive.google.com/file/d/1i4AUMzbYhYOLvA_H5Mw7wBVBATP4YsGR/view) expected-test-cost NP-completeness (scan text imperfect); [Verwer & Zhang (2019)](https://drive.google.com/file/d/1kQMSkaCz1fhLn4fAHn5OI5EYygcqSj8y/view) binary ILP classification-tree training; [Avellaneda (2020)](https://drive.google.com/file/d/11VHs_cumtrE08i1otc3llbVV9s0wGLNA/view) incremental SAT minimum-depth classifier; [Firat et al. (2020)](https://drive.google.com/file/d/1U-Yly-n0h-nccac3payWJ-0nyVuZUJ_x/view) accepted 2019 prepublication column-generation tree-classification heuristic. **Three classifier-learning optimization papers do not directly solve P73's active warrant-probe safety question**, but substantially limit novelty claims about decision-tree optimization. [Source & competing-theory court](active/p73_p1_new_literature_and_dynamic_observation.md).

**P73-P1/P2:** [history-safe exact decision court](src/p73_history_safe_court.py) demonstrates that a warrant-preserving preparation can make otherwise uninformative measurements diagnostic (worst cost 2), whereas two world-pairwise distinguishing tests may be *unusable on the full belief set*, yielding no globally safe policy. [finite winning-belief fixed-point](src/p73_winning_belief_court.py) independently verifies horizon 2 and nonexistence with globally inadmissible probes. [P0–P2 GitHub Actions #38042213562](https://github.com/WhoSia/EPISTEME/actions/runs/38042213562) SUCCESS under `contents: read`, no bot writeback. This is **classical active testing and partial-observation reachability**, not a newly established law or real audit-safety certification.

**Scientific limitations unchanged:** P71 0/32 genuine AVeriTeC human ratings; P69 manuscript construct HOLD; P70 semantic transport HOLD; source provenance-attestation flags in test fixtures are **model assumptions**, not signed independent attestations. No new provider spend or participant enrollment.

## P73 OPEN — Source-Certified Safe Warrant Observation (2026-10-10)

**Official P73 Notion:** [P73](https://app.notion.com/p/3f5ef561cf928145862cdfdc1fa556b6). **Research scope:** [P73 canonical program](active/p73_research_program.md), [exact finite decision-tree court](src/p73_safe_probe_court.py) and [G-001 read-only CI #38041279040](https://github.com/WhoSia/EPISTEME/actions/runs/38041279040) **SUCCESS**. Four *synthetic* hidden worlds share citation and time but differ in witness admissibility. Warrant-targeted safe deterministic probes yield adaptive minimax cost **3** versus best nonadaptive **4**; a cheaper probe that changes warrant-bearing evidence, and one without independent source attestation, are excluded. With a necessary safe probe removed, no safe policy exists. Standard adaptive decision-tree theory, NOT novel mathematics nor actual external passivity/experimental evidence.

**Original Drive research custody:** [Türker, Ünlüyurt & Yenigün 2016 ADS](https://drive.google.com/file/d/10N6hZKeeKT6zMp0udLza4Si1yIaYEKUm/view), **Drive held/original read**; [Hauser & Bühlmann 2012 interventional equivalence](https://drive.google.com/file/d/1eMqlfzxAZpNGbMFOCS96ZU_oosXUNxkN/view), **Drive held/original read**; [Brown 2022 stateful performativity](https://drive.google.com/file/d/1690w4PxcI0lHBFgNmTulv_CkFS36r79p/view), **Drive held**; [Rivest & Schapire 1993 homing sequences](https://drive.google.com/file/d/1JNqBDFbRgaUEHBwDQJVhgWM1CPkFn1pp/view), **file located but full text not parsed**. Hyafil & Rivest 1976 optimal decision trees: **Drive 미확보(색인 검색 기준)**, external original DOI verified. All claims of novel state identification, active experiment selection or cost minimization therefore face direct prior-art challenges.

**Unchanged hard boundaries:** P71 independent AVeriTeC packet humans **0/32**; P69 manuscript/construct HOLD; P70 semantic bridge and cross-ecology effects HOLD. No new model/provider calls or human enrollments. All new GitHub Actions have `contents: read` and no bot-authored history updates under G-001. P73-P1 must validate a *genuine* history-conditioned, independently sourced noninterference or preservation witness before making a publishable claim.

## P72-P1 source-based proof survival court — P73 proposed (2026-10-10)

- **Actual Drive prior-art verification:** Brown, Hod & Kalemaj (2022) original [`brown22a.pdf`](https://drive.google.com/file/d/1690w4PxcI0lHBFgNmTulv_CkFS36r79p/view) **보유 확인/원문 정독**; [Perdomo et al. 2020 Drive copy](https://drive.google.com/file/d/1i3Db3WOaHqxcm5SD5-HewjmAZOVnSv11/view) already held. Zhang et al. 2023 original exact DOI/title **Drive 미확보(검색 기준)**; publisher and NIH author-manuscript read externally, not falsely listed as a Drive original. Brown's state-dependent performative transition and RRM convergence kill generic `history changes the world` claims as P72 novelty.
- **P72-P1 exact proof/observation court:** [code](src/p72_warrant_fibre_court.py), [method and original-paper comparison](active/p72_p1_warrant_transport_and_p73_proposal.md); [read-only Actions #38040744999](https://github.com/WhoSia/EPISTEME/actions/runs/38040744999) PASS. Admissible premises+inference-rule preservation suffices for warranted conclusion survival but is not necessary when independent alternative proofs exist; observation-fibre constancy is an elementary iff criterion for identifying a proof-validity predicate; identical public citations can conceal opposite post-audit warrant validity. G-001 read-only CI; 0 calls, 0 external human judgments, no novel-theorem claim.
- **P73 title proposed, NOT OPEN:** *EPISTEME-P73 — Warrant-Separating Observation under Reflexive Evidence Dynamics: Minimal Discriminating Audits, History-Indexed Proof Transport, Intervention-Safe Identification & Sequential Switching Decisions Court*. Its new prospective burden: find **genuinely independent and non-disruptive** evidence observations which separate hidden admissibility worlds, and compare them with classic active causal design and value-of-information theories before scientific promotion.
- **Unchanged scientific HOLDs:** P71 independent AVeriTeC review `0/32`; P69 paper-level construct validation HOLD; P70 semantic/ecology transport HOLD. No automatic paid rerun or participant recruitment.

## P72 ACTIVE — original P0 results (2026-10-10)

P72 has been formally opened: [canonical program](active/p72_research_program.md) and [Notion](https://app.notion.com/p/3f5ef561cf928172a422ec7f44da0599). [Original P0 read-only CI #38040008919](https://github.com/WhoSia/EPISTEME/actions/runs/38040008919) PASS. Its [P0 code](src/p72_reflexive_audit_court.py) checks identification of information-acquisition versus audit-announcement contrasts and bounded synthetic ordering counterexamples. This is mathematical design validation, not observed causal behavior or novel theorem. Earlier P2-P4 and external performative prediction are explicit prior-art competitors. P71 external human reviews 0/32, P69 paper HOLD and P70 semantic bridge HOLD remain. No new commercial model calls. Actions follow G-001 read-only. [Archived scoped receipt](https://drive.google.com/file/d/1G8I6t-6pjbyktKjqyf-d91jneFEKUEX1/view).

## P71-P5 endogeneity court and P72 formal-name proposal (2026-10-10)

- **P71-P5 original-code CI:** [GitHub #38039400106](https://github.com/WhoSia/EPISTEME/actions/runs/38039400106) SUCCESS with [exact counterworld stress tests](src/p71_endogenous_audit_court.py): robust dominance vs classical minimax-regret are distinct policy objectives, and two observationally identical audit-only worlds can have opposite unaudited migration benefits. These are **known-class decision/causal identification countermodels**, NOT novel theorems, actual target outcomes, or human annotations.
- **P72 FORMAL TITLE PROPOSED ONLY:** **EPISTEME-P72 — Endogenous Warrant Acquisition & Reflexive Representation Migration: Audit-Induced State Transitions, Counterfactual Evidence Stability, Sequential Review Value & Irreversible Switching Falsification Court**. See [P71–P72 boundary and prior-art court](active/p71_endogenous_audit_p72_proposal.md) and [P71 formal program](active/p71_research_program.md). Compete against existing performative prediction/partial-identification and value-of-information theory. P72 is NOT open/activated, no paid model or real human experiments authorized.
- **HOLD unchanged:** P71 independent AVeriTeC human judgments 0/32; P69 publication construct HOLD; P70 proof bridge and behavioral cross-ecology transport not identified. Workflow is G-001 read-only and has no bot git writeback.

## P71 active — Two-Pipeline Human-Warrant Admission & Original-Source Integration (2026-10-10)

**Single canonical P71 research page:** [P71 Notion](https://app.notion.com/p/3f5ef561cf9281d6a429f59cdcf4fbc7). The [P71-P0 operational companion](https://app.notion.com/p/3f5ef561cf92819eaeafcf76bb85feaf) is NOT an additional competing research stage. [Formal program](active/p71_research_program.md) · [paper rival court](active/p71_paper_candidate_court.md) · [exploratory methods draft](active/p71_paper_A1_exploratory_extended_abstract.md).

**Actual zero-provider-call source integration:** [P71 G-001-safe CI #38030378027](https://github.com/WhoSia/EPISTEME/actions/runs/38030378027) SUCCESS at human-authored HEAD `9a36b1eb3fe6ca1d8529efc23caacd92f22bee11`. The CI executed both independent-source-preserving review pipelines against the **exact pinned original AVeriTeC 500-case dev dataset**, and checked 16 A/B masked packets, matching source packet hashes, source label masking, owner-only file permissions, separate offline HTML forms, two-adjudicator *artificial fixture* agreement and disagreement, invalid source hashes, false independence claims, and the independent third-adjudicator interface. See [src/p71_integration_court.py](src/p71_integration_court.py) and [P71 offline packet UI](src/p71_review_html.py). The combined code-based test PASS **does not mean any genuinely independent human judgments were made**: 0/32 actual AVeriTeC packet reviews, target semantic bridge HOLD, P69 manuscript scientific closure HOLD, P70 cross-ecology effects not identified.

**G-001 contributor compliance:** Actions use `permissions: contents: read`, check out sources, run tests and publish only counts/hashes/status receipts. The workflow **never commits, pushes, or merges**, and its G-001 audit checks this prospectively. GitHub Actions are not credited as source contributors; the triggering commits were authored by the human linked account. [Long-term Google Drive evidence receipt](https://drive.google.com/file/d/1c37oGfD1JPjvw0HlzYV4yEFkddlif3B-/view). No raw AVeriTeC claim/QA or sealed gold were published in Actions artifacts.

**Two existing review codepaths remain temporarily until a contributor-doctrine archive + dependency manifest supports safe retirement.** Canonical dispute adjudication authority is `src/p71_review_disagreement_court.py`; `src/p71_review_handoff.py` adds offline handoff, role mapping, and delegates third-party judgment to that canonical court. Simulated test raters are never accepted as observed people. Genuine human reviewer files require an authorized private handoff and proper consent/custody checks.

**Research direction:** P69 contract-dependent measuring failures suggest an exploratory methodological paper; P70/P71 proof- and ecology-conditioned switching requires independently certified projected-packet warrant and costed target-policy comparison. Neither paper is publication-certified yet.

## P69/P70 scoped closure, scientific holds and P71 formal-name proposal (2026-10-10)

The final [machine-read original-source closure court](active/p69_p70_scoped_closure_court.md) distinguishes **completed bounded experiments** from **unfulfilled scientific and manuscript promises**. [Real-receipt closure CI #37997389628](https://github.com/WhoSia/EPISTEME/actions/runs/37997389628) PASS, no provider calls: P69's original 192-call instrumentation and R1 64-call measurement repair are **SEALED NEGATIVE/HOLD**, *not* publishable causal-effect results; P70's conditional bound/countermodels, 32-call one-source SciFact calibration and second AVeriTeC original-source structural compiler are finished in their specifically defined scopes; original two-source partial evidence-role bridge has eight candidate same-polarity+provenance matches **without** semantic warrant identification. [ECO2 real original-source bridge CI #37997168518](https://github.com/WhoSia/EPISTEME/actions/runs/37997168518) PASS, with **0 of 32 actual independent masked human review judgments obtained**—not a semantic PASS.

The source-specific [four-claim unblinded triage and blinded-human protocol](active/p70_packet_semantic_triage.md) flags temporal reference, evidence-object mismatch, and QA dependency. Review executable: [src/p70_packet_adjudication.py](src/p70_packet_adjudication.py); cross-source typed bridge: [src/p70_cross_ecology_bridge_audit.py](src/p70_cross_ecology_bridge_audit.py). Neither the sealed source annotations nor assistant-side qualitative triage count as the demanded two human independent adjudications. P69 paper remains `PAPER_CONSTRUCT_HOLD`; P70 full cross-ecology effect remains `NOT_IDENTIFIED`. Do **not** repeat any paid model calls or mark these paper-grade promises `CLOSED`.

**Historical P71 naming proposal (superseded by the P71 active record above):** EPISTEME-P71 — Proof-Bearing Representation Migration across Interface and Evidence Ecologies: Independent Warrant Certification, Partial Semantic-Bridge Completion, Contract-Conditioned Decision Stability & Prospective Switching-Cost Falsification Court. See closure court for admission conditions. [Drive scoped-closure custody](https://drive.google.com/file/d/1XK_4Kigm99wrbV25TEBdOovLjTDxRDnO/view) · [Drive ECO2 semantic/bridge HOLD](https://drive.google.com/file/d/1mnqklHYDzgxraWjwK2MiKLrNdyW-bNh6/view).

## P70 new boundary — Gemini contract rivals and independent real-world QA ecology (2026-10-10)

- **Six-hypothesis model/contract reversal court:** actual frozen P69 R1 64-call receipts from [run #37931512662](https://github.com/WhoSia/EPISTEME/actions/runs/37931512662) were recovered read-only and reclassified by task × prompt × channel × semantic label. Gemini `procedure_v1` positive strict-schema 0/4 versus JSON-object 4/4, both with 8/8 valid-format responses. Prompt change-by-channel descriptive positive interaction `+6/4`; this is *not* a stable population effect, identified internal decoding mechanism, or P69 science PASS. [Executable rival court](src/p70_r1_rival_court.py) and [full hypothesis predictions/limitations](active/p70_rival_ecology_program.md). [Read-only CI #37987665253](https://github.com/WhoSia/EPISTEME/actions/runs/37987665253) PASS with zero model calls.
- **Second source ecology `ECO2` — AVeriTeC:** independently annotated real-world web claim verification with sourced question–answer evidence (distinct from SciFact scientific abstract claims). [Official AVeriTeC original](https://github.com/MichSchli/AVeriTeC), original author manuscript [PDF](https://arxiv.org/pdf/2305.13117). Frozen original `data/dev.json` has 500 records, SHA-256 `499793726b4a5406780928a3d9dedc48d6dd53de778f22437d129cacdb08e300` and 1,785,475 bytes. Four independently sourced claims (2 Supported, 2 Refuted) generate 16 **structural** R/H packet candidates; both packet-level gold labels and QA-dependency/partial-bridge equivalence remain **HUMAN_HOLD**. [Original source/checker](src/p70_ecology_averitec.py), [read-only CI](.github/workflows/p70_rival_ecology.yml). No AVeriTeC model experiment authorized or run. Dataset license CC-BY-NC-4.0; source text is not mirrored.
- **Source audit receipts:** original-source/rival verdict [Drive AVeriTeC evidence](https://drive.google.com/file/d/14z4qQsuIr9C8WYs67R1KsiD4VJ8wgMbw/view) and [Drive R1 model-contract rival court](https://drive.google.com/file/d/17ZzSho2K1WwWR4MbZJlGtQe9vS45-QsG/view), verified in existing EPISTEME evidence folder. Zero additional provider calls.
- **Hard research gate:** a source label obtained using all original QA is NOT automatically a correct label for a projected two-QA packet; QA order can encode dependencies. The second ecology is genuine as a documentary source, but cross-ecology experimental replication and a validated `phi` bridge have **NOT** yet been achieved. P69 `REPAIR_MEASUREMENT_HOLD` and its blocked 8,192-call paper design persist.

## 2026-10-09 — Actual paid runs, forensic recovery and cost-preserving continuation

**Two old manual workflow runs remain red for genuine orchestration bugs, but their model evidence has been recovered with ZERO additional provider calls.** [Original P69 R1 run #37929410643](https://github.com/WhoSia/EPISTEME/actions/runs/37929410643) completed **4/4 valid** provider Canary requests; the later judge failed on a missing transitive `groq` SDK import before **any** of the planned 64 calibration requests. [Original P70 external SciFact run #37929439637](https://github.com/WhoSia/EPISTEME/actions/runs/37929439637) completed **32/32** hosted responses; its old analyzer improperly included two offline fixture documents, so its model-bundle census failed. Neither red Actions badge can be retroactively changed.

[Read-only source-artifact recovery #37930648628](https://github.com/WhoSia/EPISTEME/actions/runs/37930648628) **PASS**, with `P69_MEASUREMENT_CONTRACT_READY` and `P70_PROVISIONAL_SINGLE_ECOLOGY_MEASURABLE`, using no new provider calls. [P70 original external source and recovered verdict](active/p70_external_source_pilot_protocol.md): GPT-OSS source-label matches 16/16, Gemini 8/16, all 32/32 response formats valid; each bundle observed zero matched R/H differences under four independent claim clusters from ONE SciFact ecology, not a transport law. Original sources and the independent verdict are now in the existing EPISTEME Google Drive archive.

For P69 R1, **do not manually repeat the old 68-call run**. [Resume only the remaining 64 calls](.github/workflows/p69_r1_resume_64.yml), with manual confirmation `RUN_REMAINING_64`. It reuses validated original 4-slot Canary artifacts and checks out the original experiment's exact `2363dc9b` source; [zero-call preflight #37930782814](https://github.com/WhoSia/EPISTEME/actions/runs/37930782814) **PASS**. Until manually dispatched, those remaining 64 calls are NOT RUN. P69 historical 192-call measurement `TECHNICAL_PILOT_HOLD` and manuscript `PAPER_CONSTRUCT_HOLD` remain authoritative.

## Active execution gates — P69-R1 measurement repair and P70 external source

- **P69-R1:** forensic 192-call source analysis established different failure modes: Groq JSON invalid direction vocabulary/grounding; Gemini JSON overabstention on positive cases. New [P69-R1 protocol](active/p69_measurement_repair_r1.md), [paired worker](src/p69_measurement_repair.py), [fail-closed judge](src/p69_measurement_repair_analyze.py), [capped Actions](.github/workflows/p69_measurement_repair.yml). Original 192 results are immutable. Manual call ceiling **68** (fresh four-slot provider canary gates 64 calibration calls). Push and offline CI run **zero** provider calls. Even calibration-ready does NOT authorize 192/8192 main extrapolation.
- **P70 external originality pilot:** [precommitted externally annotated SciFact protocol](active/p70_external_source_pilot_protocol.md), [source and model worker](src/p70_external_source_pilot.py), [external source judge](src/p70_external_source_analyze.py), [independent source Actions](.github/workflows/p70_external_source.yml). The official external SciFact development+corpus SHA-256 are pinned against source drift. Four externally annotated claims (2 SUPPORT, 2 CONTRADICT) × I/R/H/RH × two provider bundles = **32** maximum model calls, manual dispatch only, one ecology, no constructed semantic null and no causal/transport p-value. An earlier manual launch executed all **32 actual calls**; its receipts have now been recovered without further spending. Push remains provider-free; a new paid run is neither required nor recommended.
- **Repository authority:** P69 `TECHNICAL_PILOT_HOLD` and `PAPER_CONSTRUCT_HOLD` persist. P70 is theory-open; the externally sourced pilot is exploratory, not independent multi-ecology replication. No bot authored commits or writeback.

### EPISTEME-P69 — frozen manuscript and measurement branch

**EPISTEME-P69 — Manuscript-Directed Representation-Effect Transport, Evaluation-Artifact Disentanglement, Independent Model-Family Replication, Held-Out Task-Ecology Validation & Publication-Readiness Court**

- **Priority:** strengthen the P53–P65 task-local representation effect into a publishable, carefully bounded result. Theoretical P5–P16–P68 and measurement P66–P67 are separate research tracks.
- **Historical evidence frozen:** P56 64/64 missingness completions (0/6 primary rejections); P59 4/4 completions (0/15 prospective transport tests and 16 observed operator reversals); P62 256/256 task-locality completions; P65 4/4 structural-location test completions.
- **Instrument:** `src/p69_task_factory.py` (4 mechanisms × 2 task variants × 16 R/T-controlled vertices × valid/null), `src/p69_witness_enumerator.py` and `src/p69_independent_scorer.py` (separate answer correctness from exact-minimal evidence grounding), `src/p69_retention_controls.py` (Critical/Recoverable/Null × Rich/Coarse/Sham: 1,152 offline packets), `src/p69_retention_selftest.py` (separate reference evaluator), and `src/p69_blind_adjudication.py` (preview vs private HMAC blind-release gate).
- **Hosted zero-call verification:** [P69 Actions #37779096105](https://github.com/WhoSia/EPISTEME/actions/runs/37779096105) and [#37779477761](https://github.com/WhoSia/EPISTEME/actions/runs/37779477761) both PASS. Main 256 task packets, separate canary 64 packets, 128 witness-deletion and 128 fabricated-rationale challenges. Second run also verified a complete 8,192-row *synthetic* prediction fixture; **no provider calls**.
- **Study authority:** `active/p69_paper_program.json` and `active/p69_manuscript_gate.md`; [P69 Notion](https://www.notion.so/3f3ef561cf92815a9b04fac128aeb28b).
- **Additional verified read-only Actions:** [#37782896510](https://github.com/WhoSia/EPISTEME/actions/runs/37782896510) PASS (1,152 retention controls, 1,152 independent rule decisions, 128 shotgun and 128 duplicate-ID attacks rejected); [#37784187535](https://github.com/WhoSia/EPISTEME/actions/runs/37784187535) PASS (72 public label-omitted preview cases and 72-case secret-HMAC synthetic preflight, no real secret or private key). Both zero provider calls.
- **Manuscript readiness:** [P69 paper blueprint](active/p69_manuscript_blueprint.md), [external ecology/inference court](active/p69_manuscript_readiness_court.md), and `src/p69_inference_sensitivity.py`, `src/p69_disjoint_prediction.py`. Four authored mechanism families permit a minimum **two-sided 0.125** signed-symmetry reference probability (not a randomized test). The A/B held-out task calibration/evaluation sensitivity is separately checked; [#37786022394](https://github.com/WhoSia/EPISTEME/actions/runs/37786022394) PASS.
- **Real science source custody:** [SciFact official release](https://github.com/allenai/scifact): 5,183 corpus abstracts, 300 development claims, 16 deterministically selected annotated contradiction claims. `src/p69_external_scifact.py`, `src/p69_scifact_matched.py`, `src/p69_scifact_receipt.py` validated 128 original and 128 same-document **equal-evidence-count** contrasts; [#37785745463](https://github.com/WhoSia/EPISTEME/actions/runs/37785745463) and [#37786579297](https://github.com/WhoSia/EPISTEME/actions/runs/37786579297) PASS. No raw SciFact data published in artifacts. Withholding gold evidence does **NOT** certify semantic null: independent review remains HOLD.
- **External annotation interface:** `src/p69_human_agreement.py` tests Cohen kappa, rationale set agreement and unresolved-case HOLD with **synthetic ratings only**; [#37786485235](https://github.com/WhoSia/EPISTEME/actions/runs/37786485235) PASS. No independent human/LLM grading data collected.
- **Paper gate:** the two variants per mechanism are parameterized by one compiler, NOT externally independent task ecologies. Status remains `PAPER_CONSTRUCT_HOLD`. Recoverable/sham controls now pass offline only; they are not in the hosted 8,192-call main design. Independent real-world instances and actual third-party masked scoring remain unavailable. Output-contract canary passed, but the subsequent 192-call measurement pilot is on HOLD. The 72-case prior artifact is **label-omitted preview, NOT securely blinded**; HMAC key custody is required for real release. Held-out predictive Brier scorer: `src/p69_predictive_analysis.py`. [Research court](active/p69_instrument_court.md).
- **Measurement workflows registered:** [four-slot provider canary](https://github.com/WhoSia/EPISTEME/actions/workflows/p69_canary.yml) (Groq GPT-OSS-120B and Gemini 3.5 Flash-Lite × strict schema/JSON object) and [192-slot instrumentation pilot](https://github.com/WhoSia/EPISTEME/actions/workflows/p69_instrument.yml). Both push **zero-call preflights passed**: [37791683578](https://github.com/WhoSia/EPISTEME/actions/runs/37791683578) and [37792215371](https://github.com/WhoSia/EPISTEME/actions/runs/37792215371). Those *historical push-only runs* skipped provider jobs; subsequent manually dispatched four-slot canary and 192-slot pilot have now actually executed. Only manual `workflow_dispatch` starts model calls. The pilot additionally requires a real SUCCESS canary artifact and EXACT matching HEAD SHA.
- **Science versus feasibility:** four canary slots + 192 pilot slots are **noninferential**, do not authorize the 8,192-call main experiment, and cannot be used as evidence of cross-task transport. No independent human annotations or new independent task-family replications yet. Research and execution gates: [provider measurement court](active/p69_provider_measurement_court.md), [pilot manifest](active/p69_instrument_pilot_manifest.json).
- **Next:** diagnose the actual 192-slot `TECHNICAL_PILOT_HOLD` before considering any new paid instrument run. The canary and pilot were both run at frozen HEAD `18cb018c`. Independently mask/annotate both internal and externally sourced evidence cases, secure truly independent task-family replication with adequate cluster-level inference, and separately freeze the scientific main analysis. The 8,192-call main design remains only a **ceiling**, not a launched experiment.
- **Governance:** all code commits on `main` attributed to WhoSia; Actions have `contents: read`, `actions: read` and do not commit. `github-actions[bot]` author/committer prohibited.

## Latest closed stage — EPISTEME-P68

**EPISTEME-P68 — Cross-Channel Falsification-Route Restoration, Independent Criticism Generation–Acceptance Separation, Retained-Evidence Sufficiency Controls, Held-Out Relational Grammar Transport, Output-Interface Causal Mediation & Scientific Identifiability of Epistemic Access Loss**

- **Final verdict (2026-10-08):** `CLOSED_SCOPED_FORMAL_CONSTRUCT_ONLY_BEHAVIORAL_NONPROMOTION`. Independent adversarial graph audit PASS; 12-world finite observation-equivalence/regret construction supported, no LLM behavioral or naturalistic claim. P67 384-call pilot has only preflight successes; original prospective dependency is preserved.
- **Scientific object:** retention-induced loss of *admissible* criticism plus the downstream keep-versus-restore decision, not a general JSON format-quality penalty.
- **P68 constitution:** `active/p68_constitution.json`; **R2 correction/court:** `active/p68_r2_identification_court.md`; **sealed final verdict:** `active/p68_closure_verdict.json`. Initial one-mechanism compiler is a historical R1 prototype, not paper-grade evidence.
- **R2 instrument:** 12 synthetic worlds across direct, two-hop and guarded relations; 3 retention projections and 2 alternative encodings; 72 blinded generation packets and 72 observation-transfer packets. Coarse is an actual subset of Rich; sham richness uses true but irrelevant facts, with normalized row counts 10/9/10.
- **Formal identification witness:** per mechanism, a critical and null world have alpha-equivalent Coarse observations yet distinct Rich observations; a downstream information-restoration decision has nonzero minimax regret under the coarse state. This synthetic construction and value-of-information bound are standard formal arguments, not new empirical evidence.
- **Execution boundary:** R2 code and tests are available in a separately reviewed download package but are not asserted to be installed in the GitHub source tree; GitHub connector blocked prior Python/workflow uploads. No Actions run for P68 is claimed.
- **Audited custody:** 36 graphs + 348 edge deletions + 636 true-edge additions + 360 permutations + 72 transfer tests; separate deterministic four-step KEEP/RESTORE demonstration (not observed behavior). Public sources and tests are [archived on Drive](https://drive.google.com/file/d/1iCekBvSjCpBqDPXoIAthuS1RJuCvsAVr/view) under verified SHA-256 `5f960eada983fa96c7b8f9fdb7bc481d317ef3c56815641047b7fe97e78a2012`. Private scoring key excluded.
- **Governance:** read-only Actions, no repository push/commit in workflows, and **never allow `github-actions[bot]` to author or commit**.

## Historical P67 (prerequisite)


**EPISTEME-P67 — Output-Contract-Induced Selective Observability and the Causal Identifiability of Falsification Behavior**

- **Status:** FOUNDATION COURT OPEN / NO NEW MODEL CALLS AUTHORIZED. Prior-art and design reconstitution first.
- P66 run `37712504043`: 12,288 calls, 835 technical failures, 834 JSON validation; frozen verdict `TECHNICAL_HOLD`. Technical failure is not semantic error.
- Reconnect to founding EPISTEME: P5 selective-observation identifiability, P10 endogenous criticism-space compression, P16 independent criticism generation, P19 provenance linkage+relation. The intended object is **which defeasible criticism remains expressible and machine-observable under response-channel constraints**, not generic JSON quality.
- Canonical: `active/p67_research_constitution.json`; [Notion P67](https://www.notion.so/3f3ef561cf92816d8f40c498ad156333).
- Prospective court: randomized structured/plain response channels with explicitly channel-dependent correctness, independent semantic scoring, positive/recoverable/null/sham controls and sharp missing-data bounds; construct-equivalence audit before any paid/provider execution.
- Fatal prior art: JSONSchemaBench, The Constraint Tax, selective labels, performative prediction and partial identification. **Do not promote novelty on validity/correctness tradeoffs alone.**
- Read-only GitHub Actions and exclusively human-authored commits. The `github-actions[bot]` contributor restriction is mandatory.
- **P67 zero-call court:** 827/835 P66 failures exposed bare `NONE` generation. Finite-ledger joint-correctness bounds: BH [0,256]/1536, BT [1361,1472]/1536. The BT–BH gap is **at least 1105/1536 (71.94 percentage points)** under every possible semantic completion; technical missingness alone cannot explain it. Do not overwrite P66's frozen `TECHNICAL_HOLD`.
- **P67 pilot frozen:** `active/p67_pilot_manifest.json`; `src/p67_channels.py`, `src/p67_pilot_worker.py`, `src/p67_pilot_analyze.py`, `src/p67_selftest.py`; workflow `.github/workflows/p67_pilot.yml`. Four tasks × eight vertices × two twins × two draws × three channels = **384-call maximum**. `schema` vs `json_object` share byte-identical prompt; `plain` has a different response-envelope instruction. The pilot only tests feasibility and has no independent scorer or inferential authority.
- **Zero-call Actions preflights:** [initial](https://github.com/WhoSia/EPISTEME/actions/runs/37724086135) and [full synthetic integration](https://github.com/WhoSia/EPISTEME/actions/runs/37724227380), both successful. Pilot calls are `workflow_dispatch` only; push can run preflight but no paid/model calls.
- **Source/court:** `active/p67_p66_offline_court.json`; `active/p67_identification_dossier.md`. Original Groq `seed` argument was not passed through `p42_reopen.groq_raw`; do not claim server-seeded repetition.


## Historical P66

**EPISTEME-P66 — Relational Evidence Binding Intervention, Target–Evidence Linkage, Evidence-Location Factorial Separation & Operator Transport Court**

- An explicitly target-linked decisive evidence record versus a cross-linked neutral record; history/terminal evidence placement crossed independently, with 3 lexical skins, 32 operator vertices, valid/null semantic twins, and 16 draws.
- P66 design is **precommitted before provider calls**; 12,288 calls are a budget/ceiling, not yet executed.
- Code: `src/p66_relational_binding.py`, `src/p66_task_worker.py`, `src/p66_analyze.py`; constitution: `active/p66_manifest.json`; manual Actions: `.github/workflows/p66.yml`.
- Preflight-only trigger is `active/p66_preflight_trigger.txt`. This push event never executes model-call shards; the model experiment is `workflow_dispatch` only.
- Analysis: conditional-oracle joint semantic accuracy, within-skin exact 13,824-label permutation tests, R/T Holm and strict A/B sign transport. P66 does **not** include an independent shadow scorer. Causal claims limited to this synthetic archive grammar.
- Research page: [Notion P66](https://www.notion.so/3f3ef561cf9281babe6ed0d4aea455a8).
- GitHub Actions remains read-only, creates artifacts only, and must **never** author or commit repository changes as `github-actions[bot]`.

## Historical closed P65

P64 recovered 289/303 failed P63 provider rows; 14 unresolved responses reduce to two unresolved joint-correctness bits and four admissible scientific worlds. All four worlds select `POST_P62_R_T_EFFECTS_REMAIN_TASK_LOCAL_UNDER_STRUCTURAL_INTERVENTION`. P65 scientifically CLOSED missingness-free; original P63 technical `TECHNICAL_HOLD` retained. Canonical `active/p65_result.json`.

## Historical P64

**EPISTEME-P64 — Structure-Conditioned Provider-Failure Localization, Failed-Cell-Only Recovery, Dual-Endpoint Completion Bounds, Frozen P63 Factorial-Court Reconstitution & Scientific Identifiability Adjudication**

- Source: P63 run `37563565663` at `7c86f0daa879c9f65e76afee75eab099f64082b5`.
- P63 execution: 48,849 technically successful rows / 49,152 total; 303 `json_validate_failed`; original scientific result `TECHNICAL_HOLD`.
- Correct failure localization: terminal-embedded **301**, history-externalized **2**; valid **302**, null **1**.
- P64 missingness-free theorem: strict R/T sign-transport is impossible for all admissible completions (RH2/RT2 R stopping effects both negative), so the two strongest P63 branches are excluded. Lower constitutional branch remains unresolved.
- Recovery specification: at most one unchanged-contract replay of each **303 failed identities**, no replay of the 48,849 successful rows; unchanged P63 scientific analyzer.
- Canonical: `active/p64_manifest.json`, `active/p64_failure_localization.md`, `active/p64_zero_call_bounds.md`; [Notion P64](https://www.notion.so/3f2ef561cf928116950bf0e8c280abdb).
- **Do not claim P64 recovery completed merely because recovery source code or workflow exists.**

## Historical closed P62

P60 prospectively tested whether the R/T operator-sign reversals surviving P59 could be predicted by the predeclared record/state × diagnostic/procedural context ontology. P61 recovered 250 of P60's 254 technical failures, leaving four unresolved cells.

P62 made **zero provider calls**. It enumerated all four logical `(primary_correct, shadow_correct)` states for each remaining cell: **16 primary equivalence classes × 16 shadow completions = 256 worlds**. No missingness probability model, weighting, or world exclusion was used.

Canonical P62:
- run: `37557274582`
- head: `a09439339a483f56cb810e2e2f55b5bd67f59f89`
- artifact: `11455476585`
- artifact digest: `sha256:24bd6e6f1847b2d116d0c715801210adabea5e4ca2c3c1770a61b8634b12ef3f`
- exact result JSON SHA-256: `55ca70c53d58efb752f6ac6e20dcfe793248b7b6b85c201f76ce9e41d28cc203`

All **256 / 256** completion worlds produced the same frozen P60 branch:

`P57_OPERATOR_REVERSAL_TASK_LOCAL_AT_TESTED_CONTEXT_RESOLUTION`

No completion entered the evaluation-artifact branch. Maximum possible primary↔shadow disagreement was 4 / 49,152 = 0.00814%, far below the frozen 10% artifact threshold.

The prospective carrier prediction failed robustly across the lattice:
- R stopping-time carrier contrast (state − record): **+1.6198 to +1.6458**, opposite the frozen negative prediction; p = **0.9025–0.9050**.
- T stopping-time carrier contrast: **−2.3802 to −2.3542**, opposite the frozen positive prediction; p = **1.0**.
- stopping-time Holm pattern: `00` in every primary completion.
- stopping-time strict-sign and critical-quadrant gates: **0 / 256 worlds pass**.
- behavioral Holm pattern: `01`; T fixed-horizon carrier contrast is positive and individually small-p, but behavioral strict and critical gates are also **0 / 256**, so it cannot rescue the frozen primary court.
- role-rival Holm pattern: `00`.

Therefore P60 is now scientifically closed missingness-free: the tested coarse context ontology does **not** compress the surviving R/T operator reversal into a transportable carrier-indexed sign law. At the tested resolution, the reversal remains task-local.

This is a falsification of the proposed record/state × diagnostic/procedural context law, not evidence for a structural record-versus-state carrier mechanism. The earlier construct-validity ceiling remains in force: P60 manipulated record-like versus state-like semantic/schema framing within a common archive skeleton.

Canonical seal: `active/p62_result.json`.

Repository writeback from Actions and `github-actions[bot]` authored/committer contributions remain forbidden.

## P64 source-retirement custody receipt

- Verified pre-retirement snapshot was uploaded to [Google Drive EPISTEME archive](https://drive.google.com/file/d/10zC0eDpejpfJvfyC82DevMLlSusnBGYk/view). It was captured by GitHub Actions run `37706177499`; artifact ID `11520240159`, GitHub artifact ZIP SHA-256 `974a2c8de66636e1eaf8540211743cc8810d3c1634aaae0ad26edbb46040d3e7`.
- Latest snapshot run `37707694891` **SUCCESS**, artifact ID `11520760658`; [Google Drive archival custody](https://drive.google.com/file/d/1E1ba6lmkLUUHJV3pY7AtQOBcsQlKuCz3/view) was downloaded back and byte-verified before retirement.
- **Retirement completed:** 91 historical Python files and five old workflows were retired in human-authored commit `cf3c267659bede500f0661339a426505bd041680`. `src` now retains exactly eight transitive P64 runtime modules; the two remaining workflows are `p64_recover.yml` and `p64_archive.yml`. All retired Git blob SHA values and historical workflow paths are in `active/p64_source_retirement_manifest.json`. Drive readback verified the latest archive SHA-256 `5346a38cbb928360a0714799d84bf605fd77a5a4467d26dfca6e30bc5f16375e`.
- The P64 recovery worker and `p64_recover.yml` are already on `main`; ZIP-based manual creation is not needed. The live worker now includes a zero-provider-call `--preflight-only` gate.
