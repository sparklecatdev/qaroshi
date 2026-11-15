#!/usr/bin/env python3
"""Build an offline, provenance-separated Qaroshi 15.1 corpus reading application.

Includes all *existing separately drafted* pieces plus the new explicit
*procedural composition* layer. No unsourced model claims or speaker attestation.
"""
from pathlib import Path
import json,csv,collections,re,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'corpus/v15_completion'
def load(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def readcsv(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def g(row,k,default=''):return row.get(k,default)

original=[]
for x in load('corpus/original11/dialogues.json'):
 original.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':'legacy editorial dialogue','kind':'dialogue','release':'11.0',
  'provenance':'separately drafted editorial exercise; not speaker attested','source_method':'separately scripted editorial',
  'lines':[{'speaker':r['speaker'],'qaroshi':r['qaroshi'],'english_contextual':r['english'],'ipa':r.get('ipa','')} for r in x['turns']]})
for x in load('corpus/v12_13/dialogues_12.json'):
 original.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':'legacy editorial dialogue','kind':'dialogue','release':'12–13',
  'provenance':'separately drafted editorial exercise; not speaker attested','source_method':'separately scripted editorial',
  'lines':[{'speaker':r['speaker'],'qaroshi':r['qaroshi'],'english_contextual':r['english_editorial'],'ipa':r.get('ipa','')} for r in x['turns']]})
for x in load('corpus/v12_13/anthology_12.json'):
 original.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':x['genre'],'kind':'literature','release':'12–13',
  'provenance':'separately drafted editorial exercise; not speaker attested','source_method':'separately scripted editorial',
  'lines':[{'speaker':'NARRATOR','qaroshi':r['qaroshi'],'english_contextual':r['english_editorial'],'ipa':r.get('ipa','')} for r in x['sentences']]})
for x in load('corpus/curated/short_readings.json'):
 original.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':'legacy editorial reading','kind':'literature','release':'13.0',
  'provenance':'separately drafted editorial exercise; not speaker attested','source_method':'separately scripted editorial',
  'lines':[{'speaker':'NARRATOR','qaroshi':r['qaroshi'],'english_contextual':r['english'],'ipa':r.get('ipa','')} for r in x['sentences']]})
for x in load('corpus/v15/pieces.json'):
 original.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':x['genre'],'kind':x['kind'],'release':'15.0',
  'provenance':'separately drafted editorial exercise; not speaker attested','source_method':'separately scripted editorial',
  'lines':[{'speaker':r['speaker'],'qaroshi':r['qaroshi'],'english_contextual':r['english_contextual'],'ipa':r.get('ipa','')} for r in x['lines']]})
assert len(original)==211
assert sum(p['kind']=='dialogue' for p in original)==176
assert sum(p['kind']=='literature' for p in original)==35
orig_token=sum(len(x['qaroshi'].split()) for p in original for x in p['lines'])
assert orig_token==6828,orig_token

procedural=[]
for f in ['new_dialogues.jsonl','new_prose.jsonl']:
 with (OUT/f).open(encoding='utf8') as stream:
  for line in stream:
   x=json.loads(line)
   procedural.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':x['genre'],'kind':x['kind'],
     'release':'15.1 procedural', 'provenance':x['provenance'],'source_method':x['source_method'],
     'plot_arc':x['plot_arc'], 'lines':[{'speaker':v['speaker'],'qaroshi':v['qaroshi'],
       'english_contextual':v['english_contextual'],'ipa':'','rule_ids':v.get('rule_ids',[]),
       'paragraph':v.get('paragraph','')} for v in x['lines']]})
assert len(procedural)==994
assert sum(p['kind']=='dialogue' for p in procedural)==824
assert sum(p['kind']=='literature' for p in procedural)==170
items=original+procedural
assert len({p['id'] for p in items})==len(items),(len(items),len({p['id'] for p in items}))
assert sum(p['kind']=='dialogue' for p in items)==1000
assert sum(p['kind']=='literature' for p in items)==205

lexicon=[[r['qaroshi'],r['english'],r['pos'],r['ipa']] for r in readcsv('data/lexicon.csv')]
assert len(lexicon)==30000
aligned=[];catalog=[];source_lines=[];token_stats=collections.Counter();kind_stats=collections.Counter()
for p in items:
 group='original_editorial' if p in original else 'procedural_editorial'
 tokens=sum(len(l['qaroshi'].split()) for l in p['lines'])
 token_stats[group]+=tokens;kind_stats[(group,p['kind'])]+=1
 catalog.append({'piece_id':p['id'],'title':p['title'],'kind':p['kind'],'genre':p['genre'],'origin':group,
  'release':p['release'],'premise':p['premise'],'source_language_whitespace_tokens':tokens,'number_of_lines':len(p['lines']),
  'provenance':p['provenance'],'speaker_attested':'no','human_semantics_approved':'no'})
 source_lines.extend([f"# [{p['id']}] {p['title']} | {p['kind']} | {group}"]+[l['qaroshi'] for l in p['lines']]+[''])
 for i,l in enumerate(p['lines'],1):
  aligned.append({'record_id':f'{p["id"]}.{i:02d}','piece_id':p['id'],'line':i,'speaker':l['speaker'],'genre':p['genre'],
   'kind':p['kind'],'origin':group,'source_method':p['source_method'],'qaroshi':l['qaroshi'],
   'english_contextual':l['english_contextual'],'ipa':l.get('ipa',''),
   'provenance':p['provenance'],'speaker_attested':'no'})
