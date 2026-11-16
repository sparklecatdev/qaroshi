"""Backwards-compatible Qaroshi 20 phonemic source and recording queue tests."""
import csv,hashlib,json,unittest,sys,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data/v20';sys.path.insert(0,str(ROOT/'tools'))
from phonetics import IPA,graphemes,syllabify,guide_word,ipa_word

def rows(name):
 with (D/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

class Spoken20(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  html=ROOT/'Qaroshi_20_Speech_Studio.html'
  if not html.exists():
   import subprocess
   subprocess.run([sys.executable,str(ROOT/'tools/v20/restore_site.py')],check=True)
  with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f:cls.lex=list(csv.DictReader(f))
  cls.lexmap={r['qaroshi']:r for r in cls.lex}
  cls.queue=rows('recording_queue_3000.csv');cls.pairs=rows('lexical_sound_contrasts.csv')
  cls.phonemes=rows('phoneme_reference_26.csv');cls.stress=rows('citation_stress_drills.csv')
  cls.res=rows('resonance_delivery_prompts.csv');cls.manifest=json.loads((D/'release_manifest.json').read_text(encoding='utf8'))
 def test_01_unchanged_lexicon(self):self.assertEqual(len(self.lex),30000)
 def test_02_source_reference_count(self):
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:self.assertEqual(len(list(csv.DictReader(f))),4383)
 def test_03_phonemes_26(self):self.assertEqual(len(self.phonemes),26)
 def test_04_inventory_matches(self):self.assertEqual({x['symbol'] for x in self.phonemes},set(IPA))
 def test_05_phonetic_examples_are_dictionary_entries(self):
  for p in self.phonemes:
   self.assertIn(p['example_word'],self.lexmap)
   self.assertEqual(p['example_ipa'],self.lexmap[p['example_word']]['ipa'])
 def test_06_3000_prompt_unique(self):self.assertEqual(len(self.queue),3000);self.assertEqual(len(set(x['record_id'] for x in self.queue)),3000)
 def test_07_queue_has_exact_656_documented_phrases(self):
  with (ROOT/'data/v17/everyday_phrases.csv').open(encoding='utf8',newline='') as f:phrases={x['id']:x for x in csv.DictReader(f)}
  references=[x for x in self.queue if x['kind']=='documented_phrase'];self.assertEqual(len(references),656)
  for r in references:
   with self.subTest(r=r['record_id']):
    p=phrases[r['source_id']];self.assertEqual(r['qaroshi'],p['qaroshi']);self.assertEqual(r['broad_ipa'],p['ipa'])
 def test_08_queue_word_source_matches(self):
  byid={x['id']:x for x in self.lex}
  canonical=[x for x in self.queue if x['kind']=='canonical_word'];self.assertEqual(len(canonical),2344)
  for q in canonical:
   r=byid[q['source_id']];self.assertEqual(q['qaroshi'],r['qaroshi']);self.assertEqual(q['broad_ipa'],r['ipa'])
 def test_09_no_imaginary_recordings(self):
  self.assertTrue(all(x['speaker_recorded']=='no' and x['audio_path']=='' and x['consent_status']=='not_collected' for x in self.queue))
 def test_10_pair_count(self):self.assertGreaterEqual(len(self.pairs),100)
 def test_11_real_grapheme_contrast(self):
  for x in self.pairs:
   a,b=graphemes(x['word_a']),graphemes(x['word_b'])
   self.assertEqual(len(a),len(b));self.assertEqual(sum(u!=v for u,v in zip(a,b)),1)
   self.assertIn(x['word_a'],self.lexmap);self.assertIn(x['word_b'],self.lexmap)
 def test_12_stress_must_be_penultimate(self):
  for x in self.stress:
   self.assertEqual(int(x['stress_index_zero_based']),len(syllabify(x['qaroshi']))-2)
   self.assertEqual(x['syllable_guide'],guide_word(x['qaroshi']))
 def test_13_stress_count(self):self.assertGreaterEqual(len(self.stress),100)
 def test_14_resonance_sources(self):
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:original={x['id']:x for x in csv.DictReader(f)}
  for r in self.res:
   self.assertEqual(r['qaroshi'],original[r['reference_id']]['qaroshi']);self.assertEqual(r['register'],r['qaroshi'].split()[0])
 def test_15_all_16_registers(self):
  markers={x['marker'] for x in json.loads((ROOT/'data/resonances.json').read_text())}
  self.assertEqual({x['register'] for x in self.res},markers)
 def test_16_connected_source_140(self):
  vals=rows('connected_speech_140.csv');self.assertEqual(len(vals),140)
  self.assertTrue(all('no verified' in x['source_status'] for x in vals))
 def test_17_course_14_days(self):self.assertEqual(len(json.loads((D/'14_day_speech_course.json').read_text())),14)
 def test_18_no_speaker_claim(self):self.assertEqual(self.manifest['actual_audio_recordings_included'],0)
 def test_19_canonical_hash(self):self.assertEqual(hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest(),self.manifest['canonical_lexicon_sha256'])
 def test_20_preserve_29_canonical_hashes(self):
  raw=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())['sha256'];self.assertEqual(len(raw),29)
  for p,hash_ in raw.items():self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),hash_)
 def test_21_standalone_html(self):
  h=(ROOT/'Qaroshi_20_Speech_Studio.html').read_text(encoding='utf8')
  self.assertEqual(hashlib.sha256(h.encode('utf8')).hexdigest(),self.manifest['site_html_sha256'])
  for s in ['MediaRecorder','navigator.mediaDevices','recordConsent','RC20-0001','phonemes','decodeAudioData']:
   self.assertIn(s,h)
 def test_22_no_external_script(self):
  s=(ROOT/'Qaroshi_20_Speech_Studio.html').read_text(encoding='utf8');self.assertNotIn('script src="https:',s)
 def test_23_qa_lawful_sharing_boundary(self):
  d=json.loads((D/'audio_review_policy.json').read_text());self.assertTrue(d['explicit_consent_required']);self.assertIn('unverified',d['dialects'])
 def test_24_no_canonical_changes(self):self.assertIs(self.manifest['canonical_changed'],False)
 def test_25_reading_queue_matches_inventory(self):
  self.assertEqual(len(set(r['source_id'] for r in self.queue)),3000)

if __name__=='__main__':unittest.main()
