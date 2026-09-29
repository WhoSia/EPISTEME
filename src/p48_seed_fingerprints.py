from __future__ import annotations
import itertools,json,math,random,time
from pathlib import Path
import numpy as np
from p42_reopen import VERTICES
from p44_field import PROMPT,MODELS,CONTRACTS,parse,correct,shadow_correct,groq_raw,gemini_raw,vertex_set
from p44_field import ALIASES as OLD_ALIASES
from google import genai

STAGE='EPISTEME-P48'
OLD_SEEDS=(4701,4702,4703,4704,4705,4706,4707,4708)
FRESH_SEEDS=(4801,4802,4803,4804,4805,4806,4807,4808)
NPERM=5000
FRESH_ALIASES=(
 {'tag':'A','plain':'omicron48','renamed':'pi48','hist':'ledger48','fill0':['aux-61','aux-83'],'fill1':['aux-67','aux-89'],'decoy':'shadow-a'},
 {'tag':'B','plain':'chi48','renamed':'psi48','hist':'record48','fill0':['aux-71','aux-97'],'fill1':['aux-73','aux-101'],'decoy':'shadow-b'},
 {'tag':'C','plain':'iota48','renamed':'zeta48','hist':'register48','fill0':['aux-79','aux-103'],'fill1':['aux-107','aux-109'],'decoy':'shadow-c'},
 {'tag':'D','plain':'beta48','renamed':'gamma48','hist':'chronicle48','fill0':['aux-113','aux-127'],'fill1':['aux-131','aux-137'],'decoy':'shadow-d'},
)
OLD_ALIAS={a['tag']:a for a in OLD_ALIASES}
FRESH_ALIAS={a['tag']:a for a in FRESH_ALIASES}

def load_baseline():
    d=json.load(open('active/p47_seed_panel_baseline.json'))
    assert tuple(d['seeds'])==OLD_SEEDS
    M=np.array([[int(x) for x in d['failure_bitstrings'][str(s)]] for s in OLD_SEEDS],dtype=float)
    assert M.shape==(8,64)
    return M

def panel_cells():
    out=[]
    for vi,v in enumerate(VERTICES):
        a='ABCD'[vi%4]
        for si,s in enumerate(('valid','null')):
            out.append({'cell_index':len(out),'vertex':v,'vertex_index':vi,'alias':a,'semantic':s,'semantic_index':si})
    assert len(out)==64
    return out

def make_packet(label,semantic,alias,fresh=False):
    v=vertex_set(label);renamed='R' in v;filler='F' in v;rh='H' in v;wl='T' in v;rr='L' in v
    prefix=alias['renamed'] if renamed else alias['plain'];key=f"{prefix}-source-p48";alt=key+'-counterpart'
    fills=alias['fill1'] if filler else alias['fill0']
    def tr(t): return [*fills,t] if wl else [t,*fills]
    ha_id=f"{alias['hist']}-alpha";hb_id=f"{alias['hist']}-beta"
    ha={'history':ha_id,'trace':tr(key)};hb={'history':hb_id,'trace':tr(alt)}
    histories=[hb,ha] if rh else [ha,hb]
    target={'source':key,'intervention':'u1','response_link':'history-sensitive' if semantic=='valid' else 'history-invariant'}
    decoy={'source':f"{prefix}-{alias['decoy']}",'intervention':'uX','response_link':'irrelevant'}
    relations=[decoy,target] if rr else [target,decoy]
    ns='fresh' if fresh else 'old'
    return {'archive_id':f"ar48-{ns}-{alias['tag']}-{label}-{semantic}",
      'claim':'The retained terminal summary is sufficient to predict the challenge response.',
      'terminal_observation':{ha_id:'T=stable',hb_id:'T=stable'},'available_interventions':['u1','uX','uY'],
      'instructions':'Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.',
      'surface_domain':'measurement-pipeline','retained_history':histories,'relation_notes':relations}

def old_packet(label,semantic,tag):
    # Exact P47/P44 namespace, not a P48 relabel.
    from p44_field import packet
    return packet(label,semantic,OLD_ALIAS[tag])

def gemini_call(pkt,seed):
    cfg=MODELS['gemini'];client=genai.Client(api_key=__import__('os').environ['GEMINI_API_KEY'])
    text=PROMPT+'\n\nARCHIVE:\n'+json.dumps(pkt,ensure_ascii=False)
    return parse(gemini_raw(client,cfg['model'],text,seed))

