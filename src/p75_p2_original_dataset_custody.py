"""P75-P2 actual VitaminC pinned source file byte-checking and source-cluster sealing.
Original licensed text never enters public GitHub files or CI artifacts.
Actions use temporary storage and publish ONLY derived receipts without claims.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import Request,urlopen
from urllib.parse import urlencode
import argparse,json,re,time

REV="be6febb761b0b2807687e61e0b5282e459df2fa0"
CHECKSUMS={
"train":"7461c6fd1a13459590317c5ccdc8651dd2daf7c1ad8ae4b10ccd88d164fccd5a",
"dev":"544934677f5d133873e6d38f4557f8966f4efa5d3d70874ffe6913f2091b86b5",
"test":"7ad1808dbc30c62e0a1427a53022d0dfaff668a1fde3c4b612a2d266edd753ad"
}
UA="EPISTEME-P75/1.0 (open science; github.com/WhoSia/EPISTEME)"
DATA="https://huggingface.co/datasets/tals/vitaminc/resolve/"+REV+"/"
LICENSE="https://raw.githubusercontent.com/TalSchuster/VitaminC/master/DATA_LICENSE"
PREVIEWS={"925488060":"Manchester","567579153":"Defy Media"}

def get(url,stream=None):
    err=None
    for trial in range(3):
        try:
            with urlopen(Request(url,headers={"User-Agent":UA}),timeout=120) as f:
                h=sha256(); size=0
                if stream is None:return f.read()
                with open(stream,"wb") as dst:
                    while True:
                        data=f.read(1048576)
                        if not data:break
                        h.update(data);size+=len(data);dst.write(data)
                return h.hexdigest(),size
        except Exception as e:
            err=e
            if stream:Path(stream).unlink(missing_ok=True)
            if trial<2:time.sleep(2**trial)
    raise RuntimeError("SOURCE_UNAVAILABLE_"+type(err).__name__+"_"+str(err)[:100])

def normalize(s):return s.replace("_"," ").strip().casefold()

def scan(file):
    pages=set();groups=defaultdict(lambda:{"labels":set(),"revs":set(),"rows":0})
    labels=Counter();types=Counter();rows=0
    with open(file,encoding="utf-8") as f:
        for line in f:
            if not line.strip():continue
            row=json.loads(line);rows+=1
            if not isinstance(row,dict):raise ValueError("NON_JSON_OBJECT_SOURCE")
            page=row.get("page")
            if not isinstance(page,str) or not page.strip():continue
            page=normalize(page);pages.add(page)
            kind=str(row.get("revision_type","")).lower();types[kind]+=1
            label=row.get("label");labels[str(label)]+=1
            rev=str(row.get("wiki_revision_id",""))
            case=str(row.get("case_id",""))
            if kind=="real" and re.fullmatch("[0-9]+",rev) and case:
                x=groups[(page,case)];x["rows"]+=1;x["revs"].add(rev);x["labels"].add(label)
    return pages,groups,rows,dict(types),dict(labels)

def select(splits):
    train,dev,test=(splits[n][0] for n in ("train","dev","test"))
    only=test-train-dev
    eligible={}
    for (page,case),meta in splits["test"][1].items():
        if page not in only or meta["rows"]<2 or len(meta["labels"])<2:continue
        if "NOT ENOUGH INFO" not in meta["labels"] and not ({"SUPPORTS","REFUTES"}<=meta["labels"]):continue
        if meta["revs"]:eligible.setdefault(page,(page,case,tuple(sorted(meta["revs"]))))
    # No original text or heldout group IDs are publicly disclosed.
    frozen=sorted(eligible.values(),key=lambda t:sha256(("P75-P2-v1|"+t[0]).encode()).hexdigest())[:12]
    commit=sha256("\n".join(json.dumps(x,separators=(",",":")) for x in frozen).encode()).hexdigest()
    return frozen,{"test_only_pages":len(only),"contrastive_eligible_pages":len(eligible),
                   "selected_disjoint_page_groups":len(frozen),"holdout_commitment_sha256":commit,
                   "selection_identity_list":"NOT_PUBLISHED"}

def query_wikipedia(ids):
    args=urlencode({"action":"query","prop":"revisions","revids":"|".join(ids),
        "rvprop":"ids|timestamp|sha1|size","format":"json","formatversion":"2"})
    j=json.loads(get("https://en.wikipedia.org/w/api.php?"+args))
    if j.get("error"):raise RuntimeError("WIKIMEDIA_API_ERROR")
    revisions={}
    for page in j.get("query",{}).get("pages",[]):
        for rev in page.get("revisions",[]):
            revisions[str(rev["revid"])]={
                "page":page.get("title"),"timestamp":rev.get("timestamp"),
                "sha1":rev.get("sha1"),"size":rev.get("size")}
    return revisions

def main():
    p=argparse.ArgumentParser();p.add_argument("--acquire",action="store_true")
    p.add_argument("--output",default="p75_p2_receipt")
    args=p.parse_args()
    if not args.acquire:
        a=scan_sample=[{"page":"A","case_id":"c","revision_type":"real",
           "wiki_revision_id":"123","label":"SUPPORTS"}]
        assert len(CHECKSUMS)==3 and all(re.fullmatch("[0-9a-f]{64}",v) for v in CHECKSUMS.values())
        assert normalize("New_York")=="new york"
        print(json.dumps({"stage":"P75_P2_PREFLIGHT","status":"PASS","original_files_downloaded":0}))
        return
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory(prefix="P75-licensed-ephemeral-") as tmp:
        raw_license=get(LICENSE)
        if b"Attribution-ShareAlike" not in raw_license:raise ValueError("SOURCE_LICENSE_CHANGED")
        splits={};file_meta={}
        for split,expected in CHECKSUMS.items():
            f=Path(tmp)/(split+".jsonl")
            actual,size=get(DATA+split+".jsonl",f)
            if actual!=expected:raise ValueError("ORIGINAL_SHA_MISMATCH_"+split+"_"+actual)
            info=scan(f);splits[split]=info
            file_meta[split]={"verified_sha256":actual,"source_byte_size":size,
                "rows":info[2],"revision_type_counts":info[3],"label_counts":info[4],
                "distinct_pages":len(info[0])}
            f.unlink() # never persist source bytes to GitHub workflow artifacts
        selected,holdout=select(splits)
        overlap={a+"_vs_"+b:len(splits[a][0]&splits[b][0])
                 for a,b in (("train","dev"),("train","test"),("dev","test"))}
        revs=[x for entry in selected for x in entry[2]][:8]
        revs=list(PREVIEWS)+list(dict.fromkeys(revs))
        wiki={"status":"NOT_VERIFIED"}
        try:
            response=query_wikipedia(revs)
            selected_lookup={rev:page for page,case,rs in selected for rev in rs}
            matched=sum(normalize(response[x]["page"])==selected_lookup.get(x) for x in revs
                       if x in response and x in selected_lookup)
            previews={k:(k in response and normalize(response[k]["page"])==normalize(v))
                      for k,v in PREVIEWS.items()}
            wiki={"status":"WIKIMEDIA_API_METADATA_RESPONSE","requested":len(revs),
                  "found":len(response),"preview_page_matches":previews,
                  "candidate_revision_page_matches":matched,
                  "candidate_revisions_requested":len(revs)-len(PREVIEWS),
                  "content_equivalence_to_dataset":"NOT_VERIFIED",
                  "independent_history_timestamps_found":sum(bool(v.get("timestamp")) for v in response.values())}
        except Exception as e:
            wiki={"status":"WIKIMEDIA_API_HOLD","error_type":type(e).__name__}
        public={"stage":"EPISTEME_P75_P2_PINNED_ORIGINAL_FILE_CUSTODY",
          "status":"SOURCE_BYTES_REHASHED_AND_MATCHED",
          "pinned_source_revision":REV,"source_repository":"tals/vitaminc",
          "source_licence":"Author DATA_LICENSE referencing Wikipedia and CC BY-SA 3.0",
          "license_sha256":sha256(raw_license).hexdigest(),
          "files":file_meta,"split_source_page_overlap":overlap,
          "holdout":holdout,"independent_wikipedia_revision":wiki,
          "raw_license_or_original_corpus_in_public_artifact":False,
          "full_original_dataset_permanently_saved_to_private_Drive":False,
          "real_human_reviews":0,"real_switch_utility":0,"new_paid_model_calls":0,
          "generated_utc":datetime.now(timezone.utc).isoformat()}
        (out/"public_receipt.json").write_text(json.dumps(public,indent=2,sort_keys=True)+"\n")
        print("P75_P2_ORIGINAL_SHA256_MATCHED_ALL_THREE_SPLITS rows="+str(sum(v["rows"] for v in file_meta.values())))
        print("P75_P2_HOLDOUT_COMMITMENT_SHA256 "+holdout["holdout_commitment_sha256"]+
              " selected_pages="+str(holdout["selected_disjoint_page_groups"]))
        print("P75_P2_WIKIPEDIA "+wiki["status"])

if __name__=="__main__":main()
