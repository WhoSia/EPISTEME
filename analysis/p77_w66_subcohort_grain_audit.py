"""W66: audit the six organ/blood task grains against the released source.

The original 800-record pool is reused between two queries per cancer,
while the *heuristic relevant-positive subsets* are disjoint by definition.
Neither finding confirms (or refutes) the authors' actual statistical
subject independence without production subject/run mapping.

python analysis/p77_w66_subcohort_grain_audit.py original_v2v3_Data.zip
"""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from p77_w65_query_parser_sensitivity import CONFIG, ZIP_SHA256, parse_stream


def describe_task_grain(original_records, labels, organ):
    if len(original_records) != 800 or len(labels) != 800:
        raise ValueError('Expected full 800-record source and aligned labels')
    organ_indices = {i for i, label in enumerate(labels) if label == organ}
    blood_indices = {i for i, label in enumerate(labels) if label == 'blood'}
    if organ_indices & blood_indices:
        raise ValueError('One released label cannot be both organ and blood')
    return {
        'shared_source_candidate_rows_for_both_queries': len(original_records),
        'organ_query': organ,
        'organ_relevant_rows': len(organ_indices),
        'blood_query': 'blood',
        'blood_relevant_rows': len(blood_indices),
        'overlap_of_heuristic_relevant_positive_indices': len(organ_indices & blood_indices),
        'remaining_rows_in_neither_relevant_subset': 800 - len(organ_indices | blood_indices),
        'interpretation': 'Same 800-row candidate pool; distinct positive label sets. This does not identify manuscript ANOVA subjects or independence.',
    }


def audit(path):
    b = Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest() != ZIP_SHA256:
        raise ValueError('Unverified release ZIP')
    result = {}
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError('CRC mismatch')
        for cancer, cfg in CONFIG.items():
            labels = z.read('Data/' + cfg['label']).decode('utf-8-sig').splitlines()
            rows = parse_stream(z.read('Data/' + cfg['outputs']['gpt4'][0]))
            result[cancer] = describe_task_grain(rows, labels, cfg['query'])
    return {
        'zip_sha256': ZIP_SHA256,
        'six_query_label_tasks': result,
        'caution': ('The published revised manuscript Appendix C says six sub-cohorts '
                    'are independent subjects and describes 800 input samples. '
                    'The released task construction reuses the 800-row pool '
                    'across both queries per cancer but has non-overlapping '
                    'positive label subsets; original run-level unit construction '
                    'must be identified before diagnosing an ANOVA independence violation.'),
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: p77_w66_subcohort_grain_audit.py Data.zip')
    print(json.dumps(audit(sys.argv[1]), indent=2))
