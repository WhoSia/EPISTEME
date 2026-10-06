from __future__ import annotations
import itertools, json, math, random
from pathlib import Path
from collections import OrderedDict
import numpy as np

from p42_reopen import VERTICES
from p44_field import call, correct, shadow_correct, vertex_set
from p48_seed_fingerprints import panel_cells
from p51_sufficiency import beta_mix_cs

STAGE='EPISTEME-P60'
MODEL='gptoss120'
DRAWS=tuple(range(1,65))
WIDTH=.50
OPS=('R','F','H','T','L')
PRIMARY_OPS=('R','T')

TASK_SPECS=OrderedDict([
 ('RD1',{'carrier':'record','role':'diagnostic','skin':1,'domain':'ledger-diagnosis','terminal_key':'terminal_code','records_key':'evidence_records','rules_key':'diagnostic_rules','claim':'The terminal code is sufficient to predict the challenge response.','sensitive':'record-history-sensitive','invariant':'record-history-invariant'}),
 ('RD2',{'carrier':'record','role':'diagnostic','skin':2,'domain':'trace-diagnosis','terminal_key':'terminal_label','records_key':'trace_records','rules_key':'diagnostic_links','claim':'The terminal label is sufficient to predict the challenge response.','sensitive':'trace-history-sensitive','invariant':'trace-history-invariant'}),
 ('RD3',{'carrier':'record','role':'diagnostic','skin':3,'domain':'audit-diagnosis','terminal_key':'terminal_marker','records_key':'audit_records','rules_key':'diagnostic_relations','claim':'The terminal marker is sufficient to predict the challenge response.','sensitive':'audit-history-sensitive','invariant':'audit-history-invariant'}),
 ('RP1',{'carrier':'record','role':'procedural','skin':1,'domain':'schema-procedure','terminal_key':'retained_schema','records_key':'transformation_records','rules_key':'procedure_rules','claim':'The retained schema is sufficient to predict the challenge response.','sensitive':'schema-history-sensitive','invariant':'schema-history-invariant'}),
 ('RP2',{'carrier':'record','role':'procedural','skin':2,'domain':'canonicalization-procedure','terminal_key':'retained_record','records_key':'canonicalization_records','rules_key':'procedure_links','claim':'The retained record is sufficient to predict the challenge response.','sensitive':'canonicalization-history-sensitive','invariant':'canonicalization-history-invariant'}),
 ('RP3',{'carrier':'record','role':'procedural','skin':3,'domain':'merge-procedure','terminal_key':'retained_summary','records_key':'merge_records','rules_key':'procedure_relations','claim':'The retained summary is sufficient to predict the challenge response.','sensitive':'merge-history-sensitive','invariant':'merge-history-invariant'}),
 ('SD1',{'carrier':'state','role':'diagnostic','skin':1,'domain':'state-diagnosis-a','terminal_key':'terminal_state','records_key':'state_history','rules_key':'diagnostic_rules','claim':'The terminal state is sufficient to predict the challenge response.','sensitive':'state-history-sensitive','invariant':'state-history-invariant'}),
 ('SD2',{'carrier':'state','role':'diagnostic','skin':2,'domain':'state-diagnosis-b','terminal_key':'terminal_condition','records_key':'condition_history','rules_key':'diagnostic_links','claim':'The terminal condition is sufficient to predict the challenge response.','sensitive':'condition-history-sensitive','invariant':'condition-history-invariant'}),
 ('SD3',{'carrier':'state','role':'diagnostic','skin':3,'domain':'state-diagnosis-c','terminal_key':'terminal_readout','records_key':'readout_history','rules_key':'diagnostic_relations','claim':'The terminal readout is sufficient to predict the challenge response.','sensitive':'readout-history-sensitive','invariant':'readout-history-invariant'}),
 ('SP1',{'carrier':'state','role':'procedural','skin':1,'domain':'state-procedure-a','terminal_key':'prepared_state','records_key':'preparation_history','rules_key':'procedure_rules','claim':'The prepared state is sufficient to predict the challenge response.','sensitive':'preparation-history-sensitive','invariant':'preparation-history-invariant'}),
 ('SP2',{'carrier':'state','role':'procedural','skin':2,'domain':'state-procedure-b','terminal_key':'calibrated_state','records_key':'calibration_history','rules_key':'procedure_links','claim':'The calibrated state is sufficient to predict the challenge response.','sensitive':'calibration-history-sensitive','invariant':'calibration-history-invariant'}),
 ('SP3',{'carrier':'state','role':'procedural','skin':3,'domain':'state-procedure-c','terminal_key':'conditioned_state','records_key':'conditioning_history','rules_key':'procedure_relations','claim':'The conditioned state is sufficient to predict the challenge response.','sensitive':'conditioning-history-sensitive','invariant':'conditioning-history-invariant'}),
])
TASKS=tuple(TASK_SPECS)

ALIASES={
 'A':('cobalt60','indigo60',['aux-a2','aux-a8'],['aux-a4','aux-a10']),
 'B':('ember60','opal60',['aux-b1','aux-b7'],['aux-b3','aux-b9']),
 'C':('cedar60','quartz60',['aux-c5','aux-c11'],['aux-c6','aux-c12']),
 'D':('harbor60','zenith60',['aux-d13','aux-d17'],['aux-d19','aux-d23'])
}

