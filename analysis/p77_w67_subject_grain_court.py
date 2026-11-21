"""W67: evidence-limited sample-grain accounting on held Zenodo original bytes.

No statement here identifies the authors' actual ANOVA input.  The six disjoint
800-record strata hypothesis is tested *conditional on* use of only the 2,400
published records per repository.  Canonical JSON object identity is not proof
of biological sample identity or of a manuscript execution run.
"""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

EXPECTED_SHA256 = 'bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c'
FILES = {
    'liver': 'liver_cancer_800_gpt_output_updated.json',
    'lung': 'lung_cancer_800_gpt_output.json',
    'ovarian': 'ovarian_cancer_800_gpt_output.json',
}


def parse_json_stream(blob):
    """Read either a JSON array or concatenated JSON objects, without eval."""
    s = blob.decode('utf-8-sig')
    dec = json.JSONDecoder()
    out, i = [], 0
    while i < len(s):
        while i < len(s) and s[i].isspace():
            i += 1
        if i == len(s):
            break
        obj, i = dec.raw_decode(s, i)
        out.extend(obj if isinstance(obj, list) else [obj])
    if any(not isinstance(v, dict) for v in out):
        raise ValueError('A source record is not a JSON object')
    return out


def pool_lower_bound(available_rows, subjects, rows_each):
    """If all subjects use only a fixed set of available rows, is disjointness possible?"""
    if min(available_rows, subjects, rows_each) <= 0:
        raise ValueError('Positive population, subject and stratum counts required')
    needed = subjects * rows_each
    return {
        'published_candidate_slots': available_rows,
        'subcohorts': subjects,
        'rows_claimed_per_subcohort': rows_each,
        'subject_memberships_required': needed,
        'minimum_repeated_memberships_if_only_published_pool': max(0, needed - available_rows),
        'pairwise_disjoint_possible_under_same_pool': needed <= available_rows,
        'note': ('Only a conditional counting result. Different unarchived candidate samples '
                 'or a different definition of subject may resolve the source discrepancy.'),
    }


def audit(original_zip):
    path = Path(original_zip)
    b = path.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    if h != EXPECTED_SHA256:
        raise ValueError('Held release ZIP SHA-256 does not match the verified original')
    canon_sets = {}
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError('Original ZIP failed CRC')
        for cohort, filename in FILES.items():
            records = parse_json_stream(z.read('Data/' + filename))
            if len(records) != 800:
                raise ValueError('Expected original 800 rows per cancer cohort')
            if any(not isinstance(x.get('BioSample'), dict) for x in records):
                raise ValueError('Missing original BioSample object')
            canon_sets[cohort] = {
                json.dumps(x['BioSample'], sort_keys=True, separators=(',', ':'),
                           ensure_ascii=False) for x in records
            }
    across = set().union(*canon_sets.values())
    return {
        'zip_sha256': h,
        'cohort_record_rows': {key: 800 for key in FILES},
        'cohort_unique_source_json_objects': {k: len(v) for k, v in canon_sets.items()},
        'released_source_record_positions': 2400,
        'distinct_canonical_source_json_objects': len(across),
        'repeated_canonical_source_object_positions': 2400 - len(across),
        'between_cancer_canonical_json_intersections': {
            f'{a}_vs_{b}': len(canon_sets[a] & canon_sets[b])
            for a, b in (('liver','lung'),('liver','ovarian'),('lung','ovarian'))
        },
        'paper_biosample_six_by_800': pool_lower_bound(2400, 6, 800),
        'paper_geo_six_by_800': pool_lower_bound(2400, 6, 800),
        'scope_limit': ('Canonical JSON equality cannot establish sample identity. The manuscript '
                        'may have run unarchived samples, independent new model calls, or another '
                        'subject definition. Six actual ANOVA subject membership lists remain missing.'),
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python p77_w67_subject_grain_court.py /path/to/Zenodo_Data.zip')
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
