import csv,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
class QaroshiFinalReference(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.words=rows('data/lexicon.csv')
  cls.sentences=rows('corpus/parallel_sentences.csv')
  cls.grammar=(ROOT/'docs/grammar.md').read_text(encoding='utf-8')
  cls.html=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf-8')
 def test_dictionary_size(self):self.assertEqual(len(self.words),11878)
 def test_dictionary_headwords_unique(self):self.assertEqual(len(set(x['qaroshi'] for x in self.words)),len(self.words))
 def test_dictionary_ids_unique(self):self.assertEqual(len(set(x['id'] for x in self.words)),len(self.words))
 def test_dictionary_schema_unified(self):self.assertEqual(set(self.words[0]),{'id','qaroshi','pos','english','domain','type','components','note'})
 def test_dictionary_no_status_or_edition(self):self.assertNotIn('review',self.words[0]);self.assertNotIn('edition',self.words[0])
 def test_glosses_nonempty(self):self.assertTrue(all(x['english'].strip() for x in self.words))
 def test_dictionary_json_same(self):self.assertEqual(json.loads((ROOT/'data/lexicon.json').read_text()),self.words)
 def test_original_phrase_preserved(self):
  self.assertTrue(any(x['qaroshi']=='më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.' for x in self.sentences))
 def test_phrase_count(self):self.assertEqual(len(self.sentences),2017)
 def test_phrase_ids_unique(self):self.assertEqual(len(set(x['id'] for x in self.sentences)),2017)
 def test_phrase_json_same(self):self.assertEqual(json.loads((ROOT/'corpus/parallel_sentences.json').read_text()),self.sentences)
 def test_phrase_schema_unified(self):self.assertNotIn('edition',self.sentences[0])
 def test_70_chapters(self):self.assertEqual([int(x) for x in re.findall(r'^## (\d+)\.',self.grammar,re.M)],list(range(1,71)))
 def test_glyph_inventory(self):self.assertEqual(len(list((ROOT/'assets/glyphs').glob('*.png'))),26)
 def test_resonances(self):
  obj=json.loads((ROOT/'data/resonances.json').read_text());self.assertEqual(len(obj),16)
 def test_granular_particles(self):
  obj=json.loads((ROOT/'data/grammatical_particles.json').read_text())
  self.assertEqual(len(obj),96);self.assertEqual(len({a['form'] for a in obj}),96)
  for x in obj:self.assertIn(x['form'],{a['qaroshi'] for a in self.words})
 def test_english_index(self):self.assertGreaterEqual(len(rows('data/english_index.csv')),11878)
 def test_offline_html_embed(self):
  self.assertIn('id="wiki-data"',self.html);self.assertIn('id="leftSidebar"',self.html)
  self.assertIn('id="mainContent"',self.html);self.assertIn('id="scriptInput"', (ROOT/'web/qaroshi.js').read_text())
 def test_wiki_no_review_controls(self):
  self.assertNotIn('wordStatus',self.html);self.assertNotIn('wordEdition',self.html)
  self.assertNotIn('phraseEdition',self.html);self.assertNotIn('w.review',self.html)
 def test_no_legacy_grammars(self):self.assertEqual(len(list((ROOT/'docs').glob('grammar*.md'))),1)
 def test_release_description(self):
  self.assertIn('Unified Standard Reference 4.1',(ROOT/'README.md').read_text())
 def test_sample_headwords(self):
  w={r['qaroshi']:r['english'] for r in self.words}
  for x in ['qaro','qaroshi','pëla','lësha','qor','sen','zha','womaro','riqosha']:
   self.assertIn(x,w)
if __name__=='__main__': unittest.main()