def schedule():
    cells=panel_cells();jobs=[]
    for lane,seeds,fresh_ns in (
        ('old_seed_exact_replay',OLD_SEEDS,False),
        ('old_seed_fresh_archive',OLD_SEEDS,True),
        ('fresh_seed_old_archive',FRESH_SEEDS,False),
        ('fresh_seed_fresh_archive',FRESH_SEEDS,True)):
        for seed in seeds:
            for c in cells:
                jobs.append((lane,seed,fresh_ns,c))
    random.Random(480048).shuffle(jobs)
    assert len(jobs)==2048
    return jobs

def run():
    rows=[]
    for pos,(lane,seed,fresh_ns,c) in enumerate(schedule()):
        pkt=make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True) if fresh_ns else old_packet(c['vertex'],c['semantic'],c['alias'])
        t0=time.perf_counter_ns()
        try:
            o=gemini_call(pkt,seed);pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**c,'lane':lane,'seed':seed,'fresh_archive':fresh_ns,'schedule_position':pos,
                     'latency_ms':(time.perf_counter_ns()-t0)/1e6,'status':status,
                     'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def lane_matrix(rows,lane,seeds):
    M=np.full((8,64),np.nan)
    sidx={s:i for i,s in enumerate(seeds)}
    for r in rows:
        if r['lane']==lane and r['status']=='OK':
            M[sidx[r['seed']],r['cell_index']]=float(not r['primary_correct'])
    return M

def centered(M):
    return M-np.nanmean(M,axis=0,keepdims=True)

def row_cos(a,b):
    na=np.linalg.norm(a);nb=np.linalg.norm(b)
    return np.nan if na==0 or nb==0 else float(np.dot(a,b)/(na*nb))

def diagonal_cos(A,B,perm=None):
    EA=centered(A);EB=centered(B)
    if perm is not None: EB=EB[list(perm)]
    vals=[row_cos(EA[i],EB[i]) for i in range(8)]
    vals=[x for x in vals if not math.isnan(x)]
    return float(np.mean(vals)) if vals else None

def exact_seed_perm_test(A,B):
    obs=diagonal_cos(A,B);ge=0;n=0
    if obs is None:return {'statistic':None,'p':None,'permutations':0}
    for p in itertools.permutations(range(8)):
        x=diagonal_cos(A,B,p);n+=1
        if x is not None and x>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':ge/n,'permutations':n}

def train_basis(M):
    E=centered(M)
    u,s,vt=np.linalg.svd(E,full_matrices=False)
    tol=max(E.shape)*np.finfo(float).eps*(s[0] if len(s) else 0)
    rank=int(np.sum(s>tol))
    return E,vt[:rank],s,rank

def projection_stat(M,basis):
    E=centered(M);vals=[]
    for row in E:
        den=float(np.dot(row,row))
        if den<=1e-15:continue
        proj=(row@basis.T)@basis
        vals.append(float(np.dot(proj,proj)/den))
    return float(np.mean(vals)) if vals else None,vals

def projection_perm_test(M,basis,seed):
    obs,per=projection_stat(M,basis)
    if obs is None:return {'statistic':None,'p':None,'permutations':0,'per_seed':per}
    rng=random.Random(seed);ge=0
    for _ in range(NPERM):
        p=list(range(64));rng.shuffle(p)
        x,_=projection_stat(M[:,p],basis)
        if x>=obs-1e-15:ge+=1
    return {'statistic':obs,'p':(ge+1)/(NPERM+1),'permutations':NPERM,'per_seed':per}

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

def agreement(A,B,same=True):
    vals=[]
    if same:
        for i in range(8):vals.extend((A[i]==B[i]).astype(float).tolist())
    else:
        for i in range(8):
            for j in range(8):
                if i!=j:vals.extend((A[i]==B[j]).astype(float).tolist())
    return float(np.mean(vals))

def cell_variance(M):
    return np.var(M,axis=0).tolist()

def self_test():
    base=load_baseline();_,basis,s,rank=train_basis(base)
    assert base.shape==(8,64)
    assert 1<=rank<=7
    fake={'z':{'p':.2},'a':{'p':.001},'q':{'p':.02}}
    h=holm(fake);assert h['rejected']['a'] and h['adjusted_p']['a']<=.003000001
    assert len(schedule())==2048
    print('P48_PRECHECK_PASS',rank,[float(x) for x in s])

