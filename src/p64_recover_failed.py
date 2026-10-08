import argparse,json,time
from pathlib import Path
from collections import Counter
from p44_field import call,correct,shadow_correct
from p63_structural_location import MODEL,TASKS,packet

ALIASES={'RD1':'RH1','RD2':'RH2','RD3':'RH3','RP1':'RT1','RP2':'RT2','RP3':'RT3','SD1':'SH1','SD2':'SH2','SD3':'SH3','SP1':'ST1','SP2':'ST2','SP3':'ST3'}
def ident(r): return (r['task'],int(r['draw']),int(r['cell_index']))
def main():
 p=argparse.ArgumentParser()
 for name in ('p63-result','source-shards','out-root','receipt'): p.add_argument('--'+name,required=True)
 p.add_argument('--preflight-only',action='store_true')
 x=p.parse_args()
 z=json.loads(Path(x.p63_result).read_text());g=z['technical']
 assert z['stage']=='EPISTEME-P63' and z['constitutional_verdict']=='TECHNICAL_HOLD'
 assert (g['ok'],g['total'],g['failed_count'])==(48849,49152,303)
 allrows=[]
 for carrier,actual in ALIASES.items():
  matches=list(Path(x.source_shards).rglob(carrier+'.json'));assert len(matches)==1,carrier
  d=json.loads(matches[0].read_text());assert d['task']==actual and len(d['rows'])==4096
  allrows.extend(d['rows'])
 wanted={ident(r) for r in g['failed_rows']}
 assert len(wanted)==303 and len(allrows)==49152
 assert len({ident(r) for r in allrows})==49152
 assert wanted=={ident(r) for r in allrows if r['status']!='OK'}
 if x.preflight_only:
  print('P64_PREFLIGHT_PASS: 49152 canonical rows; 303 failed identities; 0 provider calls')
  return
 output=[];attempts=[]
 for orig in allrows:
  r=dict(orig)
  if ident(orig) in wanted:
   start=time.perf_counter_ns()
   try:
    response=call(MODEL,packet(r['task'],r['vertex'],r['semantic'],r['alias']),6300+int(r['draw']))
    primary=correct(response,r['semantic'])
    shadow=shadow_correct(response,r['semantic'])
    status='OK';error=None
   except Exception as ex:
    primary=shadow=None;status='TECHNICAL_FAIL';error=type(ex).__name__+':'+str(ex)[:300]
   r.update(status=status,primary_correct=primary,shadow_correct=shadow,error=error,latency_ms=(time.perf_counter_ns()-start)/1e6,p64_recovery=True)
   attempts.append({'task':r['task'],'draw':r['draw'],'cell_index':r['cell_index'],'status':status,'error':error})
  output.append(r)
 assert len(attempts)==303 and sum('p64_recovery' in r for r in output)==303
 out=Path(x.out_root);out.mkdir(parents=True,exist_ok=True)
 for task in TASKS:
  rs=[r for r in output if r['task']==task];assert len(rs)==4096
  (out/(task+'.json')).write_text(json.dumps({'task':task,'rows':rs}))
 residual=[r for r in output if r['status']!='OK']
 receipt={'stage':'EPISTEME-P64','attempted_cells':303,'recovered_cells':303-len(residual),'remaining_failed_cells':len(residual),'successful_source_rows_replayed':0,'complete':not residual,'remaining_by_task':dict(Counter(r['task'] for r in residual)),'attempts':attempts}
 dst=Path(x.receipt);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
