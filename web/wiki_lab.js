/* Qaroshi Wiki: reader-first grammar lab and transparent editorial case browser.
 * No remote services, no model API. This is only the licensed 9.3 sublanguage.
 */
(function(root){
  'use strict';
  const E=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const N=n=>Number(n).toLocaleString('en-US');
  const title=s=>String(s||'').replaceAll('_',' ').replace(/\b\w/g,x=>x.toUpperCase());
  const roles=['patient','recipient','goal','source','location','comitative'];
  const roleLabel={patient:'Object · -m',recipient:'Recipient · -tu',goal:'Destination · -gu',
    source:'Starting point · -de',location:'Location · -lo',comitative:'With someone · -wa'};
  const meanings={after:'After',before:'Before',when:'When / during',if:'If (open)',
    counterfactual:'If (unreal past)'};
  const ACTS={statement:'Statement',polar:'Yes/no question'};
  function choose(items,value){return items.map(x=>{
    const v=typeof x==='string'?x:x.value,label=typeof x==='string'?x:x.label;
    return '<option value="'+E(v)+'"'+(value===v?' selected':'')+'>'+E(label)+'</option>';
  }).join('')}
  function mountGrammar(host,data,options={}){
    const g=root.QaroshiGrammar.createGrammar(data.grammarLicenses,data.grammarFrames);
    const spec=g.spec;
    const example='sen mi mara-m tika-te.';
    const verbs=Object.entries(spec.verb_overrides).map(([value,info])=>({value,
      label:value+' · '+info.sense})).sort((a,b)=>a.label.localeCompare(b.label));
    const resonances=spec.allowed_resonances;
    const field=(label,key,options,initial='')=>'<label class="lab-field"><span>'+E(label)+'</span><select data-field="'+E(key)+'" class="field">'+choose(options,initial)+'</select></label>';
    const event=(which,verb)=>'<fieldset class="lab-event" data-event="'+which+'"><legend>'+ (which==='A'?'Main action':'Second action')+'</legend>'+
      '<div class="lab-event-controls">'+field('Verb',which+'-verb',verbs,verb)+
      field('Subject',which+'-actor',spec.nouns.map(n=>({value:n.form,label:n.form+' · '+n.gloss})),which==='A'?'mi':'ti')+
      roles.map(role=>'<div class="lab-role" data-role-wrap="'+which+'-'+role+'">'+
         field(roleLabel[role],which+'-'+role,[{value:'',label:'Not specified'}])+'</div>').join('')+
      field('Tense',which+'-tense',[{value:'',label:'Unmarked / present'},{value:'te',label:'Past · -te'},{value:'yu',label:'Future · -yu'}],'te')+
      field('Aspect',which+'-aspect',[{value:'',label:'None'},...spec.aspect_suffixes.filter(Boolean).map(x=>({value:x,label:'-'+x}))])+
      field('Modality',which+'-modal',[{value:'',label:'None'},{value:'ki',label:'Possible / able · -ki'},
         {value:'ho',label:'Permitted · -ho'},{value:'du',label:'Required · -du'}])+
      '<label class="lab-check"><input data-field="'+which+'-negated" type="checkbox"> Negate this action (nu)</label></div></fieldset>';
    host.innerHTML='<article class="readable lab-page">'+
      '<div class="article-header"><div class="article-kicker">Wiki / Write & understand</div>'+
      '<h1>Sentence workshop</h1><p class="article-sub">Build Qaroshi from grammatical roles or inspect a sentence. Runs locally, without a Python installation or API key.</p></div>'+
      '<div class="lab-notice"><strong>Source-licensed subset:</strong> 25 reviewed verbs and 10 noun forms. This checks structure and scope, not free English translation or independent human comprehension. Unsupported inputs are declined instead of guessed.</div>'+
      '<div class="lab-tabs" role="tablist" aria-label="Workshop tools">'+
      '<button type="button" role="tab" id="labTabBuild" aria-selected="true" aria-controls="labBuild" data-lab-tab="build">Build a sentence</button>'+
      '<button type="button" role="tab" id="labTabInspect" aria-selected="false" aria-controls="labInspect" data-lab-tab="inspect">Inspect Qaroshi</button></div>'+
      '<section id="labBuild" class="lab-section" role="tabpanel" aria-labelledby="labTabBuild">'+
      '<p class="muted">Choose who does what. Optional second actions use the same grammar rather than a memorized sentence template.</p>'+
      '<form id="labBuilder"><div class="lab-general">'+field('Opening resonance','resonance',resonances,'sen')+
      field('Sentence type','mood',[{value:'statement',label:'Statement'}, {value:'polar',label:'Yes/no question'}])+
      field('Evidence or attribution','attribution',[
        {value:'',label:'Direct statement'}, {value:'reported_to_speaker',label:'Someone told me'},
        {value:'unknown_whether',label:"I don't know whether"},
        {value:'si',label:'I witnessed this'}, {value:'ye',label:'I inferred this'}, {value:'hu',label:'Reported evidence'}])+
      field('Connect another action','relation',[{value:'single',label:'One action'},...Object.entries(meanings).map(([value,label])=>({value,label}))])+
      '</div><div class="lab-event-stack">'+event('A',(options.verb&&spec.verb_overrides[options.verb])?options.verb:'tika')+event('B','këmë')+'</div>'+
      '<button class="button primary" type="submit">Compose Qaroshi</button></form>'+
      '<div class="lab-result" id="labComposeResult" role="status" aria-live="polite"><p class="muted">Your composed sentence will appear here.</p></div></section>'+
      '<section id="labInspect" class="lab-section" role="tabpanel" aria-labelledby="labTabInspect" hidden>'+
      '<form id="labInspector"><label for="labText">Qaroshi sentence</label>'+
      '<textarea id="labText" class="lab-input" spellcheck="false" rows="4" maxlength="900">'+E(example)+'</textarea>'+
      '<div class="controls"><button class="button primary" type="submit">Inspect sentence</button>'+
      '<button class="button" type="button" id="labUseLast">Use my last composition</button></div></form>'+
      '<div class="lab-result" id="labInspectResult" role="status" aria-live="polite"><p class="muted">Inspect a licensed sentence to see its roles, tense, negation, evidence, and scope.</p></div>'+
      '</section><details class="lab-help"><summary>What this tool supports (and what it does not)</summary>'+
      '<p>It validates exact subject, object, recipient, goal, source, location and companion roles for the <strong>25 reviewed verbs</strong>. It handles tense, aspect, modal, negation, after/before/when/if links, quoted reports and direct questions. It does not yet parse arbitrary passive forms, relative clauses, creative word formations or every dictionary entry.</p>'+
      '<p>If a sentence is rejected here, that means it lies outside this tested subset, <em>not</em> that it is wrong in the full language. Source: <a href="#standard">Unified editorial grammar</a>.</p></details></article>';
    const $=id=>host.querySelector('#'+id);
    const fields=()=>new Map([...host.querySelectorAll('[data-field]')].map(el=>[el.dataset.field,el]));
    const get=k=>fields().get(k)?.value||'';
    let last='';
    const select=(k,opts,selected)=>{const el=fields().get(k);if(!el)return;
      el.innerHTML=choose(opts,opts.some(x=>(typeof x==='string'?x:x.value)===selected)?selected:opts[0]?.value||'');
    };
    function syncEvent(which){
      const verb=get(which+'-verb'),rule=spec.verb_overrides[verb];
      const actors=g.candidateNouns(verb,'subject');
      select(which+'-actor',actors.map(n=>({value:n.form,label:n.form+' · '+n.gloss})),get(which+'-actor'));
      for(const role of roles){
        const list=g.candidateNouns(verb,role),wrap=host.querySelector('[data-role-wrap="'+which+'-'+role+'"]');
        const required=role==='patient'&&g.frames.find(f=>f.lemma===verb)?.required_roles.includes('object:-m') ||
          role==='recipient'&&g.frames.find(f=>f.lemma===verb)?.frame==='V2';
        wrap.hidden=!list.length;
        if(!list.length)select(which+'-'+role,[{value:'',label:'Not licensed'}],'');
        else select(which+'-'+role,[
          ...(!required?[{value:'',label:'Not specified'}]:[]),
          ...list.map(n=>({value:n.form,label:n.form+' · '+n.gloss}))],get(which+'-'+role));
      }
    }
    function syncScope(){
      const two=get('relation')!=='single';
      host.querySelector('[data-event="B"]').hidden=!two;
      if(two && get('relation')==='counterfactual')
        fields().get('A-tense').value='te';
      const mood=get('mood'),attr=fields().get('attribution');
      if(mood==='polar'&&attr.value)attr.value='';
      const current=get('resonance');
      if(!resonances.includes(current))fields().get('resonance').value='sen';
    }
    function atom(which){
      const values={actor:get(which+'-actor'),verb:get(which+'-verb')};
      for(const role of roles)values[role]=get(which+'-'+role)||null;
      for(const tag of ['tense','aspect','modal'])values[tag]=get(which+'-'+tag);
      values.negated=fields().get(which+'-negated').checked;
      return g.atom(values);
    }
    function sentence(){
      const a=atom('A'),relation=get('relation'),p=relation==='single'?a:
        {type:'link',relation,first:a,second:atom('B')};
      const aType=get('attribution');
      return {proposition:p,resonance:get('resonance'),
        mood:get('mood'),attribution:['reported_to_speaker','unknown_whether'].includes(aType)?aType:'',
        evidential:['si','ye','hu'].includes(aType)?aType:''};
    }
    function pretty(s,analysis){
      const pieces=analysis.roles.map((a,i)=>{
        const details=[
          ['Actor',a.actor],['Verb',a.verb],['Object',a.patient],['Recipient',a.recipient],
          ['Destination',a.goal],['Source',a.source],['Location',a.location],['Companion',a.comitative],
          ['Tense',a.tense||'unmarked'],['Aspect',a.aspect||'none'],
          ['Modality',a.modal||'none'],['Negation',a.negated?'yes':'no']];
        return '<div class="lab-roles"><h3>Action '+(i+1)+'</h3><dl>'+details.filter(x=>x[1]!=null)
          .map(([k,v])=>'<div><dt>'+E(k)+'</dt><dd>'+E(v)+'</dd></div>').join('')+'</dl></div>';
      }).join('');
      return '<div class="lab-output"><div class="lab-output-head"><strong class="roman">'+E(s)+'</strong>'+
        '<button type="button" class="button" data-copy-qaroshi="'+E(s)+'">Copy</button></div>'+
        '<p class="muted">Structural reading: <strong>'+E(title(analysis.speech_act))+
        '</strong> · '+E(analysis.relation==='single'?'one action':title(analysis.relation))+
        (analysis.evidential?' · '+E(analysis.evidential):'')+
        ' · <strong>'+(analysis.matrix_event_asserted?'matrix event asserted':'matrix event not asserted')+'</strong></p>'+
        '<div class="lab-actions">'+pieces+'</div><p class="lab-caveat">This describes the licensed grammar structure, not an independently verified English translation.</p></div>';
    }
    function errorPlace(dest,error){
      dest.innerHTML='<p class="lab-error"><strong>Not supported by this grammar subset.</strong> '+E(error.message||error)+
        '</p><p class="muted">Try a reviewed verb and the suggested actor/object choices. A rejection does not prove the phrase is impossible in Qaroshi.</p>';
    }
    $('labBuilder').addEventListener('change',e=>{
      const k=e.target?.dataset?.field||'';
      if(k==='A-verb')syncEvent('A');
      if(k==='B-verb')syncEvent('B');
      if(k==='relation'||k==='mood')syncScope();
    });
    $('labBuilder').addEventListener('submit',e=>{
      e.preventDefault();
      try{
        const s=g.render(sentence()),parsed=g.parse(s);
        last=s;$('labComposeResult').innerHTML=pretty(s,g.meaning(parsed));
      }catch(err){errorPlace($('labComposeResult'),err);}
    });
    $('labInspector').addEventListener('submit',e=>{
      e.preventDefault();
      try{
        const s=$('labText').value.trim(),parsed=g.parse(s);
        $('labInspectResult').innerHTML=pretty(s,g.meaning(parsed));
      }catch(err){errorPlace($('labInspectResult'),err);}
    });
    $('labUseLast').addEventListener('click',()=>{
      $('labText').value=last||example;
      $('labInspector').requestSubmit();
    });
    host.querySelectorAll('[data-lab-tab]').forEach(button=>button.addEventListener('click',()=>{
      const tab=button.dataset.labTab,isBuild=tab==='build';
      $('labBuild').hidden=!isBuild;$('labInspect').hidden=isBuild;
      $('labTabBuild').setAttribute('aria-selected',String(isBuild));
      $('labTabInspect').setAttribute('aria-selected',String(!isBuild));
      (isBuild?$('labTabBuild'):$('labTabInspect')).focus();
    }));
    host.querySelector('.lab-page').addEventListener('click',e=>{
      const b=e.target.closest('[data-copy-qaroshi]');if(!b)return;
      const value=b.dataset.copyQaroshi;
      if(navigator.clipboard?.writeText)navigator.clipboard.writeText(value).then(()=>b.textContent='Copied').catch(()=>{b.textContent='Select the text to copy';});
      else b.textContent='Select the text to copy';
    },{once:false});
    syncEvent('A');syncEvent('B');syncScope();
    return g;
  }
  function renderCases(host,data,requestedId=''){
    const cases=data.semanticCases||[];
    const map=new Map(cases.map(x=>[x.id,x]));
    const domains=[...new Set(cases.map(x=>x.domain))].sort();
    const prettyScope=s=>title(s).replaceAll('Past ', 'Past ');
    if(requestedId){
      const item=map.get(requestedId);
      if(!item){host.innerHTML='<article><h1>Case not found</h1><p><a href="#cases">Browse all cases</a></p></article>';return;}
      host.innerHTML='<article class="readable case-page">'+
        '<p class="article-kicker"><a href="#cases">Semantic cases</a> / '+E(item.id)+'</p><h1>Review '+E(item.id)+'</h1>'+
        '<div class="lab-notice"><strong>Editorial proposal, not independently confirmed.</strong> The English below is the source intention, not a certified translation of what a reader would understand.</div>'+
        '<h2>Proposed Qaroshi</h2><div class="quote"><strong class="roman">'+E(item.qaroshi)+'</strong></div>'+
        '<h2>Original English target</h2><p>'+E(item.english)+'</p>'+
        '<h2>Scope and source roles</h2><p>'+E(prettyScope(item.scope))+'</p>'+
        '<dl class="case-roles">'+Object.entries(item.roles||{}).map(([k,v])=>'<div><dt>'+E(title(k))+'</dt><dd>'+E(v)+'</dd></div>').join('')+'</dl>'+
        '<p class="lab-caveat">Source: '+E(item.source_status)+'. Independent human meaning review: '+E(item.review_status)+
        '. This is not an official native-speaker endorsement.</p>'+
        '<p><a class="button" href="#workshop">Check a sentence in the limited grammar workshop</a></p></article>';
      return;
    }
    host.innerHTML='<article class="readable case-page"><div class="article-header"><div class="article-kicker">Wiki / Meaning & evidence</div>'+
      '<h1>Semantic case library</h1><p class="article-sub">All 500 original challenge cases, with proposed Qaroshi and source-English meaning requirements. Explore truth conditions, actors, and references.</p></div>'+
      '<div class="lab-notice">All 500 translations are <strong>editorial candidates</strong>. They have not passed independent human comprehension testing. This is a transparent reference, not a certification score.</div>'+
      '<div class="controls"><input id="caseQuery" type="search" class="field search" placeholder="Search English, Qaroshi or QS81 case ID" aria-label="Search semantic cases">'+
      '<select id="caseDomain" class="field select" aria-label="Filter semantic case domain">'+
      choose([{value:'',label:'All 10 areas'},...domains.map(x=>({value:x,label:title(x)}))])+'</select></div>'+
      '<p id="caseCounter" class="muted" role="status" aria-live="polite"></p>'+
      '<div id="caseList" class="case-list"></div><button type="button" class="button" id="caseMore">Show more</button>'+
      '<details class="lab-help"><summary>How to use these cases for practice</summary><p>Try reading Qaroshi first, hiding the original English, and writing your own paraphrase. Then compare the roles and original intent. This is not an independently scored study unless a separate blind reviewer records the response.</p></details></article>';
    const $=id=>host.querySelector('#'+id);
    let limit=24;
    const show=()=>{
      const q=$('caseQuery').value.trim().toLowerCase(),domain=$('caseDomain').value;
      const selected=cases.filter(x=>(!domain||x.domain===domain)&&(!q||
        [x.id,x.english,x.qaroshi,x.scope].some(y=>String(y).toLowerCase().includes(q))));
      $('caseCounter').textContent=N(selected.length)+' matches · '+N(Math.min(limit,selected.length))+' shown';
      $('caseList').innerHTML=selected.slice(0,limit).map(x=>'<a class="case-item" href="#case/'+E(x.id)+'">'+
        '<span class="case-label">'+E(x.id)+' · '+E(title(x.domain))+'</span>'+
        '<strong>'+E(x.qaroshi)+'</strong><span>'+E(x.english)+'</span></a>').join('')||
        '<p class="empty">No cases match. Try a different word or area.</p>';
      $('caseMore').hidden=selected.length<=limit;
    };
    $('caseQuery').addEventListener('input',()=>{limit=24;show();});
    $('caseDomain').addEventListener('change',()=>{limit=24;show();});
    $('caseMore').addEventListener('click',()=>{limit+=24;show();});
    show();
  }
  root.QaroshiWikiLab=Object.freeze({mountGrammar,renderCases});
})(typeof window!=='undefined'?window:globalThis);
