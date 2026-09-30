from __future__ import annotations
import json,math,os,random,time,sys
from pathlib import Path
import numpy as np
from p44_field import call,correct,shadow_correct
from p48_seed_fingerprints import panel_cells,make_packet,FRESH_ALIAS

STAGE='EPISTEME-P50'
MODELS=('gemini','gptoss120')
DRAWS=tuple(range(1,33))
GEMINI_SEEDS=tuple(range(5001,5033))
PREFIXES=(1,2,4,8,16)
NPERM=5000

def holm(tests,alpha=.05):
    valid=sorted([(k,v['p']) for k,v in tests.items() if v.get('p') is not None],key=lambda x:x[1])
    m=len(valid);adj={k:None for k in tests};rej={k:False for k in tests};running=0.0
    for i,(k,p) in enumerate(valid):
        running=max(running,min(1.0,(m-i)*p));adj[k]=running
    stop=False
    for i,(k,p) in enumerate(valid):
        if stop: continue
        if p<=alpha/(m-i):rej[k]=True
        else:stop=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def pearson(a,b):
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
    a=a-a.mean();b=b-b.mean()
    na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
    return None if na<=1e-15 or nb<=1e-15 else float(np.dot(a,b)/(na*nb))

def perm_corr_test(a,b,seed):
    obs=pearson(a,b)
    if obs is None:return {'statistic':None,'p':None,'permutations':0}
    rng=random.Random(seed);ge=0
    idx=list(range(len(b)))
    for _ in range(NPERM):
        p=idx.copy();rng.shuffle(p);cur=pearson(a,np.asarray(b)[p])
        if cur is not None and cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def signflip_test(deltas,seed):
    d=np.asarray(deltas,dtype=float);obs=float(d.mean());rng=random.Random(seed);ge=0
    for _ in range(NPERM):
        signs=np.array([1 if rng.random()<.5 else -1 for _ in range(len(d))],dtype=float)
        cur=float(np.mean(d*signs))
        if cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def fresh_packet(cell):
    return make_packet(cell['vertex'],cell['semantic'],FRESH_ALIAS[cell['alias']],True)

