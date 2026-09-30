from __future__ import annotations
import json, math, random, time, sys
from pathlib import Path
import numpy as np
from p48_seed_fingerprints import panel_cells, old_packet, make_packet, FRESH_ALIAS, gemini_call

STAGE='EPISTEME-P49'
SEEDS=tuple(range(4901,4933))
PREFIXES=(4,8,16,32)
NPERM=5000
TRAIN_IDX=np.array([i for i in range(64) if i%4!=3],dtype=int)
HOLD_IDX=np.array([i for i in range(64) if i%4==3],dtype=int)

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
    assert len(TRAIN_IDX)==48 and len(HOLD_IDX)==16
    fake={'z':{'p':.2},'a':{'p':.001},'q':{'p':.02}}
    h=holm(fake)
    assert h['rejected']['a'] and h['adjusted_p']['a']<=.003000001
    print('P49_PRECHECK_PASS')

def schedule():
    cells=panel_cells();jobs=[]
    for ns in ('old','fresh'):
        for seed in SEEDS:
            for c in cells:
                jobs.append((ns,seed,c))
    random.Random(490049).shuffle(jobs)
    assert len(jobs)==4096
    return jobs

def run():
    rows=[]
    for pos,(ns,seed,c) in enumerate(schedule()):
        pkt=old_packet(c['vertex'],c['semantic'],c['alias']) if ns=='old' else make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True)
        t0=time.perf_counter_ns()
        try:
            o=gemini_call(pkt,seed);pc=__import__('p44_field').correct(o,c['semantic']);sc=__import__('p44_field').shadow_correct(o,c['semantic'])
            status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**c,'namespace':ns,'seed':seed,'schedule_position':pos,
                     'latency_ms':(time.perf_counter_ns()-t0)/1e6,'status':status,
                     'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def matrix(rows,ns):
    M=np.full((32,64),np.nan)
    smap={s:i for i,s in enumerate(SEEDS)}
    for r in rows:
        if r['namespace']==ns and r['status']=='OK':
            M[smap[r['seed']],r['cell_index']]=float(not r['primary_correct'])
    return M

def svd_info(X):
    U,s,Vt=np.linalg.svd(X,full_matrices=False)
    tol=max(X.shape)*np.finfo(float).eps*(s[0] if len(s) else 0.0)
    rank=int(np.sum(s>tol))
    return U,s,Vt,rank

def centered_prefix(M,n,cols):
    X=M[:n][:,cols]
    return X-X.mean(axis=0,keepdims=True)

def rank_trajectory(M):
    out={}
    for n in PREFIXES:
        X=centered_prefix(M,n,TRAIN_IDX)
        _,s,_,rank=svd_info(X)
        e=s*s
        part=(e.sum()**2/np.sum(e*e)) if np.sum(e*e)>0 else 0.0
        p=e/e.sum() if e.sum()>0 else np.zeros_like(e)
        er=float(np.exp(-np.sum(p[p>0]*np.log(p[p>0])))) if np.any(p>0) else 0.0
        out[str(n)]={'rank':rank,'ceiling':n-1,'singular_values':[float(x) for x in s],
                     'participation_rank':float(part),'entropy_rank':er}
    return out

def frozen_basis(M):
    X=M[:8][:,TRAIN_IDX]
    mu=X.mean(axis=0)
    E=X-mu
    _,s,Vt,k=svd_info(E)
    return mu,Vt[:k],s,k

def energy_fraction(X,basis):
    den=float(np.sum(X*X))
    if den<=1e-15:return None
    P=(X@basis.T)@basis
    return float(np.sum(P*P)/den)

def energy_test(M,basis,n,seed):
    mu=M[:8][:,TRAIN_IDX].mean(axis=0)
    X=M[8:n][:,TRAIN_IDX]-mu
    obs=energy_fraction(X,basis)
    if obs is None:return {'statistic':None,'p':None,'permutations':0}
    rng=random.Random(seed);ge=0
    for _ in range(NPERM):
        p=list(range(len(TRAIN_IDX)));rng.shuffle(p)
        bp=basis[:,p]
        cur=energy_fraction(X,bp)
        if cur is not None and cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM,'future_rows':n-8}

def basis_block(M,start,end,kmax):
    X=M[start:end][:,TRAIN_IDX]
    E=X-X.mean(axis=0,keepdims=True)
    _,s,Vt,r=svd_info(E)
    k=min(kmax,r)
    return Vt[:k],r,s,k

def grassmann_similarity(A,B):
    k=min(A.shape[0],B.shape[0])
    if k==0:return None
    C=A[:k]@B[:k].T
    sv=np.linalg.svd(C,compute_uv=False)
    return float(np.mean(sv*sv))

def grassmann_test(M,b8,start,end,seed):
    bb,r,s,k=basis_block(M,start,end,b8.shape[0])
    obs=grassmann_similarity(b8[:k],bb)
    if obs is None:return {'statistic':None,'p':None,'permutations':0,'block_rank':r,'k':k}
    rng=random.Random(seed);ge=0
    for _ in range(NPERM):
        p=list(range(len(TRAIN_IDX)));rng.shuffle(p)
        cur=grassmann_similarity(b8[:k],bb[:,p])
        if cur is not None and cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM,'block_rank':r,'k':k,
            'canonical_correlations':[float(x) for x in np.linalg.svd(b8[:k]@bb.T,compute_uv=False)]}

def fit_heldout_map(M,basis):
    T=M[:8][:,TRAIN_IDX];H=M[:8][:,HOLD_IDX]
    muT=T.mean(axis=0);muH=H.mean(axis=0)
    Z=(T-muT)@basis.T
    Y=H-muH
    W=np.linalg.lstsq(Z,Y,rcond=None)[0]
    return muT,muH,W

