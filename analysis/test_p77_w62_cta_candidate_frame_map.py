"""W62 cta deposit-frame candidate unit tests (not a biological time proof)."""
import unittest
from p77_w62_cta_candidate_frame_map import parse_note, frame_pair, CANDIDATES


class CtaTests(unittest.TestCase):
    NOTE = r"Pixel size 0.49 um\par 30 seconds per frame\par #1_1 t0 = 17\par #1_2 t0 = 7"

    def test_note_parses_two_embryos(self):
        self.assertEqual(parse_note(self.NOTE), {"1_1": 17, "1_2": 7})

    def test_frame_pairs(self):
        self.assertEqual(frame_pair(23, 9), [41, 42])
        self.assertEqual(frame_pair(23, 17), [57, 58])
        self.assertEqual(frame_pair(7, 9), [25, 26])

    def test_full_candidate_keys_are_five(self):
        self.assertEqual(len(CANDIDATES), 5)
        self.assertEqual(len(set(CANDIDATES.values())), 5)

    def test_no_cadence_rejected(self):
        with self.assertRaisesRegex(ValueError, "cadence"):
            parse_note("Pixel size 0.49 um #1_1 t0 = 17")

    def test_repeated_time_label_rejected(self):
        with self.assertRaisesRegex(ValueError, "Repeated"):
            parse_note(self.NOTE + r"\par #1_1 t0 = 21")

    def test_off_grid_time_rejected(self):
        with self.assertRaisesRegex(ValueError, "aligned"):
            frame_pair(23, 9, 40)


if __name__ == "__main__":
    unittest.main()
