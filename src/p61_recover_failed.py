import argparse,json,hashlib,time
from pathlib import Path
from collections import Counter
from p44_field import call,correct,shadow_correct
from p60_context_interaction import MODEL,TASKS,packet

SHA='0b36881b4d503c95e1826c5018897ba75ad63fd21de636a97cf2ff46dd28c58d'
N=49152; OK=48898; FAIL=254

def ident(r): return (r['task'],int(r['draw']),int(r['cell_index']))

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--p60-result',required=True);a.add_argument('--shards-root',required=True)
    a.add_argument('--rows-out',required=True);a.add_argument('--receipt',required=True);x=a.parse_args()
    p=Path(x.p60_result)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=SHA: raise RuntimeError('P60_RESULT_HASH')
    res=json.loads(p.read_text()); tech=res['technical']
    if res.get('constitutional_verdict')!='TECHNICAL_HOLD' or (tech['ok'],tech['total'],tech['failed_count'])!=(OK,N,FAIL):
        raise RuntimeError('P60_AUTHORITY')
    rows=[]
    for t in TASKS:
        hits=list(Path(x.shards_root).rglob(t+'.json'))
        if len(hits)!=1: raise RuntimeError('SOURCE_'+t)
        d=json.loads(hits[0].read_text())
        if d.get('task')!=t or len(d.get('rows',[]))!=4096: raise RuntimeError('ROWS_'+t)
        rows+=d['rows']
    srcfail=[r for r in rows if r.get('status')!='OK']
    if len(rows)!=N or len(srcfail)!=FAIL or sum(r.get('status')=='OK' for r in rows)!=OK: raise RuntimeError('SOURCE_COUNTS')
    ledger={ (r['task'],int(r['draw']),int(r['cell_index'])) for r in tech['failed_rows'] }
    if len(ledger)!=FAIL or ledger!={ident(r) for r in srcfail}: raise RuntimeError('FAILED_SET')
    attempts=[]; out=[]
    for r in rows:
        if ident(r) not in ledger: out.append(dict(r)); continue
        q=dict(r); t0=time.perf_counter_ns()
        try:
            z=call(MODEL,packet(r['task'],r['vertex'],r['semantic'],r['alias']),6000+int(r['draw']))
            pc=correct(z,r['semantic']); sc=shadow_correct(z,r['semantic']); status='OK'; err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        ms=(time.perf_counter_ns()-t0)/1e6
        q.update(status=status,primary_correct=pc,shadow_correct=sc,error=err,latency_ms=ms,p61_recovery=True,p61_source_error=r.get('error'))
        out.append(q); attempts.append({'task':r['task'],'draw':r['draw'],'cell_index':r['cell_index'],'vertex':r['vertex'],'semantic':r['semantic'],'alias':r['alias'],'status':status,'error':err,'latency_ms':ms})
    if len(attempts)!=FAIL: raise RuntimeError('REPLAY_COUNT')
    root=Path(x.rows_out);root.mkdir(parents=True,exist_ok=True)
    for t in TASKS:
        rr=[r for r in out if r['task']==t]
        if len(rr)!=4096: raise RuntimeError('OUT_'+t)
        (root/(t+'.json')).write_text(json.dumps({'task':t,'rows':rr},indent=2))
    rem=[r for r in out if r.get('status')!='OK']
    receipt={'stage':'EPISTEME-P61','authorized_failed_cells':FAIL,'attempted_cells':FAIL,'recovered_cells':FAIL-len(rem),'remaining_failed_cells':len(rem),'complete':not rem,'remaining_by_task':dict(Counter(r['task'] for r in rem)),'remaining_by_semantic':dict(Counter(r['semantic'] for r in rem)),'successful_source_rows_replayed':0,'attempts':attempts}
    Path(x.receipt).write_text(json.dumps(receipt,indent=2))
if __name__=='__main__': main()
