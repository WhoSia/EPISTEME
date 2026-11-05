"""EPISTEME P77 W23 — independent custody/grain audit of public CRI ZIP.

READ-ONLY. No ISSP respondent-level data are re-published and no R models run.
Run: python analysis/p77_w23_cri_archive_replay.py CRI-master.zip
"""
from collections import Counter
from hashlib import sha256
import csv
from io import TextIOWrapper
from pathlib import Path
import sys
from zipfile import ZipFile

EXPECTED_ZIP_SHA256 = "64756bfe62b25cdd7dbea57d2b063cb0f564225751d1f0251b4879f426894098"

def rows_for(z, name, encoding):
    with z.open("CRI-master/" + name) as f:
        return list(csv.DictReader(TextIOWrapper(f, encoding=encoding, newline="")))

def assert_equal(name, actual, expected):
    if actual != expected:
        raise AssertionError(f"{name}: observed={actual!r}, expected={expected!r}")
    print(f"PASS {name}: {actual}")

def main(archive):
    path = Path(archive)
    digest = sha256(path.read_bytes()).hexdigest()
    assert_equal("ZIP SHA256", digest, EXPECTED_ZIP_SHA256)
    with ZipFile(path) as z:
        assert_equal("ZIP CRC test", z.testzip(), None)
        files = [f for f in z.infolist() if not f.is_dir()]
        assert_equal("file count", len(files), 439)
        assert_equal("original extracted bytes", sum(f.file_size for f in files), 859647748)
        model = rows_for(z, "data/cri.csv", "cp1252")
        team = rows_for(z, "data/cri_team.csv", "utf-8-sig")
        assert_equal("original model-table rows", len(model), 1309)
        assert_equal("original model columns", len(model[0]), 479)
        baseline = [r for r in model if r["u_teamid"] == "0"]
        submitted = [r for r in model if r["u_teamid"] != "0"]
        assert_equal("historical baseline Team0 rows", len(baseline), 48)
        assert_equal("research cohort submitted models", len(submitted), 1261)
        assert_equal("research cohort distinct submitted team IDs", len({r["u_teamid"] for r in submitted}), 72)
        estimates = [r for r in submitted if r["AME"].strip().upper() not in ("NA", "")]
        assert_equal("nonmissing AME models", len(estimates), 1253)
        ci = [r for r in estimates if all(r[k].strip().upper() not in ("NA","") for k in ("lower","upper"))]
        assert_equal("AME models with both confidence bounds", len(ci), 1252)
        missing_ame = [r for r in submitted if r["AME"].strip().upper() in ("NA", "")]
        assert_equal("nonconverged/missing-AME rows (no mechanism implied)", len(missing_ame), 8)
        assert_equal("missing-AME team IDs", {r["u_teamid"] for r in missing_ame}, {"1"})
        ame_no_ci = [r["id"] for r in estimates if any(r[k].strip().upper() in ("NA", "") for k in ("lower", "upper"))]
        assert_equal("nonmissing AME with missing CI", ame_no_ci, ["t75m14"])
        assert_equal("team-summary rows", len(team), 89)
        assert_equal("team-summary columns", len(team[0]), 464)
        assert_equal("judgment categories", dict(Counter(r["Hresult"] for r in team)),
                     {"No test":11, "Reject":55, "Support":23})
    print("SOURCE STRUCTURE REPLAY PASS; NO R STATISTICAL RECOMPUTATION")
    print("NO AI ADAPTER TREATMENT, NO COMMUNITY STANDARD ADOPTION, NO NOVELTY CERTIFIED")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python p77_w23_cri_archive_replay.py CRI-master.zip")
    main(sys.argv[1])
