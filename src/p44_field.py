from __future__ import annotations
import itertools,json,math,os,random
from collections import defaultdict
from pathlib import Path
from groq import Groq
from google import genai
from p42_reopen import PROMPT,VERTICES,parse,correct,groq_raw,gemini_raw

STAGE='EPISTEME-P44'
MODELS={
 'gptoss120':{'provider':'groq','family':'gpt-oss','model':'openai/gpt-oss-120b'},
 'gemini':{'provider':'gemini','family':'gemini','model':'gemini-3.5-flash-lite'},
}
CONTRACTS={
 'gptoss120':{'name':'schema_hidden_medium','format':'schema','reasoning':'medium'},
 'gemini':{'name':'gemini_native_schema','format':'schema','reasoning':None},
}
ALIASES=(
 {'tag':'A','plain':'kappa44','renamed':'lambda44','hist':'trajectory44','fill0':['aux-5','aux-31'],'fill1':['aux-17','aux-23'],'decoy':'decoy-a'},
 {'tag':'B','plain':'sigma44','renamed':'tau44','hist':'pathway44','fill0':['aux-11','aux-41'],'fill1':['aux-19','aux-43'],'decoy':'decoy-b'},
 {'tag':'C','plain':'eta44','renamed':'theta44','hist':'route44','fill0':['aux-13','aux-47'],'fill1':['aux-29','aux-53'],'decoy':'decoy-c'},
 {'tag':'D','plain':'rho44','renamed':'upsilon44','hist':'sequence44','fill0':['aux-7','aux-37'],'fill1':['aux-31','aux-59'],'decoy':'decoy-d'},
)
REPLICATES=((1,4401),(2,4402))
SEMANTICS=('valid','null')
P43_ROWS={
 'gptoss120':'00000001001000100000000001100011',
 'gemini':'00001101000110000001101101100111',
}
FACTORS=('R','F','H','T','L')

def vertex_set(label): return set() if label=='I' else set(label.split('_'))

def packet(label,semantic,alias):
 v=vertex_set(label); renamed='R' in v; filler='F' in v; rh='H' in v; wl='T' in v; rr='L' in v
 prefix=alias['renamed'] if renamed else alias['plain']; key=f"{prefix}-source-q{alias['tag'].lower()}"; alt=key+'-counterpart'
 fills=alias['fill1'] if filler else alias['fill0']
 def tr(t): return [*fills,t] if wl else [t,*fills]
 ha_id=f"{alias['hist']}-alpha"; hb_id=f"{alias['hist']}-beta"
 ha={'history':ha_id,'trace':tr(key)}; hb={'history':hb_id,'trace':tr(alt)}
 histories=[hb,ha] if rh else [ha,hb]
 target={'source':key,'intervention':'u1','response_link':'history-sensitive' if semantic=='valid' else 'history-invariant'}
 decoy={'source':f"{prefix}-{alias['decoy']}",'intervention':'uX','response_link':'irrelevant'}
 relations=[decoy,target] if rr else [target,decoy]
 return {'archive_id':f"ar44-{alias['tag']}-{label}-{semantic}",
  'claim':'The retained terminal summary is sufficient to predict the challenge response.',
  'terminal_observation':{ha_id:'T=stable',hb_id:'T=stable'},'available_interventions':['u1','uX','uY'],
  'instructions':'Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.',
  'surface_domain':'measurement-pipeline','retained_history':histories,'relation_notes':relations}

def call(model_key,pkt,seed):
 cfg=MODELS[model_key]; contract=CONTRACTS[model_key]; text=PROMPT+'\n\nARCHIVE:\n'+json.dumps(pkt,ensure_ascii=False)
 if cfg['provider']=='groq':
  client=Groq(api_key=os.environ['GROQ_API_KEY'],max_retries=4); return parse(groq_raw(client,cfg['model'],text,contract))
 client=genai.Client(api_key=os.environ['GEMINI_API_KEY']); return parse(gemini_raw(client,cfg['model'],text,seed))

def shadow_correct(o,semantic):
 ch=o.get('challenge'); intervention=o.get('intervention'); direction=o.get('predicted_direction')
 abstain=(ch is None or str(ch).strip().upper()=='NONE' or (intervention is None and direction is None))
 if semantic=='null': return abstain
 return (not abstain) and intervention=='u1' and direction=='different'

