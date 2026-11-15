from pathlib import Path
p=Path(__file__).resolve().parents[1]/'web/qaroshi.js'
s=p.read_text()
def patch(old,new):
 global s
 if old not in s:raise ValueError('missing substring '+old[:130])
 s=s.replace(old,new)
# Pre-index examples and semantic domain to keep dictionary page responsive.
patch("  const wordBy = new Map(W.map(w => [w.qaroshi.toLowerCase(), w]));", """  const wordBy = new Map(W.map(w => [w.qaroshi.toLowerCase(), w]));
  const fold = s => String(s??'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
  const lexicalSearch = new Map(W.map(w => [w.id, fold([w.qaroshi,w.english,w.domain,w.sound_out].join(' '))]));
  const domainBy = new Map();
  W.forEach(w=>{if(!domainBy.has(w.domain))domainBy.set(w.domain,[]);domainBy.get(w.domain).push(w)});
  // A sentence mentions a headword only when it contains that token (or an
  // inflected form with a hyphen), never because a short spelling is a substring.
  const exampleByHeadword = new Map();
  P.forEach(p=>{
    const forms=new Set((p.qaroshi.toLowerCase().match(/[a-zë]+(?:-[a-zë]+)*/g)||[]).map(t=>{
      if(wordBy.has(t))return t;
      const base=t.split('-')[0];return wordBy.has(base)?base:t;
    }));
    forms.forEach(f=>{
      if(!wordBy.has(f))return;
      if(!exampleByHeadword.has(f))exampleByHeadword.set(f,[]);
      exampleByHeadword.get(f).push(p);
    });
  });""")
patch("  function letterBreakdown(word){\n    const gs=phoneticGraphemes(word);\n    if(!gs)return '<p class=\"muted\">No native Qaroshi letter-by-letter reading is available.</p>';\n    return `<div class=\"letter-sounds\" role=\"list\" aria-label=\"Qaroshi letters and their sounds\">${gs.map(g=>`<div role=\"listitem\" class=\"sound-token\" title=\"${esc(SOUND_NOTE[g])}\">\n      <strong>${esc(g)}</strong><span class=\"sound-token-ipa\">/${esc(PH[g])}/</span><span class=\"sound-token-cue\">${esc(SOUND_NOTE[g])}</span></div>`).join('')}</div>`;\n  }", """  function letterBreakdown(word){
    const gs=phoneticGraphemes(word);
    if(!gs)return '<p class="muted">No native Qaroshi letter-by-letter reading is available.</p>';
    const body=`<div class="letter-sounds" role="list" aria-label="Qaroshi letters and their sounds">${gs.map(g=>`<div role="listitem" class="sound-token" title="${esc(SOUND_NOTE[g])}">
      <strong>${esc(g)}</strong><span class="sound-token-ipa">/${esc(PH[g])}/</span><span class="sound-token-cue">${esc(SOUND_NOTE[g])}</span></div>`).join('')}</div>`;
    return gs.length>9?`<details class="sound-detail"><summary>Show all ${gs.length} letter sounds</summary>${body}</details>`:body;
  }""")
patch("Offline Qaroshi reference<br><strong>Unified Standard 4.3.1</strong>", "Offline Qaroshi reference<br><strong>Unified Standard 5.0</strong>")
patch("""    main.innerHTML=`<article class="readable"><div class="eyebrow">THE NARDORAGON LANGUAGE</div>
      <h1 style="margin-top:10px">Qaroshi</h1><p class="lead">A living reference to Qaroshi vocabulary, grammar, and the original 26-symbol writing system. Browse the language as a wiki, look up a term, or read its grammar chapter by chapter.</p>
      <div class="statsline"><span><b>${count(W.length)}</b> dictionary entries</span><span><b>${count(P.length)}</b> example sentences</span><span><b>70</b> grammar chapters</span><span><b>26</b> handwritten letters</span></div>""",
"""    main.innerHTML=`<article class="readable">
      <section class="home-hero" aria-label="Qaroshi introduction">
        <div class="hero-glyphs" aria-hidden="true"><img src="${G['q']}" alt=""><img src="${G['a']}" alt=""><img src="${G['r']}" alt=""></div>
        <div class="eyebrow">NARDORAGON LANGUAGE REFERENCE · STANDARD 5.0</div>
        <h1>Qaroshi<span class="hero-dot">.</span></h1>
        <p class="lead">A complete, browsable home for Qaroshi. Look up words, explore the grammar, practice pronunciation, or write using the original 26-glyph script.</p>
        <div class="statsline"><span><b>${count(W.length)}</b> words</span><span><b>${count(P.length)}</b> examples</span><span><b>${C.length}</b> grammar chapters</span><span><b>26</b> native letters</span></div>
      </section>""")
