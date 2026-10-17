#!/usr/bin/env python3
"""EPISTEME P76-P26-R1: compare pre-existing HDF4 and HDF5 NeXus LRMECS archived counterparts.
Neither filename similarity nor matching fields proves the HDF5 was produced by h4toh5.
"""
import hashlib,json,tempfile
from pathlib import Path
from urllib.request import Request,urlopen
import numpy as np,h5py,pyhdf.V
from pyhdf.HDF import HDF,HC
from pyhdf.SD import SD,SDC
PIN="eae516807ef7e27d1c45aab3af3a64a679154677"
FILES=[
 ("IPNS/LRMECS/hdf4/lrcs3701.nxs",115770,"0e031301","8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39"),
 ("IPNS/LRMECS/hdf5/lrcs3701.nx5",541008,"89484446",None)]
FIELDS=("/Histogram1/data/data","/Histogram2/data/data",
 "/Histogram1/data/time_of_flight","/Histogram2/data/time_of_flight",
 "/Histogram1/data/polar_angle","/Histogram2/data/polar_angle",
 "/Histogram1/monitor1/data","/Histogram2/monitor1/data",
 "/Histogram1/monitor2/data","/Histogram2/monitor2/data",
 "/Histogram1/instrument/source/proton_pulses","/Histogram2/instrument/source/proton_pulses",
 "/Histogram1/instrument/source/frequency","/Histogram2/instrument/source/frequency",
 "/Histogram1/run_number","/Histogram2/run_number",
 "/Histogram1/start_time","/Histogram2/start_time",
 "/Histogram1/end_time","/Histogram2/end_time")
R={"court":"P76_P26_R1_PREEXISTING_NEXUS_HDF4_HDF5_PAIR","repository":"nexusformat/exampledata",
 "pinned_commit":PIN,"both_source_bytes_verified":False,"source_files":[],
 "relationship_exact_converter_binary_proved":False,"historical_institution_adoption_proved":False,
 "scientific_physics_semantics_proved":False,"path_checks":[],"P77_independent_novelty":False}
OUT=Path("p76_p26_r1_preexisting_neXus_counterpart.json")
def pull(relative,cap):
 url=f"https://raw.githubusercontent.com/nexusformat/exampledata/{PIN}/{relative}"
 with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-source-counterpart"}),timeout=35) as f:
  d=f.read(cap+1)
 assert len(d)<=cap
 return d
def canon_text(v):
 if isinstance(v,bytes):return v.decode("utf8","replace").rstrip(chr(0))
 if isinstance(v,str):return v.rstrip(chr(0))
 a=np.asarray(v)
 if a.dtype.kind=="S":
  return b"".join(a.reshape(-1).tolist()).decode("utf8","replace").rstrip(chr(0))
 if a.dtype.kind=="U":
  return "".join(a.reshape(-1).tolist()).rstrip(chr(0))
 return None
def summarize(a):
 arr=np.asarray(a)
 return {"shape":list(arr.shape),"dtype":str(arr.dtype),"n":int(arr.size),
   "head":[str(x) for x in arr.reshape(-1)[:5]],
   "sum":float(np.sum(arr,dtype=np.float64)) if np.issubdtype(arr.dtype,np.number) else None}
