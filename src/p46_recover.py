from __future__ import annotations
import json
from pathlib import Path
from p44_field import ALIASES,packet,call,correct,shadow_correct

STAGE='EPISTEME-P46-TECHNICAL-RECOVERY'
FAILED={
'gptoss120':[
(1,'R_F_H','null','B',4601),(2,'R_H_T','valid','A',4602),(3,'R_F_H','null','D',4603),
(3,'I','null','D',4603),(3,'L','null','C',4603),(4,'L','null','C',4604),
(5,'R_H','null','D',4605),(5,'R_F_H_L','null','B',4605),(7,'R_F','null','B',4607),(7,'R_F_T','null','D',4607)],
'gemini':[(7,'L','null','B',4607)]}
ALIAS={a['tag']:a for a in ALIASES}

def main():
 out={'stage':STAGE,'authority':'Technical completion only. Replays exactly the 11 P46 calls that failed technically; no successful P46 scientific call is rerun.','rows':{}}
 for model,cases in FAILED.items():
  rows=[]
  for wave,v,s,a,seed in cases:
   try:
    o=call(model,packet(v,s,ALIAS[a]),seed); pc=correct(o,s); sc=shadow_correct(o,s); status='OK'; err=None
   except Exception as e:
    pc=sc=None; status='TECHNICAL_FAIL'; err=type(e).__name__+':'+str(e)[:300]
   rows.append({'wave':wave,'vertex':v,'semantic':s,'alias':a,'seed':seed,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
  out['rows'][model]=rows
 p=Path('receipts/p46_recovery.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')
if __name__=='__main__':main()
