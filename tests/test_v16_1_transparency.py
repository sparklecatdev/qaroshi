"""16.1 lexical transparency: source preservation and exact-split verification."""
import unittest,csv,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
LEX=rows('data/lexicon.csv');WORDS={x['qaroshi']:x for x in LEX}
AUDIT=rows('data/v16_1/headword_learnability_audit_16525.csv')
CAND=rows('data/v16_1/strict_modifier_head_candidates.csv')
CORE=rows('data/v16_1/prioritized_core_1200.csv')
GAP=rows('data/v16_1/root_gap_priorities.csv')
R=json.loads((ROOT/'data/v16_1/audit_report.json').read_text(encoding='utf8'))

class TransparentLexicon(unittest.TestCase):
 def test_00_preserves_canonical_hash(self):
  self.assertEqual(hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest(),R['canonical_sha256'])
 def test_01_canonical_total(self):self.assertEqual(len(LEX),30000)
 def test_02_headword_count(self):self.assertEqual(len(AUDIT),16525)
 def test_03_no_duplicate_audit(self):self.assertEqual(len({x['qaroshi'] for x in AUDIT}),len(AUDIT))
 def test_04_no_duplicate_ids(self):self.assertEqual(len({x['id'] for x in AUDIT}),len(AUDIT))
 def test_05_headword_type(self):self.assertTrue(all(WORDS[x['qaroshi']]['type']=='headword' for x in AUDIT))
 def test_06_audit_ids(self):self.assertTrue(all(WORDS[x['qaroshi']]['id']==x['id'] for x in AUDIT))
 def test_07_audit_meaning_unchanged(self):self.assertTrue(all(WORDS[x['qaroshi']]['english']==x['english'] for x in AUDIT))
 def test_08_audit_pos_unchanged(self):self.assertTrue(all(WORDS[x['qaroshi']]['pos']==x['part_of_speech'] for x in AUDIT))
 def test_09_audit_includes_ipa(self):self.assertTrue(all(x['ipa'] for x in AUDIT))
 def test_10_status_enum(self):self.assertTrue(all(x['analysis_status'] in ('primary_gloss_candidate','secondary_sense_candidate','semantic_anchors_only','no_documented_derivation','preexisting_compoundlike_headword') for x in AUDIT))
 def test_11_status_count(self):self.assertEqual(sum(R['count_by_status'].values()),16525)
 def test_12_status_first(self):self.assertEqual(sum(x['analysis_status']=='primary_gloss_candidate' for x in AUDIT),2662)
 def test_13_status_secondary(self):self.assertEqual(sum(x['analysis_status']=='secondary_sense_candidate' for x in AUDIT),146)
 def test_14_other_status(self):self.assertEqual(sum(x['analysis_status']=='semantic_anchors_only' for x in AUDIT),7749)
 def test_15_opaque(self):self.assertEqual(sum(x['analysis_status']=='no_documented_derivation' for x in AUDIT),5966)
 def test_16_candidate_count(self):self.assertEqual(len(CAND),R['exact_split_proposal_rows'])
 def test_17_candidate_targets(self):self.assertEqual(len({x['target_id'] for x in CAND}),R['headwords_with_any_exact_split'])
 def test_18_proposal_canonical_source(self):self.assertTrue(all(WORDS[x['canonical_word']]['id']==x['target_id'] for x in CAND))
 def test_19_real_components(self):self.assertTrue(all(x['component_1'] in WORDS and x['component_2'] in WORDS for x in CAND))
 def test_20_modifier_pos(self):self.assertTrue(all(WORDS[x['component_1']]['pos'] in ('n','adj') for x in CAND))
 def test_21_head_pos(self):self.assertTrue(all(WORDS[x['component_2']]['pos']=='n' for x in CAND))
 def test_22_target_pos(self):self.assertTrue(all(WORDS[x['canonical_word']]['pos']=='n' for x in CAND))
 def test_23_concat(self):self.assertTrue(all(x['candidate_form']==x['component_1']+x['component_2'] for x in CAND))
 def test_24_length(self):self.assertTrue(all(len(x['candidate_form'])<=37 for x in CAND))
 def test_25_distinct(self):self.assertTrue(all(x['candidate_form']!=x['canonical_word'] for x in CAND))
 def test_26_no_wrong_collisions(self):
  for x in CAND:
   if x['candidate_form'] in WORDS:
    self.assertEqual(x['is_already_canonical'],'true')
   else:self.assertEqual(x['is_already_canonical'],'false')
 def test_27_all_pending(self):self.assertTrue(all(x['review_decision']=='pending' for x in AUDIT))
 def test_28_no_approved(self):self.assertTrue(all(x['review_decision']=='pending' for x in CAND))
 def test_29_canonical_not_renamed(self):self.assertEqual(R['original_canonical_words_renamed'],0)
 def test_30_no_new_approved(self):self.assertEqual(R['editorially_approved_new_spellings'],0)
 def test_31_study_count(self):self.assertEqual(len(CORE),1200)
 def test_32_study_first_rank(self):self.assertEqual([int(x['rank']) for x in CORE],list(range(1,1201)))
 def test_33_study_source_exists(self):self.assertTrue(all(x['qaroshi'] in WORDS for x in CORE))
 def test_34_study_source_type(self):self.assertTrue(all(WORDS[x['qaroshi']]['type']=='headword' for x in CORE))
 def test_35_missing_roots_present(self):self.assertGreater(len(GAP),2500)
 def test_36_gaps_uncoined(self):self.assertTrue(all(x['proposed_qaroshi_root']=='' for x in GAP))
 def test_37_unique_gaps(self):self.assertEqual(len(GAP),len({(x['role'],x['missing_english_concept']) for x in GAP}))
 def test_38_gap_order(self):self.assertEqual(sorted([int(x['priority_count']) for x in GAP],reverse=True),[int(x['priority_count']) for x in GAP])
 def test_39_draft_status(self):self.assertIn('paraphrases',R['qualifications'][1].lower())
 def test_40_wing_joint(self):
  x=next(x for x in AUDIT if x['qaroshi']=='banuaro')
  self.assertEqual(x['proposed_transparent_form'],'banuqamago')
 def test_41_fly_is_core(self):
  x=next(x for x in AUDIT if x['qaroshi']=='goro')
  self.assertEqual(x['analysis_status'],'no_documented_derivation')
 def test_42_no_unlicensed_wing_suffix(self):
  x=next(x for x in AUDIT if x['qaroshi']=='banuwa')
  self.assertFalse(x['proposed_transparent_form'])
 def test_43_html(self):self.assertIn('A split found in English dictionary glosses is a proposed Qaroshi expression',(ROOT/'Qaroshi_16_1_Root_Reform_Studio.html').read_text(encoding='utf8'))
 def test_44_html_data(self):self.assertIn('const DATA=',(ROOT/'Qaroshi_16_1_Root_Reform_Studio.html').read_text(encoding='utf8'))
 def test_45_root_guide_baseline(self):
  f=json.loads((ROOT/'data/v16/root_learnability_manifest.json').read_text(encoding='utf8'))
  self.assertEqual(f['unique_ultimate_base_components'],1820)
 def test_46_preserved_examples(self):self.assertEqual(len(rows('corpus/parallel_sentences.csv')),4383)
 def test_47_proposals_are_from_primary_or_secondary(self):
  for x in AUDIT:
   if x['proposed_transparent_form']:
    self.assertTrue(x['analysis_status'].endswith('_gloss_candidate') or x['analysis_status']=='secondary_sense_candidate')
 def test_48_ranks(self):
  priorities=rows('data/v16_1/headword_learning_priority_16525.csv')
  self.assertEqual(len(priorities),16525)
  self.assertEqual([int(x['rank']) for x in priorities[:100]],list(range(1,101)))

 def test_49_existing_headword_components(self):
  self.assertEqual(R['existing_headwords_matching_two_component_spellings'],2)
  x=next(x for x in AUDIT if x['qaroshi']=='qaroshishimarë')
  self.assertEqual(x['analysis_status'],'preexisting_compoundlike_headword')
  self.assertEqual(x['possible_existing_component_sequence'],'qaroshi + shimarë')

if __name__=='__main__':unittest.main()
