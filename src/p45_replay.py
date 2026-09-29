from __future__ import annotations
import json,math,random
from collections import defaultdict
from pathlib import Path
from p44_field import MODELS,ALIASES,SEMANTICS,VERTICES,packet,call,shadow_correct,correct

STAGE='EPISTEME-P45'
REPS=((1,4501),(2,4502),(3,4503),(4,4504))
P44_BITS={
'gptoss120':{
'valid':{
'A':['01000100100101010000001001000010','00100000000000001000110001000100'],
'B':['10000100001001010000110000000001','00110010001001111000010010010100'],
'C':['00001000110000101011000111000000','00000100111110100101110001000010'],
'D':['00000100000000000000000000000000','00000000100000000101000000000100']},
'null':{
'A':['01100100000000100001001000000101','00100100000000000010011100111000'],
'B':['00010101001000100000100011001000','01001100000000011000000000010001'],
'C':['00000000000010010000000000000000','00000100000100010000010000010000'],
'D':['00001001000110000010100000010000','00001000000000000010100010000010']}},
'gemini':{
'valid':{
'A':['00100000110000110111110000000000','00100000010010111111110101011010'],
'B':['11100010101001100010001001000010','11101111111011110001011001001110'],
'C':['10001010100011010100000011000001','01111011100011111101111110011101'],
'D':['00010011100001110000101010000111','00110011011111111110011011111101']},
'null':{
'A':['00001000000001000001101001100111','00000000000000000000000000000000'],
'B':['00000000001000000010100000101100','00000000000000000000000000000100'],
'C':['00001000000011001000100000011010','00000000000000000000000000000000'],
'D':['00000000000000000001100000001000','00000000000000000000000000000000']}}}

def p44_counts(model,semantic):
    out={}
    for vi,v in enumerate(VERTICES):
        out[v]={}
        for a in 'ABCD':
            out[v][a]=sum(int(bits[vi]) for bits in P44_BITS[model][semantic][a])
    return out

def predictors(model,semantic):
    c=p44_counts(model,semantic); pa={}; pv={}
    for v in VERTICES:
        total=sum(c[v].values())
        pv[v]=(total+1)/10
        for a in 'ABCD': pa[(v,a)]=(c[v][a]+1)/4
    return pa,pv

def logloss(y,p):
    p=max(1e-12,min(1-1e-12,p))
    return -(y*math.log(p)+(1-y)*math.log(1-p))

def score(rows,model,semantic,perm=None):
    pa,pv=predictors(model,semantic)
    vals=[]
    for r in rows:
        if r['semantic']!=semantic or r['status']!='OK': continue
        a=r['alias']
        if perm is not None: a=perm[(r['vertex'],a)]
        y=float(not r['primary_correct']); ap=pa[(r['vertex'],a)]; bp=pv[r['vertex']]
        vals.append((y,ap,bp))
    alias_ll=sum(logloss(y,a) for y,a,b in vals)/len(vals)
    vertex_ll=sum(logloss(y,b) for y,a,b in vals)/len(vals)
    alias_brier=sum((y-a)**2 for y,a,b in vals)/len(vals)
    vertex_brier=sum((y-b)**2 for y,a,b in vals)/len(vals)
    return {'n':len(vals),'alias_logloss':alias_ll,'vertex_logloss':vertex_ll,'logloss_improvement':vertex_ll-alias_ll,
            'alias_brier':alias_brier,'vertex_brier':vertex_brier,'brier_improvement':vertex_brier-alias_brier}

def permutation_test(rows,model,semantic,seed):
    obs=score(rows,model,semantic); rng=random.Random(seed); ge=0; n=5000
    for _ in range(n):
        pm={}
        for v in VERTICES:
            src=list('ABCD'); rng.shuffle(src)
            for dst,s in zip('ABCD',src): pm[(v,dst)]=s
        x=score(rows,model,semantic,pm)['logloss_improvement']
        if x>=obs['logloss_improvement']-1e-15: ge+=1
    obs['p']=(ge+1)/(n+1); obs['permutations']=n
    return obs

def holm(tests,alpha=.05):
    pairs=sorted((k,v['p']) for k,v in tests.items()); m=len(pairs); adj={k:None for k in tests}; rej={k:False for k in tests}; running=0
    for i,(k,p) in enumerate(pairs):
        running=max(running,min(1,(m-i)*p)); adj[k]=running
    stop=False
    for i,(k,p) in enumerate(pairs):
        if stop: continue
        if p<=alpha/(m-i): rej[k]=True
        else: stop=True
    return {'alpha':alpha,'adjusted_p':adj,'rejected':rej}

