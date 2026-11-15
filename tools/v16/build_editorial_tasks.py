#!/usr/bin/env python3
"""Create review briefs for 240 lexical domains lacking independently drafted usage.

These are prompts for future authors, never counted as prose/corpus evidence.
"""
from pathlib import Path
import csv,collections,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/v16';OUT.mkdir(exist_ok=True,parents=True)
def rows(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
idx=rows('data/v16/lexical_evidence_index_30000.csv')
by=collections.defaultdict(list)
for r in idx:by[r['domain']].append(r)
scenarios=[
 ('conversation','Write a disagreement in which two people initially attach different meanings to a word, then repair the misunderstanding.'),
 ('fiction','Write a scene with a concrete problem, a risky choice and a changed outcome; use these words in distinct syntactic frames.'),
 ('memo','Write a short explanatory report that distinguishes direct observation from reported knowledge and inference.'),
 ('letter','Write a letter explaining a decision, its conditions and what you cannot promise.'),
 ('narrative','Write a first-person reflection in which the narrator revises an earlier assumption after new evidence.'),
 ('instructions','Write a practical how-to with a refusal case and an explanation of why a procedure may fail.'),
 ('debate','Write a persuasive argument and the strongest reasonable counterargument, without misusing modal expressions.'),
 ('interview','Write an exchange of questions and answers that establishes where each participant learned their information.'),
]
items=[]
for i,(dom,ws) in enumerate(sorted(by.items()),1):
 ws.sort(key=lambda w:(int(w['original_editorial_occurrences'])>0,int(w['controlled_reference_occurrences'])>0,w['lexeme_type']=='compound',w['qaroshi']))
 # Prefer adding lexical domains never documented in earlier authored corpus.
 targets=[]
 for w in ws:
  if w['pos'] in ('part','register','conj','pron','det'):continue
  if w['lexeme_type']!='compound':targets.append(w)
  if len(targets)>=4:break
 if len(targets)<3:
  for w in ws:
   if w not in targets and w['pos'] not in ('part','register','conj','pron','det'):targets.append(w)
   if len(targets)>=4:break
 style,challenge=scenarios[(i-1)%len(scenarios)]
 items.append({'brief_id':f'DOMAIN16-{i:03d}','domain':dom,'genre_assignment':style,'challenge':challenge,
 'lexical_targets':'; '.join(f"{x['qaroshi']} ({x['canonical_gloss']})" for x in targets),
 'target_headword_ids':'; '.join(x['id'] for x in targets),
 'target_words_already_in_editorial':sum(int(x['original_editorial_occurrences'])>0 for x in targets),
 'minimum_qaroshi_words':'200','required_independent_text':'yes','source_type':'writing assignment, not an authored corpus text',
 'editorial_quality_requirements':'Distinct context; clear speaker reference; no repeated template; 16-register sentence starts; checked morphology; independent semantic reading',
 'writer':'','draft_path':'','editor1':'','editor2':'','accepted':'no'})
with (OUT/'coverage_writing_briefs_240.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
report=['# Qaroshi 16.0: 240-domain writer and reviewer brief','',
 'These are prompts for future **independently written** Qaroshi texts. They contain no newly attested language and add zero tokens to the approved corpus. The target of at least 200 Qaroshi words per domain would give 48,000 words of new drafts if all prompts were completed.','',
 'Each assignment should pass two passes: (1) morphological/grammatical consistency and (2) contextual meaning and literary coherence by a separate reader. The 15.1 procedural corpus cannot substitute for those reviews.','']
for r in items:
 report+=['## '+r['brief_id']+' · '+r['domain'],'','**Genre:** '+r['genre_assignment'],'',r['challenge'],'','**Target source words:** '+r['lexical_targets'],'',
 '**Quality check:** preserve mandatory resonance, identify references, avoid recycled sentence frames, and record editorial disagreements.','']
(ROOT/'docs/v16/WRITING_BRIEFS_240_DOMAINS.md').write_text('\n'.join(report),encoding='utf8')
print('assignments',len(items),'target planned words',len(items)*200)
