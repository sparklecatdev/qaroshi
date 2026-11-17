"""Complete 9.4 frozen-English source intent ledger tests.

A structured original-English annotation is *not* an independent Qaroshi
semantic-equivalence judgment, and must remain unadjudicated.
"""
from __future__ import annotations
import json
import unittest
from collections import Counter
from pathlib import Path
from tools.semantic94.complete import build,source_components,TUPLES,SCOPE,OUT
from tools.stress91.compose import rows

ROOT=Path(__file__).resolve().parents[1]

class Semantic94(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=build()
        cls.ledger=rows(OUT/"source_semantic_requirements_500.csv")
        cls.inherited=rows(OUT/"legacy_190_backfilled.csv")
        cls.independent=rows(OUT/"independent_comprehension_review_queue.csv")
        cls.original={r["id"]:r for r in rows(ROOT/"data/stress81/challenges_500.csv")}

    def test_exact_190_missing_annotations_backfilled_without_attestation(self):
        self.assertEqual(len(self.ledger),500)
        self.assertEqual(len(self.inherited),190)
        self.assertEqual(len(self.independent),500)
        self.assertEqual(self.report["new_source_grounded_missing_signature_backfills"],190)
        self.assertEqual(self.report["inherited_9_0_or_9_1_structured_signatures_retained"],310)
        self.assertEqual(self.report["missing_source_intent_records"],0)
        self.assertEqual(self.report["known_9_2_form_blockers"],0)
        self.assertEqual(self.report["independent_human_paraphrases"],0)
        self.assertEqual(self.report["independently_confirmed_english_qaroshi_equivalences"],0)
        self.assertFalse(self.report["language_independent_of_english_proven"])
        self.assertFalse(self.report["frozen_baselines_modified"])
        self.assertTrue(self.report["all_original_english_strings_preserved"])
        self.assertEqual({r["id"] for r in self.inherited},
                         {r["id"] for r in self.ledger if not r["prior_editorial_signature_json"]})

    def test_roles_derive_from_original_scenarios_not_guessed_from_qaroshi(self):
        self.assertEqual(Counter(r["domain"] for r in self.ledger),
                         Counter({domain:50 for domain in TUPLES}))
        for row in self.ledger:
            with self.subTest(id=row["id"]):
                base=self.original[row["id"]]
                self.assertEqual(row["original_english"],base["english"])
                self.assertEqual(int(row["variant"]),int(base["variant"]))
                domain=row["domain"]
                fam=int(row["family"])
                source=TUPLES[domain][fam-1]
                s=json.loads(row["source_semantic_intent_json"])
                self.assertEqual(s["original_english_exact"],base["english"])
                self.assertEqual(s["original_role_or_event_components"],
                                 source_components(domain,source))
                self.assertEqual(s["source_feature"],base["feature"])
                self.assertEqual(s["source_semantic_scope"],SCOPE[domain][int(row["variant"])-1][0])
                self.assertTrue(s["semantic_roles_are_from_original_english_scenario"])
                self.assertTrue(s["source_assertion_derived_not_backward_parsed"])
                self.assertFalse(s["speaker_human_attestation"])
                self.assertEqual(s["english_to_qaroshi_equivalence"],"not verified")
                self.assertEqual(row["scope_operator_9_2_audit"],"bounded_form_checks_passed")
                self.assertEqual(row["independent_semantic_equivalence"],"unadjudicated")
                self.assertFalse(row["external_human_paraphrase"])
                self.assertFalse(row["external_reviewer_id"])
                self.assertEqual(row["authoritative_native_grammar_attestation"],"no")

    def test_explicit_truth_and_nonentailments_are_domain_specific(self):
        for row in self.ledger:
            x=json.loads(row["source_semantic_intent_json"])
            v=int(row["variant"])
            domain=row["domain"]
            if domain=="social_consent":
                self.assertFalse(x["implied_permission_from_silence"])
                self.assertFalse(x["requested_action_occurrence_entailed"])
                self.assertEqual(x["earlier_specific_grant_and_later_revocation_asserted"],v==5)
            if domain=="technical_precision":
                self.assertFalse(x["unsupported_q_asserted_false"])
                self.assertFalse(x["unsupported_q_proved_by_p"])
            if domain=="evidentiality":
                self.assertFalse(x["embedded_event_negated_by_matrix"])
            if domain=="counterfactual_modal":
                self.assertFalse(x["hypothetical_result_occurred_asserted"])
            if domain=="narrative_figures":
                self.assertFalse(x["literal_metaphor_occurred_in_actual_world"])
            if domain=="voice_valency":
                self.assertFalse(x["instrument_is_agent"])
                self.assertEqual(x["overt_passive_agent_required"],v in (2,5))
            if domain=="time_motion":
                self.assertEqual(x["both_events_asserted"],v in (1,2,3,4))
                self.assertEqual(x["later_event_asserted_despite_negated_preboundary"],v==4)

    def test_one_versioned_9_2_repair_not_190_fabricated_corrections(self):
        modified=[r for r in self.ledger if r["9_2_versioned_correction_reason"]]
        self.assertEqual(len(modified),1)
        self.assertEqual(modified[0]["id"],"QS81-0336")
        self.assertTrue(modified[0]["prior_9_1_original"].endswith("-te."))
        self.assertTrue(modified[0]["current_9_2_qaroshi_candidate"].endswith(" qinë."))
        for r in self.independent:
            self.assertFalse(r["without_english_reader_paraphrase"])
            self.assertFalse(r["reader_id"])
            self.assertFalse(r["reviewer_score"])
            self.assertFalse(r["reviewer_notes"])

if __name__=="__main__":unittest.main()
