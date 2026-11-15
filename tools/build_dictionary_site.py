#!/usr/bin/env python3
"""Build an independent single-file HTML dictionary with original glyph previews."""
import base64,csv,json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'data/lexicon.csv').open(encoding='utf-8-sig',newline='') as f:lex=list(csv.DictReader(f))
with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig',newline='') as f:corpus=list(csv.DictReader(f))
stats=json.loads((ROOT/'data/statistics.json').read_text())
glyphs={}
for p in sorted((ROOT/'assets/glyphs').glob('*.png')):
    glyphs[p.stem]='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
# Escape < when embedding data in an executable script tag.
def serial(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
script = '''
const LEX=__LEX__, CORPUS=__CORPUS__, GLYPHS=__GLYPHS__;
const ORDER=['sh','zh','kh','ng','k','a','w','t','r','q','o','d','z','u','ë','i','g','e','h','b','p','m','s','n','y','l'];
const el=x=>document.getElementById(x);
const norm=s=>(s||'').normalize('NFC').toLocaleLowerCase();
const escapeHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function glyphify(raw,maxCount=80){
  const target=document.createElement('span');target.className='glyphline';
  const s=norm(raw);let count=0;
  for(let i=0;i<s.length && count<maxCount;){
    const c=s[i];if(/[\\s]/.test(c)){const sp=document.createElement('span');sp.className='wordspace';target.appendChild(sp);i++;continue;}
    if(c==='-'){i++;continue;}
    let match=ORDER.find(g=>s.startsWith(g,i));
    if(match){const im=document.createElement('img');im.src=GLYPHS[match];im.alt=match;im.title=match;im.loading='lazy';target.appendChild(im);i+=match.length;count++;}
    else{let x=document.createElement('span');x.className='punct';x.textContent=c;target.appendChild(x);i++;}
  }
  return target;
}
function tag(txt,cls){return '<span class="tag '+cls+'">'+escapeHtml(txt)+'</span>';}
const domains=[...new Set(LEX.map(x=>x.domain))].sort((a,b)=>a.localeCompare(b));
for(const d of domains){const op=document.createElement('option');op.value=d;op.textContent=d;el('domain').appendChild(op);}
const postypes=[...new Set(LEX.map(x=>x.pos))].sort();
for(const p of postypes){const op=document.createElement('option');op.value=p;op.textContent=p;el('pos').appendChild(op);}
let last=[];let shown=0;
function renderLex(reset=true){
  if(reset){shown=0;let q=norm(el('q').value),status=el('status').value,domain=el('domain').value,pos=el('pos').value,edition=el('edition').value;
    last=LEX.filter(r=>(!status||r.review===status)&&(!domain||r.domain===domain)&&(!pos||r.pos===pos)&&(!edition||r.edition===edition) && (!q||norm(r.qaroshi).includes(q)||norm(r.english).includes(q)||norm(r.note).includes(q)));
    if(q)last.sort((a,b)=>score(a,q)-score(b,q)||a.qaroshi.localeCompare(b.qaroshi));
    el('results').replaceChildren();
  }
  const size=80,frag=document.createDocumentFragment();
  for(const r of last.slice(shown,shown+size)){
    const art=document.createElement('article');art.className='entry';
    art.innerHTML='<div class="entrytitle"><strong>'+escapeHtml(r.qaroshi)+'</strong>'+tag(r.pos,'')+tag(r.review,r.review==='established'?'core':r.review==='standardized'?'standard':'candidate')+tag('v'+r.edition,'')+'</div>'+
       '<div class="meaning">'+escapeHtml(r.english)+'</div><div class="minor">'+escapeHtml(r.domain)+(r.components?' · '+escapeHtml(r.components):'')+'</div>';
    const native=glyphify(r.qaroshi,32);native.classList.add('entryglyph');art.appendChild(native);
    frag.appendChild(art);
  }
  el('results').appendChild(frag);shown=Math.min(shown+size,last.length);
  el('found').textContent=last.length.toLocaleString()+' results · showing '+shown.toLocaleString();
  el('more').hidden=shown>=last.length;
}
function score(r,q){let w=norm(r.qaroshi),e=norm(r.english);return w===q?0:e===q?1:w.startsWith(q)?2:e.startsWith(q)?3:4;}
let cf=[];
function renderCorpus(){let q=norm(el('pq').value);cf=CORPUS.filter(x=>!q||norm(x.qaroshi).includes(q)||norm(x.english).includes(q)||norm(x.domain).includes(q));
 el('presults').replaceChildren();let frag=document.createDocumentFragment();
 for(let r of cf.slice(0,120)){let card=document.createElement('article');card.className='phrase';card.innerHTML='<strong>'+escapeHtml(r.qaroshi)+'</strong><p>'+escapeHtml(r.english)+'</p><small>'+escapeHtml(r.domain)+' · '+escapeHtml(r.note)+'</small>';frag.appendChild(card);}
 el('presults').appendChild(frag);el('pfound').textContent=cf.length+' sentences found (showing up to 120)';}
function converter(){const text=el('convertText').value;const target=el('glyphOutput');target.replaceChildren(glyphify(text,2000));}
function setTab(which){for(let id of ['dictionary','phrases','script','grammar']){let active=id===which;el('tab-'+id).hidden=!active;el('nav-'+id).classList.toggle('selected',active);el('nav-'+id).setAttribute('aria-selected',String(active));} if(which==='phrases')renderCorpus();if(which==='script')converter();}
for(let id of ['dictionary','phrases','script','grammar'])el('nav-'+id).onclick=()=>setTab(id);
el('q').oninput=()=>renderLex();el('domain').onchange=()=>renderLex();el('pos').onchange=()=>renderLex();el('status').onchange=()=>renderLex();el('edition').onchange=()=>renderLex();el('more').onclick=()=>renderLex(false);
el('pq').oninput=renderCorpus;el('convertText').oninput=converter;
el('copyText').onclick=async()=>{try{await navigator.clipboard.writeText(el('convertText').value);el('copyText').textContent='Copied Romanized text';}catch(e){el('copyText').textContent='Clipboard unavailable; select the text above';}};
el('downloadImage').onclick=async()=>{
  const text=el('convertText').value;
  const segments=[];let s=norm(text);for(let i=0;i<s.length;){const g=ORDER.find(x=>s.startsWith(x,i));if(g){segments.push(g);i+=g.length;}else{segments.push(s[i]);i++;}}
  const fontH=44,gap=4,wordSpace=23,wrap=1050,lineH=72;let x=22,y=20;const draw=[];
  const cache={};for(const g of ORDER){let im=new Image();im.src=GLYPHS[g];await im.decode();cache[g]=im;}
  for(const g of segments){if(g==='\\n'){x=22;y+=lineH;continue;}if(g===' '){x+=wordSpace;continue;}if(g==='-')continue;
    let w=cache[g]?Math.min(75,Math.max(16,cache[g].width/cache[g].height*fontH))+gap:15;if(x+w>wrap){x=22;y+=lineH;}draw.push({g,x,y,w});x+=w;}
  let cvs=document.createElement('canvas');cvs.width=wrap+25;cvs.height=y+lineH;let ctx=cvs.getContext('2d');ctx.fillStyle='#f4f3fb';ctx.fillRect(0,0,cvs.width,cvs.height);
  for(const z of draw){let im=cache[z.g];if(im){ctx.drawImage(im,z.x,z.y,z.w-gap,fontH);}else{ctx.fillStyle='#202030';ctx.font='20px system-ui';ctx.fillText(z.g,z.x,z.y+33);}}
  let a=document.createElement('a');a.download='qaroshi-native-script.png';a.href=cvs.toDataURL('image/png');a.click();
};
renderLex();renderCorpus();converter();
'''
script=script.replace('__LEX__',serial(lex)).replace('__CORPUS__',serial(corpus)).replace('__GLYPHS__',serial(glyphs))
styles='''
:root{color-scheme:dark;--bg:#0d101a;--ink:#edf2fc;--muted:#a6b2ca;--line:#293549;--accent:#8c9aff;--card:#171d2b;--neutral:#1c2837}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif;line-height:1.55}
a{color:#a8b8ff}header{padding:34px max(18px,calc((100% - 1120px)/2));background:linear-gradient(135deg,#172440,#0d101a 78%);border-bottom:1px solid var(--line)}
h1{font-size:clamp(2rem,4vw,3.2rem);line-height:1.05;margin:6px 0 10px;letter-spacing:-.045em}h2{margin:22px 0 8px;font-size:1.3rem;letter-spacing:-.02em}p{margin:8px 0}.eyebrow{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:#a8b8ff;font-weight:650}
.sub{max-width:660px;color:var(--muted)}.stats{display:flex;gap:11px;flex-wrap:wrap;margin-top:24px}.stat{border:1px solid var(--line);background:#ffffff06;border-radius:12px;padding:10px 16px;color:var(--muted)}.stat strong{color:white;font-size:1.2rem}
main{max-width:1120px;margin:auto;padding:18px 18px 70px}.nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;border-bottom:1px solid var(--line);padding-bottom:12px}button,select,input,textarea{font:inherit;color:var(--ink)}
button{border:1px solid #34445e;background:#1b2840;padding:9px 14px;border-radius:9px;cursor:pointer}button:hover,button.selected{border-color:var(--accent);background:#2c3457}
input,select,textarea{border:1px solid #34445e;background:#111a2b;border-radius:10px;padding:12px;min-width:0}input:focus,select:focus,textarea:focus{outline:2px solid #8492ff88}
.filter{display:grid;grid-template-columns: minmax(200px,2.3fr) repeat(4,minmax(115px,1fr));gap:10px;margin:18px 0}.found{color:var(--muted);font-size:.85rem;margin:10px 0 15px}
.results{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px}.entry,.phrase{border:1px solid var(--line);background:var(--card);border-radius:13px;padding:14px;min-width:0}.entrytitle{display:flex;gap:6px;align-items:center;flex-wrap:wrap}.entrytitle strong{font-size:1.06rem}.tag{font-size:.7rem;border:1px solid #41516a;color:#c8d7ea;padding:2px 6px;border-radius:99px}.tag.core{border-color:#48796e;color:#8ee0c4}.tag.standard{border-color:#7c68a3;color:#d1b4ff}.tag.candidate{border-color:#88704a;color:#efc77f}.meaning{margin-top:8px}.minor{font-size:.77rem;color:var(--muted);margin-top:7px}.glyphline{display:inline-flex;align-items:center;flex-wrap:wrap;gap:2px}.glyphline img{height:32px;max-width:43px;object-fit:contain}.entryglyph{margin-top:9px;min-height:33px;border-top:1px solid #283447;padding-top:7px}.wordspace{display:inline-block;width:13px}.punct{font-family:monospace;color:#b5bdd9}.more{margin:15px auto;display:block}
.phrase strong{font-size:.95rem}.phrase p{color:#d4def5}.phrase small{color:var(--muted)}.converter{min-height:160px;border:1px solid var(--line);background:#141d2c;border-radius:12px;padding:20px;margin:15px 0}.converter .glyphline img{height:52px;max-width:75px}.converter .wordspace{width:24px}.flex{display:flex;gap:10px;flex-wrap:wrap}.guide{max-width:800px}.guide table{border-collapse:collapse;width:100%;margin:10px 0 24px}.guide td,.guide th{border-bottom:1px solid var(--line);padding:8px;text-align:left}.guide th{color:#d7e0f9}.guide code{color:#b3befc}.muted{color:var(--muted)}
footer{border-top:1px solid var(--line);margin-top:25px;padding:24px 0;color:var(--muted);font-size:.85rem}
@media(max-width:760px){.filter{grid-template-columns:repeat(2,minmax(0,1fr))}.filter #q{grid-column:span 2}.results{grid-template-columns:1fr}.nav button{font-size:.87rem}main{padding:14px 12px 50px}.converter{padding:12px}}
'''
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Qaroshi 3.0 | Offline Dictionary</title><style>{styles}</style></head><body>
<header><div class="eyebrow">Nardoragon language · Standard Reference 3.0</div><h1>Qaroshi</h1><p class="sub">The offline bilingual dictionary, 26-glyph script viewer, resonance reference, and parallel-sentence corpus. Everything runs locally without a network connection.</p>
<div class="stats"><div class="stat"><strong>{len(lex):,}</strong><div>lexicon entries</div></div><div class="stat"><strong>{len(corpus):,}</strong><div>example sentences</div></div><div class="stat"><strong>16</strong><div>mandatory written resonances</div></div><div class="stat"><strong>26</strong><div>native glyphs</div></div></div></header>
<main><nav class="nav" role="tablist"><button id="nav-dictionary" class="selected" role="tab" aria-selected="true">Dictionary</button><button id="nav-phrases" role="tab" aria-selected="false">Phrasebook</button><button id="nav-script" role="tab" aria-selected="false">Native script</button><button id="nav-grammar" role="tab" aria-selected="false">Grammar summary</button></nav>
<section id="tab-dictionary"><h2>Bilingual lexical search</h2><p class="muted">Search Qaroshi or English. <b>Established</b> forms are preserved from Reference 1.0; <b>Candidate</b> forms in editions 2.0 and 3.0 await usage review; proposed grammar is labeled separately.</p>
<div class="filter"><input id="q" type="search" placeholder="Search word, meaning or note…" aria-label="Search dictionary"><select id="pos" aria-label="Part of speech"><option value="">All word classes</option></select><select id="domain" aria-label="Semantic field"><option value="">All fields</option></select><select id="status" aria-label="Review status"><option value="">All statuses</option><option value="established">Established</option><option value="standardized">Standardized grammar</option><option value="candidate">Candidate lexeme</option><option value="proposed">Proposed 3.0 grammar</option></select><select id="edition" aria-label="Reference edition"><option value="">All editions</option><option value="1.0">1.0 established</option><option value="2.0">2.0</option><option value="3.0">3.0</option></select></div><div id="found" class="found"></div><div class="results" id="results"></div><button id="more" class="more">Show 80 more</button></section>
<section id="tab-phrases" hidden><h2>Parallel sentence corpus</h2><p class="muted">Controlled grammatical examples and established phrases; not a statistical translation model.</p><input id="pq" type="search" style="width:100%" placeholder="Find sentence, English meaning, topic…"><div id="pfound" class="found"></div><div id="presults" class="results"></div></section>
<section id="tab-script" hidden><h2>Romanized Qaroshi → native glyphs</h2><p class="muted">Each handwritten glyph is retained from the supplied 26-letter alphabet. The four digraphs <code>sh zh kh ng</code> are each a single letter. Typographic punctuation and Arabic digits are additional technical marks, not native glyphs.</p><textarea id="convertText" rows="4" style="width:100%" aria-label="Qaroshi input">më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.</textarea><div class="converter" id="glyphOutput"></div><div class="flex"><button id="downloadImage">Save native-glyph PNG</button><button id="copyText">Copy Romanized text</button></div><p class="muted">The original alphabet is artwork, not a keyboard-installable font. This converter renders that artwork directly. The dictionary searches words but does not automatically translate unrestricted English.</p></section>
<section id="tab-grammar" hidden class="guide"><h2>Core grammar reference</h2><p>A full sentence begins with exactly one written resonance marker and follows a predominantly subject–object–verb pattern. A clause's finite verb comes after its main arguments, and negation <code>nu</code> directly precedes its predicate.</p>
<table><thead><tr><th>Resonance</th><th>Purpose</th></tr></thead><tbody>
{''.join(f'<tr><td><code>{a}</code></td><td>{b}</td></tr>' for a,b in [('më','affection, vulnerability'),('zha','playful joy'),('qor','solemnity, promises'),('sen','neutral information'),('hë','inquiry'),('lën','shyness'),('sur','grief'),('rak','defiance'),('khar','alarm'),('yë','wonder'),('nëm','tranquility'),('wen','longing'),('dal','resolve'),('rëm','pride'),('hol','gratitude'),('zher','doubt')])}</tbody></table>
<h2>Word order and endings</h2><p><code>REGISTER + subject + object-m + place/time + nu? + verb + evidence? + he?/ya?</code>. Nouns: <code>-ri</code> plural, <code>-na</code> possession, <code>-lo</code> location, <code>-gu</code> goal, <code>-de</code> source, <code>-wa</code> with, <code>-tu</code> recipient, <code>-shi</code> instrument, <code>-nga</code> via/through. Verbs: <code>-te</code> past, <code>-yu</code> future, <code>-se</code> ongoing, <code>-mo</code> complete, <code>-në</code> habitual; <code>-ki</code> can, <code>-ho</code> allowed, <code>-du</code> must.</p>
<h2>Advanced structures</h2><p><code>wë</code> if, <code>wënu</code> counterfactual if, <code>qinë</code> would (consequent), <code>yëmë</code> optative wish, <code>dasha</code> even if, <code>shoru</code> unless, <code>qona</code> embedded whether, <code>rëshi</code> contrastive focus, <code>toru</code> quotation introducer, <code>hëmi</code> confirmation tag.</p><p>Questions use final <code>he</code> (except confirmation questions with <code>hëmi</code>); requests use <code>ya</code>. Evidentials: <code>si</code> witnessed, <code>hu</code> reported, <code>ye</code> inferred, <code>lëshu</code> customary knowledge. The traditional number system is base six.</p><h2>3.0 discourse and timing</h2><p>Preverbal phase: <code>wëshi</code> about to, <code>shëtë</code> just finished, <code>zhoro</code> still, <code>mënoro nu</code> not yet, <code>nësha nu</code> no longer. Focus: <code>ngëshi</code> only, <code>bëso</code> also, <code>tëmiri</code> even. Quantity: noun + <code>qësho / rëshu / nëmi</code> + numeral. Evidence: <code>shëku</code> remembered, <code>wërusha</code> measured, <code>rëhu</code> written source; <code>yëqo</code> surprising result, <code>sëki / qëru</code> low/high confidence. See <code>docs/grammar_v3_extensions.md</code> in the ZIP for full precedence rules and more examples.</p>
<p>For the formal details and exceptions see <code>docs/grammar.md</code> in the complete reference pack.</p></section>
<footer>Qaroshi Reference 3.0. Lexical coverage remains a milestone toward full modern-language expressiveness, not a claim of idiomatic parity. All content is bundled in this file. Original alphabet artwork retained.</footer></main>
<script>{script}</script></body></html>'''
out=ROOT/'Qaroshi_Offline_Dictionary_v3.html'
out.write_text(page,encoding='utf-8')
print(out, 'bytes',out.stat().st_size)