try:
 with tempfile.TemporaryDirectory() as td:
  directory=Path(td);paths=[]
  for filename,size,magic,wantsha in FILES:
   data=pull(filename,size+100)
   sha=hashlib.sha256(data).hexdigest()
   row={"original_path":filename,"bytes":len(data),"sha256":sha,"magic":data[:4].hex(),
        "size_equal":len(data)==size,"magic_equal":data[:4].hex()==magic}
   assert row["size_equal"] and row["magic_equal"]
   if wantsha:assert sha==wantsha
   R["source_files"].append(row)
   path=directory/Path(filename).name;path.write_bytes(data);paths.append(path)
  R["both_source_bytes_verified"]=True
  h=HDF(str(paths[0]),HC.READ);v=h.vgstart();sd=SD(str(paths[0]),SDC.READ)
  try:
   groups={};ref=-1
   while True:
    try:ref=v.getid(ref)
    except Exception:break
    o=v.attach(ref)
    try:groups[ref]={"name":str(o._name),"children":list(o.tagrefs())}
    finally:o.detach()
   seen_children={r for d in groups.values() for tag,r in d["children"] if tag==HC.DFTAG_VG}
   old={}
   def walk(ref,prefix,seen):
    if ref in seen:return
    base=prefix+"/"+groups[ref]["name"]
    for tag,r in groups[ref]["children"]:
     if tag==HC.DFTAG_VG and r in groups:walk(r,base,seen|{ref})
     elif tag==HC.DFTAG_NDG:
      ob=sd.select(sd.reftoindex(r))
      try:
       name=ob.info()[0];full=base+"/"+name
       if full in FIELDS:
        arr=np.asarray(ob.get())
        old[full]={"ref":int(r),"array":arr,
                   "units":str(ob.attributes().get("units",""))}
      finally:ob.endaccess()
   for r in sorted(set(groups)-seen_children):walk(r,"",set())
   R["hdf4_path_count"]=len(old)
   with h5py.File(paths[1],"r") as f:
    top={};h5paths=[]
    def visitors(name,obj):
     if isinstance(obj,h5py.Dataset):h5paths.append("/"+name)
    f.visititems(visitors)
    R["hdf5_dataset_count_unique_visited"]=len(h5paths)
    R["hdf5_head_paths"]=h5paths[:45]
    for requested in FIELDS:
     left=old.get(requested)
     row={"path":requested,"hdf4_exists":left is not None,
          "hdf5_exact_path_exists":requested in f and isinstance(f[requested],h5py.Dataset)}
     if left is not None:
      row["old_ref"]=left["ref"];row["old_units"]=left["units"]
      row["old"]=summarize(left["array"])
     if row["hdf5_exact_path_exists"]:
      ds=f[requested];arr=np.asarray(ds[()])
      row["hdf5_object_addr"]=int(h5py.h5o.get_info(ds.id).addr)
      row["new"]=summarize(arr)
      row["new_units"]=canon_text(ds.attrs.get("units",""))
      if left is not None:
       row["shape_equal"]=list(left["array"].shape)==list(arr.shape)
       row["elementwise_equal"]=bool(np.array_equal(left["array"],arr))
       row["unit_string_equal"]=row["old_units"]==row["new_units"]
       if requested.endswith(("/start_time","/end_time")):
        row["semantic_datetime_equal"]=canon_text(left["array"])==canon_text(arr)
        row["old_time_text"]=canon_text(left["array"])
        row["new_time_text"]=canon_text(arr)
     R["path_checks"].append(row)
    R["hdf5_data_paths_like_data"]=[x for x in h5paths if x.endswith("/data")][:45]
  finally:sd.end();v.end();h.close()
 R["monitor_alias_checks"]=[]
 for monitor in ("monitor1","monitor2"):
  p1="/Histogram1/"+monitor+"/data"
  p2="/Histogram2/"+monitor+"/data"
  a=next(x for x in R["path_checks"] if x["path"]==p1)
  b=next(x for x in R["path_checks"] if x["path"]==p2)
  R["monitor_alias_checks"].append({"name":monitor,
   "hdf4_shared_source_ref":a["old_ref"]==b["old_ref"],
   "hdf5_shared_object_addr":a["hdf5_object_addr"]==b["hdf5_object_addr"],
   "both_path_values_equal":bool(a["elementwise_equal"] and b["elementwise_equal"])})
 R["monitor_alias_fracture_in_preexisting_hdf5"]=all(
  x["hdf4_shared_source_ref"] and not x["hdf5_shared_object_addr"] and x["both_path_values_equal"] for x in R["monitor_alias_checks"])
 R["units_semantically_equal"]=all(x.get("unit_string_equal") is True for x in R["path_checks"])
 R["datetime_semantically_equal"]=all(x.get("semantic_datetime_equal") is True for x in R["path_checks"] if x["path"].endswith(("/start_time","/end_time")))
 R["exact_path_pair_count"]=sum(x.get("hdf4_exists") and x.get("hdf5_exact_path_exists") for x in R["path_checks"])
 R["exact_path_numeric_or_string_equal_count"]=sum(x.get("elementwise_equal") is True for x in R["path_checks"])
 R["native_comparison_status"]="SAME_REPO_SOURCE_PAIR_AUDITED_NOT_EXACT_ORIGIN_CAUSALITY"
finally:
 OUT.write_text(json.dumps(R,indent=2))
 print(json.dumps(R,indent=2))
assert R["both_source_bytes_verified"] and len(R["path_checks"])==len(FIELDS)\nassert R["monitor_alias_fracture_in_preexisting_hdf5"] and R["units_semantically_equal"] and R["datetime_semantically_equal"]