patch("<div class=\"foot\">Qaroshi Unified Standard 4.3 · Offline and self-contained", "<div class=\"foot\">Qaroshi Unified Standard 5.0 · Offline and self-contained")
patch("""      const q=state.dquery.normalize('NFC').trim().toLowerCase();
      let list=W.filter(x=> (!state.domain||x.domain===state.domain) &&(!state.pos||x.pos===state.pos)&&(!q||x.qaroshi.toLowerCase().includes(q)||x.english.toLowerCase().includes(q)||x.ipa.includes(q)||x.sound_out.toLowerCase().includes(q)||x.domain.toLowerCase().includes(q)));
      if(q){list=list.sort((a,b)=>((a.qaroshi===q)?-1:(b.qaroshi===q)?1:(a.qaroshi.startsWith(q)&&!b.qaroshi.startsWith(q))?-1:(!a.qaroshi.startsWith(q)&&b.qaroshi.startsWith(q))?1:a.qaroshi.localeCompare(b.qaroshi)))}
      else list=list.sort((a,b)=>a.qaroshi.localeCompare(b.qaroshi));""", """      const q=fold(state.dquery.trim());
      let list=W.filter(x=> (!state.domain||x.domain===state.domain) &&(!state.pos||x.pos===state.pos)&&(!q||lexicalSearch.get(x.id).includes(q)||x.ipa.includes(q)));
      const score=x=>{const word=fold(x.qaroshi),en=fold(x.english);return word===q?0:word.startsWith(q)?1:en===q?2:en.startsWith(q)?3:4};
      if(q)list.sort((a,b)=>score(a)-score(b)||a.qaroshi.localeCompare(b.qaroshi));""")
patch("""    const related=W.filter(x=>x.domain===w.domain && x.qaroshi!==w.qaroshi).slice(0,8);
    const occurrences=P.filter(p=>p.qaroshi.includes(w.qaroshi)).slice(0,8);""", """    const tokens=new Set(fold(w.english).split(/[^a-z]+/).filter(x=>x.length>3));
    const related=(domainBy.get(w.domain)||[]).filter(x=>x.id!==w.id).map(x=>({x,n:fold(x.english).split(/[^a-z]+/).filter(t=>tokens.has(t)).length})).sort((a,b)=>b.n-a.n||a.x.qaroshi.localeCompare(b.x.qaroshi)).slice(0,8).map(v=>v.x);
    const occurrences=(exampleByHeadword.get(w.qaroshi.toLowerCase())||[]).slice(0,8);""")
patch("""      ${w.components?`<div class="information"><label>Components</label><span>${esc(w.components)}</span></div>`:''}""", """      ${w.components?`<div class="information"><label>Components</label><span>${w.components.split(' + ').map(part=>wordBy.has(part)?`<a href="#word/${enc(part)}">${esc(part)}</a>`:esc(part)).join(' + ')}</span></div>`:''}""")
patch("""    const q=(route.query.get('q')||'').trim().toLowerCase();
    const words=W.filter(w=>w.qaroshi.toLowerCase().includes(q)||w.english.toLowerCase().includes(q)||w.ipa.includes(q)).slice(0,35);""", """    const raw=(route.query.get('q')||'').trim(),q=fold(raw);
    const words=q?W.filter(w=>lexicalSearch.get(w.id).includes(q)||w.ipa.includes(q)).slice(0,35):[];""")
patch("""    const chapters=C.filter(c=>c.title.toLowerCase().includes(q)||c.plain.toLowerCase().includes(q)).slice(0,15);
    const examples=P.filter(p=>p.qaroshi.toLowerCase().includes(q)||p.english.toLowerCase().includes(q)||p.ipa.includes(q)).slice(0,12);""", """    const chapters=q?C.filter(c=>fold(c.title).includes(q)||fold(c.plain).includes(q)).slice(0,15):[];
    const examples=q?P.filter(p=>fold(p.qaroshi).includes(q)||fold(p.english).includes(q)||p.ipa.includes(q)).slice(0,12):[];""")
patch("Qaroshi unified grammar", "Qaroshi grammar")
p.write_text(s)
print('Patched JS:',len(s))
