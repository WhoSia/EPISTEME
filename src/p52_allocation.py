from __future__ import annotations
import json,math,random,time,sys
from pathlib import Path
import numpy as np
from p44_field import call,correct,shadow_correct
from p48_seed_fingerprints import panel_cells,make_packet,FRESH_ALIAS
from p51_sufficiency import beta_mix_cs

STAGE='EPISTEME-P52'
MODELS=('gemini','gptoss120')
DRAWS=tuple(range(1,65))
GEMINI_SEEDS=tuple(range(5201,5265))
WIDTHS=(0.50,0.40,0.30)
BUDGET_FRACS=(0.25,0.50,0.75)
PRIMARY_W=0.40
PRIMARY_B=512
NPERM=5000

def holm(tests,alpha=.05):
    valid=sorted([(k,v['p']) for k,v in tests.items() if v.get('p') is not None],key=lambda x:x[1])
    m=len(valid);adj={k:None for k in tests};rej={k:False for k in tests};running=0.0
    for i,(k,p) in enumerate(valid):
        running=max(running,min(1.0,(m-i)*p));adj[k]=running
    stop=False
    for i,(k,p) in enumerate(valid):
        if stop:continue
        if p<=alpha/(m-i):rej[k]=True
        else:stop=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def signflip_test(deltas,seed):
    d=np.asarray(deltas,float);obs=float(d.mean());rng=random.Random(seed);ge=0
    for _ in range(NPERM):
        signs=np.array([1 if rng.random()<.5 else -1 for _ in range(len(d))],float)
        cur=float(np.mean(d*signs))
        if cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM}

def pearson(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    a=a-a.mean();b=b-b.mean()
    na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
    return None if na<=1e-15 or nb<=1e-15 else float(np.dot(a,b)/(na*nb))

def fresh_packet(c):
    return make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True)

def schedule():
    cells=panel_cells();jobs=[]
    for di,draw in enumerate(DRAWS):
        order=list(cells);random.Random(520000+draw).shuffle(order)
        for pos,c in enumerate(order):
            model_order=('gemini','gptoss120') if ((draw+pos)%2==0) else ('gptoss120','gemini')
            for pair_rank,m in enumerate(model_order):
                jobs.append((m,draw,di,pos,pair_rank,c))
    assert len(jobs)==8192
    return jobs

def run():
    rows=[]
    for model,draw,di,pos,pair_rank,c in schedule():
        t0=time.perf_counter_ns()
        seed=GEMINI_SEEDS[di] if model=='gemini' else 5200+draw
        try:
            o=call(model,fresh_packet(c),seed)
            pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**c,'model':model,'draw':draw,'gemini_seed':seed if model=='gemini' else None,
                     'wave_position':pos,'pair_rank':pair_rank,'latency_ms':(time.perf_counter_ns()-t0)/1e6,
                     'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def tech(rows,model):
    rs=[r for r in rows if r['model']==model]
    ok=sum(r['status']=='OK' for r in rs)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rs)
    return {'ok':ok,'total':len(rs),'complete':ok==len(rs),'primary_shadow_disagreements':dis,
            'primary_shadow_disagreement_rate':dis/ok if ok else None}

def jmatrix(rows,model):
    J=np.full((64,32),np.nan)
    for di,draw in enumerate(DRAWS):
        for vi in range(32):
            rs=[r for r in rows if r['model']==model and r['draw']==draw and r['vertex_index']==vi and r['status']=='OK']
            if len(rs)!=2:continue
            by={r['semantic']:r for r in rs}
            if set(by)!={'valid','null'}:continue
            J[di,vi]=float(bool(by['valid']['primary_correct']) and bool(by['null']['primary_correct']))
    return J

def width_for(vals,alpha=.05):
    s=int(sum(vals));n=len(vals)
    lo,hi=beta_mix_cs(s,n,alpha)
    return hi-lo,lo,hi

