from __future__ import annotations
import itertools,json,math,random,time,sys
from pathlib import Path
import numpy as np
from p42_reopen import VERTICES
from p44_field import call,correct,shadow_correct,vertex_set
from p48_seed_fingerprints import panel_cells,make_packet,FRESH_ALIAS

STAGE='EPISTEME-P51'
MODELS=('gemini','gptoss120')
DRAWS=tuple(range(1,65))
GEMINI_SEEDS=tuple(range(5101,5165))
WIDTHS=(0.50,0.40,0.30)
NPERM=5000
FACTORS=('R','F','H','T','L')

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

def pearson(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    a=a-a.mean();b=b-b.mean()
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

def beta_mix_cs(s,t,alpha):
    if t<=0:return (0.0,1.0)
    logmix=math.lgamma(s+1)+math.lgamma(t-s+1)-math.lgamma(t+2)
    logthr=math.log(1.0/alpha)
    def f(p):
        x=logmix-logthr
        if s:x-=s*math.log(p)
        if t-s:x-=(t-s)*math.log(1-p)
        return x
    ph=s/t
    if s==0:lo=0.0
    else:
        a=1e-12;b=ph
        for _ in range(80):
            m=(a+b)/2
            if f(m)>0:a=m
            else:b=m
        lo=b
    if s==t:hi=1.0
    else:
        a=ph;b=1-1e-12
        for _ in range(80):
            m=(a+b)/2
            if f(m)<=0:a=m
            else:b=m
        hi=a
    return (float(lo),float(hi))

def cs_seq(y,alpha):
    out=[];s=0
    for t,x in enumerate(y,1):
        s+=int(x)
        lo,hi=beta_mix_cs(s,t,alpha)
        out.append({'t':t,'mean':s/t,'lo':lo,'hi':hi,'width':hi-lo})
    return out

def tau_from_seq(seq,w):
    for z in seq:
        if z['width']<=w:return z['t']
    return 33

def schedule():
    cells=panel_cells();jobs=[]
    for di,draw in enumerate(DRAWS):
        order=list(cells);random.Random(510000+draw).shuffle(order)
        for pos,c in enumerate(order):
            order_models=('gemini','gptoss120') if ((draw+pos)%2==0) else ('gptoss120','gemini')
            for pair_rank,m in enumerate(order_models):
                jobs.append((m,draw,di,pos,pair_rank,c))
    assert len(jobs)==8192
    return jobs

def run():
    rows=[]
    for model,draw,di,pos,pair_rank,c in schedule():
        pkt=make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True)
        seed=GEMINI_SEEDS[di] if model=='gemini' else 5100+draw
        t0=time.perf_counter_ns()
        try:
            o=call(model,pkt,seed);pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
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

def block_analysis(X,alpha=.05):
    # X shape 32x32
    seqs=[];taus={str(w):[] for w in WIDTHS}
    for vi in range(32):
        seq=cs_seq(X[:,vi].astype(int).tolist(),alpha)
        seqs.append(seq)
        for w in WIDTHS:taus[str(w)].append(tau_from_seq(seq,w))
    return {'surface':X.mean(axis=0).tolist(),'seqs':seqs,'taus':taus}

def simultaneous_layer(X):
    alpha=.05/32
    out={}
    for w in WIDTHS:
        taus=[]
        for vi in range(32):
            taus.append(tau_from_seq(cs_seq(X[:,vi].astype(int).tolist(),alpha),w))
        out[str(w)]={'taus':taus,'resolved_by_32':sum(t<=32 for t in taus),'all_resolved':all(t<=32 for t in taus)}
    return out

def factor_edges():
    lookup={frozenset(vertex_set(v)):i for i,v in enumerate(VERTICES)}
    out={}
    for f in FACTORS:
        edges=[]
        for i,v in enumerate(VERTICES):
            s=vertex_set(v)
            if f in s:continue
            on=frozenset(set(s)|{f})
            edges.append((i,lookup[on]))
        assert len(edges)==16
        out[f]=edges
    return out

EDGES=factor_edges()

def factor_interval(seqs,t):
    # seqs: 32 vertex individual/simultaneous seqs, t 1-based
    out={}
    for f,edges in EDGES.items():
        los=[];his=[];pts=[]
        for off,on in edges:
            a=seqs[off][t-1];b=seqs[on][t-1]
            los.append(b['lo']-a['hi']);his.append(b['hi']-a['lo']);pts.append(b['mean']-a['mean'])
        lo=float(np.mean(los));hi=float(np.mean(his));pt=float(np.mean(pts))
        sign=1 if lo>0 else (-1 if hi<0 else 0)
        out[f]={'estimate':pt,'lo':lo,'hi':hi,'sign':sign}
    return out

def decision_block(X):
    alpha=.05/32
    seqs=[cs_seq(X[:,vi].astype(int).tolist(),alpha) for vi in range(32)]
    first={f:None for f in FACTORS};final=None
    for t in range(1,33):
        cur=factor_interval(seqs,t)
        for f in FACTORS:
            if first[f] is None and cur[f]['sign']!=0:first[f]={'t':t,**cur[f]}
        if t==32:final=cur
    return {'first_certification':first,'final':final}

