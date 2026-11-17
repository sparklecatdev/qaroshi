#!/usr/bin/env python3
"""Compile a truly answer-key-free, offline Qaroshi first-pass reader form.

The generated page embeds ONLY the Qaroshi learner stimulus CSV. It never reads
facilitator_english_key.csv, standard10 resources or English source sentences.
An anonymous code is chosen by the participant. No analytics, requests,
storage, cookies, translation scoring or human identity claims are created.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path

REQUIRED = ("item_id", "previous_qaroshi_context", "target_qaroshi", "task")


def learner_rows(sheet: Path) -> list[dict[str, str]]:
    with sheet.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != list(REQUIRED):
            raise ValueError("Only the four-field Qaroshi-only reader sheet is allowed")
        rows = list(reader)
    if len(rows) != 80:
        raise ValueError("Expected 80 blind reader stimuli, got %s" % len(rows))
    if len({x["item_id"] for x in rows}) != len(rows):
        raise ValueError("Duplicate trial item IDs")
    if any(not x["item_id"].startswith("BL10-") or not x["target_qaroshi"].strip() for x in rows):
        raise ValueError("Invalid or empty stimulus row")
    return rows


def build(reader_sheet: Path, output: Path) -> dict:
    rows = learner_rows(reader_sheet)
    # Sanitize SCRIPT embedding while preserving Unicode and real Qaroshi text.
    payload = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    page = PAGE.replace("<!--__BLIND_STIMULI__-->", '<script id="blind-items" type="application/json">' +
                        payload + '</script>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    return {"learner_stimuli": len(rows), "output": str(output),
            "english_answer_key_embedded": False, "participant_data_collected": 0,
            "network_or_persistent_storage": False,
            "status": "blind-reader field kit, not a completed human trial"}


PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Qaroshi | First-pass reader study</title>
<style>
:root{font:16px/1.58 system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light dark}
*{box-sizing:border-box}body{max-width:760px;padding:20px 17px 60px;margin:auto}
h1{font-size:clamp(1.6rem,4.5vw,2.25rem);line-height:1.22;margin:10px 0}
p{line-height:1.68}.muted,small{color:light-dark(#5f6674,#afb7c5)}
.card{border:1px solid light-dark(#c9cfda,#424950);border-radius:14px;padding:20px;margin:16px 0}
.notice{background:light-dark(#f3f5f9,#292d37);border-radius:11px;padding:13px 16px}
label{display:block;font-weight:600;margin:16px 0 5px}
textarea,input,select{font:inherit;padding:10px 12px;border-radius:9px;border:1px solid #9299a8;width:100%;
background:light-dark(white,#20232a);color:inherit}textarea{resize:vertical;min-height:112px}
button{font:600 .93rem system-ui;border-radius:9px;border:1px solid #8894a6;padding:10px 15px;cursor:pointer;
background:light-dark(#f7f8fb,#333944);color:inherit}
button.primary{background:light-dark(#203650,#aac4e9);color:light-dark(white,#161f32);border-color:transparent}
button:disabled{opacity:.5;cursor:not-allowed}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.qaroshi{font:600 clamp(1.05rem,3.2vw,1.35rem)/1.6 ui-monospace,monospace;overflow-wrap:anywhere}
.context{margin-bottom:18px}.context .qaroshi{font-weight:450}
textarea:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #6093da;outline-offset:2px}
[hidden]{display:none!important}.status{font-size:.9rem;margin:12px 0}.progress{font-size:.9rem;font-weight:600}
fieldset{border:0;margin:0;padding:0}
.error{color:light-dark(#a42222,#ff9f9f)}.footer{font-size:.82rem;margin-top:32px}
</style></head><body>
<header><div class="muted">Offline · answer-key-free · anonymous</div>
<h1>Qaroshi first-pass reader study</h1>
<p>This study asks what you understand from <strong>Qaroshi-only text</strong>.
There are no hints, English translations or correctness scores in this page.
The source sentences are editorial and have not been independently ratified.</p></header>
<section id="setup" class="card">
<h2>Before you begin</h2>
<p>You must be able to consent to participating. If you have already read the editorial answers, have worked on these source scenes, or prefer not to answer, do not take this as a blind test.
You can always write “cannot determine”. Do not enter your real name, email, handles, or identifying details.</p>
<label for="code">An anonymous participant code you choose (letters, numbers and hyphens)</label>
<input id="code" autocomplete="off" maxlength="32" placeholder="Example: reader-12" pattern="[A-Za-z0-9-]{3,32}">
<label><input type="checkbox" id="consent" style="width:auto"> I consent and understand answers remain in this browser until I export them.</label>
<label for="exposure">Have you accessed these English answer keys or prior versions?</label>
<select id="exposure"><option value="unsure">Unsure</option><option value="yes">Yes</option><option value="no">No</option></select>
<button class="primary" id="begin" type="button">Begin Qaroshi-only prompts</button>
<p id="setupError" class="error" role="alert"></p></section>
<section id="study" hidden>
<div class="progress" id="progress" aria-live="polite"></div>
<div class="card">
<div class="context" id="priorWrap"><strong>Previous Qaroshi context</strong><div class="qaroshi" id="prior"></div></div>
<strong>Target Qaroshi</strong><div class="qaroshi" id="target" lang="x-qaroshi"></div>
<p id="task" class="muted"></p>
<label for="paraphrase">Your first-pass interpretation (free English paraphrase, or "cannot determine")</label>
<textarea id="paraphrase" spellcheck="true" maxlength="2500"></textarea>
<label for="roles">Who is acting? What is affected? Note any uncertainty, negation, evidence, ability or permission.</label>
<textarea id="roles" maxlength="1800" rows="3" placeholder="Describe any roles/scope you can infer."></textarea>
<label for="uncertainty">Uncertainty</label>
<select id="uncertainty"><option value="3">3 · Cannot determine</option>
<option value="2">2 · Very unsure</option><option value="1">1 · Some uncertainty</option>
<option value="0">0 · Confident</option></select>
</div>
<p class="status" id="studyError" role="alert"></p>
<div class="actions">
<button id="previous" type="button">Previous</button>
<button id="next" class="primary" type="button">Save and continue</button>
<button id="export" type="button">Export responses as CSV</button></div>
<p class="muted">Your answers are held only in memory on this page. Navigating away or refreshing clears them. Export before closing it.</p></section>
<section class="footer">This form does not administer a supervised experiment, authenticate eligibility,
contact a server, store responses permanently, or judge semantics. A separate human facilitator
must keep the English source key out of view and arrange independent adjudication.
Do not upload identifying information to public repositories.</section>
<!--__BLIND_STIMULI__-->
<script>
(function(){
'use strict';
const items=JSON.parse(document.getElementById('blind-items').textContent);
const $=id=>document.getElementById(id);
let at=0,code='',exposure='unsure',answers=[];
function validCode(s){return /^[A-Za-z0-9-]{3,32}$/.test(s);}
function display(){
 const x=items[at],r=answers[at]||{};
 $('progress').textContent='Prompt '+(at+1)+' of '+items.length+' · '+answers.filter(x=>x&&x.paraphrase).length+' responses captured locally';
 $('priorWrap').hidden=!x.previous_qaroshi_context;
 $('prior').textContent=x.previous_qaroshi_context;
 $('target').textContent=x.target_qaroshi;
 $('task').textContent=x.task;
 $('paraphrase').value=r.paraphrase||'';
 $('roles').value=r.roles||'';
 $('uncertainty').value=r.uncertainty||'3';
 $('previous').disabled=at===0;
 $('next').textContent=at===items.length-1?'Save final response':'Save and continue';
 $('studyError').textContent='';
}
function save(requireAnswer){
 const text=$('paraphrase').value.trim();
 if(requireAnswer&&!text){$('studyError').textContent='Enter a first-pass interpretation or "cannot determine" before continuing.';return false;}
 answers[at]={paraphrase:text,roles:$('roles').value.trim(),uncertainty:$('uncertainty').value};
 $('studyError').textContent='';return true;
}
$('begin').addEventListener('click',()=>{
 code=$('code').value.trim();exposure=$('exposure').value;
 if(!validCode(code)||!$('consent').checked){$('setupError').textContent='Use a 3–32 character anonymous code and confirm consent.';return;}
 $('setup').hidden=true;$('study').hidden=false;display();$('paraphrase').focus();
});
$('next').addEventListener('click',()=>{if(!save(true))return;if(at<items.length-1)at++;display();});
$('previous').addEventListener('click',()=>{save(false);if(at>0)at--;display();});
function csvCell(x){return '"'+String(x??'').replaceAll('"','""').replaceAll(/\r?\n/g,' ')+'"';}
function exportCSV(){
 save(false);
 const rows=[['item_id','reader_anonymous_code','first_pass_english_paraphrase','actor_object_scope_notes',
 'uncertainty_0_to_3','reader_confirmed_no_key_access']];
 for(let i=0;i<items.length;i++){
  const a=answers[i];if(!a||!a.paraphrase)continue;
  rows.push([items[i].item_id,code,a.paraphrase,a.roles,a.uncertainty,exposure]);
 }
 if(rows.length===1){$('studyError').textContent='No responses to export yet.';return;}
 const csv=rows.map(row=>row.map(csvCell).join(',')).join('\r\n')+'\r\n';
 const blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
 const url=URL.createObjectURL(blob);
 const link=document.createElement('a');link.href=url;link.download='qaroshi-reader-'+code+'.csv';
 document.body.appendChild(link);link.click();link.remove();URL.revokeObjectURL(url);
 $('studyError').textContent=(rows.length-1)+' first-pass responses exported. Keep the file private and share it only with your facilitator.';
}
$('export').addEventListener('click',exportCSV);
})();
</script></body></html>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reader", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.reader, args.out), indent=2))


if __name__ == "__main__":
    main()
