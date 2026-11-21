"""W66: factorial parser and source-label circular-shift negative controls.

Requires the original held Sundaram v2/v3 Data.zip; conclusions concern
release artifacts with heuristic positionally joined labels, NOT the
published manuscript's run, accession gold truth, or AI causal effects.

python analysis/p77_w66_parser_factorial_and_label_court.py Data.zip
"""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
import zipfile

from p77_w65_query_parser_sensitivity import CONFIG, ZIP_SHA256, parse_stream

MODES = {
    "exact": (False, False),
    "alias_only": (True, False),
    "normalize_only": (False, True),
    "alias_and_normalize": (True, True),
}


def contains(layer, query, alias=False, normalize=False):
    if not isinstance(layer, dict):
        raise ValueError('Expected dictionary-valued metadata layer')
    value = layer.get('tissue', layer.get('tissue_type')) if alias else layer.get('tissue')
    if normalize:
        return isinstance(value, str) and value.strip().casefold() == query.strip().casefold()
    return value == query.lower()


def metrics(rows, labels, layer, query, alias=False, normalize=False):
    if len(rows) != 800 or len(labels) != 800:
        raise ValueError('A verified 800-row positional pairing is required')
    if any(not isinstance(r, dict) or layer not in r for r in rows):
        raise ValueError('Missing layer or malformed record')
    hits = [contains(r[layer], query, alias, normalize) for r in rows]
    tp = sum(hit and truth == query for hit, truth in zip(hits, labels))
    fp = sum(hit and truth != query for hit, truth in zip(hits, labels))
    fn = sum(not hit and truth == query for hit, truth in zip(hits, labels))
    return {'tp': tp, 'fp': fp, 'fn': fn, 'hits': tp + fp,
            'precision': tp / (tp + fp) if tp + fp else 0.0,
            'recall': tp / (tp + fn) if tp + fn else 0.0,
            'f1': 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0}


def label_consistency(rows, labels):
    if len(rows) != len(labels) or not rows:
        raise ValueError('Source-label position mismatch')
    groups = defaultdict(Counter)
    for row, label in zip(rows, labels):
        if not isinstance(row, dict) or not isinstance(row.get('BioSample'), dict):
            raise ValueError('Missing original metadata')
        v = row['BioSample'].get('tissue')
        token = v.strip().casefold() if isinstance(v, str) else '<missing>'
        groups[token][label] += 1
    conflict_rows = sum(sum(c.values()) - max(c.values()) for c in groups.values())
    repeat_supported = sum(sum(c.values()) for c in groups.values() if sum(c.values()) >= 2)
    return {'distinct_normalized_tissue_values': len(groups),
            'tissue_values_with_multiple_labels': sum(len(c) > 1 for c in groups.values()),
            'minority_label_rows_within_same_tissue': conflict_rows,
            'rows_with_other_same_tissue_rows': repeat_supported}


def rotate(seq, shift):
    return seq[shift:] + seq[:shift]


def sign(value):
    return int(value > 1e-12) - int(value < -1e-12)


def reversal(model, source, labels, query, metric):
    def delta(norm):
        return (metrics(model, labels, 'LLM+CEDAR', query, False, norm)[metric] -
                metrics(source, labels, 'BioSample', query, False, norm)[metric])
    return sign(delta(False)) * sign(delta(True)) == -1


