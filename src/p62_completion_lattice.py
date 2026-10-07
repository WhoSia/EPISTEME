from __future__ import annotations
import argparse,base64,hashlib,itertools,json,zlib
from collections import Counter
from pathlib import Path
import numpy as np
import p60_analyze_shards as p60
from p60_context_interaction import TASKS,TASK_SPECS,PRIMARY_OPS,OPS

STAGE='EPISTEME-P62'
EXPECTED_INPUT_SHA='427c6686b7eb11fe1f11ecbc2a1baf11844206b054e28a34d017075c0ef531a4'
EXPECTED_ANALYZER_BLOB='c13e654e6e549e35e729f5d0f16f1815815501f6'
EXPECTED_CONTEXT_BLOB='ed5b2ef50840d41aaf641a4e5e5cb96789d1bc37'
TOTAL_ROWS=49152

def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def git_blob(path):
    b=Path(path).read_bytes();return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()

def decode_input(path):
    if sha256(path)!=EXPECTED_INPUT_SHA: raise RuntimeError('P62_INPUT_FINGERPRINT_MISMATCH')
    d=json.loads(Path(path).read_text())
    if d.get('stage')!='EPISTEME-P62-INPUT' or len(d.get('missing',[]))!=4: raise RuntimeError('P62_INPUT_AUTHORITY')
    tasks={}
    for t in TASKS:
        q=json.loads(zlib.decompress(base64.b64decode(d['tasks'][t])))
        if not all(len(q[k])==4096 for k in ('known','pc','sc')): raise RuntimeError('P62_TASK_VECTOR')
        tasks[t]=q
    return d,tasks

def pos(draw,vi,semantic): return ((int(draw)-1)*32+int(vi))*2+(0 if semantic=='valid' else 1)

def build_J(tasks,missing,primary_bits):
    miss={(m['task'],int(m['draw']),int(m['vertex_index']),m['semantic']):i for i,m in enumerate(missing)}
    out={}
    for t in TASKS:
        q=tasks[t];J=np.zeros((64,32),float)
        for d in range(1,65):
            for vi in range(32):
                vals=[]
                for s in ('valid','null'):
                    j=pos(d,vi,s);key=(t,d,vi,s)
                    if q['known'][j]=='1': vals.append(q['pc'][j]=='1')
                    elif key in miss: vals.append(bool(primary_bits[miss[key]]))
                    else: raise RuntimeError('UNDECLARED_UNKNOWN')
                J[d-1,vi]=float(vals[0] and vals[1])
        out[t]=J
    return out

