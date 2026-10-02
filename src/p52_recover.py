from pathlib import Path
import json
from p48_seed_fingerprints import panel_cells,make_packet,FRESH_ALIAS
from p44_field import call,correct,shadow_correct
T={'model':'gptoss120','draw':26,'vertex':'H_T','alias':'B','semantic':'null','cell_index':27}
C={(c['vertex'],c['alias'],c['semantic']):c for c in panel_cells()}
c=C[(T['vertex'],T['alias'],T['semantic'])];assert c['cell_index']==T['cell_index']
try:
 o=call(T['model'],make_packet(T['vertex'],T['semantic'],FRESH_ALIAS[T['alias']],True),5226)
 pc=correct(o,T['semantic']);sc=shadow_correct(o,T['semantic']);status='OK';err=None
except Exception as e:
 pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
Path('receipts').mkdir(exist_ok=True)
Path('receipts/p52_recovery.json').write_text(json.dumps({'stage':'EPISTEME-P52-TECHNICAL-RECOVERY-FINAL','target':T,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err},indent=2))
