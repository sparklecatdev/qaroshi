"""Regression tests for documented Qaroshi word transparency, not language usage endorsement."""
import csv,json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/'data/v16'
def load(name):
 with (D/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
class RootGuideTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.comp=load('compound_decomposition_13379.csv')
  cls.roots=load('productive_root_learning_ladder.csv')
  cls.info=json.loads((D/'root_learnability_manifest.json').read_text(encoding='utf8'))
  with (R/'data/lexicon.csv').open(encoding='utf8',newline='') as f:cls.lex={x['qaroshi']:x for x in csv.DictReader(f)}
 def test_exact_inventory(self):
  self.assertEqual(len(self.comp),13379)
  self.assertEqual(len(self.roots),1820)
  self.assertEqual(self.info['headword_labeled_entries'],16525)
 def test_parts_reconstruct_canonical_spelling(self):
  for x in self.comp:
   self.assertEqual(x['modifier']+x['head'],x['compound'])
   self.assertIn(x['modifier'],self.lex)
   self.assertIn(x['head'],self.lex)
 def test_max_learning_threshold(self):
  self.assertEqual(self.info['learning_curve'][-1]['unlocked_compounds'],13379)
  self.assertEqual(self.info['learning_curve'][-1]['unique_base_roots_learned'],1820)
 def test_monotonic_coverage(self):
  pairs=[(x['unique_base_roots_learned'],x['unlocked_compounds']) for x in self.info['learning_curve']]
  self.assertEqual(pairs,sorted(pairs))
 def test_example_is_source_grounded(self):
  d={x['compound']:x for x in self.comp}
  self.assertEqual(d['babawayabikhimi']['modifier'],'babawaya')
  self.assertEqual(d['babawayabikhimi']['head'],'bikhimi')
  self.assertEqual(d['babawayabikhimi']['english'],'binaural session')
 def test_not_overclaiming_etymology(self):
  self.assertIn('not a way to guess lexical roots', ' '.join(self.info['claim_limits']))
  self.assertEqual(self.info['unique_ultimate_base_components'],1820)
 def test_site_root_explorer_embedded(self):
  s=(R/'Qaroshi_16_Semantic_Atlas.html').read_text(encoding='utf8')
  self.assertIn('Root Explorer & word builder',s)
  self.assertIn('data-roottry',s)
  self.assertIn('babawayabikhimi',s)
if __name__=='__main__': unittest.main()
