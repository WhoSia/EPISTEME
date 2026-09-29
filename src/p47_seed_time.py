from __future__ import annotations
import itertools,json,math,random,sys,time
from collections import defaultdict
from pathlib import Path
from p44_field import MODELS,ALIASES,SEMANTICS,VERTICES,packet,call,shadow_correct,correct

STAGE='EPISTEME-P47'
WAVES=tuple(range(1,9))
SEEDS=(4701,4702,4703,4704,4705,4706,4707,4708)
NPERM=5000

def panel(vi,ai): return (vi+ai)%2

def holm(tests,alpha=.05):
    valid=sorted([(k,v['p']) for k,v in tests.items() if v.get('p') is not None],key=lambda x:x[1])
    m=len(valid);adj={k:None for k in tests};rej={k:False for k in tests};running=0.0
    for i,(k,p) in enumerate(valid):
        running=max(running,min(1.0,(m-i)*p));adj[k]=running
    stopped=False
    for i,(k,p) in enumerate(valid):
        if stopped: continue
        if p<=alpha/(m-i): rej[k]=True
        else: stopped=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def self_test():
    fake={'a':{'p':0.20},'b':{'p':0.001},'c':{'p':0.02}}
    h=holm(fake)
    assert h['adjusted_p']['b']<=0.0030000001
    assert h['rejected']['b'] is True
    assert h['adjusted_p']['c']<=0.0400000001
    print('P47_HOLM_SELFTEST_PASS')

