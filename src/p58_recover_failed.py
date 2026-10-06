from __future__ import annotations
import argparse,hashlib,json,time
from collections import Counter
from pathlib import Path
from p44_field import call,correct,shadow_correct
from p57_interaction_tensor import MODEL,TASKS,packet

STAGE='EPISTEME-P58'
EXPECTED_SOURCE_SHA256='4b3b8d1222e47639846f7c7c701c4f7709fc746e9daaed01416c3caf1b95d60d'
EXPECTED_TOTAL=12288
EXPECTED_OK=12250
EXPECTED_FAILED=38

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def identity(r):
    return (r['task'],int(r['draw']),int(r['cell_index']))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--rows-out',required=True)
    ap.add_argument('--receipt',required=True)
    a=ap.parse_args()
    if sha256(a.source)!=EXPECTED_SOURCE_SHA256:
        raise RuntimeError('P57_SOURCE_FINGERPRINT_MISMATCH')
    src=json.loads(Path(a.source).read_text(encoding='utf-8'))
    rows=src['raw_rows']
    if src.get('stage')!='EPISTEME-P57' or src.get('constitutional_verdict')!='TECHNICAL_HOLD':
        raise RuntimeError('P57_SOURCE_AUTHORITY_MISMATCH')
    if len(rows)!=EXPECTED_TOTAL:
        raise RuntimeError(f'P57_TOTAL_MISMATCH:{len(rows)}')
    ok=[r for r in rows if r.get('status')=='OK']
    fail=[r for r in rows if r.get('status')!='OK']
    if len(ok)!=EXPECTED_OK or len(fail)!=EXPECTED_FAILED:
        raise RuntimeError(f'P57_TECH_COUNTS_MISMATCH:{len(ok)}:{len(fail)}')
    ids=[identity(r) for r in fail]
    if len(ids)!=len(set(ids)):
        raise RuntimeError('DUPLICATE_FAILED_CELL_IDENTITY')
    recovered=[]; attempts=[]
    fail_ids=set(ids)
    for r in rows:
        if identity(r) not in fail_ids:
            recovered.append(dict(r)); continue
        t0=time.perf_counter_ns(); new=dict(r)
        try:
            o=call(MODEL,packet(r['task'],r['vertex'],r['semantic'],r['alias']),5700+int(r['draw']))
            pc=correct(o,r['semantic']); sc=shadow_correct(o,r['semantic'])
            status='OK'; err=None
        except Exception as e:
            pc=sc=None; status='TECHNICAL_FAIL'; err=type(e).__name__+':'+str(e)[:300]
        latency=(time.perf_counter_ns()-t0)/1e6
        new.update({'latency_ms':latency,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err,
                    'p58_recovery':True,'p58_source_error':r.get('error')})
        recovered.append(new)
        attempts.append({'identity':{'task':r['task'],'draw':r['draw'],'cell_index':r['cell_index']},
                         'vertex':r['vertex'],'semantic':r['semantic'],'alias':r['alias'],
                         'original_error':r.get('error'),'replay_status':status,'replay_error':err,'latency_ms':latency})
    if len(attempts)!=EXPECTED_FAILED or len(recovered)!=EXPECTED_TOTAL:
        raise RuntimeError('P58_REPLAY_CARDINALITY_BREACH')
    by_task={t:[] for t in TASKS}
    for r in recovered: by_task[r['task']].append(r)
    outroot=Path(a.rows_out);outroot.mkdir(parents=True,exist_ok=True)
    for t in TASKS:
        if len(by_task[t])!=4096: raise RuntimeError(f'{t}_ROW_COUNT:{len(by_task[t])}')
        (outroot/f'{t}.json').write_text(json.dumps({'task':t,'rows':by_task[t]},indent=2),encoding='utf-8')
    remain=[r for r in recovered if r.get('status')!='OK']
    rec={
      'stage':STAGE,
      'source':{'stage':'EPISTEME-P57','run':37390830384,'head':'f6c9156b1b0820bbb72eaa6afb148487e70d2e5d','sha256':EXPECTED_SOURCE_SHA256},
      'authorized_failed_cells':EXPECTED_FAILED,
      'attempted_cells':len(attempts),
      'recovered_cells':EXPECTED_FAILED-len(remain),
      'remaining_failed_cells':len(remain),
      'complete':len(remain)==0,
      'remaining_by_task':dict(Counter(r['task'] for r in remain)),
      'remaining_by_semantic':dict(Counter(r['semantic'] for r in remain)),
      'provider_failure_separation':'technical errors are not scientific incorrectness',
      'successful_source_rows_replayed':0,
      'attempts':attempts
    }
    p=Path(a.receipt);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(rec,indent=2),encoding='utf-8')
if __name__=='__main__':main()
