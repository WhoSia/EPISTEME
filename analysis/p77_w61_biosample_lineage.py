"""Audit released BioSample source fields; not a reconstruction of author metrics.

Usage: python analysis/p77_w61_biosample_lineage.py Data.zip
Compares source dictionaries after removing explicit accession, not biological identity.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from p77_w60_zenodo_cohort_court import load_archive, parse_concatenated_json

FILES = {
    'liver': ('liver_cancer_800_gpt_output_updated.json', 'liver_cancer_llama3_output_dd.json', 'liver_cancer_llama3_output_cedar.json', 'liver_cancer_medllama_output.json'),
    'lung': ('lung_cancer_800_gpt_output.json', 'lung_cancer_llama3_output.json', 'lung_cancer_medllama_output.json'),
    'ovarian': ('ovarian_cancer_800_gpt_output.json', 'ovarian_cancer_llama3_output.json', 'ovarian_cancer_medllama_biosample_output.json'),
}

def key(row):
    source = row['BioSample']
    if not isinstance(source, dict):
        raise ValueError('BioSample must be an object')
    return json.dumps({k:v for k,v in source.items() if k != 'biosample_accession'}, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

def compare(ref, rows):
    a, b = [key(x) for x in ref], [key(x) for x in rows]
    ca, cb = Counter(a), Counter(b)
    accessions = [r['BioSample']['biosample_accession'] for r in rows if 'biosample_accession' in r['BioSample']]
    return {'rows':len(b), 'accessions':sum('biosample_accession' in r['BioSample'] for r in rows),
            'unique_accessions':len(set(accessions)),
            'unique_source_signatures':len(cb), 'duplicate_signature_rows':sum(n for n in cb.values() if n > 1),
            'position_matches':sum(x == y for x,y in zip(a,b)),
            'multiset_overlap':sum((ca & cb).values()),
            'unique_ref_join_rows':sum(ca[x] == 1 for x in b),
            'ambiguous_ref_join_rows':sum(ca[x] > 1 for x in b),
            'unmatched_ref_rows':sum(ca[x] == 0 for x in b)}

def audit(path):
    items = load_archive(path, 'v2v3')
    result = {}
    for cohort, filenames in FILES.items():
        parsed = {f:parse_concatenated_json(items['Data/'+f]) for f in filenames}
        ref=parsed[filenames[0]]
        result[cohort]={f:compare(ref,rows) for f,rows in parsed.items()}
    return {'archive_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(), 'cohorts':result,
            'limitations':'Signature equality is not proof of identical biological sample; accession absent cannot be recovered through position alone.'}

if __name__ == '__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python p77_w61_biosample_lineage.py Data.zip')
    print(json.dumps(audit(sys.argv[1]), indent=2))