def run():
    cells=panel_cells();rows=[]
    for di,draw in enumerate(DRAWS):
        order=list(cells);random.Random(500000+draw).shuffle(order)
        for pos,c in enumerate(order):
            model_order=('gemini','gptoss120') if ((draw+pos)%2==0) else ('gptoss120','gemini')
            pkt=fresh_packet(c)
            for pair_rank,model in enumerate(model_order):
                t0=time.perf_counter_ns()
                try:
                    seed=GEMINI_SEEDS[di] if model=='gemini' else 5000+draw
                    o=call(model,pkt,seed)
                    pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
                except Exception as e:
                    pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
                rows.append({**c,'model':model,'draw':draw,
                             'gemini_seed':GEMINI_SEEDS[di] if model=='gemini' else None,
                             'randomization_label':GEMINI_SEEDS[di] if model=='gemini' else draw,
                             'wave_position':pos,'pair_rank':pair_rank,
                             'latency_ms':(time.perf_counter_ns()-t0)/1e6,
                             'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def tech_gate(rows,model):
    rs=[r for r in rows if r['model']==model]
    ok=sum(r['status']=='OK' for r in rs)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rs)
    return {'ok':ok,'total':len(rs),'complete':ok==len(rs),
            'primary_shadow_disagreements':dis,
            'primary_shadow_disagreement_rate':dis/ok if ok else None}

def matrices(rows,model):
    J=np.full((32,32),np.nan);V=np.full((32,32),np.nan);N=np.full((32,32),np.nan)
    for di,draw in enumerate(DRAWS):
        for vi in range(32):
            pair=[r for r in rows if r['model']==model and r['draw']==draw and r['vertex_index']==vi and r['status']=='OK']
            if len(pair)!=2:continue
            by={r['semantic']:r for r in pair}
            if set(by)!= {'valid','null'}:continue
            V[di,vi]=float(bool(by['valid']['primary_correct']))
            N[di,vi]=float(bool(by['null']['primary_correct']))
            J[di,vi]=float(bool(by['valid']['primary_correct']) and bool(by['null']['primary_correct']))
    return J,V,N

def analyze_model(J,seedbase):
    A=J[:16].mean(axis=0);B=J[16:].mean(axis=0)
    half=perm_corr_test(A,B,seedbase+1)
    curve={}
    for n in PREFIXES:
        p=J[:n].mean(axis=0)
        err=(p-B)**2
        curve[str(n)]={'mse':float(err.mean()),'rmse':float(np.sqrt(err.mean())),
                       'max_abs_error':float(np.max(np.abs(p-B)))}
    dconv=(J[0]-B)**2-(A-B)**2
    conv=signflip_test(dconv,seedbase+2)
    single=((J[:16]-B[None,:])**2).mean(axis=0)
    marginal=(A-B)**2
    bias=signflip_test(single-marginal,seedbase+3)
    return {'pi_A':A.tolist(),'pi_B':B.tolist(),'pi_full':J.mean(axis=0).tolist(),
            'half_surface_reproducibility':half,'convergence_curve':curve,
            'monte_carlo_convergence':conv,'single_draw_selection_bias':bias}

def ranks(a):
    order=np.argsort(np.argsort(np.asarray(a,dtype=float)))
    return order.astype(float)

def main():
    rows=run();gates={m:tech_gate(rows,m) for m in MODELS}
    complete=all(g['complete'] for g in gates.values())
    analyses={};tests={}
    mats={}
    if complete:
        for mi,m in enumerate(MODELS):
            J,V,N=matrices(rows,m);mats[m]=(J,V,N)
            assert not np.isnan(J).any()
            a=analyze_model(J,5050+mi*10);analyses[m]=a
            tests[f'{m}:half_surface']=a['half_surface_reproducibility']
            tests[f'{m}:mc_convergence']=a['monte_carlo_convergence']
            tests[f'{m}:selection_bias']=a['single_draw_selection_bias']
        corr=holm(tests)
        model_gate={}
        for m in MODELS:
            keys=[f'{m}:half_surface',f'{m}:mc_convergence',f'{m}:selection_bias']
            model_gate[m]=all(tests[k]['statistic'] is not None and tests[k]['statistic']>0 and corr['rejected'][k] for k in keys)
        any_mean=any(tests[f'{m}:half_surface']['statistic'] is not None and tests[f'{m}:half_surface']['statistic']>0 and corr['rejected'][f'{m}:half_surface'] for m in MODELS)
        artifact=any((g['primary_shadow_disagreement_rate'] or 0)>=0.10 for g in gates.values())
        if artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif all(model_gate.values()):verdict='CROSS_INTERFACE_RANDOMIZATION_MARGINAL_ESTIMAND_CONSTITUTED'
        elif model_gate['gemini']:verdict='EXPLICIT_SEED_MARGINAL_ESTIMAND_ONLY'
        elif model_gate['gptoss120']:verdict='IMPLICIT_HOSTED_DRAW_MARGINAL_ESTIMAND_ONLY'
        elif any_mean:verdict='REPRODUCIBLE_MEAN_WITH_UNRESOLVED_MONTE_CARLO_AUTHORITY'
        else:verdict='NO_REPRODUCIBLE_RANDOMIZATION_MARGINAL_ESTIMAND'
        secondary={}
        for m,(J,V,N) in mats.items():
            A=J[:16].mean(axis=0);B=J[16:].mean(axis=0)
            secondary[m]={
                'valid_pi_full':V.mean(axis=0).tolist(),
                'null_pi_full':N.mean(axis=0).tolist(),
                'single_draw_mse_to_target':[float(np.mean((J[i]-B)**2)) for i in range(16)],
                'half_rank_correlation':pearson(ranks(A),ranks(B)),
                'mc_standard_error_full':[float(math.sqrt(p*(1-p)/32)) for p in J.mean(axis=0)]}
        secondary['cross_interface_full_surface_correlation']=pearson(
            np.asarray(analyses['gemini']['pi_full']),np.asarray(analyses['gptoss120']['pi_full']))
    else:
        corr=holm({});model_gate={m:False for m in MODELS};secondary={};verdict='TECHNICAL_HOLD'
    out={'stage':STAGE,'design':{'models':list(MODELS),'draws_per_model':32,'vertices':32,'semantic_twins':2,
         'calls_per_model':2048,'total_calls':4096,'estimator_half':16,'target_half':16},
         'technical':gates,'analyses':analyses,'primary_tests':tests if complete else {},
         'holm_familywise_005':corr,'interface_marginal_gate':model_gate,
         'secondary':secondary,'constitutional_verdict':verdict,
         'authority':'P50 tests whether randomization-marginal representation surfaces are reproducible measurement objects under two distinct hosted inference interfaces: explicit Gemini seeds and implicit repeated Groq-hosted GPT-OSS draws. The interfaces are not assumed to share a stochastic mechanism. No provider-internal, neural-state, or behavioral-SVEC claim is licensed.',
         'raw_rows':rows}
    p=Path('receipts/p50_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:
        fake={'b':{'p':.2},'a':{'p':.001},'c':{'p':.02}};h=holm(fake)
        assert h['rejected']['a'] and h['adjusted_p']['a']<=.003000001
        assert len(panel_cells())==64
        print('P50_PRECHECK_PASS')
    else:main()
