"""P76 P11: authentic HDF4 original vs h5utils HDF5 conversion numeric query.
h5fromh4 is third-party, NOT HDFGroup h4toh5; conclusions route-specific.
"""
import hashlib,json,subprocess,re
from pathlib import Path
from urllib.request import urlopen,Request
import numpy as np
import h5py
PIN="2c46ad56bea5aab05e996e473a81dcbd9a66b125"
ROOT=f"https://raw.githubusercontent.com/HDFGroup/hdf4/{PIN}/"
INPUTS=[("mfhdf/hdfimport/SDSfloat2.hdf","3ba791239a5874bf9d97e1765a3e2896dbe965680b7fee59f9cc96afefb28b38"),("mfhdf/hdp/testfiles/sds_compressed.hdf","bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb")]
out=[]
for path,want in INPUTS:
    b=urlopen(Request(ROOT+path,headers={"User-Agent":"EPISTEME-P76-P11"}),timeout=30).read()
    got=hashlib.sha256(b).hexdigest()
    assert got==want,(path,got,want)
    src=Path(path).name;Path(src).write_bytes(b)
    native=subprocess.run(["hdp","dumpsds",src],capture_output=True,text=True,timeout=30)
    assert native.returncode==0,(src,native.stderr)
    txt=native.stdout
    rank=re.search(r"Rank\s*=\s*(\d+)",txt)
    dims=[int(v) for v in re.findall(r"\bSize\s*=\s*(\d+)",txt)]
    assert rank and len(dims)>=int(rank.group(1)),(src,dims,rank.group(1) if rank else "none")
    dims=dims[:int(rank.group(1))]
    assert "Data :" in txt,txt[:500]
    value_text=txt.split("Data :",1)[1]
    numbers=[float(v) for v in re.findall(r"(?<![a-zA-Z])[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?",value_text)]
    assert len(numbers)>=int(np.prod(dims)),(src,len(numbers),dims,txt[-500:])
    old=np.asarray(numbers[:int(np.prod(dims))]).reshape(dims)
    proc=subprocess.run(["h5fromh4", "-o",src+".h5",src],capture_output=True,text=True,timeout=45)
    desc={"source":path,"sha256":got,"nbytes":len(b),"converter":"h5fromh4 (h5utils, not HDFGroup h4toh5)","exit":proc.returncode,"stderr":proc.stderr[:400],"native_reader":"hdp dumpsds","original_datasets":["original SDS read via hdp"]}
    if proc.returncode!=0:
        desc["verification_status"]="CONVERTER_INPUT_READ_FAILURE"
        desc["source_hdp_reader_success"]=True
        desc["new_hdf5_query_untested"]=True
        out.append(desc)
        continue
    with h5py.File(src+".h5","r") as h5:
        dsets={}
        def visit(name,obj):
            if isinstance(obj,h5py.Dataset):dsets[name]=np.asarray(obj[()])
        h5.visititems(visit)
    assert len(dsets)==1,dsets.keys()
    new=next(iter(dsets.values()))
    desc.update({"converted_datasets":list(dsets),"original_shape":list(old.shape),"converted_shape":list(new.shape),
      "original_dtype":"numeric values parsed from hdp; original type from hdp metadata","converted_dtype":str(new.dtype),"elementwise_equal":bool(np.array_equal(old,new)),
      "old_sum":float(np.asarray(old,dtype=np.float64).sum()),"new_sum":float(np.asarray(new,dtype=np.float64).sum())})
    desc["verification_status"]="QUERY_PRESERVED" if (desc["elementwise_equal"] and desc["original_shape"]==desc["converted_shape"]) else "CONVERSION_QUERY_MISMATCH"
    out.append(desc)
r={"source_commit":PIN,"fixtures":out,"verified_numeric_query_count":sum(x.get("verification_status")=="QUERY_PRESERVED" for x in out),"conversion_failed_count":sum(x.get("verification_status")=="CONVERTER_INPUT_READ_FAILURE" for x in out),
 "route":"h5utils third-party h5fromh4","official_h4toh5_used":False,
 "scientific_meaning_fully_preserved":None,"irreversible_loss_proved":False,
 "new_P76_theorem":False}
assert len(out)==len(INPUTS) and sum(x.get("verification_status")=="QUERY_PRESERVED" for x in out)>=1
Path("p76_p11_h5utils_numeric_concordance.json").write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
