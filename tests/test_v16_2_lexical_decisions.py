"""16.2 noncanonical root-form trials, editorial provenance and source integrity."""
import unittest,csv,json,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data/v16_2'
def rows(name):
 with (D/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
LEX={x['qaroshi']:x for x in csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf8'))}
ALL=rows('all_3817_candidates_screened.csv');MAN=rows('individually_editorially_reviewed.csv')
ROOTS=rows('eight_root_decision_dossiers.csv');DER=rows('hypothetical_new_root_derivatives.csv');LEARN=rows('sixteen_grammar_and_learnability_examples.csv')
REUSE=rows('reuse_before_coinage.csv');SUMMARY=json.loads((D/'review_summary.json').read_text(encoding='utf8'))
class Standard16_2(unittest.TestCase):
 def test_00_preserves_29_baseline_sha256(self):
  m=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))
  self.assertEqual(len(m['sha256']),29)
  for file,hash_ in m['sha256'].items():
   with self.subTest(file=file):self.assertEqual(hashlib.sha256((ROOT/file).read_bytes()).hexdigest(),hash_)
 def test_01_lexicon_count(self):self.assertEqual(len(LEX),30000)
 def test_02_candidate_count(self):self.assertEqual(len(ALL),3817)
 def test_03_manual_count(self):self.assertEqual(len(MAN),65)
 def test_04_manual_trial_count(self):self.assertEqual(sum(x['status']=='manual_trial' for x in MAN),44)
 def test_05_manual_hold_count(self):self.assertEqual(sum(x['status']=='manual_hold' for x in MAN),9)
 def test_06_manual_reject_count(self):self.assertEqual(sum(x['status']=='manual_reject' for x in MAN),12)
 def test_07_root_count(self):self.assertEqual(len(ROOTS),8)
 def test_08_derivatives_count(self):self.assertEqual(len(DER),26)
 def test_09_lessons_count(self):self.assertEqual(len(LEARN),16)
 def test_10_reuse_count(self):self.assertEqual(len(REUSE),8)
 def test_11_not_approved(self):
  self.assertTrue(all(x['proposed_for_dictionary_acceptance']=='no' for x in ALL))
  self.assertTrue(all(x['new_roots_added_to_canonical_dictionary']==0 for x in [SUMMARY]))
 def test_12_existing_sources(self):self.assertTrue(all(x['canonical_word'] in LEX for x in ALL))
 def test_13_existing_components(self):self.assertTrue(all(x['modifier'] in LEX and x['head'] in LEX for x in ALL))
 def test_14_component_concat(self):self.assertTrue(all(x['candidate_form']==x['modifier']+x['head'] for x in ALL))
 def test_15_gloss_provenance(self):
  self.assertTrue(all(x['modifier_meaning']==LEX[x['modifier']]['english'] and x['head_meaning']==LEX[x['head']]['english'] for x in ALL))
 def test_16_no_magic_acceptance(self):self.assertTrue(all(not x['status'].startswith('accepted') for x in ALL))
 def test_17_manual_split_labels(self):self.assertEqual(len({(x['canonical_id'],x['candidate_form']) for x in MAN}),len(MAN))
 def test_18_unique_root_names(self):self.assertEqual(len({x['tentative_form'] for x in ROOTS}),8)
 def test_19_new_root_names_not_canonical(self):self.assertTrue(all(x['tentative_form'] not in LEX for x in ROOTS))
 def test_20_new_root_not_ratifed(self):self.assertTrue(all(x['canonical_entry_created']=='no' and x['decision']=='not_accepted' for x in ROOTS))
 def test_21_no_fabricated_speaker_attestation(self):self.assertTrue(all(x['independently_speaker_attested']=='no' for x in ALL))
 def test_22_shortlist_not_editorial(self):self.assertTrue(all(x['status']=='screened_shortlist_not_reviewed' for x in rows('machine_shortlist_unapproved.csv')))
 def test_23_narrow_derived_examples(self):
  forbidden=['time signature','digital signature','memory card','virtual card','musical note','voice note','graphics card']
  self.assertTrue(all(x['source_english'].casefold().strip() not in forbidden for x in DER))
 def test_24_html_contains_proposals_and_dictionary(self):
  h=(ROOT/'Qaroshi_16_2_Root_Standardization_Studio.html').read_text(encoding='utf8')
  self.assertIn('banuqamago',h);self.assertIn('NOT',h.upper());self.assertIn('exportReview',h)
 def test_25_resonance_safety(self):
  x=json.loads((ROOT/'data/resonances.json').read_text(encoding='utf8'))
  self.assertEqual(len(x),16)
 def test_26_native_glyphs(self):self.assertEqual(len(list((ROOT/'assets/glyphs').glob('*.png'))),26)
 def test_27_sense_keys(self):
  self.assertEqual(SUMMARY['manual_trial_count'],44);self.assertEqual(SUMMARY['manual_reject_count'],12)
 def test_28_lexicon_same_as_original(self):
  self.assertEqual(SUMMARY['canonical_lexicon_sha256'],hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest())
# Individual cases remain distinguishable in test output.
for x in MAN:
 def method(self,x=x):
  self.assertIn(x['status'],('manual_trial','manual_hold','manual_reject'))
  self.assertTrue(len(x['editorial_note'])>45)
  self.assertEqual(x['canonical_id'],LEX[x['canonical_word']]['id'])
  if x['status']=='manual_reject':self.assertNotIn(x,rows('machine_shortlist_unapproved.csv'))
 name='test_manual_'+x['canonical_id'].lower()+'_'+x['candidate_form']
 setattr(Standard16_2,name,method)
for i,x in enumerate(ROOTS):
 def method(self,x=x):
  self.assertNotIn(x['tentative_form'],LEX)
  self.assertTrue(x['narrow_proposed_sense'] and x['review_comment'])
  self.assertEqual(x['independent_attestation'],'none')
 setattr(Standard16_2,'test_root_dossier_'+str(i),method)
for i,x in enumerate(DER):
 def method(self,x=x):
  self.assertIn(x['source_headword'],LEX)
  self.assertEqual(x['draft_compositional_paraphrase'],x['draft_modifier']+x['new_root_proposal'])
  self.assertEqual(x['candidate_not_standard'],'true')
 setattr(Standard16_2,'test_derivative_example_'+str(i),method)
if __name__=='__main__':unittest.main()
