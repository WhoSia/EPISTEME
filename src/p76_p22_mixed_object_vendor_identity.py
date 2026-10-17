#!/usr/bin/env python3
"""P76-P22b: old mixed SDS/Vdata/Vgroup exact-path vs vendor-HDF5 values, conservative mapping."""
import hashlib,json,re,subprocess,tarfile,tempfile
from collections import Counter
from pathlib import Path
from urllib.request import Request,urlopen
import numpy as np,h5py
import pyhdf.V,pyhdf.VS
from pyhdf.HDF import HDF,HC
from pyhdf.SD import SD,SDC
SRC_SHA="8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39"
PIN="eae516807ef7e27d1c45aab3af3a64a679154677"
SRC="IPNS/LRMECS/hdf4/lrcs3701.nxs"
BASE="https://support.hdfgroup.org/ftp/HDF5/releases/h4toh5/h4toh5-2.2.5/bin/"
BUNDLE="h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz"
R={"court":"P76_P22_MIXED_OBJECT_PATH_TEST","original_sha":SRC_SHA,"source_pin":PIN,
   "primary_pairs":[],"original_path_records":[],"vendor_checksum_verified":False,
   "format_conversion_executed":False,"historical_institution_adoption_established":False,"P77_independent_novelty":False}
OUT=Path("p76_p22_mixed_path_comparison.json")
def get(u,lim):
 with urlopen(Request(u,headers={"User-Agent":"EPISTEME-P76-P22"}),timeout=40) as f: b=f.read(lim+1)
 assert len(b)<=lim,(u,len(b))
 return b
def cmd(a,**k):return subprocess.run(a,capture_output=True,text=True,timeout=60,**k)
def js(v):
 if isinstance(v,bytes):return v.decode("utf8","replace")
 if isinstance(v,np.ndarray):return [js(x) for x in v.tolist()]
 if isinstance(v,(list,tuple)):return [js(x) for x in v]
 if isinstance(v,np.generic):return v.item()
 return v
