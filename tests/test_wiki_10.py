"""Standard 10 full Wiki integration and explicit provenance boundaries."""
from __future__ import annotations
import csv,json,re,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class Wiki10(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.js=(ROOT/'web/qaroshi.js').read_text(encoding='utf8')
  cls.stdjs=(ROOT/'web/wiki_standard10.js').read_text(encoding='utf8')
  cls.html=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf8')
  m=re.search(r'<script type="application/json" id="wiki-data">(.+?)</script>',cls.html,re.S)
  assert m
  cls.data=json.loads(m.group(1))
  cls.s=cls.data['standard10']
 def test_10_source_counts_and_not_a_human_study(self):
  s=self.s;manifest=s['manifest']
  self.assertEqual(manifest['canonical_words'],30000)
  self.assertEqual(len(self.data['words']),30000)
  self.assertEqual(len(self.data['phrases']),4383)
  self.assertEqual(len(s['dialogues']),manifest['editorial_conversations'])
  self.assertEqual(len(s['controlled_drills']),manifest['machine_roundtrip_drills'])
  self.assertGreaterEqual(len(s['controlled_drills']),1500)
  self.assertEqual(manifest['source_dialogues_original11'],49)
  self.assertEqual(manifest['independent_human_reader_trials'],0)
  self.assertEqual(manifest['independent_human_attestations'],0)
 def test_priority_sense_vs_unreviewed_candidate_differentiated(self):
  self.assertEqual(len(self.s['priorities']),800)
  self.assertGreaterEqual(len(self.s['draft_cards']),4500)
  self.assertGreaterEqual(len(self.s['profiles']),40)
  self.assertGreaterEqual(sum(len(v) for v in self.s['senses'].values()),40)
  for w,profile in self.s['profiles'].items():
   self.assertTrue(profile['definition'])
   self.assertEqual(profile['classification'].startswith('individually authored'),True)
  for w,proposal in self.s['draft_cards'].items():
   self.assertIn('UNREVIEWED',proposal['status'])
   self.assertEqual(proposal['independent_human_attestation'],False)
  self.assertIn('No separately reviewed sense definition',self.stdjs)
  self.assertIn('not a new approved sense',self.stdjs.lower())
 def test_routes_and_interactive_render(self):
  for label in ["case 'conversations'","case 'conversation'","case 'drills'","case 'validation'"]:
   self.assertIn(label,self.js)
  self.assertIn('ST10.sensesHTML(w)',self.js)
  self.assertIn('ST10.dialogueIndex(main)',self.js)
  self.assertIn('ST10.conversation(main,id)',self.js)
  self.assertIn('ST10.drillLibrary(main)',self.js)
  self.assertIn('ST10.validation(main)',self.js)
  self.assertIn('data-english',self.stdjs)
  self.assertIn('aria-expanded',self.stdjs)
  self.assertIn('reader_sheet_sha256', (ROOT/'tools/standard10/trial.py').read_text(encoding='utf8'))
  self.assertIn('facilitator_english_key.csv', (ROOT/'tools/standard10/trial.py').read_text(encoding='utf8'))
  self.assertNotIn('fetch(',self.stdjs)
  self.assertNotIn('localStorage',self.stdjs)
 def test_browser_module_senses_provenance_regression(self):
  proc=subprocess.run(['node','tests/standard10/ui.cjs'],cwd=ROOT,capture_output=True,text=True,timeout=40)
  self.assertEqual(proc.returncode,0,proc.stderr[:3500])
  self.assertIn('PASS Standard 10',proc.stdout)

if __name__=='__main__': unittest.main()
