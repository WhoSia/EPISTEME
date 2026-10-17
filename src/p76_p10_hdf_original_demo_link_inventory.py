#!/usr/bin/env python3
"""Read-only inventory of HDFGroup original HDF4/HDF5 demo links on a clean runner.
Not a conversion experiment: don't equate URL availability with data correctness.
"""
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.parse import urljoin, urlsplit, unquote
import json
from pathlib import Path
import hashlib

URL="https://hdfdap.hdfgroup.org/zoo/h4toh5/h4toh5-def-demo.php"
ALLOWED={"hdfdap.hdfgroup.org"}
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    all_links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            href=dict(attrs).get("href")
            if href: self.links.append(href)
def go():
    with urlopen(Request(URL,headers={"User-Agent":"EPISTEME-P76-source-custody/1.0"}),timeout=35) as f:
        raw=f.read(1500000)
    h=hashlib.sha256(raw).hexdigest()
    p=Links();p.feed(raw.decode("utf-8","replace"))
    links=[]
    for href in p.links:
        u=urljoin(URL,href)
        parsed=urlsplit(u)
        if parsed.scheme not in ("http","https") or parsed.hostname not in ALLOWED: continue
        path=unquote(parsed.path).lower()
        all_links.append({"url":u,"href":href})
        if any(ext in path for ext in (".hdf",".h5",".he5",".nc",".zip",".gz",".cdl",".odl")):
            links.append({"url":u,"type":"hdf_source" if ".hdf" in path else "converted_or_document"})
    unique={i["url"]:i for i in links}
    report={"court":"P76_P10_ORIGINAL_DEMO_INDEX","source_url":URL,"index_sha256":h,
     "index_bytes":len(raw),"relevant_links":list(unique.values())[:150],
     "all_relevant_url_count":len(unique),"all_same_host_links":all_links[:250],"original_hdf_bytes_downloaded":False,
     "converter_executed":False,"source_query_result":None,"novel_mechanism_proved":False}
    Path("p76_p10_original_link_inventory.json").write_text(json.dumps(report,indent=2))
    print(json.dumps({"court":report["court"],"index_sha256":h,
      "relevant_url_count":len(unique),"sample":list(unique)[:8]},indent=2))
    assert len(all_links)>=5, "Official HTML has no usable same-domain links"
if __name__=="__main__":go()
