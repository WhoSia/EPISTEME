from __future__ import annotations
import argparse,json
from pathlib import Path
STAGE='EPISTEME-P58'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--recovery',required=True);ap.add_argument('--p57',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    r=json.loads(Path(a.recovery).read_text(encoding='utf-8'))
    p57=json.loads(Path(a.p57).read_text(encoding='utf-8'))
    if r['stage']!=STAGE or r['attempted_cells']!=38 or r['successful_source_rows_replayed']!=0:
        raise RuntimeError('P58_RECOVERY_RECEIPT_INVALID')
    if p57.get('stage')!='EPISTEME-P57': raise RuntimeError('P57_ANALYZER_STAGE_INVALID')
    if not r['complete'] and p57.get('constitutional_verdict')!='TECHNICAL_HOLD':
        raise RuntimeError('INCOMPLETE_RECOVERY_MUST_HOLD')
    out={
      'stage':STAGE,
      'descriptor':'Failed-Cell-Only Hosted-Inference Recovery, Provider-Structured-Output Failure Separation, Exact Fresh-Task Tensor Completion, Frozen 15-Test Family Resumption & P57 Measurement-Law Adjudication',
      'recovery':r,
      'p57_adjudication_resumed':bool(r['complete']),
      'p57_constitutional_verdict':p57.get('constitutional_verdict'),
      'authority':'P58 adds no new scientific test. It either restores exact P57 technical completeness and exposes the unchanged frozen P57 verdict, or preserves TECHNICAL_HOLD.',
      'p57_result':p57
    }
    Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8')
if __name__=='__main__':main()
