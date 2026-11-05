"""P77 W38: source-labelled scientific standard decisions and causal evidence gate.

Evidence census of *published source claims*, not measured institutional panel.
Not a longitudinal adoption count, randomized trial or new epistemic theorem.
No artificial observations of adoption or test availability are generated.
"""
from dataclasses import dataclass
from typing import Literal

Status = Literal['documented', 'planned', 'not_reported']

@dataclass(frozen=True)
class Evidence:
    label: str
    source_url: str
    date: str
    archive_format_recorded: bool
    access_format_recorded: bool
    practical_converter_reported: bool
    practice_status: Status
    assigned_ai_adapter: bool
    prospective_standard_choice_outcome: bool
    independently_adjudicated_hypothesis_test: bool

    def causal_chain_identified(self) -> bool:
        # Necessary presence check only, never sufficient statistical identification.
        return (self.assigned_ai_adapter
                and self.prospective_standard_choice_outcome
                and self.independently_adjudicated_hypothesis_test)

OME = 'https://doi.org/10.1007/s00418-023-02209-1'
RISE = 'https://data.usbr.gov/catalog/8002/item/128581'
DATA_DESC = 'https://doi.org/10.1016/j.patter.2026.101493'
PARADATA = 'https://doi.org/10.1108/JD-10-2025-0324'

EVIDENCE = (
    Evidence('RISE: netCDF prioritized', RISE, '2023', True, False, False,
             'documented', False, False, False),
    Evidence('OME: IDR/BIA transformed access copies', OME, '2023', True, True,
             True, 'documented', False, False, False),
    Evidence('OME: Sanger ingestion default', OME, '2023', False, True,
             True, 'documented', False, False, False),
    Evidence('OME: SSBD selected conversions', OME, '2023', False, True,
             True, 'documented', False, False, False),
    Evidence('OME: planned dynamic archive-preserving access service', OME,
             '2023', True, True, True, 'planned', False, False, False),
    Evidence('DataDesc/ioProc: two energy-science workflows', DATA_DESC, '2026',
             False, True, True, 'documented', False, False, False),
    Evidence('Paradata: nine documentation standards compared', PARADATA,
             '2026', False, True, False, 'documented', False, False, False),
)

def audit(items=EVIDENCE):
    assert len(items) == 7
    assert len({i.label for i in items}) == len(items)
    assert all(i.source_url.startswith('https://') for i in items)
    assert all(i.practice_status in ('documented','planned','not_reported') for i in items)
    assert sum(i.practice_status == 'planned' for i in items) == 1
    assert sum(i.archive_format_recorded and i.access_format_recorded for i in items) == 2
    assert not any(i.causal_chain_identified() for i in items)
    assert not any(i.assigned_ai_adapter for i in items)
    print('PASS: 7 source-labelled case descriptions audited (not 7 lab observations)')
    print('PASS: planned on-demand conversion explicitly segregated from documented use')
    print('PASS: archive format and access format not treated as identical variables')
    print('PASS: no reported AI assignment or independently scored H0/H1 feasible-test change')
    print('NO-GO: cannot infer Z->A->T causal effect from these original publications')

if __name__ == '__main__':
    audit()
