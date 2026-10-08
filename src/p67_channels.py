"""P67 channel treatments. The schema and json_object arms share an identical prompt."""
from __future__ import annotations
import hashlib,json
from p42_reopen import PROMPT,parse
from p66_relational_binding import packet,expected_valid
TASKS=('BH1','BT1','DH1','DT1')
CHANNELS=('schema','json_object','plain')
VERTICES=('I','R','T','R_T','F_H','R_F_H','F_T_L','R_F_H_T_L')
DRAWS=(1,2)
N_CALLS=len(TASKS)*len(CHANNELS)*len(VERTICES)*2*len(DRAWS)
PLAIN_PROMPT=PROMPT.split('Return only a JSON object with exactly these keys:')[0]+'Return only the token NONE, or the exact single-line string CHALLENGE|u1|different. No further text.'

def build(task,vertex,semantic,alias,channel):
    assert task in TASKS and vertex in VERTICES and semantic in ('valid','null') and channel in CHANNELS
    pkt=packet(task,vertex,semantic,alias)
    base=PROMPT if channel!='plain' else PLAIN_PROMPT
    return base+'\n\nARCHIVE:\n'+json.dumps(pkt,ensure_ascii=False),hashlib.sha256(json.dumps(pkt,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def classify(raw,channel,task,semantic):
    try:
        if channel=='plain':
            t=(raw or '').strip()
            if t not in ('NONE','CHALLENGE|u1|different'):return {'format_valid':False,'semantic_correct':None,'answer':'unscorable'}
            yes=t=='CHALLENGE|u1|different'
        else:
            obj=parse(raw)
            ch=obj.get('challenge');none=ch is None or str(ch).strip().upper()=='NONE'
            yes=not none and obj.get('intervention')=='u1' and obj.get('predicted_direction')=='different'
            if not yes and not none:return {'format_valid':True,'semantic_correct':False,'answer':'other'}
        return {'format_valid':True,'semantic_correct':yes==expected_valid(task,semantic),'answer':'challenge' if yes else 'none'}
    except (ValueError,TypeError,KeyError,AttributeError):
        return {'format_valid':False,'semantic_correct':None,'answer':'unscorable'}

def self_test():
    assert N_CALLS==384
    assert classify('NONE','plain','BH1','null')['semantic_correct'] is True
    assert classify('NONE','plain','BH1','valid')['semantic_correct'] is False
    assert classify('CHALLENGE|u1|different','plain','BH1','valid')['semantic_correct'] is True
    assert classify('CHALLENGE|u1|different','plain','DH1','valid')['semantic_correct'] is False
    a,h1=build('BH1','R','valid','A','schema')
    b,h2=build('BH1','R','valid','A','json_object')
    c,h3=build('BH1','R','valid','A','plain')
    assert a==b and h1==h2==h3 and c!=a
    print('P67_CHANNEL_PREFLIGHT_PASS calls=384 paired-packet-equality=PASS')
if __name__=='__main__':self_test()
