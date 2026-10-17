#!/usr/bin/env python3
"""P76-P22a: independent HDF4 Vgroup/tagref path audit on original NeXus IPNS.
No inferred detector/axis relation from equal basenames; all claims are source-bound.
"""
import hashlib,json,tempfile
from pathlib import Path
from urllib.request import Request,urlopen
from collections import defaultdict
from pyhdf.HDF import HDF,HC
import pyhdf.V  # HDF.vgstart resolves this module lazily by name
from pyhdf.SD import SD,SDC
import numpy as np

PIN="eae516807ef7e27d1c45aab3af3a64a679154677"
NAME="IPNS/LRMECS/hdf4/lrcs3701.nxs"
SHA="8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39"
R={"court":"P76_P22_SOURCE_VGROUP_IDENTITY","upstream_pin":PIN,"file_sha":SHA,
 "original_paths":[],"pair_candidates":[],"data_values_recovered":0,
 "converted_hdf5_test_executed":False,"new_P77_mechanism":False}
out=Path("p76_p22_source_vgroup_court.json")
try:
 url="https://raw.githubusercontent.com/nexusformat/exampledata/"+PIN+"/"+NAME
 with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-P22"}),timeout=35) as f:b=f.read(200000)
 assert hashlib.sha256(b).hexdigest()==SHA and b[:4]==bytes.fromhex("0e031301")
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp)/"lrcs3701.nxs";p.write_bytes(b)
  h=HDF(str(p),HC.READ);v=h.vgstart();sd=SD(str(p),SDC.READ)
  groups={}
  cursor=-1
  while True:
   try:cursor=v.getid(cursor)
   except Exception:break
   vg=v.attach(cursor)
   try:
    groups[cursor]={"name":str(vg._name),"class":str(vg._class),"members":list(vg.tagrefs()),
                    "attributes":{str(k):str(val[2])[:160] for k,val in vg.attrinfo().items()}}
   finally:vg.detach()
  childrefs={r for g in groups.values() for tag,r in g["members"] if tag==HC.DFTAG_VG}
  roots=sorted(set(groups)-childrefs)
  R["group_count"]=len(groups);R["root_count"]=len(roots)
  R["root_examples"]=[{"ref":x,"name":groups[x]["name"],"class":groups[x]["class"]} for x in roots[:30]]
  raw=[]
  def walk(gref,prefix,vis):
   if gref in vis or len(vis)>20:return
   g=groups[gref];name=g["name"]
   path=prefix+"/"+name
   local=[]
   for tag,ref in g["members"]:
    if tag in (HC.DFTAG_NDG,):
     try:
      obj=sd.select(sd.reftoindex(ref))
      try:
       info=obj.info(); attrs={str(k):str(x)[:220] for k,x in obj.attributes().items()}
       item={"path":path+"/"+info[0],"ref":ref,"name":str(info[0]),"shape":list(info[2]),
             "sd_type_code":info[3],"attributes":attrs}
       try:
        a=np.asarray(obj.get())
        item["actual_shape"]=list(a.shape)
        item["decoded_dtype"]=str(a.dtype)
        item["element_count"]=int(a.size)
        item["sum"]=float(np.asarray(a,dtype=np.float64).sum()) if a.size else None
        item["head"]=[float(x) for x in a.reshape(-1)[:6]] if a.size else []
        R["data_values_recovered"]+=int(a.size)
       except Exception as exc:item["decode_error"]=type(exc).__name__+":"+str(exc)[:180]
       local.append(item);raw.append(item)
      finally:obj.endaccess()
     except Exception as exc:
      raw.append({"path":path,"ref":ref,"dataset_error":type(exc).__name__+":"+str(exc)[:180]})
    elif tag==HC.DFTAG_VG and ref in groups:
     walk(ref,path,vis|{gref})
   data=[x for x in local if x["name"]=="data"]
   axes=[x for x in local if x["name"]=="time_of_flight"]
   if data and axes:
    R["pair_candidates"].append({"group":path,"data":[x["path"] for x in data],"axes":[x["path"] for x in axes],
                                 "scope":"same source Vgroup only, axis binding not yet proven"})
  for root in roots:walk(root,"",set())
  unique={x["path"]+"|"+str(x.get("ref")):x for x in raw}
  R["original_paths"]=list(unique.values())
  R["data_name_paths"]=sorted(set(x["path"] for x in raw if x.get("name")=="data"))
  R["tof_name_paths"]=sorted(set(x["path"] for x in raw if x.get("name")=="time_of_flight"))
  sd.end();v.end();h.close()
finally:
 out.write_text(json.dumps(R,indent=2))
 print(json.dumps({k:v if k!="original_paths" else v[:18] for k,v in R.items()},indent=2))
