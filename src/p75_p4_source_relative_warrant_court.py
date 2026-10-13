"""P75-P4 retrospective label-blind assistant source-relative semantic court.

Reads only PRIVATE, license-restricted P75-P3 original packets inside an
ephemeral runner; public JSON contains IDs and categorical judgments, never
original Wiki text, VitaminC claims, gold labels, or packet contents.

IMPORTANT: Categories are human-authored (assistant) case-specific analyses.
They are NOT externally independent blind human study adjudications and NOT
formal semantic entailment proofs. No paid provider or participant.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

STATUSES=(
 "HISTORICAL_SCOPE_HOLD",
 "ONE_SENTENCE_WITNESS_CANDIDATE",
 "MARKUP_REPAIRED_EDITOR_OBJECTION_HOLD",
 "CITATION_REPAIRED_QUANTIFIER_SCOPE_HOLD",
 "INSERTION_REPAIRED_SEMANTIC_GAP_HOLD",
 "ONE_SENTENCE_WITNESS_CANDIDATE",
 "ALBUM_REFERENT_SCOPE_HOLD",
 "ENERGY_TECH_REFERENT_HOLD",
 "SOURCE_INTERNAL_CONSISTENCY_HOLD",
 "SEMANTIC_WARRANT_UNCHANGED_CONTROL",
 "REORDERING_NOT_WARRANT_FOR_ACTION",
 "FULL_PAGE_WARRANT_PERSISTS_CONTROL",
)
REASONS=(
 "Prior role at first concert does not establish unqualified present group membership.",
 "New revised lead explicitly states the exact capital-city rank; parent does not.",
 "Added occupation token conflicts with an explicit contemporaneous Wikipedia editor caution.",
 "Source rank changed; the claim's 'locations' universe and time are not fixed.",
 "Insertion about a 'suitable' home does not prove subjective comfort or source reliability.",
 "Revised sentence explicitly includes the organizational agent missing in parent.",
 "A peak after an artist's death needs a uniquely identified album/chart and time scope.",
 "Solar PV plus battery storage differs from batteries themselves and may be indirect.",
 "Positive review characterization conflicts with cited low approval percentage; source not self-consistent.",
 "Added word 'adventures' did not establish a new materially different warrant.",
 "Word order changes but does not establish who left the person or when.",
 "Nickname still appears in unchanged infobox after the edited introductory phrase.",
)
CANDIDATES={1,5} # zero-indexed groups 2, 6; only source-relative, not certified.
ALIGNMENT_REPAIRS={
 2:"WIKITEXT_TEMPLATE_COMMENT_AND_LEAD",
 3:"HYPERLINK_AND_CITATION_CONTAMINATION",
 4:"INSERTED_MULTICLAUSE_PARAGRAPH",
}

def verify_condition(index,private):
    rows=private.get("publisher_rows_NO_REFERENCE_LABELS",[])
    if len(rows)<2 or any("label" in x for x in rows):
        raise ValueError("P75_P4_PUBLISHER_GOLD_LEAK_OR_MISSING")
    changes="\n".join(private.get("source_wikitext_changed_lines_PRIVATE_ONLY",[]))
    plus="\n".join(l for l in changes.splitlines() if l.startswith("+") and not l.startswith("+++"))
    old="\n".join(l for l in changes.splitlines() if l.startswith("-") and not l.startswith("---"))
    if index==2:
        assert "[[mathematician]]" in plus and "[[mathematician]]" not in old
        assert "Please do NOT add" in plus, "Explicit editor uncertainty warning must not be hidden"
    if index==3:
        assert "third most densely populated" in plus.lower()
        assert "[[Macau]]" in plus and "[[Monaco]]" in plus
        assert "second most densely populated" in old.lower()
    if index==4:
        assert "new homes in Somalia suitable" in plus
        assert "new homes in Somalia suitable" not in old
    if index==9:
        assert "adventures of" in plus
    if index==11:
        assert "nickname" in changes.lower() and "marcy" in changes.lower()
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--private-dir",required=True)
    ap.add_argument("--public-dir",required=True)
    args=ap.parse_args()
    files=sorted(Path(args.private_dir).glob("packet_*.json"))
    if len(files)!=12:raise ValueError("P75_P4_EXPECTED_FIXED_12_PRIVATE_SOURCE_PACKETS")
    out=Path(args.public_dir);out.mkdir(parents=True,exist_ok=True)
    results=[]
    for i,f in enumerate(files):
        pkt=json.loads(f.read_text())
        verify_condition(i,pkt)
        verdict=STATUSES[i]
        results.append({
         "index":i+1,
         "masked_group_id":pkt["group_id"],
         "source_relative_warrant_status":verdict,
         "review_reason_original_authored_paraphrase":REASONS[i],
         "prior_P3_alignment_category":pkt.get("source_alignment_quality","UNSPECIFIED"),
         "source_text_recovery":ALIGNMENT_REPAIRS.get(i,"P3_DIRECT_SOURCE_TEXT_PAIR"),
         "single_atom_provisional_candidate":i in CANDIDATES,
         "single_atom_minimality_proven":False,
         "blind_external_human_evaluation":False,
         "independent_historic_truth_established":False,
         "actual_policy_improvement_observed":False,
         "raw_original_text_in_public_output":False
        })
    if len({x["masked_group_id"] for x in results})!=12:raise ValueError("P75_P4_GROUP_DUPLICATED")
    summary={
     "stage":"EPISTEME_P75_P4_LABEL_BLIND_SOURCE_RELATIVE_WARRANT",
     "status":"SOURCE_TEXT_REPAIRS_3_ORIGIN_CASES_AND_ADVERSARIAL_SEMANTIC_SCREEN_PASS",
     "original_r3_groups_preserved":12,
     "publisher_reference_labels_seen_during_case_review":False,
     "prior_direct_alignment":9,"prior_partial_alignment":1,"prior_no_alignment":2,
     "three_string_alignment_problems_mechanically_located":3,
     "source_relative_one_atom_candidates":len(CANDIDATES),
     "editorial_or_referent_or_semantic_holds":12-len(CANDIDATES),
     "independent_external_human_warrant_certifications":0,
     "actual_minimum_sufficient_proofs":0,
     "new_provider_model_calls":0,
     "author_coded_review":"ASSISTANT_REASONED_NOT_EXTERNAL_BLIND_GOLD",
     "original_claims_or_evidence_exposed_in_public_receipt":False
    }
    (out/"public_source_semantic_audit.json").write_text(
      json.dumps({"summary":summary,"results":results},indent=2,ensure_ascii=False)+"\n")
    print("P75_P4_LABEL_BLIND_12_SOURCE_REVIEW_PASS")
    print("P75_P4_THREE_ORIGINAL_STRING_ALIGNMENT_REPAIR_LOCATED")
    print("P75_P4_PROVISIONAL_ONE_ATOM_CANDIDATES "+str(len(CANDIDATES)))
    print("P75_P4_EXTERNAL_HUMAN_GOLD=0 MINIMAL_PROOF=0")

if __name__=="__main__":main()
