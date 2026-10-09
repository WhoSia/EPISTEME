"""P70: typed partial bridge between SciFact rationale and AVeriTeC QA evidence.

This is a constructive *common metadata quotient*, not a verified homomorphism
of entailment, minimal proof sets or model behavioral effects.
"""
from __future__ import annotations
from dataclasses import dataclass
import json

POLARITIES={"SUPPORT","CONTRADICT"}
ORIGINS={"SCIFACT_SENTENCE","AVERITEC_QA"}

class BridgeHold(ValueError):
    pass

@dataclass(frozen=True)
class EvidenceAtom:
    origin: str
    role: str
    text: str
    polarity: str
    source_reference: str
    claim_time: str|None = None
    evidence_time: str|None = None
    depends_on:tuple[str,...]=()
    needs_external_context:bool=False
    def audit(self):
        if self.origin not in ORIGINS or self.polarity not in POLARITIES:
            raise BridgeHold("P70_UNSUPPORTED_SOURCE_OR_POLARITY")
        if not self.role or not self.text or not self.source_reference:
            raise BridgeHold("P70_MISSING_ROLE_OR_SOURCE")

@dataclass(frozen=True)
class MechanismQuotient:
    sign: str
    provenance_present: bool
    temporal_scope_certified: bool
    dependency_free: bool
    outside_context_required: bool
    # Deliberately do NOT include the raw document-/QA-specific language.

def common_quotient(atom:EvidenceAtom,*,time_certified:bool=False)->MechanismQuotient:
    atom.audit()
    return MechanismQuotient(
        sign=atom.polarity,
        provenance_present=bool(atom.source_reference),
        temporal_scope_certified=bool(time_certified),
        dependency_free=not bool(atom.depends_on),
        outside_context_required=atom.needs_external_context,
    )

def classify(source:EvidenceAtom,target:EvidenceAtom, *,
             source_packet_truth_certified:bool=False,
             target_packet_truth_certified:bool=False,
             reviewer_proof_bijection_certified:bool=False,
             independent_dependency_audit:bool=False)->dict:
    s=common_quotient(source)
    t=common_quotient(target)
    shared={
        "sign_common":s.sign==t.sign,
        "provenance_schema_present":s.provenance_present and t.provenance_present,
        "source_evidence_roles_distinct":source.origin!=target.origin,
        "graph_source_dependency_free":s.dependency_free,
        "graph_target_dependency_free":t.dependency_free,
        "external_context_needed":s.outside_context_required or t.outside_context_required,
    }
    if not shared["sign_common"]:
        return {"verdict":"POLARITY_MISMATCH", "shared":shared,
                "transport_effect_identified":False}
    if not shared["provenance_schema_present"]:
        return {"verdict":"SOURCE_PROVENANCE_HOLD","shared":shared,
                "transport_effect_identified":False}
    fully_certified=(
        source_packet_truth_certified and target_packet_truth_certified
        and reviewer_proof_bijection_certified and independent_dependency_audit
        and s.dependency_free and t.dependency_free
        and not shared["external_context_needed"]
        and s.temporal_scope_certified and t.temporal_scope_certified
    )
    # Time is intentionally NOT certified by default; a matching time string
    # or dataset label cannot prove absence of temporal leakage.
    return {
        "verdict":"REVIEWED_PARTIAL_DEPENDENCY_BRIDGE" if fully_certified
                  else "SHARED_POLARITY_AND_PROVENANCE_QUOTIENT_ONLY",
        "shared":shared,
        "semantic_dependency_certificate":"CHECKED" if fully_certified else "HOLD",
        "proof_set_bijection":"EXTERNAL_CERTIFICATE" if fully_certified else "HOLD",
        "transport_effect_identified":False,
    }

def intervention_court(source:list[EvidenceAtom],target:list[EvidenceAtom], *,
                       source_h_safe:bool=False,target_h_safe:bool=False,
                       human_packet_reviews:bool=False)->dict:
    for a in source+target:a.audit()
    # R is syntax-preserving only if used exclusively as nonsemantic handles:
    # an evidence_id embedded inside answer text invalidates R equivalence.
    r_syntactic=all(a.role and a.role not in a.text for a in source+target)
    # H changes display order. Even a bag of equal evidence atoms need not
    # preserve human QA reading dependencies or model decision behavior.
    h_syntactic=all(not a.depends_on for a in source+target)
    return {
        "R_syntactic_alpha_equivalence":r_syntactic,
        "R_semantic_equivalence":"REVIEW_HOLD" if not human_packet_reviews else "CANDIDATE_ONLY",
        "H_evidence_multiset_preservation":True,
        "H_dependency_invariance":"REVIEW_HOLD" if not
           (source_h_safe and target_h_safe and h_syntactic and human_packet_reviews)
           else "INDEPENDENT_CERTIFICATE_REQUIRED",
        "model_decision_invariance":"NOT_PROVEN",
        "cross_ecology_effect":"NOT_IDENTIFIED",
    }

def synthetic_countercourt():
    source=EvidenceAtom("SCIFACT_SENTENCE","s1","Evidence supports outcome",
                        "SUPPORT","paper:sentence4")
    target=EvidenceAtom("AVERITEC_QA","q1","Retrieved answer supports outcome",
                        "SUPPORT","website:q1")
    reduced=classify(source,target)
    assert reduced["verdict"]=="SHARED_POLARITY_AND_PROVENANCE_QUOTIENT_ONLY"
    assert not reduced["transport_effect_identified"]
    assert classify(source,EvidenceAtom("AVERITEC_QA","q2","Answer refutes outcome",
                              "CONTRADICT","website:q2"))["verdict"]=="POLARITY_MISMATCH"
    dependent=EvidenceAtom("AVERITEC_QA","q2","Yes it was, as above",
                            "SUPPORT","website:q2",depends_on=("q1",))
    assert classify(source,dependent)["verdict"]=="SHARED_POLARITY_AND_PROVENANCE_QUOTIENT_ONLY"
    assert intervention_court([source],[dependent])["H_dependency_invariance"]=="REVIEW_HOLD"
    temporal=EvidenceAtom("AVERITEC_QA","q3","Appointment outcome",
                          "SUPPORT","website:q3",claim_time="2020-10-08",
                          evidence_time="2021-02-15",needs_external_context=True)
    assert classify(source,temporal)["semantic_dependency_certificate"]=="HOLD"
    object_mismatch=EvidenceAtom("AVERITEC_QA","q4","Physical object preserved",
                         "CONTRADICT","website:q4",needs_external_context=True)
    assert classify(source,object_mismatch)["verdict"]=="POLARITY_MISMATCH"
    assert intervention_court([source],[target])["R_syntactic_alpha_equivalence"]
    role_used_in_semantics=EvidenceAtom("AVERITEC_QA","q5","q5 is assigned the verdict",
                                      "SUPPORT","website:q5")
    assert intervention_court([source],[role_used_in_semantics])["R_syntactic_alpha_equivalence"] is False
    return {"toy_counterworlds":5,"one_typed_partial_quotient":True,
            "real_source_human_bridges":0,
            "transport_results":0,
            "authority":"FORMAL_COUNTERMODEL_ONLY"}

if __name__=="__main__":
    z=synthetic_countercourt()
    print("P70_PARTIAL_BRIDGE_SELFTEST_PASS toy_counterworlds="+str(z["toy_counterworlds"])+" human_bridge_pass=0 provider_calls=0")
