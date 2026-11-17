#!/usr/bin/env python3
"""Build the self-contained current Qaroshi Wiki with integrated discovery and practice tools.

The page is self-contained: assets, dictionary, corpus, metadata and reference
chapters are embedded. No requests, CDN or service worker are needed.
"""
from pathlib import Path
from collections import Counter
import csv,json,base64,io,re,shutil,html
from PIL import Image
import mistune
ROOT=Path(__file__).resolve().parents[1]
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
words=readcsv(ROOT/'data/lexicon.csv');sentences=readcsv(ROOT/'corpus/parallel_sentences.csv')
markdown=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])
chapter_docs=[('docs/standard_8/grammar.md','8.0 normative')]
chapters=[]
for file,edition in chapter_docs:
 text=(ROOT/file).read_text(encoding='utf-8')
 heads=list(re.finditer(r'^##\s+(\d+)\.\s+(.+)$',text,flags=re.MULTILINE))
 for idx,match in enumerate(heads):
  start=match.end();end=heads[idx+1].start() if idx+1<len(heads) else len(text)
  block=text[start:end].strip()
  n=int(match.group(1));title=match.group(2).strip()
  chapters.append({'id':str(n).zfill(2),'number':n,'title':title,'source':file,
                   'html':markdown(block),'plain':re.sub(r'[#*`|<>]+',' ',block)[:2100]})
chapters.sort(key=lambda r:r['number'])
assert [c['number'] for c in chapters]==list(range(1,91)),[c['number'] for c in chapters]
guides={}
study_index=json.loads((ROOT/'docs/deep_guides/guide_index.json').read_text(encoding='utf-8'))
for item in study_index:
    key=item['id']
    guides[key]=markdown((ROOT/item['path']).read_text(encoding='utf-8'))
for name,path in [('translation','docs/translation.md'),('lexicography','docs/lexicography.md'),('phonology','docs/phonology_and_script.md'),('roadmap','docs/roadmap.md'),('pronunciation','docs/pronunciation.md'),('release','docs/release_notes.md'),('latin','docs/latin_alphabet.md'),('living','docs/living_speech.md')]:
 guides[name]=markdown((ROOT/path).read_text(encoding='utf-8'))
letters=('k','a','w','t','r','q','o','d','sh','z','u','ë','i','g','kh','zh','e','ng','h','b','p','m','s','n','y','l')
glyphs={}
for c in letters:
 im=Image.open(ROOT/'assets/glyphs'/f'{c}.png').convert('RGBA')
 a=im.getchannel('A')
 bbox=a.getbbox()
 if bbox:im=im.crop(bbox)
 im.putdata([(0,0,0,p[3]) for p in im.getdata()])
 buf=io.BytesIO();im.save(buf,format='PNG',optimize=True)
 glyphs[c]='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
# Publish the current editorial grammar and 9.3/9.4 bounded tools directly
# inside the self-contained Wiki. Historical files and site aliases stay intact.
import sys
sys.path.insert(0,str(ROOT))
from tools.semantic94.complete import build as build_semantic_94
build_semantic_94()
semantic_rows=readcsv(ROOT/'data/stress94/source_semantic_requirements_500.csv')
assert len(semantic_rows)==500
semantic_cases=[]
for case in semantic_rows:
    req=json.loads(case['source_semantic_intent_json'])
    semantic_cases.append({
        'id':case['id'],'domain':case['domain'],'variant':int(case['variant']),
        'english':case['original_english'],
        'qaroshi':case['current_9_2_qaroshi_candidate'],
        'scope':req['source_semantic_scope'],
        'roles':req['original_role_or_event_components'],
        'source_status':case['signature_source'],
        'review_status':case['independent_semantic_equivalence'],
    })
licenses=json.loads((ROOT/'data/standard_9_3/grammar_licenses.json').read_text(encoding='utf-8'))
frames=json.loads((ROOT/'data/semantics/valency_frames.json').read_text(encoding='utf-8'))
assert len(licenses['verb_overrides'])==25 and len(frames)==25
def source_doc_html(path):
    # The public Pages site intentionally does not expose raw data/Markdown.
    # Redirect source document relative links to their actual GitHub files;
    # keep anchors/external links unmodified. The offline text itself remains.
    from posixpath import normpath
    rendered=markdown(path.read_text(encoding='utf-8'))
    parent=path.parent.relative_to(ROOT).as_posix()
    def fix(match):
        source=match.group(1)
        target,sep,fragment=source.partition('#')
        relative=normpath(parent+'/'+target)
        if relative.startswith('..') or relative.startswith('/'):
            raise ValueError('Source link traverses outside the repository: '+source)
        return 'href="https://github.com/sparklecatdev/qaroshi/blob/main/'+relative+(('#'+fragment) if sep else '')+'"'
    return re.sub(r'href="((?:\.\./|\./)[^"]+)"',fix,rendered)

