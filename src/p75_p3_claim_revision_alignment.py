"""P75-P3: source-backed 12-claim reviewer packet compiler (offline source text held only in runner).

Reconstructs exact P75-P2 R3 fixed selection, checks 3 original sha256s,
pulls independent Wikipedia oldid/parent WIKITEXT, attempts conservative
sentence-to-source alignment. PRIVATE packets written only if explicitly
given --private-dir (never uploaded by Actions). GitHub only receives
metadata-only receipts. Heuristic passage matching != semantic entailment.
"""
from __future__ import annotations
import argparse,collections,difflib,hashlib,html,json,re
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote
from p75_p2_original_dataset_custody import (DATA,CHECKSUMS,PREVIEWS,REV,
    get,scan,select,query_wikipedia,normalize)

def digest(x):return hashlib.sha256(x.encode("utf-8")).hexdigest()
def clean(x):
    if not isinstance(x,str):return ""
    x=html.unescape(x)
    x=re.sub(r"<!--.*?-->"," ",x,flags=re.S)
    x=re.sub(r"\[\[[^\]|]*\|([^\]]+)\]\]",r"\1",x)
    x=re.sub(r"\[\[([^\]]+)\]\]",r"\1",x)
    x=re.sub(r"\[(https?://[^ ]+) ([^\]]+)\]",r"\2",x)
    x=re.sub(r"<[^>]+>"," ",x)
    x=x.replace("'''","").replace("''","")
    x=re.sub(r"\{\{[^{}]{0,400}\}\}"," ",x)
    return re.sub(r"\s+"," ",x).strip()

def norm(x):
    x=clean(x).casefold()
    return re.sub(r"[^a-z0-9]+"," ",x).strip()

def sentences(wiki):
    # Conservative human-readable candidates, never imply parsed Wikipedia AST.
    lines=wiki.splitlines()
    result=[]
    for ln in lines:
        if ln.lstrip().startswith(("{{","|","[[File:","[[Category:","==","!","{|","|-")):continue
        if len(ln)>2500:continue
        for seg in re.split(r"(?<=[.!?])\s+(?=[A-Z(])",clean(ln)):
            if len(seg)>=35 and len(seg)<=800:result.append(seg)
    return result

def words(x):return set(re.findall(r"[a-z0-9]+",norm(x)))
def closest(sentence_list,claim,evidence):
    w=words(evidence)|words(claim)
    if not sentence_list or len(w)<2:return "",0.0
    def score(s):
        q=words(s);return len(w&q)/max(1,len(w))
    result=max(sentence_list,key=score)
    return result,round(score(result),4)

def source_text(ids):
    ids=[str(v) for v in ids if str(v).isdigit()]
    collected={}
    for i in range(0,len(ids),20):
        # Never log returned original full-source text.
        url=("https://en.wikipedia.org/w/api.php?action=query&prop=revisions"
         "&revids="+quote("|".join(ids[i:i+20]),safe="")+
         "&rvprop=ids%7Ctimestamp%7Csha1%7Ccontent&rvslots=main&format=json&formatversion=2")
        j=json.loads(get(url))
        if j.get("error"):raise RuntimeError("WIKIMEDIA_WIKITEXT_ACCESS_REJECTED")
        for p in j.get("query",{}).get("pages",[]):
            for r in p.get("revisions",[]):
                raw=r.get("slots",{}).get("main",{}).get("content")
                if isinstance(raw,str):collected[str(r["revid"])]={
                    "page":p.get("title"),"text":raw,"sha256":digest(raw),
                    "wikipedia_sha1":r.get("sha1"),"timestamp":r.get("timestamp"),
                    "parentid":r.get("parentid")}
    return collected

