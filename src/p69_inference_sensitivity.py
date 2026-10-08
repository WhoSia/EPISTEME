"""P69 paper-level inferential sensitivity court, provider-free.

NOT a significance certification: there are only four hand-authored mechanism
clusters. Sign-flip reference p-values assume symmetry, not guaranteed randomization.
"""
from __future__ import annotations
import itertools,json,math,tempfile
from pathlib import Path
from p69_predictive_analysis import MODELS,CHANNELS,FAMILIES,TASKS,VERTICES,DRAWS,full_input,report,fixture

def signflip_reference(values):
    """One- and two-sided signed-symmetry REFERENCE distributions for n clusters."""
    if not values:raise ValueError("no clusters")
    observed=sum(values)/len(values)
    reference=[sum(sign*v for sign,v in zip(signs,values))/len(values)
               for signs in itertools.product((-1,1),repeat=len(values))]
    eps=1e-12
    positive=sum(z>=observed-eps for z in reference)/len(reference)
    negative=sum(z<=observed+eps for z in reference)/len(reference)
    two=min(1.0,2*min(positive,negative))
    return {"effect_mean":observed,"n_independent_mechanisms_assumed":len(values),
            "reference_support":len(reference),"one_sided_positive":positive,
            "one_sided_negative":negative,"two_sided":two,
            "authority":"SIGNED-SYMMETRY SENSITIVITY ONLY; no randomized mechanism sign labels."}

def family_summary(full,loss_margin=0.02):
    m=report(full)
    by={}
    for model,channel in itertools.product(MODELS,CHANNELS):
        means=[]
        for family in FAMILIES:
            p=[z["improvement"] for z in m["heldout_predictions"]
               if z["model"]==model and z["channel"]==channel and z["heldout_family"]==family]
            assert len(p)==2
            means.append(sum(p)/2)
        test=signflip_reference(means)
        test["family_improvements"]={name:val for name,val in zip(FAMILIES,means)}
        test["practical_margin"]=loss_margin
        test["uniformly_above_margin"]=all(v>loss_margin for v in means)
        test["uniformly_below_margin"]=all(v<loss_margin for v in means)
        by[model+"|"+channel]=test
    return by

def twin(full,model,task,vertex,channel,draw,endpoint="grounded"):
    pair=[full[(model,task,vertex,s,channel,draw)] for s in ("valid","null")]
    if endpoint=="grounded":
        vals=[r["format_valid"] and r["semantic_correct"] is True for r in pair]
    else:
        if any("answer_correct" not in r for r in pair):
            raise ValueError("P69_V2_ANSWER_FIELDS_REQUIRED")
        vals=[r["format_valid"] and r["answer_correct"] is True for r in pair]
    return int(all(vals))

def signed_half_effects(full,endpoint="grounded"):
    output={}
    for model,channel,task in itertools.product(MODELS,CHANNELS,TASKS):
        family=task.rsplit("_",1)[0]
        trial={}
        for block,draws in (("A",range(1,5)),("B",range(5,9))):
            levels={v:sum(twin(full,model,task,v,channel,d,endpoint) for d in draws)/4 for v in VERTICES}
            for op in ("R","T"):
                diffs=[]
                for v in VERTICES:
                    letters=set() if v=="I" else set(v)
                    if op in letters:continue
                    paired="".join(q for q in "RFHTL" if q in letters|{op})
                    assert paired in levels
                    diffs.append(levels[paired]-levels[v])
                assert len(diffs)==8
                trial[block+"_"+op]=sum(diffs)/8
        output[model+"|"+channel+"|"+task]={"family":family,**trial,
            "R_AB_sign_agree":trial["A_R"]*trial["B_R"]>0,
            "T_AB_sign_agree":trial["A_T"]*trial["B_T"]>0}
    return output

def all_attempt_bounds(full,model,channel,task):
    rows=[v for (m,t,vertex,semantic,c,d),v in full.items()
          if m==model and t==task and c==channel]
    assert len(rows)==16*2*8
    n=len(rows)
    k=sum(v["format_valid"] and v["semantic_correct"] is True for v in rows)
    unknown=sum(not v["format_valid"] for v in rows)
    return {"n":n,"known_correct":k,"technical_unknown":unknown,
            "latent_correctness_interval":[k/n,(k+unknown)/n],
            "executable_correctness":k/n}

def adjudicate(path):
    data=full_input(path)
    by=family_summary(data)
    blocks=signed_half_effects(data)
    counts=[all_attempt_bounds(data,m,c,t) for m,c,t in itertools.product(MODELS,CHANNELS,TASKS)]
    return {"stage":"EPISTEME-P69","status":"INFERENCE_SENSITIVITY_ONLY",
            "cluster_level_prediction":by,"half_split_operators":blocks,
            "all_attempt_bounds":counts,
            "reason_for_hold":"Only four hand-authored mechanism clusters; 16 signed-symmetry configurations (minimum two-sided reference p=0.125). No family-level significance certification or paper promotion.",
            "provider_calls":0}

def self_test():
    assert signflip_reference([1,1,1,1])["two_sided"]==0.125
    assert signflip_reference([1,1,1,1])["one_sided_positive"]==0.0625
    assert signflip_reference([1,1,1,1,1,1])["two_sided"]==0.03125
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/"mock.jsonl"
        for opposite in (False,True):
            fixture(path,opposite=opposite)
            z=adjudicate(path)
            assert len(z["cluster_level_prediction"])==4
            assert len(z["half_split_operators"])==32
            assert len(z["all_attempt_bounds"])==32
            assert all(q["n"]==256 and q["technical_unknown"]==0 for q in z["all_attempt_bounds"])
            if not opposite:
                assert all(t["A_R"]==t["B_R"]==t["A_T"]==t["B_T"]==0
                           for t in z["half_split_operators"].values())
            else:
                assert any(t["R_AB_sign_agree"] for t in z["half_split_operators"].values())
    print("P69_INFERENCE_SENSITIVITY_PASS four_families_min_twosided_p=0.125")
    print("holdout_family_predictions=4x4 half_effects=32 provider_calls=0")

if __name__=="__main__":self_test()
