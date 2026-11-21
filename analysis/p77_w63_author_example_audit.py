"""Bounded replay of explicit public notebook examples; not publication reproduction.

Run: python analysis/p77_w63_author_example_audit.py Data.zip
The parser and query reproduce the inspected notebook cells, with fail-closed input checks.
"""
import hashlib, json, sys, zipfile
from pathlib import Path

EXPECTED = 'bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c'

def rule(tissue):
    tissue = tissue.lower()
    # Rules.ipynb checks upper-case PBMC after lowercasing; preserve that behavior.
    if 'lung' in tissue: return 'lung'
    if 'PBMC' in tissue or 'blood' in tissue: return 'blood'
    if 'lymph' in tissue: return 'lymph'
    if 'plasma' in tissue: return 'plasma'
    return 'unknown'

def search(rows, layer, term):
    return [i for i,r in enumerate(rows) if r[layer].get('tissue') == term.lower()]

def evaluate(indices, labels, query):
    truth = {i for i,x in enumerate(labels) if x == query}
    tp = len(set(indices) & truth)
    p = tp/len(indices) if indices else 0
    r = tp/len(truth) if truth else 0
    return {'retrieved':len(indices),'relevant':len(truth),'tp':tp,'fp':len(indices)-tp,
            'fn':len(truth)-tp,'precision':p,'recall':r,'f1':2*p*r/(p+r) if p+r else 0}

def audit(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED: raise ValueError('unexpected ZIP hash')
    with zipfile.ZipFile(path) as z:
        if z.testzip(): raise ValueError('CRC failure')
        def rows(name): return [json.loads(x) for x in z.read('Data/'+name).decode('utf-8').splitlines()]
        def labels(name): return z.read('Data/'+name).decode('utf-8').splitlines()
        lung=rows('lung_cancer_800_gpt_output.json')
        gold=labels('annotated_800_simple_lung.txt')
        ovary=rows('ovarian_cancer_medllama_biosample_output.json')
        ogold=labels('annotated_800_simple_ovary.txt')
    if any(len(x)!=800 for x in (lung,gold,ovary,ogold)): raise ValueError('unexpected row count')
    derived=[rule(r['BioSample'].get('tissue','unknown')) for r in lung]
    comparisons={}
    for layer in ('BioSample','LLM','LLM+CEDAR'):
        found=search(ovary,layer,'blood')
        comparisons[layer]={'notebook_blood_search_ovary_truth':evaluate(found,ogold,'ovary'),
                            'same_query_blood_counterfactual':evaluate(found,ogold,'blood'),
                            'rows_missing_tissue_key':sum('tissue' not in r[layer] for r in ovary)}
    return {'archive_sha256':EXPECTED, 'lung_rule_matches_archive':sum(a==b for a,b in zip(derived,gold)),
            'lung_rule_differences':sum(a!=b for a,b in zip(derived,gold)),
            'ovarian_notebook_example':comparisons,
            'caveat':'Row-order joins and example notebook execution are conditional; manuscript provenance unverified.'}

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: p77_w63_author_example_audit.py Data.zip')
    print(json.dumps(audit(sys.argv[1]),indent=2))

