#!/usr/bin/env python3
"""Editorial corpus QA: repetition, translation divergence, source provenance.
Never turns heuristics into speaker-validated naturalness claims.
"""
from pathlib import Path
import collections,csv,json,re,statistics
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v15';OUT.mkdir(parents=True,exist_ok=True)
with (ROOT/'corpus/v15/full_editorial_parallel.csv').open(encoding='utf8') as f:ALL=list(csv.DictReader(f))
with (ROOT/'corpus/v15/corpus_rows.csv').open(encoding='utf8') as f:NEW=list(csv.DictReader(f))
def key(s):return ' '.join(s.lower().split())
groups=collections.defaultdict(list)
for x in ALL: groups[key(x['qaroshi'])].append(x)
review=[]
for sentence,rs in groups.items():
 en=collections.defaultdict(list)
 for r in rs:en[key(r['english_contextual'])].append(r)
 if len(en)>1:
  review.append({'qaroshi':rs[0]['qaroshi'],'number_of_occurrences':len(rs),'distinct_contextual_english_readings':len(en),
                'contextual_english_samples':' || '.join(list(en)[:6]),
                'piece_ids':';'.join(sorted({r['piece_id'] for r in rs})[:15]),
                'review_severity':'attention' if len(en)>3 else 'observe',
                'interpretation':'Different English renderings may reflect context or actual inconsistency; human adjudication needed.'})
review.sort(key=lambda x:(-x['distinct_contextual_english_readings'],-x['number_of_occurrences'],x['qaroshi']))
with (OUT/'cross_release_translation_variants.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(review[0]));w.writeheader();w.writerows(review)
# New-release divergence independently counted, not conflated with earlier 115 v14 clusters.
g2=collections.defaultdict(list)
for x in NEW:g2[key(x['qaroshi'])].append(x)
newdiv=[(q,len({key(r['english_contextual']) for r in rr}),len(rr)) for q,rr in g2.items() if len({key(r['english_contextual']) for r in rr})>1]
# Unusual concentration of repeatedly used phrases is an editorial warning, not evidence of a defect.
freq=collections.Counter(key(x['qaroshi']) for x in NEW)
repeated=sum(n for n in freq.values() if n>1)
report={'all_reviewable_editorial_lines':len(ALL), 'all_source_whitespace_tokens':sum(len(r['qaroshi'].split()) for r in ALL),
        'all_distinct_sentence_surfaces':len(groups),'cross_release_contextual_translation_variation_groups':len(review),
        'new_release_lines':len(NEW),'new_release_distinct_sentences':len(freq),
        'new_release_repeated_surface_instances':repeated,'new_release_repetition_rate':round(repeated/len(NEW),4),
        'new_release_english_variant_groups':len(newdiv),'most_repeated_new_sentence_forms':freq.most_common(12),
        'quality_criterion':'Separate narrative contexts and independent drafting were used. Frequent formulaic language remains; this is editorial teaching data, not authentic naturalistic speech.',
        'review_criterion':'Semantic variations are not adjudicated automatically; independent reviewers must decide what English translation is licensed by the source.'}
(OUT/'quality_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
