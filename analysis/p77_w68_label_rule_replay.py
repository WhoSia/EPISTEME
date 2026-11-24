"""W68: release-label replay, not biological gold truth or manuscript run provenance."""
import hashlib, json, re, sys, zipfile
from collections import Counter
from pathlib import Path
SHA = 'bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c'
RULE = (('lung', ('lung',)), ('liver', ('liver','hcc')), ('ovary', ('ovary','ovarian')), ('blood', ('pbmc','blood')), ('plasma', ('plasma',)), ('lymph', ('lymph',)))
LUNG = (('lung', ('lung',)), ('blood', ('PBMC','blood')), ('lymph', ('lymph',)), ('plasma', ('plasma',)))
LIVER = (('liver', ('liver','HCC')), *LUNG[1:])
OVARY = (('ovary', ('ovary','ovarian')), ('plasma', ('plasma',)), ('blood', ('PBMC','blood')), ('lymph', ('lymph',)))

def records(b):
    s=b.decode('utf-8-sig'); d=json.JSONDecoder(); i=0; out=[]
    while i<len(s):
        while i<len(s) and s[i].isspace(): i+=1
        if i==len(s): break
        x,i=d.raw_decode(s,i); out.extend(x if isinstance(x,list) else [x])
    if any(not isinstance(x,dict) for x in out): raise ValueError('Invalid JSON row')
    return out

def predict(v, rules=RULE, whole_word=False):
    s=v.lower() if isinstance(v,str) else ''
    for label,keys in rules:
        if any((re.search(r'\b'+re.escape(k)+r'\b',s) is not None) if whole_word else k in s for k in keys): return label
    return 'unknown'

def compare(pred, labels):
    if len(pred)!=800 or len(labels)!=800: raise ValueError('Expected 800 aligned rows')
    errors=Counter((a,b) for a,b in zip(pred,labels) if a!=b)
    return {'matches':800-sum(errors.values()),'mismatches':{a+' -> '+b:n for (a,b),n in sorted(errors.items())}}

def retrieval(a,b,query):
    tp=sum(x==query and y==query for x,y in zip(a,b)); hits=a.count(query); pos=b.count(query)
    return {'tp':tp,'fp':hits-tp,'fn':pos-tp,'recall':tp/pos if pos else None,'precision':tp/hits if hits else None,'f1':2*tp/(hits+pos) if hits+pos else None}

def audit(path):
    raw=Path(path).read_bytes(); h=hashlib.sha256(raw).hexdigest()
    if h!=SHA: raise ValueError('ZIP SHA mismatch')
    out={}
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None: raise ValueError('ZIP CRC mismatch')
        for cancer,organ in (('liver','liver'),('lung','lung'),('ovarian','ovary')):
            for db in ('biosample','geo'):
                name=cancer+'_cancer_'+('800_gpt_output'+('_updated' if cancer=='liver' else '') if db=='biosample' else 'gpt4_geo_output')+'.json'
                label='Data/annotated_800_'+('geo_' if db=='geo' else '')+'simple_'+organ+'.txt'
                key=db+'_'+cancer
                if label not in z.namelist():
                    out[key]={'status':'expected label member missing','expected_member':label}; continue
                rows=records(z.read('Data/'+name)); labels=z.read(label).decode('utf-8-sig').splitlines()
                if len(rows)!=800 or len(labels)!=800: raise ValueError('Expected 800 rows and labels')
                if any(not isinstance(x.get('BioSample'),dict) for x in rows): raise ValueError('Missing source layer')
                v=[x['BioSample'].get('tissue') for x in rows]
                sub=[predict(x) for x in v]; word=[predict(x,whole_word=True) for x in v]
                # Lung is executable historical code; liver/ovary are reconstructions from commented variants.
                # GEO uses the paper rule, not a claimed historical GEO annotator.
                hist=[predict(x,{'lung':LUNG,'liver':LIVER,'ovarian':OVARY}[cancer] if db=='biosample' else RULE) for x in v]
                out[key]={'paper_substring':compare(sub,labels),'paper_whole_word':compare(word,labels),'historically_motivated_candidate':compare(hist,labels), 'candidate_against_same_heuristic_reference':{q:retrieval(hist,labels,q) for q in (organ,'blood')}}
    return {'zip_sha256':h,'cohorts':out,'warning':'Positional pairing. Reconstructed variants selected after inspecting historical source and released labels; not independent ground truth or production execution evidence. GEO liver expected named member absent; other label representations not ruled out.'}

if __name__=='__main__': print(json.dumps(audit(sys.argv[1]),indent=2))
