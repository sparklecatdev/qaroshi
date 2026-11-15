#!/usr/bin/env python3
"""Qaroshi 17.0: Reference-grounded practical communication kit.

Never promote editorial examples, generated translations or suggested roots to
speaker attestation. All text derives from the locked 4,383 reference pairs
or the selected existing editorial dialogues.
"""
import base64, collections, csv, hashlib, html, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v14'))
from semantic_validator import validate_sentence

P=ROOT/'data/v17';P.mkdir(exist_ok=True,parents=True)
rows=list(csv.DictReader((ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8')))
byid={r['id']:r for r in rows}
canon=list(csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf8')))
res=json.loads((ROOT/'data/resonances.json').read_text(encoding='utf8'))

# Category decisions are discoverability tags, not linguistic claims.
function_patterns=[
 ('Safety and consent',r'consent|boundary|unsafe|danger|protect|warn|password|private|may i|permi|stop|do not|don.t send|need help|help me'),
 ('Greetings',r'hello|goodbye|welcome|good night|thank|sorry|appreciate|how are|are you well|my name|what is your name'),
 ('Learning and clarification',r'qaroshi|understand|repeat|slowly|say|speak|learn|read|write|question|answer|explain|teach|dictionary|translate'),
 ('Feelings and care',r'feel|happy|sad|lonel|tired|worried|afraid|angry|shy|care|cherish|love|rest|comfort|trust|hope'),
 ('Food and home',r'food|water|drink|eat|hungry|thirst|meal|sleep|door|window|home|bathroom|bed|wash|kitchen|blanket'),
 ('Directions and travel',r'where|toward|travel|fly|from home|going|go to|leave|arriv|cliff|route|direction|navigation|path|transport'),
 ('Messages and privacy',r'message|reply|file|send|computer|phone|screen|network|internet|app|software|device|data|login|account|online'),
 ('Social and plans',r'friend|family|together|meet|visit|tomorrow|today|tonight|when will|plan|promise|festival|dance'),
 ('Health and access',r'health|pain|doctor|medicine|clinic|ill|hurt|injur|breath|medical|accessib|assist'),
 ('Work and learning',r'project|study|lesson|class|collaborat|task|practice|teach|work|education|research'),
 ('Nature and Nardoragons',r'wing|sky|star|moon|nest|storm|wind|rain|nardo|roost|flight|flying|forest|ocean'),
 ('Money and shopping',r'price|cost|buy|purchase|pay|market|money|sell|trade|shop|receipt'),
 ('Arts and culture',r'song|music|melody|art|dance|story|read|festival|poem|culture'),
]

def category(r):
 text=(r['english']+' '+r.get('domain','')).lower()
 for k,pat in function_patterns:
  if re.search(pat,text):return k
 return 'Other useful reference'

def intent(r):
 t=r['english'].lower();q=r['qaroshi'];
 if '?' in t or q.endswith('?'):return 'question'
 if re.search(r'\b(?:please|don.t|stop|warn|open the|close the|use a|write a)\b',t):return 'request'
 if re.search(r'\b(?:not|no|never|cannot|won.t|refuse|decline)\b',t):return 'refusal / negative'
 if re.search(r'\b(?:can|may|must|allowed|permission)\b',t):return 'ability / permission'
 if re.search(r'\b(?:will|going to|tomorrow|later)\b',t):return 'plan'
 return 'statement'

# Favor source-original canonical utterances and editor-prepared living-speech
# rather than the 123,000-token generated dialogues.
core=[r for r in rows if r['pattern'] in ('original phrasebook','living speech 5.3')]
# Add a broad collection of topical references, each category bounded to avoid
# a flood of one specialized domain.
topical=[r for r in rows if r['pattern']=='Reference 5.0 topical corpus']
by_cat=collections.defaultdict(list)
for r in topical:
 if 2<=len(r['english'].split())<=16:by_cat[category(r)].append(r)
for arr in by_cat.values():arr.sort(key=lambda r:(len(r['english'].split()),r['id']))
extra=[]
for cat in [p[0] for p in function_patterns]+['Other useful reference']:
 extra+=by_cat[cat][:34]
ids=set();chosen=[]
for r in core+extra:
 if r['id'] in ids:continue
 ids.add(r['id'])
 check=validate_sentence(r['qaroshi'],r['english'],context_id=r['id'])
 errs=[x for x in check['findings'] if x['severity']=='error']
 if errs and r['pattern'] not in ('original phrasebook','living speech 5.3'):continue
 chosen.append({
 'id':r['id'],'qaroshi':r['qaroshi'],'english':r['english'],
 'ipa':r['ipa'],'sound_out':r['sound_out'],'reading':r['reading'],
 'category':category(r),'intent':intent(r),'note':r['note'],
 'pattern':r['pattern'],'provenance':'documented controlled reference example; not speaker attested',
 'review_rules':sorted({x['rule_id'] for x in check['findings'] if x['severity'] in ('review','error')}),
 })
cat_counts=collections.Counter(x['category'] for x in chosen)
print('selected',len(chosen),'core',len(core),'cat counts',cat_counts)
# Exact, coherent dialogue scenes from original editorial corpus. These are NOT
# spontaneously recorded human conversations.
old=json.loads((ROOT/'corpus/original11/dialogues.json').read_text(encoding='utf8'))
print('dialogue JSON shape',type(old).__name__,list(old)[:2] if isinstance(old,dict) else len(old))
# Use explicitly aligned older rows and preserve speaker turns and scene_id.
scenes=collections.defaultdict(list)
with (ROOT/'corpus/original11/dialogue_turns.csv').open(encoding='utf8') as f:
 for r in csv.DictReader(f):scenes[r['scene_id']].append(r)
# Keep manageable coherent scripted scenes, order stable.
missions=[]
for sid,turns in scenes.items():
 if not (4<=len(turns)<=9):continue
 issues=[]
 for t in turns:
  result=validate_sentence(t['qaroshi'],t['literal_translation'])
  issues.extend(x['rule_id'] for x in result['findings'] if x['severity']=='error')
 if issues:continue
 missions.append({'id':sid,'title':sid.replace('-',' ').title(),'origin':'v11 editorial dialogue; not speaker attested',
                  'turns':[{'speaker':t['speaker'],'qaroshi':t['qaroshi'],'english':t['english'],'literal':t['literal_translation'],'ipa':t['ipa'],'sound_out':t['sound_out']} for t in turns]})
missions=missions[:32]
print('missions',len(missions))

# Allowed simple structures for offline sentence-builder practice, separately
# marked as auto-composed; no open-domain translation or free-form valency.
verbs=[
 {'root':'goro','english':'fly','obj':[]},
 {'root':'nëru','english':'rest','obj':[]},
 {'root':'nëra','english':'stay','obj':[]},
 {'root':'gura','english':'travel','obj':[]},
 {'root':'rëmi','english':'learn','obj':[]},
 {'root':'këmë','english':'drink','obj':['kima']},
 {'root':'shëliro','english':'read','obj':['shima','shiwaro']},
 {'root':'tika','english':'see','obj':['sëra','qaro','naro','shima']},
 {'root':'shiwari','english':'send','obj':['shiwaro']},
 {'root':'shiroli','english':'write','obj':['shina','shiwaro']},
 {'root':'daru','english':'protect','obj':['mi','ti','sa']},
 {'root':'dëmi','english':'help','obj':['mi','ti','sa']},
]
lex={r['qaroshi']:r for r in canon}
for v in verbs:
 if v['root'] not in lex:raise ValueError('unknown verb '+v['root'])
 for o in v['obj']:
  if o not in lex:raise ValueError('unknown object '+o)
# Build test fixtures for builder. Structural checks not semantic endorsement.
probes=[]
for verb in verbs:
 for subj in ['mi','ti','sa','naru']:
  for obj in (verb['obj'] or ['']):
   if obj==subj:continue
   for tense in ['','-te','-yu']:
    for modal in ['','-ki','-ho']:
     if tense and modal:continue
     mood='hë' if (len(probes)%3==1) else 'sen'
     t=mood+' '+subj+(' '+obj+'-m' if obj else '')+' '+verb['root']+tense+modal+(' he?' if mood=='hë' else '.')
     a=validate_sentence(t)
     if not a['valid_surface'] or any(x['rule_id'] in ['R14-009'] for x in a['findings']):
      raise AssertionError((t,a['findings']))
     probes.append({'qaroshi':t,'verb':verb['root'],'subject':subj,'object':obj,'tense':tense,'modal':modal})

# High-priority 120-lemma inventory from original 190: highest lexical surface
# counts, excluding resonance and particles, then headword training rationale.
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(ROOT/'tools/fluency11'))
from engine import words,word_analysis,RESONANCES,FUNCTIONS,CONNECTORS
freq=Counter()
for r in chosen:
 if r['pattern']!='original phrasebook':continue
 for token in words(r['qaroshi']):
  if token in RESONANCES or token in FUNCTIONS or token in CONNECTORS:continue
  a=word_analysis(token)
  if a['known']:freq[a['root']]+=1
core_words=[]
for root,n in freq.most_common(160):
 if root not in lex:continue
 rr=lex[root]
 core_words.append({'root':root,'meaning':rr['english'],'ipa':rr['ipa'],'sound_out':rr['sound_out'],'frequency_in_190_reference_phrases':n,'pos':rr['pos']})
core_words=core_words[:120]

# Personal syllabus: all prompts pull directly from reference examples.
# Five daily practical units; these are fixed recall exercises not accredited grading.
units=[
 ('Start talking','Greetings',['S00001','S00003','S00004','S00015','S00007']),
 ('Ask for clarification','Learning and clarification',['S00013','S00017','S00018','S00019','S00112']),
 ('Care and safety','Safety and consent',['S00138','S00139','S00140','S00151','S00152']),
 ('Daily needs','Food and home',['S00064','S00065','S00066','S00069','S00075']),
 ('Questions and travel','Directions and travel',['S00086','S00089','S00100','S00101','S00090']),
 ('Connect and respect','Feelings and care',['S00031','S00032','S00046','S00055','S00057']),
 ('Make plans','Social and plans',['S00071','S00034','S00052','S00148','S00150']),
 ('Online messages','Messages and privacy',['S00124','S00125','S00126','S00127','S00130']),
 ('Distinguish truth claims','Learning and clarification',['S00095','S00096','S00097','S00112','S00114']),
 ('Talk about learning','Learning and clarification',['S00118','S00119','S00121','S00122','S00134']),
]
lessons=[]
for title,cat,refs in units:
 phrases=[]
 for sid in refs:
  r=byid[sid];phrases.append({'id':sid,'qr':r['qaroshi'],'en':r['english']})
 lessons.append({'name':title,'category':cat,'phrases':phrases})

# Writing policy guide. This is pedagogical summary of actual source references.
guide='''# Qaroshi 17.0: Everyday use and communication guide

## What the release fixes

A lexicon of 30,000 entries and over 200,000 generated tokens does not by itself make the language easy to **use**. Qaroshi 17 adds a practical entry point: curated documented phrases, a sound-out-first mobile toolkit, bounded message composition, real context from existing editorial scenes, an offline script viewer, and a learner core-root path. The vocabulary and grammar have **not** been revised.

## Your first thirty seconds

1. Start with **zha ha, mara!** (Hello, friend!) or neutral/calm **nëm ha, mara.**
2. Ask **hë ti haro he?** (Are you well?) and answer **sen mi haro.** (I am well.)
3. Say **lën mi nu zhëmi.** (I don't understand.) and **më pëla ngëlawe shiri ya.** (Please speak slowly.)
4. For a written sentence, begin with a **resonance marker** (e.g. sen, hë, më) and end a yes/no question with **he**. A direct command/request uses **ya**, with other politeness words if appropriate.
5. Distinguish **-ki** ability, **-ho** permission, and **-du** obligation. Consent must be made explicit when it matters.

## Sentence anatomy

**Resonance + subject + object-m + other roles + predicate + he/ya**.

`sen mi kima-m këmë.` = I drink water. `hë ti mi-m dëmi-ki he?` = Can you help me? `hë mi ti-m mërali-ho he?` = May I hug you? The last one asks about permission, not physical ability.

The case **-m** marks direct objects, **-tu** marks a recipient, **-lo** location, **-gu** toward, **-de** from and **-wa** a companion. Verb endings: **-te** past, **-yu** future; **-se** progressive; **-ki/-ho/-du** ability/permission/obligation. Negative **nu** comes immediately before the predicate for basic clauses. Written independent sentences need a resonance marker.

## 16 resonances are not optional decoration

A resonance expresses the speaker's pragmatic stance (e.g., sen neutral, hë inquiry, më tenderness, khar alarm, hol gratitude, zher uncertainty). They do NOT by themselves establish someone's gender, intent to consent, a promise, or how certain a factual claim is. The offline app lets you inspect all 16 and render words using the 26 original native glyph artworks.

## Important naturalness and trust boundaries

- The quick-reference phrases reproduce *previously documented controlled bilingual examples*. They were not recorded from fluent, independent Qaroshi speakers.
- The dialogues come from existing **editorial scripts**. Some contextual English readings add narrative interpretation not overtly encoded in the Qaroshi. A separate literal reading is shown.
- The sentence builder is a **closed, practice-only SOV pattern**. It does not grant any claim that a generated message is idiomatic or semantically unambiguous. Review unusual verb arguments or claims.
- No sound files are included. IPA and English sound-outs are text pronunciation guides, not recorded speech or evidence of dialect.
- An offline text-to-speech voice should not be mistaken for native pronunciation. None is implemented here.
- The 30,000-word lexicon, 4,383 examples, 90 grammar chapters, 26 glyphs and 16 resonance markers remain unchanged.

## What practical fluency still needs

Independent people using Qaroshi in real interactions, a recorded/corrected phrasebook, accessibility reviews, additional realistic free conversation, proper mobile platform keyboard testing, speaker pronunciation recordings, and formal semantic approval of compound alternatives. This kit intentionally does not invent these.
'''
(ROOT/'docs/v17/EVERYDAY_GUIDE.md').write_text(guide,encoding='utf8')
with (P/'everyday_phrases.csv').open('w',encoding='utf8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=['id','category','intent','english','qaroshi','ipa','sound_out','reading','pattern','note','review_rules','provenance']);writer.writeheader()
 for r in chosen:writer.writerow({**r,'review_rules':';'.join(r['review_rules'])})
(P/'everyday_phrases.json').write_text(json.dumps(chosen,ensure_ascii=False,indent=2),encoding='utf8')
(P/'missions.json').write_text(json.dumps(missions,ensure_ascii=False,indent=2),encoding='utf8')
(P/'lessons.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2),encoding='utf8')
(P/'sentence_builder_fixtures.json').write_text(json.dumps(probes,ensure_ascii=False,indent=1),encoding='utf8')
(P/'core_learning_120.csv').write_text('root,meaning,ipa,sound_out,frequency_in_190_reference_phrases,pos\n'+''.join(','.join('"'+str(r[x]).replace('"','""')+'"' for x in ['root','meaning','ipa','sound_out','frequency_in_190_reference_phrases','pos'])+'\n' for r in core_words),encoding='utf8')

# App single-file generation. Native glyph samples source 26 unchanged PNG.
glyphs={}
for p in (ROOT/'assets/glyphs_display').glob('*.png'):
 glyphs[p.stem]='data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
resmap=[{'marker':r['marker'],'meaning':r['meaning'],'name':r['name'],'sound_out':r['sound_out']} for r in res]
meta={
'phrase_count':len(chosen),'original_phrasebook':sum(r['pattern']=='original phrasebook' for r in chosen),
'living_speech':sum(r['pattern']=='living speech 5.3' for r in chosen),
'other_topical':sum(r['pattern']=='Reference 5.0 topical corpus' for r in chosen),
'mission_count':len(missions),'lesson_count':len(lessons), 'builder_fixtures':len(probes),
'core_roots':len(core_words),'resonance_count':len(res),'glyph_count':len(glyphs),
'qa_review_rows':sum(bool(r['review_rules']) for r in chosen),
'categories':dict(cat_counts),
'limit':'controlled reference examples and editorial dialogues; no spontaneous speakers, not unrestricted translation'}
(P/'practical_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
print('manifest',meta)
# Script gets separate HTML template, escapes JSON embed against </script>.
json_data=json.dumps({'phrases':chosen,'missions':missions,'lessons':lessons,'roots':core_words,
'lex':[[r['qaroshi'],r['english'],r['pos'],r['ipa'],r['sound_out']] for r in canon],
'resonances':resmap,'glyphs':glyphs,'verbs':verbs,'meta':meta},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
template=(ROOT/'tools/v17/app_template.html').read_text(encoding='utf8')
app=template.replace('/*__QAROSHI_DATA__*/',json_data)
if '/*__QAROSHI_DATA__*/' in app:raise Exception('unfilled json template')
(ROOT/'Qaroshi_17_Everyday_Communicator.html').write_text(app,encoding='utf8')
print('HTML',len(app))
