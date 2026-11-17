"""Check the self-contained Wiki 9.5 actually embeds current tools and data."""
from __future__ import annotations
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class Wiki95(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/"tools/build_wiki.py").read_text(encoding="utf8")
        cls.html=(ROOT/"Qaroshi_Wiki.html").read_text(encoding="utf8")
        cls.script=(ROOT/"web/qaroshi.js").read_text(encoding="utf8")
        cls.lab=(ROOT/"web/wiki_lab.js").read_text(encoding="utf8")
        cls.gram=(ROOT/"web/grammar_live.js").read_text(encoding="utf8")
        match=re.search(r'<script type="application/json" id="wiki-data">(.+?)</script>',cls.html,re.S)
        assert match,"Missing embedded, offline semantic + grammar metadata"
        cls.metadata=json.loads(match.group(1))

    def test_current_standard_90_chapters_and_ten_complete_amendments(self):
        self.assertEqual(len(self.metadata["chapters"]),90)
        self.assertEqual(len(self.metadata["grammarAddenda"]),10)
        self.assertEqual([x["edition"] for x in self.metadata["grammarAddenda"]],
            ["8.1","8.4","8.5","8.6","8.7","8.8A","8.8B","8.9","9.0","9.1"])
        self.assertIn("Current single-entry grammar",self.metadata["currentGrammarIntro"])
        self.assertIn("docs/standard_8/grammar.md",self.source)
        self.assertNotIn("chapter_docs=[('docs/grammar.md'",self.source)
        self.assertEqual([x["number"] for x in self.metadata["chapters"]],list(range(1,91)))

    def test_live_grammar_subset_is_embedded_with_original_licenses(self):
        licenses=self.metadata["grammarLicenses"]
        frames=self.metadata["grammarFrames"]
        self.assertEqual(licenses,json.loads((ROOT/"data/standard_9_3/grammar_licenses.json").read_text(encoding="utf8")))
        self.assertEqual(frames,json.loads((ROOT/"data/semantics/valency_frames.json").read_text(encoding="utf8")))
        self.assertEqual(len(licenses["verb_overrides"]),25)
        self.assertEqual(len(licenses["nouns"]),10)
        self.assertIn("QaroshiGrammar",self.html)
        self.assertIn("QaroshiWikiLab",self.html)
        self.assertIn("role=\"tabpanel\"",self.lab)
        self.assertIn("aria-selected",self.lab)

    def test_exact_500_cases_and_no_invented_human_validation(self):
        cases=self.metadata["semanticCases"]
        self.assertEqual(len(cases),500)
        self.assertEqual(len({c["id"] for c in cases}),500)
        self.assertEqual({c["domain"] for c in cases},
           {"daily","time_motion","social_consent","quantifier_logic","evidentiality",
            "embedding_reference","counterfactual_modal","voice_valency",
            "narrative_figures","technical_precision"})
        self.assertEqual({c["review_status"] for c in cases},{"unadjudicated"})
        self.assertTrue(all(c["english"] and c["qaroshi"] and c["roles"] for c in cases))
        with (ROOT/"data/standard_9_2/semantic_repairs.json").open(encoding="utf8") as file:
            repair=json.load(file)["corrections"][0]
        actual=next(x for x in cases if x["id"]==repair["case_id"])
        self.assertEqual(actual["qaroshi"],repair["current_9_2"])
        self.assertNotIn("external_human_paraphrase",actual)

    def test_navigation_is_reduced_but_all_routes_and_deep_links_persist(self):
        self.assertIn("function groupedTopics()",self.script)
        self.assertIn("topicGroups",self.script)
        self.assertIn("data-topic-group",self.script)
        self.assertNotIn("Popular topics",self.script)
        self.assertIn("case 'workshop'",self.script)
        self.assertIn("case 'cases'",self.script)
        self.assertIn("case 'case'",self.script)
        self.assertIn("case 'standard'",self.script)
        self.assertIn("case 'word'",self.script)
        self.assertIn("case 'grammar'",self.script)
        self.assertIn("dictionary?domain=",self.script)
        self.assertIn("Qaroshi_21_23_Translation_Immersion_Academy.html",self.script)
        self.assertIn("Qaroshi_20_Speech_Studio.html",self.script)
        self.assertIn("Qaroshi_18_19_Living_Language_Studio.html",self.script)
        self.assertIn('<details class="chapter-group"',self.script)

    def test_self_contained_browser_no_remote_api_and_no_raw_data(self):
        self.assertIn("<script>",self.html)
        self.assertIn("id=\"wiki-data\"",self.html)
        self.assertIn("wiki_lab.js",self.source)
        self.assertIn("grammar_live.js",self.source)
        self.assertNotIn("<script src=\"https://",self.html)
        self.assertNotIn("https://cdn.",self.html)
        self.assertNotIn('getUserMedia',self.gram)
        self.assertNotIn('fetch(',self.gram)
        self.assertNotIn('fetch(',self.lab)
        self.assertNotIn('eval(',self.gram)
        self.assertGreater(len(self.html),12000000)

    def test_node_browser_grammar_parity(self):
        proc=subprocess.run(["node","tests/wiki95/grammar_browser.cjs"],
                            cwd=ROOT,capture_output=True,text=True,timeout=45)
        self.assertEqual(proc.returncode,0,proc.stderr[:4000])
        self.assertIn("PASS",proc.stdout)
        self.assertIn("browser parser/composer roundtrips",proc.stdout)

if __name__=="__main__":unittest.main()
