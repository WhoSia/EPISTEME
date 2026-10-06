from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from p60_context_interaction import *

def load_rows(root):
    rows=[]
    for t in TASKS:
        hits=list(Path(root).rglob(f'{t}.json'))
        if len(hits)!=1: raise RuntimeError(f'{t} hits={hits}')
        d=json.loads(hits[0].read_text());assert d['task']==t and len(d['rows'])==4096
        rows.extend(d['rows'])
    assert len(rows)==49152
    return rows

def tech(rows):
    ok=sum(r['status']=='OK' for r in rows)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    failed=[{k:r.get(k) for k in ('task','draw','cell_index','vertex','semantic','alias','error')} for r in rows if r['status']!='OK']
    return {'ok':ok,'total':len(rows),'complete':ok==len(rows),'failed_count':len(failed),'failed_rows':failed,
            'primary_shadow_disagreements':dis,'primary_shadow_disagreement_rate':dis/ok if ok else None}

def jmatrix(rows,task):
    J=np.full((64,32),np.nan)
    for d in DRAWS:
        for vi in range(32):
            rs=[r for r in rows if r['task']==task and r['draw']==d and r['vertex_index']==vi and r['status']=='OK']
            by={r['semantic']:r for r in rs}
            if set(by)=={'valid','null'}:
                J[d-1,vi]=float(bool(by['valid']['primary_correct']) and bool(by['null']['primary_correct']))
    return J

def task_analysis(J):
    out={'blocks':{}}
    for b,X in [('A',J[:32]),('B',J[32:])]:
        tau=tau_vec(X)
        error=1.0-X.mean(axis=0)
        out['blocks'][b]={'tau':tau.tolist(),'error':error.tolist(),'tau_effects':operator_effect(tau),'error_effects':operator_effect(error)}
    out['task_tau_effects']={op:float(np.mean([out['blocks'][b]['tau_effects'][op] for b in ('A','B')])) for op in OPS}
    out['task_error_effects']={op:float(np.mean([out['blocks'][b]['error_effects'][op] for b in ('A','B')])) for op in OPS}
    return out

def sign_ok(x,s): return x>0 if s>0 else x<0

def strict_gate(analyses,endpoint):
    detail={}
    allok=True
    for op in PRIMARY_OPS:
        for t in TASKS:
            s=expected_sign(op,TASK_SPECS[t]['carrier'])
            taskv=analyses[t][f'task_{endpoint}_effects'][op]
            blocks=[analyses[t]['blocks'][b][f'{endpoint}_effects'][op] for b in ('A','B')]
            ok=sign_ok(taskv,s) and all(sign_ok(x,s) for x in blocks)
            detail[f'{op}:{t}']={'expected_sign':s,'task_effect':taskv,'block_effects':blocks,'pass':ok}
            allok=allok and ok
    return {'pass':allok,'detail':detail}

def critical_gate(analyses,endpoint):
    detail={}
    ok=True
    for t in ('SD1','SD2','SD3'):
        for op in PRIMARY_OPS:
            s=expected_sign(op,'state')
            vals=[analyses[t]['blocks'][b][f'{endpoint}_effects'][op] for b in ('A','B')]
            tv=analyses[t][f'task_{endpoint}_effects'][op]
            cur=sign_ok(tv,s) and all(sign_ok(x,s) for x in vals)
            detail[f'{op}:{t}']={'expected_sign':s,'task_effect':tv,'block_effects':vals,'pass':cur}
            ok=ok and cur
    return {'pass':ok,'detail':detail}

