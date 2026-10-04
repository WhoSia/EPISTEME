from __future__ import annotations
import itertools, json, math, random, time, sys
from pathlib import Path
from collections import defaultdict
import numpy as np

import p53_cross_task as p53
from p42_reopen import VERTICES
from p44_field import call, correct, shadow_correct, vertex_set
from p48_seed_fingerprints import panel_cells
from p51_sufficiency import beta_mix_cs

STAGE='EPISTEME-P57'
MODEL='gptoss120'
TASKS=('FAULT_DIAGNOSIS_HISTORY','NORMALIZATION_PIPELINE','MATERIAL_PRECONDITIONING')
DRAWS=tuple(range(1,65))
WIDTH=.50
NPERM=5000
ANCHOR=np.array([i for i in range(32) if i%4==0],dtype=int)
HOLD=np.array([i for i in range(32) if i%4!=0],dtype=int)
OPS=('R','F','H','T','L')

ALIASES={
 'A':('cobalt57','indigo57',['aux-a2','aux-a8'],['aux-a4','aux-a10']),
 'B':('ember57','opal57',['aux-b1','aux-b7'],['aux-b3','aux-b9']),
 'C':('cedar57','quartz57',['aux-c5','aux-c11'],['aux-c6','aux-c12']),
 'D':('harbor57','zenith57',['aux-d13','aux-d17'],['aux-d19','aux-d23'])
}

def packet(task,label,semantic,tag):
    v=vertex_set(label);ren='R' in v;fill='F' in v;rh='H' in v;revtrace='T' in v;revrule='L' in v
    plain,renamed,f0,f1=ALIASES[tag];prefix=renamed if ren else plain
    key=f'{prefix}-target';alt=key+'-counterpart';fills=f1 if fill else f0
    def tr(x): return [*fills,x] if revtrace else [x,*fills]
    a=f'{task.lower()}-alpha';b=f'{task.lower()}-beta'
    recA={'id':a,'trace':tr(key)};recB={'id':b,'trace':tr(alt)}
    records=[recB,recA] if rh else [recA,recB]
    sensitive={
      'FAULT_DIAGNOSIS_HISTORY':'fault-history-sensitive',
      'NORMALIZATION_PIPELINE':'normalization-pipeline-sensitive',
      'MATERIAL_PRECONDITIONING':'preconditioning-history-sensitive'
    }[task]
    invariant={
      'FAULT_DIAGNOSIS_HISTORY':'fault-history-invariant',
      'NORMALIZATION_PIPELINE':'normalization-pipeline-invariant',
      'MATERIAL_PRECONDITIONING':'preconditioning-history-invariant'
    }[task]
    target={'object':key,'intervention':'u1','response_link':sensitive if semantic=='valid' else invariant}
    decoy={'object':f'{prefix}-decoy','intervention':'uX','response_link':'irrelevant'}
    rules=[decoy,target] if revrule else [target,decoy]
    common={
      'archive_id':f'p57-{task}-{tag}-{label}-{semantic}',
      'available_interventions':['u1','uX','uY'],
      'instructions':'Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.'
    }
    if task=='FAULT_DIAGNOSIS_HISTORY':
        common.update({
          'claim':'The terminal diagnostic code is sufficient to predict the challenge response.',
          'surface_domain':'fault-diagnosis',
          'terminal_diagnostic':{a:'code=stable',b:'code=stable'},
          'diagnostic_records':records,
          'fault_rules':rules
        })
    elif task=='NORMALIZATION_PIPELINE':
        common.update({
          'claim':'The retained normalized summary is sufficient to predict the challenge response.',
          'surface_domain':'data-normalization',
          'normalized_summary':{a:'summary=stable',b:'summary=stable'},
          'normalization_records':records,
          'pipeline_rules':rules
        })
    else:
        common.update({
          'claim':'The terminal measured material state is sufficient to predict the challenge response.',
          'surface_domain':'material-preconditioning',
          'terminal_measurement':{a:'state=stable',b:'state=stable'},
          'conditioning_records':records,
          'material_rules':rules
        })
    return common

