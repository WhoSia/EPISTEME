#!/usr/bin/env python3
"""P76-P16 NSIDC original research sample archive source-custody preflight.
This lists original records only; no byte download or scientific query comparison.
"""
from urllib.request import urlopen,Request
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit
from pathlib import Path
import hashlib,json
URL="https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0397_HDF4_Sampler_v01/"
class A(HTMLParser):
 def __init__(self):super().__init__();self.hrefs=[]
 def handle_starttag(self,tag,attrs):
  if tag=="a":
   u=dict(attrs).get("href")
   if u:self.hrefs.append(u)
receipt={"court":"P76_P16_NSIDC_0397_REAL_DATA_INDEX","catalog_url":URL,
         "sample_bytes_downloaded":False,"scientific_queries_executed":False,
         "format_migration_test_executed":False,"original_sample_sha_verified":False}
try:
 req=Request(URL,headers={"User-Agent":"EPISTEME-P76-P16-research-source-index"})
 with urlopen(req,timeout=35) as f:
  body=f.read(1500000);receipt["http_status"]=f.status
 receipt["html_sha256"]=hashlib.sha256(body).hexdigest()
 receipt["html_length"]=len(body)
 a=A();a.feed(body.decode("utf-8","replace"))
 links=[]
 for href in a.hrefs:
  u=urljoin(URL,href);p=urlsplit(u)
  if p.hostname!="daacdata.apps.nsidc.org" or not p.path.startswith("/pub/DATASETS/nsidc0397_HDF4_Sampler_v01/"):continue
  links.append(u)
 receipt["entry_count"]=len(links)
 receipt["sample_entries"]=links[:100]
 receipt["status"]="INDEX_RETRIEVED"
except Exception as e:
 receipt["status"]="INDEX_FETCH_FAIL"
 receipt["error"]=type(e).__name__+":"+str(e)[:500]
finally:
 Path("p76_p16_nsidc0397_index.json").write_text(json.dumps(receipt,indent=2))
 print(json.dumps(receipt,indent=2))
