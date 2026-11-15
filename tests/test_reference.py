"""Regression checks for the Qaroshi standard and project build."""
import csv,importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from qaroshi import (LETTERS,RESONANCES,analyze_word,entries,format_morphology,
                     glyphs_of,validate_data)
class ReferenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.rows=entries()
  cls.lex={r['qaroshi']:r for r in cls.rows}
 def test_original_853_preserved(self):
  with (ROOT/'source/Qaroshi_Dictionary_853.csv').open(encoding='utf-8-sig') as f: src=list(csv.DictReader(f))
  self.assertEqual(len(src),853)
  for r in src:
   self.assertIn(r['qaroshi'],self.lex)
   self.assertEqual(self.lex[r['qaroshi']]['english'],r['english'])
   self.assertEqual(self.lex[r['qaroshi']]['pos'],r['pos'])
 def test_unique_headwords(self):
  self.assertEqual(len(self.rows),len(self.lex))
  self.assertGreaterEqual(len(self.rows),6500)
 def test_all_26_native_letters(self):
  self.assertEqual(len(set(LETTERS)),26)
  for g in LETTERS:self.assertTrue((ROOT/'assets/glyphs'/f'{g}.png').is_file())
  for r in self.rows:self.assertTrue(glyphs_of(r['qaroshi']))
 def test_digraphs_are_individual_glyphs(self):
  self.assertEqual(glyphs_of('shazhakhng'),['sh','a','zh','a','kh','ng'])
 def test_resonance_markers(self):
  self.assertEqual(len(RESONANCES),16)
  self.assertTrue(all(r in self.lex for r in RESONANCES))
 def test_existing_phrase_stays_canonical(self):
  s='më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.'
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig') as f:
   self.assertIn(s,[r['qaroshi'] for r in csv.DictReader(f)])
 def test_noun_morphology(self):
  self.assertEqual(format_morphology('mara','noun',plural=True,case='m',endear=True),'mara-lë-ri-m')
  self.assertEqual(format_morphology('qaro','noun',plural=True,case='nga'),'qaro-ri-nga')
  self.assertEqual(format_morphology('mi','noun',case='wa'),'mi-wa')
 def test_verb_morphology(self):
  self.assertEqual(format_morphology('goro','verb',voice='ru',tense='te',aspect='mo',modal='ki',tender=True),
                   'goro-ru-te-mo-ki-la')
  self.assertEqual(format_morphology('nëra','verb',modal='ki'),'nëra-ki')
 def test_morphology_rejects_conflicting_endings(self):
  with self.assertRaises(ValueError):format_morphology('mara','noun',case='ro')
  with self.assertRaises(ValueError):format_morphology('goro','verb',tense='wrong')
  self.assertIsNone(analyze_word('goro-te-yu',self.lex))
 def test_parser_prefers_exact_headword(self):
  self.assertEqual(analyze_word('qaroshi',self.lex)['exact'],True)
  self.assertEqual(analyze_word('goro-te-se',self.lex)['segments'],['te','se'])
 def test_corpus_has_resonance(self):
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig') as f: corp=list(csv.DictReader(f))
  self.assertGreaterEqual(len(corp),800)
  for r in corp:
   self.assertIn(r['qaroshi'].split()[0],RESONANCES,r)
 def test_compounds_are_compositional(self):
  for r in self.rows:
   if r['type']!='compound':continue
   a,b=r['components'].split(' + ')
   self.assertIn(a,self.lex);self.assertIn(b,self.lex)
   self.assertEqual(r['qaroshi'],a+b)
 def test_full_validation(self):
  problems,info=validate_data();self.assertEqual(problems,[])
  self.assertEqual(info['core_preserved'],853)
 def test_edition_markings(self):
  self.assertIn('candidate',{r['review'] for r in self.rows})
  self.assertIn('established',{r['review'] for r in self.rows})
  self.assertIn('standardized',{r['review'] for r in self.rows})
if __name__=='__main__': unittest.main()
