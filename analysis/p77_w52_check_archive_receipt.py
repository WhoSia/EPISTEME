"""Check W52 frame-inventory and OME-Zarr time-scale findings.

Input: the public-evidence receipt archived with the W52 research note.
This checks directory listings and metadata, without loading image pixels.
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path


def audit(receipt):
    embryos = receipt["embryos"]
    if len({row["embryo"] for row in embryos}) != len(embryos):
        raise ValueError("Duplicate embryo directory")
    conditions = Counter(row["condition"] for row in embryos)
    for row in embryos:
        markers = row["marker"]
        if not markers or markers != list(range(markers[0], markers[-1] + 1)):
            raise ValueError(f"Missing or nonconsecutive marker frame: {row['embryo']}")
    known = [row for row in embryos if row["t0"] is not None]
    covered = 0
    membrane_covered = 0
    for row in known:
        # Assume the acquisition note's t0 gives T_cell=0 with 30 s cadence.
        required = {row["t0"] + offset for offset in (18, 19, 34, 35)}
        covered += required <= set(row["marker"])
        if row["membrane"] is not None:
            membrane_covered += required <= set(row["membrane"])

    images = receipt["api"]["images"]
    if receipt["api"]["image_total"] != {"value": len(images), "relation": "eq"}:
        raise ValueError("Image response is not a complete exact hit count")
    image_roles = Counter(tuple(row["pattern"].split("/")[1:3]) for row in images)
    scales = []
    for sidecar in receipt["sidecars"]:
        multiscale = sidecar["metadata"]["multiscales"][0]
        axes = [axis["name"] for axis in multiscale["axes"]]
        base = next(dataset for dataset in multiscale["datasets"] if dataset["path"] == "0")
        transforms = base["coordinateTransformations"]
        scale = next(transform["scale"] for transform in transforms
                     if transform["type"] == "scale")[axes.index("t")]
        try:
            finite_seconds = isinstance(scale, (float, int)) and math.isfinite(scale) and scale > 0
        except TypeError:
            finite_seconds = False
        scales.append({"stored_t_scale": scale, "finite_positive_number": finite_seconds})
    return {
        "embryos": dict(conditions),
        "explicit_t0": len(known),
        "both_timepoints_and_next_frame_in_markers": covered,
        "both_timepoints_and_next_frame_in_numbered_membrane": membrane_covered,
        "unresolved_t0": [row["embryo"] for row in embryos if row["t0"] is None],
        "indexed_images": {"/".join(key): value for key, value in sorted(image_roles.items())},
        "sidecars": scales,
    }


if __name__ == "__main__":
    print(json.dumps(audit(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))), indent=2))
