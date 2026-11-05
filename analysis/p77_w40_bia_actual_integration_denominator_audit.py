"""EPISTEME P77 W40: validate author-reported institutional integration counts.

Zulueta-Coarasa et al. (2026), Nucleic Acids Research gkag1108,
https://doi.org/10.1093/nar/gkag1108 (published 2026-11-05).
Institutional counts as of 2026-06-30, drawn from published author report,
NOT independently retrieved raw accession history or format migration panel.
"""
from dataclasses import dataclass

AS_OF = "2026-06-30"

@dataclass(frozen=True)
class Institution:
    name: str
    accession_entries_total: int
    entries_ingested: int

    def coverage(self):
        assert 0 <= self.entries_ingested <= self.accession_entries_total
        return self.entries_ingested / self.accession_entries_total

COHORTS = (
    Institution("BIA/BioStudies", 1477, 1396),
    Institution("EMPIAR", 3019, 508),
)
CONVERTED_IMAGES_LOWER_BOUND = 25000  # Different grain from accession entries.
FUTURE_PLANS_NOT_OBSERVED = {
    "all_entries_indexed_target": "2026-12",
    "70pct_images_converted_target": "2027-03",
    "unified_deposition_target": "2027-mid",
}

def audit():
    a, b = COHORTS
    assert abs(a.coverage() - 1396/1477) < 1e-15
    assert abs(b.coverage() - 508/3019) < 1e-15
    assert CONVERTED_IMAGES_LOWER_BOUND == 25000
    for x in COHORTS:
        print(f"PASS source article as-of {AS_OF}: {x.name}: "
              f"{x.entries_ingested}/{x.accession_entries_total} entries "
              f"({100*x.coverage():.3f}%)")
    print(">25,000 images available via derived OME-Zarr; this is NOT 25,000 entries")
    print("Planned milestones NOT outcomes:", FUTURE_PLANS_NOT_OBSERVED)
    print("NO-GO: source reports no assigned AI translation vs deterministic control,"
          " no lab-specific standard transition panel and no adjudicated H0/H1 testability")

if __name__ == "__main__":
    audit()