def variance_decomp(rows,semantic):
    rs=[r for r in rows if r['semantic']==semantic and r['status']=='OK']
    if len(rs)!=32*4*4: return {'status':'INCOMPLETE'}
    y={(r['vertex_index'],r['alias_index'],r['replicate']-1):float(not r['primary_correct']) for r in rs}
    V,A,R=32,4,4; grand=sum(y.values())/(V*A*R)
    mv=[sum(y[v,a,r] for a in range(A) for r in range(R))/(A*R) for v in range(V)]
    ma=[sum(y[v,a,r] for v in range(V) for r in range(R))/(V*R) for a in range(A)]
    mva=[[sum(y[v,a,r] for r in range(R))/R for a in range(A)] for v in range(V)]
    ssV=A*R*sum((x-grand)**2 for x in mv); ssA=V*R*sum((x-grand)**2 for x in ma)
    ssVA=R*sum((mva[v][a]-mv[v]-ma[a]+grand)**2 for v in range(V) for a in range(A))
    ssW=sum((y[v,a,r]-mva[v][a])**2 for v in range(V) for a in range(A) for r in range(R))
    ssT=ssV+ssA+ssVA+ssW
    comp={'vertex':ssV,'alias':ssA,'vertex_alias':ssVA,'within_cell_stochastic':ssW}
    return {'status':'COMPLETE_BALANCED','total_ss':ssT,'ss':comp,'shares':{k:(x/ssT if ssT else 0) for k,x in comp.items()}}

def calibration(rows,model,semantic):
    pa,_=predictors(model,semantic); bins=defaultdict(lambda:[0,0])
    for r in rows:
        if r['semantic']==semantic and r['status']=='OK':
            p=pa[(r['vertex'],r['alias'])]; bins[str(p)][0]+=int(not r['primary_correct']); bins[str(p)][1]+=1
    return {k:{'predicted':float(k),'observed':v[0]/v[1],'n':v[1]} for k,v in sorted(bins.items())}

def run_model(model):
    rows=[]
    for vi,v in enumerate(VERTICES):
        for semantic in SEMANTICS:
            for ai,a in enumerate(ALIASES):
                pkt=packet(v,semantic,a)
                for rep,seed in REPS:
                    try:
                        o=call(model,pkt,seed); pc=correct(o,semantic); sc=shadow_correct(o,semantic); status='OK'; err=None
                    except Exception as e:
                        pc=sc=None; status='TECHNICAL_FAIL'; err=type(e).__name__+':'+str(e)[:240]
                    rows.append({'vertex':v,'vertex_index':vi,'semantic':semantic,'alias':a['tag'],'alias_index':ai,
                                 'replicate':rep,'seed':seed,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    return rows

def model_gate(rows):
    mins=min(sum(r['status']=='OK' for r in rows if r['vertex']==v and r['semantic']==s and r['alias']==a)
             for v in VERTICES for s in SEMANTICS for a in 'ABCD')
    ok=sum(r['status']=='OK' for r in rows); dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    return {'technical_ok':ok,'technical_total':len(rows),'minimum_successes_per_cell':mins,'technical_evaluable':mins>=3,
            'primary_shadow_disagreements':dis,'primary_shadow_disagreement_rate':dis/ok if ok else None}

def main():
    raw={m:run_model(m) for m in MODELS}; gates={m:model_gate(r) for m,r in raw.items()}
    tests={}
    for mi,m in enumerate(MODELS):
        for si,s in enumerate(SEMANTICS): tests[f'{m}:{s}']=permutation_test(raw[m],m,s,4550+mi*10+si)
    correction=holm(tests)
    model_law={}
    for m in MODELS:
        model_law[m]=all(tests[f'{m}:{s}']['logloss_improvement']>0 and correction['rejected'][f'{m}:{s}'] for s in SEMANTICS)
    any_sig=any(tests[k]['logloss_improvement']>0 and correction['rejected'][k] for k in tests)
    if not all(g['technical_evaluable'] for g in gates.values()): verdict='TECHNICAL_HOLD'
    elif any((g['primary_shadow_disagreement_rate'] or 0)>=0.10 for g in gates.values()): verdict='EVALUATION_ARTIFACT_DOMINANT'
    elif all(model_law.values()): verdict='CROSS_FAMILY_ALIAS_CONDITIONAL_PERSISTENCE'
    elif any(model_law.values()): verdict='MODEL_INDEXED_ALIAS_CONDITIONAL_PERSISTENCE'
    elif any_sig: verdict='PARTIAL_ALIAS_PREDICTIVE_SIGNAL'
    else: verdict='NO_ALIAS_PREDICTIVE_PERSISTENCE'
    out={'stage':STAGE,'design':{'models':list(MODELS),'vertices':32,'semantics':2,'aliases':4,'fresh_replicates':4,'total_calls':2048},
         'gates':gates,'primary_tests':tests,'holm_familywise_005':correction,'model_alias_law':model_law,
         'calibration':{m:{s:calibration(raw[m],m,s) for s in SEMANTICS} for m in MODELS},
         'variance_decomposition':{m:{s:variance_decomp(raw[m],s) for s in SEMANTICS} for m in MODELS},
         'constitutional_verdict':verdict,
         'authority':'Prospective predictive persistence for the exact P44 A/B/C/D alias constructions under frozen P42/P44 contracts. Significant prediction would not identify semantic or neural mechanism; nonprediction defeats only persistence of this tested alias-conditioned boundary.',
         'raw_rows':raw}
    p=Path('receipts/p45_result.json'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__': main()