def holm(tests,alpha=.05):
    valid=sorted([(k,v['p']) for k,v in tests.items() if v.get('p') is not None],key=lambda x:x[1])
    m=len(valid);adj={k:None for k in tests};rej={k:False for k in tests};run=0.0
    for i,(k,p) in enumerate(valid):
        run=max(run,min(1.0,(m-i)*p));adj[k]=run
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
        p=idx.copy();rng.shuffle(p);cur=pearson(a,np.asarray(b)[p])
        if cur is not None and cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def schedule():
    cells=panel_cells();jobs=[]
    for draw in DRAWS:
        task_order=list(TASKS);random.Random(570000+draw).shuffle(task_order)
        for ti,task in enumerate(task_order):
            order=list(cells);random.Random(571000+draw*10+ti).shuffle(order)
            for pos,c in enumerate(order):
                jobs.append((task,draw,pos,c))
    assert len(jobs)==12288
    return jobs

def run():
    rows=[]
    for task,draw,pos,c in schedule():
        t0=time.perf_counter_ns()
        try:
            o=call(MODEL,packet(task,c['vertex'],c['semantic'],c['alias']),5700+draw)
            pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**c,'model':MODEL,'task':task,'draw':draw,'position':pos,
                     'latency_ms':(time.perf_counter_ns()-t0)/1e6,'status':status,
                     'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def tech(rows):
    ok=sum(r['status']=='OK' for r in rows)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    return {'ok':ok,'total':len(rows),'complete':ok==len(rows),
            'primary_shadow_disagreements':dis,
            'primary_shadow_disagreement_rate':dis/ok if ok else None}

def jmatrix(rows,task):
    J=np.full((64,32),np.nan)
    for d in DRAWS:
        for vi in range(32):
            rs=[r for r in rows if r['task']==task and r['draw']==d and r['vertex_index']==vi and r['status']=='OK']
            by={r['semantic']:r for r in rs}
            if set(by)=={'valid','null'}:
                J[d-1,vi]=float(bool(by['valid']['primary_correct']) and bool(by['null']['primary_correct']))
    return J

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

def load_historical_worlds(path):
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    est=d['estimand_identifiability']['by_model_task']['gptoss120']
    base={}
    unresolved=[]
    for task in p53.TASKS:
        vals=np.empty(32,float)
        for vi,v in enumerate(est[task]['vertices']):
            poss=tuple(int(x) for x in v['possible_taus'])
            if len(poss)==1: vals[vi]=poss[0]
            else: unresolved.append((task,vi,v['vertex'],poss))
        base[task]=vals
    if len(unresolved)!=1:
        raise RuntimeError(f'expected one historical GPT-OSS ambiguity, got {unresolved}')
    task,vi,vertex,poss=unresolved[0]
    worlds=[]
    for val in poss:
        w={t:base[t].copy() for t in p53.TASKS};w[task][vi]=val
        worlds.append({'assignment':{'task':task,'vertex':vertex,'value':val},'tau':w})
    return worlds

def interaction_basis(world):
    T=np.stack([world['tau'][t] for t in p53.TASKS])
    grand=float(T.mean());tm=T.mean(axis=1);vm=T.mean(axis=0)
    beta=vm-grand
    G=T-tm[:,None]-vm[None,:]+grand
    U,s,Vt=np.linalg.svd(G,full_matrices=False)
    tol=max(G.shape)*np.finfo(float).eps*(s[0] if len(s) else 0.0)
    k=int(np.sum(s>tol))
    return {'beta':beta,'G':G,'basis':Vt[:k],'singular_values':s,'rank':k}

def projection_fraction(x,B):
    den=float(np.dot(x,x))
    if den<=1e-15:return None
    p=(x@B.T)@B
    return float(np.dot(p,p)/den)

def projection_test(tau,basis_obj,seed):
    x=tau-tau.mean()-basis_obj['beta'];B=basis_obj['basis']
    obs=projection_fraction(x,B)
    if obs is None:return {'statistic':None,'p':None}
    rng=random.Random(seed);ge=0;idx=list(range(32))
    for _ in range(NPERM):
        p=idx.copy();rng.shuffle(p);cur=projection_fraction(x[p],B)
        if cur is not None and cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def prediction_improvement(tau,basis_obj,Bperm=None):
    x=tau-tau.mean()-basis_obj['beta']
    B=basis_obj['basis'] if Bperm is None else Bperm
    if B.shape[0]==0:return None
    A=B[:,ANCHOR].T
    coef=np.linalg.lstsq(A,x[ANCHOR],rcond=None)[0]
    pred=coef@B[:,HOLD]
    base=float(np.mean(x[HOLD]**2))
    mse=float(np.mean((x[HOLD]-pred)**2))
    return base-mse

