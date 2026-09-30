from __future__ import annotations
import json
from pathlib import Path
from p48_seed_fingerprints import old_packet, gemini_call
from p44_field import correct, shadow_correct

STAGE='EPISTEME-P49-TECHNICAL-RECOVERY'
TARGET={'seed':4932,'namespace':'old','vertex':'R_F_L','alias':'C','semantic':'valid','cell_index':36}

def main():
    pkt=old_packet(TARGET['vertex'],TARGET['semantic'],TARGET['alias'])
    try:
        o=gemini_call(pkt,TARGET['seed'])
        pc=correct(o,TARGET['semantic']); sc=shadow_correct(o,TARGET['semantic'])
        status='OK'; err=None
    except Exception as e:
        pc=sc=None; status='TECHNICAL_FAIL'; err=type(e).__name__+':'+str(e)[:300]
    out={'stage':STAGE,'authority':'Technical completion only; exactly one failed P49 call is replayed and no successful P49 call is rerun.',
         'target':TARGET,'status':status,'primary_correct':pc,'shadow_correct':sc,'error':err}
    p=Path('receipts/p49_recovery.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2),encoding='utf-8')

if __name__=='__main__':main()