def context_tests(analyses,endpoint):
    carrier={};role={}
    for op in PRIMARY_OPS:
        vals={t:analyses[t][f'task_{endpoint}_effects'][op] for t in TASKS}
        carrier[op]=stratified_factor_test(vals,'carrier','role',positive=(op=='T'))
        role[op]=stratified_factor_test(vals,'role','carrier',positive=True)
    return carrier,role

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rows-root',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    rows=load_rows(a.rows_root);tg=tech(rows)
    if not tg['complete']:
        out={'stage':STAGE,'technical':tg,'constitutional_verdict':'TECHNICAL_HOLD','authority':'No P60 scientific branch opens unless all 49,152 calls are technically valid. Provider failures are not scientific incorrectness.'}
    else:
        analyses={}
        for t in TASKS:
            J=jmatrix(rows,t)
            if np.isnan(J).any(): raise RuntimeError(f'NAN_J:{t}')
            analyses[t]=task_analysis(J)
        tau_carrier,tau_role=context_tests(analyses,'tau')
        err_carrier,err_role=context_tests(analyses,'error')
        tau_tests={f'tau_carrier_{op}':tau_carrier[op] for op in PRIMARY_OPS}
        err_tests={f'error_carrier_{op}':err_carrier[op] for op in PRIMARY_OPS}
        tau_holm=holm(tau_tests);err_holm=holm(err_tests)
        tau_direction=(tau_carrier['R']['statistic']<0 and tau_carrier['T']['statistic']>0)
        err_direction=(err_carrier['R']['statistic']<0 and err_carrier['T']['statistic']>0)
        tau_primary=tau_direction and all(tau_holm['rejected'].values())
        err_primary=err_direction and all(err_holm['rejected'].values())
        tau_strict=strict_gate(analyses,'tau');err_strict=strict_gate(analyses,'error')
        tau_critical=critical_gate(analyses,'tau');err_critical=critical_gate(analyses,'error')
        role_tests={f'tau_role_{op}':tau_role[op] for op in PRIMARY_OPS}
        role_holm=holm(role_tests)
        artifact=(tg['primary_shadow_disagreement_rate'] or 0)>=.10
        if artifact:
            verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif tau_primary and tau_strict['pass'] and tau_critical['pass'] and err_primary and err_strict['pass'] and err_critical['pass']:
            verdict='PROSPECTIVE_CARRIER_INDEXED_R_T_QUALITATIVE_INTERACTION_WITH_BEHAVIORAL_CONCORDANCE'
        elif tau_primary and tau_strict['pass'] and tau_critical['pass']:
            verdict='PROSPECTIVE_CARRIER_INDEXED_R_T_STOPPING_INTERACTION_ONLY'
        elif tau_primary:
            verdict='CARRIER_MODERATION_WITHOUT_STRICT_SIGN_TRANSPORT'
        elif any(role_holm['rejected'].values()):
            verdict='ROLE_OR_HIGHER_ORDER_CONTEXT_MODERATION'
        else:
            verdict='P57_OPERATOR_REVERSAL_TASK_LOCAL_AT_TESTED_CONTEXT_RESOLUTION'
        secondary={}
        for op in OPS:
            vals={t:analyses[t]['task_tau_effects'][op] for t in TASKS}
            secondary[op]={
              'carrier':stratified_factor_test(vals,'carrier','role',positive=(op in ('T',))),
              'role':stratified_factor_test(vals,'role','carrier',positive=True)
            }
        out={
          'stage':STAGE,
          'design':{'tasks':list(TASKS),'task_specs':TASK_SPECS,'model':MODEL,'draws_per_task':64,'blocks':['A','B'],'vertices':32,'semantic_twins':2,'total_calls':49152,'width':WIDTH},
          'technical':tg,'task_analyses':analyses,
          'primary_tau_tests':tau_tests,'primary_tau_holm':tau_holm,
          'behavioral_error_tests':err_tests,'behavioral_error_holm':err_holm,
          'tau_strict_sign_gate':tau_strict,'behavioral_strict_sign_gate':err_strict,
          'tau_critical_quadrant_gate':tau_critical,'behavioral_critical_quadrant_gate':err_critical,
          'role_rival_tests':role_tests,'role_rival_holm':role_holm,
          'secondary_context_tests':secondary,
          'constitutional_verdict':verdict,
          'authority':'Prospective black-box hosted-behavior test of context-indexed qualitative operator interaction. Qualitative-interaction statistics, prompt sensitivity, and interaction analysis are prior art. P60 does not identify neural mechanisms or a universal model law.'
        }
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))

if __name__=='__main__': main()
