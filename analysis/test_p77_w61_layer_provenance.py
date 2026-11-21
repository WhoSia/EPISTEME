"""Synthetic regression checks for Sundaram W61 input/output provenance audit."""
import copy
import json
import unittest
from p77_w61_layer_provenance import analyze_payload, records, accession, CANCERS, MODELS


def fake_payloads():
    src = {c: [{'gse':f'GSE_{c}_{i}','gsm':[f'GSM_{c}_{i}']} for i in range(800)] for c in CANCERS}
    data={}
    for c,rs in src.items():
        data[f'Data/{c}_cancer_geo.json']=json.dumps(rs).encode()
    for c in CANCERS:
        for m in MODELS:
            source = src['lung'] if m == 'llama3' else src[c]
            out=[]
            for i,raw in enumerate(source):
                lung_llm = {'bioproject_accession':src['lung'][i]['gse']}
                if m=='gpt4' and c in ('liver','lung'):
                    llm=lung_llm
                else:
                    llm={'bioproject_accession':raw['gse']}
                cedar={'geo_accession':src['liver'][i]['gse']} if c=='liver' and m=='gpt4' else {'tissue':c}
                out.append({'BioSample':raw, 'LLM':llm, 'LLM+CEDAR':cedar})
            data[f'Data/{c}_cancer_{m}_geo_output.json']=json.dumps(out).encode()
    data['Data/annotated_800_geo_simple_lung.txt'] = b'lung\n'*800
    data['Data/annotated_800_geo_simple_ovary.txt'] = b'ovary\n'*800
    return data


class W61Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good=fake_payloads()

    def test_expected_positive_and_negative_controls(self):
        out=analyze_payload(self.good)
        self.assertEqual(out['gpt4_liver_split_layer']['llm_dict_identical_to_lung_gpt4'],800)
        self.assertEqual(out['gpt4_liver_split_layer']['liver_llm_bioproject_matches_liver'],0)
        self.assertEqual(out['gpt4_liver_split_layer']['liver_cedar_geo_accession_matches_liver'],800)
        self.assertEqual(out['llama3_biosample_equals_lung_by_cancer']['ovarian'],800)
        self.assertFalse(out['annotation_files']['geo_liver'])

    def test_all_nine_output_files_reported(self):
        self.assertEqual(len(analyze_payload(self.good)['original_to_output_alignment']),9)

    def test_distinct_originals_are_matched(self):
        out=analyze_payload(self.good)
        for r in out['original_to_output_alignment']:
            expected='lung' if r['model']=='llama3' else r['cancer']
            self.assertEqual(r['source_order_matches'][expected],800)

    def test_duplicate_original_rejected(self):
        bad=self.good.copy();rows=json.loads(bad['Data/liver_cancer_geo.json'])
        rows[1]=rows[0];bad['Data/liver_cancer_geo.json']=json.dumps(rows).encode()
        with self.assertRaisesRegex(ValueError,'original accession'):
            analyze_payload(bad)

    def test_overlapping_cancer_cohort_rejected(self):
        bad=self.good.copy();rows=json.loads(bad['Data/liver_cancer_geo.json'])
        other=json.loads(bad['Data/lung_cancer_geo.json']);rows[0]=other[0]
        bad['Data/liver_cancer_geo.json']=json.dumps(rows).encode()
        with self.assertRaisesRegex(ValueError,'cohort collision'):
            analyze_payload(bad)

    def test_model_output_duplicate_rejected(self):
        bad=self.good.copy();fname='Data/ovarian_cancer_medllama_geo_output.json'
        rows=json.loads(bad[fname]);rows[1]=rows[0];bad[fname]=json.dumps(rows).encode()
        with self.assertRaisesRegex(ValueError,'Repeated output source'):
            analyze_payload(bad)

    def test_gpt4_liver_cedar_wrong_source_rejected(self):
        bad=self.good.copy();name='Data/liver_cancer_gpt4_geo_output.json'
        rows=json.loads(bad[name]);rows[0]['LLM+CEDAR']['geo_accession']='GSEbad'
        bad[name]=json.dumps(rows).encode()
        with self.assertRaisesRegex(ValueError,'split-layer control'):
            analyze_payload(bad)

    def test_gpt4_liver_llm_replacement_rejected(self):
        bad=self.good.copy();name='Data/liver_cancer_gpt4_geo_output.json'
        rows=json.loads(bad[name]);rows[0]['LLM']['bioproject_accession']='GSEbad'
        bad[name]=json.dumps(rows).encode()
        with self.assertRaisesRegex(ValueError,'split-layer control'):
            analyze_payload(bad)

    def test_llama_source_repair_detected(self):
        bad=self.good.copy();name='Data/ovarian_cancer_llama3_geo_output.json'
        rows=json.loads(bad[name]);rows[0]['BioSample']={'gse':'GSE_ovarian_0','gsm':['GSM_ovarian_0']}
        bad[name]=json.dumps(rows).encode()
        with self.assertRaisesRegex(ValueError,'W60 Llama'):
            analyze_payload(bad)

    def test_concatenated_json_and_array(self):
        self.assertEqual(len(records(b'{"a":1}\n{"a":2}')),2)
        self.assertEqual(len(records(b'[{"a":1},{"a":2}]')),2)

    def test_reject_record_missing_accession(self):
        with self.assertRaisesRegex(ValueError,'Missing GSE'):
            accession({'gse':'GSE1','gsm':[]})


if __name__=='__main__': unittest.main()
