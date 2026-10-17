# EPISTEME-P76-P28-R2 — Early NeXus Documentation and Unresolved Generator Lineage
Date: 2026-10-18 KST. SOURCE TRACE ONLY; NOT new physical science inference or successful P28 CI.

## Source finding with stronger chronology
NeXus documentation Release 3.1, archived as 2012-09-18 nexus-developers PDF, explicitly identifies both lrcs3701.nxs and lrcs3701.nx5 and states that the LRMECS HDF4 example is being converted to HDF5 for an example. URL: https://lists.nexusformat.org/pipermail/nexus-developers/attachments/20120918/af4aebb4/attachment-0001.pdf . A contemporaneous old SVN path refers to both formats. Therefore the companion filename and example-format pairing are documented no later than this manual, predating GitHub repository reorganization. This is a documentation-era upper bound for known distribution, NOT original file creation date or proof of the exact binary/tool/parameters used, and not proof of historic scientific facility adoption.

The later Release 3.2 and current manual repeat a description of conversion, but exact original converter still UNKNOWN. Documentation's statement is not sufficient to override directly observed archive object alias fracture or to attribute it to modern h4toh5 v2.2.5. P23's official converter preserved monitor aliases, while historical companion has four distinct objects for four monitor paths.

## Physical source
NXlrcs.f90 in NeXus wiki uses IPNS_module and calls get_IPNS_item('PLS', int_value), writes proton_pulses and literal 30.0 Hz. The source calls open_IPNS_file('/data/lrmecs/lrcs'//run_no//'.run'); published code alone neither provides that run file nor defines PLS counter/gate, and archived example producer binary remains unauthenticated. Preserve distinctions: file value vs pulse counter definition vs physical exposure vs beam charge vs independent monitor episode.

## Current operational status and verification
P28 code: src/p76_p28_three_representation_court.py.
P28 workflow: .github/workflows/p76_p28_three_representation.yml, read-only contents and artifact upload, additionally runs original P27 A/B source pair verifier.
No P28 completed run ID/log/artifact was available to this session: GitHub connector's commit-run method filters PR runs, and ordinary CI execution status is NOT thereby determined. Consequently not yet PASS or FAIL; no new scientific comparison verdict. Do not claim the workflow has been triggered, completed, or certified.

## Next decisive archival searches
Search NeXus mailing list / original SVN logs before September 2012 for conversion examples and version-specific data link handling; search original IPNS_module implementation and lrcs3701.run acquisition source in institutional public holdings. A documentation statement, a relocation date and a measured object-address difference are separate evidence classes. If no independent witness exists, maintain UNIDENTIFIED, not IRRETRIEVABLE.

P77 HOLD. PAPER HOLD. BOT_CONTRIBUTION_ZERO.
