"""Compare 2025 author Git snapshot with held ZIP, without checking out data.

Usage: python analysis/p77_w63_release_history_compare.py AUTHOR_REPO DATA_ZIP
Requires a local clone with commit fcc91cc321c649fd96895eb435e978fb57d00acc.
"""
import hashlib, json, subprocess, sys, zipfile
from pathlib import Path

COMMIT='fcc91cc321c649fd96895eb435e978fb57d00acc'
EXPECTED='bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c'

def audit(repo, path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED: raise ValueError('ZIP SHA-256 mismatch')
    with zipfile.ZipFile(path) as z:
        if z.testzip(): raise ValueError('ZIP CRC failure')
        names=sorted(x for x in z.namelist() if x.startswith('Data/') and not x.endswith('/'))
        historical=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','--name-only',COMMIT,'--','Data/'],text=True).splitlines()
        results=[]
        for name in names:
            if name not in historical:
                results.append({'path':name,'status':'absent'}); continue
            source=subprocess.check_output(['git','-C',str(repo),'show',COMMIT+':'+name])
            current=z.read(name)
            results.append({'path':name,'same_bytes':source==current,'sha256':hashlib.sha256(source).hexdigest()})
    return {'git_commit':COMMIT,'zip_sha256':EXPECTED,'zip_count':len(names),'git_count':len(historical),
            'git_only':sorted(set(historical)-set(names)),'files':results,
            'scope':'byte identity only; does not establish manuscript run inputs'}

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: author_repo Data.zip')
    print(json.dumps(audit(*sys.argv[1:]),indent=2))

