#!/usr/bin/env python3
"""Wire the deep study library into Qaroshi's single-file offline wiki."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
b=ROOT/'tools/build_wiki.py';s=b.read_text(encoding='utf8')
s=s.replace('import mistune','import mistune')
s=s.replace("markdown=mistune.create_markdown(plugins=['table','strikethrough'])", "markdown=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])")
s=s.replace("chapters.sort(key=lambda r:r['number'])", "chapters.sort(key=lambda r:r['number'])")
s=s.replace("guides={}\n", "guides={}\nstudy_index=json.loads((ROOT/'docs/deep_guides/guide_index.json').read_text(encoding='utf-8'))\nfor item in study_index:\n    key=item['id']\n    guides[key]=markdown((ROOT/item['path']).read_text(encoding='utf-8'))\n")
s=s.replace("'letters':letters,'glyphs':glyphs,'domains':domains,", "'letters':letters,'glyphs':glyphs,'domains':domains,'studyIndex':study_index,")
s=s.replace("<title>Qaroshi Wiki · Unified Standard 5.0</title>","<title>Qaroshi Wiki · Unified Standard 5.1</title>")
s=s.replace('dictionary, and native handwritten alphabet entirely offline.', 'dictionary, deep learning guides, exercises, and native handwritten alphabet entirely offline.')
s=s.replace('Build one self-contained, offline wiki HTML for Qaroshi Unified Standard 5.0','Build one self-contained, offline wiki HTML for Qaroshi Unified Standard 5.1')
b.write_text(s,encoding='utf8')

j=ROOT/'web/qaroshi.js';s=j.read_text(encoding='utf8')
start="  const PH = Object.fromEntries(D.phonemes.map(p => [p.glyph, p.ipa.slice(1,-1)]));"
s=s.replace(start,start+"\n  const STUDY = D.studyIndex || [];\n  const studyBy = new Map(STUDY.map(x => [x.id,x]));")
s=s.replace("home:'Overview', dictionary:'Dictionary'","home:'Overview', learn:'Learning library', dictionary:'Dictionary'")
needle="${a('home','Home')}${a('dictionary','Dictionary')}"
s=s.replace(needle,"${a('home','Home')}${a('learn','Learn Qaroshi')}${a('dictionary','Dictionary')}")
needle="      <div class=\"side-group\"><div class=\"side-heading\">Grammar</div>"
insertion="""      <div class="side-group"><div class="side-heading">Learn Qaroshi</div>
      ${a('learn','Learning library')}
      ${a('guide/getting_started','Start here')}
      ${a('guide/graded_course','Guided course · 16 lessons')}
      ${a('guide/sentence_atlas','Annotated sentence atlas')}
      ${a('guide/workbook','Practice and answer keys')}
      <details class="chapter-group"><summary>Deep topic guides · 16</summary><div class="nested">
        ${STUDY.filter(x => !['graded_course','sentence_atlas','workbook'].includes(x.id)).map(x=>a('guide/'+x.id,x.title)).join('')}
      </div></details></div>
      <div class="side-group"><div class="side-heading">Grammar</div>"""
assert needle in s
s=s.replace(needle,insertion)
s=s.replace("Unified Standard 5.0</strong>","Unified Standard 5.1</strong>")
s=s.replace("Qaroshi Unified Standard 5.0 · Offline", "Qaroshi Unified Standard 5.1 · Offline")
s=s.replace('All 70 chapters belong to the same unified grammar.', 'All 70 chapters belong to the same unified grammar. <a href="#learn">Study them with guided examples and answer keys.</a>')

# More helpful homepage discovery without reorganizing the main dictionary.
needle="        <a class=\"quick-card\" href=\"#grammar\"><span class=\"arrow\">›</span><strong>Grammar</strong><small>Read rules, examples and suffixes</small></a>"
if needle in s:
    s=s.replace(needle,"""        <a class="quick-card learning-quick" href="#learn"><span class="arrow">›</span><strong>Learning library</strong><small>16 lessons, step-by-step guides and practice answers</small></a>
