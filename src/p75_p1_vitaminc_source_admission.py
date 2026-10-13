"""P75-P1: authentic external VitaminC TRAIN-preview metadata admission.

Only IDs/labels/revision references from actual Hugging Face public viewer,
the authors' official repo licence, and repository file-manifest hashes.
Original dataset file bytes and Wikipedia edits have NOT been independently
downloaded/hashed; reference labels are not new human warrant labels.
No third ecology outcome, no model call, no reviewers recruited.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
import json
import re

HF_DATASET="tals/vitaminc"
HF_REPOSITORY_COMMIT="be6febb761b0b2807687e61e0b5282e459df2fa0"
# SHA-256 values below are producer PUBLISHED Xet large-file metadata,
# NOT cryptographic hashes computed here from retrieved original full bytes.
PUBLISHED_TRAIN_SHA256="7461c6fd1a13459590317c5ccdc8651dd2daf7c1ad8ae4b10ccd88d164fccd5a"
PUBLISHED_DEV_SHA256="544934677f5d133873e6d38f4557f8966f4efa5d3d70874ffe6913f2091b86b5"
PUBLISHED_TEST_SHA256="7ad1808dbc30c62e0a1427a53022d0dfaff668a1fde3c4b612a2d266edd753ad"
SOURCE_VIEWER="https://huggingface.co/datasets/tals/vitaminc"
DATA_LICENSE="https://github.com/TalSchuster/VitaminC/blob/main/DATA_LICENSE"
ORIGINAL_PAPER="https://aclanthology.org/2021.naacl-main.52.pdf"

LABELS={"SUPPORTS","REFUTES","NOT ENOUGH INFO"}

@dataclass(frozen=True)
class PublicSourceGroup:
    page: str
    case_id: str
    revision_id: str
    revision_type: str
    # Curated short metadata only; raw copyrighted claim/evidence text stays
    # at licensed original dataset source, not in open GitHub.
    labels: tuple[str, str, str, str]
    split: str = "train"
    full_original_bytes_verified: bool = False
    independent_wikipedia_revision_verified: bool = False
    independently_adjudicated_warrant: bool = False


def public_preview() -> tuple[PublicSourceGroup,...]:
    # Exactly two unrelated case groups actually visible in original
    # Hugging Face public TRAIN viewer at source readback, not a random sample.
    return (
        PublicSourceGroup(
            page="Manchester",
            case_id="5ec5598dc9e77c000842c3cd",
            revision_id="925488060",
            revision_type="real",
            labels=("SUPPORTS","NOT ENOUGH INFO","NOT ENOUGH INFO","SUPPORTS")),
        PublicSourceGroup(
            page="Defy Media",
            case_id="5ec7d50dc9e77c00084418c7",
            revision_id="567579153",
            revision_type="real",
            labels=("NOT ENOUGH INFO","REFUTES","NOT ENOUGH INFO","SUPPORTS")),
    )


def validate_public_metadata(groups:tuple[PublicSourceGroup,...]) -> None:
    if not groups or len({g.case_id for g in groups}) != len(groups):
        raise ValueError("P75_SOURCE_GROUPS_EMPTY_OR_DUPLICATE")
    if len({g.revision_id for g in groups}) != len(groups):
        raise ValueError("P75_REVISION_ID_OVERLAP")
    if len({g.page for g in groups}) != len(groups):
        raise ValueError("P75_SOURCE_PAGE_LEAKAGE")
    for g in groups:
        if (g.split!="train" or g.revision_type!="real"
            or not re.fullmatch(r"[0-9a-f]{24}",g.case_id)
            or not re.fullmatch(r"[0-9]+",g.revision_id)):
            raise ValueError("P75_WRONG_PREVIEW_SPLIT_OR_REVISION_TYPE")
        if len(g.labels)!=4 or not set(g.labels).issubset(LABELS):
            raise ValueError("P75_BAD_DATASET_LABELS")
        if g.full_original_bytes_verified or g.independent_wikipedia_revision_verified or g.independently_adjudicated_warrant:
            raise ValueError("P75_FORBIDDEN_SOURCE_AUTHORITY_PROMOTION")
    assert len(PUBLISHED_TRAIN_SHA256)==len(PUBLISHED_DEV_SHA256)==len(PUBLISHED_TEST_SHA256)==64


@dataclass(frozen=True)
class EvidenceWitnessLayout:
    group_id: str
    source_revision_id: str
    condition: str
    # Witness must remain in retained trace *and* referenced in relations.
    # This is abstract admission metadata, never raw license-bound evidence.
    retained_trace_refs: tuple[str,...]
    relation_refs: tuple[str,...]
    minimal_evidence_refs: tuple[str,...]
    extra_decoy_refs: tuple[str,...]


def matched_recoverability(full:EvidenceWitnessLayout, positive:EvidenceWitnessLayout)->bool:
    if (full.group_id!=positive.group_id or full.source_revision_id!=positive.source_revision_id
        or full.condition!="FULL" or positive.condition!="RECOVERABLE"
        or not full.minimal_evidence_refs or not positive.minimal_evidence_refs):
        return False
    target=set(full.minimal_evidence_refs)
    # Preserve exact referent identity and the actual positions *where a
    # recipient can access it*. Relations alone are NOT a matched control.
    return (
        target==set(positive.minimal_evidence_refs)
        and target.issubset(full.retained_trace_refs)
        and target.issubset(full.relation_refs)
        and target.issubset(positive.retained_trace_refs)
        and target.issubset(positive.relation_refs)
        and not target.intersection(positive.extra_decoy_refs)
    )


def required_independent_human_warrant_fields()->tuple[str,...]:
    # The evaluator/packet author may not self-certify the signature.
    return (
        "masked_packet_sha256", "claim_group_id", "source_revision_id",
        "evidence_condition", "claim_label_independently_judged",
        "original_page_access_limitations", "candidate_minimal_evidence_ids",
        "necessity_after_each_atom_removed", "sufficiency_without_decoys",
        "other_valid_minimal_proof_sets", "claim_temporal_role",
        "reviewer_pseudonym", "external_custodian_verified_reviewer_identity",
        "decision_KEEP_SWITCH_REVIEW", "decision_confidence",
        "decision_cost_assumptions", "unresolved_ambiguity_flags",
    )


def negative_test(fn, marker):
    try:fn()
    except ValueError as e: assert marker in str(e),str(e)
    else:raise AssertionError("P75_UNSAFE_ACCEPTANCE_"+marker)


def self_test():
    groups=public_preview()
    validate_public_metadata(groups)
    assert len(groups)==2 and len({g.page for g in groups})==2
    assert sum(len(g.labels) for g in groups)==8
    assert all(g.revision_type=="real" and g.split=="train" for g in groups)
    assert any(len(set(g.labels))>1 for g in groups)
    assert len(required_independent_human_warrant_fields())==17
    base=EvidenceWitnessLayout(
        groups[0].case_id,groups[0].revision_id,"FULL",
        ("article-1:sentence-8",),("article-1:sentence-8",),
        ("article-1:sentence-8",),("article-1:sentence-9",))
    positive=replace(base,condition="RECOVERABLE")
    assert matched_recoverability(base,positive)
    assert not matched_recoverability(base,replace(
        positive,retained_trace_refs=("article-1:summary-A",)))
    assert not matched_recoverability(base,replace(
        positive,minimal_evidence_refs=("article-1:sentence-9",)))
    assert not matched_recoverability(base,replace(
        positive,extra_decoy_refs=("article-1:sentence-8",)))
    negative_test(lambda:validate_public_metadata(groups+(groups[0],)),
                  "SOURCE_GROUPS_EMPTY_OR_DUPLICATE")
    negative_test(lambda:validate_public_metadata((groups[0],replace(
        groups[1],revision_id=groups[0].revision_id))),"REVISION_ID_OVERLAP")
    negative_test(lambda:validate_public_metadata((replace(
        groups[0],split="test"),groups[1])),"WRONG_PREVIEW_SPLIT")
    negative_test(lambda:validate_public_metadata((replace(
        groups[0],independent_wikipedia_revision_verified=True),groups[1])),
                  "FORBIDDEN_SOURCE_AUTHORITY_PROMOTION")
    negative_test(lambda:validate_public_metadata((replace(
        groups[0],labels=("WRONG","REFUTES","REFUTES","SUPPORTS")),groups[1])),
                  "BAD_DATASET_LABELS")
    return {
        "stage":"P75_P1_VITAMINC_EXTERNAL_SOURCE_METADATA_GATE",
        "status":"REAL_EXTERNAL_ORIGINAL_DATASET_METADATA_RECONCILED_NOT_FULL_SOURCE_ADMITTED",
        "original_paper_read_from_primary_venue":True,
        "author_repo_readme_and_license_inspected":True,
        "hf_repo_commit_manifest_pinned":HF_REPOSITORY_COMMIT,
        "dataset_files_published_sha256":{
            "train":PUBLISHED_TRAIN_SHA256,"dev":PUBLISHED_DEV_SHA256,
            "test":PUBLISHED_TEST_SHA256},
        "complete_dataset_file_bytes_retrieved_and_hashed_here":False,
        "public_train_preview_source_groups":len(groups),
        "public_train_preview_dataset_rows":sum(len(g.labels) for g in groups),
        "distinct_wikipedia_revision_ids_reported_by_dataset":len(groups),
        "independent_source_revision_authentication":False,
        "read_back_source_group_ids":[g.case_id for g in groups],
        "eligible_test_or_human_holdout_claims":0,
        "matched_recoverable_witness_formal_positive_control":"PASS_SYNTHETIC_LAYOUT_ONLY",
        "blind_human_review_packets_authoritatively_certified":0,
        "genuine_independent_human_judgments":0,
        "switch_utility_observations":0,
        "new_paid_model_calls":0,
        "scientific_mechanism_transport":"HOLD"
    }


if __name__=="__main__":
    print(json.dumps(self_test(),indent=2,sort_keys=True))
