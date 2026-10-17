#!/usr/bin/env python3
"""P76-P13: vendor verified official conversion, all named SDS query and type court."""
import hashlib,json,re,subprocess,tarfile,tempfile
from pathlib import Path
from urllib.request import urlopen,Request
import numpy as np,h5py
BASE="https://support.hdfgroup.org/ftp/HDF5/releases/h4toh5/h4toh5-2.2.5/bin/"
NAME="h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz"
PIN="2c46ad56bea5aab05e996e473a81dcbd9a66b125"
FILES=[("mfhdf/hdfimport/SDSfloat2.hdf","3ba791239a5874bf9d97e1765a3e2896dbe965680b7fee59f9cc96afefb28b38"),
("mfhdf/hdp/testfiles/sds_compressed.hdf","bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb")]
def get(url,limit=12000000):
 with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-P13"}),timeout=45) as f:b=f.read(limit+1)
 assert len(b)<=limit
 return b
def run(cmd,**kw):return subprocess.run(cmd,capture_output=True,text=True,timeout=55,**kw)
R={"court":"P76_P13_VENDOR_ELEMENTWISE","files":[],"complete":False,"scientific_claim_preserved":None,
   "real_world_migration_case":False,"new_epistemic_theorem":False}
OUT=Path("p76_p13_vendor_elementwise_receipt.json")
try:
 expected=re.search(r"[a-fA-F0-9]{64}",get(BASE+NAME+".sha256",20000).decode()).group(0).lower()
 tar=get(BASE+NAME);R["publisher_sha_match"]=hashlib.sha256(tar).hexdigest()==expected
 assert R["publisher_sha_match"]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td);t=d/NAME;t.write_bytes(tar)
  with tarfile.open(t,"r:gz") as f:
   assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts and not m.issym() and not m.islnk() for m in f.getmembers())
   f.extractall(d,filter="data")
  expanded=d/"expanded";expanded.mkdir()
  inst=run(["bash",str(d/"hdf"/"H4H5-2.2.5-Linux.sh")],cwd=expanded,input="y\ny\ny\ny\n")
  assert inst.returncode==0,(inst.stdout[-600:],inst.stderr)
  binary=next(p for p in expanded.rglob("*") if p.is_file() and "h4toh5" in p.name.lower())
  binary.chmod(binary.stat().st_mode|0o111)
  for path,want in FILES:
   raw=get("https://raw.githubusercontent.com/HDFGroup/hdf4/"+PIN+"/"+path,2000000)
   assert hashlib.sha256(raw).hexdigest()==want
   src=d/Path(path).name;src.write_bytes(raw)
   converted=d/(src.name+".h5")
   conv=run([str(binary),str(src),str(converted)])
   assert conv.returncode==0,(path,conv.stderr)
   native=run(["hdp","dumpsds",str(src)])
   assert native.returncode==0
   text=native.stdout
   blocks=re.split(r"(?=Variable Name\s*=)",text)[1:]
   original={}
   for blk in blocks:
    name=re.search(r"Variable Name\s*=\s*([^\n]+)",blk).group(1).strip()
    rank=int(re.search(r"Rank\s*=\s*(\d+)",blk).group(1))
    dims=[int(z) for z in re.findall(r"\bSize\s*=\s*(\d+)",blk)][:rank]
    tp=re.search(r"Type\s*=\s*([^\n]+)",blk).group(1).strip()
    if "Data :" not in blk:continue
    data=blk.split("Data :",1)[1]
    nums=[float(v) for v in re.findall(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?",data)]
    if len(nums)!=int(np.prod(dims)):
     original[name]={"status":"HD P_TEXT_NOT_EXACTLY_ARRAY","num_tokens":len(nums),"expected":int(np.prod(dims))}
     continue
    original[name]={"status":"DATA_PARSE_OK","shape":dims,"type":tp,"values":np.array(nums).reshape(dims)}
   with h5py.File(converted,"r") as f:
    names={}
    def collect(name,obj):
     if isinstance(obj,h5py.Dataset):
      names[name]={"shape":list(obj.shape),"dtype":str(obj.dtype),"values":np.asarray(obj[()]),"attributes":sorted(obj.attrs.keys())}
    f.visititems(collect)
   item={"source":path,"original_sha":want,"original_dataset_count":len(original),"converted_dataset_count":len(names),"SDS":[]}
   for name,old in original.items():
    match=[(p,v) for p,v in names.items() if p.rsplit("/",1)[-1]==name]
    rec={"original_name":name,"original_type":old.get("type"),"original_shape":old.get("shape"),"native_parser_status":old["status"],"matched":len(match)}
    if len(match)==1:
     p,v=match[0];rec.update(target_name=p,converted_type=v["dtype"],converted_shape=v["shape"],converted_attributes=v["attributes"])
     if old["status"]=="DATA_PARSE_OK":
      rec["numeric_equal"]=bool(np.array_equal(old["values"],v["values"]))
      rec["element_count"]=int(old["values"].size)
      rec["original_sum"]=float(old["values"].sum())
      rec["converted_sum"]=float(v["values"].sum())
    item["SDS"].append(rec)
   R["files"].append(item)
 R["complete"]=True
finally:
 OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2))
 print(json.dumps(R,ensure_ascii=False,indent=2))
assert R["complete"] and len(R["files"])==2
