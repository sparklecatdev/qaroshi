#!/usr/bin/env python3
"""Generate reproducible learner data from checked Qaroshi source material.

Self-study testing only, not an accredited external proficiency examination.
"""
import json,csv,re,sys,random,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/fluency11'))
from engine import parse_qaroshi,generate_qaroshi,CORPUS_Q,CORPUS_EN,LEX,RESONANCES,words
R=random.Random(1100)
OUT=ROOT/'data/fluency11';OUT.mkdir(exist_ok=True,parents=True)
orig=json.loads((ROOT/'corpus/original11/dialogues.json').read_text(encoding='utf8'))
contrasts=json.loads((ROOT/'data/semantics/minimal_contrasts.json').read_text(encoding='utf8'))
LEVELS=[
 {'id':'q1','name':'Foundation','focus':'Resonance, core vocabulary and basic word order','target':0.75},
 {'id':'q2','name':'Structure','focus':'Plural, cases, possession and complete clauses','target':0.78},
 {'id':'q3','name':'Expression','focus':'Past, future, aspect, negation and modality','target':0.80},
 {'id':'q4','name':'Reasoning','focus':'Reported evidence, uncertainty, questions and scope','target':0.82},
 {'id':'q5','name':'Connected fluency','focus':'Coherent reading, contextual interpretation and translation','target':0.85},
]
QUESTIONS=[]
def add(level,kind,prompt,options,answer,explanation,source_id):
    if answer not in options or len(set(options))!=len(options) or len(options)<2:return
    QUESTIONS.append({'id':f'Q11-{len(QUESTIONS)+1:05d}','level':level,'kind':kind,'prompt':prompt,
                      'choices':options,'correct':options.index(answer),'explanation':explanation,
                      'source':source_id,'status':'editorial self-study item, not independent proficiency certification'})
# Core words
NOUNS={'kima':'water','naro':'home','mara':'friend','sëra':'star','shiwaro':'message','shima':'book','banu':'wing','moru':'memory',
       'gëro':'throat','wena':'sky','runa':'chosen family','lushënga':'storm','shenaro':'device','shëno':'question','qaro':'Nardoragon'}
for k,v in NOUNS.items():
    ds=[v]+R.sample([vv for kk,vv in NOUNS.items() if kk!=k],3)
    R.shuffle(ds);add('q1','lexicon',f'Which English word best corresponds to {k}?',ds,v,
                      f'{k} is defined in the preserved reference as {LEX[k]["english"]}.',f'LEX:{k}')
# Resonance modes
for k,v in RESONANCES.items():
    other=R.sample([vv for kk,vv in RESONANCES.items() if kk!=k],3)
    ds=[v,*other];R.shuffle(ds)
    add('q1','resonance',f'Which stance does sentence-initial {k} conventionally signal?',ds,v,
        'Resonance is a mandatory written pragmatic marker, separate from propositional truth.',f'REG:{k}')
# 26 letters from source phoneme list
phon=json.loads((ROOT/'data/phoneme_inventory.json').read_text(encoding='utf8'))
for p in phon:
    opts=[p['glyph']]+R.sample([x['glyph'] for x in phon if x['glyph']!=p['glyph']],3)
    R.shuffle(opts)
    add('q1','glyph','Which romanized letter corresponds to this native glyph?',opts,p['glyph'],
        'Each of the 26 original signs corresponds to a distinct Qaroshi letter. sh/zh/kh/ng each count as one letter.',f'GLYPH:{p["glyph"]}')
# Morphological minimal contrasts
for c in contrasts:
    options=[a['qaroshi'] for a in c['choices']]
    level=('q3' if c['family'] in ('tense','aspect','modality','voice') else
           'q4' if c['family'] in ('evidential','logic','scope','discourse') else 'q2')
    for choice in c['choices']:
        add(level,'contrast',f'Which Qaroshi sentence means: {choice["english"]}',options,
            choice['qaroshi'],c['explanation'],c['id'])
