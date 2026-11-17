"""Wiki 9.6 integration checks for dictionary discovery and private study.

The original lexicon/corpus are unchanged. A shared English gloss is not a
certified synonym and no human comprehension results are invented here.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Wiki96(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = (ROOT / "web/qaroshi.js").read_text(encoding="utf8")
        cls.discovery = (ROOT / "web/wiki_discovery.js").read_text(encoding="utf8")
        cls.practice = (ROOT / "web/wiki_practice.js").read_text(encoding="utf8")
        cls.html = (ROOT / "Qaroshi_Wiki.html").read_text(encoding="utf8")
        match = re.search(r'<script type="application/json" id="wiki-data">(.+?)</script>', cls.html, re.S)
        assert match
        cls.metadata = json.loads(match.group(1))

    def test_self_contained_bundles_and_no_online_study_tracking(self):
        self.assertIn("QaroshiDiscovery", self.html)
        self.assertIn("QaroshiPractice", self.html)
        self.assertIn("wiki_discovery.js", (ROOT / "tools/build_wiki.py").read_text(encoding="utf8"))
        self.assertIn("wiki_practice.js", (ROOT / "tools/build_wiki.py").read_text(encoding="utf8"))
        self.assertNotIn("fetch(", self.discovery)
        self.assertNotIn("fetch(", self.practice)
        self.assertNotIn("localStorage", self.practice)
        self.assertNotIn("sendBeacon", self.practice)
        self.assertEqual((ROOT / "index.html").read_bytes(), (ROOT / "Qaroshi_Wiki.html").read_bytes())

    def test_dictionary_and_training_data_are_original(self):
        words = self.metadata["words"]
        phrases = self.metadata["phrases"]
        self.assertEqual(len(words), 30001)
        self.assertEqual(len(phrases), 4383)
        self.assertTrue(all(w.get("id") and w.get("qaroshi") and "components" in w for w in words))
        self.assertTrue(all(p.get("id") and p.get("qaroshi") and p.get("english") for p in phrases))
        self.assertEqual(len(self.metadata["semanticCases"]), 500)
        self.assertEqual({s["review_status"] for s in self.metadata["semanticCases"]}, {"unadjudicated"})

    def test_word_family_has_grounded_components_and_honest_gloss_status(self):
        self.assertIn("recorded component field", self.js)
        self.assertIn("graph.parts", self.js)
        self.assertIn("graph.compounds", self.js)
        self.assertIn("not necessarily interchangeable synonyms", self.js)
        self.assertIn("not verified synonyms or antonyms", self.js)
        self.assertIn("unsupportedAntonyms:true", self.discovery)
        self.assertIn('href="#practice?word=', self.js)
        self.assertIn("discovery.find", self.js)
        self.assertIn("groupedTopics", self.js)
        self.assertIn("dictionaryAdvanced", self.js)

    def test_learning_is_truly_integrated_and_legacy_routes_survive(self):
        self.assertIn("case 'practice':renderPractice(route)", self.js)
        self.assertIn("QaroshiPractice.mount(main,D", self.js)
        self.assertIn("case 'workshop'", self.js)
        self.assertIn("case 'categories'", self.js)
        self.assertIn("case 'grammar'", self.js)
        self.assertIn("Qaroshi_Academy.html", self.js)
        self.assertIn("Qaroshi_20_Speech_Studio.html", self.js)
        self.assertIn("Qaroshi_21_23_Translation_Immersion_Academy.html", self.js)
        self.assertIn("source teaching corpus", self.practice.lower())
        self.assertIn("private", self.practice.lower())

    def test_node_pure_behavior_and_rejects_fake_synonyms(self):
        p = subprocess.run(["node", "tests/wiki96/discovery_practice.cjs"],
                           cwd=ROOT, capture_output=True, text=True, timeout=45)
        self.assertEqual(p.returncode, 0, p.stderr[:4000])
        self.assertIn("PASS Wiki 9.6", p.stdout)


if __name__ == "__main__":
    unittest.main()