def adjudicate(Js,disagreements):
    analyses={t:p60.task_analysis(Js[t]) for t in TASKS}
    tau_carrier,tau_role=p60.context_tests(analyses,'tau')
    err_carrier,err_role=p60.context_tests(analyses,'error')
    tau_tests={f'tau_carrier_{op}':tau_carrier[op] for op in PRIMARY_OPS}
    err_tests={f'error_carrier_{op}':err_carrier[op] for op in PRIMARY_OPS}
    tau_holm=p60.holm(tau_tests);err_holm=p60.holm(err_tests)
    tau_direction=(tau_carrier['R']['statistic']<0 and tau_carrier['T']['statistic']>0)
    err_direction=(err_carrier['R']['statistic']<0 and err_carrier['T']['statistic']>0)
    tau_primary=tau_direction and all(tau_holm['rejected'].values())
    err_primary=err_direction and all(err_holm['rejected'].values())
    tau_strict=p60.strict_gate(analyses,'tau');err_strict=p60.strict_gate(analyses,'error')
    tau_critical=p60.critical_gate(analyses,'tau');err_critical=p60.critical_gate(analyses,'error')
    role_tests={f'tau_role_{op}':tau_role[op] for op in PRIMARY_OPS}
    role_holm=p60.holm(role_tests)
    artifact=(disagreements/TOTAL_ROWS)>=.10
    if artifact: verdict='EVALUATION_ARTIFACT_DOMINANT'
    elif tau_primary and tau_strict['pass'] and tau_critical['pass'] and err_primary and err_strict['pass'] and err_critical['pass']:
        verdict='PROSPECTIVE_CARRIER_INDEXED_R_T_QUALITATIVE_INTERACTION_WITH_BEHAVIORAL_CONCORDANCE'
    elif tau_primary and tau_strict['pass'] and tau_critical['pass']:
        verdict='PROSPECTIVE_CARRIER_INDEXED_R_T_STOPPING_INTERACTION_ONLY'
    elif tau_primary: verdict='CARRIER_MODERATION_WITHOUT_STRICT_SIGN_TRANSPORT'
    elif any(role_holm['rejected'].values()): verdict='ROLE_OR_HIGHER_ORDER_CONTEXT_MODERATION'
    else: verdict='P57_OPERATOR_REVERSAL_TASK_LOCAL_AT_TESTED_CONTEXT_RESOLUTION'
    return {
      'constitutional_verdict':verdict,
      'primary_shadow_disagreements':disagreements,
      'primary_shadow_disagreement_rate':disagreements/TOTAL_ROWS,
      'primary_tau_tests':tau_tests,'primary_tau_holm':tau_holm,
      'behavioral_error_tests':err_tests,'behavioral_error_holm':err_holm,
      'tau_strict_sign_gate_pass':tau_strict['pass'],'behavioral_strict_sign_gate_pass':err_strict['pass'],
      'tau_critical_quadrant_gate_pass':tau_critical['pass'],'behavioral_critical_quadrant_gate_pass':err_critical['pass'],
      'role_rival_tests':role_tests,'role_rival_holm':role_holm
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',default='active/p62_completion_input.json');ap.add_argument('--out',default='receipts/p62_result.json');a=ap.parse_args()
    if git_blob('src/p60_analyze_shards.py')!=EXPECTED_ANALYZER_BLOB: raise RuntimeError('FROZEN_P60_ANALYZER_DRIFT')
    if git_blob('src/p60_context_interaction.py')!=EXPECTED_CONTEXT_BLOB: raise RuntimeError('FROZEN_P60_CONTEXT_DRIFT')
    raw,tasks=decode_input(a.input);missing=raw['missing']
    known_dis=0
    for t in TASKS:
        q=tasks[t]
        known_dis+=sum(k=='1' and p!=s for k,p,s in zip(q['known'],q['pc'],q['sc']))
    if known_dis!=0: raise RuntimeError('KNOWN_DISAGREEMENT_DRIFT')
    primary_results={}
    for pb in itertools.product((0,1),repeat=4):
        key=''.join(map(str,pb));Js=build_J(tasks,missing,pb)
        primary_results[key]=adjudicate(Js,0)
    worlds=[]
    for pb in itertools.product((0,1),repeat=4):
        pk=''.join(map(str,pb));base=primary_results[pk]
        for sb in itertools.product((0,1),repeat=4):
            dis=known_dis+sum(int(x!=y) for x,y in zip(pb,sb))
            artifact=(dis/TOTAL_ROWS)>=.10
            verdict='EVALUATION_ARTIFACT_DOMINANT' if artifact else base['constitutional_verdict']
            worlds.append({'primary':pk,'shadow':''.join(map(str,sb)),'disagreements':dis,'artifact':artifact,'verdict':verdict})
    if len(worlds)!=256: raise RuntimeError('WORLD_CARDINALITY')
    vc=Counter(w['verdict'] for w in worlds); artifacts=sum(w['artifact'] for w in worlds)
    def rng(field,op,sub='statistic'):
        vals=[r[field][op][sub] for r in primary_results.values()]
        return [float(min(vals)),float(max(vals))]
    summary={
      'tau_carrier_R_statistic_range':rng('primary_tau_tests','tau_carrier_R'),
      'tau_carrier_T_statistic_range':rng('primary_tau_tests','tau_carrier_T'),
      'tau_carrier_R_p_range':rng('primary_tau_tests','tau_carrier_R','p'),
      'tau_carrier_T_p_range':rng('primary_tau_tests','tau_carrier_T','p'),
      'error_carrier_R_statistic_range':rng('behavioral_error_tests','error_carrier_R'),
      'error_carrier_T_statistic_range':rng('behavioral_error_tests','error_carrier_T'),
      'error_carrier_R_p_range':rng('behavioral_error_tests','error_carrier_R','p'),
      'error_carrier_T_p_range':rng('behavioral_error_tests','error_carrier_T','p'),
      'max_shadow_disagreements':max(w['disagreements'] for w in worlds),
      'max_shadow_disagreement_rate':max(w['disagreements'] for w in worlds)/TOTAL_ROWS,
      'tau_strict_gate_pass_worlds':sum(r['tau_strict_sign_gate_pass'] for r in primary_results.values())*16,
      'behavioral_strict_gate_pass_worlds':sum(r['behavioral_strict_sign_gate_pass'] for r in primary_results.values())*16,
      'tau_critical_gate_pass_worlds':sum(r['tau_critical_quadrant_gate_pass'] for r in primary_results.values())*16,
      'behavioral_critical_gate_pass_worlds':sum(r['behavioral_critical_quadrant_gate_pass'] for r in primary_results.values())*16,
      'tau_holm_rejection_patterns':sorted(set(''.join('1' if x else '0' for x in r['primary_tau_holm']['rejected'].values()) for r in primary_results.values())),
      'behavioral_holm_rejection_patterns':sorted(set(''.join('1' if x else '0' for x in r['behavioral_error_holm']['rejected'].values()) for r in primary_results.values())),
      'role_holm_rejection_patterns':sorted(set(''.join('1' if x else '0' for x in r['role_rival_holm']['rejected'].values()) for r in primary_results.values()))
    }
    invariant=(len(vc)==1 and artifacts==0)
    final_verdict=next(iter(vc)) if invariant else 'COMPLETION_SENSITIVE_P60_BRANCH'
    out={
      'stage':STAGE,
      'descriptor':'Four-Cell Completion-Lattice Closure, Frozen R/T Carrier-Interaction Invariance, Dual-Endpoint Missingness-Free Adjudication, Critical-Quadrant Robustness & P60 Task-Locality Identification',
      'provider_calls':0,
      'input_sha256':EXPECTED_INPUT_SHA,
      'frozen_source':{'p60_analyzer_git_blob_sha1':EXPECTED_ANALYZER_BLOB,'p60_context_git_blob_sha1':EXPECTED_CONTEXT_BLOB},
      'completion_lattice':{'missing_cells':missing,'primary_equivalence_classes':16,'shadow_completions_per_primary':16,'total_worlds':256,'missingness_probability_model_used':False},
      'known_primary_shadow_disagreements':known_dis,
      'primary_results':primary_results,
      'world_verdict_counts':dict(vc),'artifact_worlds':artifacts,'summary':summary,
      'completion_invariant':invariant,
      'p60_missingness_free_constitutional_verdict':final_verdict,
      'constitutional_verdict':('MISSINGNESS_FREE_P60_TASK_LOCALITY_IDENTIFIED' if invariant and final_verdict=='P57_OPERATOR_REVERSAL_TASK_LOCAL_AT_TESTED_CONTEXT_RESOLUTION' else 'MISSINGNESS_FREE_P60_BRANCH_IDENTIFIED' if invariant else 'P60_BRANCH_REMAINS_COMPLETION_SENSITIVE'),
      'authority':'Zero-provider-call logical completion court. No probability distribution over missing cells is assumed or estimated. P62 licenses only claims invariant across all 256 logical primary/shadow completions under the unchanged frozen P60 adjudication functions.'
    }
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))

if __name__=='__main__': main()