def uniform_policy(X,budget_pairs):
    base=budget_pairs//32;rem=budget_pairs%32
    ys=[];counts=[];intervals=[]
    for v in range(32):
        n=min(32,base+(1 if v<rem else 0))
        vals=X[:n,v].astype(int).tolist()
        ys.append(vals);counts.append(n);intervals.append(width_for(vals))
    return policy_summary(ys,counts,intervals,budget_pairs,'UNIFORM_FIXED')

def adaptive_policy(X,budget_pairs,w,q,kind):
    ys=[[] for _ in range(32)];counts=[0]*32
    spent=0
    # mandatory one observation per vertex
    for v in range(32):
        ys[v].append(int(X[0,v]));counts[v]=1;spent+=1
    q=np.asarray(q,float);qmed=float(np.median(q)) if np.median(q)>0 else 1.0
    while spent<budget_pairs:
        candidates=[]
        for v in range(32):
            if counts[v]>=32:continue
            width,lo,hi=width_for(ys[v])
            if width<=w:continue
            if kind=='ONLINE_WIDTH':score=width
            elif kind=='FIELD_GUIDED_HYBRID':score=width*(q[v]/qmed)
            else:raise ValueError(kind)
            candidates.append((score,-v,v))
        if not candidates:break
        _,_,v=max(candidates)
        nxt=counts[v]
        ys[v].append(int(X[nxt,v]));counts[v]+=1;spent+=1
    intervals=[width_for(y) for y in ys]
    return policy_summary(ys,counts,intervals,spent,kind)

def policy_summary(ys,counts,intervals,spent,name):
    means=[float(sum(y)/len(y)) for y in ys]
    return {'policy':name,'means':means,'counts':counts,'spent_pairs':int(spent),
            'retired_w_primary':None,'intervals':[{'width':float(x[0]),'lo':float(x[1]),'hi':float(x[2])} for x in intervals]}

def reference_summary(X):
    means=X.mean(axis=0)
    intervals=[]
    for v in range(32):
        width,lo,hi=width_for(X[:,v].astype(int).tolist(),.05/32)
        side=1 if lo>.5 else (-1 if hi<.5 else 0)
        intervals.append({'width':width,'lo':lo,'hi':hi,'side':side})
    return {'means':means,'intervals':intervals,'certified_count':sum(z['side']!=0 for z in intervals)}

def policy_decisions(pol):
    out=[]
    for v in range(32):
        vals=None
        # intervals in pol are alpha .05; recompute simultaneous from counts/means via integer successes
        n=pol['counts'][v];s=int(round(pol['means'][v]*n))
        lo,hi=beta_mix_cs(s,n,.05/32)
        side=1 if lo>.5 else (-1 if hi<.5 else 0)
        out.append({'lo':lo,'hi':hi,'side':side})
    return out

def decision_preservation(pol,ref):
    pd=policy_decisions(pol);correct=false=unresolved=0
    for v,r in enumerate(ref['intervals']):
        if r['side']==0:continue
        if pd[v]['side']==r['side']:correct+=1
        elif pd[v]['side']==0:unresolved+=1
        else:false+=1
    return {'reference_certified':ref['certified_count'],'correct_certified':correct,'false_certified':false,'unresolved':unresolved}

def eval_direction(Xpolicy,Xref,q,w,budget_pairs):
    ref=reference_summary(Xref)
    policies={
      'UNIFORM_FIXED':uniform_policy(Xpolicy,budget_pairs),
      'ONLINE_WIDTH':adaptive_policy(Xpolicy,budget_pairs,w,q,'ONLINE_WIDTH'),
      'FIELD_GUIDED_HYBRID':adaptive_policy(Xpolicy,budget_pairs,w,q,'FIELD_GUIDED_HYBRID')}
    for p in policies.values():
        p['retired_w_primary']=sum(z['width']<=w for z in p['intervals'])
        p['decision_preservation']=decision_preservation(p,ref)
        err=(np.asarray(p['means'])-np.asarray(ref['means']))**2
        p['squared_error']=err.tolist();p['mse']=float(err.mean())
    return {'reference':{'means':ref['means'].tolist(),'intervals':ref['intervals'],'certified_count':ref['certified_count']},
            'policies':policies}

