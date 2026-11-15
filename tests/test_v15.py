"""15.0 editorial corpus tests. Count only actual new authored Qaroshi source lines."""
import csv,json,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/v14'))
from semantic_validator import validate_sentence

def data(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def rows(path):
 with (ROOT/path).open(encoding='utf8') as f:return list(csv.DictReader(f))
class CorpusV15Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.pieces=data('corpus/v15/pieces.json');cls.man=data('corpus/v15/manifest.json');cls.rows=rows('corpus/v15/corpus_rows.csv')
 def test_new_piece_counts(self):
  self.assertEqual(len(self.pieces),85)
  self.assertEqual(sum(p['kind']=='dialogue' for p in self.pieces),73)
  self.assertEqual(sum(p['kind']=='literature' for p in self.pieces),12)
 def test_sentence_counts(self):
  self.assertEqual(len(self.rows),561)
  self.assertEqual(len([r for r in self.rows if r['kind']=='dialogue']),441)
  self.assertEqual(len([r for r in self.rows if r['kind']=='literature']),120)
 def test_whitespace_token_count(self):
  self.assertEqual(sum(len(r['qaroshi'].split()) for r in self.rows),self.man['new_source_language_tokens_whitespace'])
 def test_all_new_structurally_accepted(self):
  failed=[(r['source_id'],validate_sentence(r['qaroshi'],r['english_contextual'])['findings']) for r in self.rows if not validate_sentence(r['qaroshi'],r['english_contextual'])['valid_surface']]
  self.assertEqual(failed,[])
 def test_zero_new_flags(self):
  flags=[(r['source_id'],r['rule_ids']) for r in self.rows if r['rule_ids']]
  self.assertEqual(flags,[])
 def test_id_unique(self):
  self.assertEqual(len(self.rows),len({r['source_id'] for r in self.rows}))
  self.assertEqual(len(self.pieces),len({p['title'] for p in self.pieces}))
 def test_pronunciation_all(self):
  self.assertTrue(all(r['ipa'].startswith('/') and r['sound_out'] for r in self.rows))
 def test_independent_piece_metadata(self):
  self.assertTrue(all(p['premise'] and p['genre'] and p['provenance'] and len(p['lines'])>=5 for p in self.pieces))
 def test_no_native_attestation_claim(self):
  self.assertEqual(self.man['speaker_attestations'],0)
  self.assertEqual(self.man['human_semantic_approvals'],0)
 def test_no_template_source_in_new(self):
  self.assertTrue(all('editorial writing' in r['source_type'] for r in self.rows))
 def test_baseline_content(self):
  self.assertEqual(self.man['baseline_lexicon_sha256'],hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest())
  self.assertEqual(len(rows('data/lexicon.csv')),30000)
  self.assertEqual(len(rows('corpus/parallel_sentences.csv')),4383)
 def test_web_browser_embedded(self):
  html=(ROOT/'Qaroshi_15_Corpus_Library.html').read_text(encoding='utf8')
  self.assertIn('A language in context',html)
  self.assertIn('Concordance',html)
  self.assertNotIn('__DATA__',html)
  self.assertNotIn('data:font/ttf',html)
  bm=data('data/v15/browser_manifest.json')
  self.assertEqual(bm['dialogues'],176)
  self.assertEqual(bm['literature'],35)
 def test_variant_source_separated(self):
  script=(ROOT/'tools/v15/build_browser.py').read_text(encoding='utf8')
  self.assertNotIn('corpus/fluency2026/dialogue_turns.csv',script)
if __name__=='__main__':unittest.main()
