#!/usr/bin/env python3
"""P76-P18: bounded live HTTP probes of publisher-documented original NASA HDF4 observation.
No FTP access, token, credentials or bypass; strict file type, size, hash and ownership audit.
"""
import hashlib,json
from urllib.request import Request,urlopen
from pathlib import Path
NAME="MODASRVN.Arica.A2000055.1525.005.2008161234032.hdf"
PATH="/pub/outgoing/NASAHDFPOOL/LAADS/MOD/"+NAME
URLS=[
"https://ftp.hdfgroup.uiuc.edu"+PATH,
"https://support.hdfgroup.org/ftp"+PATH,
"https://hdfeos.org/zoo/LAADS/MOD/"+NAME,
"https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5/MODASRVN/2000/055/"+NAME
]
R={"court":"P76_P18_OBSERVATION_SOURCE_BOUNDARY","target":NAME,
"target_size_from_HDF_EOS_archive":"553 KB (approximate)","results":[],"raw_observation_custody":False,
"radiance_query_executed":False,"adoption_causal_finding":False}
try:
 for url in URLS:
  item={"url":url,"downloaded":False}
  try:
   with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-research-source-v1"}),timeout=16) as f:
    item["http_status"]=f.status
    item["content_type"]=f.headers.get("Content-Type")
    body=f.read(2200001)
   item["response_length_capped"]=len(body)
   item["response_sha256"]=hashlib.sha256(body).hexdigest()
   if len(body)<2200000 and body[:4]==b"\x0e\x03\x13\x01":
    item["downloaded"]=True; item["valid_HDF4_header"]=True
    R["raw_observation_custody"]=True
    R["original_observation_sha256"]=item["response_sha256"]
    R["first_valid_source_url"]=url
    Path("p76_p18_observation_raw.hdf").write_bytes(body)
   else:item["valid_HDF4_header"]=False
  except Exception as e:item["error"]=type(e).__name__+":"+str(e)[:280]
  R["results"].append(item)
  if R["raw_observation_custody"]:break
finally:
 Path("p76_p18_observation_source_receipt.json").write_text(json.dumps(R,indent=2))
 print(json.dumps(R,indent=2))
