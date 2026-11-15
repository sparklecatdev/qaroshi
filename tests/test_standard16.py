"""Qaroshi 16.0 semantic index and editorial-provenance regression tests."""
import unittest,csv,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];V=R/'data/v16'
def read(p):
 with (R/p).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
class Standard16Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.lex=read('data/lexicon.csv')
  cls.index=read('data/v16/lexical_evidence_index_30000.csv')
  cls.senses=read('data/v16/sense_editorial_5000.csv')
  cls.idioms=read('data/v16/idiom_editorial_1000.csv')
  cls.profiles=read('data/v16/new_core_lexical_profiles.csv')
  cls.man=json.loads((V/'semantic_atlas_manifest.json').read_text(encoding='utf8'))
 def test_original_size(self):self.assertEqual(len(self.lex),30000)
 def test_all_headword_ids_maintained(self):self.assertEqual({x['id'] for x in self.lex},{x['id'] for x in self.index})
 def test_all_original_forms_maintained(self):self.assertEqual({x['qaroshi'] for x in self.lex},{x['qaroshi'] for x in self.index})
 def test_no_duplicate_lemmas(self):self.assertEqual(len({x['qaroshi'] for x in self.lex}),30000)
 def test_same_canonical_gloss(self):
  src={x['qaroshi']:x for x in self.lex}
  self.assertTrue(all(x['canonical_gloss']==src[x['qaroshi']]['english'] for x in self.index))
 def test_source_compounds_verified(self):
  self.assertEqual(sum(x['lexeme_type']=='compound' for x in self.index),13379)
  self.assertTrue(all(x['parts_found_in_dictionary']=='yes' for x in self.index))
 def test_source_remains_unchanged(self):
  base=json.loads((R/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))['sha256']
  self.assertEqual(len(base),29)
  for name,digest in base.items():self.assertEqual(hashlib.sha256((R/name).read_bytes()).hexdigest(),digest)
 def test_original_editorial_coverage(self):self.assertEqual(sum(int(x['original_editorial_occurrences'])>0 for x in self.index),143)
 def test_controlled_reference_coverage(self):self.assertEqual(sum(int(x['controlled_reference_occurrences'])>0 for x in self.index),3752)
 def test_provenance_counts_match_release(self):
  self.assertEqual(sum(int(x['original_editorial_occurrences']) for x in self.index),6828)
  self.assertEqual(sum(int(x['procedural_occurrences']) for x in self.index),204538)
 def test_unmatched_senses(self):
  self.assertEqual(sum(not x['context_example_qaroshi'] for x in self.senses),4388)
 def test_sense_card_count(self):self.assertEqual(len(self.senses),5000)
 def test_senses_link_source(self):
  byid={x['id']:x for x in self.lex}
  self.assertTrue(all(x['headword_id'] in byid and byid[x['headword_id']]['qaroshi']==x['qaroshi'] for x in self.senses))
 def test_no_accepted_new_senses(self):self.assertTrue(all(x['new_sense_accepted']=='no' for x in self.senses))
 def test_no_synonymy_assumed(self):self.assertTrue(all(x['synonym_claim_approved']=='no' for x in self.senses))
 def test_no_approved_idioms(self):self.assertTrue(all(x['conventional_status']=='NOT established' for x in self.idioms))
 def test_idiom_count(self):self.assertEqual(len(self.idioms),1000)
 def test_no_attested_idiom_exact_occurrence(self):self.assertTrue(all(int(x['exact_editorial_occurrences'])==0 for x in self.idioms))
 def test_57_individually_explained_words(self):self.assertEqual(len(self.profiles),57)
 def test_61_prior_core_profiles_kept(self):self.assertEqual(len(read('data/v12_13/core_lexical_profiles.csv')),61)
 def test_new_profiles_each_have_boundary_and_contrast(self):
  for x in self.profiles:
   self.assertGreater(len(x['editorial_definition_proposal']),20)
   self.assertGreater(len(x['restriction_and_usage_boundary']),20)
   self.assertGreater(len(x['contrast_or_false_friend']),20)
 def test_each_new_profile_traceable(self):
  byid={x['id']:x for x in self.lex}
  for x in self.profiles:self.assertEqual(byid[x['source_headword_id']]['qaroshi'],x['qaroshi'])
 def test_new_examples_are_prior_evidence(self):
  ed={x['qaroshi'] for x in read('corpus/v15_completion/complete_corpus_rows.csv') if x['origin']=='original_editorial'}
  controlled={x['qaroshi'] for x in read('corpus/parallel_sentences.csv')}
  self.assertTrue(all(x['example_qaroshi'] in ed|controlled for x in self.profiles))
 def test_contrast_gallery_source_count(self):self.assertEqual(len(read('data/v16/semantic_contrast_gallery.csv')),195)
 def test_exact_grammar_contrasts_preserved(self):self.assertEqual(len(json.loads((R/'data/semantics/minimal_contrasts.json').read_text(encoding='utf8'))),94)
 def test_gloss_collisions_marked_unverified(self):
  c=read('data/v16/english_gloss_collisions.csv');self.assertEqual(len(c),26)
  self.assertTrue(all('NOT approved' in x['review_interpretation'] for x in c))
 def test_240_domains(self):self.assertEqual(len(read('data/v16/domain_coverage_240.csv')),240)
 def test_240_domain_briefs(self):self.assertEqual(len(read('data/v16/coverage_writing_briefs_240.csv')),240)
 def test_prompts_are_not_corpus(self):
  d=read('data/v16/coverage_writing_briefs_240.csv')
  self.assertTrue(all(x['source_type']=='writing assignment, not an authored corpus text' and x['accepted']=='no' for x in d))
 def test_original_semantic_variants_count(self):self.assertEqual(len(read('data/v16/editorial_translation_variants.csv')),223)
 def test_original_metadata_stats(self):
  self.assertEqual(self.man['lexicon_entries'],30000)
  self.assertEqual(self.man['independent_speaker_attestations'],0)
  self.assertEqual(self.man['accepted_new_idioms'],0)
 def test_offline_app_embeds_dictionary(self):
  s=(R/'Qaroshi_16_Semantic_Atlas.html').read_text(encoding='utf8')
  self.assertIn('"lexicon":[',s)
  self.assertIn('"senses":[',s)
  self.assertIn('"metaphors":[',s)
  self.assertIn('"tasks":[',s)
 def test_handbook_includes_review_disclaimer(self):
  txt=(R/'Qaroshi_16_Semantic_Handbook.md').read_text(encoding='utf8')
  self.assertIn('Editorial development reference',txt)
  self.assertIn('118',str(61+len(self.profiles)))
 def test_idiom_speaker_attestations_zero(self):
  self.assertTrue(all(x['independent_speaker_attestations']=='0' for x in self.idioms))
 def test_sense_review_priority_exists(self):
  self.assertEqual({x['priority'] for x in self.senses},{'P1','P2','P3'})
if __name__=='__main__':unittest.main()
