#!/usr/bin/env python3
"""Deterministically assemble Qaroshi 28–34 lexical/grammar standard overlays.

No new apps, no mass spellings, no invented spontaneous-language attestations.
Outputs are explanatory source-backed data plus a compact, adopted function word.
"""
from __future__ import annotations
import collections,csv,hashlib,json,re,sys,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v28_34';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/v28_34'))
from phonetics import ipa_word,guide_word,graphemes
from reform_content import NEW_DETERMINER,LOGIC_EXAMPLES,DISCOURSE_RULES,LEXICAL_PAIRS,LITERARY_CONVENTIONS,EXEMPLAR_REVIEWED_VERBS
from reform_core import evaluate_on_finite_domain,analyze_quantifier

def readcsv(path):
 with (ROOT/path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def writecsv(path,rows):
 if not rows:raise ValueError('No rows: '+str(path))
 with path.open('w',encoding='utf-8',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');d.writeheader();d.writerows(rows)
def writejson(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lexrows=readcsv('data/lexicon.csv');lex={r['qaroshi']:r for r in lexrows}
assert len(lex)==len(lexrows)==30000 and len({r['id'] for r in lexrows})==30000
corpus=readcsv('corpus/parallel_sentences.csv');assert len(corpus)==4383
phrases=readcsv('data/v17/everyday_phrases.csv');assert len(phrases)==656
frames=json.loads((ROOT/'data/semantics/valency_frames.json').read_text(encoding='utf-8'))
senses=json.loads((ROOT/'data/semantics/curated_senses.json').read_text(encoding='utf-8'))
figurative=json.loads((ROOT/'data/semantics/figurative_expressions.json').read_text(encoding='utf-8'))
contrasts=json.loads((ROOT/'data/semantics/minimal_contrasts.json').read_text(encoding='utf-8'))
compounds=readcsv('data/v16/compound_decomposition_13379.csv');assert len(compounds)==13379
review=readcsv('data/semantics/lexical_migration_decisions_24_27.csv');assert len(review)==65

# 28: real-use priority from *documented* controlled examples; do not
# confuse frequency in this templated corpus with independent speaker usage.
frequency=collections.Counter();refs=collections.defaultdict(list)
verbfrequency=collections.Counter();verb_cases=collections.defaultdict(collections.Counter)
for r in corpus+phrases:
 tokens=re.findall(r'[a-zë]+(?:-[a-zë]+)*',r['qaroshi'].lower())
 for i,t in enumerate(tokens):
  base=t.split('-')[0]
  if base not in lex:continue
  frequency[base]+=1
  if len(refs[base])<4 and r['id'] not in refs[base]:refs[base].append(r['id'])
  if lex[base]['pos']=='v':
   verbfrequency[base]+=1
   for tok in tokens[:i]:
    endings=tok.split('-')[1:]
    if endings and endings[-1] in ('m','tu','lo','gu','de','wa','shi','za'):
     verb_cases[base][endings[-1]]+=1
# Reserve core roots and reviewed words before corpus-derived frequency ranking.
core=readcsv('data/v17/core_learning_120.csv')
manual={r['lemma'] for r in senses};frame_keys={r['lemma'] for r in frames}
keyset={w for w in manual|frame_keys if w in lex}
ordering=sorted(keyset,key=lambda w:(-frequency[w],w)) + [r['root'] for r in core if r['root'] in lex]
ordering+= [w for w,_ in sorted(frequency.items(),key=lambda x:(-x[1],x[0])) if w in lex]
seen=set();top=[]
for w in ordering:
 if w not in seen:seen.add(w);top.append(w)
 if len(top)>=800:break
assert len(top)==800
senses_by=collections.defaultdict(list)
for r in senses:senses_by[r['lemma']].append(r)
rows=[]
for rank,w in enumerate(top,1):
 r=lex[w];reviewed=senses_by[w]
 rows.append({'priority_rank':rank,'dictionary_id':r['id'],'lemma':w,'pos':r['pos'],'reference_gloss':r['english'],
 'domain':r['domain'],'type':r['type'],'corpus_mentions':frequency[w],
 'source_reference_ids':' | '.join(refs[w]),'curated_sense_ids':' | '.join(x['id'] for x in reviewed),
 'lexical_treatment':('normative_editorial_senses_exist' if reviewed else 'reference_gloss_only_no_new_sense_approved'),
 'gloss_interpretation':'English is an indexing gloss, not permission to substitute every English homonym.',
 'speaker_attestation':'none asserted'})
writecsv(OUT/'core_semantic_index_800.csv',rows)

# Selected distinct English lexical senses, not auto-created synonyms.
pairs=[]
for i,(a,b,contrast) in enumerate(LEXICAL_PAIRS,1):
 assert a in lex or a==NEW_DETERMINER['lemma'],(a,contrast)
 assert b in lex or b==NEW_DETERMINER['lemma'],(b,contrast)
 pairs.append({'id':f'S28-{i:03d}','left':a,'left_gloss':lex.get(a,{'english':NEW_DETERMINER['meaning']})['english'],
  'right':b,'right_gloss':lex.get(b,{'english':NEW_DETERMINER['meaning']})['english'],
  'semantic_boundary':contrast,'status':'editorial normative boundary: not a claim of natural-speaker frequency'})
writecsv(OUT/'meaning_boundaries.csv',pairs)

# 29: 25 manually specified frames are normative. The additional 375
# corpus-anchored candidate frames describe *observed syntactic shapes only*;
# the case distribution is not evidence for all allowed arguments or an obligatory
# object. A true dictionary-wide valency assignment still needs individualized review.
frame_map={f['lemma']:f for f in frames}
exemplar_licenses={}
# A limited normative frame requires an exact simple, source-attested case
# pattern, not just a gloss or a loose same-sentence occurrence.
for row in corpus:
 tokens=re.findall(r'[a-zë]+(?:-[a-zë]+)*',row['qaroshi'].lower())
 if len(tokens)<4 or tokens[0] not in ('sen','zha','nëm','më','qor','dal','hë','lën','sur','rak','khar','yë','wen','rëm','hol','zher'):continue
 if not tokens[1]=='mi':continue
 predicate=tokens[-1].split('-')[0]
 if predicate not in EXEMPLAR_REVIEWED_VERBS or predicate in exemplar_licenses:continue
 marked=[t for t in tokens[2:-1] if t.endswith('-m') and t.split('-')[0] in lex and lex[t.split('-')[0]]['pos']=='n']
 if len(marked)!=1:continue
 object_root=marked[0].split('-')[0]
 exemplar_licenses[predicate]={'source_id':row['id'],'source_qaroshi':row['qaroshi'],
   'source_english':row['english'],'object_root':object_root,'object_reference_gloss':lex[object_root]['english']}
assert set(exemplar_licenses)==set(EXEMPLAR_REVIEWED_VERBS),(len(exemplar_licenses),sorted(set(EXEMPLAR_REVIEWED_VERBS)-set(exemplar_licenses)))
ordered_verb=[f['lemma'] for f in frames]+[w for w,_ in verbfrequency.most_common() if w not in frame_map]
ordered_verb=ordered_verb[:400]
assert len(ordered_verb)==400 and len(set(ordered_verb))==400
frame_out=[]
for i,w in enumerate(ordered_verb,1):
 r=lex[w];f=frame_map.get(w);e=exemplar_licenses.get(w)
 casecounts=verb_cases[w];observed=' | '.join(f'-{k}:{casecounts[k]}' for k in sorted(casecounts))
 status=('normative_manual_frame_24_27' if f else
   'source_exemplar_limited_license' if e else 'corpus_observed_provisional_roles')
 req=(' | '.join(f['required_roles']) if f else
   'subject:documented_actor | object:-m (only this source-licensed target)' if e else 'not individually assigned')
 optional=(' | '.join(f['licensed_optional_roles']) if f else 'none inferred from this exemplar' if e else 'not individually assigned')
 infer=(' | '.join(f['disallowed_inferences']) if f else
   'no unsupported object class, causative or passive extrapolation' if e else 'no additional claims')
 frame_out.append({'frame_id':f'VF29-{i:04d}','lemma':w,'dictionary_id':r['id'],'reference_gloss':r['english'],
 'source_count_controlled':verbfrequency[w],'example_ids':' | '.join(refs[w]),
 'observed_case_counts':observed,'review_status':status,
 'reviewed_required_roles':req,'reviewed_optional_roles':optional,'disallowed_inferences':infer,
 'licensed_exemplar_id':e['source_id'] if e else '',
 'licensed_exemplar_qaroshi':e['source_qaroshi'] if e else '',
 'licensed_object_root':e['object_root'] if e else '',
 'licensed_object_gloss':e['object_reference_gloss'] if e else '',
 'passive_actor_case':'-za if licensed for reviewed transitive sense' if f and f['frame']!='V0' else ('not applicable to reviewed intransitive sense' if f else 'not adjudicated'),
 'caution':('Only the exact editorial exemplar object slot is licensed; other senses, patients and voice changes need separate review.' if e else
            'Observed in editorial reference text; not proof of complete valency or native use.')})
writecsv(OUT/'verb_frame_inventory_400.csv',frame_out)

# 30: one new productive lexical determiner, with explicit finite-model truth
# testing, a fixed POS, IPA, and compatibility with historical lexicon hashes.
assert NEW_DETERMINER['lemma'] not in lex
newword=dict(NEW_DETERMINER)
newword.update({'ipa':ipa_word(newword['lemma']),'reading':guide_word(newword['lemma']),
                'source_id':'Q28D001','written_glyph_count':len(graphemes(newword['lemma']))})
writejson(OUT/'adopted_function_words.json',[newword])
logic=[]
for id,q,kind,english,formula,caveat in LOGIC_EXAMPLES:
 logic.append({'id':id,'qaroshi':q,'meaning':english,'operator':kind,'logical_form':formula,'caveat':caveat,
   'provenance':'editorial norm-setting example (not native speaker attestation)'})
 assert not q.startswith(' ')
writecsv(OUT/'quantifier_scope_examples.csv',logic)
models=[]
for n in (0,1,2,3,4):
 for yes in range(n+1):
  values=[True]*yes+[False]*(n-yes)
  models.append({'domain_size':n,'predicate_true_members':yes,
    'every':evaluate_on_finite_domain('every',values),
    'none':evaluate_on_finite_domain('none',values),
    'not_every':evaluate_on_finite_domain('not_every',values),
    'some':evaluate_on_finite_domain('some',values),
    'some_not':evaluate_on_finite_domain('some_not',values),
    'only_one':evaluate_on_finite_domain('only_one',values),
    'at_least_two':evaluate_on_finite_domain('at_least_two',values),
    'at_most_two':evaluate_on_finite_domain('at_most_two',values),
    'exactly_two':evaluate_on_finite_domain('exactly_two',values)})
writejson(OUT/'finite_model_truth_tables.json',models)

# 31: social functions are normative descriptions of existing 7.0 discourse
# markers and source examples, not a novel unlicensed text-message syntax.
discourse=[]
for id,topic,rule,good,compare,caution in DISCOURSE_RULES:
 discourse.append({'id':id,'topic':topic,'rule':rule,'preferred_or_documented_example':good,
    'contrast_or_omission':compare,'scope_note':caution,'status':'normative usage clarification; no new inflection'})
writejson(OUT/'conversational_usage_rules.json',discourse)

# 32: exhaustive canonical compound analysis as a compressed CSV, preserving
# the official 13,379 compounds; glyph-boundary warnings are pronunciation
# analysis flags only and never propose a rewritten canonical spelling.
audit=[];risk=collections.Counter()
for r in compounds:
 m,h=r['modifier'],r['head']
 assert m in lex and h in lex,(m,h)
 assert r['compound'] in lex
 boundary=(m[-1]+h[0]).lower()
 crossing=boundary if boundary in {'sh','zh','kh','ng'} else ''
 gloss_ambiguous=(';' in r['modifier_english']) or (';' in r['head_english'])
 risk_code=('crossing_digraph' if crossing else 'none') + ('|multi_sense_gloss' if gloss_ambiguous else '')
 risk[risk_code]+=1
 audit.append({'dictionary_id':r['id'],'compound':r['compound'],'canonical_gloss':r['english'],
 'modifier':m,'modifier_gloss':r['modifier_english'],'head':h,'head_gloss':r['head_english'],
 'boundary':boundary,'grapheme_merge_risk':crossing,'component_polysemy_gloss_flag':gloss_ambiguous,
 'audit_status':'structural_compatible_not_semantically_reviewed','review_action':'verify lexicalized sense in context, retain spelling'})
import gzip
csvtext=[]
import io
buf=io.StringIO(newline='');d=csv.DictWriter(buf,fieldnames=list(audit[0]),lineterminator='\n');d.writeheader();d.writerows(audit)
with (OUT/'canonical_compound_audit_13379.csv.gz').open('wb') as f:f.write(gzip.compress(buf.getvalue().encode('utf-8'),compresslevel=9,mtime=0))
writejson(OUT/'word_formation_audit_summary.json',{'canonical_compound_count':len(audit),
    'status':'spelling preserved; boundary flags need lexical phonetic analysis',
    'risk_counts':dict(sorted(risk.items())),'sample_compounds_with_risk':[r for r in audit if r['grapheme_merge_risk'] or r['component_polysemy_gloss_flag']][:80],
    'new_headword_renames':0})

# 33: establish documented editorial-literary uses and conventional interaction
# frames. No corpus is turned into alleged indigenous folklore or evidence of
# independent idiom frequency.
assert len(figurative)==len(LITERARY_CONVENTIONS)==32
literary=[]
for r in figurative:
 cls,reading=LITERARY_CONVENTIONS[r['id']]
 literary.append({'id':r['id'],'qaroshi':r['qaroshi'],'literal_english':r['literal_english'],
  'accepted_editorial_literary_interpretation':r['figurative_meaning'],
  'interpretive_domain':cls,'restriction':reading,'context':r['context'],
  'status':'editorial literary convention in reference material, not independent oral attestation'})
writejson(OUT/'literary_conventions_32.json',literary)

# 34: fixed manifest with source evidence. The frozen canonical hashes are
# checked at runtime but are never replaced or silently recomputed.
prior=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())
sha_map=prior['sha256']
canonical_mismatches=[p for p,h in sha_map.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not canonical_mismatches,canonical_mismatches
outfiles=sorted(f for f in OUT.iterdir() if f.is_file() and f.name!='release_manifest.json')
manifest={'release':'Qaroshi 28–34 semantic and grammar standard extension','frozen_standard_7_0_unchanged':True,
 'historic_lexicon':30000,'adopted_lexical_overlay_additions':1,'effective_v28_34_lexical_inventory':30001,
 'historic_parallel_examples':4383,'historic_grammar_chapters':90,'resonance_markers':16,'native_graphemes':26,
 'top_lexical_index':len(rows),'new_editorial_meaning_boundaries':len(pairs),
 'verb_frame_inventory':len(frame_out),'manually_reviewed_verb_frames':len(frame_map),
 'source_exemplar_limited_verb_frames':len(exemplar_licenses),
 'provisional_corpus_observed_verb_frames':len(frame_out)-len(frame_map)-len(exemplar_licenses),
 'scope_examples':len(logic),'truth_table_rows':len(models),'conversational_rules':len(discourse),
 'canonical_compound_forms_checked':len(audit),'literary_conventions':len(literary),
 'frozen_source_hashes_verified':len(sha_map),'canonical_compound_renames':0,
 'lexical_review_policy':'lexicon-derived study entries and corpus-observed argument patterns are NOT individualized semantic or valency approval',
 'word_addition_provenance':'nëgëra is a newly authored normative constructed-language particle; not speaker attested',
 'generated_artifact_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in outfiles}}
writejson(OUT/'release_manifest.json',manifest)
print(json.dumps({k:v for k,v in manifest.items() if isinstance(v,(int,bool))},indent=2))
