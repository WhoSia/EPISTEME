#!/usr/bin/env python3
"""Source-grounded HDF4 read-only preflight (NOT h4toh5 conversion)."""
import hashlib,json,subprocess
from pathlib import Path
from urllib.request import urlopen,Request
ROOT="https://raw.githubusercontent.com/HDFGroup/hdf4/2c46ad56bea5aab05e996e473a81dcbd9a66b125/"
FILES=("mfhdf/hdfimport/SDSfloat2.hdf","mfhdf/hdp/testfiles/sds_compressed.hdf")
out=[]
for relative in FILES:
    raw=urlopen(Request(ROOT+relative,headers={"User-Agent":"EPISTEME-source-check"}),timeout=30).read()
    assert 100<len(raw)<100_000, "Unexpected sample length"
    name=Path(relative).name
    Path(name).write_bytes(raw)
    p=subprocess.run(["hdp","dumpsds",name],capture_output=True,text=True,timeout=30)
    out.append({"path":relative,"sha256":hashlib.sha256(raw).hexdigest(),
      "byte_count":len(raw),"hdp_returncode":p.returncode,
      "hdp_output_preview":p.stdout[:600],"hdp_stderr_preview":p.stderr[:350]})
    assert p.returncode==0, f"Source HDF4 native reader failed for {relative}: {p.stderr[:200]}"
r={"court":"P76_P10_OFFICIAL_SOURCE_HDF4_READER","upstream_sha":"2c46ad56bea5aab05e996e473a81dcbd9a66b125",
  "source_files":out,"original_reader_executed":True,
  "official_h4toh5_converter_executed":False,"converted_hdf5_query_equal":None,
  "physical_original_measurement":False,"new_epistemic_mechanism":False}
Path("p76_p10_official_hdf4_native_reader_receipt.json").write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
