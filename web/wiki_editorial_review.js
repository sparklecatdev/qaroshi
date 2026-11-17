/* Qaroshi 10.1: private editorial-review workbench.
 * This collects PROPOSALS and provenance notes, never changes source data,
 * never sets "approved", never contacts a server or records human outcomes.
 */
(function(root){
'use strict';
const E=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=s=>String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
const N=n=>Number(n).toLocaleString('en-US');
const VERDICTS={
 needs_definition:'Needs a precise sense definition',
 needs_boundary:'Clarify semantic/selection boundary',
 needs_example:'Needs a source-reviewed example',
 contradictory:'Possible conflict with prior source',
 no_issue_noted:'No issue noted in this editorial pass'
};
function create(data){
 const std=data.standard10||{};
 const byWord=new Map((data.words||[]).map(w=>[w.qaroshi,w]));
 const priority=Object.entries(std.priorities||{})
   .map(([form,meta])=>({word:byWord.get(form),meta}))
   .filter(x=>!!x.word).sort((a,b)=>a.meta.rank-b.meta.rank);
 const controlled=(data.phrases||[]);
 const indexed=root.QaroshiUsage.sourceIndex(controlled,
   new Map((data.words||[]).map(w=>[w.qaroshi.toLowerCase(),w])),data.affixes||[]);
 function mount(host,options={}){
   const notes=new Map();
   let shown=20,filtered=[],active='';
   host.innerHTML='<article class="readable editorial-workbench">'+
     '<div class="article-header"><div class="article-kicker">Wiki / Research workflow</div>'+
     '<h1>Lexical editorial review desk</h1>'+
     '<p class="article-sub">Inspect source meanings, previous sense decisions, examples and evidence gaps for the 800 prioritized words. Record precise suggested corrections for an independent editor.</p></div>'+
     '<div class="lab-notice"><strong>Editorial working notes, not approved language changes.</strong>'+
     ' No forms, definitions, utterances or human review scores are modified by this page. Your work stays in memory until you export it locally.</div>'+
     '<div class="controls"><input id="editorialQuery" type="search" class="field search" placeholder="Search word, meaning or topic…" aria-label="Search priority lexemes">'+
     '<select id="editorialFilter" class="field select" aria-label="Filter review needs">'+
     '<option value="">All priority words</option>'+
     '<option value="no-profile">Without authored definition</option>'+
     '<option value="no-example">Without original corpus example</option>'+
     '<option value="sense">Previously curated senses</option>'+
     '<option value="draft">Has unreviewed proposal</option></select></div>'+
     '<p class="muted" id="editorialCount" role="status" aria-live="polite"></p>'+
     '<div id="editorialItems"></div><button class="button" id="editorialMore" type="button">Show more priority words</button>'+
     '<div class="editorial-export"><div><strong>Private reviewer notes</strong>'+
     '<p class="muted small" id="editorialSaved">No notes entered. No repository data has been changed.</p></div>'+
     '<button type="button" class="button primary" id="editorialDownload">Export editorial proposals (JSON)</button></div>'+
     '<details class="lab-help"><summary>Evidence and acceptance rules</summary>'+
     '<p>Existing authored definitions and curated sense records are earlier editorial work, not proof of independent comprehension. The priority index is a review inventory. Existing 5,000-card examples are unreviewed proposals and must not be used as native-speaker attestations.</p>'+
     '<p>Review an example by checking its lemma, intended argument roles, grammatical form, semantic restriction and source license. Exported notes are <strong>unverified suggestions</strong>; no option in this workbench certifies meanings, claims independent participants, or automatically edits the lexicon.</p>'+
     '<p>For independent readers, see the <a href="#validation">trial protocol</a>. For connected contexts, see <a href="#conversations">source-labeled conversation scenes</a>.</p></details></article>';
   const $=id=>host.querySelector('#'+id);
   if(options.word)$('editorialQuery').value=String(options.word);
   const note=x=>notes.get(x)||{verdict:'',definition:'',restriction:'',contrast:'',example_id:'',comment:''};
   function saveVisible(){
     for(const form of active){
       const n={};
       const article=[...host.querySelectorAll('[data-editorial-form]')].find(x=>x.dataset.editorialForm===form);
       if(!article)continue;
       for(const key of ['verdict','definition','restriction','contrast','example_id','comment']){
         n[key]=article.querySelector('[data-review-field="'+key+'"]')?.value.trim()||'';
       }
       if(Object.values(n).some(Boolean))notes.set(form,n);
       else notes.delete(form);
     }
     $('editorialSaved').textContent=N(notes.size)+' editorial proposal(s) in page memory. Nothing is automatically approved or uploaded.';
   }
   function renderItem({word:w,meta}){
     const prof=std.profiles?.[w.qaroshi],senses=std.senses?.[w.qaroshi]||[],
       draft=std.draft_cards?.[w.qaroshi],examples=(indexed.get(w.qaroshi.toLowerCase())||[]).slice(0,3);
     const n=note(w.qaroshi);
     const rows=Object.entries(VERDICTS).map(([value,label])=>
       '<option value="'+E(value)+'"'+(n.verdict===value?' selected':'')+'>'+E(label)+'</option>').join('');
     return '<section class="editorial-entry" data-editorial-form="'+E(w.qaroshi)+'">'+
       '<div class="editorial-entry-head"><div><small>Priority '+E(meta.rank)+' · '+E(w.pos)+' · '+E(w.domain)+'</small>'+
       '<h2><a href="#word/'+encodeURIComponent(w.qaroshi)+'">'+E(w.qaroshi)+'</a></h2>'+
       '<p><strong>Canonical gloss:</strong> '+E(w.english)+'</p></div>'+
       '<span class="word-chip">'+E(examples.length?'Corpus occurrence(s)':'No source corpus example')+'</span></div>'+
       (prof?'<div class="editorial-source"><strong>Earlier individually authored definition</strong><p>'+E(prof.definition)+'</p>'+
         (prof.restriction?'<p><b>Boundary:</b> '+E(prof.restriction)+'</p>':'')+
         (prof.contrast?'<p><b>Contrast:</b> '+E(prof.contrast)+'</p>':'')+
         '<small>'+E(prof.profile_id)+' · '+E(prof.reviewer_status)+'</small></div>':
         '<p class="muted small">No individually authored sense definition is linked to this entry.</p>')+
       (senses.length?'<details><summary>Prior curated sense distinctions ('+senses.length+')</summary>'+
         senses.map(s=>'<p><strong>'+E(s.label)+':</strong> '+E(s.definition)+
          ' <small>'+E(s.sense_id)+' · '+E(s.source_status)+'</small></p>').join('')+'</details>':'')+
       (examples.length?'<details><summary>Original teaching examples ('+examples.length+' shown)</summary>'+
         examples.map(e=>'<p><code>'+E(e.sentence.qaroshi)+'</code><br>'+E(e.sentence.english)+
           ' <a href="#phrase/'+encodeURIComponent(e.sentence.id)+'">Source '+E(e.sentence.id)+'</a></p>').join('')+
         '</details>':'')+
       (draft?'<details><summary>Unreviewed legacy draft · never accepted automatically</summary>'+
         '<p>'+E(draft.candidate_qaroshi)+' · '+E(draft.candidate_english)+'</p>'+
         '<small>'+E(draft.status)+'</small></details>':'')+
       '<fieldset class="editorial-fields"><legend>Draft review notes (not an approval)</legend>'+
       '<label>Issue / follow-up category<select class="field" data-review-field="verdict">'+
         '<option value="">No notes yet</option>'+rows+'</select></label>'+
       '<label>Suggested definition (only if source-grounded)<textarea rows="2" data-review-field="definition" placeholder="Do not infer a new sense from an English homonym">'+E(n.definition)+'</textarea></label>'+
       '<label>Context or selection restriction<textarea rows="2" data-review-field="restriction">'+E(n.restriction)+'</textarea></label>'+
       '<label>Contrast or possible false friend<textarea rows="2" data-review-field="contrast">'+E(n.contrast)+'</textarea></label>'+
       '<label>Source example ID (not a fabricated citation)<input class="field" data-review-field="example_id" value="'+E(n.example_id)+'"></label>'+
       '<label>Rationale and unresolved questions<textarea rows="2" data-review-field="comment">'+E(n.comment)+'</textarea></label>'+
       '</fieldset></section>';
   }
   function draw(){
     const query=norm($('editorialQuery').value),filter=$('editorialFilter').value;
     filtered=priority.filter(({word:w,meta})=>{
       const profile=std.profiles?.[w.qaroshi],senses=std.senses?.[w.qaroshi]||[];
       const draft=std.draft_cards?.[w.qaroshi];
       if(filter==='no-profile'&&(profile||senses.length))return false;
       if(filter==='no-example'&&indexed.get(w.qaroshi.toLowerCase())?.length)return false;
       if(filter==='sense'&&!senses.length)return false;
       if(filter==='draft'&&!draft)return false;
       return !query||[w.qaroshi,w.english,w.domain].some(x=>norm(x).includes(query));
     });
     const visible=filtered.slice(0,shown);
     active=visible.map(x=>x.word.qaroshi);
     $('editorialCount').textContent=N(filtered.length)+' prioritized entries match · '+N(visible.length)+' displayed';
     $('editorialItems').innerHTML=visible.map(renderItem).join('')||
       '<p class="muted">No source entries match those filters.</p>';
     $('editorialMore').hidden=shown>=filtered.length;
   }
   for(const id of ['editorialQuery','editorialFilter'])$(id).addEventListener('input',()=>{
     saveVisible();shown=20;draw();
   });
   $('editorialMore').addEventListener('click',()=>{saveVisible();shown+=20;draw()});
   $('editorialItems').addEventListener('input',()=>saveVisible());
   $('editorialDownload').addEventListener('click',()=>{
     saveVisible();
     if(!notes.size){$('editorialSaved').textContent='Add at least one note before exporting.';return;}
     const proposals=[...notes.entries()].map(([lemma,fields])=>{
       const w=byWord.get(lemma);
       return {dictionary_id:w.id,lemma,original_gloss:w.english,
         ...fields,status:'UNREVIEWED_EDITORIAL_PROPOSAL_NOT_APPROVED',
         attestation:'no independent human comprehension recorded'};
     });
     const blob=new Blob([JSON.stringify({schema:'qaroshi-editorial-notes-v1',
       source_standard:'10.1',proposals},null,2)],{type:'application/json;charset=utf-8'});
     const uri=URL.createObjectURL(blob),a=document.createElement('a');
     a.href=uri;a.download='qaroshi-editorial-review-proposals.json';
     document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(uri);
   });
   draw();
   return {getNotes:()=>[...notes.entries()].map(([lemma,v])=>({lemma,...v})),counts:{priority:priority.length}};
 }
 return Object.freeze({mount,prioritized:priority.length,verdicts:VERDICTS});
}
root.QaroshiEditorial=Object.freeze({create});
})(typeof window!=='undefined'?window:globalThis);
