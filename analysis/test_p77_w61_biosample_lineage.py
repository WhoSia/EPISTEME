import unittest
from p77_w61_biosample_lineage import compare

class LineageTests(unittest.TestCase):
    def test_accession_removed_and_duplicates_ambiguous(self):
        ref = [{'BioSample': {'biosample_accession':'A','x':1}}, {'BioSample': {'biosample_accession':'B','x':1}}, {'BioSample': {'biosample_accession':'C','x':2}}]
        out = [{'BioSample': {'x':1}}, {'BioSample': {'x':1}}, {'BioSample': {'x':2}}]
        r = compare(ref, out)
        self.assertEqual((r['position_matches'], r['ambiguous_ref_join_rows'], r['unique_ref_join_rows']), (3,2,1))
    def test_reordering_and_missing_are_visible(self):
        ref = [{'BioSample': {'x':1}}, {'BioSample': {'x':2}}]
        rows = [{'BioSample': {'x':2}}, {'BioSample': {'x':3}}]
        r=compare(ref, rows)
        self.assertEqual((r['position_matches'],r['multiset_overlap'],r['unmatched_ref_rows']), (0,1,1))
    def test_invalid_source_rejected(self):
        with self.assertRaises(ValueError): compare([{'BioSample':[]}], [])

if __name__ == '__main__': unittest.main()

