from __future__ import annotations
import json,random,time,sys,math
from pathlib import Path
import numpy as np
from p42_reopen import VERTICES
from p44_field import call,correct,shadow_correct,vertex_set
from p48_seed_fingerprints import panel_cells
from p51_sufficiency import beta_mix_cs
from p52_allocation import eval_direction

STAGE='EPISTEME-P53'
TASKS=('CALIBRATION_PATH','PROVENANCE_LINEAGE','PROTOCOL_ORDER')
MODELS=('gemini','gptoss120')
DRAWS=tuple(range(1,33))
GEMINI_SEEDS=tuple(range(5301,5333))
WIDTH=.50
NPERM=5000

ALIASES={
 'A':('orion53','vega53',['aux-c1','aux-c7'],['aux-c3','aux-c9']),
 'B':('lyra53','cygnus53',['aux-p2','aux-p8'],['aux-p4','aux-p10']),
 'C':('terra53','luna53',['aux-r5','aux-r11'],['aux-r6','aux-r12']),
 'D':('atlas53','nova53',['aux-s13','aux-s17'],['aux-s19','aux-s23'])
}

def packet(task,label,semantic,tag):
    v=vertex_set(label);ren='R' in v;fill='F' in v;rh='H' in v;revtrace='T' in v;revrule='L' in v
    plain,renamed,f0,f1=ALIASES[tag];prefix=renamed if ren else plain
    key=f'{prefix}-target';alt=key+'-counterpart';fills=f1 if fill else f0
    def tr(x): return [*fills,x] if revtrace else [x,*fills]
    a_id=f'{task.lower()}-alpha';b_id=f'{task.lower()}-beta'
    recA={'id':a_id,'trace':tr(key)};recB={'id':b_id,'trace':tr(alt)}
    records=[recB,recA] if rh else [recA,recB]
    sens={'CALIBRATION_PATH':'calibration-path-sensitive','PROVENANCE_LINEAGE':'lineage-sensitive','PROTOCOL_ORDER':'preparation-order-sensitive'}[task]
    inv={'CALIBRATION_PATH':'calibration-path-invariant','PROVENANCE_LINEAGE':'lineage-invariant','PROTOCOL_ORDER':'preparation-order-invariant'}[task]
    target={'object':key,'intervention':'u1','response_link':sens if semantic=='valid' else inv}
    decoy={'object':f'{prefix}-decoy','intervention':'uX','response_link':'irrelevant'}
    rules=[decoy,target] if revrule else [target,decoy]
    common={'archive_id':f'p53-{task}-{tag}-{label}-{semantic}',
      'available_interventions':['u1','uX','uY'],
      'instructions':'Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.'}
    if task=='CALIBRATION_PATH':
        common.update({'claim':'The retained final calibration state is sufficient to predict the challenge response.',
          'surface_domain':'sensor-calibration','final_calibration':{a_id:'C=stable',b_id:'C=stable'},
          'calibration_runs':records,'calibration_rules':rules})
    elif task=='PROVENANCE_LINEAGE':
        common.update({'claim':'The retained final record is sufficient to predict the audit challenge response.',
          'surface_domain':'data-provenance','retained_checksum':{a_id:'digest=stable',b_id:'digest=stable'},
          'lineage_records':records,'provenance_rules':rules})
    else:
        common.update({'claim':'The retained terminal preparation state is sufficient to predict the perturbation response.',
          'surface_domain':'experimental-protocol','terminal_state':{a_id:'state=stable',b_id:'state=stable'},
          'preparation_records':records,'protocol_rules':rules})
    return common

def holm(tests,alpha=.05):
    valid=sorted([(k,v['p']) for k,v in tests.items() if v.get('p') is not None],key=lambda x:x[1])
    m=len(valid);adj={k:None for k in tests};rej={k:False for k in tests};run=0.
    for i,(k,p) in enumerate(valid):
        run=max(run,min(1.,(m-i)*p));adj[k]=run
    stop=False
    for i,(k,p) in enumerate(valid):
        if stop: continue
        if p<=alpha/(m-i):rej[k]=True
        else:stop=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def pearson(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float);a=a-a.mean();b=b-b.mean()
    na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
    return None if na<=1e-15 or nb<=1e-15 else float(np.dot(a,b)/(na*nb))