"""+needle)
needle="      <div class=\"foot\">Qaroshi Unified Standard 5.1"
# No-op, home page already has a footer; quick card enough.

# New learning index view.
needle="  function renderDictionary(route){"
assert needle in s
learning=r'''  function renderLearn(){
    const featured=['getting_started','graded_course','sentence_atlas','workbook'];
    const lead=featured.map(id=>studyBy.get(id)).filter(Boolean);
    const rest=STUDY.filter(x=>!featured.includes(x.id));
    const entry=x=>`<a class="learning-card" href="#guide/${enc(x.id)}">
      <span class="learning-arrow" aria-hidden="true">↗</span>
      <strong>${esc(x.title)}</strong><small>${esc(x.chapters==='all'?'Complete reference':('Grammar chapters '+x.chapters))}</small>
      <span class="learning-activity">${x.id==='graded_course'?'16 staged lessons and answer keys':x.id==='workbook'?'Grammar traps and mixed assessment':x.id==='sentence_atlas'?'21 worked morphology parses':'Detailed explanations, IPA and checked examples'}</span>
    </a>`;
    main.innerHTML=`<article class="readable">${mkHeader('Reference / Study','Learn Qaroshi','A structured, self-contained curriculum with lessons, deep topic guides, worked sentence analyses, and answer keys.')} 
      <div class="study-summary"><strong>Start with a complete sentence.</strong> Learn its resonance, identify roles, read the predicate, then translate. The 16-lesson course grows those skills with existing reference examples; it does not introduce new grammar rules or replace the dictionary.</div>
      <h2 id="path">Recommended path</h2>
      <ol class="study-steps"><li>Read <a href="#guide/getting_started">Start here</a> and the <a href="#guide/pronunciation_lab">Pronunciation laboratory</a>.</li>
      <li>Complete lessons 1–8 in the <a href="#guide/graded_course">guided course</a>.</li>
      <li>Study the <a href="#guide/nouns_cases">noun cases</a>, <a href="#guide/verb_workshop">verb endings</a> and <a href="#guide/resonance_mastery">resonance registers</a>.</li>
      <li>Complete lessons 9–16, then check the <a href="#guide/sentence_atlas">sentence atlas</a> and <a href="#guide/workbook">practice workbook</a>.</li></ol>
      <h2 id="featured">Core study resources</h2><div class="learning-grid">${lead.map(entry).join('')}</div>
      <h2 id="deep">Deep-dive guides</h2><p class="muted">Each guide explains a topic in context and includes reference IPA, worked examples, independent practice, and a revealable answer key.</p>
      <div class="learning-grid">${rest.map(entry).join('')}</div>
      <div class="foot">The original standard dictionary and 70 grammar chapters remain the normative basis for every guide.</div></article>`;
    setToc([{id:'path',name:'Study route'},{id:'featured',name:'Core resources'},{id:'deep',name:'Deep guides'}]);
  }
'''
s=s.replace(needle,learning+needle)

# Link related guides at end of each grammar chapter. Matching chapters are parsed from numeric range metadata.
needle="    main.innerHTML=`<article class=\"readable\">${mkHeader('Grammar / Chapter '+c.number,c.title,'Qaroshi grammar')}"
assert needle in s
replace="""    const related=STUDY.filter(x=>x.chapters!=='all'&&x.chapters.split(',').some(piece=>{
      const match=piece.trim().match(/^(\\d+)(?:[–-](\\d+))?$/);
      if(!match)return false;return c.number>=Number(match[1])&&c.number<=Number(match[2]||match[1]);
    })).slice(0,5);
    const deeper=related.length?`<section class="chapter-further"><h2 id="further-reading">Go deeper</h2><p>Read a step-by-step explanation and practice this topic using existing Qaroshi sentences.</p>
      <ul>${related.map(x=>`<li><a href="#guide/${enc(x.id)}">${esc(x.title)}</a></li>`).join('')}</ul></section>`:'';
    main.innerHTML=`<article class="readable">${mkHeader('Grammar / Chapter '+c.number,c.title,'Qaroshi grammar')}"""
s=s.replace(needle,replace)
s=s.replace('      <div class="doc-body" id="chapterBody">${c.html}</div><div class="divider"></div>', '      <div class="doc-body" id="chapterBody">${c.html}</div>${deeper}<div class="divider"></div>')

# Proper titles for all new docs instead of raw slugs.
s=s.replace("  function renderGuide(id){\n    if(!D.guides[id])", "  function renderGuide(id){\n    if(!D.guides[id])")
s=s.replace("mkHeader('Reference / Guides',TOP_PAGES[id]||id,'Qaroshi supporting documentation')", "mkHeader('Reference / Guides',studyBy.get(id)?.title || TOP_PAGES[id] || id,studyBy.has(id)?'Deep learning guide · Worked examples, IPA, and active practice':'Qaroshi supporting documentation')")
s=s.replace("  function enrichToc(){\n    const headings=main.querySelectorAll('.doc-body h2,.doc-body h3');const items=[];", "  function enrichToc(){\n    const h2=main.querySelectorAll('.doc-body h2');\n    const headings=h2.length>11?h2:main.querySelectorAll('.doc-body h2,.doc-body h3');const items=[];")
s=s.replace("headings.forEach((h,i)=>{h.id='inpage-'+i;items.push({id:h.id,name:h.textContent.trim().slice(0,74)});});", "headings.forEach((h,i)=>{h.id='inpage-'+i;if(items.length<28)items.push({id:h.id,name:h.textContent.trim().slice(0,74)});});")
s=s.replace("      case 'home':renderHome();break;", "      case 'home':renderHome();break;\n      case 'learn':renderLearn();break;")
s=s.replace('Qaroshi Unified Standard Reference 4.3; fully offline','Qaroshi Unified Standard Reference 5.1; fully offline')
j.write_text(s,encoding='utf8')

c=ROOT/'web/qaroshi.css';s=c.read_text(encoding='utf8')
s+='''
/* 5.1 learning library: wiki-native, compact, readable, keyboard-accessible. */
.learning-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;margin:16px 0 30px}
.learning-card{display:flex;flex-direction:column;min-height:138px;gap:4px;position:relative;padding:17px 18px;border:1px solid var(--border);border-radius:12px;color:var(--text);background:var(--panel);text-decoration:none;transition:border-color .14s,box-shadow .14s}
.learning-card:hover,.learning-card:focus-visible{color:var(--text);text-decoration:none;border-color:var(--accent-border);box-shadow:var(--shadow)}
.learning-card strong{max-width:90%;font-size:.97rem;line-height:1.4;letter-spacing:-.02em}
.learning-card small{font-size:.72rem;color:var(--muted)}
.learning-activity{font-size:.77rem;color:var(--link);margin-top:auto}
.learning-arrow{position:absolute;top:11px;right:14px;color:var(--muted);font-size:.95rem}
.study-summary{border-left:4px solid var(--link);border-radius:0 10px 10px 0;padding:15px 19px;margin:14px 0 28px;background:var(--accent-bg);line-height:1.8}
.study-steps{padding-left:25px;margin:14px 0 30px}.study-steps li{margin:9px 0;padding-left:4px}
.doc-body details{border:1px solid var(--accent-border);border-radius:10px;background:var(--canvas);padding:12px 17px;margin:18px 0 24px}
.doc-body details summary{font-weight:700;color:var(--link);cursor:pointer;line-height:1.5;list-style:revert}
.doc-body details[open]{background:var(--panel)}
.doc-body details ol,.doc-body details ul{padding-left:24px}
.doc-body details li{margin:6px 0}
.doc-body table{display:table;max-width:100%;width:100%;font-size:.85rem}
.doc-body{overflow-wrap:anywhere}
.doc-body h2{padding-top:8px}
.doc-body blockquote{background:var(--canvas);border-left:3px solid var(--accent-border);padding:12px 18px;margin:16px 0}
.chapter-further{background:var(--canvas);padding:13px 21px 17px;border-radius:10px;margin:28px 0}
.chapter-further h2{margin:6px 0 8px;font-size:1.2rem}
.chapter-further p{font-size:.84rem;color:var(--muted)}
.chapter-further ul{margin-bottom:4px;padding-left:19px}
@media(max-width:670px){.learning-grid{grid-template-columns:1fr}.learning-card{min-height:125px}.doc-body table{font-size:.76rem}.doc-body th,.doc-body td{padding:7px 5px}}
@media print{.doc-body details{break-inside:avoid}.doc-body details>summary{font-weight:700}.learning-grid{display:block}.learning-card{margin:10px 0}}
'''
c.write_text(s,encoding='utf8')
print('patched wiki source and build')
