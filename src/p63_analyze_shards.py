from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
from p63_structural_location import *


def load_rows(root):
    files=list(Path(root).rglob('*.json'))
    docs=[]
    for p in files:
        try:d=json.loads(p.read_text())
        except Exception:continue
        if isinstance(d,dict) and d.get('task') in TASKS and isinstance(d.get('rows'),list):docs.append(d)
    by={d['task']:d for d in docs}
    if set(by)!=set(TASKS) or len(docs)!=12: raise RuntimeError(f'P63_TASK_SET:{sorted(by)} docs={len(docs)}')
    rows=[]
    for t in TASKS:
        if len(by[t]['rows'])!=4096: raise RuntimeError(f'{t}:{len(by[t]["rows"])}')
        rows.extend(by[t]['rows'])
    if len(rows)!=49152: raise RuntimeError(len(rows))
    return rows


def tech(rows):
    ok=sum(r['status']=='OK' for r in rows)
    dis=sum(r['status']=='OK' and r['primary_correct']!=r['shadow_correct'] for r in rows)
    failed=[{k:r.get(k) for k in ('task','draw','cell_index','vertex','semantic','alias','error')} for r in rows if r['status']!='OK']
    return {'ok':ok,'total':len(rows),'complete':ok==len(rows),'failed_count':len(failed),'failed_rows':failed,
            'primary_shadow_disagreements':dis,'primary_shadow_disagreement_rate':dis/ok if ok else None}


def jmatrix(rows,task):
    J=np.full((64,32),np.nan)
    rs0=[r for r in rows if r['task']==task]
    for d in DRAWS:
        for vi in range(32):
            rs=[r for r in rs0 if r['draw']==d and r['vertex_index']==vi and r['status']=='OK']
            by={r['semantic']:r for r in rs}
            if set(by)=={'valid','null'}:
                J[d-1,vi]=float(bool(by['valid']['primary_correct']) and bool(by['null']['primary_correct']))
    return J


def task_analysis(J):
    out={'blocks':{}}
    for b,X in [('A',J[:32]),('B',J[32:])]:
        tau=tau_vec(X);error=1.0-X.mean(axis=0)
        out['blocks'][b]={'tau':tau.tolist(),'error':error.tolist(),'tau_effects':operator_effect(tau),'error_effects':operator_effect(error)}
    out['task_tau_effects']={op:float(np.mean([out['blocks'][b]['tau_effects'][op] for b in ('A','B')])) for op in OPS}
    out['task_error_effects']={op:float(np.mean([out['blocks'][b]['error_effects'][op] for b in ('A','B')])) for op in OPS}
    return out


def factorial_family(analyses,endpoint):
    byop={}
    for op in PRIMARY_OPS:
        vals={t:analyses[t][f'task_{endpoint}_effects'][op] for t in TASKS}
        byop[op]=exact_factorial_test(vals)
    loc={f'{endpoint}_location_{op}':byop[op]['location'] for op in PRIMARY_OPS}
    frame={f'{endpoint}_framing_{op}':byop[op]['framing'] for op in PRIMARY_OPS}
    inter={f'{endpoint}_interaction_{op}':byop[op]['interaction'] for op in PRIMARY_OPS}
    return byop,loc,holm(loc),frame,holm(frame),inter,holm(inter)


def sign(x): return 1 if x>0 else (-1 if x<0 else 0)


