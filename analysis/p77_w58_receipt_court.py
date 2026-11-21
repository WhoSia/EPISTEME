"""Audit archived P77 W53 JSON against W54 ZIP without rerunning PIV.

Run: python w58_receipt_court.py W53-receipt.json W54-evidence.zip
No network, image decoding, publication-level p-value or sample inference.
"""
import hashlib
import json
import math
import sys
from pathlib import Path
from zipfile import ZipFile

MEMBER = 'EPISTEME-P77-W54-WT-Time-Sensitivity.json'
POLICIES = ('pair_offset_minus1', 'pair_original', 'pair_offset_plus1',
            'centered_moving_average_halfwidth1')


def assert_close(actual, expected, context, atol=1e-10):
    if not math.isclose(float(actual), float(expected), rel_tol=0, abs_tol=atol):
        raise ValueError(f'{context}: {actual!r} != {expected!r}')


def analyze(w53_bytes, zip_bytes):
    w53 = json.loads(w53_bytes)
    from io import BytesIO
    with ZipFile(BytesIO(zip_bytes)) as z:
        w54 = json.loads(z.read(MEMBER))
        for name in ('F_037.tif', 'F_053.tif'):
            hash_ = hashlib.sha256(z.read('w54data/' + name)).hexdigest()
            if hash_ != w54['input_sha256'][name]:
                raise ValueError(f'archive/source mask hash mismatch: {name}')
    digest53 = hashlib.sha256(w53_bytes).hexdigest()
    if digest53 != w54['source_receipt_sha256']:
        raise ValueError('W54 is not descended from this exact W53 receipt')
    if not w54['w53_central_projections_exact']:
        raise ValueError('W54 did not independently check W53 central outputs')
    by_time = {entry['minutes']: entry for entry in w53['measurements']}
    for minute, start in ((9, 38), (17, 54)):
        if by_time[minute]['frames'] != [start, start + 1]:
            raise ValueError('changed central frame identification')
        earlier = {(x['orientation_parameter'], x['reference_axis_quadrant']):
                   x['clockwise_positive_um_per_min'] for x in by_time[minute]['projections']}
        later = {(x['orientation_parameter'], x['reference_axis_quadrant']):
                 x['clockwise_positive_um_per_min'] for x in w54['original_projection_rows'][str(start)]}
        if earlier.keys() != later.keys():
            raise ValueError('mismatch of orientation labels')
        for key in earlier:
            assert_close(earlier[key], later[key], f'W53/W54 {minute} {key}')

    measurements = {}
    for row in w54['results']:
        k = (row['orientation'], row['quadrant'])
        name = row['reduction']
        if name not in POLICIES or name in measurements.setdefault(k, {}):
            raise ValueError('unexpected or duplicate reduction')
        assert_close(row['17_min_um_per_min'] - row['9_min_um_per_min'],
                     row['difference_um_per_min'], f'difference {k} {name}')
        measurements[k][name] = row['difference_um_per_min']
    if len(measurements) != 4 or any(set(x) != set(POLICIES) for x in measurements.values()):
        raise ValueError('incomplete four-setting by four-policy design')

    fixed = {(r['orientation'], r['quadrant']): r for r in
             w54['held_contour_control']['shifted_rows']}
    if fixed.keys() != measurements.keys() or not w54['held_contour_control']['central_replay_equal']:
        raise ValueError('fixed-mask negative control incomplete')
    rows = []
    for key in sorted(measurements):
        x = measurements[key]
        average = sum(x[p] for p in POLICIES[:3]) / 3
        assert_close(x[POLICIES[3]], average, f'temporal average {key}')
        f = fixed[key]
        assert_close(f['late'] - f['early'], f['difference'], f'fixed-mask {key}')
        rows.append({'orientation': key[0], 'quadrant': key[1],
                     'offset_minus1': x[POLICIES[0]],
                     'central': x[POLICIES[1]],
                     'offset_plus1': x[POLICIES[2]],
                     'three_pair_mean': x[POLICIES[3]],
                     'plus1_fixed_mask': f['difference'],
                     'mask_effect_at_plus1': x[POLICIES[2]] - f['difference']})
    def positive(k):
        return sum(row[k] > 0 for row in rows)
    return {
        'source_sha256_match': digest53,
        'archive_sha256': hashlib.sha256(zip_bytes).hexdigest(),
        'mask_bytes_checked': ['F_037.tif', 'F_053.tif'],
        'settings_not_independent_specimens': len(rows),
        'sign_counts': {k: positive(k) for k in
            ('offset_minus1','central','offset_plus1','three_pair_mean','plus1_fixed_mask')},
        'max_absolute_mask_effect_at_plus1': max(abs(r['mask_effect_at_plus1']) for r in rows),
        'rows': rows,
        'limitation': 'One WT embryo, four alternative settings of one input, not four independent specimens. No author production t0 or Figure 2E group p-value.',
    }


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: w58_receipt_court.py W53.json W54.zip')
    output = analyze(Path(sys.argv[1]).read_bytes(), Path(sys.argv[2]).read_bytes())
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