for filename,records in [('complete_corpus_rows.csv',aligned),('complete_piece_catalog.csv',catalog)]:
 with (OUT/filename).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
(OUT/'all_qaroshi_source_only.txt').write_text('\n'.join(source_lines),encoding='utf8')

tokens_by_origin=dict(token_stats)
new_sum=sum(len(l['qaroshi'].split()) for p in procedural for l in p['lines'])
old_sum=sum(len(l['qaroshi'].split()) for p in original for l in p['lines'])
assert tokens_by_origin=={'original_editorial':old_sum,'procedural_editorial':new_sum}
assert new_sum>100000
forms=collections.Counter(row['qaroshi'] for row in aligned)
wordforms=collections.Counter(tok for row in aligned for tok in row['qaroshi'].split())
ambigs=collections.defaultdict(set)
for r in aligned:ambigs[r['qaroshi']].add(r['english_contextual'])
ambiguous=sum(len(en)>1 for en in ambigs.values())
flagged=collections.Counter((r['qaroshi'],r['record_id']) for r in aligned)
manifest={'release':'15.1 Quantitative Corpus Scale-up, non-naturalistic editorial development',
 'total_dialogue_instances':1000,'original_editorial_dialogues':176,'procedurally_composed_dialogue_instances':824,
 'total_prose_instances':205,'original_editorial_prose':35,'procedurally_composed_prose_instances':170,
 'total_parallel_utterances':len(aligned),'source_language_token_count_whitespace':sum(token_stats.values()),
 'source_language_tokens_by_provenance':tokens_by_origin,
 'source_unique_word_forms':len(wordforms),'unique_exact_source_sentences':len(forms),
 'repeated_sentence_occurrences':sum(v for v in forms.values() if v>1),
 'source_sentence_surface_with_multiple_contextual_english_readings':ambiguous,
 'original_independently_speaker_attested_utterances':0,
 'independently_human_reviewed_lines':0,
 'counting_policy':'Count whitespace-separated Qaroshi graphic tokens only, exclude titles/English/IPA/metadata and the earlier template exercise corpus.',
 'qualitative_limitations':['The 824 new dialogue instances were generated by combining controlled discourse modules; not independently human-authored naturalistic conversations.',
  '170 additional prose pieces are procedural, constrained first-person paragraphs; not literary works with independent human editing.',
  'A large proportion of utterance occurrences reuse the same sentence surfaces; the numeric 100,000-word threshold is not proof of a varied naturalistic corpus.',
  'The pre-existing 123,000-token 1,000-variant teaching drill corpus is NOT counted.',
  'IPA from the original separately drafted pieces is retained. New generated items require naturalness and phonetic-context review.',
  'The 14.0 grammar validator checks recognized morphosyntax, not pragmatic/natural discourse or full semantic truth.']}
(OUT/'completion_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
with (OUT/'genre_metrics.csv').open('w',encoding='utf8',newline='') as f:
 tally=collections.Counter((p['genre'],p['kind'],('original_editorial' if p in original else 'procedural_editorial')) for p in items)
 w=csv.writer(f);w.writerow(['genre','kind','origin','pieces'])
 for (genre,kind,origin),c in sorted(tally.items()):w.writerow([genre,kind,origin,c])

payload={'pieces':[{'id':p['id'],'title':p['title'],'premise':p['premise'],'genre':p['genre'],'kind':p['kind'],
                    'origin':('original' if p in original else 'procedural'), 'release':p['release'],
                    'provenance':p['provenance'],'lines':[[l['speaker'],l['qaroshi'],l['english_contextual'],l.get('ipa',''),l.get('paragraph','')] for l in p['lines']]} for p in items],
 'lexicon':lexicon,'manifest':manifest}
# Pre-loading HTML makes this portable across file://, including offline mobile.
text=(ROOT/'web/v15_completion/browser_template.html').read_text(encoding='utf8')
blob=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
assert '__CORPUS_PAYLOAD__' in text
html=text.replace('__CORPUS_PAYLOAD__',blob)
path=ROOT/'Qaroshi_15_Expanded_Corpus_Library.html'
path.write_text(html,encoding='utf8')
print('Dialogues: 1000 (176 separately drafted, 824 procedurally composed)')
print('Prose:',len([p for p in items if p['kind']=='literature']))
print('Tokens:',sum(token_stats.values()),tokens_by_origin)
print('Total aligned lines:',len(aligned),'Unique sentences:',len(forms),'Repeated sentence occurrences:',manifest['repeated_sentence_occurrences'])
print('Browser bytes:',path.stat().st_size)
