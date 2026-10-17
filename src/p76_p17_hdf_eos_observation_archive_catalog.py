#!/usr/bin/env python3
from urllib.request import Request,urlopen
from urllib.parse import urljoin,urlsplit
from html.parser import HTMLParser
import hashlib,json
from pathlib import Path
URL="https://hdfeos.org/zoo/Data_Collection/index.php"
class P(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):
  if t=="a":
   h=dict(a).get("href")
   if h:self.links.append(h)
out={"court":"P76_P17_REAL_HDF4_SCIENCE_ARCHIVE_INDEX","source_url":URL,"original_science_bytes_downloaded":False,"science_query_executed":False}
try:
 with urlopen(Request(URL,headers={"User-Agent":"EPISTEME-P76-P17-research"}),timeout=35) as f:
  b=f.read(1000000)
 out["html_sha256"]=hashlib.sha256(b).hexdigest();out["html_bytes"]=len(b)
 a=P();a.feed(b.decode("utf-8","replace"))
 links=[urljoin(URL,h) for h in a.links]
 targets=[u for u in links if any(k in u.lower() for k in ["mod","misr","airs","data_collection","hdf","ftp","nsidc"])]
 out.update(status="CATALOG_RETRIEVED",link_count=len(links),candidate_links=targets[:70])
except Exception as e:out.update(status="CATALOG_FETCH_FAIL",error=str(e))
Path("p76_p17_hdf_science_archive_index.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
