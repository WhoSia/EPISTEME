# W53 WT Pair Replay — Runtime and Inputs

- [Pinned author source at 8e09f3329d08303e78af6252887d9fc880ed5409](https://github.com/HiBandan/modelTissueFlow/tree/8e09f3329d08303e78af6252887d9fc880ed5409), particularly `analysisModule.py`, `inOutTools.py`, `analysis_ANIMAL`, and the example parameters. Fetch a separate checkout. The example file named `movie_2/MARKERS/F_054.tif` was pixel-different from the WT deposit mask of the same frame name; do not transfer the demo's embryo identity or orientation labels.
- [OpenPIV 0.22.3 source release](https://pypi.org/project/OpenPIV/0.22.3/), SHA-256 `3b97358e531b57594456b4ec00dc2c903e423f7d7bb87bd50f3f4fc1823e55dc`. This includes the Cython `openpiv.process` required by the author code. The inspected 0.23.9 wheel lacks this module; switching to `pyprocess` would change the interrogation grid in an extended-area run. Use a local build with GCC and build isolation disabled.
- [Archived inputs](https://drive.google.com/file/d/1yGE5H8rcc1SODeaCENSChCLVvQxI_TZB/view). Zip SHA-256 `2db6833c2225d5f9eee82f08ea213ef645e77ac0c15fd47901c292dd69f33c6a`, 32,403,617 bytes, verified on download from Drive. See `source_manifest.json` inside for all individual hashes.

## Environment used

Linux x86_64, Python 3.12.14; GCC for OpenPIV. Core versions: numpy 1.26.4, SciPy 1.12.0, Cython 0.29.37, OpenPIV 0.22.3, OpenCV headless 4.10.0.84, scikit-image 0.24.0, scikit-learn 1.8.0, Shapely 2.0.7, tifffile 2025.6.11, numcodecs 0.15.1, imageio 2.37.0, matplotlib 3.10.8, pillow 13.0.0. Additional import dependencies included progressbar2 4.7.1, python-utils 4.2.2, deprecated 1.2.18, wrapt 2.5.2, lazy-loader 0.4, and networkx 3.4.2. This is a documented execution environment, not the undisclosed Figure 2E production environment.

## Local compatibility changes

1. In OpenPIV 0.22.3 `openpiv/validation.py`, import Python's `warnings` module and change `np.warnings.filterwarnings('ignore')` to `warnings.filterwarnings('ignore')`. Unchanged old source hits AttributeError with NumPy 1.26.4.
2. In the pinned author's `analysisModule.py`, inside `apical_basal_markers_and_masks_with_respect_to_midline`, set `dtype=object` on each of the final four polygon-mask array conversions. NumPy 1.26.4 otherwise rejects ragged mask vertices. The W53 harness consumes the two returned boundary-marker sequences, which are formed before these conversions. It does not consume the returned myosin-mask arrays. Changes apply to the isolated copies only.
3. Run on extracted source ZIP contents. `PYTHONPATH` must contain the prepared author source and the OpenPIV environment.

```sh
MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 python analysis/p77_w53_wt_pair_replay.py path-to-extracted-inputs w53-receipt.json
```

Scope is one WT embryo with public t0, a 30-second cadence supplied outside the structured time field, and two exact forward frame pairs. Demo settings supply 0.497 micrometres/pixel and the legacy PIV parameter values. The harness evaluates both contour orientations and both ends of the major axis. Pair values use the author spatial smoothing and omit the later temporal smoothing over an entire trajectory. Use these measurements as a route-fidelity diagnostic pending an original specimen manifest, production settings, and author velocity outputs.
