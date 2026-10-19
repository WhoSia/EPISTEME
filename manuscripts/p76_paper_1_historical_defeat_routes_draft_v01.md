# Paper 1 — The Afterlives of Scientific Evidence: Recovery, Restricted Reanalysis, and the Boundaries of Archival Sufficiency

**EPISTEME Writing Loop 1 — Draft v0.1, 2026-10-20. NOT SUBMISSION READY.**  
**Type:** historically grounded comparative methods paper.  
**Status:** SOURCE-SUPPORTED CASE DESCRIPTIONS / CROSS-CASE MECHANISM UNPROVEN / PAPER HOLD.

## Abstract

A scientific record can outlive the experimental environment that once made it intelligible. Conversely, the disappearance of a digital file need not end the ability to reconstruct the measurement to which it refers. These possibilities complicate familiar claims that data preservation is equivalent to the preservation of scientific evidence. We examine three historical high-energy-physics archives in which the relation between stored records and possible future analyses is unusually explicit. The JADE collaboration reconstructed missing luminosity information from a surviving paper printout and a retained checking program. An ALEPH policy distinguished the retention of archived collision data, simulation and software from the ability to repeat several precision analyses. DELPHI's 2024 preservation policy describes a modernized software stack and accessible data alongside diminishing specialist knowledge about detector and run conditions. These cases cannot establish an adoption-induced irreversible loss of scientific verifiability. They do, however, motivate a query-specific account of archival sufficiency: the question is not whether 'the data' survived, but whether an identified scientific analysis can be justified with the records, calibration dependencies, executable procedures and expertise still available. We propose an adversarial protocol for distinguishing recoverable omission, technical non-executability, interpretive underdetermination, authorized-use restrictions and irreversible evidential loss. Its comparative predictions remain open to direct analysis-level audit.

## 1. The file that was not enough

An archive is normally described by what it contains. A directory of detector events, a software release and a document collection can all be inventoried and assigned checksums. But the scientific use of an archive is not a single operation. One physicist may wish to redraw an event distribution; another may wish to re-estimate a calibrated cross section; a third may ask whether a historical hypothesis was fairly excluded once correlated systematic uncertainties are reconsidered. The same collection can suffice for the first and not for the latter two.

This difference is easily obscured by the opposition between preservation success and preservation failure. Both labels are too coarse. A file that no longer exists online may be recoverable from paper. A data file whose bytes remain untouched may no longer support a justified replication of a precision result if its uncertainty model, run conditions or tacit checks have not survived.

Our question is accordingly narrow: what evidence would warrant the statement that a *specified scientific verification route* survived, failed, or was repaired? This is not the broader claim that knowledge is locked into a local optimum. Previous research on data preservation, infrastructure and scientific path dependence has already recognized many of the relevant vulnerabilities.

## 2. What the cases actually tell us

### 2.1 JADE: restoration from an independent witness

Bethke and Wagner's historical account of JADE describes efforts to revive data and software from the PETRA experiment. A set of run-level integrated-luminosity values needed for cross-section work was absent from the routine surviving electronic holdings. An old paper printout was found and entered manually. Crucially, a retained checking routine identified five transcription errors, which were corrected. The recovery mechanism was neither digital redundancy alone nor free reconstruction from physical theory. It combined a non-digital witness, continuing human attention and executable historical verification.

This is a counterexample to an unqualified claim of permanent loss from a missing digital object. It is *not* by itself proof that any particular later JADE event-shape determination of the strong coupling constant used the restored luminosity entries. Event-shape analyses may use normalized distributions with different dependencies. To test a causal claim about the recovered values, we must locate one published absolute cross-section result and its original input-processing chain.

### 2.2 ALEPH: explicit limits on precision reproduction

The ALEPH Collaboration's December 2003 archival statement reports that reconstructed data, final simulation and analysis software were retained. Yet it identifies specific analyses that cannot be repeated on the archived material, especially where systematic effects are decisive. Named examples include the Z lineshape, W mass and tau polarization. This is an unusually informative exclusion statement because it names analyses rather than treating 'scientific utility' as a single binary property.

