"""Standard 9.2: unified grammar and held-out composition, with adversarial controls.

These are model/structure tests; no result is an independent reader score.
"""
from __future__ import annotations
import json
import unittest
from collections import Counter
from pathlib import Path

from tools.stress92.build_grammar import render as render_grammar
from tools.stress92.heldout import build as build_heldout, OUT, load
from tools.stress91.compose import rows as csvrows
from tools.stress92.parse_temporal import parse, parse_not_until_two_sentences, Undecodable

ROOT=Path(__file__).resolve().parents[1]

class Grammar92(unittest.TestCase):
    def test_one_reference_matches_90_chapters_and_all_amendments(self):
        out=ROOT/"docs/standard_9_2/grammar.md"
        content=out.read_text(encoding="utf8")
        self.assertEqual(content,render_grammar())
        self.assertGreater(len(content),180000)
        self.assertIn("## 1. Writing and sound",content)
        self.assertIn("## 90. Genre conventions",content)
        self.assertIn("ROOT → voice/valency → tense → aspect → modality",content)
        self.assertIn("current editorial interpretation",content.casefold())
        self.assertIn("independent",content.casefold())
        for edition in ("8.1","8.4","8.5","8.6","8.7","8.8A","8.8B","8.9","9.0","9.1"):
            self.assertIn("## Edition appendix "+edition,content)
        self.assertEqual(content.count("## Edition appendix "),10)

    def test_9_2_registry_labels_external_attestation_honestly(self):
        x=json.loads((ROOT/"data/standard_9_2/amendment_registry.json").read_text(encoding="utf8"))
        self.assertEqual(x["core_normative"],"docs/standard_8/grammar.md")
        self.assertEqual(len(x["source_paths"]),10)
        self.assertEqual(x["external_human_comprehension_observations"],0)
        self.assertFalse(x["frozen_source_modified"])
        self.assertEqual(len(x["conflict_ids"]),8)
        self.assertTrue(all(z["kind"] in ("adopted","restricted editorial") for z in x["source_paths"]))
        self.assertEqual(x["source_paths"][0]["kind"],"adopted")

class Unseen92(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=build_heldout()
        cls.rows=csvrows(OUT/"unseen_compositions_450.csv")
        cls.older={r["english"].casefold() for r in csvrows(ROOT/"data/stress81/challenges_500.csv")}
        cls.older_q={r["qaroshi_full_candidate"] for r in csvrows(ROOT/"data/stress91/case_evidence_500.csv")}
        cls.spec,cls.frames,cls.labels=load()

    def test_450_originally_unseen_pairings_are_unique(self):
        self.assertEqual(len(self.rows),450)
        self.assertEqual(self.report["novel_editorial_stimuli"],450)
        self.assertEqual(self.report["distinct_cross_family_event_pairs"],90)
        self.assertEqual(self.report["original_English_overlaps"],0)
        self.assertEqual(self.report["original_Qaroshi_overlaps"],0)
        self.assertEqual(self.report["independent_comprehension_trials"],0)
        self.assertEqual(self.report["human_meaning_certified"],0)
        self.assertEqual(set(self.report["relation_types"]),set(self.spec["relations"]))
        self.assertEqual(set(self.report["relation_types"].values()),{90})
        self.assertEqual(len({r["english_novel_target"] for r in self.rows}),450)
        self.assertEqual(len({r["qaroshi_editorial_candidate"] for r in self.rows}),450)
        for row in self.rows:
            self.assertNotEqual(int(row["main_family"]),int(row["endpoint_family"]))
            self.assertNotIn(row["english_novel_target"].casefold(),self.older)
            self.assertNotIn(row["qaroshi_editorial_candidate"],self.older_q)
            self.assertFalse(row["actual_human_backtranslation"])
            self.assertEqual(row["independently_understood_by_humans"],"no")

    def test_independent_reader_recovers_role_order_and_source_status(self):
        for row in self.rows:
            with self.subTest(row=row["id"]):
                got=parse(row["qaroshi_editorial_candidate"])
                self.assertEqual(got.main_family,int(row["main_family"]))
                self.assertEqual(got.endpoint_family,int(row["endpoint_family"]))
                self.assertEqual(got.relation,row["relation"])
                self.assertEqual(got.matrix_event_asserted,row["matrix_event_asserted"]=="true")
                self.assertEqual(got.indefinite_source_report,row["indefinite_source_report"]=="true")
                self.assertEqual(got.direct_polar_question,row["direct_polar_question"]=="true")
                self.assertFalse(got.implied_event_causation)

    def test_mutating_temporal_scopes_changes_meaning_or_is_rejected(self):
        by_relation={}
        for row in self.rows:
            by_relation.setdefault(row["relation"],[]).append(row)
        for row in by_relation["after"][:25]:
            q=row["qaroshi_editorial_candidate"]
            changed=q.replace("sen ana ","sen ëna ",1)
            with self.assertRaises(Undecodable):
                parse(changed)  # The subordinate/matrix event roles invert.
            first,rest=q.split(", ",1)
            malformed=first.replace("sen ana ","sen ana ",1)+", "+rest.replace("-te.","-yu.",1)
            with self.assertRaises(Undecodable):
                parse(malformed)
        for row in by_relation["reported_after"][:25]:
            q=row["qaroshi_editorial_candidate"]
            self.assertTrue(parse(q).indefinite_source_report)
            changed=q.replace(" do yano mi-tu shiri-te.",".")
            interpreted=parse(changed)
            self.assertFalse(interpreted.indefinite_source_report)
            self.assertTrue(interpreted.matrix_event_asserted)
            self.assertNotEqual(interpreted.relation,parse(q).relation)
            with self.assertRaises(Undecodable):
                parse(q.replace("do yano mi-tu shiri-te.","hu."))
        for row in by_relation["question_before"][:25]:
            q=row["qaroshi_editorial_candidate"]
            self.assertTrue(parse(q).direct_polar_question)
            with self.assertRaises(Undecodable):
                parse(q[:-len(" he?")]+".")
            with self.assertRaises(Undecodable):
                parse(q.replace("hë ","sen ",1))

    def test_older_not_until_requires_second_real_event_and_same_boundary(self):
        olds=[r for r in csvrows(ROOT/"data/stress91/case_evidence_500.csv")
              if r["domain"]=="time_motion" and r["variant"]=="4"]
        self.assertEqual(len(olds),10)
        for row in olds:
            q=row["qaroshi_full_candidate"]
            parsed=parse_not_until_two_sentences(q)
            self.assertTrue(parsed["negative_before_boundary"])
            self.assertTrue(parsed["positive_event_asserted_later"])
            self.assertTrue(parsed["same_endpoint"])
            self.assertFalse(parsed["causation_asserted"])
            incomplete=q.split(". sen ana ")[0]+"."
            with self.assertRaises(Undecodable):
                parse_not_until_two_sentences(incomplete)
            negated=q.replace(" nu "," ",1)
            with self.assertRaises(Undecodable):
                parse_not_until_two_sentences(negated)
            dropped=q.replace(". sen ana ",". sen ëna ",1)
            with self.assertRaises(Undecodable):
                parse_not_until_two_sentences(dropped)

if __name__=="__main__": unittest.main()
