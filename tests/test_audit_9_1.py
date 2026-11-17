"""All 500 original challenge texts stay blind until real readers answer them."""
import csv,json,unittest
from pathlib import Path
from tools.stress91.audit import run
from tools.stress91.compose import rows,OUT

ROOT=Path(__file__).resolve().parents[1]

class Audit91(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run()
        cls.ledger=rows(OUT/"case_evidence_500.csv")
        cls.review=rows(OUT/"formal_review_500.csv")
        cls.blind=rows(OUT/"blind_qaroshi_500.csv")
        cls.key=rows(OUT/"private_reviewer_english_key_500.csv")
        cls.source={r["id"]:r for r in rows(ROOT/"data/stress81/challenges_500.csv")}
        cls.old={r["id"]:r for r in rows(ROOT/"data/stress90/case_evidence_500.csv")}

    def test_all_500_edits_generate_review_rows_not_a_fake_human_reading(self):
        r=self.report
        self.assertEqual(r["frozen_original_items"],500)
        self.assertTrue(r["all_have_full_editorial_candidates"])
        self.assertEqual(r["original_9_0_or_earlier_candidates_preserved"],318)
        self.assertEqual(r["new_9_1_editorial_candidates"],182)
        self.assertEqual(r["untranslated_items_at_editorial_draft_stage"],0)
        self.assertEqual(len(self.review),500)
        self.assertEqual(len(self.blind),500)
        self.assertEqual(len(self.key),500)
        self.assertTrue(r["automated_checks_are_not_semantic_certification"])
        self.assertEqual(r["independent_human_backtranslations"],0)
        self.assertEqual(r["independent_comprehension_trials"],0)
        self.assertEqual(r["independent_english_equivalence_decisions"],0)
        self.assertTrue(r["private_english_key_separate_from_blind_packet"])

    def test_original_english_is_exact_and_shown_only_to_raters(self):
        self.assertEqual({x["case_id"] for x in self.blind},
                         {x["case_id"] for x in self.key})
        self.assertEqual({x["case_id"] for x in self.blind},
                         set(self.source))
        self.assertEqual({x["case_id"] for x in self.review},
                         set(self.source))
        self.assertTrue(all("target_english" not in x and "original_english" not in x
                            and "required_semantic_components" not in x for x in self.blind))
        for item in self.key:
            self.assertEqual(item["target_english"],self.source[item["case_id"]]["english"])
            self.assertFalse(item["rater_id"])
            self.assertFalse(item["rater_score"])
            self.assertFalse(item["rater_notes"])

    def test_no_participant_answers_or_attestations_are_fabricated(self):
        for item in self.blind:
            self.assertTrue(item["qaroshi_only"])
            self.assertFalse(item["participant_id"])
            self.assertFalse(item["consent_to_test"])
            self.assertFalse(item["reader_english"])
            self.assertFalse(item["uncertain_elements"])
            self.assertFalse(item["reader_confidence"])
            self.assertIn(item["packet"],("A","B","C"))
        for item in self.review:
            self.assertEqual(item["independent_semantic_equivalence"],"not_tested")
            self.assertEqual(item["human_backtranslation"],"not_collected")
            self.assertEqual(item["independent_reader_count"],"0")
            self.assertEqual(item["human_readers_claimed"],"no")
            self.assertFalse(item["researcher_decision"])
            self.assertFalse(item["researcher_notes"])

    def test_inherited_candidates_are_preserved_in_final_review(self):
        before=sum(bool(x["qaroshi_full_candidate"]) for x in self.old.values())
        self.assertEqual(before,318)
        new={x["id"]:x for x in self.ledger}
        for id_,item in self.old.items():
            if item["qaroshi_full_candidate"]:
                self.assertEqual(new[id_]["qaroshi_full_candidate"],
                                 item["qaroshi_full_candidate"])
        self.assertEqual(sum(x["draft_origin"]=="9.1" for x in self.review),182)
        self.assertEqual(sum(x["draft_origin"]=="9.0_or_earlier" for x in self.review),318)

    def test_structural_flags_are_explicit_not_considered_certifications(self):
        self.assertEqual(
            self.report["cases_with_basic_form_flags"],
            len(self.report["flagged_case_ids"]))
        for item in self.review:
            self.assertIn(item["automated_check_result"],
                          ("form_flagged","no_basic_form_flag_NOT_certified"))
            self.assertTrue(item["semantic_source_signature"] or item["editorial_limits"])
            self.assertTrue(item["required_semantic_factors"])
        flagged={x["case_id"] for x in self.review if x["automated_check_result"]=="form_flagged"}
        self.assertEqual(flagged,set(self.report["flagged_case_ids"]))

if __name__=="__main__":unittest.main()
