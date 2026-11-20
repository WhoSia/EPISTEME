"""Replay two WT membrane frame pairs with published PIV/geometry primitives.

Requires the modelTissueFlow checkout at 8e09f33 on PYTHONPATH and the
dependencies recorded with the W53 receipt. Inputs are the archived WT MEM
TIFF, numbered MARKERS TIFFs, and the downloaded full-resolution Zarr chunks.
Frame indices are zero-based and conditional on the deposited t0 annotation.
"""
import argparse
import hashlib
import json
import math
import platform
import re
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
from numcodecs import get_codec
from tifffile import TiffFile

from modelTissueFlow.modules import analysisModule as analysis
from modelTissueFlow.modules import inOutTools as geometry

FRAMES = {9: 38, 17: 54}
CHECKED_CHUNKS = (20, 37, 38, 39, 40, 53, 54, 55, 56)
T0 = 20
MINUTES_PER_FRAME = 0.5
MICROMETERS_PER_PIXEL = 0.497


def sha256(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def read_indexed_frames(directory, metadata):
    codec = get_codec(metadata["compressor"])
    shape = tuple(metadata["shape"][-2:])
    return {
        index: np.frombuffer(
            codec.decode((directory / f"zarr_{index:03}.raw").read_bytes()),
            dtype=np.dtype(metadata["dtype"]),
        ).reshape(shape)
        for index in CHECKED_CHUNKS
    }


def embryo_axes(directory, orientation):
    reference = str(directory / f"F_{T0:03}.tif")
    apical, _, _, _ = analysis.extract_different_markers(
        reference, 100, -1.0, 0.0, orientation,
    )
    _, principal_axes, _, _ = geometry.coordinate_frame_with_respect_to_polygon(apical)
    endpoint, center = principal_axes[0]
    vector = geometry.normalize(endpoint - center)
    return [(center + sign * 2048 * vector, center) for sign in (-1, 1)]


def project_velocity(directory, index, piv, orientations):
    results = []
    for orientation, axes in orientations.items():
        apical, basal, _, dimensions = analysis.extract_different_markers(
            str(directory / f"F_{index:03}.tif"), 100, -1.0, 0.0, orientation,
        )
        for side, axis in enumerate(axes):
            _, midline, outer, inner = geometry.midline_polygon_from_a_pair_of_ploygons(
                apical, basal, axis, equal_apical_basal_distance=False,
            )
            outer, inner, *_ = analysis.apical_basal_markers_and_masks_with_respect_to_midline(
                midline, apical, basal, outer, inner, dimensions, [10, 16],
            )
            outer_dist, outer_dir = geometry.nearest_distance_and_direction_to_one_polygon_from_another_polygon(
                midline, outer, direction="outer",
            )
            inner_dist, inner_dir = geometry.nearest_distance_and_direction_to_one_polygon_from_another_polygon(
                midline, inner, direction="inner",
            )
            sub_apical = midline - 0.75 * np.asarray(outer_dist)[:, None] * outer_dir
            sub_basal = midline + 0.75 * np.asarray(inner_dist)[:, None] * inner_dir
            tangent, _, _ = analysis.split_PIV_in_components(
                *piv, [sub_apical, midline, sub_basal], 20,
            )
            for _ in range(2):
                tangent = np.asarray(geometry.sliding_window_average_data(tangent, 1))
            arc, arc_max = geometry.arc_length_along_polygon(midline)
            velocity = float(geometry.area_under_curve(
                arc / arc_max, tangent * MICROMETERS_PER_PIXEL, closed=False,
            ))
            if not math.isfinite(velocity):
                raise ValueError(f"Non-finite projected velocity at frame {index}")
            next_node = np.roll(midline, -1, axis=0)
            image_clockwise = np.sum(
                midline[:, 0] * next_node[:, 1] - midline[:, 1] * next_node[:, 0]
            ) > 0
            quadrant = geometry.point_at_which_quandrant(
                np.array([axis[0][0] - axis[1][0], axis[1][1] - axis[0][1]]) + 1e-3
            )
            results.append({
                "orientation_parameter": orientation,
                "reference_axis_side": side,
                "reference_axis_quadrant": quadrant,
                "image_clockwise": bool(image_clockwise),
                "signed_um_per_min": velocity,
                "clockwise_positive_um_per_min": velocity if image_clockwise else -velocity,
                "midline_nodes": len(midline),
            })
    return results


def compare_routes(directory):
    source = directory / "wt_mem.tif"
    indexed = read_indexed_frames(directory, json.loads((directory / "wt_zarray.json").read_text()))
    orientations = {
        key: embryo_axes(directory, key) for key in ("D-cw", "D-ccw")
    }
    projections = []
    start_time = time.perf_counter()
    with TiffFile(source) as stack:
        acquisition = stack.imagej_metadata
        structured = acquisition["finterval"]
        if not math.isinf(structured):
            raise ValueError(f"Expected the observed nonfinite TIFF interval, got {structured}")
        attrs = json.loads((directory / "current_wt_attrs.json").read_text())
        scale = attrs["multiscales"][0]["datasets"][0]["coordinateTransformations"][0]["scale"][0]
        equality = {
            i: int(np.count_nonzero(indexed[i] != stack.pages[i].asarray()))
            for i in CHECKED_CHUNKS
        }
        if any(equality.values()):
            raise ValueError(f"TIFF and Zarr pixel mismatch at observed frames: {equality}")
        for minutes, index in FRAMES.items():
            if index != T0 + minutes / MINUTES_PER_FRAME:
                raise ValueError(f"Time calibration mismatch at {minutes} min")
            raw = [stack.pages[i].asarray() for i in (index, index + 1)]
            zarr = [indexed[i] for i in (index, index + 1)]
            source_piv = analysis.calculate_PIV(*raw, 20, 0, MINUTES_PER_FRAME, 25, "peak2peak", 3.0)
            index_piv = analysis.calculate_PIV(*zarr, 20, 0, MINUTES_PER_FRAME, 25, "peak2peak", 3.0)
            piv_equal = all(np.array_equal(a, b, equal_nan=True) for a, b in zip(source_piv, index_piv))
            if not piv_equal:
                raise ValueError(f"Calculated PIV arrays differ at {minutes} min")
            measured = project_velocity(directory, index, source_piv[:4], orientations)
            replayed = project_velocity(directory, index, index_piv[:4], orientations)
            if replayed != measured:
                raise ValueError(f"Tangential projections differ at {minutes} min")
            projections.append({
                "minutes": minutes,
                "frames": [index, index + 1],
                "vectors_grid_shape": source_piv[2].shape,
                "piv_arrays_equal": piv_equal,
                "source_and_index_projections_equal": replayed == measured,
                "projections": measured,
            })
        receipt = {
            "scope": "single-embryo diagnostic with shared deposited masks and repaired 30 s calibration",
            "assumptions": {
                "t0_frame_zero_based": T0,
                "minutes_per_frame": MINUTES_PER_FRAME,
                "micrometers_per_pixel": MICROMETERS_PER_PIXEL,
                "spatial_scale_source": "authors' demo setting, not calibrated anew",
                "spatial_smoothing": "two author window_SIZE=1 passes",
                "temporal_smoothing": "omitted for the two standalone forward pairs",
                "orientation": "both code orientations and both ends of reference major axis",
                "openpiv_compatibility": "validation.py imports Python warnings instead of numpy.warnings",
                "author_compatibility": "ragged myosin-mask arrays explicitly use object dtype; velocity uses only the returned boundary points",
            },
            "source_hashes": {
                name: sha256(directory / name)
                for name in ("wt_mem.tif", "F_020.tif", "F_038.tif", "F_054.tif")
            },
            "shape": stack.series[0].shape,
            "raw_tiff_structured_interval": str(structured),
            "embedded_acquisition_period": re.findall(r"Period [^\n)]+", acquisition["Info"])[:2],
            "ome_zarr_time_scale_seconds": scale,
            "tiff_vs_zarr_pixel_mismatches": equality,
            "measurements": projections,
        }
    receipt["elapsed_seconds"] = round(time.perf_counter() - start_time, 3)
    receipt["environment"] = {
        "python": platform.python_version(),
        **{package: version(package) for package in (
            "numpy", "scipy", "OpenPIV", "opencv-python-headless",
            "scikit-image", "shapely", "tifffile", "numcodecs",
        )},
    }
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_directory", type=Path)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    receipt = compare_routes(args.input_directory)
    args.receipt.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
