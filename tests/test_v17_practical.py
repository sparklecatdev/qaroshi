"""Checks for the reference-grounded Qaroshi 17 practical communication release."""
import csv, hashlib, json, unittest
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/v17'

class TestPractical17(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.phrases=json.loads((DATA/'everyday_phrases.json').read_text())
  cls.lessons=json.loads((DATA/'lessons.json').read_text())
  cls.missions=json.loads((DATA/'missions.json').read_text())
  cls.probes=json.loads((DATA/'sentence_builder_fixtures.json').read_text())
  cls.meta=json.loads((DATA/'practical_manifest.json').read_text())
  cls.source={r['id']:r for r in csv.DictReader((ROOT/'corpus/parallel_sentences.csv').open())}
 def test_base_30000(self):
  self.assertEqual(sum(1 for x in csv.DictReader((ROOT/'data/lexicon.csv').open())),30000)
 def test_preserve_source(self):
  source=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())['sha256']
  self.assertEqual(len(source),29)
  for rel,sha in source.items():
   with self.subTest(rel=rel):self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),sha)
 def test_phenomena_preserved(self):
  self.assertEqual(len(json.loads((ROOT/'data/resonances.json').read_text())),16)
  self.assertEqual(len(list((ROOT/'assets/glyphs').glob('*.png'))),26)
 def test_phrase_size(self):
  self.assertGreaterEqual(len(self.phrases),600)
  self.assertEqual(len(self.phrases),self.meta['phrase_count'])
 def test_all_296_core_preserved(self):
  core={i for i,r in self.source.items() if r['pattern'] in ('original phrasebook','living speech 5.3')}
  self.assertEqual(len(core),296)
  self.assertTrue(core.issubset({p['id'] for p in self.phrases}))
 def test_corpus_alignment(self):
  for p in self.phrases:
   with self.subTest(id=p['id']):
    src=self.source[p['id']]
    for f in ('qaroshi','english','ipa','sound_out','pattern'):
     self.assertEqual(src[f],p[f])
 def test_unique_ids(self):self.assertEqual(len(self.phrases),len({p['id'] for p in self.phrases}))
 def test_provenance_not_attested(self):
  self.assertTrue(all('not speaker attested' in p['provenance'] for p in self.phrases))
 def test_screening_annotates_known_issue(self):
  p=next(p for p in self.phrases if p['id']=='S00019')
  self.assertIn('R14-003',p['review_rules'])
 def test_pronunciation(self):
  self.assertTrue(all(p['ipa'].startswith('/') and p['sound_out'] for p in self.phrases))
 def test_practical_coverage(self):
  cats={p['category'] for p in self.phrases}
  self.assertGreaterEqual(len(cats),12)
  self.assertIn('Safety and consent',cats)
  self.assertTrue(any('do not consent' in p['english'].lower() for p in self.phrases))
  self.assertTrue(any("don't understand" in p['english'].lower() for p in self.phrases))
 def test_dialogue_count(self):self.assertGreaterEqual(len(self.missions),25)
 def test_dialogue_turns_source(self):
  originals={}
  for r in csv.DictReader((ROOT/'corpus/original11/dialogue_turns.csv').open()): originals.setdefault(r['scene_id'],[]).append(r)
  for m in self.missions:
   with self.subTest(id=m['id']):
    a=originals[m['id']];self.assertEqual(len(m['turns']),len(a))
    self.assertEqual([r['qaroshi'] for r in m['turns']],[r['qaroshi'] for r in a])
 def test_learning_path(self):
  self.assertEqual(len(self.lessons),10)
  for l in self.lessons:
   self.assertEqual(len(l['phrases']),5)
   for p in l['phrases']:
    self.assertEqual(p['qr'],self.source[p['id']]['qaroshi'])
 def test_builder_fixtures(self):
  self.assertGreaterEqual(len(self.probes),250)
  from tools.v14.semantic_validator import validate_sentence
  for p in self.probes:
   result=validate_sentence(p['qaroshi'])
   self.assertTrue(result['valid_surface'],p['qaroshi'])
   self.assertFalse(any(f['rule_id']=='R14-009' for f in result['findings']),p['qaroshi'])
 def test_120_lemmas(self):
  p=list(csv.DictReader((DATA/'core_learning_120.csv').open()))
  self.assertEqual(len(p),120)
  self.assertEqual(len({r['root'] for r in p}),120)
 def test_standalone_and_glyphs(self):
  s=(ROOT/'Qaroshi_17_Everyday_Communicator.html').read_text()
  self.assertIn('<!doctype html>',s.lower())
  self.assertIn('data:image/png;base64',s)
  self.assertIn('not speaker-attested',s)
  self.assertNotIn('/*__QAROSHI_DATA__*/',s)
 def test_manifest_consistency(self):
  self.assertEqual(self.meta['mission_count'],len(self.missions))
  self.assertEqual(self.meta['builder_fixtures'],len(self.probes))
  self.assertEqual(self.meta['glyph_count'],26)
  self.assertEqual(self.meta['original_phrasebook'],190)
  self.assertEqual(self.meta['living_speech'],106)

if __name__=='__main__':unittest.main()
