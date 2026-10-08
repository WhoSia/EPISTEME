from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np
from p60_context_interaction import operator_effect,holm
from p66_relational_binding import TASKS,SPECS,DRAWS
def signed_stats(vals):
 names=[('target_linked','history_externalized'),('target_linked','terminal_embedded'),('decoy_linked','history_externalized'),('decoy_linked','terminal_embedded')]
 def contrast(v):
  binding=np.mean([v[('target_linked',l,s)]-v[('decoy_linked',l,s)] for l in ('history_externalized','terminal_embedded') for s in (1,2,3)])
  location=np.mean([v[(b,'terminal_embedded',s)]-v[(b,'history_externalized',s)] for b in ('target_linked','decoy_linked') for s in (1,2,3)])
  interaction=np.mean([(v[('target_linked','terminal_embedded',s)]-v[('decoy_linked','terminal_embedded',s)])-(v[('target_linked','history_externalized',s)]-v[('decoy_linked','history_externalized',s)]) for s in (1,2,3)])
  return {'binding':float(binding),'location':float(location),'interaction':float(interaction)}
 obs={ (SPECS[t]['binding'],SPECS[t]['location'],SPECS[t]['skin']):float(vals[t]) for t in TASKS}
 real=contrast(obs)
 perms=[]
 for s in (1,2,3):
  vs=[obs[(b,l,s)] for b,l in names]
  perms.append(list(itertools.permutations(vs)))
 exceed=dict.fromkeys(real,0)
 for group in itertools.product(*perms):
  x={(b,l,s):v for s,p in enumerate(group,1) for (b,l),v in zip(names,p)}
  z=contrast(x)
  for k in real:
   if abs(z[k])>=abs(real[k])-1e-12: exceed[k]+=1
 return {k:{'effect':real[k],'p':exceed[k]/13824,'permutations':13824} for k in real}
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',required=True);a.add_argument('--out',required=True);x=a.parse_args()
 docs=[]
 for p in Path(x.root).rglob('*.json'):
  try:d=json.loads(p.read_text())
  except Exception:continue
  if isinstance(d,dict) and d.get('stage')=='EPISTEME-P66' and d.get('task') in TASKS:docs.append(d)
 if len(docs)!=12 or {d['task'] for d in docs}!=set(TASKS):raise RuntimeError('P66_TASK_SET')
 rows=[r for d in docs for r in d['rows']]
 if len(rows)!=12288 or any(len(d['rows'])!=1024 for d in docs):raise RuntimeError('P66_TOTAL')
 missing=[{k:r.get(k) for k in ('task','draw','cell_index','error')} for r in rows if r['status']!='OK']
 out={'stage':'EPISTEME-P66','technical':{'ok':len(rows)-len(missing),'total':len(rows),'failures':len(missing),'failed_rows':missing},'constitutional_verdict':'TECHNICAL_HOLD'}
 if not missing:
  effects={};means={}
  for task in TASKS:
   rr=[r for r in rows if r['task']==task]
   joint=np.zeros((16,32),float)
   for draw in DRAWS:
    for vertex in range(32):
     cell=[r for r in rr if r['draw']==draw and r['vertex_index']==vertex]
     if len(cell)!=2 or {r['semantic'] for r in cell}!={'valid','null'}:raise RuntimeError('P66_BAD_TWIN')
     joint[draw-1,vertex]=float(all(r['primary_correct'] for r in cell))
   means[task]=float(joint.mean())
   effects[task]={'R':operator_effect(1-joint.mean(axis=0))['R'],'T':operator_effect(1-joint.mean(axis=0))['T']}
  binding_test=signed_stats(means)
  op_tests={op:signed_stats({t:effects[t][op] for t in TASKS})['binding'] for op in ('R','T')}
  op_holm=holm({op:op_tests[op] for op in ('R','T')})
  # Operator-specific tests are secondary; avoid substituting them for joint-accuracy primary.
  primary=binding_test['binding']['p']<=.05
  op_primary=all(op_holm['rejected'].values())
  if primary and op_primary:verdict='RELATIONAL_BINDING_EFFECT_WITH_R_T_OPERATOR_MODERATION'
  elif primary:verdict='RELATIONAL_BINDING_EFFECT_WITHOUT_JOINT_R_T_MODERATION'
  elif op_primary:verdict='R_T_MODERATION_WITHOUT_PRIMARY_JOINT_ACCURACY_EFFECT'
  else:verdict='NO_PRECOMMITTED_BINDING_EFFECT_DETECTED'
  out.update(task_joint_accuracy=means,task_operator_effects=effects,binding_factorial=binding_test,operator_binding_tests=op_tests,operator_binding_holm=op_holm,constitutional_verdict=verdict)
 Path(x.out).parent.mkdir(parents=True,exist_ok=True);Path(x.out).write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
