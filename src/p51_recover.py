from __future__ import annotations
import json
from pathlib import Path
from p48_seed_fingerprints import panel_cells, make_packet, FRESH_ALIAS
from p44_field import call, correct, shadow_correct

STAGE='EPISTEME-P51-TECHNICAL-RECOVERY'
TARGETS=[
 {'model':'gptoss120','draw':3,'vertex':'H_L','alias':'C','semantic':'null','cell_index':29},
 {'model':'gptoss120','draw':5,'vertex':'R_F','alias':'C','semantic':'null','cell_index':13},
 {'model':'gemini','draw':6,'vertex':'H_L','alias':'C','semantic':'null','cell_index':29},
 {'model':'gptoss120','draw':7,'vertex':'T_L','alias':'D','semantic':'valid','cell_index':30},
 {'model':'gptoss120','draw':8,'vertex':'F_H','alias':'C','semantic':'null','cell_index':21},
 {'model':'gptoss120','draw':17,'vertex':'T_L','alias':'D','semantic':'null','cell_index':31},
 {'model':'gptoss120','draw':17,'vertex':'H_L','alias':'C','semantic':'null','cell_index':29},
 {'model':'gptoss120','draw':26,'vertex':'R_F_H_L','alias':'D','semantic':'null','cell_index':55},
 {'model':'gptoss120','draw':26,'vertex':'H_L','alias':'C','semantic':'null','cell_index':29},
 {'model':'gptoss120','draw':36,'vertex':'H_L','alias':'C','semantic':'null','cell_index':29},
 {'model':'gptoss120','draw':38,'vertex':'F_H_T','alias':'C','semantic':'null','cell_index':45},
 {'model':'gptoss120','draw':42,'vertex':'I','alias':'A','semantic':'null','cell_index':1},
 {'model':'gptoss120','draw':44,'vertex':'R_F','alias':'C','semantic':'null','cell_index':13},
 {'model':'gptoss120','draw':53,'vertex':'R_T_L','alias':'B','semantic':'null','cell_index':43},
 {'model':'gptoss120','draw':57,'vertex':'F_H','alias':'C','semantic':'null','cell_index':21},
 {'model':'gptoss120','draw':57,'vertex':'R_H','alias':'D','semantic':'null','cell_index':15},
 {'model':'gptoss120','draw':59,'vertex':'H_T','alias':'B','semantic':'null','cell_index':27},
 {'model':'gptoss120','draw':60,'vertex':'R_F_H','alias':'A','semantic':'null','cell_index':33},
 {'model':'gptoss120','draw':64,'vertex':'R_F_T','alias':'B','semantic':'null','cell_index':35},
]
CELL={(c['vertex'],c['alias'],c['semantic']):c for c in panel_cells()}

def main():
    rows=[]
    for t in TARGETS:
        c=CELL[(t['vertex'],t['alias'],t['semantic'])]
        assert c['cell_index']==t['cell_index']
        pkt=make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True)
        seed=5100+t['draw']
        try:
            o=call(t['model'],pkt,seed)
            pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**t,'vertex_index':c['vertex_index'],'semantic_index':c['semantic_index'],
                     'gemini_seed':seed if t['model']=='gemini' else None,
                     'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    out={'stage':STAGE,'authority':'Technical completion only. Replays exactly the 19 P51 calls that failed technically; no successful P51 call is rerun.',
         'targets':len(TARGETS),'rows':rows}
    p=Path('receipts/p51_recovery.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')
if __name__=='__main__':main()