def full_analysis(J,q,model_seed):
    A=J[:32];B=J[32:]
    primary={
      'A_to_B':eval_direction(A,B,q[str(PRIMARY_W)],PRIMARY_W,PRIMARY_B),
      'B_to_A':eval_direction(B,A,q[str(PRIMARY_W)],PRIMARY_W,PRIMARY_B)}
    tests={}
    for di,direction in enumerate(('A_to_B','B_to_A')):
        fg=np.asarray(primary[direction]['policies']['FIELD_GUIDED_HYBRID']['squared_error'])
        for ci,comp in enumerate(('UNIFORM_FIXED','ONLINE_WIDTH')):
            ce=np.asarray(primary[direction]['policies'][comp]['squared_error'])
            tests[f'{direction}:{comp}']=signflip_test(ce-fg,model_seed+di*10+ci)
    robust={}
    for w in WIDTHS:
        robust[str(w)]={}
        for frac in BUDGET_FRACS:
            Bp=int(round(1024*frac))
            robust[str(w)][str(frac)]={
              'A_to_B':eval_direction(A,B,q[str(w)],w,Bp),
              'B_to_A':eval_direction(B,A,q[str(w)],w,Bp)}
    alloc_corr={}
    for direction in ('A_to_B','B_to_A'):
        counts=primary[direction]['policies']['FIELD_GUIDED_HYBRID']['counts']
        alloc_corr[direction]=pearson(counts,q[str(PRIMARY_W)])
    return {'primary':primary,'tests':tests,'robustness':robust,'allocation_q_correlation':alloc_corr}

def decision_gate(analysis):
    ok=True;informative=True;detail={}
    for direction in ('A_to_B','B_to_A'):
        ps=analysis['primary'][direction]['policies']
        refn=analysis['primary'][direction]['reference']['certified_count']
        if refn<4:
            informative=False;detail[direction]={'reference_certified':refn,'gate':'SPARSE_REFERENCE'}
            continue
        fg=ps['FIELD_GUIDED_HYBRID']['decision_preservation']
        u=ps['UNIFORM_FIXED']['decision_preservation'];o=ps['ONLINE_WIDTH']['decision_preservation']
        passed=fg['false_certified']==0 and fg['correct_certified']>=u['correct_certified'] and fg['correct_certified']>=o['correct_certified']
        ok=ok and passed;detail[direction]={'reference_certified':refn,'passed':passed,'field':fg,'uniform':u,'online':o}
    return {'informative':informative,'passed':ok if informative else False,'detail':detail}

def robustness_gate(a):
    for direction in ('A_to_B','B_to_A'):
        for frac in ('0.25','0.75'):
            ps=a['robustness'][str(PRIMARY_W)][frac][direction]['policies']
            if ps['FIELD_GUIDED_HYBRID']['mse']>ps['UNIFORM_FIXED']['mse']+1e-15:return False
            if ps['FIELD_GUIDED_HYBRID']['mse']>ps['ONLINE_WIDTH']['mse']+1e-15:return False
    return True

