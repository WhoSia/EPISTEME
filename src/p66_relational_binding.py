from __future__ import annotations
import json,random
from collections import OrderedDict
from p63_structural_location import packet as p63_packet,ALIASES,SKIN_WORDS
from p48_seed_fingerprints import panel_cells
from p44_field import vertex_set
MODEL='gptoss120'
DRAWS=tuple(range(1,17))
SPECS=OrderedDict()
for b,bc in [('target_linked','B'),('decoy_linked','D')]:
 for l,lc in [('history_externalized','H'),('terminal_embedded','T')]:
  for s in (1,2,3): SPECS[bc+lc+str(s)]={'binding':b,'location':l,'skin':s}
TASKS=tuple(SPECS)
def packet(task,label,semantic,alias):
 sp=SPECS[task];loc=sp['location'];s=sp['skin']
 source=('RH' if loc=='history_externalized' else 'RT')+str(s)
 p=p63_packet(source,label,semantic,alias)
 p['archive_id']='p66-'+task+'-'+label+'-'+semantic+'-'+alias
 p['frame_note']='Only an explicitly bound target-to-evidence link is admissible for a falsifying challenge. An unlinked evidence code cannot justify an experiment.'
 target_slot,decoy_slot=SKIN_WORDS[s][0],SKIN_WORDS[s][1]
 p['binding_register']={'target_link':target_slot if sp['binding']=='target_linked' else decoy_slot,'decoy_link':decoy_slot if sp['binding']=='target_linked' else target_slot}
 p['instructions']='Use only the evidence_code in the panel entry whose slot equals binding_register.target_link. Propose one justified experiment to falsify the claim, or answer NONE if that target-linked code is UNINFORMATIVE or CHALLENGE_INVARIANT. Evidence bound to decoy_link must not be used for target inference.'
 return p
def expected_valid(task,semantic):
 return semantic=='valid' and SPECS[task]['binding']=='target_linked'
def score(o,task,semantic):
 challenge=o.get('challenge');intervention=o.get('intervention');direction=o.get('predicted_direction')
 none=challenge is None or str(challenge).strip().upper()=='NONE'
 if expected_valid(task,semantic):
  return not none and intervention=='u1' and direction=='different'
 return none
def self_test():
 assert len(TASKS)==12 and len(panel_cells())==64
 for task in TASKS:
  for sem in ('valid','null'):
   for label in ('I','R','T','R_T'):
    for alias in ('A','D'):
     p=packet(task,label,sem,alias)
     assert len(p['history_panel'])==len(p['terminal_panel'])==2
     assert len(p['binding_register'])==2
     assert set(p['binding_register'].values())==set(SKIN_WORDS[SPECS[task]['skin']][:2])
 print('P66_PRECHECK_PASS 12 tasks, 64 cells each')
if __name__=='__main__':self_test()
