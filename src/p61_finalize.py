import argparse,json
from pathlib import Path

def main():
    a=argparse.ArgumentParser();a.add_argument('--recovery',required=True);a.add_argument('--p60',required=True);a.add_argument('--out',required=True);x=a.parse_args()
    r=json.loads(Path(x.recovery).read_text()); p=json.loads(Path(x.p60).read_text())
    if r.get('stage')!='EPISTEME-P61' or r.get('attempted_cells')!=254 or r.get('successful_source_rows_replayed')!=0:
        raise RuntimeError('P61_RECOVERY_RECEIPT_INVALID')
    if p.get('stage')!='EPISTEME-P60': raise RuntimeError('P60_ANALYZER_STAGE_INVALID')
    if not r.get('complete') and p.get('constitutional_verdict')!='TECHNICAL_HOLD':
        raise RuntimeError('INCOMPLETE_RECOVERY_MUST_HOLD')
    out={
      'stage':'EPISTEME-P61',
      'descriptor':'Failed-Cell-Only Prospective Context Recovery, Cross-Task Structured-Output Failure Localization, Exact 49,152-Cell Dual-Endpoint Tensor Completion, Frozen R/T Carrier-Interaction Court Resumption & P60 Scientific Adjudication',
      'recovery':r,
      'p60_adjudication_resumed':bool(r.get('complete')),
      'p60_constitutional_verdict':p.get('constitutional_verdict'),
      'authority':'P61 adds no new scientific test. It either restores exact P60 technical completeness and exposes the unchanged frozen P60 verdict, or preserves TECHNICAL_HOLD.',
      'p60_result':p
    }
    Path(x.out).write_text(json.dumps(out,indent=2))
if __name__=='__main__': main()
