"""Formal semantic audit of all 500 proposed Qaroshi translations.

A source-linked machine test is never a human-certified interpretation.
"""
from __future__ import annotations
import json
import unittest
from collections import Counter
from pathlib import Path

from tools.stress92.semantic_audit import run,check,FEATURES,OUT
from tools.stress91.compose import rows as csvrows

ROOT=Path(__file__).resolve().parents[1]

class SemanticAudit92(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run()
        cls.review=csvrows(OUT/"semantic_review_500.csv")
        cls.queue=csvrows(OUT/"editorial_action_queue.csv")
        cls.original={r["id"]:r for r in csvrows(ROOT/"data/stress81/challenges_500.csv")}
        cls.ledger={r["id"]:r for r in csvrows(ROOT/"data/stress91/case_evidence_500.csv")}

    def test_every_one_of_500_stimuli_checked_without_fabricating_human_approval(self):
        summary=self.report
        self.assertEqual(summary["original_cases"],500)
        self.assertEqual(summary["full_existing_editorial_drafts"],500)
        self.assertEqual(summary["checked_for_speech_act_by_domain"],500)
        self.assertEqual(summary["unresolved_editorial_equivalence"],500)
        self.assertEqual(summary["structural_blockers"],0)
        self.assertEqual(summary["all_9_1_originals_preserved"],500)
        self.assertEqual(summary["versioned_9_2_grammatical_corrections"],1)
        self.assertEqual(summary["versioned_correction_case_ids"],["QS81-0336"])
        self.assertEqual(summary["human_backtranslations_collected"],0)
        self.assertEqual(summary["independent_semantic_truth_condition_ratings"],0)
        self.assertEqual(summary["humans_who_used_qaroshi_without_english"],0)
        self.assertEqual(len(FEATURES),10)
        self.assertEqual(len(self.review),len(self.queue))
        self.assertEqual(len(self.review),500)
        self.assertEqual({r["case_id"] for r in self.review},set(self.original))
        self.assertEqual(sum(summary["blockers_by_domain"].values()),summary["structural_blockers"])

    def test_source_identity_operator_features_and_preliminary_status_are_exact(self):
        self.assertEqual(Counter(r["domain"] for r in self.review),
                         Counter({domain:50 for domain in FEATURES}))
        for row in self.review:
            with self.subTest(row=row["case_id"]):
                id_=row["case_id"]
                self.assertEqual(row["english_target"],self.original[id_]["english"])
                inherited=self.ledger[id_]["qaroshi_full_candidate"]
                if id_=="QS81-0336":
                    self.assertEqual(row["qaroshi_proposal"],inherited[:-1]+" qinë.")
                    self.assertTrue(row["9_2_versioned_correction_reason"])
                else:
                    self.assertEqual(row["qaroshi_proposal"],inherited)
                    self.assertFalse(row["9_2_versioned_correction_reason"])
                self.assertEqual(row["prior_9_1_proposal"],inherited)
                self.assertEqual(row["source_feature"],
                                 FEATURES[row["domain"]][int(row["variant"])-1])
                self.assertEqual(row["certified_translation"],"no")
                self.assertEqual(row["speaker_comprehension"],"not_tested")
                self.assertEqual(row["human_editorial_equivalence"],"unadjudicated")
                self.assertEqual(row["independent_backtranslation"],"")
                self.assertEqual(row["reviewer_notes"],"")
                self.assertTrue(row["editorial_origin"])
                self.assertIn(row["structural_status"],
                              ("bounded_form_checks_passed","blocked_review"))

    def test_counterfactual_scope_bug_corrected_with_immutable_old_string(self):
        current={r["case_id"]:r for r in self.review}["QS81-0336"]
        old=self.ledger["QS81-0336"]["qaroshi_full_candidate"]
        self.assertEqual(old,"sen wënu regaro pënaro-m rëgë-te, yarowe wërawë-te.")
        self.assertEqual(current["qaroshi_proposal"],old[:-1]+" qinë.")
        self.assertEqual(current["prior_9_1_proposal"],old)
        self.assertIn("counterfactual",current["9_2_versioned_correction_reason"])
        self.assertEqual(current["structural_status"],"bounded_form_checks_passed")
        self.assertEqual(current["certified_translation"],"no")

    def test_errors_become_visible_action_items_not_automatic_fake_translations(self):
        self.assertEqual({r["case_id"] for r in self.queue},
                         {r["case_id"] for r in self.review})
        byid={r["case_id"]:r for r in self.review}
        for item in self.queue:
            orig=byid[item["case_id"]]
            if orig["structural_status"]=="blocked_review":
                self.assertEqual(item["priority"],"structural_blocker")
                self.assertTrue(json.loads(item["issues"]))
            else:
                self.assertEqual(item["priority"],"requires_external_comprehension")
            self.assertFalse(item["editorial_decision"])
            self.assertFalse(item["independent_reading"])
            self.assertFalse(item["rater_id"])

    def test_mutations_of_genuine_scope_markers_are_flagged(self):
        from tools.stress92.semantic_audit import check
        with (ROOT/"data/lexicon.csv").open(newline="",encoding="utf8") as f:
            import csv
            canon={r["id"]:r for r in csv.DictReader(f)}
        overlay={x["id"]:x for x in json.loads(
            (ROOT/"data/standard_8/editorial_lexicon_9_1.json").read_text(encoding="utf8")
        )["entries"]}
        # Select an original explicitly consent-based source prompt and turn
        # its *revocation* into a weaker sentence with no consent withdrawal.
        id_="QS81-0130"
        x=dict(self.ledger[id_])
        q=x["qaroshi_full_candidate"]
        self.assertIn("maho-m keleyu-te.",q)
        x["qaroshi_full_candidate"]=q.replace("maho-m keleyu-te.","maho-m hari-te.")
        got=check(x,self.original[id_],canon,overlay)
        self.assertEqual(got["structural_status"],"blocked_review")
        self.assertTrue(any("Missing expected semantic operator" in x
                        for x in json.loads(got["blocking_form_issues"])))
        # Reverse modal ordering in a known permission-withdrawal case.
        x=dict(self.ledger[id_])
        self.assertIn("-te-ki",x["qaroshi_full_candidate"])
        x["qaroshi_full_candidate"]=x["qaroshi_full_candidate"].replace("-te-ki","-ki-te")
        got=check(x,self.original[id_],canon,overlay)
        self.assertEqual(got["structural_status"],"blocked_review")
        self.assertTrue(any("Reversed modal" in x
                        for x in json.loads(got["blocking_form_issues"])))

if __name__=="__main__": unittest.main()
