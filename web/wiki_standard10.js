/* Qaroshi Standard 10: editorial sense evidence + connected dialogue + drills.
 * Standalone browser bundle. No server, no artificial human endorsement.
 */
(function(root){
  'use strict';
  const E=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const key=x=>String(x??'').normalize('NFC').toLowerCase();
  const title=s=>String(s||'').replace(/[_-]+/g,' ').replace(/\b[a-z]/g,c=>c.toUpperCase());
  const n=x=>Number(x).toLocaleString('en-US');
  const policy='Editorial source material. No independent fluent-reader ratification or verified idiomaticity.';
  function create(data){
    const corpus=data.standard10||{};
    const profiles=corpus.profiles||{},senses=corpus.senses||{},priorities=corpus.priorities||{};
    const drafts=corpus.draft_cards||{},dialogues=corpus.dialogues||[],drills=corpus.controlled_drills||[];
    const byDialogue=new Map(dialogues.map(d=>[d.id,d]));
    const byDrill=new Map(drills.map(d=>[d.id,d]));
    const wordMap=new Map((data.words||[]).map(w=>[key(w.qaroshi),w]));
    const affixes=data.affixes||[];
    const licenses=new Set(['case','nominal','discourse','tense','aspect','modality','manner','voice']);
    const suffixes=new Set(affixes.filter(a=>licenses.has(a.category)).map(a=>a.form));
    for(const extra of ['-m','-te','-yu','-ho','-ki','-du','-ri','-lo','-na'])suffixes.add(extra);
    function links(text){
      // Preserve the original punctuation, and link ONLY a whole canonical
      // token or a source-licensed inflected token. Compound substrings are
      // not independent word hits.
      return String(text||'').split(/([A-Za-zëË]+(?:-[A-Za-zëË]+)*)/g).map(part=>{
        if(!/^[A-Za-zëË]+(?:-[A-Za-zëË]+)*$/.test(part))return E(part);
        const result=root.QaroshiUsage.resolveToken(part,wordMap,suffixes);
        const w=result&&wordMap.get(result.headword);
        return w?'<a class="std10-lex" href="#word/'+encodeURIComponent(w.qaroshi)+'" title="'+E(w.english)+'">'+E(part)+'</a>':E(part);
      }).join('');
    }
    function sensesHTML(word){
      const form=word.qaroshi,p=profiles[form],ss=senses[form]||[],priority=priorities[form],draft=drafts[form];
      const count=ss.length+(p?1:0);
      return '<section class="std10-senses" id="sense-details">'+
        '<div class="word-section-title"><div><span class="word-section-kicker">Source meanings & distinctions</span><h2>Definition and sense notes</h2></div><span class="word-section-counter">'+
        (count?n(count)+' editorial distinctions':'Reference gloss only')+'</span></div>'+
        '<p class="muted small">The English dictionary gloss is the source entry. A sense is shown separately only when an earlier editor actually documented that distinction. A selected English synonym alone does not create new polysemy.</p>'+
        (p?'<div class="std10-profile"><strong>Individually authored explanation</strong><p>'+E(p.definition)+'</p>'+
          (p.restriction?'<p><strong>Where not to use it:</strong> '+E(p.restriction)+'</p>':'')+
          (p.contrast?'<p><strong>Distinguish from:</strong> '+E(p.contrast)+'</p>':'')+
          (p.qaroshi_example?'<p class="std10-example-editor"><b>Earlier editorial example:</b> <code>'+E(p.qaroshi_example)+'</code>'+
            (p.english_example?' · '+E(p.english_example):'')+
            '<small>Author-edited contextual line, not independent speaker attestation</small></p>':'')+
          '<small>'+E(p.meaning_status)+' · '+E(p.reviewer_status)+' · '+E(p.profile_id)+'</small></div>':'')+
        (ss.length?'<div class="std10-sense-list">'+ss.map((s,i)=>
          '<div class="std10-sense"><span class="std10-sense-number">'+(i+1)+'</span><div><strong>'+E(s.label)+'</strong>'+
          '<p>'+E(s.definition)+'</p>'+(s.construction?'<div class="std10-construction">Documented construction: <code>'+E(s.construction)+'</code></div>':'')+
          '<small>'+E(s.sense_id)+' · '+E(s.source_status)+' · independently unverified</small></div></div>').join('')+'</div>':
          (p?'':'<p class="std10-no-sense">No separately reviewed sense definition exists for this word yet. Use its canonical gloss, grammar description and source examples without treating an English homonym as an extra Qaroshi sense.</p>'))+
        (priority?'<details class="std10-priority"><summary>Core lexicon review evidence · priority '+E(priority.rank)+'</summary>'+
          '<p>Recorded corpus occurrences: '+n(priority.corpus_mentions)+'. Known source IDs: '+E(priority.source_reference_ids||'none')+'</p>'+
          '<p>'+E(priority.gloss_interpretation)+'</p><p>Source status: '+E(priority.lexical_treatment)+'. Speaker attestation: '+E(priority.speaker_attestation)+'</p>'+
          '<small>'+E(priority.source)+'</small></details>':'')+
        (draft?'<details class="std10-proposal"><summary>Unreviewed candidate card · NOT an approved additional sense</summary>'+
          '<p><strong>Selected canonical gloss:</strong> '+E(draft.selected_reference_gloss)+'</p>'+
          '<p><strong>Unreviewed candidate line:</strong> <code>'+E(draft.candidate_qaroshi)+'</code></p>'+
          '<p>'+E(draft.candidate_english)+'</p>'+
          '<p class="muted small">Research-only draft, explicitly not source-attested conversation, independently verified translation, conventional synonym or approved polysemy.</p>'+
          '<small>'+E(draft.sense_id)+' · '+E(draft.source)+' · '+E(draft.status)+'</small></details>':'')+
        '<p class="muted small">Coverage is editorial and evidence-graded, never a claim of independently observed human usage.</p></section>';
    }
    function dialogueIndex(host){
      const stats=corpus.manifest||{};
      host.innerHTML='<article class="readable std10-library">'+
        '<div class="article-header"><div class="article-kicker">Wiki / Everyday speech</div><h1>Conversations in context</h1>'+
        '<p class="article-sub">'+n(dialogues.length)+' connected editorial scenarios with '+n(stats.conversation_turns||0)+' recorded turns. Read Qaroshi first, then reveal the source English and literal distinction.</p></div>'+
        '<div class="lab-notice">'+E(policy)+' The source-linked conversation paths reuse documented reference phrases; conversational sequencing is editorial, not observed spontaneous speech.</div>'+
        '<div class="controls"><input class="field search" type="search" id="std10DialogueSearch" aria-label="Search conversations" placeholder="Search situations, meanings or Qaroshi…">'+
        '<select class="field select" id="std10DialogueType" aria-label="Source type"><option value="">All sources</option>'+
        '<option value="original11/">Individually authored scenes</option><option value="source18/">Recombined source-phrase scenes</option></select></div>'+
        '<p class="muted" id="std10DialogueCount" aria-live="polite"></p><div class="std10-dialogue-list" id="std10DialogueList"></div>'+
        '<button type="button" class="button" id="std10MoreDialogue">Show more conversations</button>'+
        '<div class="foot"><a href="#drills">Sentence drills</a> · <a href="#validation">Comprehension trial protocol</a> · <a href="#practice">Vocabulary practice</a></div></article>';
      const $=id=>host.querySelector('#'+id);
      let limit=16;
      const draw=()=>{
        const term=key($('std10DialogueSearch').value.trim()),kind=$('std10DialogueType').value;
        const matches=dialogues.filter(d=>(!kind||d.id.startsWith(kind))&&(!term||
          [d.title,d.context,d.domain,...d.turns.flatMap(t=>[t.qaroshi,t.english])].some(s=>key(s).includes(term))));
        $('std10DialogueCount').textContent=n(matches.length)+' conversations found';
        $('std10DialogueList').innerHTML=matches.slice(0,limit).map(d=>
          '<a class="std10-dialogue-card" href="#conversation/'+encodeURIComponent(d.id)+'">'+
          '<span class="std10-dialogue-kind">'+(d.id.startsWith('original11/')?'Original editorial scene':'Source-linked reconstruction')+
          ' · '+n(d.turns.length)+' turns</span><strong>'+E(d.title)+'</strong><span>'+E(d.context)+'</span></a>').join('')||
          '<p class="muted">No scenes match this query.</p>';
        $('std10MoreDialogue').hidden=matches.length<=limit;
      };
      $('std10DialogueSearch').addEventListener('input',()=>{limit=16;draw()});
      $('std10DialogueType').addEventListener('change',()=>{limit=16;draw()});
      $('std10MoreDialogue').addEventListener('click',()=>{limit+=16;draw()});
      draw();
    }
    function conversation(host,id){
      const d=byDialogue.get(id);
      if(!d){host.innerHTML='<article class="readable"><h1>Conversation not found</h1><a href="#conversations">Browse conversations</a></article>';return;}
      host.innerHTML='<article class="readable std10-conversation">'+
        '<div class="word-back"><a href="#conversations">Conversations</a> / '+E(d.id)+'</div>'+
        '<div class="article-header"><div class="article-kicker">'+E(d.domain)+'</div><h1>'+E(d.title)+'</h1><p class="article-sub">'+E(d.context)+'</p></div>'+
        '<div class="lab-notice"><strong>Editorial scene, not a natural conversation recording.</strong> '+
          E(d.status)+' · '+E(policy)+'</div>'+
        '<div class="std10-conversation-actions"><button class="button primary" type="button" id="std10AllEnglish">Reveal all English</button>'+
        '<button class="button" type="button" id="std10HideEnglish">Hide all English</button>'+
        '<span class="muted small">Click Qaroshi words to open their definitions</span></div>'+
        '<div class="std10-turns">'+d.turns.map((t,i)=>{
          const name='std10-en-'+i;
          return '<section class="std10-turn"><div class="std10-speaker">'+E(t.speaker)+' · '+n(i+1)+'</div>'+
            '<div class="std10-qaroshi" lang="x-qaroshi">'+links(t.qaroshi)+'</div>'+
            (t.sound_out?'<div class="ipa-small">'+E(t.sound_out)+'</div>':'')+
            '<div class="std10-turn-reveal"><button class="button" type="button" data-english="'+name+'" aria-expanded="false">Show meaning</button></div>'+
            '<div class="std10-english" id="'+name+'" hidden><p><strong>Contextual editorial English:</strong> '+E(t.english)+'</p>'+
            (t.literal_english&&t.literal_english!==t.english?'<p><strong>Literal parser gloss:</strong> '+E(t.literal_english)+'</p>':'')+
            '<p class="muted small">'+E(t.status)+
            (t.reference_id?' · <a href="#phrase/'+encodeURIComponent(t.reference_id)+'">Original phrase '+E(t.reference_id)+'</a>':'')+
            '</p></div></section>';
        }).join('')+'</div>'+
        '<p class="lab-caveat">This dialogue is a controlled editorial teaching script. Reading it without English can be useful practice, but it does not count as blind human testing when the answer is accessible on this same page.</p>'+
        '<div class="foot"><a href="#conversations">Other situations</a> · <a href="#drills">Controlled sentence drills</a> · <a href="#validation">Independent-reader trial design</a></div></article>';
      host.querySelectorAll('[data-english]').forEach(button=>button.addEventListener('click',()=>{
        const node=host.querySelector('#'+button.dataset.english);
        node.hidden=!node.hidden;
        button.setAttribute('aria-expanded',String(!node.hidden));
        button.textContent=node.hidden?'Show meaning':'Hide meaning';
      }));
      const setAll=reveal=>{
        host.querySelectorAll('[data-english]').forEach(button=>{
          const node=host.querySelector('#'+button.dataset.english);
          node.hidden=!reveal;button.setAttribute('aria-expanded',String(reveal));
          button.textContent=reveal?'Hide meaning':'Show meaning';
        });
      };
      host.querySelector('#std10AllEnglish').addEventListener('click',()=>setAll(true));
      host.querySelector('#std10HideEnglish').addEventListener('click',()=>setAll(false));
    }
    function drillLibrary(host){
      host.innerHTML='<article class="readable std10-drills">'+
        '<div class="article-header"><div class="article-kicker">Wiki / Guided examples</div><h1>Controlled sentence drills</h1>'+
        '<p class="article-sub">'+n(drills.length)+' existing machine-round-tripped bilingual pairs, available here to practice grammar and common lexical combinations.</p></div>'+
        '<div class="lab-notice"><strong>Machine-controlled training patterns only.</strong> Each line has a deterministic translation/backtranslation check, NOT independent semantic equivalence or speaker usage. Separate from the <a href="#phrases">original teaching examples</a> and <a href="#conversations">editorial dialogues</a>.</div>'+
        '<div class="controls"><input class="field search" id="std10DrillSearch" type="search" placeholder="Search meanings, verbs and cases..." aria-label="Search controlled drills">'+
        '<select class="field select" id="std10DrillDirection" aria-label="Choose language to reveal"><option value="qr">Read Qaroshi first</option><option value="en">Read English first</option></select></div>'+
        '<p class="muted" id="std10DrillCount" aria-live="polite"></p><div class="std10-drill-list" id="std10DrillList"></div>'+
        '<button class="button" id="std10MoreDrills" type="button">Show more practice pairs</button></article>';
      const $=id=>host.querySelector('#'+id);
      let limit=20;
      const draw=()=>{
        const q=key($('std10DrillSearch').value),direction=$('std10DrillDirection').value;
        const matches=drills.filter(d=>!q||key(d.english).includes(q)||key(d.qaroshi).includes(q));
        $('std10DrillCount').textContent=n(matches.length)+' draft-controlled pairs';
        $('std10DrillList').innerHTML=matches.slice(0,limit).map(d=>
          '<div class="std10-drill"><span class="std10-drill-id">'+E(d.id)+'</span><div class="std10-drill-prompt">'+
          (direction==='qr'?links(d.qaroshi):E(d.english))+'</div>'+
          '<button type="button" class="button" aria-expanded="false" data-drill="'+E(d.id)+'">Reveal editorial answer</button>'+
          '<div class="std10-drill-answer" data-answer="'+E(d.id)+'" hidden>'+
          '<p><strong>'+(direction==='qr'?'English target':'Proposed Qaroshi')+':</strong> '+
          (direction==='qr'?E(d.english):links(d.qaroshi))+'</p>'+
          (d.backtranslated_english&&d.backtranslated_english!==d.english?'<p><strong>Roundtrip:</strong> '+E(d.backtranslated_english)+'</p>':'')+
          (d.warning?'<p class="muted small">'+E(d.warning)+'</p>':'')+
          '</div></div>').join('')||'<p class="muted">No matching drill.</p>';
        $('std10MoreDrills').hidden=matches.length<=limit;
      };
      $('std10DrillSearch').addEventListener('input',()=>{limit=20;draw()});
      $('std10DrillDirection').addEventListener('change',draw);
      $('std10MoreDrills').addEventListener('click',()=>{limit+=20;draw()});
      host.querySelector('#std10DrillList').addEventListener('click',event=>{
        const btn=event.target.closest('[data-drill]');if(!btn)return;
        const id=btn.dataset.drill;
        const ans=[...host.querySelectorAll('[data-answer]')].find(x=>x.dataset.answer===id);
        if(!ans)return;ans.hidden=!ans.hidden;
        btn.textContent=ans.hidden?'Reveal editorial answer':'Hide editorial answer';
        btn.setAttribute('aria-expanded',String(!ans.hidden));
      });
      draw();
    }
    function validation(host){
      const m=corpus.manifest||{};
      host.innerHTML='<article class="readable std10-validation">'+
        '<div class="article-header"><div class="article-kicker">Wiki / Research & validation</div>'+
        '<h1>Independent comprehension testing</h1>'+
        '<p class="article-sub">An experiment is specified and exportable, but it has no independent participants yet. Never turn automated coverage into evidence of human understanding.</p></div>'+
        '<div class="lab-notice"><strong>Current independent reader outcomes: 0.</strong> The original editorial answer keys have not been ratified by readers unfamiliar with Qaroshi. Existing drills and dialogue English keys are self-study, not blind experimental evidence.</div>'+
        '<h2>What a real trial requires</h2>'+
        '<ol><li>Recruit consenting readers who did not author these materials.</li>'+
        '<li>Distribute Qaroshi-only stimuli in a separate file; do not show the answer key or this answer-revealing Wiki.</li>'+
        '<li>Collect first-pass translations, actor/object and negation/consent/evidence distinctions, plus explicit uncertainty.</li>'+
        '<li>Have a separate human adjudicator assess preserved, partial, incorrect or indeterminate meaning and document disputed source glosses.</li>'+
        '<li>Publish anonymized denominators, failures, disagreements and protocol limitations. Do not publish identifying data or retroactively call self-study blind.</li></ol>'+
        '<h2>Reproducible source experiment</h2>'+
        '<p>On the repository, build an 80-item balanced evaluation pack from the original scene sources:</p>'+
        '<pre class="code"><code>python tools/standard10/trial.py --build --out trial-export</code></pre>'+
        '<p>The generated bundle separates <code>learner_blind_items.csv</code> from <code>facilitator_english_key.csv</code>. This separation is procedural, not cryptographic secrecy. A filled form can be manually adjudicated and scored only after real responses are provided:</p>'+
        '<pre class="code"><code>python tools/standard10/trial.py --score filled_responses.csv --out evaluation.json</code></pre>'+
        '<p>See the <a href="https://github.com/sparklecatdev/qaroshi/blob/main/tools/standard10/trial.py" target="_blank" rel="noopener">complete open trial script</a> and its generated PROTOCOL.md. Scores describe human-supplied judgments; the script cannot authenticate participants or certify idiomaticity.</p>'+
        '<h2>Evidence inventory</h2>'+
        '<dl class="case-roles"><div><dt>Words in core dictionary</dt><dd>'+n(m.canonical_words||0)+'</dd></div>'+
        '<div><dt>Individually authored lexical profiles</dt><dd>'+n(m.core_individually_authored_profiles||0)+'</dd></div>'+
        '<div><dt>Earlier editorial sense descriptions</dt><dd>'+n(m.previous_editorial_sense_descriptions||0)+'</dd></div>'+
        '<div><dt>Unreviewed sense-candidate cards</dt><dd>'+n(m.unreviewed_gloss_selection_and_example_cards||0)+'</dd></div>'+
        '<div><dt>Connected editorial conversations</dt><dd>'+n(m.editorial_conversations||0)+'</dd></div>'+
        '<div><dt>Controlled, unverified sentence drills</dt><dd>'+n(m.machine_roundtrip_drills||0)+'</dd></div>'+
        '<div><dt>Human blind comprehension trials</dt><dd>0</dd></div></dl>'+
        '<p class="lab-caveat">No sourced lexeme or existing contributor entry has been silently rewritten to make these metrics look better.</p></article>';
    }
    return Object.freeze({sensesHTML,dialogueIndex,conversation,drillLibrary,validation,
      counts:{dialogues:dialogues.length,drills:drills.length,
        coreProfiles:Object.keys(profiles).length,curatedEntries:Object.keys(senses).length,
        proposals:Object.keys(drafts).length}});
  }
  root.Qaroshi10=Object.freeze({create});
})(typeof window!=='undefined'?window:globalThis);
