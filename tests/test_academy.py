import csv,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AcademyStaticChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'Qaroshi_Academy.html').read_text(encoding='utf-8')
  cls.wiki=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf-8')
  cls.src=(ROOT/'web/academy/academy.js').read_text(encoding='utf-8')
  data=cls.html.split('<script type="application/json" id="academy-data">',1)[1].split('</script>',1)[0]
  cls.data=json.loads(data)
 def test_all_dictionary_entries(self):self.assertEqual(len(self.data['words']),18663)
 def test_all_corpus_sentences(self):self.assertEqual(len(self.data['sentences']),3183)
 def test_stable_word_id_count(self):self.assertEqual(len({w[0] for w in self.data['words']}),18663)
 def test_stable_sentence_id_count(self):self.assertEqual(len({w[0] for w in self.data['sentences']}),3183)
 def test_all_lessons(self):self.assertEqual([x['id'] for x in self.data['lessons']],list(range(1,17)))
 def test_all_lesson_models_have_source_ids(self):
  ids={s[0] for s in self.data['sentences']}
  for lesson in self.data['lessons']:
   self.assertEqual(len(lesson['examples']),10)
   self.assertTrue(all(ex['id'] in ids for ex in lesson['examples']))
 def test_guides(self):self.assertEqual(len(self.data['guides']),16)
 def test_resonances(self):self.assertEqual(len(self.data['resonances']),16)
 def test_affixes(self):self.assertEqual(len(self.data['affixes']),29)
 def test_glyphs(self):self.assertEqual(len(self.data['glyphs']),26)
 def test_pronunciations(self):self.assertTrue(all(w[6] and w[7] for w in self.data['words']))
 def test_source_corpus_unchanged(self):
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
  self.assertEqual([w[1] for w in self.data['sentences']],[w['qaroshi'] for w in rows])
 def test_source_dictionary_unchanged(self):
  with (ROOT/'data/lexicon.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
  self.assertEqual([w[1] for w in self.data['words']],[w['qaroshi'] for w in rows])
 def test_wiki_link_to_academy(self):self.assertIn('href="Qaroshi_Academy.html"',self.wiki)
 def test_academy_link_to_wiki(self):self.assertIn('href="Qaroshi_Wiki.html"',self.src)
 def test_progress_export_and_import(self):self.assertIn('Export progress',self.src);self.assertIn('Import progress',self.src)
 def test_no_external_resources(self):
  self.assertNotRegex(self.html,r'<script[^>]+src="https?://')
  self.assertNotRegex(self.html,r'<link[^>]+href="https?://')
