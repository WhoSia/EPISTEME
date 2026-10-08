"""P67 384-call prospective output-channel feasibility pilot; no repository writeback."""
from __future__ import annotations
import argparse,json,random,time
from pathlib import Path
from groq import Groq
from p42_reopen import SCHEMA
from p48_seed_fingerprints import panel_cells
from p67_channels import CHANNELS,DRAWS,TASKS,VERTICES,build,classify

def run(task):
    cells=[c for c in panel_cells() if c['vertex'] in VERTICES]
    assert len(cells)==16
    plan=[(draw,channel,c) for draw in DRAWS for channel in CHANNELS for c in cells]
    random.Random(6700+TASKS.index(task)).shuffle(plan)
    client=Groq(max_retries=0)
    rows=[]
    for draw,channel,c in plan:
        prompt,h=build(task,c['vertex'],c['semantic'],c['alias'],channel)
        request={'model':'openai/gpt-oss-120b','messages':[{'role':'user','content':prompt}],
                 'temperature':.2,'top_p':.95,'max_completion_tokens':1536,'stream':False,
                 'reasoning_effort':'medium','reasoning_format':'hidden'}
        if channel=='schema':
            request['response_format']={'type':'json_schema','json_schema':{'name':'episteme_p42','strict':True,'schema':SCHEMA}}
        elif channel=='json_object':request['response_format']={'type':'json_object'}
        start=time.perf_counter_ns()
        try:
            response=client.chat.completions.create(**request)
            raw=response.choices[0].message.content or ''
            parsed=classify(raw,channel,task,c['semantic'])
            status='RESPONSE';error=None
        except Exception as exc:
            raw=None;parsed={'format_valid':False,'semantic_correct':None,'answer':'unobserved'}
            status='PROVIDER_FAILURE';error=(type(exc).__name__+':'+str(exc))[:900]
        rows.append({**c,'task':task,'draw':draw,'channel':channel,'packet_sha256':h,
                     'provider_status':status,**parsed,'raw_response':raw,'error':error,
                     'latency_ms':(time.perf_counter_ns()-start)/1e6,'api_seed_sent':False,'sdk_max_retries':0})
    assert len(rows)==96
    return {'stage':'EPISTEME-P67','pilot':True,'task':task,'rows':rows}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--task',choices=TASKS,required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(run(args.task),ensure_ascii=False))
