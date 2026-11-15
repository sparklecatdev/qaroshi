#!/usr/bin/env python3
"""Single-file offline Qaroshi 11 learning and reference site."""
import json, csv, base64, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
read=lambda name:json.loads((ROOT/name).read_text(encoding='utf8'))
with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f:
    lex=[[r['qaroshi'],r['english'],r['pos'],r['ipa']] for r in csv.DictReader(f)]
with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:
    examples=[{k:r[k] for k in ('id','qaroshi','english')} for r in csv.DictReader(f)]
glyphs={p.stem:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() for p in sorted((ROOT/'assets/glyphs_display').glob('*.png'))}
resonance=[['më','Tender'],['zha','Joyful'],['qor','Solemn'],['sen','Neutral'],['hë','Inquisitive'],['lën','Shy'],['sur','Grieving'],['rak','Defiant'],['khar','Alarmed'],['yë','Surprised'],['nëm','Calm'],['wen','Longing'],['dal','Determined'],['rëm','Proud'],['hol','Grateful'],['zher','Uncertain']]
aff={'ri':'plural','m':'direct object','na':'genitive/possession','lo':'location','gu':'goal','de':'source','wa':'companionship','tu':'recipient','shi':'instrument','së':'topic','lë':'diminutive', 'te':'past','yu':'future','se':'progressive','mo':'completive','në':'habitual','ki':'ability','ho':'permission','du':'obligation','la':'tender manner','ru':'causative','li':'passive','wo':'reciprocal','ne':'reflexive'}
D={
 'lex':lex,'examples':examples,'pairs':read('data/fluency11/translation_pairs.json'),
 'questions':read('data/fluency11/proficiency_questions.json'),'levels':read('data/fluency11/proficiency_levels.json'),
 'dialogues':read('corpus/original11/dialogues.json'),'readings':read('corpus/curated/short_readings.json'),
 'glyphs':glyphs,'registers':resonance,'affixes':aff}
template=(ROOT/'web/fluency11/index_template.html').read_text(encoding='utf8')
text=template.replace('__DATA__',json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
out=ROOT/'Qaroshi_Fluency_11.html';out.write_text(text,encoding='utf8')
js=text.split('<script>')[-1].split('</script>')[0]
(ROOT/'web/fluency11/runtime.js').write_text(js,encoding='utf8')
meta={'lexicon_entries':len(lex),'reference_examples':len(examples),'translation_pairs':len(D['pairs']),
 'quiz_items':len(D['questions']),'proficiency_levels':len(D['levels']),'original_scenes':len(D['dialogues']),
 'original_turns':sum(len(x['turns']) for x in D['dialogues']),
 'human_attested_dialogues':0,'app_bytes':out.stat().st_size,
 'qualification_note':'Self-study only. Not CEFR accredited or an independent speaker credential.'}
(ROOT/'data/fluency11/site_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(meta,ensure_ascii=False,indent=2))
