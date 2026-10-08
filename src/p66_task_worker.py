import argparse,json,random,time
from pathlib import Path
from p44_field import call
from p48_seed_fingerprints import panel_cells
from p66_relational_binding import TASKS,DRAWS,MODEL,packet,score

def run(task):
 rows=[];cells=panel_cells()
 for draw in DRAWS:
  order=list(cells);random.Random(660000+draw*20+TASKS.index(task)).shuffle(order)
  for position,c in enumerate(order):
   ts=time.perf_counter_ns()
   try:
    z=call(MODEL,packet(task,c['vertex'],c['semantic'],c['alias']),6600+draw)
    ok=score(z,task,c['semantic']);status='OK';err=None
   except Exception as e:
    ok=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:250]
   rows.append({**c,'task':task,'draw':draw,'position':position,'status':status,'primary_correct':ok,'shadow_correct':ok,'error':err,'latency_ms':(time.perf_counter_ns()-ts)/1e6})
 return {'stage':'EPISTEME-P66','task':task,'rows':rows}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--task',required=True,choices=TASKS);ap.add_argument('--out',required=True);a=ap.parse_args()
 p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(run(a.task)))
