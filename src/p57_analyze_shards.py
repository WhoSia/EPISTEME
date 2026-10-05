from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np
from p57_interaction_tensor import *
import p53_cross_task as p53

def load_rows(root):
    rows=[]
    for t in TASKS:
        hits=list(Path(root).rglob(f'{t}.json'))
        if len(hits)!=1: raise RuntimeError(f'{t} hits={hits}')
        d=json.loads(hits[0].read_text());assert d['task']==t and len(d['rows'])==4096
        rows.extend(d['rows'])
    assert len(rows)==12288
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rows-root',required=True);ap.add_argument('--p55',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    worlds=load_historical_worlds(a.p55);bases=[interaction_basis(w) for w in worlds]
    rows=load_rows(a.rows_root);tg=tech(rows)
    if not tg['complete']:
        out={'stage':STAGE,'technical':tg,'constitutional_verdict':'TECHNICAL_HOLD','raw_rows':rows}
    else:
        J={t:jmatrix(rows,t) for t in TASKS};assert all(not np.isnan(J[t]).any() for t in TASKS)
        tau={t:{'A':tau_vec(J[t][:32]),'B':tau_vec(J[t][32:])} for t in TASKS}
        tests={}
        for i,t in enumerate(TASKS):
            tests[f'repro:{t}']=perm_corr(tau[t]['A']-tau[t]['A'].mean(),tau[t]['B']-tau[t]['B'].mean(),5750+i)
        for ti,t in enumerate(TASKS):
            for bi,b in enumerate(('A','B')):
                ps=[projection_test(tau[t][b],bases[w],5760+ti*20+bi) for w in range(2)]
                qs=[prediction_test(tau[t][b],bases[w],5790+ti*20+bi) for w in range(2)]
                tests[f'subspace:{t}:{b}']=robust_two_world(ps[0],ps[1])
                tests[f'predict:{t}:{b}']=robust_two_world(qs[0],qs[1])
        h=holm(tests)
        repok=all(tests[f'repro:{t}']['statistic'] is not None and tests[f'repro:{t}']['statistic']>0 and h['rejected'][f'repro:{t}'] for t in TASKS)
        subok=all(tests[f'subspace:{t}:{b}']['statistic'] is not None and tests[f'subspace:{t}:{b}']['statistic']>0 and h['rejected'][f'subspace:{t}:{b}'] for t in TASKS for b in ('A','B'))
        predok=all(tests[f'predict:{t}:{b}']['statistic'] is not None and tests[f'predict:{t}:{b}']['statistic']>0 and h['rejected'][f'predict:{t}:{b}'] for t in TASKS for b in ('A','B'))
        op={t:{b:operator_effects(tau[t][b]) for b in ('A','B')} for t in TASKS}
        reversals=[]
        for b in ('A','B'):
            for x,y in itertools.combinations(TASKS,2):
                for opn in OPS:
                    a1=op[x][b][opn];a2=op[y][b][opn]
                    if a1*a2<0:reversals.append({'block':b,'task_a':x,'task_b':y,'operator':opn,'effect_a':a1,'effect_b':a2})
        expanded={}
        for wi,w in enumerate(worlds):
            for b in ('A','B'):
                T=np.vstack([np.stack([w['tau'][t] for t in p53.TASKS]),np.stack([tau[t][b] for t in TASKS])])
                expanded[f'world{wi}_{b}']=spectrum(T)
        artifact=(tg['primary_shadow_disagreement_rate'] or 0)>=.10
        fam={'repro_pass':sum(tests[f'repro:{t}']['statistic'] is not None and tests[f'repro:{t}']['statistic']>0 and h['rejected'][f'repro:{t}'] for t in TASKS),
             'subspace_pass':sum(tests[f'subspace:{t}:{b}']['statistic'] is not None and tests[f'subspace:{t}:{b}']['statistic']>0 and h['rejected'][f'subspace:{t}:{b}'] for t in TASKS for b in ('A','B')),
             'predict_pass':sum(tests[f'predict:{t}:{b}']['statistic'] is not None and tests[f'predict:{t}:{b}']['statistic']>0 and h['rejected'][f'predict:{t}:{b}'] for t in TASKS for b in ('A','B'))}
        if artifact: verdict='EVALUATION_ARTIFACT_DOMINANT'
        elif repok and subok and predok: verdict='LOW_RANK_INTERACTION_BASIS_TRANSPORTS_WITH_FRESH_TASK_PREDICTION'
        elif repok and subok: verdict='LOW_RANK_INTERACTION_SUBSPACE_TRANSPORT_WITHOUT_VERTEX_PREDICTION'
        elif repok and predok: verdict='ANCHOR_PREDICTION_WITHOUT_GLOBAL_SUBSPACE'
        elif all(x>=1 for x in fam.values()): verdict='PARTIAL_INTERACTION_STRUCTURE_TRANSPORT'
        elif reversals: verdict='OPERATOR_REVERSAL_WITH_NONTRANSPORTABLE_INTERACTION'
        else: verdict='TASK_LOCAL_INTERACTION_UNSTRUCTURED_AT_TESTED_RESOLUTION'
        out={'stage':STAGE,'design':{'model':MODEL,'tasks':list(TASKS),'draws_per_task':64,'blocks':['A','B'],'vertices':32,'semantic_twins':2,'total_calls':12288,'width':WIDTH,'anchors':ANCHOR.tolist(),'holdout':HOLD.tolist()},
             'technical':tg,'historical_training_worlds':[{'assignment':w['assignment'],'rank':bases[i]['rank'],'singular_values':[float(x) for x in bases[i]['singular_values']]} for i,w in enumerate(worlds)],
             'fresh_tau':{t:{b:tau[t][b].tolist() for b in ('A','B')} for t in TASKS},'primary_tests':tests,'holm_familywise_005':h,'family_pass_counts':fam,
             'operator_effects':op,'strict_operator_reversals':reversals,'expanded_tensor_spectra':expanded,'constitutional_verdict':verdict,
             'authority':'Canonical sharded P57 run; task shards are combined before the unchanged frozen analysis. Historical ambiguity retained exactly as two worlds.',
             'raw_rows':rows}
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
