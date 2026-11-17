"""Standard 10.1: field-kit isolation, source conversations and editorial provenance.

No test is a human comprehension outcome; synthetic answers test only the tooling.
"""
from __future__ import annotations

import csv
import json
import re
import tempfile
import unittest
from pathlib import Path

from tools.standard10.trial import build as build_trial
from tools.standard10.reader_html import build as build_reader, learner_rows
from tools.standard10.resources import assemble

ROOT = Path(__file__).resolve().parents[1]


class OfflineHumanStudy(unittest.TestCase):
    def test_reader_page_contains_only_qaroshi_stimuli_not_source_answers(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            manifest = build_trial(out)
            kit = build_reader(out / "learner_blind_items.csv", out / "reader.html")
            page = (out / "reader.html").read_text(encoding="utf-8")
            source_english = list(csv.DictReader((out / "facilitator_english_key.csv").open(
                encoding="utf-8", newline="")))
            self.assertEqual(kit["learner_stimuli"], 80)
            self.assertEqual(manifest["items"], 80)
            self.assertFalse(kit["english_answer_key_embedded"])
            self.assertEqual(kit["participant_data_collected"], 0)
            self.assertNotIn('"contextual_editorial_english"', page)
            self.assertNotIn('"literal_editorial_english"', page)
            self.assertNotIn('"backtranslated_english"', page)
            self.assertNotIn("facilitator_english_key.csv", page)
            self.assertNotIn("localStorage", page)
            self.assertNotIn("sessionStorage", page)
            self.assertNotIn("fetch(", page)
            self.assertNotIn("XMLHttpRequest", page)
            self.assertNotIn("https://", page)
            self.assertIn("consent", page)
            self.assertIn("first_pass_english_paraphrase", page)
            self.assertIn("actor_object_scope_notes", page)
            self.assertIn("reader_confirmed_no_key_access", page)
            match = re.search(r'<script id="blind-items" type="application/json">(.+?)</script>', page, re.S)
            self.assertIsNotNone(match)
            data = json.loads(match.group(1))
            self.assertEqual(data, learner_rows(out / "learner_blind_items.csv"))
            self.assertEqual(len(data), 80)
            self.assertEqual(set(data[0]), {
                "item_id", "previous_qaroshi_context", "target_qaroshi", "task"
            })
            # A source English target must not be embedded as its own keyed field.
            for row in source_english:
                self.assertNotIn(row["contextual_editorial_english"], match.group(1))

    def test_refuse_bogus_english_fields_and_malicious_html(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "reader.csv"
            columns = ("item_id", "previous_qaroshi_context", "target_qaroshi", "task")
            rows = [{"item_id": f"BL10-{i:03d}",
                     "previous_qaroshi_context": "", "target_qaroshi": "sen mi shiri.",
                     "task": "Paraphrase"} for i in range(1, 81)]
            rows[0]["target_qaroshi"] = "</script><img src=x onerror=alert(1)>"
            with p.open("w", newline="", encoding="utf8") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows)
            output = p.parent / "reader.html"
            build_reader(p, output)
            contents = output.read_text(encoding="utf8")
            self.assertNotIn("</script><img", contents)
            self.assertIn("\\u003c", contents)
            rows[0]["editorial_answer"] = "I speak"
            with p.open("w", newline="", encoding="utf8") as f:
                writer = csv.DictWriter(f, fieldnames=(*columns, "editorial_answer"))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "four-field"):
                build_reader(p, output)


class SourceEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = assemble()
        cls.wiki = (ROOT / "web" / "qaroshi.js").read_text(encoding="utf8")
        cls.review = (ROOT / "web" / "wiki_editorial_review.js").read_text(encoding="utf8")
        cls.std = (ROOT / "web" / "wiki_standard10.js").read_text(encoding="utf8")

    def test_conversation_examples_are_separately_labeled_and_exact(self):
        self.assertIn("dialogueByHeadword", self.wiki)
        self.assertIn("window.QaroshiUsage.sourceIndex(connectedTurns", self.wiki)
        self.assertIn("Individually scripted editorial scene", self.wiki)
        self.assertIn("Recombined reference-line scene", self.wiki)
        self.assertIn('id="conversation-context"', self.wiki)
        self.assertIn("not spontaneous speech", self.wiki)
        self.assertIn("window.QaroshiUsage.highlight(t.qaroshi,w.qaroshi", self.wiki)
        self.assertIn("Read the scene", self.wiki)
        self.assertEqual(self.data["manifest"]["independent_human_attestations"], 0)

    def test_review_workbench_is_provisional_with_no_auto_approval(self):
        self.assertEqual(len(self.data["priorities"]), 800)
        self.assertIn("QaroshiEditorial.create(D)", self.wiki)
        self.assertIn("case 'editorial'", self.wiki)
        self.assertIn("UNREVIEWED_EDITORIAL_PROPOSAL_NOT_APPROVED", self.review)
        self.assertIn("No forms, definitions", self.review)
        self.assertIn("document.createElement('a')", self.review)
        self.assertNotIn("fetch(", self.review)
        self.assertNotIn("localStorage", self.review)
        self.assertNotIn("sessionStorage", self.review)
        self.assertIn("Source example ID", self.review)
        self.assertIn("adjudicator", self.std.lower())


if __name__ == "__main__":
    unittest.main()