def audit(archive_path):
    raw = Path(archive_path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != ZIP_SHA256:
        raise ValueError('Original Zenodo source ZIP SHA-256 mismatch')
    rows_and_labels = {}
    cells = 0
    alias_changed = 0
    normalized_changed = 0
    rank_contrasts = 0
    rev_by_policy = Counter()
    ovarian = {}
    with zipfile.ZipFile(archive_path) as z:
        if z.testzip() is not None:
            raise ValueError('Invalid ZIP member CRC')
        for cancer, cfg in CONFIG.items():
            labels = z.read('Data/' + cfg['label']).decode('utf-8-sig').splitlines()
            if len(labels) != 800:
                raise ValueError('Expected 800 heuristic labels: ' + cancer)
            raw_gpt = parse_stream(z.read('Data/' + cfg['outputs']['gpt4'][0]))
            rows_and_labels[cancer] = (raw_gpt, labels)
            for model, (filename, layers) in cfg['outputs'].items():
                rows = parse_stream(z.read('Data/' + filename))
                for layer in layers:
                    for query in (cfg['query'], 'blood'):
                        score = {mode: metrics(rows, labels, layer, query, *opts)
                                 for mode, opts in MODES.items()}
                        cells += 1
                        alias_changed += score['exact'] != score['alias_only']
                        normalized_changed += score['exact'] != score['normalize_only']
                        if cancer == 'ovarian' and model == 'gpt4' and layer in ('BioSample', 'LLM+CEDAR'):
                            ovarian[f'{layer}_{query}'] = score
                if 'BioSample' not in layers:
                    raise ValueError('Output file lacks original source layer')
                for layer in ('LLM', 'LLM+CEDAR'):
                    if layer not in layers:
                        continue
                    for query in (cfg['query'], 'blood'):
                        src = {mode: metrics(rows, labels, 'BioSample', query, *opts)
                               for mode, opts in MODES.items()}
                        out = {mode: metrics(rows, labels, layer, query, *opts)
                               for mode, opts in MODES.items()}
                        for metric in ('precision', 'recall', 'f1'):
                            rank_contrasts += 1
                            base = sign(out['exact'][metric] - src['exact'][metric])
                            for mode in ('alias_only', 'normalize_only', 'alias_and_normalize'):
                                other = sign(out[mode][metric] - src[mode][metric])
                                rev_by_policy[mode] += base * other == -1
    # Shifting labels is a falsification diagnostic, not a randomization null or p-value.
    controls = {}
    for cancer, (rows, labels) in rows_and_labels.items():
        values = [label_consistency(rows, rotate(labels, k)) for k in range(800)]
        controls[cancer] = {
            'original': values[0],
            'number_of_circular_offsets_with_zero_tissue_conflicts': sum(
                v['minority_label_rows_within_same_tissue'] == 0 for v in values),
            'min_conflict_rows_across_nonzero_offsets': min(
                v['minority_label_rows_within_same_tissue'] for v in values[1:]),
            'max_conflict_rows_across_nonzero_offsets': max(
                v['minority_label_rows_within_same_tissue'] for v in values[1:]),
        }
    ovarian_rows, ovarian_labels = rows_and_labels['ovarian']
    ovarian_rank_negative_control = {}
    for metric in ('recall', 'f1'):
        ovarian_rank_negative_control[metric] = {
            'rank_reversal_at_recorded_position': reversal(
                ovarian_rows, ovarian_rows, ovarian_labels, 'blood', metric),
            'rank_reversals_under_all_800_circular_offsets': sum(
                reversal(ovarian_rows, ovarian_rows, rotate(ovarian_labels, k), 'blood', metric)
                for k in range(800)),
        }
    if cells != 56 or rank_contrasts != 108:
        raise ValueError('Unexpected data/model/query accounting')
    return {
        'original_zip_sha256': digest,
        'retrieval_cells': cells,
        'cells_changed_by_alias_only': alias_changed,
        'cells_changed_by_normalization_only': normalized_changed,
        'rank_metric_comparisons': rank_contrasts,
        'strict_rank_reversals_vs_original': dict(rev_by_policy),
        'ovarian_gpt4_factorial': ovarian,
        'source_label_circular_controls': controls,
        'ovarian_blood_reversal_shift_control': ovarian_rank_negative_control,
        'qualification': ('All results are conditional on positional pairing to a heuristic-label text file. '
                          'Circular offsets deliberately invalidate source-label linkage, '
                          'are NOT independent simulations or significance tests, and '
                          'cannot identify original author model/statistical execution.'),
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: p77_w66_parser_factorial_and_label_court.py original_Data.zip')
    print(json.dumps(audit(sys.argv[1]), ensure_ascii=False, indent=2))
