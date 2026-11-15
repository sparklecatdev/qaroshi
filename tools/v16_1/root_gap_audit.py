#!/usr/bin/env python3
"""Find missing standalone semantic building blocks; do not fabricate new roots."""
from __future__ import annotations
import sys,csv,json,re
from collections import defaultdict, Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from headword_audit import load_csv, norm, index, head, OUT
GAPS=defaultdict(lambda:{'targets':set(),'evidence':[]})
STOP={'a','an','the','of','and','or','for','to','with','in','on','at','from','by','as','without','not','into','over','under','across'}
for x in head:
 if x['pos']!='n':continue
 words=norm(x['english'].split(';')[0]).split()
 if not 2<=len(words)<=4:continue
 for i in range(1,len(words)):
  a=' '.join(words[:i]);b=' '.join(words[i:])
  aok=any(r['pos'] in ('n','adj') for r in index.get(a,[]))
  bok=any(r['pos']=='n' for r in index.get(b,[]))
  if aok and not bok and 1<=len(b.split())<=2 and b not in STOP and not any(v in STOP for v in b.split()):
   entry=GAPS[('missing_noun_head',b)];entry['targets'].add(x['qaroshi']);entry['evidence'].append((x['qaroshi'],x['english'],a))
  if bok and not aok and 1<=len(a.split())<=2 and a not in STOP and not any(v in STOP for v in a.split()):
   entry=GAPS[('missing_modifier',a)];entry['targets'].add(x['qaroshi']);entry['evidence'].append((x['qaroshi'],x['english'],b))
rows=[]
for (role,stem),v in GAPS.items():
 roots=len(v['targets']);examples=' | '.join(f"{q} = {en}" for q,en,_ in v['evidence'][:6]);
 rows.append({'priority_count':roots,'missing_english_concept':stem,'role':role,'affected_canonical_headwords':roots,
 'examples':examples,'proposed_qaroshi_root':'','root_has_been_coined':'no',
 'editorial_next_step':'Seek existing semantic equivalent, define sense boundary, then optionally coin ONE reusable base root with grammar/phonology review; do not auto-approve.',
 'review_status':'needs review'})
rows.sort(key=lambda x:(-x['priority_count'],x['missing_english_concept']))
with (OUT/'root_gap_priorities.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={'unique_missing_english_concept_gaps':len(rows),'missing_heads':sum(r['role']=='missing_noun_head' for r in rows),
 'missing_modifiers':sum(r['role']=='missing_modifier' for r in rows),
 'gaps_affecting_3_or_more_headwords':sum(r['priority_count']>=3 for r in rows),'top_20':[{'english':r['missing_english_concept'],'role':r['role'],'headwords':r['priority_count']} for r in rows[:20]],
 'new_qaroshi_roots_coinages':0,'interpretation':'English missing-component concepts are candidate semantic gaps, not proof no suitable Qaroshi synonym exists.'}
(OUT/'root_gap_manifest.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
