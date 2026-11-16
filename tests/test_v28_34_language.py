"""Conformance and honest-evidence checks for Qaroshi 28–34 language reform."""
from __future__ import annotations
import csv,gzip,hashlib,io,json,re,sys,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/v28_34'))
from phonetics import graphemes,ipa_word
from reform_core import validate_sentence,analyze_quantifier,evaluate_on_finite_domain,LEX,NEW

def read_csv(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

def read_json(path):return json.loads((ROOT/path).read_text(encoding='utf8'))

class Reform28To34Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.lex=read_csv('data/lexicon.csv')
  cls.lexmap={r['qaroshi']:r for r in cls.lex}
  cls.reference=read_csv('corpus/parallel_sentences.csv')
  cls.phrases=read_csv('data/v17/everyday_phrases.csv')
  cls.reference_map={r['id']:r for r in cls.reference+cls.phrases}
  cls.words=read_csv('data/v28_34/core_semantic_index_800.csv')
  cls.frames=read_csv('data/v28_34/verb_frame_inventory_400.csv')
  cls.contrasts=read_csv('data/v28_34/meaning_boundaries.csv')
  cls.logic=read_csv('data/v28_34/quantifier_scope_examples.csv')
  cls.truth=read_json('data/v28_34/finite_model_truth_tables.json')
  cls.conversation=read_json('data/v28_34/conversational_usage_rules.json')
  cls.literary=read_json('data/v28_34/literary_conventions_32.json')
  cls.new=read_json('data/v28_34/adopted_function_words.json')
  cls.m=read_json('data/v28_34/release_manifest.json')
  cls.formation=read_json('data/v28_34/word_formation_audit_summary.json')
  cls.doc=(ROOT/'docs/language_reform_28_34.md').read_text(encoding='utf8')

 def test_01_canonical_count(self):self.assertEqual(len(self.lex),30000)
 def test_02_unique_lexeme_ids(self):self.assertEqual(len({x['id'] for x in self.lex}),30000)
 def test_03_unique_lexeme_spellings(self):self.assertEqual(len(self.lexmap),30000)
 def test_04_canonical_reference_count(self):self.assertEqual(len(self.reference),4383)
 def test_05_legacy_phrase_count(self):self.assertEqual(len(self.phrases),656)
 def test_06_grammar_chapter_count(self):
  s=(ROOT/'docs/grammar.md').read_text(encoding='utf8');self.assertEqual([int(x) for x in re.findall(r'^## (\d+)\.',s,re.M)],list(range(1,91)))
 def test_07_resonance_count(self):self.assertEqual(len(read_json('data/resonances.json')),16)
 def test_08_native_graphemes(self):self.assertEqual(len(read_json('data/phoneme_inventory.json')),26)
 def test_09_frozen_base_hashes(self):
  legacy=read_json('data/v14/baseline_sha256.json')['sha256'];self.assertEqual(len(legacy),29)
  for p,expected in legacy.items():
   with self.subTest(p=p):self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),expected)
 def test_10_one_unique_new_lexeme(self):
  self.assertEqual(len(self.new),1);self.assertEqual(self.new[0]['lemma'],NEW);self.assertNotIn(NEW,self.lexmap)
 def test_11_new_word_spelling(self):
  self.assertEqual(graphemes(NEW),['n','ë','g','ë','r','a']);self.assertEqual(ipa_word(NEW),self.new[0]['ipa'])
 def test_12_new_word_pos(self):self.assertEqual(self.new[0]['pos'],'det')
 def test_13_new_word_scope(self):self.assertEqual(self.new[0]['logical_form'],'∃x∈D ¬P(x)')
 def test_14_narrow_new_word_parser(self):
  r=validate_sentence('sen nëgëra qaro goro.');self.assertTrue(r['valid_surface'],r['findings'])
  self.assertEqual(r['scope_analysis']['logical_form'],'∃x∈D ¬P(x)')
 def test_15_adjective_predicate_scope(self):
  r=validate_sentence('sen nëgëra qaro haro.');self.assertTrue(r['valid_surface'],r['findings'])
 def test_16_every_positive(self):
  self.assertEqual(analyze_quantifier('sen ngënao qaro goro.')['logical_form'],'∀x∈D P(x)')
 def test_17_every_negative(self):
  self.assertEqual(analyze_quantifier('sen ngënao qaro nu goro.')['logical_form'],'∀x∈D ¬P(x)')
 def test_18_some_positive(self):
  self.assertEqual(analyze_quantifier('sen shërano qaro goro.')['logical_form'],'∃x∈D P(x)')
 def test_19_some_negative(self):
  self.assertEqual(analyze_quantifier('sen shërano qaro nu goro.')['logical_form'],'∃x∈D ¬P(x)')
 def test_20_duplicate_new_determiner_rejected(self):
  r=validate_sentence('sen nëgëra nëgëra qaro goro.');self.assertFalse(r['valid_surface'])
 def test_21_misplaced_determiner_rejected(self):
  r=validate_sentence('sen qaro nëgëra goro.');self.assertFalse(r['valid_surface'])
 def test_22_pure_new_word_double_negative_rejected(self):
  r=validate_sentence('sen nëgëra qaro nu goro.');self.assertFalse(r['valid_surface'])
 def test_23_new_determiner_unlicensed_missing_resonance(self):
  r=validate_sentence('nëgëra qaro goro.');self.assertFalse(r['valid_surface'])
 def test_24_not_all_true_when_none_true(self):
  self.assertTrue(evaluate_on_finite_domain('not_every',[False,False,False]))
  self.assertTrue(evaluate_on_finite_domain('none',[False,False,False]))
 def test_25_not_all_false_when_every_true(self):
  self.assertFalse(evaluate_on_finite_domain('not_every',[True,True,True]))
 def test_26_not_all_does_not_entail_some(self):
  val=[False,False,False];self.assertTrue(evaluate_on_finite_domain('not_every',val));self.assertFalse(evaluate_on_finite_domain('some',val))
 def test_27_some_does_not_entail_not_all(self):
  val=[True,True,True];self.assertTrue(evaluate_on_finite_domain('some',val));self.assertFalse(evaluate_on_finite_domain('not_every',val))
 def test_28_empty_domain_premise(self):self.assertFalse(evaluate_on_finite_domain('not_every',[]))
 def test_29_exact_count_boundaries(self):
  for val in ([False,False],[True,False],[True,True],[True,True,True]):
   self.assertEqual(evaluate_on_finite_domain('exactly_two',val),sum(val)==2)
 def test_30_all_models_consistent(self):
  self.assertEqual(len(self.truth),15)
  for r in self.truth:
   yes,n=int(r['predicate_true_members']),int(r['domain_size']);val=[True]*yes+[False]*(n-yes)
   for form in ['every','none','not_every','some','some_not','only_one','at_least_two','at_most_two','exactly_two']:
    with self.subTest(n=n,yes=yes,form=form):self.assertEqual(r[form],evaluate_on_finite_domain(form,val))
 def test_31_core_index_size(self):self.assertEqual(len(self.words),800)
 def test_32_core_index_lex_id(self):
  for r in self.words:
   self.assertEqual(r['dictionary_id'],self.lexmap[r['lemma']]['id'])
 def test_33_core_index_no_fake_attestation(self):
  self.assertTrue(all(r['speaker_attestation']=='none asserted' for r in self.words))
 def test_34_core_index_source_refs(self):
  for r in self.words:
   for rid in r['source_reference_ids'].split(' | '):
    if rid:self.assertIn(rid,self.reference_map)
 def test_35_meaning_boundary_count(self):self.assertEqual(len(self.contrasts),30)
 def test_36_meaning_boundary_sources(self):
  for r in self.contrasts:
   self.assertTrue(r['left'] in self.lexmap or r['left']==NEW)
   self.assertTrue(r['right'] in self.lexmap or r['right']==NEW)
 def test_37_no_gloss_overlap_approval(self):
  self.assertTrue(all('not a claim' in r['status'] for r in self.contrasts))
 def test_38_frame_total(self):self.assertEqual(len(self.frames),400)
 def test_39_frame_review_counts(self):
  self.assertEqual(Counter(r['review_status'] for r in self.frames),{
    'normative_manual_frame_24_27':25,'source_exemplar_limited_license':108,'corpus_observed_provisional_roles':267})
 def test_40_no_machine_normative_roles(self):
  for r in self.frames:
   if r['review_status']=='corpus_observed_provisional_roles':
    self.assertEqual(r['reviewed_required_roles'],'not individually assigned')
    self.assertEqual(r['passive_actor_case'],'not adjudicated')
 def test_41_frame_lexical_ids(self):
  for r in self.frames:
   self.assertEqual(r['dictionary_id'],self.lexmap[r['lemma']]['id'])
 def test_42_frame_sources(self):
  for r in self.frames:
   for rid in r['example_ids'].split(' | '):
    if rid:self.assertIn(rid,self.reference_map)
 def test_43_manually_reviewed_frames_unchanged(self):
  f=read_json('data/semantics/valency_frames.json')
  self.assertEqual([x['lemma'] for x in self.frames[:25]],[x['lemma'] for x in f])
 def test_44_transfer_roles(self):
  f=next(x for x in self.frames if x['lemma']=='pëli');self.assertIn('recipient:-tu',f['reviewed_required_roles']);self.assertIn('object:-m',f['reviewed_required_roles'])
 def test_45_compound_audit(self):
  with gzip.open(ROOT/'data/v28_34/canonical_compound_audit_13379.csv.gz','rt',encoding='utf-8') as f:a=list(csv.DictReader(f))
  self.assertEqual(len(a),13379);self.assertEqual({x['compound'] for x in a},{x['compound'] for x in read_csv('data/v16/compound_decomposition_13379.csv')})
 def test_46_compound_flags(self):
  self.assertEqual(sum(self.formation['risk_counts'].values()),13379)
  self.assertEqual(self.formation['new_headword_renames'],0)
 def test_47_compound_no_silent_approval(self):
  with gzip.open(ROOT/'data/v28_34/canonical_compound_audit_13379.csv.gz','rt',encoding='utf8') as f:
   self.assertTrue(all(x['audit_status']=='structural_compatible_not_semantically_reviewed' for x in csv.DictReader(f)))
 def test_48_literary_count(self):self.assertEqual(len(self.literary),32)
 def test_49_literary_unchanged_literal_forms(self):
  old=read_json('data/semantics/figurative_expressions.json');new={x['id']:x for x in self.literary}
  for x in old:
   self.assertEqual(x['qaroshi'],new[x['id']]['qaroshi'])
   self.assertEqual(x['figurative_meaning'],new[x['id']]['accepted_editorial_literary_interpretation'])
 def test_50_discourse_rules(self):self.assertEqual(len(self.conversation),20)
 def test_51_discourse_still_resonance(self):
  self.assertIn('exactly one initial resonance',self.conversation[0]['rule'])
 def test_52_discourse_distinguishes_consent(self):
  self.assertTrue(any('consent' in str(r).lower() for r in self.conversation))
 def test_53_structural_release_versions(self):
  for n in range(28,35):self.assertRegex(self.doc,rf'## {n} ·')
 def test_54_scope_table_in_doc(self):
  for x in ['nëgëra','∀x∈D','∃x∈D','does **not**','shoru']:
   self.assertIn(x,self.doc)
 def test_55_existing_passive_case_preserved(self):
  from fluency11.engine import CASES
  self.assertEqual(CASES['za'],'passive_agent')
 def test_56_archive_word_review_not_repromoted(self):
  old=read_csv('data/semantics/lexical_migration_decisions_24_27.csv')
  self.assertEqual(len(old),65);self.assertTrue(all(r['canonical_replacement']=='no' for r in old))
 def test_57_reproducible_artifact_hashes(self):
  for relative,digest in self.m['generated_artifact_sha256'].items():
   self.assertEqual(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(),digest)
 def test_58_invariants_manifest(self):
  for k,v in [('historic_lexicon',30000),('effective_v28_34_lexical_inventory',30001),('verb_frame_inventory',400),('top_lexical_index',800),('canonical_compound_forms_checked',13379),('literary_conventions',32),('frozen_source_hashes_verified',29)]:
   self.assertEqual(self.m[k],v)
 def test_61_limited_manual_examples_are_source_grounded(self):
  matched=[x for x in self.frames if x['review_status']=='source_exemplar_limited_license']
  self.assertEqual(len(matched),108)
  for x in matched:
   with self.subTest(word=x['lemma']):
    source=self.reference_map[x['licensed_exemplar_id']]
    self.assertEqual(x['licensed_exemplar_qaroshi'],source['qaroshi'])
    self.assertIn(x['licensed_object_root']+'-m',source['qaroshi'])
    self.assertIn('source-licensed target',x['reviewed_required_roles'])
 def test_62_no_automated_voice_approval(self):
  for x in self.frames:
   if x['review_status']!='normative_manual_frame_24_27':
    self.assertEqual(x['passive_actor_case'],'not adjudicated')
 def test_63_manifest_source_exemplars(self):
  self.assertEqual(self.m['source_exemplar_limited_verb_frames'],108)
  self.assertEqual(self.m['provisional_corpus_observed_verb_frames'],267)
 def test_64_logic_examples_validated_against_active_rules(self):
  for item in self.logic:
   with self.subTest(example=item['id']):self.assertTrue(validate_sentence(item['qaroshi'])['valid_surface'])
 def test_65_literary_not_independently_attested(self):
  self.assertTrue(all('not independent oral attestation' in x['status'] for x in self.literary))
 def test_59_new_data_cannot_claim_native_speakers(self):
  self.assertIn('not speaker attested',self.m['word_addition_provenance'])
 def test_60_legacy_grammar_not_replaced(self):
  self.assertIn('historical',self.doc)

if __name__=='__main__':unittest.main()