# Fully aligned, distinct reading comprehension prompts from curated scenes.
# Choose uniquely different distractor English meanings, keeping the correct source line visible.
for d in orig:
    good=[t for t in d['turns'] if len(t['english'])>12]
    for idx in [0,max(1,len(good)//2)]:
        t=good[idx]
        distract=[x['english'] for x in d['turns'] if x['english']!=t['english']]
        pool=list(dict.fromkeys(distract))
        if len(pool)<3:pool+=['I have not yet been told.','We should ask a question.','I will rest at home.']
        opts=[t['english']]+R.sample(pool,3);R.shuffle(opts)
        add('q5','dialogue',f'{d["title"]}: what is the intended contextual reading of “{t["qaroshi"]}”?',
            opts,t['english'],f'{d["premise"]}. This is an editorial contextual gloss, not an attested natural utterance.',d['id'])
# Combinatorial, but grammatically controlled machine-readable translation pairs.
subjects=['I','you','we','they'];intr=['fly','rest','stay','learn','speak'];trans={
 'drink':['water'],'protect':['me','you','a friend','a Nardoragon'],
 'see':['a star','a friend','a Nardoragon','the sky','a message'],
 'cherish':['me','you','a friend','a Nardoragon'],
 'help':['me','you','a friend'],
 'read':['a book','a message','a memory'],
 'write':['a message','a memory','a book'],
 'send':['a message'],'have':['a book','a friend','a home','a memory'],
 'repair':['a device'], 'ask':['a question']}
auxes=['','will ','can ','may ','must ','did ','do not ','will not ','cannot ']
pairs={}
for subject in subjects:
 for verb in intr:
  for aux in auxes:
   text=f'{subject} {aux}{verb}'.strip()+'.'
   v=generate_qaroshi(text)
   if v['translation']:
    parsed=parse_qaroshi(v['translation'])
    if parsed['translation']:
     pairs[(text.lower().rstrip('.'),v['translation'].lower().rstrip('.'))]={'en':text,'qr':v['translation'],
          'parsed_en':parsed['translation'],'confidence':v['confidence'],'note':v['warnings'][0] if v.get('warnings') else ''}
 for verb,objects in trans.items():
  for obj in objects:
   if (subject=='I' and obj=='me') or (subject=='you' and obj=='you'):continue
   for aux in auxes:
    text=f'{subject} {aux}{verb} {obj}'.strip()+'.'
    v=generate_qaroshi(text)
    if v['translation']:
     parsed=parse_qaroshi(v['translation'])
     if parsed['translation']:
      pairs[(text.lower().rstrip('.'),v['translation'].lower().rstrip('.'))]={'en':text,'qr':v['translation'],
       'parsed_en':parsed['translation'],'confidence':v['confidence'],'note':v['warnings'][0] if v.get('warnings') else ''}
for subject in subjects:
 for verb in intr+list(trans):
  for aux in ['can','may','will','did','do']:
   objs=[None] if verb in intr else trans[verb]
   for obj in objs:
    if (subject=='I' and obj=='me') or (subject=='you' and obj=='you'):continue
    text=f'{aux} {subject} {verb}'+(' '+obj if obj else '')+'?'
    v=generate_qaroshi(text)
    if v['translation']:
     parsed=parse_qaroshi(v['translation'])
     if parsed['translation']:
      pairs[(text.lower().rstrip('?'),v['translation'].lower().rstrip('?'))]={'en':text,'qr':v['translation'],'parsed_en':parsed['translation'],'confidence':v['confidence'],'note':''}
PAIRS=list(pairs.values());PAIRS.sort(key=lambda x:(x['en'],x['qr']))
# Add translation evaluation Q for distinct English prompts.
seen_en=set()
for i,p in enumerate(PAIRS):
    if p['en'] in seen_en or i%13:continue
    seen_en.add(p['en'])
    distract=[x['qr'] for x in PAIRS[(i+5)%len(PAIRS):(i+70)%len(PAIRS)] if x['qr']!=p['qr']]
    if len(distract)<3:distract=R.sample([x['qr'] for x in PAIRS if x['qr']!=p['qr']],3)
    opts=[p['qr']]+list(dict.fromkeys(distract))[:3]
    if len(opts)<4:continue
    R.shuffle(opts)
    add('q4' if p['en'].lower().startswith(('may','can','must','did')) else 'q3','translation',
        f'Choose the Qaroshi rendering of: {p["en"]}',opts,p['qr'],
        f'Within this controlled template the sentence is {p["qr"]}. Alternate resonance choices are possible.',f'T:{i}')
# Fill and ensure all tiers have solid coverage.
perlevel={lv['id']:sum(q['level']==lv['id'] for q in QUESTIONS) for lv in LEVELS}
report={'dialogues':len(orig),'dialogue_turns':sum(len(x['turns']) for x in orig),'translation_pairs':len(PAIRS),
        'questions':len(QUESTIONS),'by_level':perlevel,'original_utterance_provenance':'editorial distinct scene scripts; not spontaneous/attested',
        'proficiency_status':'unofficial self-study only, no CEFR or formal accreditation'}
(OUT/'translation_pairs.json').write_text(json.dumps(PAIRS,ensure_ascii=False,separators=(',',':')),encoding='utf8')
(OUT/'proficiency_questions.json').write_text(json.dumps(QUESTIONS,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'proficiency_levels.json').write_text(json.dumps(LEVELS,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'curriculum_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
