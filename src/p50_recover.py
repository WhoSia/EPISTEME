from __future__ import annotations
import json
from pathlib import Path
from p48_seed_fingerprints import panel_cells, make_packet, FRESH_ALIAS
from p44_field import call, correct, shadow_correct

STAGE='EPISTEME-P50-TECHNICAL-RECOVERY'
TARGETS=[
 {'model':'gptoss120','draw':9,'vertex':'H_T','alias':'B','semantic':'valid'},
 {'model':'gptoss120','draw':9,'vertex':'H_T','alias':'B','semantic':'null'},
 {'model':'gptoss120','draw':10,'vertex':'H','alias':'D','semantic':'null'},
 {'model':'gptoss120','draw':11,'vertex':'F','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':11,'vertex':'F_H','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':13,'vertex':'F_H','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':13,'vertex':'R_F','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':14,'vertex':'F_H_T','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':14,'vertex':'F','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':26,'vertex':'R_H_T','alias':'D','semantic':'null'},
 {'model':'gptoss120','draw':28,'vertex':'F_H_T_L','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':29,'vertex':'F_H_T','alias':'C','semantic':'null'},
 {'model':'gptoss120','draw':31,'vertex':'R_F','alias':'C','semantic':'null'},
 {'model':'gemini','draw':31,'vertex':'H_T_L','alias':'B','semantic':'null'},
]
GEMINI_SEEDS={i:5000+i for i in range(1,33)}
CELL={(c['vertex'],c['alias'],c['semantic']):c for c in panel_cells()}

def pkt(t):
    c=CELL[(t['vertex'],t['alias'],t['semantic'])]
    return c,make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True)

def main():
    rows=[]
    for t in TARGETS:
        c,p=pkt(t)
        seed=GEMINI_SEEDS[t['draw']] if t['model']=='gemini' else 5000+t['draw']
        try:
            o=call(t['model'],p,seed)
            pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**t,'cell_index':c['cell_index'],'vertex_index':c['vertex_index'],
                     'semantic_index':c['semantic_index'],'gemini_seed':seed if t['model']=='gemini' else None,
                     'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    out={'stage':STAGE,'authority':'Technical completion only. Replays exactly the 14 P50 calls that failed technically; no successful P50 call is rerun.',
         'targets':len(TARGETS),'rows':rows}
    p=Path('receipts/p50_recovery.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':main()
