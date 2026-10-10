"""P71 human-grade OFFLINE blinded review interface generator.

Locally generated HTML from the original source, no API calls, no browser
network or analytics. Do not put raw licensed packet HTML in public CI artifacts.
Output JSON follows p70/p71 independent-human review court contracts.
"""
from __future__ import annotations
import argparse, html, json
from pathlib import Path

FLAGS=("temporal_scope","subject_identity","evidence_specificity",
       "cross_qa_dependency","source_access","context_dependency","other")
VERDICTS=("SUPPORT","CONTRADICT","INSUFFICIENT","AMBIGUOUS")

def render(bundle,template):
    if bundle.get("kind")!="P71_BLIND_EVIDENCE_PACKET_BUNDLE":
        raise ValueError("P71_REVIEW_UI_UNVERIFIED_BUNDLE")
    if template.get("role")!="INDEPENDENT_HUMAN_REVIEW":
        raise ValueError("P71_REVIEW_UI_BAD_TEMPLATE")
    cases=bundle.get("cases",[])
    j=template.get("judgments",[])
    if len(cases)!=16 or len(j)!=16:
        raise ValueError("P71_REVIEW_UI_WRONG_CASE_COUNT")
    ids={x["case_id"] for x in cases}
    if len(ids)!=16 or ids!={x["case_id"] for x in j}:
        raise ValueError("P71_REVIEW_UI_CASES_DONT_MATCH")
    data=json.dumps({
        "assignment":bundle["assignment"],"cases":cases,
        "sha":{x["case_id"]:x["packet_sha256"] for x in j},
        "flags":FLAGS,"verdicts":VERDICTS,
    },ensure_ascii=False).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    return """<!doctype html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EPISTEME P71 — Independent Blind Evidence Review</title>
<style>body{font-family:system-ui,sans-serif;background:#f7f7f5;color:#20211f;
max-width:860px;margin:0 auto;padding:20px;line-height:1.5}main{margin-top:12px}
h1{font-size:1.6rem;line-height:1.24}section{border:1px solid #d9dcda;background:white;
border-radius:14px;padding:18px;margin:18px 0}h2{font-size:1.1rem;margin:0 0 10px}
.record{margin:8px 0;padding:10px;border-left:3px solid #c4cad0;background:#f7f9fa}
small,.hint{color:#58616b}select,textarea,input{font:inherit}select{width:100%;padding:9px}
textarea{width:100%;box-sizing:border-box;padding:10px;min-height:78px}
.checks{display:flex;flex-wrap:wrap;gap:8px}.checks label{padding:4px 9px;
border:1px solid #d9dcda;border-radius:9px}button{background:#164970;color:white;
border:0;border-radius:10px;padding:13px 18px;font-weight:bold}
button:focus-visible{outline:3px solid orange}code{overflow-wrap:anywhere}
#notice{font-weight:bold;white-space:pre-wrap}a{overflow-wrap:anywhere}
label{display:block;margin:10px 0 5px}</style></head><body>
<h1>EPISTEME-P71 · Independent evidence-only judgment</h1>
<p>License/attribution: AVeriTeC, Schlichtkrull et al. (2023), CC BY-NC 4.0.
Use this offline form noncommercially. This browser page does not contact any
server or autosave. Save the downloaded JSON privately.</p>
<p><strong>Study contract:</strong> Only packet information counts. Do not consult
original fact-check labels, model outputs, external web pages or another rater.
A source URL tells you provenance; it is not evidence you independently opened.
Use AMBIGUOUS or INSUFFICIENT where warranted. Cite indispensable evidence IDs.</p>
<label for="reviewer">Private reviewer pseudonym (must differ from other reviewer)</label>
<input id="reviewer" autocomplete="off" placeholder="RATER_A" style="width:100%">
<label><input type="checkbox" id="independent"> I made these judgments myself,
independently of study authors, prior model answers, and the other reviewer.</label>
<main id="cases"></main>
<button id="export">Validate all 16 and save response JSON</button>
<p id="notice" role="status"></p>
<script type="application/json" id="packetdata">__DATA__</script>
<script>
const data=JSON.parse(document.getElementById('packetdata').textContent);
const root=document.getElementById('cases');
function item(t,txt,cls){const x=document.createElement(t);if(cls)x.className=cls;x.textContent=txt;return x;}
function fieldset(values, kind,caseid){const box=item('div','','checks');
for(const v of values){const label=document.createElement('label');
const input=document.createElement('input');input.type='checkbox';input.value=v;
input.dataset.kind=kind;input.dataset.caseid=caseid;
label.append(input,document.createTextNode(' '+v));box.append(label);}return box;}
for(const [i,p] of data.cases.entries()){
const section=document.createElement('section');section.dataset.caseid=p.case_id;
section.append(item('h2','Packet '+(i+1)+' of 16'));
section.append(item('small','Case '+p.case_id));
section.append(item('p','CLAIM: '+p.claim));
for(const ev of p.question_answer_evidence){
const div=item('div','','record');div.append(item('strong',ev.evidence_id));
div.append(item('p','Question: '+ev.question));
div.append(item('p','Answer: '+ev.answer));
div.append(item('small','Provenance (not a reviewed source): '+ev.source_url));
section.append(div);}
section.append(item('label','Your evidence-only verdict'));
const select=document.createElement('select');select.dataset.kind='verdict';
select.append(new Option('Select one…',''));for(const v of data.verdicts)select.append(new Option(v,v));
section.append(select);
section.append(item('label','Indispensable evidence IDs (only those essential to your verdict)'));
section.append(fieldset(p.question_answer_evidence.map(x=>x.evidence_id),'evidence',p.case_id));
section.append(item('label','Potential limitations (check all that apply)'));
section.append(fieldset(data.flags,'flags',p.case_id));
section.append(item('label','Does changing the order of these QAs preserve the intended meaning?'));
const order=document.createElement('select');order.dataset.kind='safe';
order.append(new Option('Select one…',''),new Option('Yes','true'),new Option('No','false'));
section.append(order);
section.append(item('label','Reasoned explanation (minimum 12 characters)'));
const why=document.createElement('textarea');why.dataset.kind='reason';section.append(why);
root.append(section);}
document.getElementById('export').addEventListener('click',()=>{
const pseudonym=document.getElementById('reviewer').value.trim();
const note=document.getElementById('notice');
if(!pseudonym||!document.getElementById('independent').checked){
note.textContent='Enter a distinct pseudonym and truthfully confirm independence.';return;}
const results=[];
for(const sec of root.querySelectorAll('section')){
const cid=sec.dataset.caseid;
const read=k=>sec.querySelector('[data-kind="'+k+'"]');
const verdict=read('verdict').value,safety=read('safe').value,
reason=read('reason').value.trim();
const marked=k=>Array.from(sec.querySelectorAll('input[data-kind="'+k+'"]:checked')).map(x=>x.value);
const evidence=marked('evidence'),flags=marked('flags');
if(!verdict||!safety||reason.length<12||
((verdict==='SUPPORT'||verdict==='CONTRADICT')&&!evidence.length)){
note.textContent='Incomplete response in packet '+(results.length+1)+'. Select verdict and order safety, add evidence IDs for SUPPORT/CONTRADICT, and a reason of 12+ characters.';return;}
results.push({case_id:cid,packet_sha256:data.sha[cid],verdict:verdict,
sufficient_evidence_ids:evidence,flags:flags,qa_order_semantically_safe:safety==='true',
reason:reason});}
const output={role:'INDEPENDENT_HUMAN_REVIEW',reviewer_id:pseudonym,
independent_from_author_and_model_outputs:true,
blind_to_original_gold_and_peer_judgments:true,
judgments:results};
const url=URL.createObjectURL(new Blob([JSON.stringify(output,null,2)],
{type:'application/json'}));
const a=document.createElement('a');a.href=url;
a.download='P71_review_'+data.assignment+'_'+pseudonym.replace(/[^a-zA-Z0-9_-]/g,'_')+'.json';
document.body.append(a);a.click();a.remove();URL.revokeObjectURL(url);
note.textContent='Exported 16 judgments. Share JSON privately with research custodian. No server received them.';});
</script></body></html>""".replace("__DATA__",data)

