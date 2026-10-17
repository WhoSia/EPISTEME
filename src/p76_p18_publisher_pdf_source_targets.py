#!/usr/bin/env python3
"""P76-P18: publisher PDF link-target custody audit; no assumption about source access."""
import json,hashlib,io
from pathlib import Path
from urllib.request import urlopen,Request
import fitz
U="https://hdfeos.org/zoo/Data_Collection/LAADS_MOD.pdf"
r={"stage":"P76-P18","original_HDF_bytes_obtained":False,"science_query_executed":False,"source_pdf":U}
try:
 with urlopen(Request(U,headers={"User-Agent":"EPISTEME-P76-science-source-audit"}),timeout=30) as f:b=f.read(7000000)
 r["pdf_sha256"]=hashlib.sha256(b).hexdigest()
 doc=fitz.open(stream=b,filetype="pdf")
 candidates=[]
 for page_index,page in enumerate(doc):
  for l in page.get_links():
   u=l.get("uri","")
   if u:candidates.append({"page":page_index+1,"url":u})
 r["pdf_link_count"]=len(candidates)
 r["file_or_ftp_links"]=[x for x in candidates if ".hdf" in x["url"].lower() or "ftp" in x["url"].lower()][:80]
 r["status"]="PDF_LINKS_RETRIEVED"
except Exception as e:r.update(status="FAIL",error=type(e).__name__+": "+str(e))
Path("p76_p18_publisher_source_targets.json").write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
