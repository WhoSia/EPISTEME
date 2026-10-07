from pathlib import Path
import base64,zlib,json,time
from collections import Counter
from p44_field import call,correct,shadow_correct
from p60_context_interaction import MODEL,packet
D=json.loads(zlib.decompress(base64.b64decode("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")))
rows=D['failed_cells']; attempts=[]
assert D['stage']=='EPISTEME-P61' and D['count']==254 and len(rows)==254
for r in rows:
 t0=time.perf_counter_ns()
 try:
  o=call(MODEL,packet(r['task'],r['vertex'],r['semantic'],r['alias']),6000+int(r['draw']))
  pc=correct(o,r['semantic']);sc=shadow_correct(o,r['semantic']);status='OK';err=None
 except Exception as e:
  pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
 attempts.append({**r,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err,'latency_ms':(time.perf_counter_ns()-t0)/1e6})
rem=[r for r in attempts if r['status']!='OK']
out={'stage':'EPISTEME-P61','execution_carrier':'legacy P52 technical-recovery workflow only; no P52 scientific authority','source_run':D['source_run'],'source_result_sha256':D['source_result_sha256'],'authorized_failed_cells':254,'attempted_cells':len(attempts),'recovered_cells':254-len(rem),'remaining_failed_cells':len(rem),'complete':not rem,'remaining_by_task':dict(Counter(r['task'] for r in rem)),'successful_source_rows_replayed':0,'attempts':attempts}
Path('receipts').mkdir(exist_ok=True)
Path('receipts/p52_recovery2.json').write_text(json.dumps(out,indent=2))
