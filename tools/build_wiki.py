#!/usr/bin/env python3
"""Build one self-contained, offline wiki HTML for Qaroshi Unified Standard 5.3.

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
chapter_docs=[('docs/grammar.md','5.0')]
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
assert [c['number'] for c in chapters]==list(range(1,71)),[c['number'] for c in chapters]
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
domains=dict(sorted(Counter(w['domain'] for w in words).items()))
public_words=[{k:r[k] for k in ['id','qaroshi','pos','english','domain','components','note','ipa','reading','sound_out']} for r in words]
public_sentences=[{k:r[k] for k in ['id','domain','qaroshi','english','note','pattern','ipa','reading','sound_out']} for r in sentences]
metadata={'words':public_words,'phrases':public_sentences,'chapters':chapters,'guides':guides,
          'letters':letters,'glyphs':glyphs,'domains':domains,'studyIndex':study_index,
          'phonemes':json.loads((ROOT/'data/phoneme_inventory.json').read_text(encoding='utf-8')),
          'latin':json.loads((ROOT/'data/latin_alphabet.json').read_text(encoding='utf-8')),
          'resonances':json.loads((ROOT/'data/resonances.json').read_text(encoding='utf-8')),
          'affixes':json.loads((ROOT/'data/affixes.json').read_text(encoding='utf-8')),
          'counts':{'dictionary':len(words),'phrasebook':len(sentences),'grammar':len(chapters),'letters':len(letters)}}
blob=json.dumps(metadata,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
css=(ROOT/'web/qaroshi.css').read_text(encoding='utf-8');js=(ROOT/'web/qaroshi.js').read_text(encoding='utf-8')
page=f'''<!doctype html>
<html lang="en" data-theme="light"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="description" content="Qaroshi, the Nardoragon language: browse grammar, dictionary, deep learning guides, exercises, and native handwritten alphabet entirely offline.">
<title>Qaroshi Wiki · Unified Standard 5.3</title>
<style>{css}</style></head><body>
<header class="topbar"><a class="brand" href="#home" aria-label="Qaroshi home"><span class="brand-mark" aria-hidden="true">Q</span><span>Qaroshi <span class="light">Wiki</span></span></a>
<div class="toolbar"><form class="top-search" id="topSearchForm" role="search"><label class="sr-only" for="topSearch">Search Qaroshi</label><span class="search-ico" aria-hidden="true">⌕</span>
<input id="topSearch" autocomplete="off" placeholder="Search the reference" type="search"><span class="kbd" aria-hidden="true">/</span></form>
<button class="iconbtn" type="button" id="themeBtn" aria-label="Use dark theme" title="Toggle light/dark appearance">☾</button>
<button class="iconbtn" type="button" id="menuBtn" aria-controls="leftSidebar" aria-expanded="false" aria-label="Open sidebar">☰</button></div></header>
<div class="backdrop" id="sideBackdrop" aria-hidden="true"></div>
<div class="shell"><aside class="sidebar" id="leftSidebar" aria-label="Reference navigation"></aside>
<main class="content" id="mainContent" tabindex="-1"><article><h1>Qaroshi</h1><p>Loading the offline reference…</p></article></main>
<nav class="right-rail" aria-label="On this page" id="pageToc"></nav></div>
<noscript><p style="padding:2rem">This offline wiki requires JavaScript for navigation and search. The Markdown and CSV sources are provided in the full release package.</p></noscript>
<script type="application/json" id="wiki-data">{blob}</script><script>{js}</script>
</body></html>'''
for filename in ('index.html', 'Qaroshi_Wiki.html'):
 (ROOT/filename).write_text(page,encoding='utf-8')
# GitHub Pages serves index.html from the repository root.
print('wiki build:',len(words),'lexemes,',len(sentences),'sentences,',len(chapters),'chapters,',len(domains),'domains,',
      len(page.encode('utf-8')),'bytes,',len(glyphs),'original-derived glyphs')
