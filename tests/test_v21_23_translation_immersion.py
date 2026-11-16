"""Source parity, comprehension integrity, refusal, and preservation tests."""
from __future__ import annotations
import csv, hashlib, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/v21_23'))
from translator import interpret,records,norm,indices
from restore_artifacts import restore
restore()

class TranslationImmersion21to23(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=records();cls.readers=json.loads((ROOT/'data/v22/graded_editorial_readers_108.json').read_text())
  cls.quests=json.loads((ROOT/'data/v23/source_matching_quizzes.json').read_text());cls.manifest=json.loads((ROOT/'data/v21_23_release_manifest.json').read_text())
  with (ROOT/'corpus/parallel_sentences.csv').open() as f:cls.phrases=list(csv.DictReader(f))
  cls.qa=json.loads((ROOT/'data/v21/editorial_discrepancy_ledger_103.json').read_text())
 def test_01_preserve_29_sha_files(self):
  m=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())['sha256'];self.assertEqual(len(m),29)
  for path,sha in m.items():
   with self.subTest(path=path):self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha)
 def test_02_bilingual_counts(self):
  self.assertEqual(len(self.phrases),4383)
  self.assertEqual(len(self.source),5249)
  self.assertEqual(len({x['id'] for x in self.source}),len(self.source))
 def test_03_reader_counts(self):
  self.assertEqual(len(self.readers),108)
  self.assertEqual(sum(len(r['lines']) for r in self.readers),866)
  self.assertEqual(len({r['id'] for r in self.readers}),108)
 def test_04_all_reading_lines_have_lookup_records(self):
  ids={r['id']:r for r in self.source}
  for piece in self.readers:
   for line in piece['lines']:
    with self.subTest(line=line['id']):
     self.assertIn(line['id'],ids)
     self.assertEqual(line['qaroshi'],ids[line['id']]['qaroshi'])
     self.assertEqual(line['english'],ids[line['id']]['english'])
 def test_05_grades_bounded_and_nonempty(self):
  distribution=self.manifest['reading_bands'];self.assertEqual(sum(distribution.values()),108)
  self.assertTrue(all(distribution[x]>=15 for x in ('foundation','developing','stretch')))
  self.assertTrue(all(0<=x['difficulty_proxy']<=1 for x in self.readers))
 def test_06_exact_q_retrieval(self):
  x=interpret('hë ti haro he?','to-en');self.assertEqual(x['translation'],'Are you well?')
  self.assertEqual(x['status'],'exact documented source match, context-sensitive')
 def test_07_exact_en_retrieval(self):
  x=interpret('I am well.','to-qr');self.assertIn('sen mi haro.',[r['qaroshi'] for r in x['variants']]);self.assertIn('documented source',x['status'])
 def test_08_complex_unlicensed_refused(self):
  x=interpret('The rocket performed a quantum pirouette while negotiating with a stone.','to-qr');self.assertIsNone(x['translation']);self.assertEqual(x['status'],'unresolved')
 def test_09_unknown_qaroshi_refused(self):
  x=interpret('sen zzqxzzll-dë kimë.','to-en');self.assertIsNone(x['translation'])
 def test_10_no_neighbor_claim_as_translation(self):
  x=interpret('A friend will hear me yesterday.','to-qr');self.assertIsNone(x['translation']);self.assertTrue(all('NOT' in r['warning'] for r in x['related_examples']))
 def test_11_context_ledger(self):
  self.assertEqual(len(self.qa),103)
  self.assertTrue(all(x['human_approved'].lower()!='yes' for x in self.qa))
 def test_12_learner_items(self):
  self.assertEqual(len(self.quests),324);self.assertEqual(len({x['id'] for x in self.quests}),len(self.quests))
  for q in self.quests:
   with self.subTest(q=q['id']):
    self.assertEqual(len(q['options']),4)
    self.assertEqual(len(set(q['options'])),4)
    self.assertIn(q['answer_index'],range(4))
    self.assertIn('source',q['skill'])
 def test_13_quizzes_follow_actual_readings(self):
  rdr={r['id']:r for r in self.readers}
  for q in self.quests:
   r=rdr[q['reading_id']];line=next(l for l in r['lines'] if l['id']==q['line_id'])
   self.assertEqual(q['options'][q['answer_index']],line['english']);self.assertEqual(q['qaroshi'],line['qaroshi'])
 def test_14_study_curriculum(self):
  x=json.loads((ROOT/'data/v23/twelve_lesson_learning_path.json').read_text());self.assertEqual(len(x),12)
 def test_15_html_data_and_navigation(self):
  h=(ROOT/'Qaroshi_21_23_Translation_Immersion_Academy.html').read_text()
  for key in ('#reader','id="globalSearch"','id="translateBtn"','id="reviewSearch"','id="wordDetail"','id="quizBody"'):
   self.assertIn(key,h)
  self.assertNotIn('__QAROSHI_21_23_DATA__',h)
 def test_16_morphological_analysis(self):
  x=interpret('sen mi kima-m këmë.','to-en')
  self.assertTrue(any(w.get('root')=='kima' for w in x['word_analysis']))
 def test_17_no_speaker_claim(self):
  self.assertEqual(self.manifest['new_spontaneous_speaker_attestations'],0)
  self.assertEqual(self.manifest['verified_independent_learner_scores'],0)
  self.assertEqual(self.manifest['new_canonical_words'],0)
 def test_18_source_texts_are_preexisting(self):
  self.assertEqual(self.manifest['v15_editorial_lines'],561)
  for p in self.readers:self.assertIn(p['source_path'],['corpus/v15/pieces.json','corpus/v12_13/anthology_12.json','corpus/curated/short_readings.json'])
 def test_19_exact_all_original_reference_ids(self):
  source_ids={x['id'] for x in self.source}
  self.assertTrue(all(x['id'] in source_ids for x in self.phrases))
 def test_20_normalization(self):
  self.assertEqual(norm('  HË  ti  haro   he?  '),norm('hë ti haro he?'))
 def test_21_unapproved_v16_2_still_unapproved(self):
  with (ROOT/'data/v16_2/individually_editorially_reviewed.csv').open() as f:data=list(csv.DictReader(f))
  self.assertEqual(len(data),65)
  self.assertTrue(all(x['status'].startswith('manual_') for x in data))

if __name__=='__main__':unittest.main()
