"""Source-layer audit for the held Sundaram et al. 2026 Zenodo v3 ZIP + XLSX.

W61 evidence goal: trace accession identity separately for original input, LLM-only
payload, and LLM+CEDAR payload. Raw member data never leave the archive or appear
in the aggregate report. This does NOT reproduce the manuscript's scoring run.

python p77_w61_layer_provenance.py <zenodo_v2v3.zip> <workbook.xlsx> [receipt.json]
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from collections import Counter

ZIP_SHA256 = 'bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c'
XLSX_MD5 = '66fa6ffbf5470a73c9737f3d94470bbc'
CANCERS = ('liver', 'lung', 'ovarian')
MODELS = ('gpt4', 'llama3', 'medllama')


def records(payload: bytes) -> list[dict]:
    text = payload.decode('utf-8-sig')
    result = []
    dec = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos == len(text):
            break
        obj, pos = dec.raw_decode(text, pos)
        result.extend(obj if isinstance(obj, list) else [obj])
    if any(not isinstance(r, dict) for r in result):
        raise ValueError('JSON stream contains non-record values')
    return result


def accession(x: dict):
    if not isinstance(x, dict):
        raise ValueError('Missing original-record dictionary')
    gse, gsms = x.get('gse'), x.get('gsm')
    if not isinstance(gse, str) or not isinstance(gsms, list) or not gsms:
        raise ValueError('Missing GSE/GSM accession')
    return (gse, tuple(gsms))


def _matches(a, b):
    return sum(x == y for x, y in zip(a, b))


def analyze_payload(payloads: dict[str, bytes]) -> dict:
    original = {c: records(payloads[f'Data/{c}_cancer_geo.json']) for c in CANCERS}
    raw_id = {c: list(map(accession, original[c])) for c in CANCERS}
    for c in CANCERS:
        if len(raw_id[c]) != 800 or len(set(raw_id[c])) != 800:
            raise ValueError('Unexpected original accession denominator: ' + c)
    for idx, c in enumerate(CANCERS):
        for other in CANCERS[idx + 1:]:
            if set(raw_id[c]) & set(raw_id[other]):
                raise ValueError('Original cohort collision')

    data, report = {}, []
    for c in CANCERS:
        for m in MODELS:
            name = f'Data/{c}_cancer_{m}_geo_output.json'
            rs = records(payloads[name])
            if len(rs) != 800 or any(set(('BioSample', 'LLM', 'LLM+CEDAR')) - set(r) for r in rs):
                raise ValueError('Output denominator or layers: ' + name)
            keys = [accession(r['BioSample']) for r in rs]
            if len(set(keys)) != 800:
                raise ValueError('Repeated output source accession: ' + name)
            record = {'cancer': c, 'model': m, 'records': len(keys),
                      'source_order_matches': {o: _matches(keys, raw_id[o]) for o in CANCERS},
                      'source_key_overlap': {o: len(set(keys) & set(raw_id[o])) for o in CANCERS}}
            report.append(record)
            data[c, m] = rs

    l4 = data['liver', 'gpt4']
    p4 = data['lung', 'gpt4']
    gpt4_same = _matches([r['LLM'] for r in l4], [r['LLM'] for r in p4])
    liver_llm_own_gse = sum(r['LLM'].get('bioproject_accession') == r['BioSample']['gse'] for r in l4)
    liver_llm_lung_gse = sum(r['LLM'].get('bioproject_accession') == p4[i]['BioSample']['gse'] for i, r in enumerate(l4))
    liver_llm_gse_present = sum('bioproject_accession' in r['LLM'] for r in l4)
    liver_cedar_own_gse = sum(r['LLM+CEDAR'].get('geo_accession') == r['BioSample']['gse'] for r in l4)
    if gpt4_same != 800 or liver_cedar_own_gse != 800:
        raise ValueError('Known W61 split-layer control changed')

    llama = {c: data[c, 'llama3'] for c in CANCERS}
    ll_lung = llama['lung']
    llama_lung_source_equal = {c: _matches([r['BioSample'] for r in llama[c]],
                                           [r['BioSample'] for r in ll_lung]) for c in CANCERS}
    if any(value != 800 for value in llama_lung_source_equal.values()):
        raise ValueError('Known W60 Llama cohort control changed')
    return {
        'original_denominators': {c: len(raw_id[c]) for c in CANCERS},
        'input_overlap_count': 0,
        'original_to_output_alignment': report,
        'gpt4_liver_split_layer': {
            'llm_dict_identical_to_lung_gpt4': gpt4_same,
            'liver_llm_bioproject_present': liver_llm_gse_present,
            'liver_llm_bioproject_matches_liver': liver_llm_own_gse,
            'liver_llm_bioproject_matches_lung': liver_llm_lung_gse,
            'liver_cedar_geo_accession_matches_liver': liver_cedar_own_gse,
            'llm_source_mismatch_cannot_be_inferred_from_biosample_alone': True,
        },
        'llama3_biosample_equals_lung_by_cancer': llama_lung_source_equal,
        'annotation_files': {
            'geo_lung': 'Data/annotated_800_geo_simple_lung.txt' in payloads,
            'geo_ovary': 'Data/annotated_800_geo_simple_ovary.txt' in payloads,
            'geo_liver': 'Data/annotated_800_geo_simple_liver.txt' in payloads,
        },
    }


def audit(zip_path: Path, workbook_path: Path) -> dict:
    zbytes, xbytes = zip_path.read_bytes(), workbook_path.read_bytes()
    if hashlib.sha256(zbytes).hexdigest() != ZIP_SHA256:
        raise ValueError('Wrong Zenodo v2/v3 ZIP SHA256')
    if hashlib.md5(xbytes).hexdigest() != XLSX_MD5:
        raise ValueError('Wrong original Zenodo workbook MD5')
    with zipfile.ZipFile(zip_path) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        names = archive.namelist()
        if len(names) != len(set(names)) or any(n.startswith('/') or '..' in n.split('/') for n in names):
            raise ValueError('Unsafe ZIP path or duplicate')
        payloads = {n: archive.read(n) for n in names if n.startswith('Data/') and not n.endswith('/')}
    output = analyze_payload(payloads)
    from openpyxl import load_workbook
    workbook = load_workbook(workbook_path, read_only=True, data_only=True)
    accession_cells = []
    for sheet in workbook:
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and re.search(r'\b(?:GSE|GSM)\d+\b', cell.value):
                    accession_cells.append((sheet.title, cell.coordinate))
    output.update({
        'source_zip_sha256': ZIP_SHA256,
        'workbook_md5': XLSX_MD5,
        'workbook_sheets': list(workbook.sheetnames),
        'workbook_accession_bearing_cells': len(accession_cells),
        'scope': 'Held release artifact only; no author model execution / statistical table provenance proof',
    })
    return output


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) not in (2, 3):
        raise SystemExit('usage: p77_w61_layer_provenance.py v2v3_Data.zip original.xlsx [out.json]')
    out = audit(Path(argv[0]), Path(argv[1]))
    rendered = json.dumps(out, indent=2, ensure_ascii=False) + '\n'
    if len(argv) == 3:
        Path(argv[2]).write_text(rendered)
    print(rendered)


if __name__ == '__main__':
    main()
