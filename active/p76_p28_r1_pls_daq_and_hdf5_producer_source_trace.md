# EPISTEME-P76-P28-R1 — Historical Producer and PLS Source-Trace Court

2026-10-18 KST. Documentary evidence only; NOT acquisition calibration authentication or CI result.

## PLS physical source
NeXus historical NXlrcs.f90 producer demonstration (source/content/NXlrcs.f90.md) copied the input PLS key into proton_pulses and hard-coded frequency 30.0 Hz. That source is not the authenticated running executable for 2001 LRMECS run 3701, and does not define how PLS is incremented, whether rejected/delayed/prescaled pulses are counted, or what gating/exposure interval applies. Consequently 2,268,088 pulse field / (191,912 s × 30 Hz) ≈0.394 is NOT an observed beam uptime or a calibrated neutron normalization.

Potential contextual prior publication: Rinehart and McMichael, 'EPICS upgrade of IPNS accelerator control and data acquisition system', 2001 Particle Accelerator Conference, DOI 10.1109/PAC.2001.986469. Abstract discusses accelerator acquisition/control upgrade, synchronization with a 30 Hz repetition rate, and CAMAC-to-VME conversion. This corroborates historical systems context, not the LRMECS PLS counting algorithm. Search and evaluate full primary text and any surviving source/logs before making stronger claims.

## Archived HDF5 producer
NeXus Manual, 'Viewing 2-D Data from LRMECS', identifies lrcs3701.nxs (HDF4) and lrcs3701.nx5 (HDF5), and says it will start with a conversion of the original into HDF5. This historical tutorial language strengthens the plausibility of a conversion lineage but does NOT uniquely identify the pre-existing companion's original creator, executable/tool version, parameters, source code revision, or institutional adoption. The manual also supplies a h5dump example with a historical local file path; a documentation example is not a production provenance log.

Earlier NeXus user manuals also show both filenames (e.g. Release 3.2 and later). The present source repo's relocation commit dates prove custody no earlier than those repository events; do not conflate them with file birth dates. Read-only direct pair comparison P27 found archived HDF5 duplicate monitor objects, whereas official h4toh5 2.2.5 P23 retained aliases. Therefore historical companion should not be attributed to the pinned official 2.2.5 conversion without direct evidence.

## Concrete acquisition-chain checklist
- Locate original binary/input and archived run data file for run 3701, with exact hash and release identity.
- Look for IPNS_module or get_IPNS_item('PLS') implementation, DAQ pulse counter semantics, beam gate logic, monitor integration and normalization.
- Look for historical exampledata SVN logs or NeXus manual creation notes for lrcs3701.nx5 including command line, converter version, author, timestamps and object-link behavior.
- Distinguish textual evidence (tutorial) from executable reproducibility and from accepted scientific normalization.
- If source not found, verdict remains UNIDENTIFIED rather than missing permanently.

## Contemporaneous execution status
P28 comparison code and artifact-only workflow committed, but at documentary write time no P28 workflow-run ID, completed log, or resulting artifact has been authenticated. Do not report CI SUCCESS. Physical acquisition unit, exact historical companion generator, and original PLS semantics remain HOLD. P77 WATCH/HOLD; PAPER HOLD.

Sources:
https://manual.nexusformat.org/_static/NeXusManual.pdf
https://github.com/nexusformat/wiki/blob/main/source/content/NXlrcs.f90.md
https://github.com/nexusformat/exampledata
https://doi.org/10.1109/PAC.2001.986469
