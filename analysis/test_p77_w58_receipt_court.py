"""Small mutation tests of receipt integrity; no private source artifacts needed."""
import copy
import hashlib
import io
import json
import unittest
import zipfile
from p77_w58_receipt_court import analyze, MEMBER


def fixture():
    keys = [('D-cw','Q-2'),('D-cw','Q-4'),('D-ccw','Q-2'),('D-ccw','Q-4')]
    def proj(key, value):
        return {'orientation_parameter':key[0], 'reference_axis_quadrant':key[1],
                'clockwise_positive_um_per_min':value}
    w53 = {'measurements': [{'minutes':t,'frames':[s,s+1], 'projections': [proj(k,float(i+shift)) for i,k in enumerate(keys)]}
                            for t,s,shift in [(9,38,0),(17,54,1)]]}
    original = json.dumps(w53).encode()
    d={}
    for s,shift in ((38,0),(54,1)):
        d[str(s)]=[proj(k,float(i+shift)) for i,k in enumerate(keys)]
    rows=[]; fixed=[]
    for k in keys:
        for policy,value in [('pair_offset_minus1',2),('pair_original',1),('pair_offset_plus1',-1),('centered_moving_average_halfwidth1',2/3)]:
            rows.append({'orientation':k[0], 'quadrant':k[1], 'reduction':policy,
                         '9_min_um_per_min':0,'17_min_um_per_min':value,'difference_um_per_min':value})
        fixed.append({'orientation':k[0], 'quadrant':k[1], 'early':0,'late':-1,'difference':-1})
    m={'source_receipt_sha256':hashlib.sha256(original).hexdigest(),
       'input_sha256':{'F_037.tif':hashlib.sha256(b'first').hexdigest(),
                       'F_053.tif':hashlib.sha256(b'second').hexdigest()},
       'w53_central_projections_exact':True,
       'original_projection_rows':d,'results':rows,
       'held_contour_control':{'central_replay_equal':True,'shifted_rows':fixed}}
    def pack(document, corrupt_mask=False):
        out=io.BytesIO()
        with zipfile.ZipFile(out,'w') as z:
            z.writestr(MEMBER,json.dumps(document))
            z.writestr('w54data/F_037.tif', b'wrong' if corrupt_mask else b'first')
            z.writestr('w54data/F_053.tif',b'second')
        return out.getvalue()
    return original,m,pack


class ReceiptTests(unittest.TestCase):
    def test_valid_fixture(self):
        source,doc,pack=fixture(); data=analyze(source,pack(doc))
        self.assertEqual(data['sign_counts']['central'],4)
        self.assertEqual(data['sign_counts']['offset_plus1'],0)
        self.assertEqual(data['max_absolute_mask_effect_at_plus1'],0)

    def test_rejects_source_mutation(self):
        source,doc,pack=fixture()
        with self.assertRaisesRegex(ValueError,'not descended'):
            analyze(source+b'\n',pack(doc))

    def test_rejects_mask_byte_mutation(self):
        source,doc,pack=fixture()
        with self.assertRaisesRegex(ValueError,'mask hash mismatch'):
            analyze(source,pack(doc,corrupt_mask=True))

    def test_rejects_misaligned_time_average(self):
        source,doc,pack=fixture()
        bad=copy.deepcopy(doc); bad['results'][-1]['difference_um_per_min']=0.7
        bad['results'][-1]['17_min_um_per_min']=0.7
        with self.assertRaisesRegex(ValueError,'temporal average'):
            analyze(source,pack(bad))

    def test_rejects_central_revision(self):
        source,doc,pack=fixture()
        bad=copy.deepcopy(doc);bad['original_projection_rows']['38'][0]['clockwise_positive_um_per_min']=100
        with self.assertRaisesRegex(ValueError,'W53/W54'):
            analyze(source,pack(bad))


if __name__=='__main__':
    unittest.main()
