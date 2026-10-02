from __future__ import annotations
import json
from pathlib import Path
from p48_seed_fingerprints import panel_cells, make_packet, FRESH_ALIAS
from p44_field import call, correct, shadow_correct

STAGE='EPISTEME-P52-TECHNICAL-RECOVERY'
TARGETS=[{"model":"gptoss120","draw":8,"vertex":"R_F_T_L","alias":"A","semantic":"null","cell_index":57},{"model":"gptoss120","draw":12,"vertex":"R_F","alias":"C","semantic":"null","cell_index":13},{"model":"gptoss120","draw":12,"vertex":"R_F_H_L","alias":"D","semantic":"null","cell_index":55},{"model":"gptoss120","draw":13,"vertex":"F_H_T_L","alias":"C","semantic":"null","cell_index":61},{"model":"gptoss120","draw":15,"vertex":"R_F","alias":"C","semantic":"null","cell_index":13},{"model":"gptoss120","draw":17,"vertex":"R_T_L","alias":"B","semantic":"null","cell_index":43},{"model":"gptoss120","draw":21,"vertex":"I","alias":"A","semantic":"null","cell_index":1},{"model":"gptoss120","draw":23,"vertex":"R_F_H","alias":"A","semantic":"null","cell_index":33},{"model":"gptoss120","draw":23,"vertex":"R_F_H_T","alias":"C","semantic":"null","cell_index":53},{"model":"gptoss120","draw":25,"vertex":"F_H_T","alias":"C","semantic":"null","cell_index":45},{"model":"gptoss120","draw":26,"vertex":"H_T","alias":"B","semantic":"null","cell_index":27},{"model":"gptoss120","draw":38,"vertex":"R_T","alias":"A","semantic":"null","cell_index":17},{"model":"gptoss120","draw":41,"vertex":"R_F","alias":"C","semantic":"null","cell_index":13},{"model":"gptoss120","draw":47,"vertex":"F_H_T_L","alias":"C","semantic":"null","cell_index":61},{"model":"gptoss120","draw":52,"vertex":"F_H_T","alias":"C","semantic":"null","cell_index":45},{"model":"gptoss120","draw":59,"vertex":"R_F_T","alias":"B","semantic":"null","cell_index":35},{"model":"gptoss120","draw":59,"vertex":"F_L","alias":"A","semantic":"null","cell_index":25},{"model":"gptoss120","draw":60,"vertex":"H_L","alias":"C","semantic":"null","cell_index":29},{"model":"gptoss120","draw":63,"vertex":"R_F_T_L","alias":"A","semantic":"null","cell_index":57}]

CELL={(c['vertex'],c['alias'],c['semantic']):c for c in panel_cells()}

def main():
    rows=[]
    for t in TARGETS:
        c=CELL[(t['vertex'],t['alias'],t['semantic'])]
        assert c['cell_index']==t['cell_index']
        pkt=make_packet(c['vertex'],c['semantic'],FRESH_ALIAS[c['alias']],True)
        seed=5200+t['draw']
        try:
            o=call(t['model'],pkt,seed)
            pc=correct(o,c['semantic']);sc=shadow_correct(o,c['semantic']);status='OK';err=None
        except Exception as e:
            pc=sc=None;status='TECHNICAL_FAIL';err=type(e).__name__+':'+str(e)[:300]
        rows.append({**t,'vertex_index':c['vertex_index'],'semantic_index':c['semantic_index'],
                     'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err})
    out={'stage':STAGE,'authority':'Technical completion only. Replays exactly the 19 P52 calls that failed technically; no successful P52 call is rerun.',
         'targets':len(TARGETS),'rows':rows}
    p=Path('receipts/p52_recovery.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')
if __name__=='__main__':main()
