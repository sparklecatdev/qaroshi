#!/usr/bin/env python3
"""Qaroshi 16: reproducible semantic evidence index and editorial triage.

This tool *never* accepts, coins or ratifies a sense, idiom, synonym or dialect.
It combines dictionary gloss matching and known *editorial* corpus counts.
"""
from __future__ import annotations
from pathlib import Path
import csv,json,re,collections,hashlib,sys,unicodedata
R=Path(__file__).resolve().parents[2]; OUT=R/'data/v16';OUT.mkdir(exist_ok=True,parents=True)
TOK=re.compile(r'[a-zë]+(?:-[a-zë]+)*',re.I)

def read(path):
 with (R/path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def write(filename,rows,fields=None):
 rows=list(rows)
 if fields is None:fields=list(rows[0]) if rows else []
 with (OUT/filename).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def phrase_normal(text):return unicodedata.normalize('NFC',text).lower().strip()
def first_gloss(s):return re.split(r';\s*',s)[0].strip()
def main():
 lex=read('data/lexicon.csv'); idx={x['qaroshi']:x for x in lex}; ids={x['id']:x for x in lex}
 core=read('data/v12_13/core_lexical_profiles.csv'); coremap={x['qaroshi']:x for x in core}
 frames=json.loads((R/'data/semantics/valency_frames.json').read_text(encoding='utf8'));framemap={x['lemma']:x for x in frames}
 cur_senses=json.loads((R/'data/semantics/curated_senses.json').read_text(encoding='utf8'))
 curmap=collections.defaultdict(list)
 for x in cur_senses:curmap[x['lemma']].append(x)
 original=collections.Counter();generated=collections.Counter();reference=collections.Counter()
 examples={k:collections.defaultdict(list) for k in ('original','reference')}
 original_sentences=collections.defaultdict(list)
 original_strings=set();generated_strings=set()
 original_rows=[]
 for row in read('corpus/v15_completion/complete_corpus_rows.csv'):
  sent=phrase_normal(row['qaroshi']);kind='original' if row['origin']=='original_editorial' else 'generated'
  if kind=='original':original_strings.add(sent);original_rows.append(row);original_sentences[sent].append(row)
  else:generated_strings.add(sent)
  seen=set()
  for token in TOK.findall(sent):
   root=token.split('-')[0]
   if root not in idx:continue
   (original if kind=='original' else generated)[root]+=1
   if kind=='original' and root not in seen and len(examples['original'][root])<3:
    examples['original'][root].append((row['qaroshi'],row['english_contextual'],row['piece_id']))
   seen.add(root)
 for row in read('corpus/parallel_sentences.csv'):
  sent=phrase_normal(row['qaroshi']);seen=set()
  for token in TOK.findall(sent):
   root=token.split('-')[0]
   if root not in idx:continue
   reference[root]+=1
   if root not in seen and len(examples['reference'][root])<2:
    examples['reference'][root].append((row['qaroshi'],row['english'],row['id']))
   seen.add(root)
 # Exact source gloss match is evidence for editorial comparison, not synonymy.
 group=collections.defaultdict(list)
 for x in lex:group[(x['pos'],phrase_normal(first_gloss(x['english'])))].append(x)
 relationships=[]
 for x in lex:
  id_,q=x['id'],x['qaroshi'];grp=group[(x['pos'],phrase_normal(first_gloss(x['english'])))]
  neighbors=[v for v in grp if v['qaroshi']!=q]
  neighbors.sort(key=lambda v:(v['type']=='compound',v['domain']!=x['domain'],v['qaroshi']))
  lex_parts=[y.strip() for y in x['components'].split('+') if y.strip()];missing=[v for v in lex_parts if v not in idx]
  head=lex_parts[-1] if len(lex_parts)==2 else ''
  e=examples['original'][q] or examples['reference'][q]
  relationships.append({'id':id_,'qaroshi':q,'ipa':x['ipa'],'sound_out':x['sound_out'],'pos':x['pos'],'canonical_gloss':x['english'],'first_gloss':first_gloss(x['english']),
   'domain':x['domain'],'lexeme_type':x['type'],'compound_parts':x['components'],'compound_head':head,
   'parts_found_in_dictionary':'yes' if not missing else 'no','missing_component':'; '.join(missing),
   'source_gloss_segments':len([a for a in x['english'].split(';') if a.strip()]),
   'original_editorial_occurrences':original[q], 'controlled_reference_occurrences':reference[q], 'procedural_occurrences':generated[q],
   'editorial_example_qaroshi':e[0][0] if e else '','editorial_example_english':e[0][1] if e else '',
   'editorial_example_source':e[0][2] if e else '',
   'same_first_gloss_candidate_count':len(neighbors),
   'same_first_gloss_candidates':'; '.join(n['qaroshi'] for n in neighbors[:5]),
   'curated_profile_id':coremap[q]['id'] if q in coremap else '',
   'curated_valency_frame':framemap[q]['frame'] if q in framemap else '',
   'earlier_curated_senses':'; '.join(s['id']+': '+s['sense'] for s in curmap[q]),
   'acceptance':'existing canonical headword; relationships and additional senses are NOT independently validated'})
 write('lexical_evidence_index_30000.csv',relationships)
 # Distinguish English homonym collisions from proven Qaroshi synonyms.
 collisions=[]
 for (pos,gloss),values in sorted(group.items()):
  if len(values)>1:
   for chunk in [values[i:i+20] for i in range(0,len(values),20)]:
    collisions.append({'english_gloss':gloss,'pos':pos,'total_qr_forms':len(values),
       'example_forms':'; '.join(x['qaroshi'] for x in chunk),
       'headwords_in_group':sum(x['type']=='headword' for x in values),
       'review_interpretation':'English gloss collision / candidate lexical comparison; NOT approved Qaroshi synonyms'})
 write('english_gloss_collisions.csv',collisions)
 # Prior 5,000 draft 'senses' are one selected gloss per dictionary headword;
 # do not promote a semicolon-delimited gloss into new independent sense.
 prev={x['sense_id']:x for x in read('data/v14/sense_review_5000.csv')}
 senses=[]
 for x in read('data/editorial/sense_cards_5000.csv'):
  q=x['qaroshi'];h=idx.get(q);prevrow=prev.get(x['sense_id'],{})
  # No extra inference for lone entries. Existing canonical gloss is the only source asserted.
  semicolon=len([a for a in (h or {}).get('english','').split(';') if a.strip()])
  profile=coremap.get(q)
  ori=examples['original'][q];ref=examples['reference'][q]
  flags=[]
  if not h or h['id']!=x['headword_id']:flags.append('headword or ID mismatch')
  if h and x['part_of_speech']!=h['pos']:flags.append('part-of-speech mismatch')
  if h and x['gloss'].casefold() not in h['english'].casefold():flags.append('selected gloss not found verbatim in reference gloss')
  if 'generic' in prevrow.get('earlier_risk','').lower():flags.append('generic example may lack semantic selection')
  if len(ori)==0:flags.append('no separately drafted editorial example in current corpus')
  if len(ref)==0:flags.append('no reference bilingual example in controlled reference')
  if semicolon>1:flags.append('multiple English gloss segments do not establish polysemy')
  f=framemap.get(q)
  if f and x['part_of_speech']=='v':flags.append('check example against curated verb argument frame')
  if h and h['type']=='compound':flags.append('compound interpretation depends on modifier-head context')
  grade='P0' if (not h or 'mismatch' in ' '.join(flags)) else 'P1' if prevrow.get('priority')=='high' and not ori else 'P2' if prevrow.get('priority')=='high' or not ori else 'P3'
  candidate=group.get(((h or {}).get('pos',''),phrase_normal(first_gloss((h or {}).get('english','')))),[])
  rel=[v['qaroshi'] for v in candidate if v['qaroshi']!=q][:4]
  senses.append({'sense_id':x['sense_id'],'headword_id':x['headword_id'],'qaroshi':q,'pos':x['part_of_speech'],'source_definition':h['english'] if h else '',
   'draft_selected_gloss':x['gloss'],'word_domain':x['domain'],'selected_gloss_provenance':'selected substring of canonical dictionary gloss; NOT independent polysemy evidence',
   'canonical_gloss_segments':semicolon,'example_qaroshi_unreviewed':x['candidate_example'],
   'example_english_unreviewed':x['candidate_example_en'],'original_editorial_occurrences':original[q],
   'controlled_reference_occurrences':reference[q], 'procedural_occurrences':generated[q],
   'context_example_qaroshi':ori[0][0] if ori else ref[0][0] if ref else '',
   'context_example_english':ori[0][1] if ori else ref[0][1] if ref else '',
   'context_source':ori[0][2] if ori else ref[0][2] if ref else '',
   'context_provenance':'separately drafted editorial; not speaker-attested' if ori else 'controlled bilingual reference; not speaker-attested' if ref else 'none',
   'same_english_gloss_comparison_candidates':'; '.join(rel),'comparison_warning':'English gloss collision not verified synonymy' if rel else '',
   'curated_profile_id':profile['id'] if profile else '',
   'known_valency_frame':f['frame'] if f else '',
   'known_valency_note':f['selection_note'] if f else '',
   'priority':grade,'risk_notes':'; '.join(flags+[prevrow.get('earlier_risk','')] if prevrow.get('earlier_risk') else flags),
   'definition_decision':'unreviewed','context_decision':'unreviewed',
   'new_sense_accepted':'no', 'synonym_claim_approved':'no','reviewer':'','rationale':'','revised_example':'','revised_gloss':''})
 write('sense_editorial_5000.csv',senses)
 # Idiom exact matches in unrelated prose are not evidence of conventionalization.
 idioms=[];families=collections.Counter(x['family'] for x in read('data/editorial/idiom_candidates_1000.csv'))
 lit_original='\n'.join(row['qaroshi'] for row in original_rows).casefold()
 authored_metaphors=read('data/v12_13/original_metaphors.csv')
 for x in read('data/editorial/idiom_candidates_1000.csv'):
  expr=phrase_normal(x['qaroshi_expression']);parts=expr.split()
  exact=sum(row['qaroshi'].lower().find(expr)>=0 for row in original_rows)
  risk=[]
  if exact==0:risk.append('no exact phrase occurrence in separately drafted editorial prose')
  if families[x['family']]>=10:risk.append('pattern-derived family: not independently conventionalized')
  if x['anchor_qaroshi'] in idx and idx[x['anchor_qaroshi']]['pos'] in ('n','adj'):risk.append('figurative reading is a proposal, not evidenced conventional sense')
  idioms.append({'candidate_id':x['id'],'family':x['family'],'expression':x['qaroshi_expression'],'literal_english':x['literal_english'],
  'suggested_figurative_meaning':x['suggested_figurative_meaning'],'usage_condition_draft':x['usage_condition'],
  'anchor':x['anchor_qaroshi'],'anchor_existing_gloss':idx.get(x['anchor_qaroshi'],{}).get('english',''),
  'family_pattern_size':families[x['family']],'exact_editorial_occurrences':exact,
  'independent_speaker_attestations':0,'lexical_review':'unreviewed','cultural_review':'unreviewed',
  'conventional_status':'NOT established','risks':'; '.join(risk),'reviewer':'','meaning_decision':'','evidence_url':'','replacement_proposal':'','note':''})
 write('idiom_editorial_1000.csv',idioms)
 # Contrast gallery carries already authored content without conflating with attestation.
 contrast=[]
 for x in core:
  if x['qaroshi'] not in idx:continue
  contrast.append({'reference_id':x['id'],'type':'lexical semantic profile','qaroshi':x['qaroshi'],'ipa':x['ipa'],
   'canonical_gloss':x['canonical_gloss'],'definition':x['editorial_sense_definition'],
   'restriction':x['grammatical_or_semantic_restriction'],'contrast':x['contrast_or_false_friend'],
   'example':x['qaroshi_example'],'english':x['english_example_contextual'],
   'source_status':'individually written editorial profile; not independently approved'})
 for x in json.loads((R/'data/semantics/minimal_contrasts.json').read_text(encoding='utf8')):
  contrast.append({'reference_id':x['id'],'type':'grammar minimal pair','qaroshi':x['choices'][0]['qaroshi']+' | '+x['choices'][1]['qaroshi'],
   'ipa':x['choices'][0].get('ipa',''), 'canonical_gloss':x['skill'],
   'definition':x['explanation'],'restriction':'Difference between two tested grammatical constructions, not a lexical synonym/antonym claim',
   'contrast':x['choices'][0]['english']+' / '+x['choices'][1]['english'],
   'example':x['choices'][0]['qaroshi'],'english':x['choices'][0]['english'],
   'source_status':'reference-grounded controlled contrast; not independent speaker evidence'})
 for x in authored_metaphors:
  contrast.append({'reference_id':x['id'],'type':'original metaphor candidate','qaroshi':x['qaroshi'],'ipa':x['ipa'],
   'canonical_gloss':x['literal_translation'],'definition':x['proposed_figurative_meaning'],
   'restriction':x['counterexample_and_restriction'],'contrast':'Proposed figurative use; no idiomatic conventionality proven',
   'example':x['qaroshi'],'english':x['literal_translation'],
   'source_status':'individually written editorial proposal; no speaker attestation'})
 write('semantic_contrast_gallery.csv',contrast)
 # Inspect curated value conflicts only; repeated sentences across procedural data
 # are not evidence of independent semantic alternatives.
 diverge=collections.defaultdict(lambda:collections.defaultdict(list))
 for row in original_rows:
  diverge[phrase_normal(row['qaroshi'])][row['english_contextual']].append(row['piece_id'])
 ambiguous=[]
 for q,vs in diverge.items():
  if len(vs)<2:continue
  ambiguous.append({'qaroshi':q,'different_contextual_english':len(vs),'english_variants':' | '.join(list(vs)[:6]),
    'documented_piece_examples':' | '.join(f"{en}: {','.join(pieces[:2])}" for en,pieces in list(vs.items())[:3]),
    'classification':'possible contextual paraphrase, anaphora or error; NOT automatically a contradiction',
    'reviewer':'','decision':'','preferred_english':'','contextual_explanation':''})
 ambiguous.sort(key=lambda r:(-int(r['different_contextual_english']),r['qaroshi']))
 write('editorial_translation_variants.csv',ambiguous)
 domain=collections.Counter(x['domain'] for x in lex)
 by_domain=[]
 for dom,n in domain.most_common():
  k=[r for r in relationships if r['domain']==dom];by_domain.append({'domain':dom,'canonical_entries':n,
  'lexical_items_in_original_editorial':sum(int(r['original_editorial_occurrences'])>0 for r in k),
  'lexical_items_in_controlled_reference':sum(int(r['controlled_reference_occurrences'])>0 for r in k),
  'lexical_items_only_procedural':sum(int(r['procedural_occurrences'])>0 and not int(r['original_editorial_occurrences']) for r in k),
  'compound_entries':sum(r['lexeme_type']=='compound' for r in k),
  'contributor_work':'Prioritize domain examples and argument frames; frequency does not certify semantic naturalness'})
 write('domain_coverage_240.csv',by_domain)
 base=json.loads((R/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))['sha256'];changed=[]
 for file,digest in base.items():
  if not (R/file).is_file() or hashlib.sha256((R/file).read_bytes()).hexdigest()!=digest:changed.append(file)
 if changed:raise RuntimeError('Canonical source mutated: '+', '.join(changed))
 report={'project':'Qaroshi 16.0 semantic dictionary / quality atlas','lexicon_entries':len(lex),
 'canonical_headword_entries':sum(r['type']=='headword' for r in lex),'canonical_compound_entries':sum(r['type']=='compound' for r in lex),
 'domains':len(domain),'sense_draft_cards':len(senses),'idiom_draft_candidates':len(idioms),
 'semantic_contrast_cards_reused':len(contrast),'individually_curated_core_word_cards':len(core),
 'source_gloss_collision_group_rows':len(collisions),'gloss_collision_groups':sum(len(v)>1 for v in group.values()),
 'source_composition_mismatches':sum(r['parts_found_in_dictionary']=='no' for r in relationships),
 'lexemes_with_original_editorial_occurrence':sum(bool(original[r['qaroshi']]) for r in lex),
 'lexemes_with_controlled_reference_occurrence':sum(bool(reference[r['qaroshi']]) for r in lex),
 'lexemes_with_procedural_occurrence':sum(bool(generated[r['qaroshi']]) for r in lex),
 'original_editorial_tokens':sum(original.values()),'procedural_source_tokens_excluding_unknown':sum(generated.values()),
 'original_editorial_translation_variation_groups':len(ambiguous),
 'accepted_new_senses':0,'accepted_new_idioms':0,'independent_speaker_attestations':0,
 'preserved_sha256_canonical_files':len(base),
 'method':'Token counts are only recognized lexemes. Gloss matching is a candidate relation; neither editorial corpus frequency nor generated material proves synonymy, an idiom, or a new sense.'}
 (OUT/'semantic_atlas_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
