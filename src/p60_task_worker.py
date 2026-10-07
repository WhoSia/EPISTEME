from __future__ import annotations
import argparse,json
from pathlib import Path
from p63_structural_location import TASKS as P63_TASKS,self_test
from p63_task_worker import run_task

CARRIER_TASKS=('RD1','RD2','RD3','RP1','RP2','RP3','SD1','SD2','SD3','SP1','SP2','SP3')
MAP=dict(zip(CARRIER_TASKS,P63_TASKS))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--task',required=True,choices=CARRIER_TASKS);ap.add_argument('--out',required=True);a=ap.parse_args()
    self_test()
    d=run_task(MAP[a.task])
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2))

if __name__=='__main__':main()
