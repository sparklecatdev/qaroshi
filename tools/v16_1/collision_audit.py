#!/usr/bin/env python3
"""Prevent collisions between *proposed* aliases for distinct existing canonical headwords."""
from pathlib import Path
from collections import defaultdict
import csv,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/v16_1'
with (OUT/'strict_modifier_head_candidates.csv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f))
groups=defaultdict(list)
for row in rows:groups[row['candidate_form']].append(row)
issues=[]
for form,entries in sorted(groups.items()):
 unique={r['target_id'] for r in entries}
 if len(unique)<2:continue
 canonical=' | '.join(sorted({r['canonical_word']+' = '+r['canonical_english'] for r in entries}))
 issues.append({'candidate_form':form,'affected_canonical_entries':len(unique),'canonical_meanings':canonical,
 'risk':'Same proposed spelling for distinct existing concepts; must not accept without meaning-disambiguation and editor approval',
 'editorial_status':'blocked_for_review'})
with (OUT/'proposal_collision_review.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(issues[0]));w.writeheader();w.writerows(issues)
report={'cross_headword_candidate_collisions':len(issues),'affected_headword_candidates':sum(r['affected_canonical_entries'] for r in issues),
 'new_words_approved':0,'review_policy':'Do not accept any proposed spelling that maps to distinct target senses without disambiguation.'}
(OUT/'collision_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print(report)
