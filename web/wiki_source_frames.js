/* Qaroshi 11.2: strict, source-anchored offline verb experiment.
 * Derived forms are explicitly editor-generated, NEVER original corpus evidence.
 */
(function(root){
'use strict';
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
}[c]));
const fold=x=>String(x??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function create(source){
  if(!Array.isArray(source)||source.length!==97)
    throw new Error('Exact 97-source edition is unavailable');
  const byVerb=new Map();
  for(const row of source){
    if(byVerb.has(row.lemma)||row.human_attested!==false||
       row.review_status!=='bounded_source_exemplar_not_general_frame'||
       !/^sen mi [a-zë]+-m [a-zë]+(?:-se)?\.$/.test(row.source_sentence))
      throw new Error('Source-only verb registry failed integrity checks');
    byVerb.set(row.lemma,row);
  }
  const allowedResonance=new Set(['sen','hë','më','zha']);
  function compose(lemma,options={}){
    const r=byVerb.get(lemma);
    if(!r)throw new Error('Unknown exact verb-object pairing');
    const tense=options.tense||'';
    const resonance=options.resonance||'sen';
    const negative=options.negative===true,question=options.question===true;
    if(!['','te','yu'].includes(tense)||!allowedResonance.has(resonance)||
       typeof negative!=='boolean'||typeof question!=='boolean')
      throw new Error('Requested variation is outside evidence-gated syntax');
    return resonance+' mi '+r.patient+'-m '+(negative?'nu ':'')+
      r.lemma+(tense?'-'+tense:'')+(question?' he?':'.');
  }
  function renderCard(r,opts){
    const generated=compose(r.lemma,opts);
    const same=generated===r.source_sentence;
    return '<section class="editorial-entry source-frame-card">'+
      '<div class="editorial-entry-head"><div><small>'+esc(r.domain)+' · '+esc(r.source_id)+
      ' · exact source V1 frame</small><h2><a href="#word/'+encodeURIComponent(r.lemma)+'">'+
      esc(r.lemma)+'</a></h2></div></div>'+
      '<p><strong>Meaning:</strong> '+esc(r.gloss)+'</p>'+
      '<p><b>Recorded actor:</b> <code>mi</code> · <b>Only licensed object:</b> '+
      '<a href="#word/'+encodeURIComponent(r.patient)+'"><code>'+esc(r.patient)+'</code></a></p>'+
      '<p><strong>Original controlled example:</strong> <a href="#phrase/'+
      encodeURIComponent(r.source_example_id)+'"><code>'+esc(r.source_sentence)+'</code></a></p>'+
      '<p class="muted small">'+esc(r.source_english)+' · Original corpus '+esc(r.source_example_id)+'</p>'+
      '<p><strong>Generated structure:</strong> <code class="source-frame-output">'+esc(generated)+'</code></p>'+
      '<p class="muted small">'+(same?
        'This exact form is the source-recorded teaching example.':
        'EDITORIAL SYNTHETIC FORM. Not present as an original attested sentence; not independently validated for idiomatic meaning.')+'</p>'+
      '<details><summary>Meaning boundary and evidence restrictions</summary>'+
      '<p>'+esc(r.semantic_boundary)+'</p>'+
      '<p>Only this verb with this original actor and exact object is licensed here. Other actors, patients, aspects, modals, and voice changes are intentionally unsupported.</p>'+
      '</details></section>';
  }
  function mount(host,options={}){
    host.innerHTML='<article class="readable source-frame-workshop">'+
      '<div class="article-header"><div class="article-kicker">Qaroshi / 11.2 opt-in editorial grammar</div>'+
      '<h1>97 source-bound verb constructions</h1>'+
      '<p class="article-sub">Use original documented verb/object pairs to explore basic morphology and questions without inventing unsupported argument meanings.</p></div>'+
      '<div class="note"><strong>Evidence matters.</strong> These are 97 exact V1 pairings from the controlled 8.7 teaching source, not 97 independently reviewed general verb frames. Changing a tense, negation, or speech act makes a synthetic formal example, NOT a speaker-attested sentence. No new actor, object, passive, modal or arbitrary aspect is approved.</div>'+
      '<div class="controls">'+
      '<label for="sourceFrameQuery">Find a source verb</label>'+
      '<input id="sourceFrameQuery" class="field search" type="search" placeholder="Verb, object, meaning, or subject area…" value="'+esc(options.word||'')+'">'+
      '<label for="sourceFrameTense">Tense</label>'+
      '<select id="sourceFrameTense" class="field select"><option value="">Unmarked</option><option value="te">Past (-te)</option><option value="yu">Future (-yu)</option></select>'+
      '<label for="sourceFrameResonance">Resonance</label>'+
      '<select id="sourceFrameResonance" class="field select">'+
      '<option value="sen">sen · neutral</option><option value="hë">hë · inquiry</option>'+
      '<option value="më">më · warm</option><option value="zha">zha · playful</option></select>'+
      '<label><input id="sourceFrameNegative" type="checkbox"> Negate predicate</label>'+
      '<label><input id="sourceFrameQuestion" type="checkbox"> Ask a polar question</label>'+
      '</div><p class="muted small" id="sourceFrameCount" role="status" aria-live="polite"></p>'+
      '<div id="sourceFrameList"></div><button type="button" class="button" id="sourceFrameMore">Show more source frames</button>'+
      '<div class="foot"><a href="#workshop">Strict 25-frame sentence workshop</a> · '+
      '<a href="#meaning">Meaning and contrast lab</a> · <a href="#validation">Independent-reader protocol</a></div></article>';
    const $=id=>host.querySelector('#'+id);
    let limit=20;
    function draw(){
      const search=fold($('sourceFrameQuery').value);
      const visible=source.filter(x=>fold([
        x.lemma,x.gloss,x.domain,x.patient,x.source_english,x.semantic_boundary,x.source_example_id
      ].join(' ')).includes(search));
      const opts={
        tense:$('sourceFrameTense').value,
        resonance:$('sourceFrameResonance').value,
        negative:$('sourceFrameNegative').checked,
        question:$('sourceFrameQuestion').checked
      };
      const shown=visible.slice(0,limit);
      $('sourceFrameCount').textContent=visible.length+' source pairs matched; '+shown.length+' displayed';
      $('sourceFrameList').innerHTML=shown.map(r=>renderCard(r,opts)).join('')||
        '<p class="muted">No source-licensed pairs match. No alternative meanings are guessed.</p>';
      $('sourceFrameMore').hidden=shown.length>=visible.length;
    }
    for(const id of ['sourceFrameQuery','sourceFrameTense','sourceFrameResonance',
                     'sourceFrameNegative','sourceFrameQuestion'])
      $(id).addEventListener('input',()=>{limit=20;draw()});
    $('sourceFrameMore').addEventListener('click',()=>{limit+=20;draw()});
    draw();
  }
  return Object.freeze({compose,renderCard,mount,count:source.length});
}
root.QaroshiSourceFrames=Object.freeze({create});
})(window);