def packet(task,label,semantic,tag):
    spec=TASK_SPECS[task]
    v=vertex_set(label);ren='R' in v;fill='F' in v;rh='H' in v;revtrace='T' in v;revrule='L' in v
    plain,renamed,f0,f1=ALIASES[tag];prefix=renamed if ren else plain
    key=f'{prefix}-target';alt=key+'-counterpart';fills=f1 if fill else f0
    def tr(x): return [*fills,x] if revtrace else [x,*fills]
    a=f'{task.lower()}-alpha';b=f'{task.lower()}-beta'
    recA={'id':a,'trace':tr(key)};recB={'id':b,'trace':tr(alt)}
    records=[recB,recA] if rh else [recA,recB]
    target={'object':key,'intervention':'u1','response_link':spec['sensitive'] if semantic=='valid' else spec['invariant']}
    decoy={'object':f'{prefix}-decoy','intervention':'uX','response_link':'irrelevant'}
    rules=[decoy,target] if revrule else [target,decoy]
    instruction=('Using only this archive, propose the single strongest admissible diagnostic challenge that could falsify the claim. '
                 if spec['role']=='diagnostic' else
                 'Using only this archive, propose the single strongest admissible procedural intervention that could falsify the claim. ')
    instruction+='If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.'
    out={
      'archive_id':f'p60-{task}-{tag}-{label}-{semantic}',
      'claim':spec['claim'],
      'surface_domain':spec['domain'],
      'available_interventions':['u1','uX','uY'],
      'instructions':instruction,
      spec['terminal_key']:{a:'stable',b:'stable'},
      spec['records_key']:records,
      spec['rules_key']:rules,
    }
    return out

def tau_vec(X):
    out=[]
    for v in range(32):
        s=0;tau=33
        for t,x in enumerate(X[:,v],1):
            s+=int(x);lo,hi=beta_mix_cs(s,t,.05)
            if hi-lo<=WIDTH:
                tau=t;break
        out.append(tau)
    return np.asarray(out,float)

def operator_edges():
    lookup={frozenset(vertex_set(v)):i for i,v in enumerate(VERTICES)}
    out={}
    for op in OPS:
        edges=[]
        for i,v in enumerate(VERTICES):
            s=vertex_set(v)
            if op in s: continue
            edges.append((i,lookup[frozenset(set(s)|{op})]))
        assert len(edges)==16
        out[op]=edges
    return out
EDGES=operator_edges()

def operator_effect(vec):
    vec=np.asarray(vec,float)
    return {op:float(np.mean([vec[on]-vec[off] for off,on in edges])) for op,edges in EDGES.items()}

def expected_sign(op,carrier):
    if op=='R': return 1 if carrier=='record' else -1
    if op=='T': return -1 if carrier=='record' else 1
    raise KeyError(op)

def holm(tests,alpha=.05):
    valid=sorted([(k,v['p']) for k,v in tests.items() if v.get('p') is not None],key=lambda x:x[1])
    m=len(valid);adj={k:None for k in tests};rej={k:False for k in tests};run=0.0
    for i,(k,p) in enumerate(valid):
        run=max(run,min(1.0,(m-i)*p));adj[k]=run
    stop=False
    for i,(k,p) in enumerate(valid):
        if stop: continue
        if p<=alpha/(m-i): rej[k]=True
        else: stop=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def stratified_factor_test(values,factor,stratify,positive):
    tasks=list(TASKS)
    def delta(assign):
        a=[values[t] for t in tasks if assign[t]==1]
        b=[values[t] for t in tasks if assign[t]==0]
        return float(np.mean(a)-np.mean(b))
    if factor=='carrier':
        actual={t:int(TASK_SPECS[t]['carrier']=='state') for t in tasks}
        strata=('diagnostic','procedural')
        members={s:[t for t in tasks if TASK_SPECS[t]['role']==s] for s in strata}
    elif factor=='role':
        actual={t:int(TASK_SPECS[t]['role']=='procedural') for t in tasks}
        strata=('record','state')
        members={s:[t for t in tasks if TASK_SPECS[t]['carrier']==s] for s in strata}
    else:
        raise KeyError(factor)
    obs=delta(actual)
    choices=[]
    for s in strata:
        ms=members[s];k=sum(actual[t] for t in ms)
        choices.append([(ms,set(c)) for c in itertools.combinations(ms,k)])
    vals=[]
    for x,y in itertools.product(*choices):
        assign={}
        for ms,ones in (x,y):
            for t in ms: assign[t]=int(t in ones)
        vals.append(delta(assign))
    if positive:
        p=sum(v>=obs-1e-15 for v in vals)/len(vals)
    else:
        p=sum(v<=obs+1e-15 for v in vals)/len(vals)
    return {'statistic':obs,'p':p,'exact_assignments':len(vals),'direction':'positive' if positive else 'negative'}

def self_test():
    assert len(TASKS)==12
    cells=[(v['carrier'],v['role']) for v in TASK_SPECS.values()]
    for c in ('record','state'):
        for r in ('diagnostic','procedural'):
            assert cells.count((c,r))==3
    assert len(panel_cells())==64
    assert all(len(x)==16 for x in EDGES.values())
    keys=[]
    for t in TASKS:
        p=packet(t,'I','valid','A')
        assert len(p['available_interventions'])==3
        keys.append(len(p))
    assert len(set(keys))==1
    fake={t:(1 if TASK_SPECS[t]['carrier']=='state' else -1) for t in TASKS}
    z=stratified_factor_test(fake,'carrier','role',True)
    assert z['exact_assignments']==400 and z['p']<=.01
    print('P60_PRECHECK_PASS')

if __name__=='__main__':
    import sys
    if '--self-test' in sys.argv: self_test()
