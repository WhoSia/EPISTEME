"""W62: derive *candidate*, not manuscript-certified, Figure 2E cta frame pairs.

The three small RTF files are the original S-BIAD602 dated acquisition notes.
The t0 notation is not sufficient to verify exact biological Tcell registration.
No TIFF image is downloaded or analyzed by this program.

Usage: python analysis/p77_w62_cta_candidate_frame_map.py EmbryoInfo210929.rtf EmbryoInfo211005.rtf EmbryoInfo211007.rtf
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SOURCE_RECEIPTS = {
    "210929": ("f276dbc5caa9b42de87ac98310d9f5b0fa3fec275b4800341c8005df8c2915f9", 697),
    "211005": ("378f5fe961a668b28d443e44944899c9cfd81ebbf09b6aa250229ff6b537cbc2", 660),
    "211007": ("7af88904395e0d381ab797431b7a99c9b9444a733c64c8c39473151019f39522", 682),
}
CANDIDATES = {
    "embryo1_210929_1_1": ("210929", "1_1"),
    "embryo2_210929_1_3": ("210929", "1_3"),
    "embryo3_211005_1_2": ("211005", "1_2"),
    "embryo4_211007_1_1": ("211007", "1_1"),
    "embryo5_211007_1_2": ("211007", "1_2"),
}


def parse_note(text):
    if not re.search(r"30\s+seconds per frame", text):
        raise ValueError("Expected 30 second acquisition cadence")
    if not re.search(r"Pixel size\s+0\.49\s+um", text):
        raise ValueError("Unexpected documented spatial calibration")
    t0s = re.findall(r"#(\d+_\d+)\s+t0\s*=\s*(\d+)", text)
    if len(set(k for k, _ in t0s)) != len(t0s):
        raise ValueError("Repeated t0 label")
    return {key: int(value) for key, value in t0s}


def frame_pair(t0, minutes, cadence_seconds=30):
    if minutes * 60 % cadence_seconds:
        raise ValueError("Time not aligned to acquisition cadence")
    i = t0 + minutes * 60 // cadence_seconds
    return [i, i + 1]


def audit(paths):
    parsed = {}
    for path in paths:
        p = Path(path)
        date_match = re.search(r"EmbryoInfo(\d{6})\.rtf$", p.name)
        if not date_match:
            raise ValueError("Unidentified RTF acquisition-date name")
        date = date_match.group(1)
        if date not in SOURCE_RECEIPTS or date in parsed:
            raise ValueError("Unknown or repeated date")
        raw = p.read_bytes()
        digest, size = SOURCE_RECEIPTS[date]
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("RTF raw bytes do not match held Drive evidence")
        parsed[date] = parse_note(raw.decode("latin1"))
    if set(parsed) != set(SOURCE_RECEIPTS):
        raise ValueError("All three cta date notes required")
    rows = []
    for embryo, (date, suffix) in CANDIDATES.items():
        if suffix not in parsed[date]:
            raise ValueError("Missing candidate t0: " + embryo)
        t0 = parsed[date][suffix]
        rows.append({"candidate_embryo": embryo, "note_date": date,
                     "note_suffix": suffix, "recorded_t0": t0,
                     "nine_minute_conditional_frames": frame_pair(t0, 9),
                     "seventeen_minute_conditional_frames": frame_pair(t0, 17)})
    extra_annotations = {date: {k: v for k, v in note.items()
                                if (date, k) not in set(CANDIDATES.values())}
                         for date, note in parsed.items()}
    return {
        "candidate_count": len(rows),
        "cadence_seconds": 30,
        "pixel_size_um_per_pixel_reported": 0.49,
        "conditional_indexing_assumption": "Source note t0 is the zero-based index of the paper's actual biological Tcell=0; NOT verified.",
        "original_rtf_sha256": {d: SOURCE_RECEIPTS[d][0] for d in parsed},
        "candidate_rows": rows,
        "other_note_labels_not_in_five_candidates": extra_annotations,
        "not_verified": ["Figure 2E inclusion", "marker image frame existence",
                         "exact author t0 registration", "PIV masks and parameters",
                         "published statistical data"],
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: p77_w62_cta_candidate_frame_map.py 210929.rtf 211005.rtf 211007.rtf")
    print(json.dumps(audit(sys.argv[1:]), ensure_ascii=False, indent=2))
