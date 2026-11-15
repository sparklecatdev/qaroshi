import csv,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CoverageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with (ROOT/'data/lexicon.csv').open(encoding='utf-8-sig') as f: cls.rows=list(csv.DictReader(f))
 def test_domains_not_concentrated_in_one_area(self):
  counts=Counter(r['domain'] for r in self.rows)
  self.assertGreaterEqual(len(counts),30)
  for category in ('Medicine and wellbeing','Computers and devices','Mathematics and logic','Food and cooking','Nardoragon life and flight','Law and civic life','Education and learning'):
   self.assertGreater(counts[category],60)
 def test_corpus_translation_not_empty(self):
  with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
  self.assertTrue(all(r['english'] and r['qaroshi'] and r['domain'] for r in rows))
 def test_english_index_covers_entries(self):
  with (ROOT/'data/english_index.csv').open(encoding='utf-8-sig') as f: ix=list(csv.DictReader(f))
  self.assertGreaterEqual(len(ix),len(self.rows))
if __name__=='__main__':unittest.main()
