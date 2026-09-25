from __future__ import annotations
import json,os
from pathlib import Path
from groq import Groq

client=Groq(api_key=os.environ["GROQ_API_KEY"],max_retries=0)
rows=[]
for m in client.models.list().data:
    d=m.model_dump() if hasattr(m,"model_dump") else {"id":m.id}
    rows.append(d)
rows=sorted(rows,key=lambda x:x.get("id",""))
out={"stage":"EPISTEME-P40","phase":"provider-census","provider":"groq","models":rows}
p=Path("receipts/p40_groq_model_census.json")
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(out,indent=2),encoding="utf-8")
