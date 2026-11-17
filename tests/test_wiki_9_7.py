"""Wiki 9.7 every-word meaning/usage reference coverage and source fidelity."""
from __future__ import annotations
import csv
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class RichLexicalGuides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js=(ROOT/"web/qaroshi.js").read_text(encoding="utf8")
        cls.usage=(ROOT/"web/wiki_usage.js").read_text(encoding="utf8")
        cls.html=(ROOT/"Qaroshi_Wiki.html").read_text(encoding="utf8")
        match=re.search(r'<script type="application/json" id="wiki-data">(.+?)</script>',cls.html,re.S)
        assert match
        cls.metadata=json.loads(match.group(1))

    def test_all_30000_original_entries_and_4383_sentences_untouched(self):
        with (ROOT/"data/lexicon.csv").open(encoding="utf-8-sig",newline="") as fh:
            lexicon=list(csv.DictReader(fh))
        with (ROOT/"corpus/parallel_sentences.csv").open(encoding="utf-8-sig",newline="") as fh:
            corpus=list(csv.DictReader(fh))
        self.assertEqual(len(lexicon),30000)
        self.assertEqual(len(corpus),4383)
        self.assertEqual(self.metadata["words"],[{k:x[k] for k in
            ["id","qaroshi","pos","english","domain","components","note","ipa","reading","sound_out"]} for x in lexicon])
        self.assertEqual(self.metadata["phrases"],[{k:x[k] for k in
            ["id","domain","qaroshi","english","note","pattern","ipa","reading","sound_out"]} for x in corpus])

    def test_part_of_speech_and_source_specific_usage_are_embedded(self):
        self.assertIn("QaroshiUsage",self.html)
        self.assertEqual(self.metadata["pronouns"],json.loads((ROOT/"data/pronouns.json").read_text(encoding="utf8")))
        self.assertEqual(self.metadata["grammaticalParticles"],json.loads((ROOT/"data/grammatical_particles.json").read_text(encoding="utf8")))
        self.assertEqual(self.metadata["resonances"],json.loads((ROOT/"data/resonances.json").read_text(encoding="utf8")))
        self.assertIn("meaningIsEditorialGloss:true",self.usage)
        self.assertIn("sourceRule",self.usage)
        self.assertIn("grammarFrames",self.usage)
        self.assertIn("profile(word,data)",self.usage)

    def test_all_word_articles_have_visible_core_teaching_sections(self):
        for label in ["word-gloss","word-usage","word-example-list","word-example-empty",
                      "word-forms","word-family","word-source-line","word-specific-rule",
                      "word-verb-frame","word-writing","word-neighbors","word-citation"]:
            self.assertIn(label,self.js)
        self.assertIn('id="definition"',self.js)
        self.assertIn('id="usage"',self.js)
        self.assertIn('id="examples"',self.js)
        self.assertIn('id="family"',self.js)
        self.assertIn("pronunciation(w)",self.js)
        self.assertIn("letterBreakdown(w.qaroshi)",self.js)
        self.assertIn("window.QaroshiUsage.sourceIndex",self.js)
        self.assertIn("window.QaroshiUsage.highlight",self.js)

    def test_no_auto_invented_sentences_or_unverified_synonyms(self):
        self.assertIn("not invented complete Qaroshi sentences",self.js)
        self.assertIn("not independently verified translations",self.js)
        self.assertIn("No exact use in the source sentence collection yet",self.js)
        self.assertIn("not necessarily interchangeable synonyms",self.js)
        self.assertIn("not verified synonyms or antonyms",self.js)
        self.assertNotIn("fetch(",self.usage)
        self.assertNotIn("localStorage",self.usage)

    def test_every_word_profile_and_corpus_grounding_node_audit(self):
        p=subprocess.run(["node","tests/wiki97/coverage_all.cjs"],cwd=ROOT,
                         capture_output=True,text=True,timeout=80)
        self.assertEqual(p.returncode,0,p.stderr[:6000])
        self.assertIn("PASS Wiki 9.7 every canonical word",p.stdout)
        self.assertIn('"checked_words": 30000',p.stdout)
        self.assertIn('"independent_human_semantic_comprehension_count": 0',p.stdout)

if __name__=="__main__":
    unittest.main()