def heldout_score(M,basis,n):
    muT,muH,W=fit_heldout_map(M,basis)
    T=M[8:n][:,TRAIN_IDX];H=M[8:n][:,HOLD_IDX]
    Z=(T-muT)@basis.T
    pred=muH+Z@W
    base=np.broadcast_to(muH,H.shape)
    pred_mse=float(np.mean((H-pred)**2))
    base_mse=float(np.mean((H-base)**2))
    return base_mse-pred_mse,pred,H,base_mse,pred_mse

def heldout_test(M,basis,n,seed):
    obs,pred,H,base_mse,pred_mse=heldout_score(M,basis,n)
    rng=random.Random(seed);ge=0;nr=H.shape[0]
    for _ in range(NPERM):
        p=list(range(nr));rng.shuffle(p)
        cur=base_mse-float(np.mean((H-pred[p])**2))
        if cur>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM,
            'future_rows':nr,'baseline_mse':base_mse,'predicted_mse':pred_mse}

def namespace_analysis(M,ns,seedbase):
    traj=rank_trajectory(M)
    mu,b8,s8,k8=frozen_basis(M)
    tests={
      f'{ns}:energy16':energy_test(M,b8,16,seedbase+1),
      f'{ns}:energy32':energy_test(M,b8,32,seedbase+2),
      f'{ns}:grassmann_9_16':grassmann_test(M,b8,8,16,seedbase+3),
      f'{ns}:grassmann_17_32':grassmann_test(M,b8,16,32,seedbase+4),
      f'{ns}:heldout16':heldout_test(M,b8,16,seedbase+5),
      f'{ns}:heldout32':heldout_test(M,b8,32,seedbase+6)}
    return {'rank_trajectory':traj,'n8_rank':k8,'n8_singular_values':[float(x) for x in s8],
            'basis':b8,'tests':tests}

def basis_alignment(a,b):
    k=min(a.shape[0],b.shape[0])
    if k==0:return None
    sv=np.linalg.svd(a[:k]@b[:k].T,compute_uv=False)
    return {'mean_squared_canonical_correlation':float(np.mean(sv*sv)),
            'canonical_correlations':[float(x) for x in sv],'k':k}

def main():
    rows=run()
    tech=sum(r['status']=='OK' for r in rows)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    M={ns:matrix(rows,ns) for ns in ('old','fresh')}
    complete=all(not np.isnan(x).any() for x in M.values())
    if complete:
        A={ns:namespace_analysis(M[ns],ns,4990+(0 if ns=='old' else 20)) for ns in ('old','fresh')}
        tests={k:v for ns in ('old','fresh') for k,v in A[ns]['tests'].items()}
        corr=holm(tests)
        ns_pass={}
        for ns in ('old','fresh'):
            keys=[f'{ns}:energy16',f'{ns}:energy32',f'{ns}:grassmann_9_16',f'{ns}:grassmann_17_32',
                  f'{ns}:heldout16',f'{ns}:heldout32']
            ns_pass[ns]=all(tests[k]['statistic'] is not None and tests[k]['statistic']>0 and corr['rejected'][k] for k in keys)
        ranks={ns:{n:A[ns]['rank_trajectory'][str(n)]['rank'] for n in PREFIXES} for ns in ('old','fresh')}
        saturation=all(ranks[ns][32]<31 and ranks[ns][32]==ranks[ns][16] for ns in ('old','fresh'))
        full_ceiling=all(ranks[ns][32]==31 for ns in ('old','fresh'))
        if saturation and all(ns_pass.values()): verdict='SATURATING_SEED_RESPONSE_MANIFOLD'
        elif all(ns_pass.values()): verdict='STABLE_LOW_RANK_CORE_WITH_STOCHASTIC_TAIL'
        elif sum(ns_pass.values())==1: verdict='ARCHIVE_CONDITIONAL_MANIFOLD_ONLY'
        elif full_ceiling: verdict='FINITE_SEED_SPAN_ARTIFACT'
        else: verdict='NO_IDENTIFIABLE_SEED_MANIFOLD'
        compact={ns:{k:v for k,v in A[ns].items() if k!='basis'} for ns in ('old','fresh')}
        align=basis_alignment(A['old']['basis'],A['fresh']['basis'])
    else:
        tests={};corr=holm(tests);ns_pass={'old':False,'fresh':False};ranks={};align=None;compact={}
        verdict='TECHNICAL_HOLD'
    artifact=(dis/tech if tech else 1.0)>=0.10
    if complete and artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
    out={'stage':STAGE,'design':{'seeds':32,'cells':64,'train_cells':48,'heldout_cells':16,'namespaces':2,'total_calls':4096},
         'technical':{'ok':tech,'total':len(rows),'complete':complete,'primary_shadow_disagreements':dis,
                      'primary_shadow_disagreement_rate':dis/tech if tech else None},
         'namespace_analysis':compact,'primary_tests':tests,'holm_familywise_005':corr,
         'namespace_full_gate':ns_pass,'old_fresh_n8_basis_alignment':align,
         'constitutional_verdict':verdict,
         'authority':'P49 tests whether an API-seed-conditioned behavioral response geometry survives seed-count growth, independent seed-block subspace comparison, and prospectively held-out representation cells. Any stable subspace is behavioral and hosted-system-relative, not an identified neural latent space or provider mechanism.',
         'raw_rows':rows}
    p=Path('receipts/p49_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    if '--self-test' in sys.argv:self_test()
    else:main()