def transport_gate(analyses,endpoint):
    detail={};overall=True
    for op in PRIMARY_OPS:
        orientations=[];opok=True
        for frame in FRAMES:
            for skin in SKINS:
                h=[t for t,x in TASK_SPECS.items() if x['frame']==frame and x['location']=='history_externalized' and x['skin']==skin][0]
                q=[t for t,x in TASK_SPECS.items() if x['frame']==frame and x['location']=='terminal_embedded' and x['skin']==skin][0]
                hv=analyses[h][f'task_{endpoint}_effects'][op];tv=analyses[q][f'task_{endpoint}_effects'][op]
                hb=[analyses[h]['blocks'][b][f'{endpoint}_effects'][op] for b in ('A','B')]
                tb=[analyses[q]['blocks'][b][f'{endpoint}_effects'][op] for b in ('A','B')]
                taskopp=sign(hv)*sign(tv)==-1
                blockopp=all(sign(x)*sign(y)==-1 for x,y in zip(hb,tb))
                ori=(sign(hv),sign(tv));orientations.append(ori)
                cur=taskopp and blockopp and 0 not in ori
                detail[f'{op}:{frame}:skin{skin}']={'history_task_effect':hv,'terminal_task_effect':tv,'history_block_effects':hb,'terminal_block_effects':tb,'orientation':ori,'task_opposite':taskopp,'blocks_opposite':blockopp,'pass':cur}
                opok=opok and cur
        orientation_transport=len(set(orientations))==1 and orientations[0][0]*orientations[0][1]==-1
        detail[f'{op}:orientation_transport']={'orientations':orientations,'pass':orientation_transport}
        opok=opok and orientation_transport;overall=overall and opok
    return {'pass':overall,'detail':detail}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rows-root',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    rows=load_rows(a.rows_root);tg=tech(rows)
    if not tg['complete']:
        out={'stage':STAGE,'technical':tg,'constitutional_verdict':'TECHNICAL_HOLD',
             'authority':'No P63 scientific branch opens unless all 49,152 calls are technically valid. Any bounded failed-cell recovery requires a new P-number.'}
    else:
        analyses={}
        for t in TASKS:
            J=jmatrix(rows,t)
            if np.isnan(J).any():raise RuntimeError(f'NAN_J:{t}')
            analyses[t]=task_analysis(J)
        tau_by,tau_loc,tau_loc_h,tau_frame,tau_frame_h,tau_int,tau_int_h=factorial_family(analyses,'tau')
        err_by,err_loc,err_loc_h,err_frame,err_frame_h,err_int,err_int_h=factorial_family(analyses,'error')
        tau_primary=all(tau_loc_h['rejected'].values());err_primary=all(err_loc_h['rejected'].values())
        tau_gate=transport_gate(analyses,'tau');err_gate=transport_gate(analyses,'error')
        framing_rival=any(tau_frame_h['rejected'].values()) or any(tau_int_h['rejected'].values())
        artifact=(tg['primary_shadow_disagreement_rate'] or 0)>=.10
        if artifact:verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif tau_primary and tau_gate['pass'] and err_primary and err_gate['pass']:
            verdict='STRUCTURAL_LOCATION_INDEXED_R_T_SIGN_REVERSAL_WITH_BEHAVIORAL_CONCORDANCE'
        elif tau_primary and tau_gate['pass']:
            verdict='STRUCTURAL_LOCATION_INDEXED_R_T_STOPPING_INTERACTION_ONLY'
        elif tau_primary:
            verdict='STRUCTURAL_LOCATION_MODERATION_WITHOUT_STRICT_SIGN_TRANSPORT'
        elif framing_rival:
            verdict='FRAMING_OR_FRAME_STRUCTURE_INTERACTION_DOMINANT'
        else:
            verdict='POST_P62_R_T_EFFECTS_REMAIN_TASK_LOCAL_UNDER_STRUCTURAL_INTERVENTION'
        out={
          'stage':STAGE,
          'design':{'tasks':list(TASKS),'task_specs':TASK_SPECS,'model':MODEL,'draws_per_task':64,'blocks':['A','B'],'vertices':32,'semantic_twins':2,'total_calls':49152,'width':WIDTH,'exact_factorial_assignments':13824},
          'technical':tg,'task_analyses':analyses,
          'stopping_factorial_by_operator':tau_by,'stopping_location_tests':tau_loc,'stopping_location_holm':tau_loc_h,
          'stopping_framing_tests':tau_frame,'stopping_framing_holm':tau_frame_h,'stopping_interaction_tests':tau_int,'stopping_interaction_holm':tau_int_h,
          'behavioral_factorial_by_operator':err_by,'behavioral_location_tests':err_loc,'behavioral_location_holm':err_loc_h,
          'behavioral_framing_tests':err_frame,'behavioral_framing_holm':err_frame_h,'behavioral_interaction_tests':err_int,'behavioral_interaction_holm':err_int_h,
          'stopping_transport_gate':tau_gate,'behavioral_transport_gate':err_gate,
          'constitutional_verdict':verdict,
          'authority':'Prospective factorial black-box intervention separating semantic framing from the physical location of decisive evidence within a lexically matched synthetic archive grammar. Strong branches require exact structural-location tests plus strict matched-skin sign transport; no neural or universal-law claim is licensed.'
        }
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))

if __name__=='__main__':main()
