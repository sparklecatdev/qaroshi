#!/usr/bin/env python3
"""Compare contextual paraphrases with literal grammar-engine interpretations.

This flags differences for manual review. String similarity is not semantic proof.
"""
import csv,json,difflib,collections,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
texts=json.loads((ROOT/'corpus/original11/dialogues.json').read_text(encoding='utf8'))
rows=[]
for d in texts:
 for index,t in enumerate(d['turns'],1):
  literal=t['literal_translation'] or ''
  contextual=t['english']
  ratio=difflib.SequenceMatcher(None,literal.casefold(),contextual.casefold()).ratio()
  if ratio<.40:flag='priority semantic review'
  elif ratio<.70:flag='contextual paraphrase review'
  else:flag='close surface alignment; still requires human review'
  rows.append({'scene_id':d['id'],'turn':index,'speaker':t['speaker'],'qaroshi':t['qaroshi'],
               'literal_interpretation':literal,'contextual_english':contextual,
               'string_similarity_heuristic':f'{ratio:.3f}','flag':flag,
               'source':'unverified editorial translation, not independent speaker evidence',
               'reviewer':'','decision':'','notes':''})
with (ROOT/'corpus/original11/review_ledger.csv').open('w',encoding='utf8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
report={'scenes':len(texts),'turns':len(rows),'unique_contextual_english':len(set(r['contextual_english'] for r in rows)),
 'unique_qaroshi_sentences':len(set(r['qaroshi'] for r in rows)),
 'prioritized_for_review':collections.Counter(r['flag'] for r in rows),
 'warning':'Similarity ranking merely organizes editorial review; it cannot determine semantic equivalence or idiomaticity.'}
(ROOT/'corpus/original11/quality_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