def run_experiment():
    rows={m:[] for m in MODELS}
    cells=[(ci,vi,v,si,s,ai,a) for ci,(vi,v,si,s,ai,a) in enumerate(
        (x for vi,v in enumerate(VERTICES) for si,s in enumerate(SEMANTICS) for ai,a in enumerate(ALIASES))
    )]
    for wave in WAVES:
        order=list(cells);random.Random(470000+wave).shuffle(order)
        for pos,(ci,vi,v,si,s,ai,a) in enumerate(order):
            seed_index=(ci+(wave-1))%8
            gem_seed=SEEDS[seed_index]
            model_order=('gptoss120','gemini') if ((wave+pos)%2==0) else ('gemini','gptoss120')
            pair_start=time.perf_counter_ns()
            for pair_rank,model in enumerate(model_order):
                started_ns=time.time_ns();t0=time.perf_counter_ns()
                try:
                    used_seed=gem_seed if model=='gemini' else 4700+wave
                    o=call(model,packet(v,s,a),used_seed)
                    pc=correct(o,s);sc=shadow_correct(o,s);status='OK';err=None
                except Exception as e:
                    pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
                latency_ms=(time.perf_counter_ns()-t0)/1e6
                rows[model].append({
                    'wave':wave,'wave_position':pos,'canonical_cell_index':ci,
                    'vertex':v,'vertex_index':vi,'semantic':s,'semantic_index':si,
                    'alias':a['tag'],'alias_index':ai,'panel':panel(vi,ai),
                    'gemini_seed':gem_seed,'gemini_seed_index':seed_index if model=='gemini' else None,
                    'model_pair_order':model_order,'pair_rank':pair_rank,
                    'started_ns':started_ns,'latency_ms':latency_ms,
                    'pair_elapsed_ms':(time.perf_counter_ns()-pair_start)/1e6,
                    'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def gate(rows):
    mins=min(sum(r['status']=='OK' for r in rows if r['vertex']==v and r['semantic']==s and r['alias']==a)
             for v in VERTICES for s in SEMANTICS for a in 'ABCD')
    ok=sum(r['status']=='OK' for r in rows)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    return {'technical_ok':ok,'technical_total':len(rows),'minimum_successes_per_cell':mins,'technical_evaluable':mins>=7,
            'primary_shadow_disagreements':dis,'primary_shadow_disagreement_rate':dis/ok if ok else None}

def complete_cells(rows,semantic,panel_id=None):
    out={}
    for vi,v in enumerate(VERTICES):
        for ai,a in enumerate('ABCD'):
            if panel_id is not None and panel(vi,ai)!=panel_id: continue
            rs=sorted([r for r in rows if r['semantic']==semantic and r['vertex']==v and r['alias']==a and r['status']=='OK'],key=lambda x:x['wave'])
            if len(rs)==8: out[(v,a)]=rs
    return out

def axis_sequences(rows,semantic,axis,panel_id=None):
    cells=complete_cells(rows,semantic,panel_id);out={}
    for key,rs in cells.items():
        if axis=='wave':
            ordered=sorted(rs,key=lambda r:r['wave'])
        elif axis=='seed':
            if any(r['gemini_seed_index'] is None for r in rs): continue
            ordered=sorted(rs,key=lambda r:r['gemini_seed_index'])
        else: raise ValueError(axis)
        out[key]=[float(not r['primary_correct']) for r in ordered]
    return out

def residual_vector(seqs):
    if not seqs:return None
    vec=[]
    for t in range(8):
        vals=[]
        for ys in seqs.values():
            m=sum(ys)/8;vals.append(ys[t]-m)
        vec.append(sum(vals)/len(vals))
    return vec

def variance_stat(seqs):
    v=residual_vector(seqs)
    if v is None:return None
    m=sum(v)/8
    return sum((x-m)**2 for x in v)/8

def perm_variance_test(seqs,seed):
    obs=variance_stat(seqs)
    if obs is None:return {'statistic':None,'p':None,'permutations':0,'n_cells':len(seqs)}
    rng=random.Random(seed);ge=0
    for _ in range(NPERM):
        ps={}
        for k,ys in seqs.items():
            z=list(ys);rng.shuffle(z);ps[k]=z
        cur=variance_stat(ps)
        if cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM,'n_cells':len(seqs),'residual_vector':residual_vector(seqs)}

def corr(a,b):
    if a is None or b is None:return None
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    xa=[x-ma for x in a];xb=[x-mb for x in b]
    na=math.sqrt(sum(x*x for x in xa));nb=math.sqrt(sum(x*x for x in xb))
    return None if na==0 or nb==0 else sum(x*y for x,y in zip(xa,xb))/(na*nb)

def exact_corr_test(a,b):
    obs=corr(a,b)
    if obs is None:return {'correlation':None,'p':None,'permutations':0}
    ge=0;n=0
    for perm in itertools.permutations(range(8)):
        bp=[b[i] for i in perm];c=corr(a,bp);n+=1
        if c is not None and c>=obs-1e-15:ge+=1
    return {'correlation':obs,'p':ge/n,'permutations':n}

def position_diagnostic(rows,semantic):
    cells=complete_cells(rows,semantic)
    xs=[];ys=[]
    for (v,a),rs in cells.items():
        outcomes=[float(not r['primary_correct']) for r in rs];m=sum(outcomes)/8
        for r,y in zip(rs,outcomes):
            xs.append((r['wave_position']-127.5)/127.5);ys.append(y-m)
    return corr(xs,ys)

def latency_summary(rows):
    by=defaultdict(list)
    for r in rows:
        if r['status']=='OK':by[r['wave']].append(r['latency_ms'])
    return {str(w):{'mean_ms':sum(v)/len(v),'n':len(v)} for w,v in sorted(by.items())}

def main():
    raw=run_experiment();gates={m:gate(rs) for m,rs in raw.items()}
    wave_tests={}
    for mi,m in enumerate(MODELS):
        for si,s in enumerate(SEMANTICS):
            wave_tests[f'{m}:{s}']=perm_variance_test(axis_sequences(raw[m],s,'wave'),4750+mi*10+si)
    wave_holm=holm(wave_tests)
    seed_tests={}
    for si,s in enumerate(SEMANTICS):
        seed_tests[f'gemini:{s}']=perm_variance_test(axis_sequences(raw['gemini'],s,'seed'),4770+si)
    seed_holm=holm(seed_tests)

    loc={}
    for s in SEMANTICS:
        for axis in ('seed','wave'):
            a=residual_vector(axis_sequences(raw['gemini'],s,axis,0))
            b=residual_vector(axis_sequences(raw['gemini'],s,axis,1))
            loc[f'gemini:{s}:{axis}_panel']=exact_corr_test(a,b)
        ga=residual_vector(axis_sequences(raw['gptoss120'],s,'wave'))
        gm=residual_vector(axis_sequences(raw['gemini'],s,'wave'))
        loc[f'cross:{s}:wave']=exact_corr_test(ga,gm)
    loc_holm=holm(loc)

    model_wave={m:all(wave_holm['rejected'][f'{m}:{s}'] for s in SEMANTICS) for m in MODELS}
    gem_seed=all(seed_holm['rejected'][f'gemini:{s}'] for s in SEMANTICS)
    seed_panel=all(loc_holm['rejected'][f'gemini:{s}:seed_panel'] for s in SEMANTICS)
    wave_panel=all(loc_holm['rejected'][f'gemini:{s}:wave_panel'] for s in SEMANTICS)
    cross_wave=all(loc_holm['rejected'][f'cross:{s}:wave'] for s in SEMANTICS)

    if not all(g['technical_evaluable'] for g in gates.values()):
        verdict='TECHNICAL_HOLD'
    elif any((g['primary_shadow_disagreement_rate'] or 0)>=0.10 for g in gates.values()):
        verdict='EVALUATION_ARTIFACT_DOMINANT'
    elif gem_seed and not model_wave['gemini']:
        verdict='P46_SIGNAL_REDUCED_TO_EXPLICIT_SEED_INDEXING'
    elif gem_seed and model_wave['gemini']:
        verdict='SEED_AND_TEMPORAL_COMMON_MODE_BOTH_PRESENT'
    elif model_wave['gemini'] and cross_wave:
        verdict='CONTEMPORANEOUS_CROSS_ARM_TEMPORAL_SIGNAL'
    elif model_wave['gemini']:
        verdict='GEMINI_ARM_SPECIFIC_TEMPORAL_COMMON_MODE'
    elif model_wave['gptoss120']:
        verdict='TEMPORAL_COMMON_MODE_REPLICATED_AFTER_SEED_ORTHOGONALIZATION'
    else:
        verdict='NO_COMMON_MODE_SIGNAL_AFTER_ORTHOGONALIZATION'

    out={'stage':STAGE,'design':{'models':list(MODELS),'vertices':32,'semantics':2,'aliases':4,'waves':8,'total_calls':4096,
                                 'gemini_seed_latin_crossing':True},
         'gates':gates,'primary_wave_tests':wave_tests,'primary_wave_holm':wave_holm,
         'primary_seed_tests':seed_tests,'primary_seed_holm':seed_holm,
         'conditional_localization_tests':loc,'localization_holm':loc_holm,
         'model_wave_replication':model_wave,'gemini_seed_effect':gem_seed,
         'gemini_seed_panel_coherence':seed_panel,'gemini_wave_panel_coherence':wave_panel,
         'cross_arm_temporal_concordance':cross_wave,
         'secondary':{
             'position_correlation':{m:{s:position_diagnostic(raw[m],s) for s in SEMANTICS} for m in MODELS},
             'latency_by_wave':{m:latency_summary(raw[m]) for m in MODELS}},
         'constitutional_verdict':verdict,
         'authority':'Prospective black-box deconfounding of explicit Gemini seed and temporal wave under fixed cells. Seed effects are hosted-inference observables, not neural mechanisms. Residual temporal effects remain compatible with provider/runtime/batching processes; model and provider identity remain confounded within each arm. No behavioral-SVEC promotion.',
         'raw_rows':raw}
    p=Path('receipts/p47_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:self_test()
    else:main()
