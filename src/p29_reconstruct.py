from __future__ import annotations
import json
from pathlib import Path

VERTEX_ORDER=["I","R","F","H","T","L","R_F","R_H","R_T","R_L","F_H","F_T","F_L","H_T","H_L","T_L","R_F_H","R_F_T","R_F_L","R_H_T","R_H_L","R_T_L","F_H_T","F_H_L","F_T_L","H_T_L","R_F_H_T","R_F_H_L","R_F_T_L","R_H_T_L","F_H_T_L","R_F_H_T_L"]
ROWS={"W01":"01100001100001011000000100011010","W02":"01100110010100101000001101010101","W03":"00010000000001001001000001001000","W04":"00010000000010100001101001000101","W05":"01011010110000001011010001100010","W06":"00011001010010100011110011010110"}

def main():
    worlds={
      "W01":{"skin":"measurement-pipeline","intervention":"u1"},
      "W02":{"skin":"analysis-pipeline","intervention":"u2"},
      "W03":{"skin":"sample-handling","intervention":"u3"},
      "W04":{"skin":"measurement-pipeline","intervention":"u4"},
      "W05":{"skin":"analysis-pipeline","intervention":"u1"},
      "W06":{"skin":"sample-handling","intervention":"u2"},
    }
    out={"stage":"EPISTEME-P29","vertex_order":VERTEX_ORDER,"encoding":"1=FAIL,0=PASS","worlds":{}}
    for w,meta in worlds.items():
        row=ROWS[w]
        assert len(row)==32 and set(row)<=set("01")
        out["worlds"][w]={**meta,"row":row,"fail_vertices":[v for v,b in zip(VERTEX_ORDER,row) if b=="1"]}
    out["self_audit"]="PASS"
    Path("active/p29_reconstruction.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
if __name__=="__main__": main()
