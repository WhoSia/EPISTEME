from __future__ import annotations
import argparse,json,random,time
from pathlib import Path
from p44_field import call,correct,shadow_correct
from p48_seed_fingerprints import panel_cells
from p60_context_interaction import packet,MODEL,DRAWS,TASKS,TASK_SPECS

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--task',required=True,choices=TASKS);ap.add_argument('--out',required=True);a=ap.parse_args()
    rows=[];cells=panel_cells();ti=TASKS.index(a.task)
    for draw in DRAWS:
        order=list(cells);random.Random(601000+draw*20+ti).shuffle(order)
        for pos,c in enumerate(order):
            t0=time.perf_counter_ns()
            try:
                o=call(MODEL,packet(a.task,c['vertex'],c['semantic'],c['alias']),6000+draw)
                pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
            except Exception as e:
                pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
            rows.append({**c,'model':MODEL,'task':a.task,'carrier':TASK_SPECS[a.task]['carrier'],'role':TASK_SPECS[a.task]['role'],
                         'skin':TASK_SPECS[a.task]['skin'],'draw':draw,'position':pos,
                         'latency_ms':(time.perf_counter_ns()-t0)/1e6,'status':status,
                         'primary_correct':pc,'shadow_correct':sc,'error':err})
    if len(rows)!=4096: raise RuntimeError(len(rows))
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps({'task':a.task,'rows':rows},indent=2))

if __name__=='__main__': main()
