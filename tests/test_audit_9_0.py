"""Evidence integrity for all 190 inherited editorial drafts and 9.0 blind packets.

Formal checks and prepared questionnaires do not count as human backtranslations.
"""
from __future__ import annotations
import csv
import unittest
from pathlib import Path

from tools.stress90.audit import run,rows
from tools.stress90.compose import OUT

ROOT=Path(__file__).resolve().parents[1]

class Audit90(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary=run()
        cls.ledger=rows(OUT/"case_evidence_500.csv")
        cls.review=rows(OUT/"formal_review_500.csv")
        cls.blind=rows(OUT/"blind_qaroshi_only.csv")
        cls.key=rows(OUT/"private_english_answer_key.csv")
        cls.unresolved=rows(OUT/"unresolved_cases.csv")
        cls.old=rows(ROOT/"data/stress89/case_evidence_500.csv")

    def test_500_stimuli_and_total_counts_are_consistent(self):
        self.assertEqual(self.summary["all_stimuli_preserved"],500)
        self.assertEqual(len(self.ledger),len(self.review))
        self.assertEqual(len(self.ledger),500)
        self.assertEqual(self.summary["inherited_editorial_candidates_formally_reviewed"],190)
        self.assertEqual(self.summary["all_current_candidate_prompts_blinded"],len(self.blind))
        self.assertEqual(len(self.blind),len(self.key))
        self.assertEqual(self.summary["still_no_full_draft"],len(self.unresolved))
        self.assertEqual(len(self.ledger),len(self.blind)+len(self.unresolved))
        self.assertEqual(self.summary["human_backtranslations_collected"],0)
        self.assertEqual(self.summary["independent_comprehension_trials"],0)
        self.assertEqual(self.summary["independent_semantic_equivalence_decisions"],0)
        self.assertFalse(self.summary["speaker_comprehension_claimed"])
        self.assertTrue(self.summary["blind_key_separated"])

    def test_all_190_inherited_drafts_preserved_and_reviewed(self):
        prior={x["id"] for x in self.old if x["qaroshi_full_candidate"]}
        self.assertEqual(len(prior),190)
        observed={x["id"] for x in self.review if x["source_edition"]=="8.9_or_earlier" and x["qaroshi_candidate"]}
        self.assertEqual(prior,observed)
        current={x["id"]:x for x in self.ledger}
        for x in self.old:
            if x["id"] in prior:
                self.assertEqual(x["qaroshi_full_candidate"],current[x["id"]]["qaroshi_full_candidate"])

    def test_blind_packets_have_no_originals_or_answers(self):
        self.assertEqual({x["case_id"] for x in self.blind},
                         {x["case_id"] for x in self.key})
        self.assertTrue(all("original_english" not in x and "english_target" not in x
                            and "required_semantic_components" not in x for x in self.blind))
        self.assertTrue(all(not x["human_translation"] and not x["reader_consent"] and
                            not x["uncertain_parts"] and not x["reader_id"] for x in self.blind))
        self.assertTrue(all(not x["independent_rater_score"] and not x["rater_id"] and
                            not x["rater_reasoning"] for x in self.key))
        self.assertTrue(all(x["packet"] in ("A","B","C") for x in self.blind))
        self.assertTrue(all(x["qaroshi_only"] for x in self.blind))
        originals={x["id"]:x["english"] for x in self.ledger}
        for x in self.key:
            self.assertEqual(x["original_english"],originals[x["case_id"]])

    def test_formal_flags_are_not_human_certification(self):
        for x in self.review:
            self.assertEqual(x["independent_backtranslation_status"],"not undertaken")
            self.assertEqual(x["external_reader_count"],"0")
            self.assertEqual(x["semantic_equivalence_decision"],"unadjudicated")
            self.assertEqual(x["attestation_claim"],"none")
            self.assertTrue(x["formal_check_not_human"])
        self.assertEqual(sum(self.summary["formal_check_counts"].values()),500)
        self.assertEqual({x["id"] for x in self.review if not x["qaroshi_candidate"]},
                         {x["id"] for x in self.unresolved})

    def test_unresolved_cases_are_explicit_unknowns_not_inexpressibility_proofs(self):
        for x in self.unresolved:
            self.assertEqual(x["proven_inexpressible_in_qaroshi"],"no")
            self.assertTrue(x["semantic_components_required"])
            self.assertTrue(x["why_unresolved"])
            self.assertEqual(x["needs_attested_speaker_review"],"yes")
        self.assertTrue(self.summary["no_content_invented_for_unresolved"])

if __name__=="__main__":
    unittest.main()
