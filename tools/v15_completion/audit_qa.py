#!/usr/bin/env python3
"""Quality audit for Qaroshi 15.1 corpus with explicit human-review gates."""
from pathlib import Path
import csv,json,collections,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'corpus/v15_completion'
def read(filename):
 with (OUT/filename).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
rows=read('complete_corpus_rows.csv');cat=read('complete_piece_catalog.csv');man=json.loads((OUT/'completion_manifest.json').read_text(encoding='utf8'))
line_groups=collections.defaultdict(list)
for x in rows:line_groups[x['qaroshi']].append(x)
record_review=[]
for row in read('aligned_generated.csv'):
 if row['rule_ids']:
  record_review.append({'record_id':row['record_id'],'piece_id':row['piece_id'],'title':row['piece_title'],
    'category':'complex clause scope','rule_ids':row['rule_ids'],'qaroshi':row['qaroshi'],
    'contextual_english':row['english_contextual'],
    'editorial_problem':'Coordinator or conditional requires review for participant scope and discourse licensing',
    'structural_status':row['surface_valid'], 'human_decision':'','reviewer':'','corrected_source':'','corrected_translation':''})
with (OUT/'complex_clause_review_queue.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(record_review[0]));w.writeheader();w.writerows(record_review)
# Contextually divergent English renderings can be legitimate; this is a review queue.
variations=[]
for q,rs in line_groups.items():
 meanings={x['english_contextual'] for x in rs}
 if len(meanings)<2:continue
 variations.append({'qaroshi':q,'occurrences':len(rs),'distinct_contextual_english':len(meanings),
  'english_samples':' || '.join(sorted(meanings)[:4]),'source_id_samples':';'.join(x['record_id'] for x in rs[:4]),
  'review_state':'unresolved; contextual variants NOT automatically contradictions'})
with (OUT/'translation_variation_review.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(variations[0]));w.writeheader();w.writerows(variations)
repeated=[]
for q,rs in line_groups.items():
 if len(rs)<=1:continue
 repeated.append({'qaroshi':q,'occurrences':len(rs),'genre_count':len({x['genre'] for x in rs}),
 'distinct_english_count':len({x['english_contextual'] for x in rs}),
 'human_review_needed':'check frequency naturalness; formulaic reuse is not independent language evidence'})
repeated.sort(key=lambda x:-x['occurrences'])
with (OUT/'repeated_forms_quality.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(repeated[0]));w.writeheader();w.writerows(repeated)
forms=collections.Counter(tok.split('-')[0].strip('.,?!').lower() for r in rows for tok in r['qaroshi'].split())
with (OUT/'lexeme_frequency.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.writer(f);w.writerow(['surface_root','occurrences'])
 for root,n in forms.most_common():w.writerow([root,n])
# Source preservation includes all 26 native glyph PNGs, not only headword counts.
baseline=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))['sha256']
for path,expected in baseline.items():
    p=ROOT/path
    assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==expected,('baseline mutated',path)
assert len(baseline)==29
assert len(rows)==man['total_parallel_utterances']
assert len(record_review)==1988, len(record_review)
assert sum(int(x['source_language_whitespace_tokens']) for x in cat)==man['source_language_token_count_whitespace']
assert len({x['piece_id'] for x in cat})==len(cat)
assert len([x for x in cat if x['kind']=='dialogue'])==1000
assert len({tuple(r['qaroshi'] for r in rows if r['piece_id']==x['piece_id']) for x in cat if x['origin']=='procedural_editorial' and x['kind']=='dialogue'})==824
summary={'canonical_source_files_bytewise_preserved':len(baseline),
 'all_dialogues':1000,'separately_drafted_editorial_dialogues':176,'procedural_dialogue_instances':824,
 'all_prose':205,'separately_drafted_editorial_prose':35,'procedural_prose_instances':170,
 'all_source_language_tokens':man['source_language_token_count_whitespace'],
 'repeated_sentence_occurrences':man['repeated_sentence_occurrences'],
 'repeated_sentence_percentage':round(100*man['repeated_sentence_occurrences']/len(rows),2),
 'unique_sentence_forms':man['unique_exact_source_sentences'],
 'unique_lexeme_roots':len(forms),
 'complex_clause_review_queue':len(record_review),
 'translation_variation_groups':len(variations),
 'independent_speaker_attestations':0,
 'editorial_human_semantic_approvals':0,
 'warning':'Raw volume thresholds have been met only by including procedurally composed synthetic examples; the naturalistic independent-authorship goal is not met. A structural pass does not certify this corpus for standardization.'}
(OUT/'qa_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,indent=2))
