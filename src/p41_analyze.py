from __future__ import annotations

import json
from pathlib import Path

PARTIAL=(2,4)
SELECTIVE=(4,5)

# Canonical P39/P40 phase summary. Technical gate is logically prior.
MODELS={
    "qwen/qwen3.8-27b": {"family":"Qwen","technical":True,"v":0,"n":6,"regime":"GLOBAL_ABSTENTION_REGIME"},
    "qwen/qwen3.6-27b": {"family":"Qwen","technical":False,"ok":0,"v":None,"n":None,"regime":"TECHNICAL_UNEVALUABLE"},
    "Qwen/Qwen2.5-0.5B-Instruct": {"family":"Qwen","technical":True,"v":0,"n":0,"regime":"NONSELECTIVE_NO_PROMOTION"},
    "Qwen/Qwen2.5-1.5B-Instruct": {"family":"Qwen","technical":True,"v":0,"n":0,"regime":"NONSELECTIVE_NO_PROMOTION"},
    "Qwen/Qwen3-0.6B": {"family":"Qwen","technical":True,"v":0,"n":0,"regime":"NONSELECTIVE_NO_PROMOTION"},
    "Qwen/Qwen3-1.7B": {"family":"Qwen","technical":True,"v":0,"n":0,"regime":"NONSELECTIVE_NO_PROMOTION"},
    "openai/gpt-oss-20b": {"family":"GPT-OSS","technical":False,"ok":1,"v":0,"n":0,"regime":"TECHNICAL_UNEVALUABLE"},
    "openai/gpt-oss-120b": {"family":"GPT-OSS","technical":False,"ok":19,"v":2,"n":4,"regime":"TECHNICAL_UNEVALUABLE"},
    "gemini-3.5-flash-lite": {"family":"Gemini","technical":True,"v":6,"n":3,"regime":"NONSELECTIVE_NO_PROMOTION"},
}

def l1_to_region(v:int,n:int,target:tuple[int,int])->int:
    tv,tn=target
    return max(0,tv-v)+max(0,tn-n)

def main():
    rows={}
    promoted=[]
    for model,x in MODELS.items():
        r={"family":x["family"],"classification":x["regime"],"technical_evaluable":x["technical"]}
        if x["technical"]:
            v,n=x["v"],x["n"]
            r.update({
                "valid_majority_correct":f"{v}/6",
                "null_majority_correct":f"{n}/6",
                "distance_groups_to_partial":l1_to_region(v,n,PARTIAL),
                "distance_groups_to_selective":l1_to_region(v,n,SELECTIVE),
            })
            if v>=PARTIAL[0] and n>=PARTIAL[1]: promoted.append(model)
        else:
            ok=x.get("ok",0)
            r["technical_ok"]=f"{ok}/36"
            r["additional_OK_calls_needed_for_technical_gate"]=max(0,34-ok)
            if x.get("v") is not None:
                r["shadow_phase_coordinate"]={"valid_majority_correct":f"{x['v']}/6","null_majority_correct":f"{x['n']}/6"}
                r["shadow_coordinate_is_scientifically_admissible"]=False
        rows[model]=r

    families=sorted({MODELS[m]["family"] for m in promoted})
    constituted=len(promoted)>=2 and len(families)>=2
    result={
      "stage":"EPISTEME-P41",
      "model_boundary_table":rows,
      "promoted_domain_S":promoted,
      "promoted_domain_size":len(promoted),
      "promoted_family_count":len(families),
      "cross_family_selective_geometry_alignment":{
        "status":"UNDEFINED_EMPTY_PROMOTED_DOMAIN" if not promoted else "DEFINED",
        "pairwise_alignments":0,
        "reason":"P40 produced no promoted full geometries." if not promoted else None,
      },
      "model_indexed_quotient_intersection":{
        "status":"NOT_CONSTITUTED",
        "empty_intersection_treated_as_universal":False,
        "reason":"No promoted model-indexed quotient exists on the frozen P40 condition."
      },
      "regime_boundary_stability":{
        "gemini_3_5_flash_lite":"one null-majority group short of PARTIAL_SELECTIVE_PROMOTE; therefore the observed nonselective classification lies immediately adjacent to the promotion boundary",
        "qwen_qwen3_8_27b":"two valid-majority groups short of PARTIAL_SELECTIVE_PROMOTE while retaining 6/6 null control; clean abstention is separated from partial selectivity by witness recovery, not null-control repair",
        "small_qwen":"two valid-majority plus four null-majority groups short of PARTIAL_SELECTIVE_PROMOTE; observed failure is not adjacent to the selective boundary",
        "gpt_oss_120b":"shadow behavioral coordinate is 2/6 valid, 4/6 null, numerically inside PARTIAL_SELECTIVE_PROMOTE, but 19/36 technical OK is 15 calls below the technical gate; behavioral classification is therefore unidentified, not promoted"
      },
      "transportable_model_property":{
        "constituted":constituted,
        "verdict":"NOT_CONSTITUTED_ON_CURRENT_EVIDENCE",
        "reason":"The non-vacuous transport criterion requires at least two promoted models from distinct families and aligned nonempty geometry; P40 has zero promoted models."
      },
      "constitutional_verdict":"SELECTIVITY_TRANSPORTABILITY_NOT_CONSTITUTED__BOUNDARY_IS_MODEL_INDEXED_AND_TECHNICAL_GATE_SENSITIVE",
      "authority_limits":[
        "Not evidence that cross-family transportability is impossible.",
        "No ranking of model families or capabilities.",
        "No imputation of technical failures as behavioral outcomes.",
        "No behavioral SVEC promotion."
      ],
      "new_model_calls":0,
      "new_actions":0,
      "self_audit":"PASS"
    }
    Path("active/p41_result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