def run_model(model_key):
 rows=[]
 for vi,label in enumerate(VERTICES):
  for semantic in SEMANTICS:
   for ai,alias in enumerate(ALIASES):
    pkt=packet(label,semantic,alias)
    for rep,seed in REPLICATES:
     try:
      o=call(model_key,pkt,seed); pc=correct(o,semantic); sc=shadow_correct(o,semantic); status='OK'; err=None
     except Exception as e:
      pc=sc=None; status='TECHNICAL_FAIL'; err=type(e).__name__+':'+str(e)[:300]
     rows.append({'vertex':label,'vertex_index':vi,'semantic':semantic,'alias':alias['tag'],'alias_index':ai,'replicate':rep,'seed':seed,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
 return rows

def field(rows,semantic,aliases=None):
 aliases=set(aliases) if aliases else None; out=[]
 for v in VERTICES:
  rs=[r for r in rows if r['vertex']==v and r['semantic']==semantic and r['status']=='OK' and (aliases is None or r['alias'] in aliases)]
  out.append(None if not rs else sum(not r['primary_correct'] for r in rs)/len(rs))
 return out

def walsh(vals):
 if any(x is None for x in vals): return None
 coeff=[]; sets=[vertex_set(v) for v in VERTICES]
 for k in range(6):
  for comb in itertools.combinations(FACTORS,k):
   S=set(comb); c=sum(y*((-1)**len(S & x)) for y,x in zip(vals,sets))/32
   coeff.append({'term':'I' if not comb else '*'.join(comb),'order':k,'coef':c,'energy':c*c})
 return coeff

def lowvec(spec): return [x['coef'] for x in spec if 1<=x['order']<=2]

def cosine(a,b):
 na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(x*x for x in b))
 return None if na==0 or nb==0 else sum(x*y for x,y in zip(a,b))/(na*nb)

def perm_test(a_vals,b_vals,seed):
 sa=walsh(a_vals); sb=walsh(b_vals)
 if sa is None or sb is None:return {'cosine':None,'p':None,'reason':'missing'}
 obs=cosine(lowvec(sa),lowvec(sb))
 if obs is None:return {'cosine':None,'p':None,'reason':'flat-low-order-spectrum'}
 rng=random.Random(seed); ge=0; n=5000
 for _ in range(n):
  b=list(b_vals); rng.shuffle(b); s=walsh(b); c=cosine(lowvec(sa),lowvec(s))
  if c is not None and c>=obs-1e-15: ge+=1
 return {'cosine':obs,'p':(ge+1)/(n+1),'permutations':n}

def holm(tests,alpha=.05):
 valid=[(k,v['p']) for k,v in tests.items() if v.get('p') is not None]; valid.sort(key=lambda x:x[1]); m=len(valid)
 rejected={k:False for k in tests}; adjusted={k:None for k in tests}; running=0
 for i,(k,p) in enumerate(valid):
  running=max(running,min(1,(m-i)*p)); adjusted[k]=running
 stop=False
 for i,(k,p) in enumerate(valid):
  if stop: continue
  if p<=alpha/(m-i): rejected[k]=True
  else: stop=True
 return {'alpha':alpha,'adjusted_p':adjusted,'rejected':rejected}

def anova_decomposition(rows,semantic):
 rs=[r for r in rows if r['semantic']==semantic]
 if any(r['status']!='OK' for r in rs): return {'status':'UNAVAILABLE_MISSING_TECHNICAL'}
 y={(r['vertex_index'],r['alias_index'],r['replicate']-1):float(not r['primary_correct']) for r in rs}
 V,A,R=32,4,2; grand=sum(y.values())/(V*A*R)
 mv=[sum(y[v,a,r] for a in range(A) for r in range(R))/(A*R) for v in range(V)]
 ma=[sum(y[v,a,r] for v in range(V) for r in range(R))/(V*R) for a in range(A)]
 mr=[sum(y[v,a,r] for v in range(V) for a in range(A))/(V*A) for r in range(R)]
 mva=[[sum(y[v,a,r] for r in range(R))/R for a in range(A)] for v in range(V)]
 mvr=[[sum(y[v,a,r] for a in range(A))/A for r in range(R)] for v in range(V)]
 mar=[[sum(y[v,a,r] for v in range(V))/V for r in range(R)] for a in range(A)]
 ssV=A*R*sum((x-grand)**2 for x in mv); ssA=V*R*sum((x-grand)**2 for x in ma); ssR=V*A*sum((x-grand)**2 for x in mr)
 ssVA=R*sum((mva[v][a]-mv[v]-ma[a]+grand)**2 for v in range(V) for a in range(A))
 ssVR=A*sum((mvr[v][r]-mv[v]-mr[r]+grand)**2 for v in range(V) for r in range(R))
 ssAR=V*sum((mar[a][r]-ma[a]-mr[r]+grand)**2 for a in range(A) for r in range(R))
 ssT=sum((x-grand)**2 for x in y.values()); ssVAR=max(0,ssT-ssV-ssA-ssR-ssVA-ssVR-ssAR)
 comps={'vertex':ssV,'alias':ssA,'replicate':ssR,'vertex_alias':ssVA,'vertex_replicate':ssVR,'alias_replicate':ssAR,'residual_threeway':ssVAR}
 return {'status':'COMPLETE_BALANCED','total_ss':ssT,'ss':comps,'shares':{k:(v/ssT if ssT else 0) for k,v in comps.items()}}

def threshold_row(rows):
 bits=[]
 for v in VERTICES:
  good=True
  for s in SEMANTICS:
   rs=[r for r in rows if r['vertex']==v and r['semantic']==s and r['status']=='OK']
   good=good and len(rs)>=7 and sum(bool(r['primary_correct']) for r in rs)>=5
  bits.append('0' if good else '1')
 return ''.join(bits)

def summarize(model_key,rows):
 tech=sum(r['status']=='OK' for r in rows)
 cell_min=min(sum(r['status']=='OK' for r in rows if r['vertex']==v and r['semantic']==s) for v in VERTICES for s in SEMANTICS)
 disagreements=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
 fs={s:field(rows,s) for s in SEMANTICS}; specs={s:walsh(fs[s]) for s in SEMANTICS}
 split={s:perm_test(field(rows,s,['A','B']),field(rows,s,['C','D']),4450+(0 if model_key=='gptoss120' else 100)+(0 if s=='valid' else 1)) for s in SEMANTICS}
 row=threshold_row(rows)
 return {'technical_ok':tech,'technical_total':len(rows),'minimum_successes_per_vertex_semantic':cell_min,'technical_evaluable':cell_min>=7,
  'primary_shadow_disagreements':disagreements,'primary_shadow_disagreement_rate':disagreements/tech if tech else None,
  'failure_fields':fs,'walsh_spectra':specs,'split_half_low_order_tests':split,
  'anova':{s:anova_decomposition(rows,s) for s in SEMANTICS},'diagnostic_majority_row':row,
  'p43_hamming':sum(a!=b for a,b in zip(P43_ROWS[model_key],row))}

def main():
 raw={k:run_model(k) for k in MODELS}; summaries={k:summarize(k,v) for k,v in raw.items()}
 tests={}
 for m in MODELS:
  for s in SEMANTICS: tests[f'within:{m}:{s}']=summaries[m]['split_half_low_order_tests'][s]
 for s in SEMANTICS:
  tests[f'cross:{s}']=perm_test(summaries['gptoss120']['failure_fields'][s],summaries['gemini']['failure_fields'][s],4490+(s=='null'))
 correction=holm(tests)
 all_tech=all(x['technical_evaluable'] for x in summaries.values())
 within_ok=all(correction['rejected'].get(f'within:{m}:{s}',False) for m in MODELS for s in SEMANTICS)
 cross_ok=all(correction['rejected'].get(f'cross:{s}',False) for s in SEMANTICS)
 artifact=max(x['primary_shadow_disagreement_rate'] or 0 for x in summaries.values())
 if not all_tech: verdict='TECHNICALLY_UNEVALUABLE_FIELD'
 elif artifact>=0.10: verdict='EVALUATION_ARTIFACT_DOMINANT'
 elif within_ok and cross_ok: verdict='STOCHASTIC_FIELD_WITH_TRANSPORTABLE_LOW_ORDER_STRUCTURE'
 elif within_ok: verdict='MODEL_INDEXED_STOCHASTIC_FIELDS'
 else: verdict='POINTWISE_INSTABILITY_WITHOUT_STABLE_LOW_ORDER_FIELD'
 out={'stage':STAGE,'models':MODELS,'design':{'vertices':32,'semantic_twins':2,'fresh_alias_blocks':4,'replicates_per_alias':2,'calls_per_model':512,'total_calls':1024},
  'summaries':summaries,'primary_tests':tests,'holm_familywise_005':correction,'constitutional_verdict':verdict,
  'authority':'Prospective black-box behavioral susceptibility fields under P42-frozen provider-native response contracts. Walsh coefficients describe the finite R/F/H/T/L intervention cube; they do not identify neural mechanisms or establish population-level model-family laws. P43 majority rows are diagnostic replication targets only.',
  'raw_rows':raw}
 p=Path('receipts/p44_result.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__': main()
