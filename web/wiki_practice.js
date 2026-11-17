/* Qaroshi Wiki 9.6 offline study studio.
 * Cards use unchanged canonical dictionary/corpus, with honest English glosses.
 * Private in-page progress only; no network, storage, invented speaker data.
 */
(function(root){
  'use strict';
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','&quot;':'&quot;',"'":'&#39;'}[c]));
  const fmt=n=>Number(n).toLocaleString('en-US');
  function createDeck(items,{limit=12,seed=37,word='',domain=''}={}){
    let pool=items.filter(x=>x&&x.qaroshi&&x.english&&(!domain||x.domain===domain));
    if(word){
      const form=word.toLowerCase();
      const exact=pool.filter(x=>x.qaroshi.toLowerCase()===form);
      const similar=pool.filter(x=>x.qaroshi.toLowerCase()!==form);
      pool=[...exact,...similar];
    }
    // Stable weighted shuffle, no mutated global dictionary and no hidden
    // claim that shuffled cards estimate native speaker proficiency.
    let s=seed>>>0;
    const rand=()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);
    if(word){
      const first=pool.slice(0,1),rest=pool.slice(1);
      for(let i=rest.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[rest[i],rest[j]]=[rest[j],rest[i]];}
      pool=[...first,...rest];
    }else{
      pool=pool.slice();
      for(let i=pool.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[pool[i],pool[j]]=[pool[j],pool[i]];}
    }
    const seen=new Set();
    return pool.filter(x=>{if(seen.has(x.qaroshi))return false;seen.add(x.qaroshi);return true}).slice(0,limit);
  }
  function mount(host,data,options={}){
    const WORDS=data.words||[],PHRASES=data.phrases||[];
    const max=12;
    const allDomains=[...new Set(WORDS.map(x=>x.domain))].sort();
    const target=options.word||'';
    const available=WORDS.some(x=>x.qaroshi===target);
    const grouped=['words','phrases'];
    let mode='words',direction='qaroshi',domain='',index=0,revealed=false,got=0,again=0,session=0;
    let deck=[];
    const opts=(list,chosen)=>list.map(x=>'<option value="'+esc(x.value)+'"'+(x.value===chosen?' selected':'')+'>'+esc(x.label)+'</option>').join('');
    host.innerHTML='<article class="readable practice-studio">'+
      '<div class="article-header"><div class="article-kicker">Wiki / Learn & practice</div>'+
      '<h1>Practice studio</h1><p class="article-sub">Short, focused recall sessions using the actual dictionary and original teaching corpus. No accounts, scores stored online or external apps.</p></div>'+
      '<div class="lab-notice"><strong>Study aid, not a fluency exam.</strong> These answers show editorial English glosses. Recognizing a card does not independently verify Qaroshi comprehension or an idiomatic translation.</div>'+
      '<div class="practice-settings">'+
      '<label class="lab-field"><span>Practice material</span><select class="field" id="practiceMode">'+
        opts([{value:'words',label:'Dictionary words'},{value:'phrases',label:'Source example sentences'}],'words')+'</select></label>'+
      '<label class="lab-field"><span>Prompt direction</span><select class="field" id="practiceDirection">'+
        opts([{value:'qaroshi',label:'Read Qaroshi → recall English'},{value:'english',label:'Read English → recall Qaroshi'}],'qaroshi')+'</select></label>'+
      '<label class="lab-field"><span>Topic (words only)</span><select class="field" id="practiceDomain">'+
        opts([{value:'',label:'All topics'},...allDomains.map(x=>({value:x,label:x}))],'')+'</select></label>'+
      '<button class="button" type="button" id="practiceNew">New 12-card session</button></div>'+
      '<div class="practice-progress" id="practiceProgress" role="status" aria-live="polite"></div>'+
      '<div class="practice-card" id="practiceCard" tabindex="-1"></div>'+
      '<div class="practice-actions"><button id="practiceReveal" class="button primary" type="button">Show answer</button>'+
      '<button id="practiceAgain" class="button" type="button" hidden>Practice again</button>'+
      '<button id="practiceKnow" class="button primary" type="button" hidden>I recalled it</button></div>'+
      '<p class="muted small">Use the prompt to think of your answer before revealing it. Mark your own recall; the result is a personal study estimate, not independently scored evidence. Sessions reset on navigation or reload.</p>'+
      '<details class="lab-help"><summary>How these exercises work</summary><p>Word cards are taken from the canonical dictionary, with IPA and sound-out guidance. Example-sentence cards come from the parallel teaching corpus. No synthetic sentences or uncertified translations are added. This exercise is useful for review, not a native-like proficiency assessment.</p>'+
      '<p>For source-licensed grammatical composition try the <a href="#workshop">sentence workshop</a>. For full lessons see <a href="#learn">Learn Qaroshi</a>, and for the native alphabet see <a href="#script">Native script</a>.</p></details></article>';
    const $=id=>host.querySelector('#'+id);
    const settings=()=>{mode=$('practiceMode').value;direction=$('practiceDirection').value;domain=$('practiceDomain').value;};
    function start(){
      settings();session++;index=0;revealed=false;got=0;again=0;
      const collection=mode==='words'?WORDS:PHRASES;
      const selectedDomain=mode==='words'?domain:'';
      const selectedWord=mode==='words'&&available?target:'';
      deck=createDeck(collection,{limit:max,seed:session*7919+37,word:selectedWord,domain:selectedDomain});
      $('practiceDomain').disabled=mode!=='words';
      draw();
    }
    function draw(){
      const item=deck[index],finished=!item;
      $('practiceProgress').textContent=finished?
        'Session finished · '+got+' recalled · '+again+' to revisit':
        'Card '+(index+1)+' of '+deck.length+' · '+got+' recalled · '+again+' for review';
      $('practiceReveal').hidden=finished||revealed;
      $('practiceAgain').hidden=finished||!revealed;
      $('practiceKnow').hidden=finished||!revealed;
      if(finished){
        $('practiceCard').innerHTML='<div class="practice-finish"><strong>Session complete</strong><p>You marked '+
          fmt(got)+' recalled and '+fmt(again)+' for review. Your responses stay on this page only.</p>'+
          '<button class="button primary" id="practiceRestart" type="button">Start another session</button></div>';
        $('practiceRestart').addEventListener('click',start);
        return;
      }
      const prompt=direction==='qaroshi'?item.qaroshi:item.english;
      const answer=direction==='qaroshi'?item.english:item.qaroshi;
      $('practiceCard').innerHTML='<span class="practice-eyebrow">'+(mode==='words'?'Dictionary word':'Teaching example')+
        ' · '+(direction==='qaroshi'?'Read the Qaroshi':'Recall Qaroshi from English')+'</span>'+
        '<div class="practice-prompt">'+esc(prompt)+'</div>'+
        (revealed?'<div class="practice-answer"><div class="practice-answer-label">Editorial reference answer</div>'+
          '<strong>'+esc(answer)+'</strong><div class="ipa-small">'+esc(item.ipa||'')+
          (item.sound_out?' · '+esc(item.sound_out):'')+'</div>'+
          '<a href="'+(mode==='words'?'#word/'+encodeURIComponent(item.qaroshi):'#phrase/'+encodeURIComponent(item.id))+
          '" class="practice-reference">Open source entry</a></div>':
          '<div class="practice-placeholder">Try to recall the answer, then choose “Show answer”.</div>');
    }
    $('practiceReveal').addEventListener('click',()=>{revealed=true;draw();});
    for(const [key,ok] of [['practiceKnow',true],['practiceAgain',false]])
      $(key).addEventListener('click',()=>{ok?got++:again++;index++;revealed=false;draw();});
    $('practiceNew').addEventListener('click',start);
    for(const id of ['practiceMode','practiceDirection','practiceDomain'])
      $(id).addEventListener('change',()=>{
        // Changing an exercise configuration starts a fresh honest session.
        start();
      });
    const loc=host.querySelector('.practice-studio');
    loc.addEventListener('keydown',e=>{
      if(['INPUT','TEXTAREA','SELECT','BUTTON'].includes(e.target.tagName))return;
      if(e.key===' '&&!revealed){e.preventDefault();$('practiceReveal').click();}
      if(revealed&&e.key==='1')$('practiceKnow').click();
      if(revealed&&e.key==='2')$('practiceAgain').click();
    });
    start();
    return {getState:()=>({index,got,again,deckLength:deck.length,direction,mode})};
  }
  root.QaroshiPractice=Object.freeze({mount,createDeck});
})(typeof window!=='undefined'?window:globalThis);
