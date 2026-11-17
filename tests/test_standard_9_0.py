"""Standard 9.0 source and compositional semantic-scope tests, not speaker attestation."""
from __future__ import annotations
import csv,json,unittest
from pathlib import Path
from tools.stress90.compose import build,rows,proposals,read
from tools.stress90.consent import compose as ccompose,semantic_record
from tools.stress90.relatives import compose as rcompose,semantics

ROOT=Path(__file__).resolve().parents[1]

class Standard90(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary=build()
        cls.cases={x["id"]:x for x in rows(ROOT/"data/stress90/case_evidence_500.csv")}
        cls.previous={x["id"]:x for x in rows(ROOT/"data/stress89/case_evidence_500.csv")}
        cls.source={x["id"]:x for x in rows(ROOT/"data/stress81/challenges_500.csv")}
        cls.consent=read("consent_action_frames_8_9.json")
        cls.relatives=read("relative_frames_9_0.json")
        with (ROOT/"data/lexicon.csv").open(encoding="utf8",newline="") as fp:
            cls.lex={x["id"]:x for x in csv.DictReader(fp)}

    def test_exact_500_items_preservation_and_unverified_status(self):
        a=self.summary
        self.assertEqual(a["fixed_challenges"],500)
        self.assertEqual(a["original_8_9_editorial_draft_count"],190)
        self.assertEqual(a["total_editorial_drafts"],190+a["9_0_new_full_editorial_draft_count"])
        self.assertEqual(a["total_editorial_drafts"]+a["remaining_no_complete_draft"],500)
        self.assertFalse(a["certified_general_language_completeness"])
        self.assertEqual(a["independent_human_comprehension"],0)
        self.assertEqual(a["independent_human_backtranslations"],0)
        self.assertEqual(len(self.cases),500)
        for id_,r in self.cases.items():
            old=self.previous[id_]
            self.assertEqual(r["english"],self.source[id_]["english"])
            self.assertEqual(r["prior_8_9_candidate"],old["qaroshi_full_candidate"])
            self.assertEqual(r["independently_semantically_verified"],"no")
            self.assertEqual(r["human_backtranslation"],"not performed")
            self.assertEqual(r["external_comprehension"],"not performed")
            if old["qaroshi_full_candidate"]:
                self.assertEqual(r["qaroshi_full_candidate"],old["qaroshi_full_candidate"])
                self.assertEqual(r["candidate_status"],old["candidate_status"])
            if not r["qaroshi_full_candidate"]:
                self.assertEqual(r["edition_9_0_witness_ids"],"")

    def test_consent_rejection_is_explicitly_not_assent(self):
        self.assertEqual(len(self.consent),8)
        for f in self.consent:
            for variant in (4,5):
                key=f"QS81-{100+(f['family']-1)*5+variant:04d}"
                row=self.cases[key]
                qr=ccompose(f,variant)
                self.assertEqual(qr,row["qaroshi_full_candidate"])
                self.assertEqual(row["candidate_status"],"9_0_explicit_no_inferred_consent_or_action_specific_revocation")
                self.assertEqual(qr.count("sen "),2)
                self.assertEqual(qr.count("."),2)
                s=json.loads(row["edition_9_0_semantic_signature_json"])
                self.assertFalse(s["target_action_occurred_asserted"])
                self.assertFalse(s["permission_granted_by_silence"])
                self.assertEqual(s["actor"],f["actor"])
                self.assertEqual(s["other"],f["other"])
                if variant==4:
                    self.assertEqual(s["speech_act"],"reject_silent_permission_inference")
                    self.assertTrue(s["silent_departure_asserted"])
                    self.assertIn(f["other"]+" shëlahe dëru-te.",qr)
                    self.assertIn(f["actor"]+" nu shërawë-te.",qr)
                    self.assertNotIn("kele yu",qr)
                else:
                    self.assertEqual(s["speech_act"],"withdraw_action_specific_consent")
                    self.assertTrue(s["grant_earlier_asserted"])
                    self.assertTrue(s["withdrawal_asserted"])
                    self.assertTrue(s["opportunity_boundary_not_act_assertion"])
                    self.assertIn(" maho-m hëzhohe-te.",qr)
                    self.assertIn(" dëna maho-m keleyu-te.",qr)
                    self.assertIn("-ki-te",qr)
                    self.assertNotIn(f["actor"]+" {f['action']}-te.",qr)

    def test_relative_gap_roles_and_speaker_attitudes(self):
        self.assertEqual(len(self.relatives),5)
        for f in self.relatives:
            self.assertFalse(f["human_attested"])
            self.assertIn(f["head_gap_role"],("relative_subject","relative_patient"))
            self.assertEqual(self.lex[f["head_id"]]["qaroshi"],f["head"])
            self.assertEqual(self.lex[f["head_id"]]["pos"],"n")
            self.assertIn(" sha",f["relative_clause"])
            self.assertIn(f["relative_clause"],f["matrix_event"])
            # All source references are canonical ids, never invented Q ids.
            for id_ in set(f["source_ids"]+f.get("consequence_source_ids",[])+f.get("reason_ids",[])):
                self.assertIn(id_,self.lex,(f["id"],id_))
            for variant in range(1,6):
                key=f"QS81-{250+(f['family']-1)*5+variant:04d}"
                expected=rcompose(f,variant)
                row=self.cases[key]
                self.assertEqual(row["qaroshi_full_candidate"],expected or "")
                if expected is None:continue
                signature=json.loads(row["edition_9_0_semantic_signature_json"])
                self.assertEqual(signature["head_gap_role"],f["head_gap_role"])
                self.assertTrue(signature["relative_gap_belongs_to_head"])
                self.assertEqual(signature["truth_of_matrix_event_asserted"],variant in (1,5))
                self.assertEqual(signature["causal_reason_asserted"],True if variant==5 else None)
                if variant==2:
                    self.assertTrue(expected.endswith(" do mi tëmiro-te."))
                    self.assertFalse(signature["truth_of_matrix_event_asserted"])
                if variant==3:
                    self.assertTrue(expected.endswith(" he do mi nu sëmi."))
                    self.assertFalse(signature["truth_of_matrix_event_asserted"])
                if variant==4:
                    self.assertTrue(expected.startswith("sen wë "))
                    self.assertTrue(expected.endswith(f["conditional_consequence"]+"."))
                    self.assertFalse(signature["conditional_antecedent_asserted"])
                if variant==5:
                    self.assertTrue(expected.endswith(" ro "+f["reason"]+"."))
                    self.assertTrue(signature["causal_reason_asserted"])

    def test_technical_p_is_not_equated_with_report_possible_or_proof(self):
        from tools.stress81.scenarios import TECH
        from tools.stress90.technical import compose as tcompose
        tech=read("technical_propositions_9_0.json")
        self.assertEqual(len(tech),5)
        for f in tech:
            self.assertEqual(f["english_claim"],TECH[f["family"]-1][0])
            self.assertTrue(f["decision"])
            self.assertTrue(f["risk"])
            for source_id in f["p_ids"]+f["recommendation_ids"]+f["unsupported_ids"]:
                self.assertIn(source_id,self.lex,(f["id"],source_id))
            for variant in range(1,6):
                row=self.cases[f"QS81-{450+(f['family']-1)*5+variant:04d}"]
                qr=tcompose(f,variant)
                self.assertEqual(row["qaroshi_full_candidate"],qr or "")
                if not qr:continue
                sig=json.loads(row["edition_9_0_semantic_signature_json"])
                self.assertEqual(sig["proposition_asserted_by_main_speaker"],variant==5)
                self.assertFalse(sig["unsupported_q_asserted_false"])
                self.assertEqual(row["candidate_status"],
                    "9_0_technical_reporting_unverified_possibility_or_nonentailment")
                if variant==1:
                    self.assertTrue(qr.endswith("do zhikasasho shërawëhu-te."))
                elif variant==2:
                    self.assertTrue(qr.endswith("do larëno subali-mi khunikhu-te."))
                elif variant==3:
                    self.assertTrue(sig["lack_of_independent_verification_asserted"])
                    self.assertIn(" do këraro nao ",qr)
                    self.assertIn(" tequyu nu shërawëhe-li-te.",qr)
                elif variant==4:
                    self.assertTrue(sig["condition_is_hypothetical"])
                    self.assertTrue(qr.startswith("sen wë "+f["p"]+", "))
                    self.assertTrue(qr.endswith("-du."))
                    self.assertFalse(sig["recommendation_act_occurred"])
                elif variant==5:
                    self.assertTrue(sig["only_p_as_premise"])
                    self.assertTrue(sig["unsupported_q_does_not_follow_from_p"])
                    self.assertTrue(qr.startswith("sen "+f["p"]+". sen "+f["p"]+" do ngëshi zhëwëra, "))
                    self.assertTrue(qr.endswith(" do zotenga nu eri."))
                    self.assertEqual(qr.count("sen "),2)
                    self.assertNotIn("nu "+f["unsupported"].split()[-1]+".",qr)

    def test_old_cases_stay_unfilled_unless_specific_new_9_0_license(self):
        allowed=set(proposals())
        self.assertEqual(allowed,{id_ for id_,r in self.cases.items() if r["edition_9_0_witness_ids"]})
        self.assertEqual(len(allowed),self.summary["9_0_new_full_editorial_draft_count"])
        for family in (2,3,6,7,10):
            for variant in range(1,6):
                id_=f"QS81-{250+(family-1)*5+variant:04d}"
                self.assertEqual(self.cases[id_]["qaroshi_full_candidate"],"")
        for family in (6,9):
            for variant in range(1,6):
                id_=f"QS81-{100+(family-1)*5+variant:04d}"
                self.assertEqual(self.cases[id_]["qaroshi_full_candidate"],"")

if __name__=="__main__":
    unittest.main()
