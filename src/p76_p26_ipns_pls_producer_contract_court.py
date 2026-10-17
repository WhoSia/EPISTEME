#!/usr/bin/env python3
"""EPISTEME P76-P26: original NeXus source, producer-source fidelity, conditional exposure audit.
Read-only source-only job. No physical normalization asserted.
"""
import hashlib,json,re,tempfile
from pathlib import Path
from datetime import datetime
from urllib.request import Request,urlopen
import numpy as np
import pyhdf.V
from pyhdf.HDF import HDF,HC
from pyhdf.SD import SD,SDC

SRC_PIN="eae516807ef7e27d1c45aab3af3a64a679154677"
SRC="IPNS/LRMECS/hdf4/lrcs3701.nxs"
SRC_SHA="8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39"
GEN_PIN="ca703eda4dd2ca7fe3460011206fe90eef752179"
GEN_PATH="source/content/NXlrcs.f90.md"
OUT=Path("p76_p26_producer_contract_and_exposure_audit.json")
def pull(u,limit):
 with urlopen(Request(u,headers={"User-Agent":"EPISTEME-P76-P26-lrmecs-producer"}),timeout=35) as f:
  b=f.read(limit+1)
 assert len(b)<=limit,(u,len(b))
 return b
def decoded(v):
 a=np.asarray(v).ravel()
 if a.dtype.kind in "iub" and 8<=a.size<256 and np.all((a>=0)&(a<128)):
  s="".join(chr(int(x)) for x in a)
  return s.rstrip("\x00 ")
 if a.dtype.kind in "SU":
  return "".join(str(x.decode() if isinstance(x,bytes) else x) for x in a).rstrip("\x00 ")
 if a.size==1:
  x=a[0];return x.item() if hasattr(x,"item") else x
 return {"length":int(a.size),"dtype":str(a.dtype)}
R={"court":"P76_P26_SOURCE_ACQUISITION_CONTRACT","source_pin":SRC_PIN,"source_sha256":SRC_SHA,
   "historical_generator_was_exact_binary":False,"PLS_physical_normalization_defined":False,
   "beam_monitor_gate_identified":False,"P77_independent_result":False}
try:
 raw=pull(f"https://raw.githubusercontent.com/nexusformat/exampledata/{SRC_PIN}/{SRC}",180000)
 assert hashlib.sha256(raw).hexdigest()==SRC_SHA and raw[:4]==bytes.fromhex("0e031301")
 gen=pull(f"https://raw.githubusercontent.com/nexusformat/wiki/{GEN_PIN}/{GEN_PATH}",100000)
 g=gen.decode("utf8","replace")
 R["generator_markdown_sha256"]=hashlib.sha256(gen).hexdigest()
 R["generator_repo_commit"]=GEN_PIN
 R["generator_verbatim_snippets"]={}
 for key,fragment in {"PLS_source":'get_IPNS_item ("PLS", int_value)',
  "write_pulses":'NXUwritedata (file_id, "proton_pulses", int_value)',
  "source_nominal_frequency":'NXUwritedata (file_id, "frequency", 30.0, "Hz")',
  "monitor_alias":'NXmakelink (file_id, M1_id)',
  "monitor2_alias":'NXmakelink (file_id, M2_id)'}.items():
  R["generator_verbatim_snippets"][key]=fragment in g
 assert all(R["generator_verbatim_snippets"].values())
 # No embedded IPNS module definition in the primary public generator file
 R["generator_is_call_site_only_for_PLS"]=not bool(re.search(r"(?im)^\s*module\s+IPNS_module\b",g))
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/"lrcs3701.nxs";p.write_bytes(raw)
  h=HDF(str(p),HC.READ);v=h.vgstart();sd=SD(str(p),SDC.READ)
  try:
   groups={};ref=-1
   while True:
    try:ref=v.getid(ref)
    except Exception:break
    z=v.attach(ref)
    try:groups[ref]={"name":str(z._name),"members":list(z.tagrefs())}
    finally:z.detach()
   children={ref for d in groups.values() for tag,ref in d["members"] if tag==HC.DFTAG_VG}
   roots=sorted(set(groups)-children)
   names={"proton_pulses","frequency","start_time","end_time","run_number",
          "count_time","current","charge","integral","nominal","preset"}
   found={}
   def visit(ref,parent,visited):
    if ref in visited:return
    obj=groups[ref];here=parent+"/"+obj["name"]
    for tag,r in obj["members"]:
     if tag==HC.DFTAG_VG and r in groups:visit(r,here,visited|{ref})
     elif tag==HC.DFTAG_NDG:
      a=sd.select(sd.reftoindex(r))
      try:
       n=a.info()[0]
       if n in names and here.startswith(("/Histogram1/","/Histogram2/")):
        try: val=decoded(a.get())
        except Exception as e:val={"read_error":str(e)[:120]}
        found[here+"/"+n]={"ref":int(r),"value":val,
           "attrs":{str(k):str(y) for k,y in a.attributes().items()}}
      finally:a.endaccess()
   for root in roots:visit(root,"",set())
   R["native_acquisition_fields"]=found
  finally:sd.end();v.end();h.close()
 def val(hist,name):
  v=[d for k,d in R["native_acquisition_fields"].items() if k.startswith("/"+hist+"/") and k.endswith("/"+name)]
  return v[0]["value"] if len(v)==1 else None
 rows=[]
 for hist in ("Histogram1","Histogram2"):
  st,en,pl,freq=val(hist,"start_time"),val(hist,"end_time"),val(hist,"proton_pulses"),val(hist,"frequency")
  q={"histogram":hist,"start":st,"end":en,"stored_pulses":pl,"source_frequency_Hz":freq}
  try:
   t=(datetime.strptime(en,"%Y-%m-%dT%H:%M:%S%z")-datetime.strptime(st,"%Y-%m-%dT%H:%M:%S%z")).total_seconds()
   q["timestamp_interval_seconds"]=t
   q["pulses_per_wall_second"]=pl/t
   # 30 Hz is from public generator source. It is a conditional illustrative nominal rate,
   # not the measured 2001 accelerator frequency or a physical uptime estimate.
   q["conditional_if_30Hz_all_walltime_pulses"]=t*30
   q["conditional_stored_to_nominal_walltime_ratio"]=pl/(t*30)
   q["this_is_NOT_beam_on_fraction_or_physics_normalization"]=True
  except Exception as e:q["interval_error"]=str(e)[:150]
  rows.append(q)
 R["histograms"]=rows
 assert len(rows)==2 and all(row.get("stored_pulses")==2268088 and row.get("timestamp_interval_seconds",0)>190000 for row in rows)
 assert rows[0]["stored_pulses"]==rows[1]["stored_pulses"]
 R["physical_inference_allowed"]=False
 R["final_status"]="PRODUCER_CALL_SITE_PASS_PHYSICAL_CONTRACT_HOLD"
finally:
 OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str))
 print(json.dumps(R,ensure_ascii=False,indent=2,default=str))
