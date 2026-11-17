"""Qaroshi 8.9: evidence-linked additions and unverified-135 blind packet."""
from __future__ import annotations
import csv
import json
import unittest
from collections import Counter
from pathlib import Path
from tools.stress89.compose import build, evidence, rows
from tools.stress89.audit import run as audit

ROOT=Path(__file__).resolve().parents[1]
STD=ROOT/"data/standard_8"

def source(name):
    return json.loads((STD/name).read_text(encoding="utf8"))

class Standard89(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=build()
        cls.audit=audit()
        cls.cases={x["id"]:x for x in rows(ROOT/"data/stress89/case_evidence_500.csv")}
        cls.original={x["id"]:x for x in rows(ROOT/"data/stress81/challenges_500.csv")}
        cls.old={x["id"]:x for x in rows(ROOT/"data/stress88/case_evidence_500.csv")}
        cls.evidential=source("evidential_propositions_8_9.json")
        cls.temporal=source("motion_frames_8_9.json")
        cls.misc=source("conditional_and_voice_8_9.json")
        with (ROOT/"data/lexicon.csv").open(encoding="utf8",newline="") as f:
            cls.lex={r["id"]:r for r in csv.DictReader(f)}

    def test_all_cases_accounted_no_human_fabrication(self):
        s=self.report
        self.assertEqual(s["challenge_count"],500)
        self.assertEqual(s["previous_8_8_editorial_candidates"],135)
        self.assertGreaterEqual(s["new_8_9_editorial_candidates"],20)
        self.assertEqual(s["total_8_9_editorial_candidates"],135+s["new_8_9_editorial_candidates"])
        self.assertEqual(s["challenges_still_without_full_draft"],500-s["total_8_9_editorial_candidates"])
        self.assertFalse(s["all_challenges_solved"])
        self.assertEqual(s["independent_human_comprehension"],0)
        self.assertEqual(s["independent_human_backtranslations"],0)
        self.assertEqual(len(self.cases),500)
        for key,item in self.cases.items():
            self.assertEqual(item["english"],self.original[key]["english"])
            self.assertEqual(item["prior_8_8_candidate"],self.old[key]["qaroshi_full_candidate"])
            self.assertEqual(item["external_comprehension"],"not performed")
            self.assertEqual(item["human_backtranslation"],"not performed")
            self.assertEqual(item["independently_semantically_verified"],"no")

    def test_social_consent_three_scopes_for_eight_individual_action_frames(self):
        from tools.stress89.compose import consent_action
        from tools.stress81.scenarios import SOCIAL
        frames=source("consent_action_frames_8_9.json")
        self.assertEqual(len(frames),8)
        self.assertEqual(len({x["family"] for x in frames}),8)
        self.assertEqual({x["family"] for x in frames},{1,2,3,4,5,7,8,10})
        for frame in frames:
            with self.subTest(frame=frame["id"]):
                actor_english,other_english,action_english=SOCIAL[frame["family"]-1]
                self.assertTrue(actor_english.startswith("the "))
                self.assertTrue(other_english.startswith("the "))
                self.assertEqual(frame["licensed_variants"],[1,2,3])
                self.assertFalse(frame["human_attested"])
                if frame.get("actor_id"):
                    self.assertEqual(self.lex[frame["actor_id"]]["qaroshi"],frame["actor"])
                    self.assertEqual(self.lex[frame["actor_id"]]["pos"],"n")
                else:
                    self.assertEqual(frame["actor"],frame["actor_base"]+"-sharo")
                    self.assertEqual(self.lex[frame["actor_base_id"]]["qaroshi"],frame["actor_base"])
                    self.assertEqual(self.lex[frame["actor_base_id"]]["pos"],"v")
                self.assertEqual(self.lex[frame["other_id"]]["qaroshi"],frame["other"])
                for ident in frame["action_ids"]:
                    self.assertIn(ident,self.lex)
                for variant in (1,2,3):
                    itemid=f"QS81-{100+(frame['family']-1)*5+variant:04d}"
                    row=self.cases[itemid]
                    qr=consent_action(frame,variant)
                    self.assertEqual(row["qaroshi_full_candidate"],qr)
                    self.assertEqual(row["candidate_status"],"8_9_licensed_permission_request_or_refusal_editorial")
                    signature=json.loads(row["edition_8_9_semantic_signature_json"])
                    self.assertEqual(signature["question_actor"],frame["actor"])
                    self.assertEqual(signature["permission_addressee"],frame["other"])
                    self.assertFalse(signature["action_already_performed"])
                    self.assertFalse(signature["permission_granted_or_inferred"])
                    self.assertTrue(signature["negative_reply_did_not_assert_action_failure"])
                    if variant==1:
                        self.assertIn("-ho he do",qr)
                        self.assertIn(frame["other"]+"-tu sharoa-te",qr)
                        self.assertEqual(signature["kind"],"asked_permission")
                    elif variant==2:
                        self.assertIn("yaro ",qr)
                        self.assertIn("toru «nu.» shiri-te.",qr)
                        self.assertEqual(signature["kind"],"explicit_negative_reply")
                    else:
                        self.assertIn(" do "+frame["actor"]+" "+frame["other"]+"-tu pëli-te nao ",qr)
                        self.assertTrue(qr.endswith(frame["other"]+" noharo-te."))
                        self.assertEqual(signature["kind"],"offered_action_then_refused")
                for variant in (4,5):
                    itemid=f"QS81-{100+(frame['family']-1)*5+variant:04d}"
                    self.assertEqual(self.cases[itemid]["qaroshi_full_candidate"],"")
        for family in (6,9):
            for variant in (1,2,3,4,5):
                key=f"QS81-{100+(family-1)*5+variant:04d}"
                self.assertEqual(self.cases[key]["qaroshi_full_candidate"],"")

    def test_social_roles_are_not_interchangeable(self):
        from tools.stress89.compose import consent_action
        frames=source("consent_action_frames_8_9.json")
        for f in frames:
            original=consent_action(f,1)
            swap={**f,"actor":f["other"],"other":f["actor"]}
            self.assertNotEqual(original,consent_action(swap,1))
            self.assertNotIn(" toru «nu.»",original)
            self.assertTrue(consent_action(f,2).endswith("toru «nu.» shiri-te."))
            self.assertNotIn(" noharo-te.",original)
            self.assertEqual(self.cases[
                f"QS81-{100+(f['family']-1)*5+1:04d}"]["human_backtranslation"],"not performed")

    def test_evidential_event_lexical_source_ids(self):
        self.assertEqual(len(self.evidential),5)
        for p in self.evidential:
            for role,pos in (("actor","n"),("verb","v"),("patient","n")):
                id_=p.get(role+"_id")
                if id_:
                    src=self.lex[id_]
                    self.assertEqual(src["qaroshi"],p[role])
                    self.assertEqual(src["pos"],pos)
            for variant in range(1,5):
                id_=f"QS81-{200+(p['family']-1)*5+variant:04d}"
                item=self.cases[id_]
                generated=evidence(p,variant)
                self.assertEqual(item["qaroshi_full_candidate"],generated)
                self.assertEqual(item["candidate_status"],"8_9_evidential_editorial_composition")
                sig=json.loads(item["edition_8_9_semantic_signature_json"])
                self.assertEqual(sig["matrix_polar_knowledge_negated"],variant==4)
                if variant==1:
                    self.assertTrue(generated.endswith(" si."))
                    self.assertNotIn(" hu",generated)
                elif variant==2:
                    self.assertIn(" do yano mi-tu shiri-te.",generated)
                    self.assertFalse(sig["embedded_event_entailed"])
                elif variant==3:
                    self.assertTrue(generated.endswith(" ye."))
                elif variant==4:
                    self.assertTrue(generated.endswith(" he do mi nu sëmi."))
                    self.assertFalse(sig["embedded_event_entailed"])

    def test_no_report_is_not_report_of_a_negative(self):
        from tools.stress81.scenarios import EVIDENCE
        items=source("epistemic_nonassertions_8_9.json")
        self.assertEqual(len(items),7)
        for entry in items:
            self.assertEqual(entry["alternative"],EVIDENCE[entry["family"]-1][1])
            for ident in entry["source_ids"]:
                self.assertIn(ident,self.lex)
            id_=f"QS81-{200+(entry['family']-1)*5+5:04d}"
            row=self.cases[id_]
            text=row["qaroshi_full_candidate"]
            self.assertEqual(text,f"sen {entry['event_clause']} do mi nu shërawëhu.")
            self.assertEqual(row["candidate_status"],"8_9_explicit_negative_claim_scope_editorial")
            self.assertNotIn("nu "+entry["event_clause"].split()[-1],text)
            signature=json.loads(row["edition_8_9_semantic_signature_json"])
            self.assertTrue(signature["matrix_reporting_negated"])
            self.assertFalse(signature["embedded_event_asserted"])
            self.assertFalse(signature["embedded_event_negated"])
            self.assertEqual(signature["speaker_position_on_event_truth"],"unspecified")
        roots={(r["qaroshi"],r["pos"]) for r in self.lex.values()}
        self.assertIn(("naroaro","n"),roots)
        self.assertIn(("gura","v"),roots)

    def test_temporal_roles_and_real_question_scope(self):
        self.assertEqual(len(self.temporal),3)
        for f in self.temporal:
            for token,ident in (
                ("actor","actor_id"),("object","object_id"),("event_verb","event_verb_id"),
                ("related_actor","related_actor_id"),("related_verb","related_verb_id"),
                ("boundary_actor","boundary_actor_id"),("boundary_verb","boundary_verb_id")
            ):
                if f.get(ident):
                    self.assertEqual(self.lex[f[ident]]["qaroshi"],f[token])
            for variant,qaroshi in f["candidates"].items():
                key=f"QS81-{50+(f['family']-1)*5+int(variant):04d}"
                row=self.cases[key]
                self.assertEqual(row["qaroshi_full_candidate"],qaroshi)
                self.assertIn(row["candidate_status"],["8_9_temporal_two_event_editorial"])
                self.assertEqual(qaroshi.count(","),1)
                self.assertIn(" ",qaroshi)
                if int(variant)==1:
                    self.assertTrue(qaroshi.startswith("sen ana "))
                elif int(variant)==2:
                    self.assertTrue(qaroshi.startswith("sen ëna "))
                elif int(variant)==3:
                    self.assertTrue(qaroshi.startswith("sen yaro "))
                elif int(variant)==5:
                    self.assertTrue(qaroshi.startswith("hë ëna "))
                    self.assertTrue(qaroshi.endswith(" he?"))
        self.assertEqual(self.cases["QS81-0054"]["qaroshi_full_candidate"],"")
        self.assertEqual(self.cases["QS81-0059"]["qaroshi_full_candidate"],"")
        self.assertEqual(self.cases["QS81-0084"]["qaroshi_full_candidate"],"")

    def test_counterfactual_and_anaphoric_patient(self):
        for item in self.misc["counterfactuals"]:
            row=self.cases[f"QS81-{(item['daily_family']-1)*5+5:04d}"]
            self.assertEqual(row["qaroshi_full_candidate"],item["qaroshi"])
            self.assertEqual(row["english"],item["english"])
            self.assertIn("wënu ",row["qaroshi_full_candidate"])
            self.assertTrue(row["qaroshi_full_candidate"].endswith(" qinë."))
            sig=json.loads(row["edition_8_9_semantic_signature_json"])
            self.assertTrue(sig["antecedent_nonactual"])
            self.assertFalse(sig["consequent_asserted_actual"])
            if item["daily_family"]==1:
                self.assertEqual(row["qaroshi_full_candidate"].count("gëla-m"),2)

    def test_voice_roles_specific_but_instrument_not_guessed(self):
        x=self.misc["additional_voice"]
        self.assertEqual(self.lex[x["actor_base_id"]]["qaroshi"],x["actor_base"])
        self.assertEqual(self.lex[x["patient_id"]]["qaroshi"],x["patient"])
        self.assertEqual(self.lex[x["verb_id"]]["qaroshi"],x["verb"])
        for variant,qr in x["candidates"].items():
            row=self.cases[f"QS81-{350+(x['voice_family']-1)*5+int(variant):04d}"]
            self.assertEqual(row["qaroshi_full_candidate"],qr)
            if int(variant) in (2,5):
                self.assertIn(x["actor"]+"-za",qr)
                self.assertIn(x["verb"]+"-li-te",qr)
            if int(variant)==4:self.assertIn(" nu "+x["verb"]+"-te",qr)
        self.assertEqual(self.cases["QS81-0388"]["qaroshi_full_candidate"],"")
        for instrument in self.misc["additional_instruments"]:
            row=self.cases[f"QS81-{350+(instrument['voice_family']-1)*5+3:04d}"]
            self.assertEqual(row["qaroshi_full_candidate"],instrument["qaroshi"])
            self.assertEqual(self.lex[instrument["instrument_id"]]["qaroshi"],instrument["instrument"])
            self.assertIn(instrument["instrument"]+"-shi",row["qaroshi_full_candidate"])
            self.assertNotIn("-za",row["qaroshi_full_candidate"])

    def test_blind_instrument_keeps_answer_key_and_false_claims_apart(self):
        self.assertEqual(self.audit["existing_8_8_candidate_count"],135)
        self.assertEqual(self.audit["external_participants"],0)
        self.assertEqual(self.audit["external_responses"],0)
        self.assertEqual(self.audit["meaning_independently_validated"],0)
        public=rows(ROOT/"data/stress89/blind_qaroshi_prompts_135.csv")
        private=rows(ROOT/"data/stress89/separate_answer_key_135.csv")
        review=rows(ROOT/"data/stress89/all_candidate_form_audit_500.csv")
        self.assertEqual(len(public),len(private))
        self.assertEqual(len(public),135)
        self.assertEqual(len(review),500)
        self.assertTrue(all("english_target" not in x and
                            "original_english_target" not in x for x in public))
        self.assertTrue(all(not x["participant_response"] and
                            not x["informed_consent_record"] for x in public))
        self.assertTrue(all(x["exact_meaning_human_verified"]=="no" and
                            x["true_translation_certified"]=="no" for x in review))
        self.assertEqual({r["id"] for r in public},{r["id"] for r in private})

    def test_original_135_review_flags_are_not_hidden_or_counted_as_verified(self):
        statuses=self.audit["candidate_structural_review_statuses"]
        self.assertEqual(statuses["review_flagged"],3)
        self.assertEqual(statuses["exact_8_8_structural_model_match_not_semantic_verification"],61)
        self.assertEqual(statuses["limited_quantifier_rule_check_without_external_comprehension"],49)
        self.assertEqual(statuses["form_only_not_independently_semantically_checked"],22)
        original_reviews=rows(ROOT/"data/stress89/all_candidate_form_audit_500.csv")
        flags={r["id"] for r in original_reviews if r["formal_review"]=="review_flagged"}
        self.assertEqual(flags,{"QS81-0202","QS81-0222","QS81-0227"})
        for id_ in flags:
            before=self.old[id_]["qaroshi_full_candidate"]
            after=self.cases[id_]["qaroshi_full_candidate"]
            self.assertNotEqual(before,after)
            self.assertIn("do yano mi-tu shiri-te",after)
            self.assertNotIn("do yano mi-tu shiri-te",before)
            self.assertEqual(self.cases[id_]["independently_semantically_verified"],"no")

    def test_every_new_source_witness_has_a_real_dictionary_id(self):
        # Editorial decision IDs are namespaced and are not dictionary lemmas.
        for item in self.cases.values():
            if not item["edition_8_9_specific_witnesses"]:continue
            for witness in item["edition_8_9_specific_witnesses"].split(" | "):
                if witness.startswith("Q"):
                    self.assertIn(witness,self.lex, (item["id"],witness))


if __name__=="__main__":
    unittest.main()