def perm_corr(a,b,seed):
    obs=pearson(a,b)
    if obs is None:return {'statistic':None,'p':None,'permutations':0}
    rng=random.Random(seed);idx=list(range(len(b)));ge=0
    for _ in range(NPERM):
        p=idx.copy();rng.shuffle(p);x=pearson(a,np.asarray(b)[p])
        if x is not None and x>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def schedule():
    cells=panel_cells();jobs=[]
    for di,draw in enumerate(DRAWS):
        task_order=list(TASKS);random.Random(530000+draw).shuffle(task_order)
        for ti,task in enumerate(task_order):
            order=list(cells);random.Random(531000+draw*10+ti).shuffle(order)
            for pos,c in enumerate(order):
                model_order=('gemini','gptoss120') if ((draw+ti+pos)%2==0) else ('gptoss120','gemini')
                for pair_rank,m in enumerate(model_order):jobs.append((m,task,draw,di,pos,pair_rank,c))
    assert len(jobs)==12288
    return jobs

def run():
    rows=[]
    for model,task,draw,di,pos,pair_rank,c in schedule():
        seed=GEMINI_SEEDS[di] if model=='gemini' else 5300+draw
        t0=time.perf_counter_ns()
        try:
            o=call(model,packet(task,c['vertex'],c['semantic'],c['alias']),seed)
            pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**c,'model':model,'task':task,'draw':draw,'gemini_seed':seed if model=='gemini' else None,
                     'position':pos,'pair_rank':pair_rank,'latency_ms':(time.perf_counter_ns()-t0)/1e6,
                     'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def tech(rows,m):
    rs=[r for r in rows if r['model']==m];ok=sum(r['status']=='OK' for r in rs)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rs)
    return {'ok':ok,'total':len(rs),'complete':ok==len(rs),'shadow_disagreement_rate':dis/ok if ok else None}

def jmatrix(rows,m,task):
    J=np.full((32,32),np.nan)
    for d in DRAWS:
        for vi in range(32):
            rs=[r for r in rows if r['model']==m and r['task']==task and r['draw']==d and r['vertex_index']==vi and r['status']=='OK']
            by={r['semantic']:r for r in rs}
            if set(by)=={'valid','null'}:J[d-1,vi]=float(bool(by['valid']['primary_correct']) and bool(by['null']['primary_correct']))
    return J

def tau_vec(J):
    out=[]
    for v in range(32):
        s=0;tau=33
        for t,x in enumerate(J[:,v],1):
            s+=int(x);lo,hi=beta_mix_cs(s,t,.05)
            if hi-lo<=WIDTH:tau=t;break
        out.append(tau)
    return np.asarray(out,float)

def factorization(T):
    T=np.asarray(T,float);grand=T.mean();tm=T.mean(axis=1);vm=T.mean(axis=0)
    fit=tm[:,None]+vm[None,:]-grand
    ss_task=float(T.shape[1]*np.sum((tm-grand)**2))
    ss_rep=float(T.shape[0]*np.sum((vm-grand)**2))
    ss_int=float(np.sum((T-fit)**2));total=ss_task+ss_rep+ss_int
    return {'ss_task':ss_task,'ss_representation':ss_rep,'ss_interaction':ss_int,'ss_total':total,
            'share_task':ss_task/total if total else 0,'share_representation':ss_rep/total if total else 0,
            'share_interaction':ss_int/total if total else 0,'common_representation_profile':(vm-grand).tolist()}

def primary_tests(tau_by_task,historical):
    tests={};center_hist=np.asarray(historical,float)-np.mean(historical)
    for i,t in enumerate(TASKS):
        y=tau_by_task[t]-tau_by_task[t].mean()
        tests[f'historical:{t}']=perm_corr(center_hist,y,5340+i)
    for i,t in enumerate(TASKS):
        others=[x for x in TASKS if x!=t]
        pred=np.mean([tau_by_task[o]-tau_by_task[o].mean() for o in others],axis=0)
        target=tau_by_task[t]-tau_by_task[t].mean()
        tests[f'loo:{t}']=perm_corr(pred,target,5350+i)
    return tests

def policy_secondary(J,q):
    A=J[:16];B=J[16:];res={}
    qdict={str(WIDTH):q}
    for name,X,Y in [('A_to_B',A,B),('B_to_A',B,A)]:
        e=eval_direction(X,Y,q,WIDTH,256)
        res[name]={
          'mse':{k:v['mse'] for k,v in e['policies'].items()},
          'decision':{k:v['decision_preservation'] for k,v in e['policies'].items()},
          'field_no_worse':e['policies']['FIELD_GUIDED_HYBRID']['mse']<=e['policies']['UNIFORM_FIXED']['mse'] and e['policies']['FIELD_GUIDED_HYBRID']['mse']<=e['policies']['ONLINE_WIDTH']['mse'],
          'field_false_certified':e['policies']['FIELD_GUIDED_HYBRID']['decision_preservation']['false_certified']}
    return res

