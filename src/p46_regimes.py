from __future__ import annotations
import json,math,random
from collections import defaultdict
from pathlib import Path
from p44_field import MODELS,ALIASES,SEMANTICS,VERTICES,packet,call,shadow_correct,correct

STAGE='EPISTEME-P46'
WAVES=((1,4601),(2,4602),(3,4603),(4,4604),(5,4605),(6,4606),(7,4607),(8,4608))
NPERM=5000

def run_model(model):
    cells=[(vi,v,si,s,ai,a) for vi,v in enumerate(VERTICES) for si,s in enumerate(SEMANTICS) for ai,a in enumerate(ALIASES)]
    rows=[]
    for wave,seed in WAVES:
        order=list(cells)
        random.Random(460000 + wave + (0 if model=='gptoss120' else 1000)).shuffle(order)
        for pos,(vi,v,si,s,ai,a) in enumerate(order):
            pkt=packet(v,s,a)
            try:
                o=call(model,pkt,seed); pc=correct(o,s); sc=shadow_correct(o,s); status='OK'; err=None
            except Exception as e:
                pc=sc=None; status='TECHNICAL_FAIL'; err=type(e).__name__+':'+str(e)[:240]
            rows.append({'wave':wave,'seed':seed,'wave_position':pos,'vertex':v,'vertex_index':vi,'semantic':s,'semantic_index':si,
                         'alias':a['tag'],'alias_index':ai,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def gate(rows):
    mins=min(sum(r['status']=='OK' for r in rows if r['vertex']==v and r['semantic']==s and r['alias']==a)
             for v in VERTICES for s in SEMANTICS for a in 'ABCD')
    ok=sum(r['status']=='OK' for r in rows)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    return {'technical_ok':ok,'technical_total':len(rows),'minimum_successes_per_cell':mins,'technical_evaluable':mins>=7,
            'primary_shadow_disagreements':dis,'primary_shadow_disagreement_rate':dis/ok if ok else None}

def sequences(rows,semantic):
    out={}
    for v in VERTICES:
        for a in 'ABCD':
            rs=sorted((r for r in rows if r['semantic']==semantic and r['vertex']==v and r['alias']==a and r['status']=='OK'),key=lambda x:x['wave'])
            if len(rs)!=8: continue
            out[(v,a)]=[float(not r['primary_correct']) for r in rs]
    return out

def lag_stat(seqs):
    num=0.0; den=0.0
    for ys in seqs.values():
        m=sum(ys)/len(ys)
        num+=sum((ys[t]-m)*(ys[t-1]-m) for t in range(1,len(ys)))
        den+=sum((y-m)**2 for y in ys)
    return None if den==0 else num/den

def split_stat(seqs):
    vals=[]
    for ys in seqs.values():
        a=sum(ys[:4])/4; b=sum(ys[4:])/4
        vals.append((a-b)**2)
    return sum(vals)/len(vals) if vals else None

def sync_stat(seqs):
    if not seqs: return None
    wave=[]
    for t in range(8):
        rs=[]
        for ys in seqs.values():
            m=sum(ys)/8
            rs.append(ys[t]-m)
        wave.append(sum(rs)/len(rs))
    mean=sum(wave)/8
    return sum((x-mean)**2 for x in wave)/8

def permute_seqs(seqs,rng):
    out={}
    for k,ys in seqs.items():
        z=list(ys); rng.shuffle(z); out[k]=z
    return out

def test_family(seqs,seed):
    obs={'lag1_persistence':lag_stat(seqs),'split_overdispersion':split_stat(seqs),'wave_synchrony':sync_stat(seqs)}
    ge={k:0 for k in obs}; rng=random.Random(seed)
    for _ in range(NPERM):
        ps=permute_seqs(seqs,rng)
        cur={'lag1_persistence':lag_stat(ps),'split_overdispersion':split_stat(ps),'wave_synchrony':sync_stat(ps)}
        for k in obs:
            if obs[k] is not None and cur[k] is not None and cur[k]>=obs[k]-1e-15: ge[k]+=1
    return {k:{'statistic':obs[k],'p':None if obs[k] is None else (ge[k]+1)/(NPERM+1),'permutations':NPERM} for k in obs}

def holm(tests,alpha=.05):
    pairs=sorted((k,v['p']) for k,v in tests.items() if v['p'] is not None)
    m=len(pairs); adj={k:None for k in tests}; rej={k:False for k in tests}; running=0
    for i,(k,p) in enumerate(pairs):
        running=max(running,min(1,(m-i)*p)); adj[k]=running
    stop=False
    for i,(k,p) in enumerate(pairs):
        if stop: continue
        if p<=alpha/(m-i): rej[k]=True
        else: stop=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def vertex_map(seqs,aliases=None):
    aliases=set(aliases) if aliases else set('ABCD'); out={}
    for v in VERTICES:
        sub={k:y for k,y in seqs.items() if k[0]==v and k[1] in aliases}
        out[v]=lag_stat(sub)
    return out

def cosine_maps(a,b):
    xs=[];ys=[]
    for v in VERTICES:
        if a[v] is None or b[v] is None: continue
        xs.append(a[v]);ys.append(b[v])
    nx=math.sqrt(sum(x*x for x in xs)); ny=math.sqrt(sum(y*y for y in ys))
    return None if not xs or nx==0 or ny==0 else sum(x*y for x,y in zip(xs,ys))/(nx*ny)

def rates(rows):
    out={}
    for s in SEMANTICS:
        out[s]={}
        for v in VERTICES:
            out[s][v]={}
            for a in 'ABCD':
                rs=[r for r in rows if r['semantic']==s and r['vertex']==v and r['alias']==a and r['status']=='OK']
                out[s][v][a]=None if not rs else sum(not r['primary_correct'] for r in rs)/len(rs)
    return out

def main():
    raw={m:run_model(m) for m in MODELS}; gates={m:gate(r) for m,r in raw.items()}
    grouped={}; primary={}
    for mi,m in enumerate(MODELS):
        grouped[m]={}
        for si,s in enumerate(SEMANTICS):
            seq=sequences(raw[m],s); grouped[m][s]=seq
            tf=test_family(seq,4660+mi*10+si)
            for stat,v in tf.items(): primary[f'{m}:{s}:{stat}']=v
    corr=holm(primary)
    model_semantic={}
    model_general={}; model_temporal={}
    for m in MODELS:
        model_semantic[m]={}
        for s in SEMANTICS:
            sig=[st for st in ('lag1_persistence','split_overdispersion','wave_synchrony') if corr['rejected'][f'{m}:{s}:{st}']]
            model_semantic[m][s]=sig
        model_general[m]=all(bool(model_semantic[m][s]) for s in SEMANTICS)
        model_temporal[m]=all('lag1_persistence' in model_semantic[m][s] for s in SEMANTICS)
    any_sig=any(corr['rejected'].values())
    artifact=any((g['primary_shadow_disagreement_rate'] or 0)>=0.10 for g in gates.values())
    if not all(g['technical_evaluable'] for g in gates.values()): verdict='TECHNICAL_HOLD'
    elif artifact: verdict='EVALUATION_ARTIFACT_DOMINANT'
    elif all(model_temporal.values()): verdict='CROSS_FAMILY_TEMPORALLY_PERSISTENT_REGIME_SIGNAL'
    elif any(model_temporal.values()): verdict='MODEL_INDEXED_TEMPORALLY_PERSISTENT_REGIME_SIGNAL'
    elif any(model_general.values()): verdict='MODEL_INDEXED_NONIID_STOCHASTICITY'
    elif any_sig: verdict='SEMANTIC_SPECIFIC_NONIID_SIGNAL'
    else: verdict='IID_BERNOULLI_NOT_REJECTED'
    geom={}
    for m in MODELS:
        geom[m]={}
        for s in SEMANTICS:
            seq=grouped[m][s]; full=vertex_map(seq); ab=vertex_map(seq,'AB'); cd=vertex_map(seq,'CD')
            geom[m][s]={'vertex_lag_map':full,'alias_half_cosine':cosine_maps(ab,cd)}
    out={'stage':STAGE,'design':{'models':list(MODELS),'vertices':32,'semantics':2,'aliases':4,'waves':8,'total_calls':4096},
         'gates':gates,'primary_tests':primary,'holm_familywise_005':corr,'model_semantic_signals':model_semantic,
         'model_general_structured_stochasticity':model_general,'model_temporal_regime':model_temporal,
         'secondary_switching_geometry':geom,'failure_rates':{m:rates(raw[m]) for m in MODELS},
         'constitutional_verdict':verdict,
         'authority':'Prospective repeated black-box behavior under fixed representation×alias×semantic cells. Significant lag/split/wave structure establishes non-exchangeable observed behavior only. Provider/runtime/time effects remain observationally aliased with any internal latent model state; no neural mechanism identification or behavioral-SVEC promotion.',
         'raw_rows':raw}
    p=Path('receipts/p46_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__': main()
