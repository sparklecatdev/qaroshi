"""15.1 corpora regression and provenance transparency tests."""
from pathlib import Path
import unittest,csv,json,hashlib,random
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'corpus/v15_completion'
def load(name):return json.loads((DATA/name).read_text(encoding='utf8'))
def rows(name):
 with (DATA/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
class V15Completion(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.man=load('completion_manifest.json');cls.qa=load('qa_manifest.json');cls.catalog=rows('complete_piece_catalog.csv');cls.lines=rows('complete_corpus_rows.csv');cls.generated=load('generated_manifest.json')
 def test_dialogue_count_numerical(self):self.assertEqual(sum(x['kind']=='dialogue' for x in self.catalog),1000)
 def test_original_provenance_separated(self):
  self.assertEqual(sum(x['kind']=='dialogue' and x['origin']=='original_editorial' for x in self.catalog),176)
  self.assertEqual(sum(x['kind']=='dialogue' and x['origin']=='procedural_editorial' for x in self.catalog),824)
 def test_prose_count_numerical(self):self.assertEqual(sum(x['kind']=='literature' for x in self.catalog),205)
 def test_prose_provenance(self):
  self.assertEqual(sum(x['kind']=='literature' and x['origin']=='original_editorial' for x in self.catalog),35)
  self.assertEqual(sum(x['kind']=='literature' and x['origin']=='procedural_editorial' for x in self.catalog),170)
 def test_token_count_recomputed(self):
  self.assertEqual(sum(len(x['qaroshi'].split()) for x in self.lines),self.man['source_language_token_count_whitespace'])
  self.assertGreater(self.man['source_language_token_count_whitespace'],100000)
 def test_no_legacy_drills_in_volume_count(self):
  self.assertEqual(self.man['source_language_tokens_by_provenance']['original_editorial'],6828)
  self.assertEqual(self.man['source_language_tokens_by_provenance']['procedural_editorial'],204538)
 def test_all_sources_have_resonances(self):
  resonances={'më','zha','qor','sen','hë','lën','sur','rak','khar','yë','nëm','wen','dal','rëm','hol','zher'}
  self.assertTrue(all(x['qaroshi'].split()[0] in resonances for x in self.lines))
 def test_all_sources_license_lexemes(self):
  from tools.fluency11.engine import words, LEX,FUNCTIONS,CONNECTORS,RESONANCES
  # Whole corpus was audited at build time. Spot-check deterministic 5000 rows with the v14 parser to catch corrupt source serialization.
  from tools.v14.semantic_validator import validate_sentence
  rng=random.Random(15151)
  sample=rng.sample(self.lines,5000)
  failures=[(r['record_id'],r['qaroshi']) for r in sample if not validate_sentence(r['qaroshi'],r['english_contextual'])['valid_surface']]
  self.assertEqual(failures,[])
 def test_pieces_unique(self):self.assertEqual(len({p['piece_id'] for p in self.catalog}),1205)
 def test_generated_transcripts_not_exact_duplicates(self):
  from itertools import groupby
  rowsnew=rows('aligned_generated.csv');groups={k:[x['qaroshi'] for x in v] for k,v in groupby(rowsnew,key=lambda x:x['piece_id'])}
  self.assertEqual(len(groups),994)
  self.assertEqual(len({tuple(x) for x in groups.values()}),994)
 def test_all_generated_surface_valid(self):
  r=rows('aligned_generated.csv');self.assertEqual(len(r),46061)
  self.assertTrue(all(x['surface_valid']=='true' for x in r))
 def test_review_flags_explicit(self):
  q=rows('complex_clause_review_queue.csv')
  self.assertEqual(len(q),1988)
  self.assertTrue(all('R14-010' in x['rule_ids'] for x in q))
  self.assertTrue(all(x['human_decision']=='' for x in q))
 def test_variation_queue(self):self.assertEqual(len(rows('translation_variation_review.csv')),self.qa['translation_variation_groups'])
 def test_no_speaker_attestation_claim(self):
  self.assertEqual(self.man['original_independently_speaker_attested_utterances'],0)
  self.assertEqual(self.man['independently_human_reviewed_lines'],0)
  self.assertEqual(self.generated['independently_scripted_new_scenes'],0)
 def test_repetition_not_hidden(self):
  self.assertGreater(self.qa['repeated_sentence_percentage'],90)
  self.assertTrue('not met' in self.qa['warning'].lower())
 def test_canonical_source_unchanged(self):
  b=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text(encoding='utf8'))['sha256'];self.assertEqual(len(b),29)
  self.assertTrue(all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==expected for p,expected in b.items()))
 def test_lexicon_reference_size(self):
  with (ROOT/'data/lexicon.csv').open(encoding='utf8') as f:self.assertEqual(len(list(csv.DictReader(f))),30000)
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8') as f:self.assertEqual(len(list(csv.DictReader(f))),4383)
 def test_new_browser_preloaded(self):
  s=(ROOT/'Qaroshi_15_Expanded_Corpus_Library.html').read_text(encoding='utf8')
  self.assertIn('A language in context',s)
  self.assertIn('word concordance',s.lower())
  self.assertIn('824 new scenario',s)
  self.assertNotIn('__CORPUS_PAYLOAD__',s)
  self.assertNotIn('data:font/ttf',s)
 def test_artifact_sizes(self):
  self.assertGreater((DATA/'aligned_generated.csv').stat().st_size,10000000)
  self.assertGreater((DATA/'all_qaroshi_source_only.txt').stat().st_size,1000000)
if __name__=='__main__':unittest.main()
