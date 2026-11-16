"""Standard 8.1 stress-audit reproducibility and adopted complement-scope rules."""
import csv,hashlib,json,sys,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/stress81'))
from scenarios import create
from run_audit import run
from quantifier_composition import compose,PAIRS
from embedded_question import analyze

def csvrows(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

class ChallengeCoverage(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows=create();cls.report=run()
 def test_500_distinct_stimuli(self):
  self.assertEqual(len(self.rows),500)
  self.assertEqual(len({x['english'].casefold() for x in self.rows}),500)
  self.assertEqual(len({x['scenario_family'] for x in self.rows}),100)
 def test_ten_equal_domain_bands(self):
  self.assertEqual(set(Counter(x['domain'] for x in self.rows).values()),{50})
  self.assertEqual(len(set(x['domain'] for x in self.rows)),10)
 def test_separate_source_controls(self):
  self.assertEqual(self.report['positive_known_source_controls'],30)
  self.assertEqual(self.report['positive_controls_passed'],30)
 def test_translator_abstention_is_not_language_failure(self):
  self.assertEqual(self.report['translator_results'],{'abstained':500})
  self.assertFalse(self.report['automatically_verified_semantic_equivalence'])
  self.assertEqual(self.report['independent_human_comprehension_participants'],0)
 def test_49_limited_normative_drafts(self):
  self.assertEqual(self.report['editorial_rule_based_drafts'],49)
  self.assertEqual(self.report['remaining_without_documented_draft'],451)
  outcomes=csvrows('data/stress81/audit_results_500.csv')
  self.assertEqual(len(outcomes),500)
  for x in outcomes:
   with self.subTest(id=x['id']):
    self.assertEqual(x['human_checked_semantics'],'no')
    self.assertEqual(bool(x['normative_compositional_draft']),bool(compose(x)))
 def test_quantifier_drafts_do_not_conflate_none_and_not_all(self):
  outcomes=csvrows('data/stress81/audit_results_500.csv')
  examples=[x for x in outcomes if x['domain']=='quantifier_logic']
  for case in range(10):
   f=examples[case*5:(case+1)*5]
   self.assertIn('nëgëra',f[1]['normative_compositional_draft'])
   self.assertNotIn(' nu ',f[1]['normative_compositional_draft'])
   self.assertIn('ngënao',f[2]['normative_compositional_draft'])
   self.assertIn(' nu ',f[2]['normative_compositional_draft'])
 def test_repeated_audit_artifacts_byte_stable(self):
  names=['data/stress81/challenges_500.csv','data/stress81/audit_results_500.csv','data/stress81/audit_summary.json','data/stress81/positive_controls_30.csv']
  before=[hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names]
  run()
  after=[hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names]
  self.assertEqual(before,after)

class EmbeddedQuestionAmendment(unittest.TestCase):
 def test_that_vs_whether(self):
  x=analyze('sen sa haro do mi sëmi.')
  y=analyze('sen sa haro he do mi sëmi.')
  self.assertTrue(x['supported'] and y['supported'])
  self.assertEqual(x['complement_type'],'that');self.assertEqual(y['complement_type'],'whether')
  self.assertEqual(y['meaning_gloss'],'I know whether they are well.')
 def test_matrix_vs_embedded_negative(self):
  x=analyze('sen sa haro he do mi nu sëmi.')
  y=analyze('sen sa nu haro do mi sëmi.')
  self.assertTrue(x['matrix_negative'] and not x['embedded_negative'])
  self.assertTrue(y['embedded_negative'] and not y['matrix_negative'])
  self.assertEqual(x['meaning_gloss'],'I do not know whether they are well.')
  self.assertEqual(y['meaning_gloss'],'I know that they are not well.')
 def test_double_he_boundaries(self):
  x=analyze('hë sa haro he do mi sëmi he?')
  self.assertTrue(x['supported'])
  self.assertTrue(x['embedded_polar'] and x['matrix_polar'])
  self.assertEqual(x['meaning_gloss'],'Do I know whether they are well?')
 def test_know_whether_negative_proposition(self):
  x=analyze('sen sa nu haro he do mi sëmi.')
  self.assertTrue(x['supported']);self.assertEqual(x['complement_type'],'whether')
  self.assertTrue(x['embedded_negative']);self.assertFalse(x['matrix_negative'])
 def test_that_matrix_negative_not_false_proposition(self):
  x=analyze('sen sa haro do mi nu sëmi.')
  self.assertTrue(x['supported']);self.assertFalse(x['embedded_negative']);self.assertTrue(x['matrix_negative'])
  self.assertEqual(x['meaning_gloss'],'I do not know that they are well.')
 def test_second_person_matrix(self):
  x=analyze('sen sa haro he do ti nu sëmi.')
  self.assertTrue(x['supported']);self.assertEqual(x['meaning_gloss'],'you do not know whether they are well.'.capitalize())
 def test_out_of_scope_abstentions(self):
  bad=['sa haro he do mi sëmi.', 'sen sa haro he mi sëmi.',
       'sen sa haro he do mi sëmi he he?', 'sen sa haro he do mi sëmi do ti sëmi.',
       'sen hë sa haro he do mi sëmi.', 'sen sa haro he do mi nu nu sëmi.',
       'sen sa haro he do mi dara.', 'sen sa haro he do mi sëmi ëna.',
       'sen sa haro do do mi sëmi.', 'sen sa haro nu he do mi sëmi.']
  for sentence in bad:
   with self.subTest(sentence=sentence):self.assertFalse(analyze(sentence)['supported'])
 def test_narrow_predicate_whitelist(self):
  self.assertTrue(analyze('sen sa goro he do mi sëmi.')['supported'])
  self.assertFalse(analyze('sen sa ngaromo he do mi sëmi.')['supported'])

if __name__=='__main__':unittest.main()
