"""P67 provider-free integration test: packet coupling, oracle, and complete result court."""
import json,tempfile
from pathlib import Path
from p42_reopen import SCHEMA
from p48_seed_fingerprints import panel_cells
from p67_channels import CHANNELS,DRAWS,TASKS,VERTICES,N_CALLS,build,classify
from p67_pilot_analyze import evaluate

def run():
    null_json=json.dumps({'challenge':None,'intervention':None,'predicted_direction':None,'rationale_ids':[]})
    valid_json=json.dumps({'challenge':'contrast','intervention':'u1','predicted_direction':'different','rationale_ids':['alpha']})
    assert classify('NONE','schema','BH1','valid')['format_valid'] is False
    assert classify(null_json,'schema','BH1','null')['semantic_correct'] is True
    assert classify(valid_json,'schema','BH1','valid')['semantic_correct'] is True
    assert classify(valid_json,'json_object','DH1','valid')['semantic_correct'] is False
    cells=[c for c in panel_cells() if c['vertex'] in VERTICES]
    assert len(cells)==16 and N_CALLS==384
    with tempfile.TemporaryDirectory() as tmp:
        for task in TASKS:
            rows=[]
            for draw in DRAWS:
                for c in cells:
                    msgs={ch:build(task,c['vertex'],c['semantic'],c['alias'],ch) for ch in CHANNELS}
                    assert msgs['schema']==msgs['json_object']
                    assert len({item[1] for item in msgs.values()})==1
                    for ch in CHANNELS:
                        raw=('CHALLENGE|u1|different' if task.startswith('B') and c['semantic']=='valid' else 'NONE') if ch=='plain' else (valid_json if task.startswith('B') and c['semantic']=='valid' else null_json)
                        scored=classify(raw,ch,task,c['semantic'])
                        rows.append({'task':task,'draw':draw,'channel':ch,'cell_index':c['cell_index'],
                                     'packet_sha256':msgs[ch][1],'provider_status':'RESPONSE',**scored})
            Path(tmp,task+'.json').write_text(json.dumps({'stage':'EPISTEME-P67','pilot':True,'task':task,'rows':rows}))
        report=evaluate(tmp)
        assert report['calls']==384 and report['paired_packet_strata']==128
        assert report['pilot_verdict']=='MEASUREMENT_FEASIBLE'
        assert all(arm['executable_correct']==128 for arm in report['arms'].values())
    print('P67_INTEGRATION_PASS synthetic_calls=384 provider_calls=0')
if __name__=='__main__':run()
