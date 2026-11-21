"""W64 released GEO title crosscheck: independent synthetic tests."""
import unittest
from p77_w64_geo_title_crosscheck import count_title_markers, text_title


class TitleCrosscheckTests(unittest.TestCase):
    def test_ovarian_markers_only(self):
        x = count_title_markers([{"title": "Ovarian Cancer: study A"},
                                 {"title": "ovarian cancer study B"}])
        self.assertEqual(x["rows"], 2)
        self.assertEqual(x["titles_containing_ovarian_cancer"], 2)
        self.assertEqual(x["titles_containing_liver_cancer"], 0)

    def test_liver_title_filter(self):
        x = count_title_markers([{"title": "Liver cancer study"}])
        self.assertEqual(x["titles_containing_liver_cancer"], 1)

    def test_lung_title(self):
        x = count_title_markers([{"title": ["Lung cancer", "tissue atlas"]}])
        self.assertEqual(x["titles_containing_lung_cancer"], 1)

    def test_malformed_title_rejected(self):
        with self.assertRaisesRegex(ValueError, "title type"):
            text_title({"title": 10})

    def test_record_shape_rejected(self):
        with self.assertRaisesRegex(ValueError, "dictionaries"):
            count_title_markers([{"title":"lung"}, []])


if __name__ == "__main__":
    unittest.main()
