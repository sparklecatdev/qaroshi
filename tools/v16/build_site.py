#!/usr/bin/env python3
"""Build a fully offline semantic reference app with source-controlled metadata."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/v16'
def rows(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
lex=rows('data/v16/lexical_evidence_index_30000.csv')
senses=rows('data/v16/sense_editorial_5000.csv')
idioms=rows('data/v16/idiom_editorial_1000.csv')
contrasts=json.loads((ROOT/'data/semantics/minimal_contrasts.json').read_text(encoding='utf8'))
domain=rows('data/v16/domain_coverage_240.csv')
collisions=rows('data/v16/english_gloss_collisions.csv')
core=rows('data/v12_13/core_lexical_profiles.csv')
new=rows('data/v16/new_core_lexical_profiles.csv')
variants=rows('data/v16/editorial_translation_variants.csv')
metaphors=rows('data/v12_13/original_metaphors.csv')
tasks=rows('data/v16/coverage_writing_briefs_240.csv')
roots=rows('data/v16/productive_root_learning_ladder.csv')
learnability=json.loads((OUT/'root_learnability_manifest.json').read_text(encoding='utf8'))
def xprof(x,isnew=False):
 if isnew:return {'q':x['qaroshi'],'g':x['canonical_gloss_unmodified'],'def':x['editorial_definition_proposal'],'restriction':x['restriction_and_usage_boundary'],'contrast':x['contrast_or_false_friend'],'ipa':x['ipa'],'ex':x['example_qaroshi'],'en':x['example_english']}
 return {'q':x['qaroshi'],'g':x['canonical_gloss'],'def':x['editorial_sense_definition'],'restriction':x['grammatical_or_semantic_restriction'],'contrast':x['contrast_or_false_friend'],'ipa':x['ipa'],'ex':x['qaroshi_example'],'en':x['english_example_contextual']}
data={'manifest':json.loads((OUT/'semantic_atlas_manifest.json').read_text(encoding='utf8')),
 'lexicon':[{'q':x['qaroshi'],'id':x['id'],'g':x['canonical_gloss'],'dom':x['domain'],'pos':x['pos'],'typ':x['lexeme_type'],'ipa':x['ipa'],'comp':x['compound_parts'], 'o':int(x['original_editorial_occurrences']),'c':int(x['controlled_reference_occurrences']),'p':int(x['procedural_occurrences']),'rel':x['same_first_gloss_candidates'],'exq':x['editorial_example_qaroshi'],'exe':x['editorial_example_english'],'exsrc':x['editorial_example_source']} for x in lex],
 'senses':[{'id':x['sense_id'],'q':x['qaroshi'],'g':x['draft_selected_gloss'],'src':x['source_definition'],'pos':x['pos'],'dom':x['word_domain'],'risk':x['risk_notes'],'status':x['selected_gloss_provenance'],'priority':x['priority'],'o':int(x['original_editorial_occurrences']),'c':int(x['controlled_reference_occurrences']),'p':int(x['procedural_occurrences']),'ex':x['context_example_qaroshi'],'en':x['context_example_english'],'exkind':x['context_provenance']} for x in senses],
 'idioms':[{'id':x['candidate_id'],'family':x['family'],'q':x['expression'],'fig':x['suggested_figurative_meaning'],'literal':x['literal_english'],'anchor':x['anchor'],'familyN':int(x['family_pattern_size']),'exact':int(x['exact_editorial_occurrences']),'risk':x['risks']} for x in idioms],
 'coreProfiles':[xprof(x) for x in core],'newProfiles':[xprof(x,True) for x in new],
 'contrasts':contrasts,
 'metaphors':[{'id':x['id'],'title':x['title'],'q':x['qaroshi'],'literal':x['literal_translation'],'fig':x['proposed_figurative_meaning'],'context':x['usage_context'],'counter':x['counterexample_and_restriction']} for x in metaphors],
 'tasks':[{'id':x['brief_id'],'dom':x['domain'],'genre':x['genre_assignment'],'challenge':x['challenge'],'targets':x['lexical_targets']} for x in tasks],
 'domains':[{'dom':x['domain'],'n':int(x['canonical_entries']),'e':int(x['lexical_items_in_original_editorial']),'c':int(x['lexical_items_in_controlled_reference']),'comp':int(x['compound_entries'])} for x in domain],
 'roots':[{'rank':int(x['rank']),'q':x['root'],'english':x['english'],'ipa':x['ipa'],'pos':x['pos'],'domain':x['domain'],'uses':int(x['compounds_using_base_root']),'examples':x['first_6_compounds']} for x in roots],
 'learnability':{'curve':learnability['learning_curve'],'compound_entries':learnability['compound_entries'],'base_count':learnability['unique_ultimate_base_components'],'headwords':learnability['headword_labeled_entries'],'function_words':learnability['function_word_entries'],'nested':learnability['nested_compounds']},
 'collisions':[{'gloss':x['english_gloss'],'pos':x['pos'],'n':int(x['total_qr_forms']),'forms':x['example_forms']} for x in collisions],
 'variants':[{'q':x['qaroshi'],'english':x['english_variants'],'n':int(x['different_contextual_english'])} for x in variants]}
# A compact constant-time dictionary root membership map isn't needed in the app;
# use an explicit map of known spelling ids to avoid O(n) lookups in interactions.
data['rootIndex']={x['qaroshi']:1 for x in lex}
html=(ROOT/'web/v16/semantic_atlas_template.html').read_text(encoding='utf8')
script='const DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';'
html=html.replace('/* EMBEDDED DATA */',script)
out=ROOT/'Qaroshi_16_Semantic_Atlas.html';out.write_text(html,encoding='utf8')
print(out, len(html),'bytes; datasets:',{k:len(v) if hasattr(v,'__len__') else 0 for k,v in data.items() if k!='rootIndex'})