def main():
    base=json.load(open('active/p51_sufficiency_baseline.json'))
    rows=run();gates={m:tech(rows,m) for m in MODELS}
    complete=all(g['complete'] for g in gates.values())
    analyses={};tests={}
    if complete:
        for mi,m in enumerate(MODELS):
            J=jmatrix(rows,m);assert not np.isnan(J).any()
            q=base['mean_tau'][m]
            a=full_analysis(J,q,5250+mi*100);analyses[m]=a
            for direction in ('A_to_B','B_to_A'):
                for comp in ('UNIFORM_FIXED','ONLINE_WIDTH'):
                    tests[f'{m}:{direction}:{comp}']=a['tests'][f'{direction}:{comp}']
        corr=holm(tests)
        primary_pass={}
        for m in MODELS:
            keys=[f'{m}:{d}:{c}' for d in ('A_to_B','B_to_A') for c in ('UNIFORM_FIXED','ONLINE_WIDTH')]
            primary_pass[m]=all(tests[k]['statistic'] is not None and tests[k]['statistic']>0 and corr['rejected'][k] for k in keys)
        decision={m:decision_gate(analyses[m]) for m in MODELS}
        robust={m:robustness_gate(analyses[m]) for m in MODELS}
        artifact=any((g['primary_shadow_disagreement_rate'] or 0)>=.10 for g in gates.values())
        gem_uniform=all(tests[f'gemini:{d}:UNIFORM_FIXED']['statistic']>0 and corr['rejected'][f'gemini:{d}:UNIFORM_FIXED'] for d in ('A_to_B','B_to_A'))
        gem_online=all(tests[f'gemini:{d}:ONLINE_WIDTH']['statistic']>0 and corr['rejected'][f'gemini:{d}:ONLINE_WIDTH'] for d in ('A_to_B','B_to_A'))
        if artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif primary_pass['gemini'] and decision['gemini']['passed'] and robust['gemini'] and not primary_pass['gptoss120']:
            verdict='FIELD_GUIDED_MEASUREMENT_EFFICIENCY_LAW_ON_TESTED_GEMINI_INTERFACE'
        elif primary_pass['gemini'] and decision['gemini']['passed']:
            verdict='LOCAL_FIELD_GUIDED_ALLOCATION_GAIN'
        elif primary_pass['gemini'] and primary_pass['gptoss120']:
            verdict='CROSS_INTERFACE_ADAPTIVE_GAIN_WITHOUT_FIELD_SPECIFICITY'
        elif gem_uniform and not gem_online:
            verdict='RETIREMENT_GAIN_WITHOUT_HISTORICAL_FIELD_VALUE'
        elif all((analyses['gemini']['allocation_q_correlation'][d] or 0)>0 for d in ('A_to_B','B_to_A')):
            verdict='FIELD_PREDICTS_DIFFICULTY_BUT_NOT_DECISION_EFFICIENCY'
        else:verdict='NO_PROSPECTIVE_ALLOCATION_GAIN'
    else:
        corr=holm({});primary_pass={m:False for m in MODELS};decision={};robust={};verdict='TECHNICAL_HOLD'
    out={'stage':STAGE,'design':{'models':list(MODELS),'draws_per_model':64,'vertices':32,'semantic_twins':2,'total_calls':8192,
          'primary_width':PRIMARY_W,'primary_budget_pairs':PRIMARY_B},
         'technical':gates,'analyses':analyses,'primary_tests':tests,'holm_familywise_005':corr,
         'primary_field_gain_gate':primary_pass,'decision_preservation_gate':decision,'robustness_gate':robust,
         'constitutional_verdict':verdict,
         'authority':'P52 prospectively audits frozen allocation policies using complete fresh outcome matrices. Allocation savings are counterfactual policy costs because the full grid is collected for unbiased auditing. Gemini P51 field is authorized; GPT-OSS P51 field is a non-authoritative negative-control prior. No adaptive-sampling novelty or provider mechanism is claimed.',
         'raw_rows':rows}
    p=Path('receipts/p52_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:
        b=json.load(open('active/p51_sufficiency_baseline.json'))
        assert len(b['vertices'])==32 and len(b['mean_tau']['gemini']['0.4'])==32
        fake={'z':{'p':.2},'a':{'p':.001},'q':{'p':.02}};h=holm(fake)
        assert h['rejected']['a'] and h['adjusted_p']['a']<=.003000001
        X=np.tile(np.array([[0,1]*16],float),(32,1))
        u=uniform_policy(X,512);assert all(n==16 for n in u['counts'])
        a=adaptive_policy(X,512,.4,b['mean_tau']['gemini']['0.4'],'FIELD_GUIDED_HYBRID')
        assert sum(a['counts'])<=512 and min(a['counts'])>=1
        assert len(schedule())==8192
        print('P52_PRECHECK_PASS')
    else:main()
