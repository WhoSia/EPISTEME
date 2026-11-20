# EPISTEME-P77 W53 — WT Velocity Replay and Case Decision

2026-11-21 KST. [W52 route audit](p77_w52_20261121_s_biad602_figure_2e_route_audit.md) · [Four original PDFs and their Drive hashes](p77_w53_20261121_original_literature_intake.md) · [Notion ledger](https://app.notion.com/p/41eef561cf9281cfb375c85469d03ec9) · [Director decision](p77_w53_20261121_director_decision.md).

## Scope

The [Gehrels paper, Figure 2E](https://pmc.ncbi.nlm.nih.gov/articles/PMC9963527/) reports the whole-contour spatial mean and group comparisons at 9 and 17 min, with 5 WT, 6 toll vl and 5 cta embryos. The [supporting methods](https://drive.google.com/file/d/1B8ApKJ-ZZ6OgYjA68RGo4KQlxWSBOGlT/view) describe t0, apical/basal contours, midline, and PIV. W53 executes one candidate WT embryo's two forward pairs under explicit reconstructions with the [pinned author code](https://github.com/HiBandan/modelTissueFlow/tree/8e09f3329d08303e78af6252887d9fc880ed5409). Original panel membership, production orientation, individual expected values, and group statistics are unverified.

## Access path and calibration

- [Deposited embryo](https://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/602/S-BIAD602/Files/DataRepository/TwoPhoton/wildtype/embryo1_210122_2/). First WT MEM is an 8-bit TIFF, 78 × 1024 × 1024. The deposited ImageJ structured `finterval=inf`; the embedded instrument record says `Equidistant (Period 30000 ms)`. The [separate deposited note](https://ftp.ebi.ac.uk/biostudies/fire/S-BIAD/602/S-BIAD602/Files/DataRepository/TwoPhoton/wildtype/EmbryoInfo210122.rtf) gives 30 s/frame and frame 20 for embryo 2. The inspected [OME-Zarr scale](https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD602/2ab86128-ac80-4ab4-a1fc-463ba6883e53/cb8898db-a270-45c8-886f-835c9490a44b.ome.zarr/0/.zattrs) is the string Infinity. A nonfinite structured interval was already present in the deposited TIFF, so this pair cannot identify the converter as the source of the nonfinite interval. A separate source TIFF next to the original camera data or a conversion trace would be needed to place the original cause earlier.
- [Current image query](https://beta.bioimagearchive.org/search/v1/search/fts/image?facet.accession_id=S-BIAD602&pagination.page_size=100) still returns five hits. The WT MEM has a full time stack, but F_038 and F_054 contour masks are absent from the response, and the returned contour is F_020. One toll vl frame was returned and no cta object. For this run the masks were obtained through their deposited FTP paths. This is a query-scope result, not a verdict on all other routes through the website.
- 9 full-resolution Zarr frames (20, 37–40, and 53–56, zero-based) decoded and match their TIFF counterpart exactly. No claim for other frames, channels, scales, or embryos. The same 30 s cadence was supplied to both runs. Adjacent image chunks are not interchangeable: the 38th and 39th arrays differ at 613,300 pixels, and the 54th and 55th at 626,352.
- [Ambroset audit](https://drive.google.com/file/d/1wFy-hgWJPL6Fv9o9eHqc9gKOES0NC5hD/view) §§3.2 and 3.3.2 and [Supporting Materials S.2](https://drive.google.com/file/d/1u_QJ8UejKit-hhE_N3Llqat2EVhNJKkK/view) report execution failures. W53 built OpenPIV 0.22.3 with GCC and applied two isolated compatibility fixes. See the [runtime note](../analysis/p77_w53_wt_pair_runtime.md). The archived code's own demo movie 2 mask F_054 did not match the deposited WT mask of the same name.

## Numerical result

Both paths generated identical PIV arrays (51 × 51) and, with identical masks, parameters, and orientation, identical final velocity outputs. The 30 s cadence and t0 mapping give 38→39 and 54→55. The code uses the author's demo pixel scale (0.497 μm/pixel), original PIV call, boundary routine, projection and spatial integration, two spatial averaging passes and no across-time smoothing. Four parameter settings probe the two code directions and two ends of the principal axis. After expressing each result in image-clockwise sign convention:

| Code orientation and reference quadrant | 9 min (μm/min) | 17 min (μm/min) |
|---|---:|---:|
| D-cw / Q-4 | 0.387876 | 0.627332 |
| D-cw / Q-2 | 0.159792 | 0.416856 |
| D-ccw / Q-4 | 0.410887 | 0.521739 |
| D-ccw / Q-2 | 0.189463 | 0.418378 |

Per-setting increments run from 0.110852 to 0.257064 μm/min. This measures numerical sensitivity of this single replay. The four settings are not four independent specimens. The two results are conditional on the deposited t0, demo settings and geometry workarounds. Do not infer the published group effect or biological mechanism from the increments.

## Preservation and decision

[Replay code](../analysis/p77_w53_wt_pair_replay.py) · [Drive inputs ZIP](https://drive.google.com/file/d/1yGE5H8rcc1SODeaCENSChCLVvQxI_TZB/view) · [Drive receipt JSON](https://drive.google.com/file/d/1TVlB11PAakAu62zqbWLf6X7sptLw2Pzr/view). The input ZIP was downloaded again and matched the uploaded 32,403,617-byte ZIP. A replay from that downloaded copy reproduced every result field except elapsed seconds (35.154 and 35.671). First-run receipt SHA-256 `c0f93c2eff9844bfe8e16287c5821d050eb629dd47bf97d159f4c5b8b030144a`.

The non-AI case demonstrates unequal discovery and a calibration repair with recoverable retained inputs. No observed route choice by another research group, independently changed downstream test, or causal effect of adoption is established. Close the initial two-probe allocation on the technical-contrast branch. Pause the P77 independent case line, preserve the comparator for Research OS reuse, and retain P78 HOLD / PAPER HOLD. [Reopening criteria](p77_w53_20261121_director_decision.md) · [Current source queue](p77_w53_20261121_missing_source_queue.md).
