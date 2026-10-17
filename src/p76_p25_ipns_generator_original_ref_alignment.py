#!/usr/bin/env python3
"""P76-P25: original HDF4 identity observations vs historical NXlrcs source generator.
The generator is an EXPLANATORY source, not proven exact binary/commit for run 3701.
"""
import hashlib, json, re, subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import urlopen, Request
import pyhdf.V, pyhdf.VS
from pyhdf.HDF import HDF, HC
from pyhdf.SD import SD, SDC
import numpy as np

UPSTREAM = "eae516807ef7e27d1c45aab3af3a64a679154677"
SOURCE = "IPNS/LRMECS/hdf4/lrcs3701.nxs"
EXPECTED = "8b1dbf4f02b2f7c35c8cecebda3bfd903c32c4ecfd00b2fd105bdb0f6c668d39"
GENERATOR = "https://www.nexusformat.org/NXlrcs.f90.html"
OUT = Path("p76_p25_original_generator_alignment.json")

class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)

def retrieve(url, cap=600000):
    with urlopen(Request(url, headers={"User-Agent":"EPISTEME-P76-P25-source-audit"}),timeout=35) as f:
        body=f.read(cap+1)
    if len(body)>cap:
        raise ValueError("Source size cap exceeded")
    return body

report = {"court":"P76_P25_SOURCE_GENERATION_PROVENANCE",
    "source_sha256":EXPECTED,
    "source_origin":"nexusformat/exampledata original HDF4 instrument file",
    "generator_reference":GENERATOR,
    "generator_exact_binary_that_produced_record":False,
    "monitor_normalization_policy_identified":False,
    "physical_acquisition_independence_identified":False,
    "P77_independent_object_identified":False}
try:
    raw=retrieve(f"https://raw.githubusercontent.com/nexusformat/exampledata/{UPSTREAM}/{SOURCE}",180000)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED
    assert raw[:4] == bytes.fromhex("0e031301")
    gen=retrieve(GENERATOR,350000)
    parser=PageText();parser.feed(gen.decode("utf-8","replace"))
    txt="".join(parser.parts)
    lo=txt.find("program NXlrcs")
    hi=txt.find("end program NXlrcs", max(lo,0))
    code_only=txt[lo:hi+len("end program NXlrcs")] if lo>=0 and hi>=lo else txt
    compact=" ".join(code_only.split())
    gen_claims={
        "loop_histograms": bool(re.search(r"do\s+i\s*=\s*1\s*,\s*Nhist",compact,re.I)),
        "source_PLS_read": 'get_IPNS_item ("PLS", int_value)' in compact,
        "per_hist_proton_write": 'NXUwritedata (file_id, "proton_pulses", int_value)' in compact,
        "monitor1_alias": 'NXmakelink (file_id, M1_id)' in compact,
        "monitor2_alias": 'NXmakelink (file_id, M2_id)' in compact,
        "monitor1_first_write": 'NXUwritegroup (file_id, "monitor1", "NXmonitor")' in compact,
        "monitor2_first_write": 'NXUwritegroup (file_id, "monitor2", "NXmonitor")' in compact,
        "no_explicit_monitor_division_found": not bool(re.search(r"normali[sz]|counts\s*/\s*monitor|ratio",compact,re.I))
    }
    report["generator_source_excerpt"]=compact[compact.find("NXmakelink")-100:compact.find("NXmakelink")+100] if "NXmakelink" in compact else compact[:500]
    report["generator_html_sha256"]=hashlib.sha256(gen).hexdigest()
    report["generator_code_claims"]=gen_claims
    if not all(value for key,value in gen_claims.items() if key != "no_explicit_monitor_division_found"):
        raise AssertionError(f"Public generator code changed/missing statements: {gen_claims}")
    fpath=Path("p76_p25_lrcs3701.nxs");fpath.write_bytes(raw)
    try:
        h=HDF(str(fpath),HC.READ);v=h.vgstart();sd=SD(str(fpath),SDC.READ)
        groups={};ref=-1
        while True:
            try:ref=v.getid(ref)
            except Exception:break
            obj=v.attach(ref)
            try:groups[ref]={"name":str(obj._name),"tagrefs":list(obj.tagrefs())}
            finally:obj.detach()
        referenced={r for g in groups.values() for tag,r in g["tagrefs"] if tag==HC.DFTAG_VG}
        roots=sorted(set(groups)-referenced)
        group_paths={};sds_paths={}
        def walk(ref,prefix,seen):
            if ref in seen:return
            g=groups[ref];path=prefix+"/"+g["name"]
            group_paths[path]=ref
            for tag,child in g["tagrefs"]:
                if tag==HC.DFTAG_VG and child in groups:
                    walk(child,path,seen|{ref})
                if tag==HC.DFTAG_NDG:
                    o=sd.select(sd.reftoindex(child))
                    try:
                        name=o.info()[0]
                        val=np.asarray(o.get())
                        sds_paths[path+"/"+name]={"ref":int(child),
                            "shape":list(val.shape),"value":val.reshape(-1).tolist()[:8]}
                    finally:o.endaccess()
        for root in roots:walk(root,"",set())
        observations=[]
        for i in (1,2):
            p="/Histogram"+str(i)
            item={"histogram":i}
            for m in ("monitor1","monitor2"):
                path=p+"/"+m
                item[m+"_group_ref"]=group_paths.get(path)
                item[m+"_data"]=sds_paths.get(path+"/data")
            item["proton"]=sds_paths.get(p+"/LRMECS/source/proton_pulses")
            item["run"]=sds_paths.get(p+"/run_number")
            observations.append(item)
        report["observations"]=observations
        assert all(o["proton"] is not None and o["run"] is not None for o in observations)
        assert all(o["monitor1_group_ref"] is not None and o["monitor2_group_ref"] is not None for o in observations)
        assert observations[0]["monitor1_group_ref"]==observations[1]["monitor1_group_ref"]
        assert observations[0]["monitor2_group_ref"]==observations[1]["monitor2_group_ref"]
        assert observations[0]["proton"]["ref"]!=observations[1]["proton"]["ref"]
        assert observations[0]["proton"]["value"]==observations[1]["proton"]["value"]==[2268088]
        assert observations[0]["run"]["value"]==observations[1]["run"]["value"]==[3701]
        report["generator_pattern_explains_observed_storage_structure"]=True
        report["source_time_series_or_charge_calibration_source_found"]=False
    finally:
        if "sd" in locals(): sd.end()
        if "v" in locals(): v.end()
        if "h" in locals(): h.close()
        fpath.unlink(missing_ok=True)
finally:
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
