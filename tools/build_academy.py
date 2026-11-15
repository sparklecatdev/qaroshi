"""Build standalone Qaroshi Academy from exact Unified Standard lexical and course sources."""
from __future__ import annotations
import base64,csv,json,re
from pathlib import Path
import mistune

ROOT=Path(__file__).resolve().parents[1]
read=lambda n:(ROOT/n).read_text(encoding='utf-8')
words=list(csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf-8-sig')))
phrases=list(csv.DictReader((ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig')))
phrase_by={p['id']:p for p in phrases}
markdown=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])
course=read('docs/deep_guides/graded_course.md')
sections=re.split(r'(?=^## Lesson \d+ · )',course,flags=re.M)
lessons=[]
for content in sections:
    head=re.search(r'^## Lesson (\d+) · (.+)$',content,re.M)
    if not head: continue
    lid=int(head.group(1)); name=head.group(2)
    skills=re.search(r'\*\*Target skills:\*\* (.+?)\. \*\*Source:',content)
    ids=re.findall(r'\| (S[A-Za-z0-9]+) \|',content)
    ids=list(dict.fromkeys(ids))
    examples=[{k:p[k] for k in ['id','qaroshi','english','ipa','sound_out','domain']} for i in ids if (p:=phrase_by.get(i))]
    if len(examples)<8: raise ValueError(f'Lesson {lid} missing examples: {ids}')
    lessons.append({'id':lid,'title':name,'skills':skills.group(1) if skills else '', 'examples':examples[:10], 'html':markdown(content)})
assert len(lessons)==16
files=list((ROOT/'docs/deep_guides').glob('*.md'))
exclude={'graded_course.md','index.md','sentence_atlas.md','workbook.md'}
guides=[]
for path in sorted(files):
    if path.name in exclude:continue
    text=path.read_text(encoding='utf-8')
    title=re.search(r'^# (.+)',text,re.M)
    guides.append({'id':path.stem,'title':title.group(1).strip() if title else path.stem.replace('_',' ').title(),'html':markdown(text)})
assert len(guides)==16, [g['id'] for g in guides]
glyphs={p.stem:base64.b64encode(p.read_bytes()).decode('ascii') for p in (ROOT/'assets/glyphs').glob('*.png')}
assert len(glyphs)==26
MATURE_DOMAINS={
 'Profanity, swearing and expletives','Vulgar language and coarse behavior','Vulgar verbs',
 'Coarse intensifiers, blunt attitudes','Anatomy colloquialisms and sexual slang nouns',
 'Explicit anatomy and reproductive health','Sexual and intimate acts (neutral terminology)',
 'Sexual and affectionate actions','Vulgar verb senses and explicit slang',
 'Bodily functions slang and euphemisms','Bodily function actions and slang'
}
packet={
  'words':[[p[k] for k in ('id','qaroshi','pos','english','domain','type','ipa','sound_out')] + [p['domain'] in MATURE_DOMAINS] for p in words],
  'sentences':[[p[k] for k in ('id','qaroshi','english','ipa','sound_out','domain')] + [p['id'].startswith('S530')] for p in phrases],
  'lessons':lessons,
  'guides':guides,
  'glyphs':glyphs,
  'affixes':json.loads(read('data/affixes.json')),
  'resonances':json.loads(read('data/resonances.json')),
  'meta':{'title':'Qaroshi Academy','edition':'5.3','source':'Unified Standard 5.3','word_count':len(words),'sentence_count':len(phrases)}
}
js=read('web/academy/academy.js')
css=read('web/academy/academy.css')
theme_js=read('web/theme.js')
json_data=json.dumps(packet,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=f'''<!doctype html><html lang="en" data-theme="light"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Learn Qaroshi, the language of Nardoragons, with guided lessons, word review, games, and the original writing system.">
<title>Qaroshi Academy</title><script>{theme_js}</script><style>{css}</style></head>
<body><div class="app" id="app"><div class="mobile-shade" id="shade" aria-hidden="true"></div>
<aside class="sidebar" id="sidebar" aria-label="Main navigation"></aside>
<div class="stage"><header class="topbar"><div class="row"><button class="tiny-btn hamburger" id="menu-btn" aria-label="Open menu" aria-controls="sidebar" aria-expanded="false">☰</button><span class="crumb" id="crumb">Overview</span></div><div class="actions"><select class="theme-select" id="theme-btn" aria-label="Appearance"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></div></header>
<main class="content" id="content"></main></div></div>
<script type="application/json" id="academy-data">{json_data}</script><script>{js}</script>
</body></html>'''
(ROOT/'Qaroshi_Academy.html').write_text(html,encoding='utf-8')
(ROOT/'data/academy_lessons.json').write_text(json.dumps([{'id':l['id'],'title':l['title'],'skills':l['skills'],'example_ids':[e['id'] for e in l['examples']]} for l in lessons],ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/academy_manifest.json').write_text(json.dumps({'version':'5.3','embedded_words':len(words),'embedded_examples':len(phrases),'lessons':len(lessons),'guides':len(guides),'native_glyphs':len(glyphs),'practice_modes':['vocab','reverse','sentence','affix','resonance','glyph','forge','sound'],'offline':True,'progress':'localStorage; JSON export/import'},indent=2),encoding='utf-8')
print('Academy HTML',len(html),'bytes,',len(lessons),'lessons',len(guides),'guides',len(words),'entries',len(phrases),'sentences')