def prediction_test(tau,basis_obj,seed):
    obs=prediction_improvement(tau,basis_obj)
    if obs is None:return {'statistic':None,'p':None}
    rng=random.Random(seed);ge=0;idx=list(range(32));B=basis_obj['basis']
    for _ in range(NPERM):
        p=idx.copy();rng.shuffle(p);cur=prediction_improvement(tau,basis_obj,B[:,p])
        if cur is not None and cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def robust_two_world(test0,test1):
    vals=[test0,test1]
    if any(x['statistic'] is None or x['p'] is None for x in vals):
        return {'statistic':None,'p':None,'worlds':vals}
    return {'statistic':min(x['statistic'] for x in vals),
            'p':max(x['p'] for x in vals),'worlds':vals,
            'rule':'min statistic / max p across two admissible historical worlds'}

def operator_edges():
    lookup={frozenset(vertex_set(v)):i for i,v in enumerate(VERTICES)}
    out={}
    for op in OPS:
        edges=[]
        for i,v in enumerate(VERTICES):
            s=vertex_set(v)
            if op in s:continue
            edges.append((i,lookup[frozenset(set(s)|{op})]))
        assert len(edges)==16
        out[op]=edges
    return out
EDGES=operator_edges()

def operator_effects(tau):
    return {op:float(np.mean([tau[on]-tau[off] for off,on in edges])) for op,edges in EDGES.items()}

def spectrum(T):
    T=np.asarray(T,float);grand=T.mean();tm=T.mean(axis=1);vm=T.mean(axis=0)
    G=T-tm[:,None]-vm[None,:]+grand
    s=np.linalg.svd(G,compute_uv=False);e=s*s
    tol=max(G.shape)*np.finfo(float).eps*(s[0] if len(s) else 0.0)
    rank=int(np.sum(s>tol))
    part=float((e.sum()**2/np.sum(e*e)) if np.sum(e*e)>0 else 0.0)
    top2=float(e[:2].sum()/e.sum()) if e.sum()>0 else 0.0
    return {'singular_values':[float(x) for x in s],'rank':rank,'participation_rank':part,'top2_energy_fraction':top2}

