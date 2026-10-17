#!/usr/bin/env python3
"""P76-P21 original source and official vendor NeXus instrument HDF4 preservation preflight."""
import hashlib,json,os,re,subprocess,tarfile,tempfile
from pathlib import Path
from urllib.request import urlopen,Request
PIN="eae516807ef7e27d1c45aab3af3a64a679154677"
SOURCES=[
 ("IPNS/LRMECS/hdf4/lrcs3701.nxs","8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39"),
 ("APS/CCDImageServer/hdf4/Smither400.3_apr0300051.hdf","f67d40f0cef33c6d0336fcc012d8940d2dc8b58767f36d7468faf4b5a11c34c7")]
BASE="https://support.hdfgroup.org/ftp/HDF5/releases/h4toh5/h4toh5-2.2.5/bin/"
ARCHIVE="h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz"
R={"court":"P76_P21_AUTHENTIC_INSTRUMENT_CONVERSION","source_commit":PIN,"sources":[],"vendor_sha_verified":False,"scientific_query_equivalence_proved":False,"instrument_physical_semantics_verified":False}
def get(u,maxlen):
 with urlopen(Request(u,headers={"User-Agent":"EPISTEME-P76-P21"}),timeout=40) as f:
  d=f.read(maxlen+1)
 assert len(d)<=maxlen
 return d
def run(args,**kw):return subprocess.run(args,text=True,capture_output=True,timeout=55,**kw)
try:
 expected=re.search(r"[0-9a-fA-F]{64}",get(BASE+ARCHIVE+".sha256",10000).decode()).group().lower()
 blob=get(BASE+ARCHIVE,12000000);R["vendor_sha_verified"]=hashlib.sha256(blob).hexdigest()==expected
 assert R["vendor_sha_verified"]
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);p=root/ARCHIVE;p.write_bytes(blob)
  with tarfile.open(p,"r:gz") as f:
   assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts and not m.issym() and not m.islnk() for m in f.getmembers())
   f.extractall(root,filter="data")
  target=root/"expanded";target.mkdir()
  install=run(["bash",str(root/"hdf"/"H4H5-2.2.5-Linux.sh")],cwd=target,input="y\ny\ny\ny\n")
  assert install.returncode==0,install.stderr[-900:]
  binaries=[x for x in target.rglob("*") if x.is_file() and "h4toh5" in x.name.lower() and x.suffix not in (".h",".txt",".md",".so",".a")]
  assert binaries
  binary=binaries[0];binary.chmod(binary.stat().st_mode|0o111)
  for path,sha in SOURCES:
   data=get("https://raw.githubusercontent.com/nexusformat/exampledata/"+PIN+"/"+path,900000)
   assert hashlib.sha256(data).hexdigest()==sha and data[:4]==b"\x0e\x03\x13\x01"
   original=root/Path(path).name;original.write_bytes(data)
   old=run(["hdp","dumpsds",str(original)])
   oldl=run(["hdp","list",str(original)])
   converted=root/(original.name+".h5")
   conv=run([str(binary),str(original),str(converted)])
   item={"source":path,"sha256":sha,"source_bytes":len(data),"native_dumpsds_exit":old.returncode,
     "native_sds_names":re.findall(r"Variable Name\s*=\s*([^\n]+)",old.stdout)[:70],
     "native_snippet":old.stdout[:1300],"native_errors":old.stderr[-400:],
     "native_list_exit":oldl.returncode,"converter_exit":conv.returncode,
     "converter_stderr":conv.stderr[-1600:],
     "h5_exists":converted.exists() and converted.stat().st_size>0}
   if item["h5_exists"]:
    header=run(["h5dump","-H",str(converted)])
    item["hdf5_header_exit"]=header.returncode
    item["hdf5_datasets"]=re.findall(r'DATASET "([^"]+)"',header.stdout)[:80]
    item["hdf5_header_excerpt"]=header.stdout[:1800]
    item["h5_size"]=converted.stat().st_size
   R["sources"].append(item)
finally:
 Path("p76_p21_instrument_source_vendor_receipt.json").write_text(json.dumps(R,indent=2))
 print(json.dumps(R,indent=2))
assert R["vendor_sha_verified"] and len(R["sources"])==2
