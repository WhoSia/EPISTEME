"""W59: audit held W53 source bytes, image-index joins and acquisition calibration.

Usage: python analysis/p77_w59_source_anchor_audit.py W53-inputs.zip W53-receipt.json W54-evidence.zip
Reads existing archives only. Does not rerun PIV or query a live image index.
"""
from __future__ import annotations
import hashlib
import io
import json
import math
import re
import sys
from pathlib import Path
from zipfile import ZipFile
from p77_w58_receipt_court import analyze as audit_time_receipts

TARGET_EMBRYO = 'embryo1_210122_2'
REQUIRED_MASKS = (38, 54)


def integrity_check(source_zip: bytes):
    with ZipFile(io.BytesIO(source_zip)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate ZIP entries')
        if any(name.startswith('/') or '\\' in name or '..' in name.split('/') for name in names):
            raise ValueError('Unsafe ZIP member name')
        manifest = json.loads(archive.read('source_manifest.json'))
        listed = manifest['files']
        if set(names) != set(listed) | {'source_manifest.json'}:
            raise ValueError('Unexpected/missing source files in W53 ZIP')
        for name, expected in listed.items():
            info = archive.getinfo(name)
            if info.file_size != expected['size']:
                raise ValueError(f'Size mismatch: {name}')
            h = hashlib.sha256()
            with archive.open(name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
            if h.hexdigest() != expected['sha256']:
                raise ValueError(f'SHA256 mismatch: {name}')
        return manifest, archive.read('current_image_index.json'), archive.read('w53_EmbryoInfo210122.rtf')


def inspect_index(snapshot_bytes: bytes):
    data = json.loads(snapshot_bytes)
    hits = data['hits']['hits']
    declared = data['hits']['total']['value']
    if declared != len(hits):
        raise ValueError('Archived index query pagination incomplete')
    paths = []
    for hit in hits:
        attributes = hit['_source']['additional_metadata']
        pattern = [entry['value']['file_pattern'] for entry in attributes if entry['name'] == 'file_pattern']
        if len(pattern) != 1:
            raise ValueError('Ambiguous image file_pattern')
        paths.append(pattern[0])
    if len(set(paths)) != len(paths):
        raise ValueError('Duplicate source file paths')
    target_paths = [p for p in paths if f'/{TARGET_EMBRYO}/' in p]
    needed = [f'DataRepository/TwoPhoton/wildtype/{TARGET_EMBRYO}/MARKERS/F_{n:03d}.tif'
              for n in REQUIRED_MASKS]
    if not target_paths:
        raise ValueError('Missing the target WT source embryo')
    return {'hits': declared, 'unique_paths': len(paths),
            'target_embryo': TARGET_EMBRYO, 'target_paths': target_paths,
            'target_hits': len(target_paths),
            'required_mask_paths': needed,
            'required_masks_indexed': {p.rsplit('/', 1)[1]: p in paths for p in needed},
            'snapshot_not_live_index': True}


def parse_acquisition_note(rtf_bytes: bytes):
    # These exact ASCII phrases occur in the 699-byte original RTF.
    text = rtf_bytes.decode('latin1')
    spatial = re.search(r'Pixel size\s+(\d+(?:\.\d+)?)\s+um', text)
    cadence = re.search(r'(\d+)\s+seconds per frame', text)
    t0 = re.search(r'#2\s+t0\s*=\s*frame\s+(\d+)', text)
    if not (spatial and cadence and t0):
        raise ValueError('Expected deposition calibration facts not present')
    return {'pixels_um_reported': float(spatial.group(1)),
            'seconds_per_frame': int(cadence.group(1)),
            'embryo_2_t0_frame': int(t0.group(1)),
            'rounding_warning': '0.49 is a reported source-note value, not high-precision calibration'}


def conditional_scale(source_um, replay_um):
    if source_um <= 0 or replay_um <= 0:
        raise ValueError('Nonpositive spatial scales')
    factor = source_um / replay_um
    return {'source_note_um_per_pixel': source_um,
            'replay_demo_um_per_pixel': replay_um,
            'conditional_linear_factor': factor,
            'relative_change_percent': 100 * (factor - 1),
            'sign_preserved_if_only_postPIV_scale_changes': factor > 0}


def shift_envelope(rows):
    result = []
    for row in rows:
        ds = [row[p] for p in ('offset_minus1', 'central', 'offset_plus1')]
        result.append({'orientation': row['orientation'], 'quadrant': row['quadrant'],
                       'min': min(ds), 'max': max(ds),
                       'spans_zero': min(ds) < 0 < max(ds),
                       'central_to_plus1_change': row['offset_plus1'] - row['central'],
                       'mask_effect_at_plus1': row['mask_effect_at_plus1']})
    return result


def audit(w53_source_zip, w53_receipt_bytes, w54_archive):
    manifest, index_bytes, note_bytes = integrity_check(w53_source_zip)
    index = inspect_index(index_bytes)
    note = parse_acquisition_note(note_bytes)
    w53 = json.loads(w53_receipt_bytes)
    w58 = audit_time_receipts(w53_receipt_bytes, w54_archive)
    assumptions = w53['assumptions']
    if assumptions['t0_frame_zero_based'] != note['embryo_2_t0_frame']:
        raise ValueError('Source/replay t0 mismatch')
    if assumptions['minutes_per_frame'] * 60 != note['seconds_per_frame']:
        raise ValueError('Source/replay frame duration mismatch')
    scale = conditional_scale(note['pixels_um_reported'], assumptions['micrometers_per_pixel'])
    envelope = shift_envelope(w58['rows'])
    if len(envelope) != 4 or not all(row['spans_zero'] for row in envelope):
        raise ValueError('Unexpected source trajectory envelope')
    return {'source_sha256': hashlib.sha256(w53_source_zip).hexdigest(),
            'source_manifest_files_verified': len(manifest['files']),
            'archive_index': index, 'deposition_note': note,
            'scale_comparison': scale, 'frame_shift_envelope': envelope,
            'shifted_mask_max_abs_delta_um_per_min': w58['max_absolute_mask_effect_at_plus1'],
            'limitation': 'One candidate WT embryo; unknown Figure 2E membership, exact production settings and biological-time registration; archived index is not a live query. No publication-level or AI causal claim.'}


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('Usage: p77_w59_source_anchor_audit.py W53-inputs.zip W53-receipt.json W54-evidence.zip')
    print(json.dumps(audit(*(Path(p).read_bytes() for p in sys.argv[1:])), ensure_ascii=False, indent=2))
