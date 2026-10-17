"""P75-P5 human-free final scientific closure: source-relative calculus and strong rival.

Licensed VitaminC text remains in pinned original external publisher and
private old/new Wikipedia editions. Twelve observations are assistant-coded
source-relative classifications from P75-P4, NOT external human-certified gold.

A finite restricted claim grammar and exact Fraction decision calculus
demonstrate:
 (a) source witness persistence and conflicting edits defeat latest-snippet
     as a reliable rule;
 (b) full historical source and same logic suffices for a competent ordinary
     bitemporal-PROV + decision rival, tying the P75 candidate (not novel);
 (c) different counterfactual world-truth and switch value are observationally
     equivalent even given true source bytes/version metadata.
No factual claim that a Wikipedia sentence is true of the external world.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from hashlib import sha256
import json

R3="7d96568480e87aec80ffb8be1d3002d5fb11920ac40a3f9fd5e57a176ac22e78"
# Source-relative judgments from label-blind assistant prior P4 audit:
# NOT independent externally certified truth labels, not twelve task ecologies.
RAW=(
("807b1886","TEMPORAL_SCOPE_HOLD"),
("04415cdd","SOURCE_SENTENCE_CANDIDATE"),
("60ce362d","SOURCE_INTERNAL_OBJECTION"),
("16cb1aa7","QUANTIFIER_DOMAIN_HOLD"),
("ac936220","SEMANTIC_BRIDGE_HOLD"),
("c080d9bb","SOURCE_SENTENCE_CANDIDATE"),
("875083b8","REFERENT_TIME_HOLD"),
("6f00e272","REFERENT_TECH_HOLD"),
("fe5c5fcd","CONFLICTING_SOURCE_INTERPRETATION"),
("3595446c","UNCHANGED_SEMANTIC_WITNESS"),
("b0a3fb87","REORDERED_NON_ENTAILMENT"),
("21f2025f","FULL_ARTICLE_WITNESS_PERSISTS"))
assert len(RAW)==12 and len(set(k for k,_ in RAW))==12
CANDIDATE={"SOURCE_SENTENCE_CANDIDATE"}

@dataclass(frozen=True)
class Atom:
    source_id:str
    revision:str
    valid_time:int
    record_time:int
    subject:str
    predicate:str
    obj:str
    proof_role:str
    polarity:int
    retained_full:bool
    retained_excerpt:bool

def evidence_at(atoms:tuple[Atom,...],asof:int,record_cutoff:int,
                subject:str,predicate:str,obj:str):
    """Restricted literal claim with explicit referent and proof role.
    No natural-language inference, external real-world fact, or proof of
    independent source truth is supplied by this mechanical filter.
    """
    available=[]
    for a in atoms:
        if a.valid_time>asof or a.record_time>record_cutoff:continue
        if (a.subject,a.predicate,a.obj)!=(subject,predicate,obj):continue
        if a.proof_role not in ("direct_claim","direct_defeater"):continue
        if a.retained_full:available.append(a)
    supports=[a for a in available if a.polarity==1 and a.proof_role=="direct_claim"]
    defeats=[a for a in available if a.polarity==-1 and a.proof_role=="direct_defeater"]
    if supports and not defeats:return "SOURCE_RELATIVE_SUPPORT",tuple(supports)
    if defeats and not supports:return "SOURCE_RELATIVE_DEFEAT",tuple(defeats)
    if supports and defeats:return "SOURCE_RELATIVE_CONFLICT",tuple(supports+defeats)
    return "SOURCE_RELATIVE_UNDETERMINED",tuple()

def simple_latest_snippet(a:tuple[Atom,...],cutoff:int)->bool:
    return any(z.valid_time<=cutoff and z.retained_excerpt and z.polarity==1 for z in a)

def strong_bitemporal_prov_rival(atoms,asof,record_cutoff,claim):
    """Existing conventional full-document, source/time/role-aware calculus.
    This is intentionally as strong as P75's finite grammar, not a strawman.
    """
    return evidence_at(tuple(atoms),asof,record_cutoff,*claim)[0]

def p75_conditional_warrant(atoms,asof,record_cutoff,claim):
    return evidence_at(tuple(atoms),asof,record_cutoff,*claim)[0]

def counterexamples():
    c=("a","is","b")
    common=dict(source_id="wiki-article",revision="v2",valid_time=2,
                record_time=3,subject="a",predicate="is",obj="b")
    # One paragraph drops reference but the SAME article infobox retains it.
    nickname=(
        Atom(**{**common,"revision":"v1","valid_time":1,"record_time":1},
             proof_role="direct_claim",polarity=1,retained_full=True,retained_excerpt=True),
        Atom(**common,proof_role="direct_claim",polarity=1,
             retained_full=True,retained_excerpt=False))
    assert simple_latest_snippet((nickname[-1],),3) is False
    assert p75_conditional_warrant(nickname,2,3,c)=="SOURCE_RELATIVE_SUPPORT"
    # A new author assertion and an explicitly coded contemporaneous defeater
    # cannot be used as a unanimous warrant. 'editor warning' is an authored
    # caution, not independently validated historical fact.
    dispute=(
        Atom(**common,proof_role="direct_claim",polarity=1,retained_full=True,retained_excerpt=True),
        Atom(**{**common,"source_id":"wiki-editor-comment"},proof_role="direct_defeater",
             polarity=-1,retained_full=True,retained_excerpt=False))
    assert simple_latest_snippet(dispute,3)
    assert p75_conditional_warrant(dispute,2,3,c)=="SOURCE_RELATIVE_CONFLICT"
    # Missing complete referent/quantifier/time -> no entailment from a
    # similarly phrased paragraph.
    wrong_scope=(
        Atom(**{**common,"obj":"b2"},proof_role="direct_claim",polarity=1,
             retained_full=True,retained_excerpt=True),)
    assert simple_latest_snippet(wrong_scope,3)
    assert p75_conditional_warrant(wrong_scope,2,3,c)=="SOURCE_RELATIVE_UNDETERMINED"
    # As-of vs record time: hindsight must not enter earlier decisions.
    later=Atom(**common,proof_role="direct_claim",polarity=1,retained_full=True,retained_excerpt=True)
    assert p75_conditional_warrant((later,),2,2,c)=="SOURCE_RELATIVE_UNDETERMINED"
    assert p75_conditional_warrant((later,),2,3,c)=="SOURCE_RELATIVE_SUPPORT"
    return {"full_page_witness_persists":True,
            "added_claim_with_defeater_is_conflict":True,
            "wrong_referent_not_entailment":True,
            "record_time_no_hindsight":True,
            "strong_rival_exactly_ties":all(
               strong_bitemporal_prov_rival(x,2,3,c)==p75_conditional_warrant(x,2,3,c)
               for x in (nickname,dispute,wrong_scope,(later,)))
           }

def admissible_action_conditional(lower:Q,upper:Q,k:Q,review:Q,
                                  review_observation_available:bool):
    """Worst-case expected *loss* for an explicitly hypothetical binary world.
    P(new-standard better)=p in [lower,upper]. Keep: p.
    Switch: 1-p+k. With a PERFECT FREE-OF-ERROR, costed extra test,
    Review: review+p*k. Not a human-review assumption.
    """
    if not 0<=lower<=upper<=1 or not 0<=k<=1 or review<0:raise ValueError("BAD_INTERVAL")
    losses={"KEEP":upper,"SWITCH":1-lower+k}
    if review_observation_available:losses["REVIEW"]=review+upper*k
    value=min(losses.values())
    choices=tuple(sorted(a for a,v in losses.items() if v==value))
    return losses,choices

def count_exact_decisions():
    intervals=((Q(0),Q(1)),(Q(1,4),Q(3,4)),(Q(4,5),Q(1)),
               (Q(0),Q(1,5)),(Q(1,2),Q(1,2)))
    costs=(Q(0),Q(1,4),Q(3,4))
    review_costs=(Q(0),Q(1,8),Q(1,2))
    cases=0;with_test=0;without_test=0; changed=0;ties=0
    for (l,u),k,r,exists in product(intervals,costs,review_costs,(False,True)):
        loss,c=admissible_action_conditional(l,u,k,r,exists)
        loss2,c2=admissible_action_conditional(l,u,k,r,False)
        assert all(type(v) is Q and v>=0 for v in loss.values())
        assert set(c).issubset(loss)
        if exists:with_test+=1
        else:without_test+=1
        if c!=c2:changed+=1
        if len(c)>1:ties+=1
        cases+=1
    assert cases==90 and with_test==without_test==45
    # Human review NOT needed; review is hypothetical **perfect information
    # acquisition** whose availability is an exogenous assumption.
    loss_no,a_no=admissible_action_conditional(Q(0),Q(1),Q(1,4),Q(1,8),False)
    loss_yes,a_yes=admissible_action_conditional(Q(0),Q(1),Q(1,4),Q(1,8),True)
    assert a_no==("KEEP",)
    assert a_yes==("REVIEW",)
    assert loss_no["KEEP"]==1 and loss_yes["REVIEW"]==Q(3,8)
    return {"grid_cases":cases,"test_available_cases":with_test,
            "test_unavailable_cases":without_test,
            "decision_changes_with_perfect_test_offer":changed,
            "action_tie_cases":ties,
            "missing_test_action":"KEEP","hypothetical_perfect_test_action":"REVIEW",
            "conditional_perfect_test_regret":str(Q(3,8))}

def source_underidentification():
    """Two indistinguishable source archives, opposed unobserved state."""
    immutable_public={"corpus":"VitaminC pinned","source_revision_commitment":R3,
                      "claim_version":"v2","wikipedia_metadata_valid":True,
                      "observed_source_relative_text":"SAME"}
    models=[
      {**immutable_public,"latent_world_truth":"NEW_BETTER","switch_gain":1},
      {**immutable_public,"latent_world_truth":"OLD_BETTER","switch_gain":-1}
    ]
    observable=lambda m:{k:v for k,v in m.items()
                         if k not in ("latent_world_truth","switch_gain")}
    assert observable(models[0])==observable(models[1])
    assert models[0]["switch_gain"]*models[1]["switch_gain"]<0
    return {"same_full_observed_archive_opposite_switch_value":True,
            "real_world_switch_value_identified":False,
            "possible_latent_welfare_gain_interval":[-1,1]}

def main():
    e=counterexamples()
    d=count_exact_decisions()
    u=source_underidentification()
    assert len(RAW)==12 and sum(v in CANDIDATE for _,v in RAW)==2
    assert e["strong_rival_exactly_ties"]
    # Full-scope conventional theory is adequate: no proprietary P75
    # improvement is established by this finite model.
    verdict={
       "court":"EPISTEME-P75-P5-ZERO-HUMAN-BOUNDED-FINAL",
       "status":"SOURCE_RELATIVE_COUNTEREXAMPLES_AND_CLASSICAL_ADEQUACY_PASS",
       "r3_source_lineage_commitment":R3,
       "actually_verified_original_source_families_inherited":12,
       "source_relative_single_sentence_hypotheses":2,
       "independent_externally_certified_semantic_proofs":0,
       "classic_full_source_bitemporal_prov_rival_defeated":False,
       "generic_full_source_rival_exact_ties":True,
       "counterexamples":e,"exact_fraction_grid":d,
       "observational_underidentification":u,
       "new_human_recruitment":0,"new_human_ratings":0,
       "paid_new_model_calls":0,
       "new_empirically_identified_switch_utility":False,
       "historical_human_p69_0of16_p70_0of16_p71_0of32_inactive":True,
       "claim_status":"P75_BOUNDED_SOURCE_MODEL_CLOSED_FUNDAMENTAL_REPLACEMENT_QUESTION_OPEN",
       "paper_novelty":"NOT_ESTABLISHED"
    }
    print(json.dumps(verdict,sort_keys=True,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
