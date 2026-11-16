#!/usr/bin/env python3
"""Package a self-contained offline Qaroshi 14.0 editorial quality dashboard."""
import csv,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):
 with (ROOT/p).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
D={
 'manifest':json.loads((ROOT/'data/v14/audit_manifest.json').read_text()),
 'translations':read('data/v14/translation_review_103.csv'),
 'screening':read('data/v14/translation_screening_689.csv'),
 'idioms':read('data/v14/idiom_review_1000.csv'),
 'senses':read('data/v14/sense_review_5000.csv'),
 'variants':[dict(x,_index=i) for i,x in enumerate(read('data/v14/translation_variant_clusters.csv'))],
 'decisions':json.loads((ROOT/'data/v14/decision_register.json').read_text()),
 'rules':[],
 'words':[[x['qaroshi'],x['pos'],x['english']] for x in read('data/lexicon.csv')],
}
import sys
sys.path.insert(0,str(ROOT/'tools/v14'))
from semantic_validator import CODE
D['rules']=[{'id':k,'name':v[0],'severity':v[1]} for k,v in CODE.items()]
assert len(D['translations'])==103 and len(D['idioms'])==1000 and len(D['senses'])==5000
assert len(D['decisions'])==20 and len(D['words'])==30000
css=(ROOT/'web/v14/style.css').read_text(encoding='utf8')
js=(ROOT/'web/v14/app.js').read_text(encoding='utf8')
payload=json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
html='''<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="Qaroshi 14 offline semantic consistency and editorial review dashboard"><title>Qaroshi 14 · Language Consistency</title><style>'''+css+'''</style><script src="web/theme.js"></script><link rel="stylesheet" href="web/tool-theme.css"><script defer src="web/tool-theme.js"></script></head><body>
<header class="topbar"><button class="btn" id="mobilemenu" aria-label="Open navigation">☰</button><a href="#/overview" class="brand"><span class="logo">Q</span>Qaroshi <span class="muted" style="font-weight:500">14.0</span></a><span class="topmeta">Language Consistency & Editorial Review</span><div class="right"><button class="btn" id="theme" aria-label="Toggle dark and light mode">◐ Theme</button></div></header>
<div id="overlay" class="overlay"></div><div class="shell"><aside class="sidebar" id="sidebar" aria-label="Navigation"></aside><main id="main" class="main"><h1>Qaroshi 14.0</h1><p>Loading the audit...</p></main><aside class="rail"><div class="stick"><h3>What this release checks</h3><p>Written resonance, suffix order, case roles, questions, evidentials, and translation-alignment clues.</p><h3>What it cannot certify</h3><p>Speaker naturalness, established idioms, approved dictionary senses, or an unrestricted translation of complex prose.</p><h3>Existing resources</h3><a href="Qaroshi_12_13_Language_Studio.html" class="app-link">12–13 Language Studio</a><p><a href="Qaroshi_Wiki.html" class="app-link">Complete Wiki</a></p><p><a href="Qaroshi_Academy.html" class="app-link">Academy</a></p></div></aside></div>
<noscript><p>JavaScript is required for the offline dashboard; CSVs and documentation in the source package remain available without it.</p></noscript><script type="application/json" id="app-data">'''+payload+'''</script><script>'''+js+'''</script></body></html>'''
out=ROOT/'Qaroshi_14_Semantic_Workbench.html';out.write_text(html,encoding='utf8')
print('Wrote',out,'bytes',out.stat().st_size,'lookup',len(D['words']),'rule cards',len(D['rules']), 'variants',len(D['variants']))
