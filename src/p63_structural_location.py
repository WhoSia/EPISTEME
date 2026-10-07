from __future__ import annotations
import itertools,json,re
from collections import Counter,OrderedDict
import numpy as np

from p42_reopen import VERTICES
from p44_field import vertex_set
from p48_seed_fingerprints import panel_cells
from p51_sufficiency import beta_mix_cs
from p60_context_interaction import operator_effect,holm

STAGE='EPISTEME-P63'
MODEL='gptoss120'
DRAWS=tuple(range(1,65))
WIDTH=.50
OPS=('R','F','H','T','L')
PRIMARY_OPS=('R','T')
FRAMES=('record','state')
LOCATIONS=('history_externalized','terminal_embedded')
SKINS=(1,2,3)

TASK_SPECS=OrderedDict()
for frame,fc in [('record','R'),('state','S')]:
    for location,lc in [('history_externalized','H'),('terminal_embedded','T')]:
        for skin in SKINS:
            TASK_SPECS[f'{fc}{lc}{skin}']={'frame':frame,'location':location,'skin':skin}
TASKS=tuple(TASK_SPECS)

ALIASES={
 'A':('cobalt63','indigo63',['aux-a2','aux-a8'],['aux-a4','aux-a10']),
 'B':('ember63','opal63',['aux-b1','aux-b7'],['aux-b3','aux-b9']),
 'C':('cedar63','quartz63',['aux-c5','aux-c11'],['aux-c6','aux-c12']),
 'D':('harbor63','zenith63',['aux-d13','aux-d17'],['aux-d19','aux-d23'])
}
SKIN_WORDS={
 1:('alpha','beta','measurement-pipeline-a'),
 2:('gamma','delta','measurement-pipeline-b'),
 3:('epsilon','zeta','measurement-pipeline-c'),
}
FRAME_NOTE={
 'record':'Interpret the archive through retained-record continuity; do not assume the terminal panel is privileged.',
 'state':'Interpret the archive through current-state sufficiency; do not assume the history panel is privileged.'
}


def packet(task,label,semantic,tag):
    spec=TASK_SPECS[task];frame=spec['frame'];location=spec['location'];skin=spec['skin']
    v=vertex_set(label);ren='R' in v;fill='F' in v;rowrev='H' in v;trrev='T' in v;rulerev='L' in v
    plain,renamed,f0,f1=ALIASES[tag];prefix=renamed if ren else plain;fills=f1 if fill else f0
    key=f'{prefix}-target';alt=key+'-counterpart';s0,s1,domain=SKIN_WORDS[skin]
    def tr(x): return [*fills,x] if trrev else [x,*fills]
    decisive='CHALLENGE_SENSITIVE' if semantic=='valid' else 'CHALLENGE_INVARIANT'
    neutral='UNINFORMATIVE'
    hist_code,term_code=(decisive,neutral) if location=='history_externalized' else (neutral,decisive)
    hist=[
      {'slot':s0,'object':key,'trace':tr(key),'evidence_code':hist_code},
      {'slot':s1,'object':alt,'trace':tr(alt),'evidence_code':neutral},
    ]
    term=[
      {'slot':s0,'object':key,'trace':tr(key),'evidence_code':term_code},
      {'slot':s1,'object':alt,'trace':tr(alt),'evidence_code':neutral},
    ]
    if rowrev: hist=list(reversed(hist));term=list(reversed(term))
    target_rule={'object':key,'intervention':'u1','CHALLENGE_SENSITIVE':'different','CHALLENGE_INVARIANT':'none','UNINFORMATIVE':'none'}
    decoy_rule={'object':f'{prefix}-decoy','intervention':'uX','CHALLENGE_SENSITIVE':'none','CHALLENGE_INVARIANT':'none','UNINFORMATIVE':'none'}
    rules=[decoy_rule,target_rule] if rulerev else [target_rule,decoy_rule]
    return {
      'archive_id':f'p63-{frame}-skin{skin}-{tag}-{label}-{semantic}',
      'claim':'The retained terminal summary is sufficient to predict the challenge response.',
      'frame_note':FRAME_NOTE[frame],
      'surface_domain':domain,
      'available_interventions':['u1','uX','uY'],
      'instructions':'Using only this archive, propose the single strongest admissible experiment that could falsify the claim. If the archive does not justify a specific counterexample test, answer NONE. Do not speculate beyond retained evidence.',
      'terminal_panel':term,
      'history_panel':hist,
      'relation_rules':rules,
    }