def shared_pairs(rows):
    by_claim=collections.defaultdict(list)
    for r in rows:
        c=norm(str(r.get("claim","")))
        if c:by_claim[c].append(r)
    pairs=[]
    for name,items in by_claim.items():
        for i,x in enumerate(items):
            for y in items[i+1:]:
                if x.get("label")!=y.get("label") and norm(str(x.get("evidence","")))!=norm(str(y.get("evidence",""))):
                    pairs.append((x,y))
    return pairs

def analyse_case(entry,rows,wiki,parents):
    page,case,rr=entry;rev=rr[0]
    if rev not in wiki or rev not in parents:raise RuntimeError("P75_SELECTED_REV_MISSING")
    new=wiki[rev];old=parents[rev]
    if normalize(new["page"])!=page:raise RuntimeError("P75_WRONG_WIKIPEDIA_PAGE")
    observed_rows=[r for r in rows if normalize(str(r.get("page","")))==page and str(r.get("case_id",""))==case and str(r.get("revision_type","")).lower()=="real"]
    pairs=shared_pairs(observed_rows)
    old_norm=norm(old["text"]);new_norm=norm(new["text"])
    # Detect only exact normalized evidence inclusion in the original article
    # snapshot, not dataset-gold or independent warrant.
    rank=[]
    for pair in pairs:
        match=[]
        for row in pair:
            e=norm(str(row.get("evidence","")))
            found_old=bool(e and len(e)>30 and e in old_norm)
            found_new=bool(e and len(e)>30 and e in new_norm)
            match.append((found_old,found_new))
        score=sum(any(x) for x in match)+3*int(match[0]!=match[1])
        rank.append((score,pair,match))
    rank.sort(key=lambda x:-x[0])
    chosen=rank[0][1] if rank else None
    alignment=rank[0][2] if rank else []
    # Distinguish overlap/changed-span heuristics from human-proof validity.
    e=str(chosen[0].get("evidence","")) if chosen else (str(observed_rows[0].get("evidence","")) if observed_rows else "")
    claim=str(chosen[0].get("claim","")) if chosen else (str(observed_rows[0].get("claim","")) if observed_rows else "")
    old_sentence,old_score=closest(sentences(old["text"]),claim,e)
    new_sentence,new_score=closest(sentences(new["text"]),claim,e)
    pre_wiki="https://en.wikipedia.org/w/index.php?oldid="+str(old["id"])
    post_wiki="https://en.wikipedia.org/w/index.php?oldid="+rev
    records=[{"row_id_sha256":digest(str(row.get("unique_id",row.get("id", "")))),
       "label_sealed_sha256":digest(str(row.get("label",""))),
       "claim_sha256":digest(str(row.get("claim",""))),
       "evidence_sha256":digest(str(row.get("evidence",""))),
       "claim_length":len(str(row.get("claim",""))),
       "evidence_length":len(str(row.get("evidence","")))}
       for row in observed_rows]
    group_id=digest("P75-P3|"+page+"|"+case+"|"+rev)[:24]
    reviewer={
       "group_id":group_id,
       "condition":"MASKED_FULL_OR_PROJECTED_BY_EXTERNAL_CUSTODIAN",
       "claim":claim,
       "source_links":{"old":pre_wiki,"new":post_wiki},
       "source_sentences":{"old_heuristic":old_sentence,"new_heuristic":new_sentence},
       "source_alignment_notice":"HEURISTIC_ONLY_NOT_SEMANTIC_GOLD",
       "dataset_evidence_example":e,
       "proposed_minimal_evidence_ids":[digest(e)[:18]] if e else [],
       "review_prompts":["For the EXACT stated claim, classify old and new evidence separately as SUPPORTS/REFUTES/NOT ENOUGH INFO, without consulting publisher labels.",
          "Identify a sufficient evidence set and test each atom for necessity, including alternative minimal sets.",
          "Check whether old/new sentences refer to the same entity/time and whether exact dataset evidence is supported by cited revisions.",
          "Given predeclared cost matrix, choose KEEP/SWITCH/REVIEW and state uncertainty."],
       "attribution":{"dataset":"VitaminC (Schuster, Fisch, Barzilay, 2021)","license":"Wikipedia articles CC BY-SA as applicable; see author DATA_LICENSE",
              "dataset_release":REV},
       "blinding":"No publisher label or reference answer present in private reviewer packet"
    }
    public={
      "group_id":group_id,
      "source_revision_sha256":digest(rev),
      "source_article_sha256":digest(page),
      "original_Wikipedia_revision_accessible":True,
      "original_previous_revision_accessible":True,
      "old_source_text_sha256":old["sha256"],"new_source_text_sha256":new["sha256"],
      "differs_old_new":old["sha256"]!=new["sha256"],
      "original_revision_timestamp_present":bool(new.get("timestamp")),
      "original_parent_revision_timestamp_present":bool(old.get("timestamp")),
      "source_real_dataset_rows":len(observed_rows),
      "same_claim_changed_label_evidence_pair_count":len(pairs),
      "selected_pair_dataset_evidence_exact_in_snapshots":alignment,
      "nearest_old_sentence_lexical_overlap":old_score,
      "nearest_new_sentence_lexical_overlap":new_score,
      "heuristic_old_sentence_present":bool(old_sentence),
      "heuristic_new_sentence_present":bool(new_sentence),
      "actual_minimum_sufficient_evidence_certified":False,
      "human_semantic_warrant_completed":False,
      "publisher_gold_label_is_independent_certification":False,
      "public_packet_contains_raw_claim_or_evidence":False,
      "private_packet_example_complete":bool(claim and e and old_sentence and new_sentence),
      "source_record_fingerprints":[dict(x) for x in records]
    }
    return public,reviewer

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--acquire",action="store_true")
    p.add_argument("--public-dir",default="p75_p3_output")
    p.add_argument("--private-dir",default=None)
    args=p.parse_args()
    if not args.acquire:
        assert norm("[[Old|Correct]]")=="correct"
        assert norm("A '''test'''")=="a test"
        assert shared_pairs([{"claim":"same","label":"SUPPORTS","evidence":"e1"},{"claim":"same","label":"REFUTES","evidence":"e2"}])
        print(json.dumps({"status":"P75_P3_OFFLINE_PRECHECK_PASS","source_downloads":0}))
        return
    if args.private_dir and Path(args.private_dir).resolve()==Path(args.public_dir).resolve():
        raise ValueError("P75_PRIVATE_AND_PUBLIC_OUTPUTS_MUST_DIFFER")
    out=Path(args.public_dir);out.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory(prefix="P75-licensed-originals-") as tmp:
        splits={}
        for split,sha in CHECKSUMS.items():
            loc=Path(tmp)/(split+".jsonl")
            actual,size=get(DATA+split+".jsonl",loc)
            if actual!=sha:raise ValueError("P75_ORIGINAL_SHA_DRIFT_"+split)
            splits[split]=scan(loc)
            if split!="test":loc.unlink()
        first,meta=select(splits)
        revs=[rr[0] for _,_,rr in first]
        response=query_wikipedia(revs)
        verified=[entry for entry in first if entry[2][0] in response
             and normalize(response[entry[2][0]]["page"])==entry[0]
             and response[entry[2][0]].get("timestamp") and response[entry[2][0]].get("sha1")]
        to_check=verified[:24]
        revisions=source_text([e[2][0] for e in to_check])
        parent_ids={entry[2][0]:str(response[entry[2][0]]["parentid"])
            for entry in to_check if response[entry[2][0]].get("parentid")}
        predecessors=source_text(list(dict.fromkeys(parent_ids.values())))
        parent_lookup={k:dict(predecessors[v],id=v) for k,v in parent_ids.items() if v in predecessors}
        qualified=[e for e in to_check if e[2][0] in revisions and e[2][0] in parent_lookup
              and revisions[e[2][0]]["sha256"]!=parent_lookup[e[2][0]]["sha256"]]
        chosen=qualified[:12]
        assert len(chosen)==12,"P75_R3_HOLDOUT_RECONSTRUCTION_FAILED"
        holdout_commit=digest("\\n".join(json.dumps(
           (entry[0],entry[1],entry[2][0],revisions[entry[2][0]]["sha256"],
            parent_lookup[entry[2][0]]["sha256"]),
           separators=(",",":")) for entry in chosen))
        # P75-P2 R3 current code commitment uses literal escaped backslash+n.
        EXPECTED="7d96568480e87aec80ffb8be1d3002d5fb11920ac40a3f9fd5e57a176ac22e78"
        if holdout_commit!=EXPECTED:raise ValueError("P75_P2_SELECTION_COMMITMENT_DRIFT_"+holdout_commit)
        selected={(page,case) for page,case,rr in chosen}
        retained=[]
        with open(Path(tmp)/"test.jsonl",encoding="utf-8") as f:
            for line in f:
                row=json.loads(line)
                if (normalize(str(row.get("page",""))),str(row.get("case_id",""))) in selected:
                    retained.append(row)
        public=[];private=[]
        for entry in chosen:
            a,b=analyse_case(entry,retained,revisions,parent_lookup)
            public.append(a);private.append(b)
        assert len({p["group_id"] for p in public})==12
        summary={
          "stage":"P75_P3_SOURCE_TO_CLAIM_ALIGNMENT",
          "status":"TWELVE_SOURCE_GROUPS_PACKET_SCHEMAS_COMPILED_SEMANTIC_VALIDITY_HOLD",
          "original_publisher_commit":REV,
          "same_R3_holdout_commitment_sha256":holdout_commit,
          "groups":12,
          "source_revision_and_parent_content_captured_in_runner":12,
          "original_test_claims_in_review_bundle":sum(int(p["private_packet_example_complete"]) for p in public),
          "same_claim_cross_label_pair_groups":sum(p["same_claim_changed_label_evidence_pair_count"]>0 for p in public),
          "at_least_one_exact_evidence_match_groups":sum(any(any(t) for t in p["selected_pair_dataset_evidence_exact_in_snapshots"]) for p in public),
          "semantic_entailment_certified_groups":0,
          "independently_blind_human_reviewed_groups":0,
          "private_life_cycle":"EPHEMERAL_CI; optional --private-dir for user-authorized local build",
          "private_original_corpus_Drive_uploaded":False,
          "new_model_calls":0}
        (out/"public_alignment_receipt.json").write_text(json.dumps(summary,indent=2)+"\n")
        (out/"public_masked_packet_index.json").write_text(json.dumps(public,indent=2)+"\n")
        if args.private_dir:
            priv=Path(args.private_dir);priv.mkdir(parents=True,exist_ok=True)
            for i,packet in enumerate(private,1):
                (priv/f"packet_{i:02d}_{packet['group_id']}.json").write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n")
            (priv/"PRIVATE_ATTRIBUTION_AND_RULES.txt").write_text(
                "VitaminC author Schuster, Fisch & Barzilay 2021, NAACL; Wikipedia article original licenses CC BY-SA as applicable.\n"
                "PRIVATE SOURCE TEXTS: do not redistribute without attribution/licence compliance.\n"
                "Reviewer dataset gold labels are deliberately omitted; do not infer them from filename.\n")
        print("P75_P3_12_GROUPS_RECONSTRUCTED "+holdout_commit)
        print("P75_P3_PAIR_GROUPS "+str(summary["same_claim_cross_label_pair_groups"]))
        print("P75_P3_EXACT_SOURCE_EVIDENCE_GROUPS "+str(summary["at_least_one_exact_evidence_match_groups"]))
        print("P75_P3_PUBLIC_ONLY_NO_COPYRIGHTED_RAW_TEXT")

if __name__=="__main__":main()
