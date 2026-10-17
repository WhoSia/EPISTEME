#!/usr/bin/env python3
"""P76-P20 actual research-instrument HDF4 byte custody and native source metadata."""
import hashlib,json,subprocess
from pathlib import Path
from urllib.request import Request,urlopen
COMMIT="eae516807ef7e27d1c45aab3af3a64a679154677"
SOURCES=[
 ("ANSTO/hdf4/PLP0006018.nx.hdf",572682),
 ("IPNS/LRMECS/hdf4/lrcs3701.nxs",115770),
 ("APS/CCDImageServer/hdf4/Smither400.3_apr0300051.hdf",568977)
]
R={"court":"P76_P20_NEXUS_REAL_RESEARCH_HDF4_SOURCE","repository":"nexusformat/exampledata",
 "pin":COMMIT,"files":[],"scientific_concordance_untested":True,"adoption_causality_unproved":True}
try:
 for path,size in SOURCES:
  url=f"https://raw.githubusercontent.com/nexusformat/exampledata/{COMMIT}/{path}"
  with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-real-research-fixture"}),timeout=35) as f:raw=f.read(size+1)
  magic=raw[:4].hex()
  item={"original_path":path,"upstream_expected_length":size,"raw_length":len(raw),
     "sha256":hashlib.sha256(raw).hexdigest(),"magic":magic}
  item["source_byte_validated"]=len(raw)==size and magic=="0e031301"
  if item["source_byte_validated"]:
   p=Path(path).name;p=Path("p76_p20_"+p);p.write_bytes(raw)
   a=subprocess.run(["hdp","list",str(p)],capture_output=True,text=True,timeout=25)
   item["native_hdp_exit"]=a.returncode
   item["native_hdp_excerpt"]=a.stdout[:1800]
   item["native_hdp_error"]=a.stderr[:250]
  item["classification"]="HDF4_VERIFIED" if item["source_byte_validated"] else ("HDF5_MAGIC_UNDER_HDF4_FOLDER" if magic=="89484446" else "UNSUPPORTED_OR_UNKNOWN")
  R["files"].append(item)
finally:
 Path("p76_p20_scientific_hdf4_custody.json").write_text(json.dumps(R,indent=2))
 print(json.dumps(R,indent=2))
assert sum(x.get("source_byte_validated") and x.get("native_hdp_exit")==0 for x in R["files"])>=2,"Require two source-byte-authenticated real research HDF4 files with native reader PASS"
