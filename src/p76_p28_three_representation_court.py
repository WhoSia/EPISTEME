#!/usr/bin/env python3
"""P76-P28: SHA-gated three-way original / archived companion / official conversion."""
import hashlib, json, re, subprocess, tarfile, tempfile
from pathlib import Path
from urllib.request import Request, urlopen
import h5py
import numpy as np

PIN = "eae516807ef7e27d1c45aab3af3a64a679154677"
ROOT = "https://raw.githubusercontent.com/nexusformat/exampledata/" + PIN + "/IPNS/LRMECS/"
BASE = "https://support.hdfgroup.org/ftp/HDF5/releases/h4toh5/h4toh5-2.2.5/bin/"
BUNDLE = "h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz"
SOURCES = [
 ("hdf4/lrcs3701.nxs", "8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39", "0e031301",115770),
 ("hdf5/lrcs3701.nx5", "20a65f41ddf61afd53126847c3204f069b0f5ae69880af4777e1863a2ac66ea2", "89484446",541008)]
MONITORS = ["/Histogram"+str(i)+"/monitor"+str(j)+"/data" for i in (1,2) for j in (1,2)]
FIELDS = ("/Histogram1/data/data","/Histogram2/data/data",
 "/Histogram1/data/time_of_flight","/Histogram2/data/time_of_flight",
 "/Histogram1/data/polar_angle","/Histogram2/data/polar_angle",
 *MONITORS,
 "/Histogram1/instrument/source/proton_pulses","/Histogram2/instrument/source/proton_pulses",
 "/Histogram1/instrument/source/frequency","/Histogram2/instrument/source/frequency",
 "/Histogram1/run_number","/Histogram2/run_number",
 "/Histogram1/start_time","/Histogram2/start_time",
 "/Histogram1/end_time","/Histogram2/end_time")
out=Path("p76_p28_three_representation_court.json")
R={"court":"P76_P28_THREE_REPRESENTATION","source_pin":PIN,
 "P77_promoted":False,"physical_normalization_authorized":False,
 "historical_companion_producer_identified":False,"vendor_sha_verified":False,
 "triplet_full_path_equality":False,"source_hashes":[],"comparisons":[]}
def pull(url,lim):
 with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-P28"}),timeout=45) as f:
  b=f.read(lim+1)
 assert len(b)<=lim,(url,len(b))
 return b
def decoded(v):
 a=np.asarray(v)
 if a.dtype.kind == "S":return b"".join(a.reshape(-1).tolist()).decode("utf-8","replace").rstrip(chr(0))
 if a.dtype.kind == "U":return "".join(a.reshape(-1).tolist()).rstrip(chr(0))
 if isinstance(v,bytes):return v.decode("utf-8","replace").rstrip(chr(0))
 return str(v)
try:
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  sourcefiles=[]
  for path,want,magic,size in SOURCES:
   b=pull(ROOT+path,size+100)
   sha=hashlib.sha256(b).hexdigest()
   assert len(b)==size and sha==want and b[:4].hex()==magic
   f=d/Path(path).name;f.write_bytes(b);sourcefiles.append(f)
   R["source_hashes"].append({"path":path,"sha256":sha,"bytes":len(b)})
  sha_text=pull(BASE+BUNDLE+".sha256",10000).decode("utf-8","replace")
  expected=re.search(r"[a-fA-F0-9]{64}",sha_text).group(0).lower()
  bundle=pull(BASE+BUNDLE,12000000)
  R["vendor_package_sha256"]=hashlib.sha256(bundle).hexdigest()
  assert R["vendor_package_sha256"]==expected
  R["vendor_sha_verified"]=True
  archive=d/BUNDLE;archive.write_bytes(bundle)
  with tarfile.open(archive,"r:gz") as tf:
   assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts and not m.issym() and not m.islnk() for m in tf.getmembers())
   tf.extractall(d,filter="data")
  install=d/"vendor";install.mkdir()
  inst=subprocess.run(["bash",str(d/"hdf"/"H4H5-2.2.5-Linux.sh")],cwd=install,input="y\ny\ny\ny\n",text=True,capture_output=True,timeout=100)
  assert inst.returncode==0,inst.stderr[-1000:]
  executables=sorted(q for q in install.rglob("*") if q.is_file() and "h4toh5" in q.name.lower() and q.suffix not in (".h",".txt",".md",".so",".a"))
  assert executables
  exe=executables[0];exe.chmod(exe.stat().st_mode|0o111)
  R["binary_sha256"]=hashlib.sha256(exe.read_bytes()).hexdigest()
  target=d/"official_conversion.h5"
  converted=subprocess.run([str(exe),str(sourcefiles[0]),str(target)],text=True,capture_output=True,timeout=100)
  R["conversion_rc"]=converted.returncode
  assert converted.returncode==0 and target.is_file(),converted.stderr[-1000:]
  R["official_conversion_sha256"]=hashlib.sha256(target.read_bytes()).hexdigest()
  with h5py.File(sourcefiles[1],"r") as B,h5py.File(target,"r") as C:
   for path in FIELDS:
    assert path in B and path in C, path
    vB=np.asarray(B[path][()]);vC=np.asarray(C[path][()])
    numeric=np.issubdtype(vB.dtype,np.number) and np.issubdtype(vC.dtype,np.number)
    equal=bool(np.array_equal(vB,vC)) if numeric else decoded(vB)==decoded(vC)
    unit_equal=decoded(B[path].attrs.get("units",""))==decoded(C[path].attrs.get("units",""))
    row={"path":path,"values_semantically_equal":equal,"units_semantically_equal":unit_equal,
         "archived_shape":list(vB.shape),"official_shape":list(vC.shape),"is_numeric":bool(numeric)}
    R["comparisons"].append(row)
    assert equal and unit_equal,row
   def evidence(f):
    addr={p:int(h5py.h5o.get_info(f[p].id).addr) for p in MONITORS}
    groups={}
    for p,a in addr.items():groups.setdefault(a,[]).append(p)
    totals={p:int(np.sum(f[p][()],dtype=np.int64)) for p in MONITORS}
    return {"monitor_partition":sorted([sorted(q) for q in groups.values()]),
     "monitor_unique_object_count":len(groups),
     "monitor_all_paths_sum":sum(totals.values()),
     "monitor_unique_object_sum":sum(totals[paths[0]] for paths in groups.values()),
     "monitor_sums_by_path":totals}
   R["existing_companion"]=evidence(B)
   R["official_converted"]=evidence(C)
   R["triplet_full_path_equality"]=all(x["values_semantically_equal"] and x["units_semantically_equal"] for x in R["comparisons"])
   R["companion_alias_fractured_vs_official"]=R["existing_companion"]["monitor_unique_object_count"]==4 and R["official_converted"]["monitor_unique_object_count"]==2
   assert R["triplet_full_path_equality"] and R["companion_alias_fractured_vs_official"]
   assert R["existing_companion"]["monitor_all_paths_sum"]==356242
   assert R["official_converted"]["monitor_unique_object_sum"]==178121
  R["verdict"]="SOURCE_SHA_PASS_VENDORSHA_PASS_TWO_HDF5_ALL_PATHS_MATCH_ALIAS_PARTITION_DIFF_PHYSICAL_UNIT_UNKNOWN"
finally:
 out.write_text(json.dumps(R,indent=2,ensure_ascii=False))
 print(json.dumps(R,indent=2,ensure_ascii=False))
assert R["triplet_full_path_equality"] and R["vendor_sha_verified"]
