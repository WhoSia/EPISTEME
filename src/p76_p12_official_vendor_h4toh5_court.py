#!/usr/bin/env python3
"""P76-P12: official h4h5tools binary checksum and bounded two-fixture converter court.

The source HDF4 bytes are pinned; never interpret converter-specific failure as
irreversible loss of scientific falsification capacity.
"""
import hashlib, json, os, re, subprocess, tarfile, tempfile
from pathlib import Path
from urllib.request import Request, urlopen
BASE="https://support.hdfgroup.org/ftp/HDF5/releases/h4toh5/h4toh5-2.2.5/bin/"
NAME="h4h5tools-1.10.6-2.2.5-centos7_64.tar.gz"
PIN="2c46ad56bea5aab05e996e473a81dcbd9a66b125"
FILES=[
 ("mfhdf/hdfimport/SDSfloat2.hdf","3ba791239a5874bf9d97e1765a3e2896dbe965680b7fee59f9cc96afefb28b38"),
 ("mfhdf/hdp/testfiles/sds_compressed.hdf","bb5eeb11b4b24d2a29999df48e7e1ddf041a3cef8510d05961e6e4bdf0a98bcb")
]
def get(url, limit=12_000_000):
    with urlopen(Request(url,headers={"User-Agent":"EPISTEME-P76-original-vendor-court"}),timeout=45) as f:
        v=f.read(limit+1)
    assert len(v)<=limit,(url,len(v))
    return v
def run(*args):
    return subprocess.run(args,capture_output=True,text=True,timeout=50)
receipt={"court":"P76_P12_VENDOR_BINARY","vendor":"HDF Group h4h5tools v2.2.5",
 "original_commit":PIN,"vendor_archive":BASE+NAME,"status":"INCOMPLETE",
 "vendor_sha_match":None,"converted":[],
 "scientific_irreversibility_proved":False,"new_theorem_proved":False}
output=Path("p76_p12_vendor_binary_receipt.json")
def save():
    output.write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
try:
    check=get(BASE+NAME+".sha256",20000).decode("utf-8","replace")
    target=re.search(r"[0-9a-fA-F]{64}",check)
    assert target,"Official sha256 checksum unavailable"
    archive=get(BASE+NAME)
    calculated=hashlib.sha256(archive).hexdigest()
    receipt.update(vendor_expected_sha256=target.group(0).lower(),vendor_computed_sha256=calculated,
      vendor_sha_match=calculated==target.group(0).lower())
    assert receipt["vendor_sha_match"],"Official binary checksum mismatch"
    with tempfile.TemporaryDirectory() as d:
        directory=Path(d)
        tarpath=directory/NAME;tarpath.write_bytes(archive)
        with tarfile.open(tarpath,"r:gz") as t:
            files=t.getmembers()
            assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts and not m.issym() and not m.islnk() for m in files),"Unsafe archive path/link"
            t.extractall(directory,filter="data")
        installer=directory/"hdf"/"H4H5-2.2.5-Linux.sh"
        assert installer.is_file(),"Expected publisher Linux self-extractor"
        receipt["installer_sha256"]=hashlib.sha256(installer.read_bytes()).hexdigest()
        target=directory/"expanded";target.mkdir()
        probe=run("bash",str(installer),"--noexec","--target",str(target))
        receipt["installer_extract"]={"returncode":probe.returncode,"stdout":probe.stdout[:900],"stderr":probe.stderr[:900]}
        tools=[p for p in target.rglob("*") if p.is_file() and "h4toh5" in p.name.lower() and not p.suffix in (".txt",".md",".so",".a",".h")]
        receipt["archive_file_listing"]=[str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file()][:90]
        receipt["candidate_binaries"]=[str(p.relative_to(directory)) for p in tools]
        print("VENDOR_ARCHIVE_LISTING",json.dumps(receipt["archive_file_listing"][:90]),flush=True)
        print("INSTALLER_EXTRACT_DIAGNOSTIC",json.dumps(receipt["installer_extract"]),flush=True)
        print("EXTRACTED_LISTING",json.dumps([str(p.relative_to(directory)) for p in target.rglob("*")][:100]),flush=True)
        assert tools,"No official executable h4toh5 binary in verified publisher archive"
        binary=tools[0];binary.chmod(binary.stat().st_mode|0o111)
        receipt["binary_path"]=str(binary.relative_to(directory))
        for path,pin in FILES:
            b=get("https://raw.githubusercontent.com/HDFGroup/hdf4/"+PIN+"/"+path,2_000_000)
            sha=hashlib.sha256(b).hexdigest()
            assert sha==pin,(path,sha)
            old=directory/Path(path).name;old.write_bytes(b)
            new=directory/(old.name+".vendor.h5")
            rr=run(str(binary),str(old),str(new))
            item={"source":path,"original_sha256":sha,"original_bytes":len(b),
                "vendor_exit":rr.returncode,"stdout":rr.stdout[:500],"stderr":rr.stderr[:1200],
                "converted_exists":new.exists(),"converted_bytes":new.stat().st_size if new.exists() else 0}
            if new.exists() and new.stat().st_size:
                checkh=run("h5dump","-H",str(new))
                item.update(h5dump_header_exit=checkh.returncode,h5dump_header=checkh.stdout[:2200])
            receipt["converted"].append(item)
    receipt["status"]="SOURCE_VERIFIED_VENDOR_EXECUTED"
except Exception as e:
    receipt["status"]="VENDOR_TEST_FAILED_OR_UNAVAILABLE"
    receipt["failure"]=type(e).__name__+": "+str(e)[:900]
    raise
finally:
    save()
print(json.dumps(receipt,indent=2))