The policy cannot substitute for a contemporary independent execution attempt. Its meaning also depends on the institutional date: changes in software, additional documentation, or recovered expert knowledge after 2003 might alter what can be done now. The immediate research task is to isolate what particular uncertainty, calibration or run-condition dependency the retained collection fails to support in one chosen precision analysis.

### 2.3 DELPHI: executable access and warranted inference

DELPHI's 2024 preservation policy and documentation describe surviving data, a conditions database and a modernized analysis environment. Nevertheless, the collaboration warns that high-precision analyses have become difficult to reproduce as detailed knowledge of detector and run conditions disappears. This is evidence of an institutional assessment about analysis-level scientific warrant, not a proof that DELPHI data are unreadable or that all contemporary physics reanalysis is impossible.

The relevant contrast is not digital data versus no data. It is basic access and computation versus the grounds needed to defend a particular precision inference.

## 3. A query-relative archival sufficiency test

Let q be a predeclared scientific question. A useful evidence description separates (i) recorded observations D; (ii) measurement, calibration and uncertainty context C; (iii) an executable and inspectable analysis procedure P; (iv) independent contextual witnesses W; and (v) institutional or scientific authorization A.

We say that q is *currently auditable* only if a specified analyst can identify a legitimate reconstruction using the surviving evidence and articulate its assumptions and uncertainty. This is not a theorem about an absolute archive: the evidence set depends on discovery and restoration. An incomplete present search cannot establish permanent loss.

We therefore distinguish five reporting states: VERIFIED_REPLAY, RESTORED_WITH_INDEPENDENT_WITNESS, QUERY_INSUFFICIENCY_REPORTED, TECHNICAL_OR_INSTITUTIONAL_HOLD and NOT_IDENTIFIED. Categories are audit labels, not newly discovered natural laws. They must not be conflated with physical non-identifiability without analysis-specific proofs.

## 4. What would defeat this account?

Strong existing data-preservation scholarship already argues for maintaining software, documentation, provenance and expert knowledge. If established DPHEP methodology fully explains the cases and provides the same operational distinctions, our work is a synthesis rather than a novel theory. If accessible ALEPH or DELPHI workflows now replicate the supposedly excluded measurements with authenticated uncertainty controls, apparent deficits must be revised. If the JADE paper was not causally required by the chosen published cross section, that proposed witness link must be abandoned.

For each case, the decisive next step is therefore an individual scientific query and a recoverability audit, not another summary of archival fragility.

## 5. Discussion

JADE's story is easy to romanticize as the rescue of lost knowledge. It is more informative when read conservatively: the relevant record survived because an unexpected combination of material and procedural witnesses remained available. ALEPH cautions against judging the scientific future from a list of digital assets. DELPHI indicates that software modernization can succeed while justified high-precision inference remains difficult. Together they illustrate why an archive's continuity should be evaluated at the level of scientific questions.

What they do not show is the distinctive EPISTEME proposition that institutional adoption of one knowledge infrastructure caused the systematic disappearance of evidence capable of overturning a superior rival. That claim needs a documented adoption history, an independently authorized rival-discriminating scientific question, and a credible counterfactual. We leave it open.

## References and source custody

- Bethke, S. & Wagner, A. (2022), JADE experiment history and revival. https://doi.org/10.1140/epjh/s13129-022-00047-8
- ALEPH Collaboration (2003), Statement on the use of ALEPH data for long-term analyses. https://dphep.web.cern.ch/sites/default/files/archive_data.pdf
- DELPHI Collaboration (2024), Data preservation, re-use and open access policy. https://doi.org/10.7483/OPENDATA.DELPHI.0X8O.FBUH
- CERN DELPHI documentation and preservation portal. https://opendata.web.cern.ch/docs/about-delphi

## Next writing loop

Choose and verify one published *luminosity-dependent JADE cross section*, one ALEPH Z-lineshape uncertainty dependency and one DELPHI precision-analysis constraint. Trace primary input-to-claim links rather than repeating preservation narratives. Audit DPHEP and provenance prior art at the mechanism level. **Paper hold.**