def main():
    base=json.load(open('active/p51_sufficiency_baseline.json'))
    hist=np.asarray(base['mean_tau']['gemini']['0.5'],float)
    rows=run();gates={m:tech(rows,m) for m in MODELS};complete=all(x['complete'] for x in gates.values())
    if not complete:
        out={'stage':STAGE,'technical':gates,'constitutional_verdict':'TECHNICAL_HOLD','raw_rows':rows}
    else:
        mats={m:{t:jmatrix(rows,m,t) for t in TASKS} for m in MODELS}
        assert all(not np.isnan(mats[m][t]).any() for m in MODELS for t in TASKS)
        tau={m:{t:tau_vec(mats[m][t]) for t in TASKS} for m in MODELS}
        gtests=primary_tests(tau['gemini'],hist);gh=holm(gtests)
        full=all(gtests[k]['statistic'] is not None and gtests[k]['statistic']>0 and gh['rejected'][k] for k in gtests)
        hist_pass=sum(gh['rejected'][f'historical:{t}'] and gtests[f'historical:{t}']['statistic']>0 for t in TASKS)
        loo_pass=sum(gh['rejected'][f'loo:{t}'] and gtests[f'loo:{t}']['statistic']>0 for t in TASKS)
        # GPT-OSS fresh-task factorization only
        otests={}
        for i,t in enumerate(TASKS):
            others=[x for x in TASKS if x!=t]
            pred=np.mean([tau['gptoss120'][o]-tau['gptoss120'][o].mean() for o in others],axis=0)
            target=tau['gptoss120'][t]-tau['gptoss120'][t].mean()
            otests[f'loo:{t}']=perm_corr(pred,target,5380+i)
        oh=holm(otests)
        fac={m:factorization(np.stack([tau[m][t] for t in TASKS])) for m in MODELS}
        policy={t:policy_secondary(mats['gemini'][t],base['mean_tau']['gemini']['0.5']) for t in TASKS}
        policy_gate=all(policy[t][d]['field_no_worse'] and policy[t][d]['field_false_certified']==0 for t in TASKS for d in ('A_to_B','B_to_A'))
        artifact=any((gates[m]['shadow_disagreement_rate'] or 0)>=.10 for m in MODELS)
        if artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif full and policy_gate:verdict='CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_WITH_ZERO_SHOT_POLICY_TRANSFER'
        elif full:verdict='CROSS_TASK_MEASUREMENT_DIFFICULTY_LAW_WITHOUT_OPERATIONAL_TRANSFER'
        elif loo_pass==3 and hist_pass<3:verdict='FRESH_TASK_COMMON_COMPONENT_WITHOUT_HISTORICAL_TRANSPORT'
        elif hist_pass>=1 and loo_pass>=1:verdict='PARTIAL_TASK_TRANSPORT_ONLY'
        elif fac['gemini']['share_interaction']>fac['gemini']['share_representation']:verdict='TASK_INTERACTION_DOMINATES_REPRESENTATION_DIFFICULTY'
        else:verdict='NO_CROSS_TASK_MEASUREMENT_LAW'
        out={'stage':STAGE,'design':{'tasks':list(TASKS),'models':list(MODELS),'draws_per_task_model':32,'total_calls':12288,'primary_width':WIDTH},
             'technical':gates,
             'gemini':{'tau':{t:tau['gemini'][t].tolist() for t in TASKS},'primary_tests':gtests,'holm':gh,'factorization':fac['gemini'],'historical_pass_count':hist_pass,'loo_pass_count':loo_pass},
             'gptoss120':{'tau':{t:tau['gptoss120'][t].tolist() for t in TASKS},'loo_tests':otests,'holm':oh,'factorization':fac['gptoss120']},
             'zero_shot_policy_transfer':policy,'policy_gate':policy_gate,'constitutional_verdict':verdict,
             'authority':'P53 tests transport of measurement-sufficiency structure across independently schematized tasks. Cross-task descriptive transport and allocation utility are separate authority layers. No provider-internal, neural-state, generic prompt-robustness, or behavioral-SVEC claim is licensed.',
             'raw_rows':rows}
    p=Path('receipts/p53_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:
        b=json.load(open('active/p51_sufficiency_baseline.json'));assert len(b['mean_tau']['gemini']['0.5'])==32
        assert len(schedule())==12288
        for task in TASKS:
            p=packet(task,'R_F_H_T_L','valid','A')
            assert p['archive_id'].startswith('p53-') and 'u1' in p['available_interventions']
        fake={'a':{'p':.001},'b':{'p':.02},'c':{'p':.2}};h=holm(fake);assert h['rejected']['a']
        print('P53_PRECHECK_PASS')
    else:main()
