/* Qaroshi 11: source-labeled contrast and dialogue workshop; offline. */
(function(root){
'use strict';
const E = x => String(x == null ? '' : x).replace(/[&<>"']/g, c => ({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
}[c]));
const F = x => String(x || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const link = s => s==='nëgëra' ? '<a href="#standard" title="Adopted post-7.0 determiner; see current grammar">'+E(s)+'</a>' : '<a href="#word/'+encodeURIComponent(s)+'">'+E(s)+'</a>';
function create(data){
  const src=data.standard11||{};
  const pairs=src.contrasts||[], rules=src.conversation_rules||[];
  function renderContrast(x){
    return '<section class="editorial-entry std11-contrast" data-pair="'+E(x.id)+'">'+
      '<div class="editorial-entry-head"><div><small>Source '+E(x.id)+' · contrast</small><h2>'+
      link(x.left)+' versus '+link(x.right)+'</h2></div></div>'+
      '<p><b>'+E(x.left_gloss)+'</b> / '+E(x.right_gloss)+'</p>'+
      '<p class="muted small">Existing source distinction: '+E(x.semantic_boundary)+'</p>'+
      '<p><strong>Think first:</strong> '+E(x.learner_question)+'</p>'+
      '<details><summary>Reveal editorial explanation and false inference</summary>'+
      '<p>'+E(x.explanation)+'</p><p><b>Do not infer:</b> '+E(x.forbidden_inference)+'</p></details>'+
      '<p class="muted small">Original boundary: '+E(x.source_status)+
      ' · New commentary: unvalidated editorial explanation, not an independent reading.</p></section>';
  }
  function renderRule(x){
    const q=x.training;
    return '<section class="editorial-entry std11-rule" data-rule="'+E(x.id)+'">'+
      '<h2>'+E(x.topic.replace(/_/g,' '))+'</h2><p>'+E(x.rule)+'</p>'+
      (x.preferred_or_documented_example ? '<p><b>Source illustration:</b> <code>'+E(x.preferred_or_documented_example)+'</code></p>' : '')+
      (x.contrast_or_omission ? '<p><b>Source comparison:</b> <code>'+E(x.contrast_or_omission)+'</code></p>' : '')+
      '<p class="muted small">'+E(x.scope_note)+' · '+E(x.status)+'</p>'+
      (q?'<p><b>Situation:</b> '+E(q.scenario)+'</p><p><b>Try:</b> '+E(q.question)+'</p>'+
        '<details><summary>Reveal editorial answer</summary><p>'+E(q.editorial_answer)+'</p></details>':
        '<p class="muted small">Source usage rule; no new exercise assigned.</p>')+'</section>';
  }
  function mount(host,options={}){
    const selected=String(options.word||'');
    host.innerHTML='<article class="readable std11-workshop">'+
      '<div class="article-header"><div class="article-kicker">Qaroshi / Language · Editorial Standard 11 pilot</div>'+
      '<h1>Understand what a sentence really means</h1>'+
      '<p class="article-sub">30 meaning contrasts, 20 conversation rules and 12 situational repair questions, grounded in existing Qaroshi sources.</p></div>'+
      '<div class="note"><strong>Check the meaning, not just the words.</strong> These are source-derived teaching contrasts and new editorial explanations. None are independently approved reader outcomes, new dictionary senses or new grammatical licenses. Reveal answers only after trying.</div>'+
      '<div class="controls">'+
      '<label for="std11Kind">Explore</label><select class="field select" id="std11Kind"><option value="all">All material</option><option value="meaning">Meaning contrasts</option><option value="conversation">Conversation & repair</option></select>'+
      '<label for="std11Search">Search</label><input class="field search" id="std11Search" aria-label="Find a word, meaning or conversation rule" type="search" placeholder="Word, English meaning or topic…" value="'+E(selected)+'"></div>'+
      '<p class="muted small" id="std11Count" role="status" aria-live="polite"></p><div id="std11Results"></div>'+
      '<div class="foot"><a href="#editorial">Priority dictionary review desk</a> · <a href="#workshop">Bounded sentence workshop</a> · <a href="#validation">Independent-reader protocol</a></div></article>';
    const $=id=>host.querySelector('#'+id);
    function draw(){
      const needle=F($('std11Search').value),kind=$('std11Kind').value;
      const selectedPairs=(kind==='conversation'?[]:pairs).filter(x=>F([
        x.left,x.right,x.left_gloss,x.right_gloss,x.semantic_boundary,x.explanation,x.forbidden_inference
      ].join(' ')).includes(needle));
      const selectedRules=(kind==='meaning'?[]:rules).filter(x=>F([
        x.topic,x.rule,x.scope_note,x.preferred_or_documented_example,
        x.training?.scenario,x.training?.question
      ].join(' ')).includes(needle));
      $('std11Count').textContent=(selectedPairs.length+selectedRules.length)+
        ' source-linked learning items ('+selectedPairs.length+' meaning contrasts; '+selectedRules.length+' usage rules)';
      $('std11Results').innerHTML=selectedPairs.map(renderContrast).join('')+
        selectedRules.map(renderRule).join('') || '<p class="muted">No matching source entries. Try a different word or topic.</p>';
    }
    $('std11Kind').addEventListener('change',draw);
    $('std11Search').addEventListener('input',draw);
    draw();
  }
  return Object.freeze({renderContrast,renderRule,mount,metrics:src.metrics||{}});
}
root.Qaroshi11=Object.freeze({create});
})(window);