def budget(taus):
    fixed=32*32*2
    used=sum(min(int(t),32) for t in taus)*2
    return {'counterfactual_calls':used,'fixed_calls':fixed,'fraction_saved':(fixed-used)/fixed}

def analyze_model(J,seedbase):
    A=J[:32];B=J[32:]
    ba=block_analysis(A);bb=block_analysis(B)
    surface=perm_corr(np.asarray(ba['surface']),np.asarray(bb['surface']),seedbase)
    tests={'surface':surface}
    for wi,w in enumerate(WIDTHS):
        tests[f'tau_{w:.2f}']=perm_corr(np.asarray(ba['taus'][str(w)],float),np.asarray(bb['taus'][str(w)],float),seedbase+10+wi)
    budgets={'A':{},'B':{}}
    for w in WIDTHS:
        budgets['A'][str(w)]=budget(ba['taus'][str(w)])
        budgets['B'][str(w)]=budget(bb['taus'][str(w)])
    da=decision_block(A);db=decision_block(B)
    stable={}
    for f in FACTORS:
        sa=da['final'][f]['sign'];sb=db['final'][f]['sign']
        stable[f]={'A':da['final'][f],'B':db['final'][f],'stable_same_nonzero':sa!=0 and sa==sb}
    return {'block_A':ba,'block_B':bb,'simultaneous_A':simultaneous_layer(A),'simultaneous_B':simultaneous_layer(B),
            'tests':tests,'budgets':budgets,'decision_A':da,'decision_B':db,'stable_factor_decisions':stable}

def main():
    rows=run();gates={m:tech(rows,m) for m in MODELS}
    complete=all(g['complete'] for g in gates.values())
    analyses={};tests={}
    if complete:
        for mi,m in enumerate(MODELS):
            J=jmatrix(rows,m);assert not np.isnan(J).any()
            a=analyze_model(J,5150+mi*100);analyses[m]=a
            tests[f'{m}:surface']=a['tests']['surface']
            for w in WIDTHS:tests[f'{m}:tau:{w:.2f}']=a['tests'][f'tau_{w:.2f}']
        corr=holm(tests)
        surface_gate={m:tests[f'{m}:surface']['statistic'] is not None and tests[f'{m}:surface']['statistic']>0 and corr['rejected'][f'{m}:surface'] for m in MODELS}
        width_gate={m:{str(w):(tests[f'{m}:tau:{w:.2f}']['statistic'] is not None and tests[f'{m}:tau:{w:.2f}']['statistic']>0 and corr['rejected'][f'{m}:tau:{w:.2f}']) for w in WIDTHS} for m in MODELS}
        full={m:surface_gate[m] and all(width_gate[m].values()) for m in MODELS}
        coarse={m:surface_gate[m] and width_gate[m]['0.5'] for m in MODELS}
        artifact=any((g['primary_shadow_disagreement_rate'] or 0)>=.10 for g in gates.values())
        if artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif all(full.values()):verdict='CROSS_INTERFACE_REPRODUCIBLE_SUFFICIENCY_FIELD'
        elif full['gemini']:verdict='EXPLICIT_SEED_REPRODUCIBLE_SUFFICIENCY_FIELD_ONLY'
        elif surface_gate['gptoss120'] and not full['gptoss120'] and not full['gemini']:verdict='GROQ_MARGINAL_SURFACE_RESCUED_WITHOUT_STABLE_SUFFICIENCY_FIELD'
        elif any(coarse.values()):verdict='COARSE_RESOLUTION_SUFFICIENCY_ONLY'
        elif any(surface_gate.values()):verdict='REPRODUCIBLE_MEAN_WITHOUT_REPRODUCIBLE_STOPPING_FIELD'
        else:verdict='NO_REPRODUCIBLE_MEASUREMENT_SUFFICIENCY_FIELD'
    else:
        corr=holm({});surface_gate={m:False for m in MODELS};width_gate={m:{} for m in MODELS};full={m:False for m in MODELS};verdict='TECHNICAL_HOLD'
    out={'stage':STAGE,'design':{'models':list(MODELS),'draws_per_model':64,'block_size':32,'vertices':32,
         'semantic_twins':2,'total_calls':8192,'widths':list(WIDTHS)},
         'technical':gates,'analyses':analyses,'primary_tests':tests,'holm_familywise_005':corr,
         'surface_gate':surface_gate,'width_gate':width_gate,'full_sufficiency_gate':full,
         'constitutional_verdict':verdict,
         'authority':'P51 tests a resolution-indexed stopping-time field for randomization-marginal hosted behavior using anytime-valid beta-binomial mixture confidence sequences. Generic sequential-testing novelty is disclaimed. A stable field is interface-relative measurement structure, not provider-internal or neural mechanism identification.',
         'raw_rows':rows}
    p=Path('receipts/p51_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:
        fake={'z':{'p':.2},'a':{'p':.001},'q':{'p':.02}}
        h=holm(fake);assert h['rejected']['a'] and h['adjusted_p']['a']<=.003000001
        for s,t in [(0,1),(1,1),(8,16)]:
            lo,hi=beta_mix_cs(s,t,.05);assert 0<=lo<=hi<=1 and lo-1e-12<=s/t<=hi+1e-12
        assert len(EDGES)==5 and all(len(x)==16 for x in EDGES.values())
        assert len(schedule())==8192
        print('P51_PRECHECK_PASS')
    else:main()
