"""P67 pilot is feasibility only, not an inferential causal adjudicator."""
from __future__ import annotations
import argparse,json
from collections import defaultdict
from pathlib import Path
from p67_channels import CHANNELS,TASKS,N_CALLS

def evaluate(root):
    docs=[]
    for p in Path(root).rglob('*.json'):
        try:d=json.loads(p.read_text())
        except (ValueError,OSError):continue
        if isinstance(d,dict) and d.get('stage')=='EPISTEME-P67' and d.get('pilot') and d.get('task') in TASKS:docs.append(d)
    if len(docs)!=4 or {d['task'] for d in docs}!=set(TASKS):raise ValueError('missing or duplicate pilot task')
    rows=[r for d in docs for r in d['rows']]
    if len(rows)!=N_CALLS or len({(r['task'],r['draw'],r['channel'],r['cell_index']) for r in rows})!=N_CALLS:raise ValueError('incomplete trial lattice')
    matched=defaultdict(set)
    for r in rows:matched[(r['task'],r['draw'],r['cell_index'])].add((r['channel'],r['packet_sha256']))
    if any({x[0] for x in vals}!=set(CHANNELS) or len({x[1] for x in vals})!=1 for vals in matched.values()):raise ValueError('paired packet checksum mismatch')
    arms={}
    for ch in CHANNELS:
        local=[r for r in rows if r['channel']==ch]
        if len(local)!=128:raise ValueError('unequal channels')
        arms[ch]={'calls':128,'provider_response':sum(r['provider_status']=='RESPONSE' for r in local),
                  'format_valid':sum(r['format_valid'] for r in local),
                  'executable_correct':sum(r['semantic_correct'] is True and r['format_valid'] for r in local),
                  'semantic_wrong_observed':sum(r['semantic_correct'] is False for r in local),
                  'unobserved_or_invalid':sum(r['semantic_correct'] is None for r in local)}
    return {'stage':'EPISTEME-P67','kind':'FEASIBILITY_PILOT','calls':len(rows),'paired_packet_strata':len(matched),'arms':arms,
            'pilot_verdict':'MEASUREMENT_FEASIBLE' if all(v['provider_response']>=96 for v in arms.values()) else 'TECHNICAL_MEASUREMENT_HOLD',
            'authority':'Descriptive feasibility audit, not confirmatory inference. All packet hashes paired and complete; no MAR assumption. P66 frozen technical HOLD remains.'}
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',required=True);parser.add_argument('--out',required=True);args=parser.parse_args()
    report=evaluate(args.root);out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2));print(report['pilot_verdict'],report['calls'])