def main():
    source=sys.argv[1] if len(sys.argv)>1 else 'receipts/p55_source/p55_result.json'
    worlds=load_historical_worlds(source)
    bases=[interaction_basis(w) for w in worlds]
    rows=run();tg=tech(rows)
    if not tg['complete']:
        out={'stage':STAGE,'technical':tg,'constitutional_verdict':'TECHNICAL_HOLD','raw_rows':rows}
    else:
        J={t:jmatrix(rows,t) for t in TASKS}
        assert all(not np.isnan(J[t]).any() for t in TASKS)
        tau={t:{'A':tau_vec(J[t][:32]),'B':tau_vec(J[t][32:])} for t in TASKS}
        tests={}
        # 3 block reproducibility tests
        for i,t in enumerate(TASKS):
            tests[f'repro:{t}']=perm_corr(tau[t]['A']-tau[t]['A'].mean(),tau[t]['B']-tau[t]['B'].mean(),5750+i)
        # 6 robust subspace and 6 robust prediction tests
        for ti,t in enumerate(TASKS):
            for bi,b in enumerate(('A','B')):
                ps=[projection_test(tau[t][b],bases[w],5760+ti*20+bi) for w in range(2)]
                qs=[prediction_test(tau[t][b],bases[w],5790+ti*20+bi) for w in range(2)]
                tests[f'subspace:{t}:{b}']=robust_two_world(ps[0],ps[1])
                tests[f'predict:{t}:{b}']=robust_two_world(qs[0],qs[1])
        h=holm(tests)
        repok=all(tests[f'repro:{t}']['statistic'] is not None and tests[f'repro:{t}']['statistic']>0 and h['rejected'][f'repro:{t}'] for t in TASKS)
        subok=all(tests[f'subspace:{t}:{b}']['statistic'] is not None and tests[f'subspace:{t}:{b}']['statistic']>0 and h['rejected'][f'subspace:{t}:{b}'] for t in TASKS for b in ('A','B'))
        predok=all(tests[f'predict:{t}:{b}']['statistic'] is not None and tests[f'predict:{t}:{b}']['statistic']>0 and h['rejected'][f'predict:{t}:{b}'] for t in TASKS for b in ('A','B'))
        # operator effects / reversals
        op={t:{b:operator_effects(tau[t][b]) for b in ('A','B')} for t in TASKS}
        reversals=[]
        for b in ('A','B'):
            for a,c in itertools.combinations(TASKS,2):
                for opn in OPS:
                    x=op[a][b][opn];y=op[c][b][opn]
                    if x*y<0:
                        reversals.append({'block':b,'task_a':a,'task_b':c,'operator':opn,'effect_a':x,'effect_b':y})
        expanded={}
        for wi,w in enumerate(worlds):
            for b in ('A','B'):
                T=np.vstack([np.stack([w['tau'][t] for t in p53.TASKS]),np.stack([tau[t][b] for t in TASKS])])
                expanded[f'world{wi}_{b}']=spectrum(T)
        artifact=(tg['primary_shadow_disagreement_rate'] or 0)>=.10
        fam={
          'repro_pass':sum(tests[f'repro:{t}']['statistic'] is not None and tests[f'repro:{t}']['statistic']>0 and h['rejected'][f'repro:{t}'] for t in TASKS),
          'subspace_pass':sum(tests[f'subspace:{t}:{b}']['statistic'] is not None and tests[f'subspace:{t}:{b}']['statistic']>0 and h['rejected'][f'subspace:{t}:{b}'] for t in TASKS for b in ('A','B')),
          'predict_pass':sum(tests[f'predict:{t}:{b}']['statistic'] is not None and tests[f'predict:{t}:{b}']['statistic']>0 and h['rejected'][f'predict:{t}:{b}'] for t in TASKS for b in ('A','B'))
        }
        if artifact: verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif repok and subok and predok: verdict='LOW_RANK_INTERACTION_BASIS_TRANSPORTS_WITH_FRESH_TASK_PREDICTION'
        elif repok and subok: verdict='LOW_RANK_INTERACTION_SUBSPACE_TRANSPORT_WITHOUT_VERTEX_PREDICTION'
        elif repok and predok: verdict='ANCHOR_PREDICTION_WITHOUT_GLOBAL_SUBSPACE'
        elif all(x>=1 for x in fam.values()): verdict='PARTIAL_INTERACTION_STRUCTURE_TRANSPORT'
        elif reversals: verdict='OPERATOR_REVERSAL_WITH_NONTRANSPORTABLE_INTERACTION'
        else: verdict='TASK_LOCAL_INTERACTION_UNSTRUCTURED_AT_TESTED_RESOLUTION'
        out={
          'stage':STAGE,
          'design':{'model':MODEL,'tasks':list(TASKS),'draws_per_task':64,'blocks':['A','B'],'vertices':32,'semantic_twins':2,'total_calls':12288,'width':WIDTH,'anchors':ANCHOR.tolist(),'holdout':HOLD.tolist()},
          'technical':tg,
          'historical_training_worlds':[{'assignment':w['assignment'],'rank':bases[i]['rank'],'singular_values':[float(x) for x in bases[i]['singular_values']]} for i,w in enumerate(worlds)],
          'fresh_tau':{t:{b:tau[t][b].tolist() for b in ('A','B')} for t in TASKS},
          'primary_tests':tests,'holm_familywise_005':h,'family_pass_counts':fam,
          'operator_effects':op,'strict_operator_reversals':reversals,
          'expanded_tensor_spectra':expanded,
          'constitutional_verdict':verdict,
          'authority':'P57 tests whether the task×representation interaction promoted by P56 has reproducible and predictive low-dimensional structure on the same GPT-OSS hosted interface. Historical training ambiguity is retained exactly as two worlds. Low rank alone has no constitutive authority; fresh-block reproducibility and anchor→holdout prediction are required.',
          'raw_rows':rows
        }
    Path('receipts').mkdir(exist_ok=True)
    Path('receipts/p57_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:
        assert len(ANCHOR)==8 and len(HOLD)==24 and len(schedule())==12288
        for t in TASKS:
            x=packet(t,'R_F_H_T_L','valid','A')
            assert x['archive_id'].startswith('p57-') and 'u1' in x['available_interventions']
        fake={'a':{'p':.001},'b':{'p':.02},'c':{'p':.2}};h=holm(fake);assert h['rejected']['a']
        print('P57_PRECHECK_PASS')
    else: main()
