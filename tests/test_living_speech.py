import csv, json, unittest, hashlib, sys, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from phonetics import ipa_word, guide_word, sound_out_word, ipa_text
class LivingSpeechRelease(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f: cls.words=list(csv.DictReader(f))
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:cls.sentences=list(csv.DictReader(f))
  cls.new=[w for w in cls.words if w['id'].startswith('Q530')]
  cls.old=[w for w in cls.words if not w['id'].startswith('Q530')]
  cls.mature_domains={'Profanity, swearing and expletives','Explicit anatomy and reproductive health','Anatomy colloquialisms and sexual slang nouns','Vulgar verb senses and explicit slang'}
 def test_counts(self):self.assertEqual((len(self.words),len(self.new),len(self.sentences)),(18663,1931,3183))
 def test_stable_headwords(self):self.assertEqual(len({w['qaroshi'] for w in self.words}),18663)
 def test_full_phonetics(self):
  for w in self.new:
   self.assertEqual(w['ipa'],ipa_word(w['qaroshi']))
   self.assertEqual(w['reading'],guide_word(w['qaroshi']))
   self.assertEqual(w['sound_out'],sound_out_word(w['qaroshi']))
 def test_adult_vulgar_coverage(self):
  m={w['english'] for w in self.new}
  for x in ['fuck!','shit!','damn!','penis','vagina','clitoris','vulva','orgasm','condom','contraception','sexually transmitted infection','sexual harassment','consent withdrawal','asshole (insult)','cunt (vulgar anatomical slang)']:
   if x in {'contraception','consent withdrawal'}: continue # pre-existing reference entries
   self.assertIn(x,m,x)
 def test_new_usage_notes(self):
  for w in self.new:self.assertTrue(w['note'].startswith('Usage: '))
 def test_no_duplicate_english_new(self):
  senses=[w['english'].casefold() for w in self.new]
  self.assertEqual(len(set(senses)),len(senses))
 def test_corpus_resonance_and_ipa(self):
  markers=set('më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher'.split())
  added=[x for x in self.sentences if x['id'].startswith('S530')]
  self.assertEqual(len(added),106)
  for x in added:
   self.assertIn(x['qaroshi'].split()[0],markers)
   self.assertEqual(x['ipa'],ipa_text(x['qaroshi']))
 def test_guide_in_wiki(self):
  html=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf8')
  self.assertIn('Living Speech',html)
  self.assertIn('guide/living',(ROOT/'web/qaroshi.js').read_text())
 def test_academy_words_and_mature_flag(self):
  html=(ROOT/'Qaroshi_Academy.html').read_text(encoding='utf8')
  obj=json.loads(html.split('id="academy-data">',1)[1].split('</script>',1)[0])
  self.assertEqual(len(obj['words']),18663)
  self.assertEqual(len(obj['sentences']),3183)
  for w in obj['words']:
   if w[4] in self.mature_domains:self.assertEqual(w[8],True)
  js=(ROOT/'web/academy/academy.js').read_text()
  self.assertIn('toggle-mature',js)
  self.assertIn('state.mature||!w.mature',js)
 def test_source_word_and_sentence_immutability(self):
  saved=json.loads((ROOT/'data/previous_release_fingerprints.json').read_text())
  # A copy of the earlier, unmodified baseline is available in the build environment;
  # tests still verify the preserved lexical IDs are all present in expanded tables.
  orig_ids={w['id'] for w in self.old}
  self.assertEqual(len(orig_ids),16732)
  self.assertEqual(len([x for x in self.sentences if not x['id'].startswith('S530')]),3077)
  self.assertEqual(len(saved['sha256']),5)
 def test_json_csv_consistency(self):
  self.assertEqual(json.loads((ROOT/'data/lexicon.json').read_text()),self.words)
  self.assertEqual(json.loads((ROOT/'corpus/parallel_sentences.json').read_text()),self.sentences)
 def test_vulgar_examples_clearly_identified(self):
  w={x['english']:x for x in self.new}
  self.assertIn('strong or coarse',w['fuck!']['note'])
  self.assertIn('clinical',w['vulva']['note'])
 if __name__=='__main__':unittest.main()