def main():
    baseline=load_baseline();rows=run()
    mats={
      'old_exact':lane_matrix(rows,'old_seed_exact_replay',OLD_SEEDS),
      'old_fresh':lane_matrix(rows,'old_seed_fresh_archive',OLD_SEEDS),
      'fresh_old':lane_matrix(rows,'fresh_seed_old_archive',FRESH_SEEDS),
      'fresh_fresh':lane_matrix(rows,'fresh_seed_fresh_archive',FRESH_SEEDS)}
    tech=sum(r['status']=='OK' for r in rows);dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    complete=all(not np.isnan(M).any() for M in mats.values())
    _,basis,svals,rank=train_basis(baseline)
    tests={
      'exact_replay_identity':exact_seed_perm_test(baseline,mats['old_exact']) if complete else {'p':None},
      'old_seed_cross_archive_identity':exact_seed_perm_test(baseline,mats['old_fresh']) if complete else {'p':None},
      'fresh_seed_cross_archive_identity':exact_seed_perm_test(mats['fresh_old'],mats['fresh_fresh']) if complete else {'p':None},
      'fresh_seed_old_archive_subspace':projection_perm_test(mats['fresh_old'],basis,4861) if complete else {'p':None},
      'fresh_seed_fresh_archive_subspace':projection_perm_test(mats['fresh_fresh'],basis,4862) if complete else {'p':None}}
    corr=holm(tests)
    repro=complete and tests['exact_replay_identity']['statistic'] is not None and tests['exact_replay_identity']['statistic']>0 and corr['rejected']['exact_replay_identity']
    transport=repro and corr['rejected']['old_seed_cross_archive_identity'] and corr['rejected']['fresh_seed_cross_archive_identity']
    subspace=corr['rejected']['fresh_seed_old_archive_subspace'] and corr['rejected']['fresh_seed_fresh_archive_subspace']
    artifact=(dis/tech if tech else 1.0)>=0.10
    if not complete:verdict='TECHNICAL_HOLD'
    elif artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
    elif transport and subspace:verdict='TRANSPORTABLE_LOW_DIMENSIONAL_SEED_RANDOMIZATION_LAW'
    elif subspace and not transport:verdict='STABLE_SEED_EFFECT_SUBSPACE_WITHOUT_IDENTITY_TRANSPORT'
    elif transport:verdict='TRANSPORTABLE_SEED_COORDINATE_WITHOUT_FRESH_SEED_LAW'
    elif repro:verdict='REPRODUCIBLE_SEED_INTERVENTION_WITHOUT_ARCHIVE_TRANSPORT'
    else:verdict='SEED_IDENTITY_NOT_REPRODUCIBLE'
    secondary={
      'same_seed_same_archive_agreement':agreement(baseline,mats['old_exact']) if complete else None,
      'different_seed_same_archive_agreement':agreement(baseline,mats['old_exact'],False) if complete else None,
      'same_seed_cross_archive_agreement_old':agreement(baseline,mats['old_fresh']) if complete else None,
      'same_seed_cross_archive_agreement_fresh':agreement(mats['fresh_old'],mats['fresh_fresh']) if complete else None,
      'training_singular_values':[float(x) for x in svals],'training_effect_rank':rank,
      'baseline_cell_between_seed_variance':cell_variance(baseline)}
    out={'stage':STAGE,'design':{'model':'gemini-3.5-flash-lite','panel_cells':64,'old_seeds':list(OLD_SEEDS),
          'fresh_seeds':list(FRESH_SEEDS),'lanes':4,'total_calls':2048},
      'technical':{'ok':tech,'total':len(rows),'complete':complete,'primary_shadow_disagreements':dis,
                   'primary_shadow_disagreement_rate':dis/tech if tech else None},
      'primary_tests':tests,'holm_familywise_005':corr,
      'gates':{'reproducible_intervention':repro,'transportable_coordinate':transport,'fresh_seed_subspace':subspace},
      'secondary':secondary,'constitutional_verdict':verdict,
      'authority':'Seed integers are nominal API interventions. P48 can establish repeatability, archive-isomorphism transport, and an out-of-sample response subspace for hosted behavioral susceptibility; it cannot identify neural RNG state, batching, hardware, provider internals, or a numeric geometry over seed values.',
      'raw_rows':rows}
    p=Path('receipts/p48_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':
    import sys
    if '--self-test' in sys.argv:self_test()
    else:main()
