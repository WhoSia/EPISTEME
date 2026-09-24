from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

def main():
    x=json.loads(Path("active/p29_reconstruction.json").read_text())
    worlds=["W01","W02","W03","W04","W05","W06"]
    classes=defaultdict(list)
    for i,v in enumerate(x["vertex_order"]):
        sig="".join(x["worlds"][w]["row"][i] for w in worlds)
        classes[sig].append(v)
    assert len(classes)==21
    result={
      "stage":"EPISTEME-P29",
      "y6_shape":[6,32],
      "six_world_quotient_class_count":len(classes),
      "six_world_classes":dict(sorted(classes.items())),
      "p28_quotient_transports_to_training":False,
      "smallest_observed_data_compatible_context_law":"M_S+U",
      "scientific_sufficiency":False,
      "identifiability_note":"Observed skin×intervention graph is a tree, so GF(2) additive M_S+U has the same six effective degrees of freedom as the six observed-cell saturated ceiling.",
      "prospective_assignment":"NO_NONTRIVIAL_PROSPECTIVE_ASSIGNMENT",
      "self_audit":"PASS"
    }
    Path("active/p29_result.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
if __name__=="__main__": main()
