#!/usr/bin/env python3
"""Audit the 16,525 noncompound headwords for documented, reviewable transparency.

This is NOT etymological reconstruction and never mutates canonical data.
An exact English modifier–head split proposes an *optional* parallel
paraphrase, not an automatically valid new dictionary entry.
"""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict, Counter
import csv, json, re, hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v16_1';OUT.mkdir(exist_ok=True,parents=True)

def load_csv(path):
 with Path(path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def output_csv(path,rows):
 assert rows,'No rows'
 with (OUT/path).open('w',encoding='utf-8',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0].keys()));wr.writeheader();wr.writerows(rows)
def norm(s):
 s=re.sub(r'\([^()]*\)',' ',s.casefold().replace('-',' '))
 return ' '.join(re.findall(r'[a-z0-9]+',s))
lex=load_csv(ROOT/'data/lexicon.csv')
lookup={x['qaroshi']:x for x in lex}
head=[x for x in lex if x['type']=='headword']
assert len(lex)==30000 and len(head)==16525
index=defaultdict(list)
for x in head:
 for gl in x['english'].split(';'):
  name=norm(gl)
  if name and len(name.split())<=4:index[name].append(x)
# Explicit compound roots get a small secondary preference, but no root is considered predictable from spelling.
root_pop=Counter()
for x in load_csv(ROOT/'data/v16/productive_root_learning_ladder.csv'):
 root_pop[x['root']]=int(x['compounds_using_base_root'])
evidence={x['qaroshi']:x for x in load_csv(ROOT/'data/v16/lexical_evidence_index_30000.csv')}

def token_gloss_chunks(phrase):
 parts=phrase.split();found=[]
 for i in range(len(parts)):
  for j in range(i+1,min(len(parts),i+4)+1):
   chunk=' '.join(parts[i:j]);choices=index.get(chunk,[])
   if choices:found.append((i,j,chunk,choices))
 return found

def proposals(x):
 """Exact 2 constituent split. Prefer short, reusable modifiers and noun heads.

 No assumed suffixes, no unreviewed English synonyms, and no change to canonical forms.
 """
 if x['pos']!='n':return []
 out=[];english=x['english'].split(';')[0]
 parts=norm(english).split()
 if len(parts)<2 or len(parts)>5:return []
 for i in range(1,len(parts)):
  left,right=' '.join(parts[:i]),' '.join(parts[i:])
  a=[z for z in index.get(left,[]) if z['pos'] in ('n','adj') and z['qaroshi']!=x['qaroshi']]
  b=[z for z in index.get(right,[]) if z['pos']=='n' and z['qaroshi']!=x['qaroshi']]
  for l in a:
   for r in b:
    if l['qaroshi']==r['qaroshi']:continue
    candidate=l['qaroshi']+r['qaroshi']
    if len(candidate)>37:continue
    collision=lookup.get(candidate)
    if collision and norm(collision['english'].split(';')[0])!=norm(english):continue
    primary_left=(norm(l['english'].split(';')[0])==left)
    primary_right=(norm(r['english'].split(';')[0])==right)
    v={'source_left_gloss':left,'source_right_gloss':right,'primary_sense_on_both':bool(primary_left and primary_right),'primary_on_modifier':primary_left,'primary_on_head':primary_right,'expression':candidate,'modifier':l['qaroshi'],'head':r['qaroshi'],'modifier_english':l['english'].split(';')[0], 'head_english':r['english'].split(';')[0],
      'split_at_word':i,'is_existing_dictionary_form':bool(collision),
      'collision_id':collision['id'] if collision else '',
      'score':(60*(primary_left and primary_right)+15*primary_left+15*primary_right+max(0,37-len(candidate))+5*(len(l['qaroshi'])<=6)+5*(len(r['qaroshi'])<=6)+min(root_pop[l['qaroshi']],50)/4+min(root_pop[r['qaroshi']],50)/4+(10 if collision else 0))}
    out.append(v)
 return sorted(out,key=lambda v:(-v['score'],len(v['expression']),v['expression']))[:5]

