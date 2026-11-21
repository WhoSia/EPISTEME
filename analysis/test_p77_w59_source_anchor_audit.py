"""W59 bounded source-integrity and index-join negative controls."""
import hashlib
import io
import json
import unittest
from zipfile import ZipFile
from p77_w59_source_anchor_audit import (
    integrity_check, inspect_index, parse_acquisition_note,
    conditional_scale, shift_envelope,
)


def source_fixture(filename='test.txt', data=b'anchor'):
    parts = {filename: data, 'current_image_index.json': b'{}',
             'w53_EmbryoInfo210122.rtf': b''}
    manifest = {'files': {
        name: {'size': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
        for name, payload in parts.items()
    }}
    out = io.BytesIO()
    with ZipFile(out, 'w') as z:
        z.writestr('source_manifest.json', json.dumps(manifest))
        for name, payload in parts.items():
            z.writestr(name, payload)
    return out.getvalue()


def index_fixture(paths):
    hits = [{'_source': {'additional_metadata': [
        {'name': 'file_pattern', 'value': {'file_pattern': path}}
    ]}} for path in paths]
    return json.dumps({'hits': {'total': {'value': len(hits)}, 'hits': hits}}).encode()


class SourceAnchorTests(unittest.TestCase):
    def test_manifest_valid(self):
        manifest, *_ = integrity_check(source_fixture())
        self.assertEqual(len(manifest['files']), 3)

    def test_manifest_bad_hash(self):
        original = source_fixture()
        output = io.BytesIO()
        with ZipFile(io.BytesIO(original)) as old, ZipFile(output, 'w') as new:
            for name in old.namelist():
                data = old.read(name)
                if name == 'source_manifest.json':
                    manifest = json.loads(data)
                    manifest['files']['test.txt']['sha256'] = '0' * 64
                    data = json.dumps(manifest).encode()
                new.writestr(name, data)
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            integrity_check(output.getvalue())

    def test_manifest_reject_traversal(self):
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            integrity_check(source_fixture('../bad.txt'))

    def test_exact_index_coverage(self):
        root = 'DataRepository/TwoPhoton/wildtype/embryo1_210122_2/'
        x = inspect_index(index_fixture([root + 'x_MEM.tif', root + 'MARKERS/F_020.tif']))
        self.assertEqual(x['target_hits'], 2)
        self.assertFalse(any(x['required_masks_indexed'].values()))

    def test_reject_incomplete_index_snapshot(self):
        data = json.loads(index_fixture(['DataRepository/TwoPhoton/wildtype/embryo1_210122_2/x_MEM.tif']))
        data['hits']['total']['value'] = 2
        with self.assertRaisesRegex(ValueError, 'pagination'):
            inspect_index(json.dumps(data).encode())

    def test_reject_duplicate_index_path(self):
        path = 'DataRepository/TwoPhoton/wildtype/embryo1_210122_2/x_MEM.tif'
        with self.assertRaisesRegex(ValueError, 'Duplicate source'):
            inspect_index(index_fixture([path, path]))

    def test_deposit_note_values(self):
        note = parse_acquisition_note(b'Pixel size 0.49 um\\\n30 seconds per frame\\\n#2 t0 = frame 20\\\n')
        self.assertEqual(note['embryo_2_t0_frame'], 20)
        self.assertEqual(note['seconds_per_frame'], 30)
        self.assertEqual(note['pixels_um_reported'], .49)

    def test_scale_comparison_preserves_sign(self):
        data = conditional_scale(.49, .497)
        self.assertAlmostEqual(data['relative_change_percent'], -1.40845070422535)
        self.assertTrue(data['sign_preserved_if_only_postPIV_scale_changes'])

    def test_time_envelope_crosses_zero(self):
        out = shift_envelope([dict(orientation='a', quadrant='b', offset_minus1=.2,
                                   central=.1, offset_plus1=-.3, mask_effect_at_plus1=.001)])
        self.assertTrue(out[0]['spans_zero'])
        self.assertAlmostEqual(out[0]['central_to_plus1_change'], -.4)


if __name__ == '__main__':
    unittest.main()
