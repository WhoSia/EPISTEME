"""P69 disjoint held-out task calibration/evaluation sensitivity.

P69 original LOFO Brier report uses all 8 held-out draws for calibration
but tests other vertices. This sensitivity test calibrates ONLY from draws
A (1..4) and tests held-out vertices ONLY on draws B (5..8).
Both candidate and task-only baseline use exactly the same calibration data.
"""
from __future__ import annotations
import itertools,json,tempfile
from pathlib import Path
from p69_predictive_analysis import MODELS,CHANNELS,FAMILIES,TASKS,VERTICES,ANCHORS,DRAWS,full_input,fixture

TRAIN_DRAWS=tuple(range(1,9))
CALIBRATION_DRAWS=(1,2,3,4)
TEST_DRAWS=(5,6,7,8)
TEST_VERTICES=tuple(v for v in VERTICES if v not in ANCHORS)

def joint(data,model,task,vertex,channel,draw):
    rows=[data[(model,task,vertex,s,channel,draw)] for s in ("valid","null")]
    return int(all(r["format_valid"] and r["semantic_correct"] is True for r in rows))

def crossfit(data):
    outputs=[]
    for model,channel,heldout in itertools.product(MODELS,CHANNELS,FAMILIES):
        train=[t for t in TASKS if not t.startswith(heldout+"_")]
        assert len(train)==6
        train_task_anchor={}
        for task in train:
            train_task_anchor[task]=sum(joint(data,model,task,a,channel,d)
                    for a,d in itertools.product(ANCHORS,TRAIN_DRAWS))/(len(ANCHORS)*len(TRAIN_DRAWS))
        offsets={}
        for vertex in TEST_VERTICES:
            offsets[vertex]=sum(
                sum(joint(data,model,task,vertex,channel,d) for d in TRAIN_DRAWS)/len(TRAIN_DRAWS)
                -train_task_anchor[task] for task in train
            )/len(train)
        for task in (heldout+"_1",heldout+"_2"):
            intercept=sum(joint(data,model,task,a,channel,d)
                          for a,d in itertools.product(ANCHORS,CALIBRATION_DRAWS)) / (
                          len(ANCHORS)*len(CALIBRATION_DRAWS))
            baseline_err=0.;transport_err=0.;n=0
            for vertex,d in itertools.product(TEST_VERTICES,TEST_DRAWS):
                actual=joint(data,model,task,vertex,channel,d)
                pred=max(0.,min(1.,intercept+offsets[vertex]))
                baseline_err+=(actual-intercept)**2
                transport_err+=(actual-pred)**2
                n+=1
            assert n==48
            outputs.append({"model":model,"channel":channel,"family":heldout,"task":task,
                "anchor_calibration_draws":"A_1_TO_4","test_draws":"B_5_TO_8",
                "test_n":n,"baseline_brier":baseline_err/n,"transport_brier":transport_err/n,
                "improvement":(baseline_err-transport_err)/n})
    assert len(outputs)==32
    return outputs

def self_test():
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"fixture.jsonl"
        for opposite in (False,True):
            fixture(path,opposite)
            res=crossfit(full_input(path))
            assert len(res)==32 and all(x["test_n"]==48 for x in res)
            if not opposite:
                assert all(x["baseline_brier"]==x["transport_brier"]==0 for x in res)
            else:
                assert all(-1<=x["improvement"]<=1 for x in res)
    print("P69_DISJOINT_CALIBRATION_COURT_PASS 32_tasksxmodelxchannel test_rows_each=48")
    print("train_d=1..8 heldout_calibration_d=1..4 test_d=5..8 provider_calls=0")

if __name__=="__main__":self_test()