editions=json.loads((ROOT/'data/standard_9_2/amendment_registry.json').read_text(encoding='utf-8'))
grammar_addenda=[]
for entry in editions['source_paths']:
    path=ROOT/entry['path']
    grammar_addenda.append({'edition':entry['edition'],'kind':entry['kind'],
        'title':(path.read_text(encoding='utf-8').splitlines()[0]).lstrip('# ').strip(),
        'html':source_doc_html(path)})
current_grammar_intro=source_doc_html(ROOT/'docs/standard_9_2/FRONT_MATTER.md')
domains=dict(sorted(Counter(w['domain'] for w in words).items()))
public_words=[{k:r[k] for k in ['id','qaroshi','pos','english','domain','components','note','ipa','reading','sound_out']} for r in words]
public_sentences=[{k:r[k] for k in ['id','domain','qaroshi','english','note','pattern','ipa','reading','sound_out']} for r in sentences]
metadata={'words':public_words,'phrases':public_sentences,'chapters':chapters,'guides':guides,
          'letters':letters,'glyphs':glyphs,'domains':domains,'studyIndex':study_index,
          'phonemes':json.loads((ROOT/'data/phoneme_inventory.json').read_text(encoding='utf-8')),
          'latin':json.loads((ROOT/'data/latin_alphabet.json').read_text(encoding='utf-8')),
          'resonances':json.loads((ROOT/'data/resonances.json').read_text(encoding='utf-8')),
          'affixes':json.loads((ROOT/'data/affixes.json').read_text(encoding='utf-8')),
          'grammarLicenses':licenses,'grammarFrames':frames,
          'semanticCases':semantic_cases,'currentGrammarIntro':current_grammar_intro,
          'grammarAddenda':grammar_addenda,
          'counts':{'dictionary':len(words),'phrasebook':len(sentences),'grammar':len(chapters),'letters':len(letters)}}
blob=json.dumps(metadata,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
css=(ROOT/'web/qaroshi.css').read_text(encoding='utf-8');js=(ROOT/'web/qaroshi.js').read_text(encoding='utf-8');theme_js=(ROOT/'web/theme.js').read_text(encoding='utf-8')
grammar_js=(ROOT/'web/grammar_live.js').read_text(encoding='utf-8')
lab_js=(ROOT/'web/wiki_lab.js').read_text(encoding='utf-8')
discovery_js=(ROOT/'web/wiki_discovery.js').read_text(encoding='utf-8')
practice_js=(ROOT/'web/wiki_practice.js').read_text(encoding='utf-8')
page=f'''<!doctype html>
<html lang="en" data-theme="light"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="description" content="Qaroshi, the Nardoragon language: browse grammar, dictionary, learning guides, exercises, and the native handwritten alphabet.">
<title>Qaroshi Wiki · Dictionary, grammar, lessons and practice</title>
<script>{theme_js}</script><style>{css}</style></head><body>
<header class="topbar"><a class="brand" href="#home" aria-label="Qaroshi home"><span class="brand-mark" aria-hidden="true">Q</span><span>Qaroshi <span class="light">Wiki</span></span></a>
<div class="toolbar"><form class="top-search" id="topSearchForm" role="search"><label class="sr-only" for="topSearch">Search Qaroshi</label><span class="search-ico" aria-hidden="true">⌕</span>
<input id="topSearch" autocomplete="off" placeholder="Search the reference" type="search"><span class="kbd" aria-hidden="true">/</span></form>
<select class="theme-select" id="themeBtn" aria-label="Appearance"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select>
<button class="iconbtn" type="button" id="menuBtn" aria-controls="leftSidebar" aria-expanded="false" aria-label="Open sidebar">☰</button></div></header>
<div class="backdrop" id="sideBackdrop" aria-hidden="true"></div>
<div class="shell"><aside class="sidebar" id="leftSidebar" aria-label="Reference navigation"></aside>
<main class="content" id="mainContent" tabindex="-1"><article><h1>Qaroshi</h1><p>Loading the reference…</p></article></main>
<nav class="right-rail" aria-label="On this page" id="pageToc"></nav></div>
<noscript><p style="padding:2rem">This wiki requires JavaScript for navigation and search. The source documents are available in the repository.</p></noscript>
<script type="application/json" id="wiki-data">{blob}</script><script>{grammar_js}</script><script>{lab_js}</script><script>{discovery_js}</script><script>{practice_js}</script><script>{js}</script>
</body></html>'''
for filename in ('index.html', 'Qaroshi_Wiki.html'):
 (ROOT/filename).write_text(page,encoding='utf-8')
# GitHub Pages serves index.html from the repository root.
print('wiki build:',len(words),'lexemes,',len(sentences),'sentences,',len(chapters),'chapters,',len(domains),'domains,',
      len(page.encode('utf-8')),'bytes,',len(glyphs),'original-derived glyphs,',len(semantic_cases),'editorial review cases')