def token_multiset(pkt):
    # Value/key token multiset; ordering/placement is intentionally ignored.
    s=json.dumps(pkt,sort_keys=True,separators=(',',':'))
    return Counter(re.findall(r'[A-Za-z0-9_-]+',s))


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


def factorial_stats(assign):
    # assign[(frame,location,skin)] -> scalar
    vals=[]
    for f in FRAMES:
        for s in SKINS:
            vals.append(assign[(f,'terminal_embedded',s)]-assign[(f,'history_externalized',s)])
    loc=float(np.mean(vals))
    vals=[]
    for l in LOCATIONS:
        for s in SKINS:
            vals.append(assign[('state',l,s)]-assign[('record',l,s)])
    frame=float(np.mean(vals))
    vals=[]
    for s in SKINS:
        vals.append((assign[('state','terminal_embedded',s)]-assign[('state','history_externalized',s)])-(assign[('record','terminal_embedded',s)]-assign[('record','history_externalized',s)]))
    inter=float(np.mean(vals))
    return {'location':loc,'framing':frame,'interaction':inter}


def exact_factorial_test(values):
    # values maps task -> scalar. All 4 factorial cells occur once per skin.
    observed={(TASK_SPECS[t]['frame'],TASK_SPECS[t]['location'],TASK_SPECS[t]['skin']):values[t] for t in TASKS}
    obs=factorial_stats(observed)
    labels=[('record','history_externalized'),('record','terminal_embedded'),('state','history_externalized'),('state','terminal_embedded')]
    per_skin=[]
    for s in SKINS:
        vs=[observed[(f,l,s)] for f,l in labels]
        per_skin.append(list(itertools.permutations(vs)))
    counts={k:0 for k in obs};n=0
    for p1,p2,p3 in itertools.product(*per_skin):
        a={}
        for s,p in zip(SKINS,(p1,p2,p3)):
            for (f,l),x in zip(labels,p): a[(f,l,s)]=x
        z=factorial_stats(a);n+=1
        for k in obs:
            if abs(z[k])>=abs(obs[k])-1e-15: counts[k]+=1
    assert n==13824
    return {k:{'statistic':obs[k],'p':counts[k]/n,'exact_assignments':n,'direction':'two-sided'} for k in obs}


def self_test():
    assert len(TASKS)==12 and len(panel_cells())==64 and len(VERTICES)==32
    for f in FRAMES:
        for l in LOCATIONS:
            assert sum(x['frame']==f and x['location']==l for x in TASK_SPECS.values())==3
    for f in FRAMES:
        for s in SKINS:
            a=[t for t,x in TASK_SPECS.items() if x['frame']==f and x['location']=='history_externalized' and x['skin']==s][0]
            b=[t for t,x in TASK_SPECS.items() if x['frame']==f and x['location']=='terminal_embedded' and x['skin']==s][0]
            for label in ('I','R','T','R_T'):
                for sem in ('valid','null'):
                    p=packet(a,label,sem,'A');q=packet(b,label,sem,'A')
                    assert p['archive_id']==q['archive_id']
                    assert token_multiset(p)==token_multiset(q)
                    # decisive evidence code occupies opposite panel locations.
                    dp='CHALLENGE_SENSITIVE' if sem=='valid' else 'CHALLENGE_INVARIANT'
                    assert any(x['evidence_code']==dp for x in p['history_panel']) and not any(x['evidence_code']==dp for x in p['terminal_panel'])
                    assert any(x['evidence_code']==dp for x in q['terminal_panel']) and not any(x['evidence_code']==dp for x in q['history_panel'])
    fake={t:(1 if TASK_SPECS[t]['location']=='terminal_embedded' else -1) for t in TASKS}
    z=exact_factorial_test(fake)
    assert z['location']['exact_assignments']==13824 and z['location']['p']<.01
    print('P63_PRECHECK_PASS')

if __name__=='__main__':
    import sys
    if '--self-test' in sys.argv:self_test()