try:
 raw=get("https://raw.githubusercontent.com/nexusformat/exampledata/"+PIN+"/"+SRC,180000)
 assert hashlib.sha256(raw).hexdigest()==SRC_SHA and raw[:4]==bytes.fromhex("0e031301")
 target_sha=re.search(r"[a-fA-F0-9]{64}",get(BASE+BUNDLE+".sha256",10000).decode()).group().lower()
 archive=get(BASE+BUNDLE,12000000);R["vendor_checksum_verified"]=hashlib.sha256(archive).hexdigest()==target_sha
 assert R["vendor_checksum_verified"]
 with tempfile.TemporaryDirectory() as t:
  root=Path(t);p=root/"lrcs3701.nxs";p.write_bytes(raw)
  h=HDF(str(p),HC.READ);v=h.vgstart();vs=h.vstart();sd=SD(str(p),SDC.READ)
  groups={};ref=-1
  while True:
   try:ref=v.getid(ref)
   except Exception:break
   g=v.attach(ref)
   try:groups[ref]={"name":str(g._name),"class":str(g._class),"tagrefs":list(g.tagrefs())}
   finally:g.detach()
  children={x for g in groups.values() for tag,x in g["tagrefs"] if tag==HC.DFTAG_VG}
  roots=sorted(set(groups)-children)
  paths=[]
  def descend(ref,parent,seen):
   if ref in seen or len(seen)>24:return
   grp=groups[ref];path=parent+"/"+grp["name"]
   for tag,objref in grp["tagrefs"]:
    if tag==HC.DFTAG_VG and objref in groups:descend(objref,path,seen|{ref})
    elif tag==HC.DFTAG_NDG:
     item={"object_kind":"SDS","group_path":path,"ref":objref}
     try:
      obj=sd.select(sd.reftoindex(objref))
      try:
       name,rank,dims,typ,nattrs=obj.info()
       item.update(name=str(name),path=path+"/"+str(name),rank=rank,
                   dims=list(dims) if isinstance(dims,(list,tuple)) else [dims],
                   sd_type=typ,attributes={str(k):js(val) for k,val in obj.attributes().items()})
       try:
        arr=np.asarray(obj.get())
        item["_value"]=arr
        item["num_values"]=int(arr.size)
        item["decoded_dtype"]=str(arr.dtype)
       except Exception as e:item["value_read_failure"]=str(e)[:180]
      finally:obj.endaccess()
     except Exception as e:item["source_read_failure"]=str(e)[:190]
     paths.append(item)
    elif tag==HC.DFTAG_VH:
     item={"object_kind":"Vdata","group_path":path,"ref":objref}
     try:
      vd=vs.attach(objref)
      try:
       rec,inter,fields,size,name=vd.inquire()
       item.update(name=str(name),path=path+"/"+str(name),record_count=rec,fields=str(fields),
                   record_size=size,interlace=inter)
       if rec>0 and rec<=50000:
        try:
         values=vd.read(min(rec,10))
         item["head_records"]=js(values)[:10]
        except Exception as e:item["value_read_failure"]=str(e)[:180]
      finally:vd.detach()
     except Exception as e:item["source_read_failure"]=str(e)[:180]
     paths.append(item)
  for rootgroup in roots:descend(rootgroup,"",set())
  sd.end();vs.end();v.end();h.close()
  archive_file=root/BUNDLE;archive_file.write_bytes(archive)
  with tarfile.open(archive_file,"r:gz") as tf:
   assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts and not m.issym() and not m.islnk() for m in tf.getmembers())
   tf.extractall(root,filter="data")
  install_dir=root/"official";install_dir.mkdir()
  inst=cmd(["bash",str(root/"hdf"/"H4H5-2.2.5-Linux.sh")],cwd=install_dir,input="y\ny\ny\ny\n")
  assert inst.returncode==0,inst.stderr[-300:]
  binaries=[q for q in install_dir.rglob("*") if q.is_file() and "h4toh5" in q.name.lower() and q.suffix not in (".h",".txt",".md",".so",".a")]
  assert binaries
  binary=binaries[0];binary.chmod(binary.stat().st_mode|0o111)
  converted=root/"converted_ipns.h5"
  conversion=cmd([str(binary),str(p),str(converted)])
  R["converter_returncode"]=conversion.returncode
  assert conversion.returncode==0,conversion.stderr[-500:]
  R["format_conversion_executed"]=True
  with h5py.File(converted) as f:
   dest={}
   def read(name,obj):
    if isinstance(obj,h5py.Dataset):
     dest["/"+name]={"dtype":str(obj.dtype),"shape":list(obj.shape),
                     "attrs":{str(k):js(v) for k,v in obj.attrs.items()},
                     "_ds":obj}
   f.visititems(read)
   candidates=[i for i in paths if i.get("name") in ("data","time_of_flight","polar_angle","energy")]
   for src in candidates:
    item={k:v for k,v in src.items() if k not in ("_value","head_records")}
    options=[n for n in dest if n.rsplit("/",1)[-1]==src.get("name")]
    item["basename_candidate_count"]=len(options)
    item["exact_path_found"]=bool(src.get("path") in f and isinstance(f[src["path"]],h5py.Dataset))
    if item["exact_path_found"]:
     d=f[src["path"]];to={"dtype":str(d.dtype),"shape":list(d.shape),
         "attrs":{str(k):js(v) for k,v in d.attrs.items()},"_ds":d}
     item["hdf5_object_address"]=int(h5py.h5o.get_info(d.id).addr)
     item["hdf5_type"]=to["dtype"];item["hdf5_shape"]=to["shape"]
     attrs_old=src.get("attributes",{})
     item["old_units"]=attrs_old.get("units")
     item["new_units"]=to["attrs"].get("units")
     item["unit_value_equal"]=js(item["old_units"])==js(item["new_units"])
     if "_value" in src:
      left=src["_value"];right=np.asarray(to["_ds"][()])
      item["array_shape_equal"]=left.shape==right.shape
      item["array_value_equal"]=bool(np.array_equal(left,right))
      item["old_value_count"]=int(left.size)
      item["old_dtype"]=str(left.dtype)
      item["sample_old"]=[js(z) for z in left.reshape(-1)[:4]]
      item["sample_new"]=[js(z) for z in right.reshape(-1)[:4]]
    R["primary_pairs"].append(item)
   # Repeated HDF4 SDS refs may appear beneath several groups: audit HDF5 aliases
   refpaths={}
   for x in paths:
    if x.get("object_kind")=="SDS" and x.get("path") and x.get("name") in ("data","time_of_flight","polar_angle"):
     refpaths.setdefault(int(x["ref"]),set()).add(x["path"])
   R["source_alias_checks"]=[]
   for src_ref,src_paths in sorted(refpaths.items()):
    if len(src_paths)<2:continue
    ordered=sorted(src_paths)
    available=[p for p in ordered if p in f and isinstance(f[p],h5py.Dataset)]
    object_addrs=[int(h5py.h5o.get_info(f[p].id).addr) for p in available]
    R["source_alias_checks"].append({"source_ref":src_ref,"source_paths":ordered,
        "h5_existing_paths":available,"all_source_paths_exist":len(available)==len(ordered),
        "all_h5_paths_same_object":len(set(object_addrs))==1 if available else None})
  R["source_count"]=len(paths)
  R["source_sds_count"]=sum(i["object_kind"]=="SDS" for i in paths)
  R["source_vdata_count"]=sum(i["object_kind"]=="Vdata" for i in paths)
  R["destination_dataset_count"]=len(dest)
  R["primary_exact_paths"]=sum(i["exact_path_found"] for i in R["primary_pairs"])
  R["primary_numerical_equal"]=sum(i.get("array_value_equal") is True for i in R["primary_pairs"])
  R["primary_numerical_mismatch"]=sum(i.get("array_value_equal") is False for i in R["primary_pairs"])
  R["source_root_examples"]=[{"ref":x,"name":groups[x]["name"],"class":groups[x]["class"]} for x in roots]
  R["original_path_records"]=[{k:v for k,v in i.items() if k not in ("_value",)} for i in paths
                             if i.get("name") in ("data","time_of_flight","polar_angle","energy")][:110]
  print("SUMMARY",json.dumps({k:R[k] for k in ["source_count","source_sds_count","source_vdata_count","destination_dataset_count","primary_exact_paths","primary_numerical_equal","primary_numerical_mismatch","source_root_examples"]}))
  print("PRIMARY_PAIRS",json.dumps(R["primary_pairs"][:26],default=str)[:15000])
  print("ALIAS_AUDIT",json.dumps(R["source_alias_checks"][:14],default=str)[:4500])
finally:
 OUT.write_text(json.dumps(R,indent=2,default=str))
assert R["vendor_checksum_verified"] and R["format_conversion_executed"]