def self_test():
    data={"kind":"P71_BLIND_EVIDENCE_PACKET_BUNDLE","assignment":"A",
          "cases":[{"case_id":str(i),"claim":"Safe mock claim",
                    "question_answer_evidence":[
                        {"evidence_id":"e"+str(i),"question":"Q","answer":"A",
                         "source_url":"https://example.test"}]} for i in range(16)]}
    t={"role":"INDEPENDENT_HUMAN_REVIEW","judgments":[
        {"case_id":str(i),"packet_sha256":"mockhash"} for i in range(16)]}
    html=render(data,t)
    assert html.count('id="packetdata"')==1
    assert 'source_label_SEALED' not in html
    assert 'No server received them' in html
    assert "Safe mock claim" in html
    try:render(data,{"role":"FAKE","judgments":t["judgments"]})
    except ValueError:pass
    else:raise AssertionError("P71_FORGED_ROLE_ACCEPTED")
    print("P71_REVIEW_HTML_SELFTEST_PASS 16_mock_packets real_reviews=0 provider_calls=0")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--masked");ap.add_argument("--template");ap.add_argument("--out")
    ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test:self_test()
    else:
        if not all((a.masked,a.template,a.out)):
            ap.error("masked, template and out required")
        path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(render(json.loads(Path(a.masked).read_text()),
            json.loads(Path(a.template).read_text())),encoding="utf-8")
        print("P71_REVIEW_OFFLINE_HTML_READY blinded_cases=16 real_reviews=0 provider_calls=0")