records=[];candidate_rows=[];status=Counter();head_pos=Counter();found_source=0
for x in head:
 q=x['qaroshi'];en=x['english'].split(';')[0];n=norm(en);all_p=proposals(x); ev=evidence.get(q,{})
 internal=[z for z in all_p if z['expression']==q]
 p=[z for z in all_p if z['expression']!=q]
 # Components are semantic *teaching anchors*, not a derivational segmenter.
 # Only exact contiguous English substrings may be mapped to existing headwords.
 chunks=token_gloss_chunks(n)
 anchors=[];seen=set()
 for i,j,chunk,choices in chunks:
  for a in sorted(choices,key=lambda z:(-root_pop[z['qaroshi']],len(z['qaroshi'])))[:2]:
   if a['qaroshi'] in seen or a['qaroshi']==q:continue
   seen.add(a['qaroshi']);anchors.append((i,j,chunk,a))
 anchors=sorted(anchors,key=lambda z:(-(z[1]-z[0]),-root_pop[z[3]['qaroshi']],len(z[3]['qaroshi'])))[:5]
 has_real_reuse=int(ev.get('original_editorial_occurrences') or 0)
 has_controlled=int(ev.get('controlled_reference_occurrences') or 0)
 if internal:state='preexisting_compoundlike_headword'
 elif p:state='primary_gloss_candidate' if p[0]['primary_sense_on_both'] else 'secondary_sense_candidate'
 elif anchors:state='semantic_anchors_only'
 else:state='no_documented_derivation'
 status[state]+=1;head_pos[x['pos']]+=1
 notes=('The existing canonical spelling matches known modifier + head spellings. No new spelling is proposed; classification metadata may merit a correction.' if internal else 'Exact source-gloss match for two parts. Candidate FORM only: noun modifier–head semantics, word choice, lexicalization and native acceptability require review.' if p else 'English keywords have dictionary anchors, but NO licensed Qaroshi derivation is established.' if anchors else 'No documented lexical derivation; teach as a conventional lexical base until a reviewed analysis exists.')
 best=p[0] if p else {}
 row={'id':x['id'],'qaroshi':q,'ipa':x['ipa'],'part_of_speech':x['pos'],'english':x['english'],'domain':x['domain'],
  'word_gloss_count':len(n.split()),'analysis_status':state,
  'possible_existing_component_sequence':(' + '.join([internal[0]['modifier'],internal[0]['head']]) if internal else ''),
  'proposed_transparent_form':best.get('expression',''),'proposed_modifier':best.get('modifier',''),'modifier_meaning':best.get('modifier_english',''),
  'proposed_head':best.get('head',''),'head_meaning':best.get('head_english',''),
  'existing_alternative':str(bool(best.get('is_existing_dictionary_form',False))).lower(),
  'primary_sense_component_match':str(bool(best.get('primary_sense_on_both',False))).lower(),
  'other_exact_candidates': ' | '.join(z['expression'] for z in p[1:]),
  'grounded_english_anchors':' | '.join(f"{z[3]['qaroshi']}={z[2]}" for z in anchors),
  'reference_examples':has_controlled,'independent_editorial_occurrences':has_real_reuse,
  'learning_priority':round(100*min(has_real_reuse,4)+15*min(has_controlled,4)+min(root_pop[q],400)/2+max(0,24-len(q)),1),
  'rationale':notes,'review_decision':'pending','reviewer_notes':''}
 records.append(row)
 for altno,v in enumerate(p,1):
  candidate_rows.append({'target_id':x['id'],'canonical_word':q,'canonical_english':x['english'],'candidate_number':altno,
   'candidate_form':v['expression'],'components_match_primary_glosses':str(v['primary_sense_on_both']).lower(),
   'matched_english_modifier':v['source_left_gloss'],'matched_english_head':v['source_right_gloss'],'component_1':v['modifier'],'component_1_english':v['modifier_english'],
   'component_2':v['head'],'component_2_english':v['head_english'],'is_already_canonical':str(v['is_existing_dictionary_form']).lower(),
   'rule':'modifier + nominal head (uninflected lexical proposal)','meaning_alignment':'exact first-English-gloss word split; translation nuance not attested',
   'phonetic_and_morphological_status':'noncanonical review candidate unless explicitly existing',
   'review_decision':'pending','reviewer_notes':''})

output_csv('headword_learnability_audit_16525.csv',records)
output_csv('strict_modifier_head_candidates.csv',candidate_rows)
ranked=sorted(records,key=lambda x:(-float(x['learning_priority']),x['qaroshi']))
output_csv('headword_learning_priority_16525.csv',[{'rank':i+1,'headword':r['qaroshi'],'english':r['english'],'pos':r['part_of_speech'],'domain':r['domain'],
 'source_example_count':r['reference_examples'],'independent_editorial_count':r['independent_editorial_occurrences'],
 'compounding_reuse':root_pop[r['qaroshi']],'transparent_proposal':r['proposed_transparent_form'],'status':r['analysis_status'],
 'score':r['learning_priority'],'learnability_note':'Rank is an editorial study heuristic, not a learning experiment'} for i,r in enumerate(ranked)])
# To allow a novice to learn efficiently, generate a small core that is grounded
# in a familiar reference vocabulary and productive compound stems.
core=[];filtered=set()
for r in ranked:
 q=r['qaroshi']
 if q in filtered:continue
 # core rows must have evidenced use OR significant productive reuse
 if int(r['reference_examples']) or int(r['independent_editorial_occurrences']) or root_pop[q]>=5:
  core.append({'rank':len(core)+1,'qaroshi':q,'english':r['english'],'ipa':r['ipa'],'pos':r['part_of_speech'],
   'example_count':r['reference_examples'],'editorial_count':r['independent_editorial_occurrences'],
   'compounds_using_word':root_pop[q], 'study_hint': 'Learn this word as a base unless its derivation has been independently accepted.'})
  filtered.add(q)
 if len(core)==1200:break
output_csv('prioritized_core_1200.csv',core)
report={'canonical_sha256':hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest(),
 'headwords_audited':len(records),'count_by_status':dict(status),'headwords_by_pos':dict(head_pos),
 'exact_split_proposal_rows':len(candidate_rows),'headwords_with_any_exact_split':status['primary_gloss_candidate']+status['secondary_sense_candidate'],
 'existing_headwords_matching_two_component_spellings':status['preexisting_compoundlike_headword'],
 'primary_gloss_candidates':status['primary_gloss_candidate'],'secondary_sense_candidates':status['secondary_sense_candidate'],
 'original_canonical_words_renamed':0,'editorially_approved_new_spellings':0,'function_words_reviewed_here':0,
 'learning_core_rows':len(core), 'qualifications':[
 'Existing headword spellings and meanings have not changed.',
 'Exact English gloss splits suggest optional synonyms/paraphrases, not canonical equivalences.',
 'Split terms found in secondary dictionary glosses may have different connotations; they are flagged separately.',
 'A headword without a proposal is not necessarily meaningless or impossible to derive historically.',
 'No newly proposed word form is labeled an attested utterance or speaker-approved lexical form.',
 'Cross-POS suffix derivation has not been invented. Grammatical morphology remains separate.',
 'The priority score is a reproducible heuristic, not proven ease of language acquisition.',
 'Two existing headwords coincidentally or intentionally match component spellings; these have no new proposed form.',
 'No data generated here licenses a full-scale breaking rename of canonical reference material.'
 ]}
(OUT/'audit_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
