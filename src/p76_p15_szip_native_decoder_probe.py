#!/usr/bin/env python3
"""P76-P15: native SZIP decoding against independently loaded libaec; no HDF5 conversion surrogate."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
from urllib.request import Request,urlopen
PIN="2c46ad56bea5aab05e996e473a81dcbd9a66b125"
P="mfhdf/hdp/testfiles/sds_compressed.hdf"
SHA="bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb"
result={"source_sha_expected":SHA,"native_szip_values_verified":False,"status":"STARTED","attempts":[]}
out=Path("p76_p15_szip_native_recovery.json")
def cmd(args,env=None):
 r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=40)
 return {"cmd":args,"exit":r.returncode,"stdout_tail":r.stdout[-1250:],"stderr_tail":r.stderr[-650:],"has_unavailable":("SZIP library is not available" in r.stdout),"has_read_failure":("Unable to read SZIP" in r.stdout)}
try:
 with urlopen(Request("https://raw.githubusercontent.com/HDFGroup/hdf4/"+PIN+"/"+P,headers={"User-Agent":"EPISTEME-P76-P15"}),timeout=35) as f:raw=f.read()
 assert hashlib.sha256(raw).hexdigest()==SHA
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/"sds_compressed.hdf";p.write_bytes(raw)
  for name,environment in [("system",None),("sz_alias",dict(os.environ,LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu"))]:
   observation=cmd(["hdp","dumpsds",str(p)],env=environment)
   observation["route"]=name
   result["attempts"].append(observation)
  libs=cmd(["ldconfig","-p"])
  result["libaec_discovery"]=("\n".join(libs["stdout_tail"].splitlines()[-15:]))[:750]
  result["native_szip_values_verified"]=any(a["exit"]==0 and not a["has_unavailable"] and not a["has_read_failure"] and "Variable Name = SDSszip" in a["stdout_tail"] for a in result["attempts"])
 result["status"]="RECOVERED" if result["native_szip_values_verified"] else "NO_INDEPENDENT_SZIP_DECODE"
finally:
 out.write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
