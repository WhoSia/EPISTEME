#!/usr/bin/env python3
"""P76-P24: old mixed SDS/Vdata/Vgroup exact-path vs vendor-HDF5 values, conservative mapping."""
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
R={"court":"P76_P24_ACQUISITION_CONTRACT_AUDIT","original_sha":SRC_SHA,"source_pin":PIN,
   "primary_pairs":[],"original_path_records":[],"vendor_checksum_verified":False,
   "format_conversion_executed":False,"historical_institution_adoption_established":False,"P77_independent_novelty":False}
OUT=Path("p76_p24_acquisition_unit_inventory.json")
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
  # P24: exhaustive acquisition-condition candidates in original scientific NXentry paths
  acquisition_terms=("proton_pulses","integral","nominal","preset","start_time","end_time",
    "run_number","mode","duration","exposure","monitor","live_time","charge","frequency")
  acq=[]
  for obj in paths:
   pth=obj.get("path","")
   if not pth.startswith(("/Histogram1/","/Histogram2/")):continue
   field=str(obj.get("name","")).lower()
   if not any(k in field or k in pth.lower() for k in acquisition_terms):continue
   rec={k:val for k,val in obj.items() if k not in ("_value","head_records")}
   if "_value" in obj:
    arr=np.asarray(obj["_value"])
    rec["old_values_preview"]=js(arr.reshape(-1)[:12])
    rec["old_array_n"]=int(arr.size)
    if np.issubdtype(arr.dtype,np.number):
     rec["old_sum"]=float(np.sum(arr,dtype=np.float64))
    rec["old_values_sha256"]=hashlib.sha256(np.ascontiguousarray(arr).tobytes()).hexdigest()
   if "head_records" in obj: rec["vdata_head_records"]=obj["head_records"][:4]
   acq.append(rec)
  R["p24_original_exposure_candidates"]=acq
  R["p24_source_exposure_name_counts"]=dict(Counter(x.get("name","") for x in acq))

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

   # All checks below use original NXentry source paths, not generated CDF0.0 index vgroups.
   R["nxentry_alias_audit"]=[]
   for x in R["source_alias_checks"]:
    relevant=[q for q in x["source_paths"] if q.startswith("/Histogram1/") or q.startswith("/Histogram2/")]
    available=[q for q in relevant if q in f and isinstance(f[q],h5py.Dataset)]
    addrs=[int(h5py.h5o.get_info(f[q].id).addr) for q in available]
    R["nxentry_alias_audit"].append({"source_ref":x["source_ref"],"nxentry_paths":relevant,
          "existing_h5_paths":available,"all_exist":len(available)==len(relevant),
          "same_hdf5_object":bool(addrs) and len(set(addrs))==1})
   R["histogram_queries"]=[]
   for hist in ("Histogram1","Histogram2"):
    base="/"+hist+"/data/"
    old={}
    for name in ("data","time_of_flight","polar_angle"):
     matches=[p for p in paths if p.get("path")==base+name and "_value" in p]
     assert len(matches)==1,(base,name,len(matches))
     old[name]=matches[0]
    def summary(values,dt,axis,attrs):
     assert values.ndim==2 and axis.ndim==1 and dt.ndim==1
     valid=(axis.size==values.shape[1]+1 and dt.size==values.shape[0])
     if not valid:return {"bin_axis_compatible":False}
     n=int(np.sum(values,dtype=np.int64))
     centers=(axis[:-1].astype(np.float64)+axis[1:].astype(np.float64))/2.
     intensity=np.asarray(values,dtype=np.float64).sum(axis=0)
     weighted=float(np.dot(intensity,centers)/n) if n else None
     rows=values.sum(axis=1,dtype=np.int64)
     first=int(next((i for i,x in enumerate(rows) if x!=0),0))
     return {"bin_axis_compatible":True,"shape":list(values.shape),"sum_counts":n,
       "angle_count":int(dt.size),"time_bin_count":int(values.shape[1]),
       "time_edge_count":int(axis.size),"mean_count_weighted_tof_microseconds":weighted,
       "first_nonzero_angle_index":first,"first_nonzero_angle_degrees":float(dt[first]),
       "first_nonzero_angle_counts":int(rows[first]),
       "row_sums_sha256":hashlib.sha256(np.asarray(rows,dtype="<i8").tobytes()).hexdigest(),
       "data_axes_attribute":js(attrs.get("axes")),"data_signal_attribute":js(attrs.get("signal")),
       "counts_units":js(attrs.get("units"))}
    origin=summary(old["data"]["_value"],old["polar_angle"]["_value"],old["time_of_flight"]["_value"],old["data"].get("attributes",{}))
    newobjects=[f[base+n] if base+n in f else None for n in ("data","time_of_flight","polar_angle")]
    assert all(isinstance(a,h5py.Dataset) for a in newobjects)
    newdata,newtime,newangle=newobjects
    new=summary(np.asarray(newdata[()]),np.asarray(newangle[()]),np.asarray(newtime[()]),
       {str(k):js(val) for k,val in newdata.attrs.items()})
    fieldchecks={}
    for name,obj in zip(("data","time_of_flight","polar_angle"),newobjects):
     ox=old[name]
     fieldchecks[name]={"elementwise_equal":bool(np.array_equal(ox["_value"],np.asarray(obj[()]))),
        "source_units":js(ox["attributes"].get("units")),
        "new_units":js(obj.attrs.get("units")) if "units" in obj.attrs else None,
        "unit_equal":js(ox["attributes"].get("units"))==(js(obj.attrs.get("units")) if "units" in obj.attrs else None)}
    R["histogram_queries"].append({"entry":hist,"original":origin,"converted":new,
       "source_to_converted_scientific_query_equal":origin==new,"per_dataset_checks":fieldchecks})

   # P24 native acquisition record-to-vendor exact path and value check; no inferred normalization.
   R["p24_exposure_path_correspondence"]=[]
   for original in R["p24_original_exposure_candidates"]:
    pth=original.get("path","")
    rec={"source_path":pth,"original_kind":original.get("object_kind"),
      "original_ref":original.get("ref"),"original_name":original.get("name"),
      "source_record_count":original.get("record_count"),
      "source_fields":original.get("fields"),"old_preview":original.get("old_values_preview"),
      "old_vdata_head":original.get("vdata_head_records"),
      "source_attrs":original.get("attributes",{})}
    if pth in f and isinstance(f[pth],h5py.Dataset):
     d=f[pth];val=np.asarray(d[()])
     rec["h5_path_found"]=True;rec["h5_type"]=str(d.dtype);rec["h5_shape"]=list(d.shape)
     rec["h5_preview"]=js(val.reshape(-1)[:12]);rec["h5_attrs"]={str(k):js(z) for k,z in d.attrs.items()}
     rec["h5_obj_addr"]=int(h5py.h5o.get_info(d.id).addr)
     if original.get("original_kind")=="SDS" and "old_values_sha256" in original:
      match=[x for x in paths if x.get("path")==pth and x.get("object_kind")=="SDS" and "_value" in x]
      if len(match)==1:rec["old_new_elementwise_equal"]=bool(np.array_equal(match[0]["_value"],val))
    else:rec["h5_path_found"]=False
    R["p24_exposure_path_correspondence"].append(rec)
   R["p24_monitor_acquisition_context"]=[]
   for name in ("Histogram1","Histogram2"):
    related=[x for x in R["p24_exposure_path_correspondence"] if x["source_path"].startswith("/"+name+"/")]
    R["p24_monitor_acquisition_context"].append({"entry":name,
      "source_target_paths":len(related),
      "source_field_names":sorted(set(x.get("original_name","") for x in related)),
      "source_refs_for_proton_pulses":[x["original_ref"] for x in related if x.get("original_name")=="proton_pulses"],
      "monitor_integral_candidates":[x["source_path"] for x in related if x.get("original_name") in ("integral","nominal","preset")],
      "entry_start_end_candidates":[x["source_path"] for x in related if x.get("original_name") in ("start_time","end_time","run_number")]})
   R["p24_physical_normalization_certified"]=False
   R["p24_acquisition_independence_certified"]=False
   R["p24_distinct_p77_science_object_identified"]=False
   print("P24_EXPOSURE_INVENTORY",json.dumps(R["p24_exposure_path_correspondence"],default=str)[:24000])
   print("P24_ACQUISITION_CONTEXT",json.dumps(R["p24_monitor_acquisition_context"],default=str)[:3000])

   # P23 - actual shared monitor object versus repeated path incidence
   R["p23_monitor_identity"]=[]
   monitor_paths=[]
   for name in ("monitor1","monitor2"):
    per=[]
    for hname in ("Histogram1","Histogram2"):
     pth="/"+hname+"/"+name+"/data"
     match=[z for z in paths if z.get("object_kind")=="SDS" and z.get("path")==pth]
     record={"path":pth,"source_match_count":len(match)}
     if len(match)==1:
      old=match[0]
      record["source_ref"]=int(old["ref"])
      record["old_attrs"]=old.get("attributes",{})
      record["old_shape"]=list(old["_value"].shape) if "_value" in old else None
      if "_value" in old:
       record["old_sum"]=float(np.asarray(old["_value"],dtype=np.float64).sum())
       record["old_content_sha256"]=hashlib.sha256(np.ascontiguousarray(old["_value"]).tobytes()).hexdigest()
      if pth in f and isinstance(f[pth],h5py.Dataset):
       new_ds=f[pth]
       record["converted_object_address"]=int(h5py.h5o.get_info(new_ds.id).addr)
       record["converted_shape"]=list(new_ds.shape)
       record["converted_attrs"]={str(k):js(val) for k,val in new_ds.attrs.items()}
       if "_value" in old:
        vals=np.asarray(new_ds[()])
        record["old_vendor_elementwise_equal"]=bool(np.array_equal(vals,old["_value"]))
        record["converted_sum"]=float(np.asarray(vals,dtype=np.float64).sum())
     per.append(record)
     monitor_paths.append(record)
    if len(per)==2:
     ident={"monitor":name,"path_count":2,"paths":per,
       "source_same_ref":(per[0].get("source_ref")==per[1].get("source_ref") and "source_ref" in per[0]),
       "converted_same_object":(per[0].get("converted_object_address")==per[1].get("converted_object_address") and "converted_object_address" in per[0]),
       "old_array_equal":(per[0].get("old_content_sha256")==per[1].get("old_content_sha256") and "old_content_sha256" in per[0])}
     R["p23_monitor_identity"].append(ident)
   src_refs=[x["source_ref"] for x in monitor_paths if "source_ref" in x]
   unique_ref_values={}
   for x in monitor_paths:
    if "source_ref" in x and "old_sum" in x:
     unique_ref_values.setdefault(x["source_ref"],x["old_sum"])
   R["p23_path_vs_source_reference"]={
     "total_monitor_data_paths":len(monitor_paths),
     "source_paths_resolved":len(src_refs),
     "unique_source_data_references":len(set(src_refs)),
     "path_multiplicity":(len(src_refs)/len(set(src_refs))) if src_refs else None,
     "naive_path_sum":sum(x.get("old_sum",0.) for x in monitor_paths),
     "unique_ref_sum":sum(unique_ref_values.values()),
     "naive_to_unique_ratio":sum(x.get("old_sum",0.) for x in monitor_paths)/sum(unique_ref_values.values()) if sum(unique_ref_values.values()) else None,
     "interpretation":"Illustrative path-count aggregation only; NOT an exposure-correct neutron normalization estimator, NO statistical independence inference."
   }
   assert len(R["p23_monitor_identity"])==2,"Need two monitor types"
   assert all(x["source_same_ref"] and x["converted_same_object"] and x["old_array_equal"] for x in R["p23_monitor_identity"]),"Expected shared source monitor identity"
   assert all(all(y.get("old_vendor_elementwise_equal") is True for y in x["paths"]) for x in R["p23_monitor_identity"]),"Monitor measurements not fidelity-preserved"
   R["p23_inference_caution"]={
     "alias_induced_duplicate_count_verified":True,
     "independent_experimental_exposures_verified":False,
     "monitor_normalization_estimator_validated":False,
     "statistical_significance_change_verified":False,
     "p77_novelty_survived_prior_art":False
   }
   print("P23_MONITOR_AUDIT",json.dumps(R["p23_monitor_identity"],default=str)[:10500])
   print("P23_ALIAS_DUPLICATION",json.dumps(R["p23_path_vs_source_reference"],default=str))
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
  print("ALIAS_AUDIT",json.dumps(R["nxentry_alias_audit"][:14],default=str)[:4500])
  print("HISTOGRAM_SCIENCE_QUERIES",json.dumps(R["histogram_queries"],default=str)[:6500])
finally:
 OUT.write_text(json.dumps(R,indent=2,default=str))
assert R["vendor_checksum_verified"] and R["format_conversion_executed"]
