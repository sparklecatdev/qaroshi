"""9.1: all original 500 editorial drafts, source-linked case grammar and no inflated attestation."""
from __future__ import annotations
import csv,json,re,unittest
from collections import Counter
from pathlib import Path
from tools.stress91.compose import build,rows,proposals,EXPECTED,BASES,challenge_id,predicate_negative
from tools.stress91.compose import STD,OUT
from tools.stress90.compose import rows as oldrows

ROOT=Path(__file__).resolve().parents[1]

class Standard91(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=build()
        cls.original={r["id"]:r for r in rows(ROOT/"data/stress81/challenges_500.csv")}
        cls.previous={r["id"]:r for r in rows(ROOT/"data/stress90/case_evidence_500.csv")}
        cls.ledger={r["id"]:r for r in rows(OUT/"case_evidence_500.csv")}
        cls.proposed=proposals()
        with (ROOT/"data/lexicon.csv").open(encoding="utf8",newline="") as fp:
            cls.canon={r["id"]:r for r in csv.DictReader(fp)}
        cls.lexoverlay=json.loads((STD/"editorial_lexicon_9_1.json").read_text(encoding="utf8"))
        cls.overlay={r["id"]:r for r in cls.lexoverlay["entries"]}

    def test_exact_500_no_unresolved_drafts_without_fabricating_readers(self):
        r=self.report
        self.assertEqual(r["frozen_english_challenges"],500)
        self.assertEqual(r["inherited_9_0_draft_count"],318)
        self.assertEqual(r["new_9_1_draft_count"],182)
        self.assertEqual(r["all_full_editorial_candidate_strings"],500)
        self.assertEqual(r["no_complete_editorial_draft"],0)
        self.assertEqual(r["new_editorial_drafts_by_domain"],EXPECTED)
        self.assertEqual(len(self.ledger),500)
        self.assertEqual(len(self.proposed),182)
        self.assertEqual(r["independent_backtranslations"],0)
        self.assertEqual(r["independent_comprehension_trials"],0)
        self.assertEqual(r["certified_english_qaroshi_equivalence_count"],0)
        self.assertFalse(r["full_natural_language_functionality_established"])
        self.assertFalse(r["frozen_reference_files_modified"])

    def test_exact_318_prior_editions_untouched_and_original_english_fixed(self):
        for id_,r in self.ledger.items():
            self.assertEqual(r["english"],self.original[id_]["english"])
            self.assertEqual(r["prior_9_0_candidate"],self.previous[id_]["qaroshi_full_candidate"])
            self.assertEqual(r["independently_semantically_verified"],"no")
            self.assertEqual(r["human_backtranslation"],"not performed")
            self.assertEqual(r["external_comprehension"],"not performed")
            self.assertTrue(r["qaroshi_full_candidate"])
            if self.previous[id_]["qaroshi_full_candidate"]:
                self.assertEqual(r["qaroshi_full_candidate"],
                                 self.previous[id_]["qaroshi_full_candidate"])
                self.assertEqual(r["edition_9_1_source_ids"],"")
                self.assertEqual(r["candidate_status"],self.previous[id_]["candidate_status"])
            else:
                self.assertIn(id_,self.proposed)
                self.assertNotEqual(r["edition_9_1_source_ids"],"")
                self.assertEqual(r["candidate_status"],
                    "9_1_full_editorial_licensed_composition_pending_human_review")
                sig=json.loads(r["edition_9_1_semantic_signature_json"])
                self.assertEqual(sig["independent_reader_count"],0)
                self.assertEqual(sig["status"],"editorial, not independently attested")

    def test_canonical_and_9_1_source_ids_exist_and_were_not_invented(self):
        self.assertEqual(self.lexoverlay["immutable_source_lexicon"],True)
        for id_,p in self.proposed.items():
            for sourceid in p["source_ids"]:
                if sourceid.startswith("Q"):
                    self.assertIn(sourceid,self.canon,(id_,sourceid))
                elif sourceid.startswith("X91-"):
                    self.assertIn(sourceid,self.overlay,(id_,sourceid))
                    self.assertNotEqual(self.overlay[sourceid].get("status"),"not_adopted")
                else:
                    self.fail(f"Unreviewed source type {id_} {sourceid!r}")
        for x in self.overlay.values():
            for sourceid in x["source_ids"]:
                self.assertIn(sourceid,self.canon,(x["id"],sourceid))
            self.assertFalse(x["independently_attested"])
            self.assertTrue(x["definition"])
        self.assertEqual(len(self.overlay),len({x["form"] for x in self.overlay.values()}))
        self.assertTrue(all(" " not in x["form"] for x in self.overlay.values()))

    def test_new_editorial_lexemes_are_not_silently_renamed_or_attested(self):
        forms={x["form"] for x in self.overlay.values() if x.get("status")!="not_adopted"}
        self.assertIn("gëngora",forms)
        self.assertIn("shëwarono",forms)
        self.assertIn("gëru-yëla",forms)
        self.assertIn("shiralë",forms)
        self.assertIn("nohowa-bekega",forms)
        rejected={x["form"] for x in self.overlay.values() if x.get("status")=="not_adopted"}
        self.assertEqual(rejected,{"pënaro-m","punushu-shi","tësaro-ma","shënoho-qano"})
        self.assertTrue(all(not x["independently_attested"] for x in self.overlay.values()))

    def test_daily_tense_polar_and_reported_speech(self):
        f=json.loads((STD/"daily_frames_9_1.json").read_text(encoding="utf8"))
        assert len(f)==8
        for x in f:
            for v in x["variants"]:
                id_=challenge_id("daily",x["family"],v)
                r=self.ledger[id_]
                s=json.loads(r["edition_9_1_semantic_signature_json"])
                self.assertEqual(s["actual_positive_event_asserted"],v==1)
                self.assertEqual(s["negated_event_asserted"],v==2)
                self.assertEqual(s["third_party_report_not_narrator_verified"],v==4)
                self.assertEqual(s["counterfactual_not_actual_outcome"],v==5)
                if v==1:self.assertTrue(r["qaroshi_full_candidate"].endswith("-te."))
                if v==2:self.assertIn(" nu "+x["verb"]+"-te.",r["qaroshi_full_candidate"])
                if v==3:
                    self.assertTrue(r["qaroshi_full_candidate"].startswith("hë "))
                    self.assertTrue(r["qaroshi_full_candidate"].endswith(" he?"))
                if v==4:self.assertTrue(r["qaroshi_full_candidate"].endswith(" do yano mi-tu shiri-te."))
                if v==5:
                    self.assertIn("wënu ",r["qaroshi_full_candidate"])
                    self.assertIn(x["consequence"]+" qinë.",r["qaroshi_full_candidate"])

    def test_not_until_includes_real_later_event_and_does_not_infer_causation(self):
        frames=json.loads((STD/"motion_frames_9_1.json").read_text(encoding="utf8"))
        self.assertEqual(len(frames),10)
        self.assertEqual(sum(len(x["variants"]) for x in frames),41)
        for f in frames:
            for v in f["variants"]:
                qr=self.ledger[challenge_id("time_motion",f["family"],v)]["qaroshi_full_candidate"]
                s=json.loads(self.ledger[challenge_id("time_motion",f["family"],v)]
                             ["edition_9_1_semantic_signature_json"])
                self.assertTrue(s["unasserted_causation"])
                self.assertEqual(s["positive_main_event_asserted"],v!=5)
                if v==4:
                    self.assertTrue(s["same_endpoint_repeated_once_in_same_discourse"])
                    self.assertEqual(qr,f"sen torëne {f['before']}, {predicate_negative(f['main'])}. "
                                         f"sen ana {f['before']}, {f['main']}.")
                    self.assertIn(" nu ",qr.split(".")[0])
                    self.assertTrue(qr.endswith(f["main"]+"."))
                if v==5:
                    self.assertTrue(qr.startswith("hë ëna "))
                    self.assertTrue(qr.endswith(" he?"))
                if v==3:self.assertIn("sen yaro "+f["after"]+", ",qr)

    def test_two_new_consent_families_cover_five_speech_act_scopes(self):
        frames=json.loads((STD/"consent_frames_9_1.json").read_text(encoding="utf8"))
        self.assertEqual({f["family"] for f in frames},{6,9})
        for f in frames:
            for v in range(1,6):
                row=self.ledger[challenge_id("social_consent",f["family"],v)]
                qr=row["qaroshi_full_candidate"]
                s=json.loads(row["edition_9_1_semantic_signature_json"])
                self.assertEqual(s["actor"],f["actor"])
                self.assertEqual(s["addressee"],f["other"])
                self.assertFalse(s["action_occurred_asserted"])
                self.assertTrue(s["permission_not_inferred_from_silence"])
                if v==1:self.assertIn("-ho he do",qr)
                if v==2:self.assertIn("«nu.»",qr)
                if v==3:self.assertIn("noharo-te.",qr)
                if v==4:self.assertIn(" nu shërawë-te.",qr)
                if v==5:
                    self.assertIn(" maho-m hëzhohe-te.",qr)
                    self.assertIn(" maho-m keleyu-te.",qr)

    def test_evidence_source_identity_and_matrix_nonassertion(self):
        cases=json.loads((STD/"evidential_frames_9_1.json").read_text(encoding="utf8"))
        self.assertEqual(len(cases["events"]),5)
        self.assertEqual(len(cases["nonassertions"]),3)
        for f in cases["events"]:
            self.assertEqual(f["variants"],[1,2,3,4])
            if f["verb_id"].startswith("Q"):
                self.assertEqual(self.canon[f["verb_id"]]["qaroshi"],f["verb"],f["id"])
            for v in f["variants"]:
                row=self.ledger[challenge_id("evidentiality",f["family"],v)]
                self.assertIn(f["clause"],row["qaroshi_full_candidate"])
                if v==1:self.assertTrue(row["qaroshi_full_candidate"].endswith(" si."))
                if v==2:self.assertTrue(row["qaroshi_full_candidate"].endswith(" do yano mi-tu shiri-te."))
                if v==4:self.assertTrue(row["qaroshi_full_candidate"].endswith(" he do mi nu sëmi."))
        for f in cases["nonassertions"]:
            row=self.ledger[challenge_id("evidentiality",f["family"],5)]
            self.assertTrue(row["qaroshi_full_candidate"].endswith(" do mi nu shërawëhu."))
            self.assertIn(f["event_clause"],row["qaroshi_full_candidate"])
            s=json.loads(row["edition_9_1_semantic_signature_json"])
            self.assertFalse(s["alternative_explicitly_negated"])

    def test_reference_relative_head_gap_polarity_is_fixed(self):
        frames=json.loads((STD/"relative_frames_9_1.json").read_text(encoding="utf8"))
        self.assertEqual(len(frames),8)
        for f in frames:
            for v in f["variants"]:
                row=self.ledger[challenge_id("embedding_reference",f["family"],v)]
                qr=row["qaroshi_full_candidate"]
                self.assertIn(" sha",qr)
                s=json.loads(row["edition_9_1_semantic_signature_json"])
                self.assertTrue(s["relative_gap_belongs_to_head"])
                if v==2:self.assertTrue(qr.endswith(" do mi tëmiro-te."))
                if v==3:self.assertTrue(qr.endswith(" he do mi nu sëmi."))
                if v==4:
                    self.assertTrue(qr.startswith("sen wë "))
                    self.assertFalse(s["conditional_antecedent_asserted"])
                if v==5:
                    self.assertIn(" ro ",qr)
                    self.assertTrue(s["causal_reason_asserted"])

    def test_seven_modal_families_and_distinct_realities(self):
        frames=json.loads((STD/"modal_frames_9_1.json").read_text(encoding="utf8"))
        self.assertEqual(len(frames),7)
        for f in frames:
            qr=[]
            for v in f["variants"]:
                row=self.ledger[challenge_id("counterfactual_modal",f["family"],v)]
                s=json.loads(row["edition_9_1_semantic_signature_json"])
                self.assertFalse(s["actual_action_asserted"])
                self.assertFalse(s["actual_consequent_asserted"])
                self.assertFalse(s["permission_from_ability"])
                self.assertFalse(s["ability_from_permission"])
                self.assertFalse(s["action_occurrence_from_obligation"])
                if v==1:self.assertTrue(row["qaroshi_full_candidate"].endswith(" qinë."))
                elif v==2:self.assertIn("-te-ki nao ",row["qaroshi_full_candidate"])
                elif v==3:self.assertIn("-te-ho uro ",row["qaroshi_full_candidate"])
                elif v==4:self.assertIn("-te-du dëshu ",row["qaroshi_full_candidate"])
                elif v==5:self.assertTrue(row["qaroshi_full_candidate"].startswith("sen wë "))
                qr.append(row["qaroshi_full_candidate"])
            self.assertEqual(len(set(qr)),5)

    def test_five_material_specific_instruments_are_not_agents(self):
        frames=json.loads((STD/"instrument_frames_9_1.json").read_text(encoding="utf8"))
        self.assertEqual(len(frames),5)
        for f in frames:
            row=self.ledger[challenge_id("voice_valency",f["family"],3)]
            qr=row["qaroshi_full_candidate"]
            self.assertEqual(qr,
                f"sen {f['actor']} {f['patient']}-m {f['instrument']}-shi {f['verb']}-te.")
            sig=json.loads(row["edition_9_1_semantic_signature_json"])
            self.assertFalse(sig["instrument_is_agent"])
            self.assertEqual(sig["instrument_case"],"-shi")
            self.assertNotIn("-za",qr)

    def test_all_18_literary_and_six_technical_are_nonliteral_nonentailing(self):
        narrative=json.loads((STD/"literary_frames_9_1.json").read_text(encoding="utf8"))
        technical=json.loads((STD/"technical_completion_9_1.json").read_text(encoding="utf8"))
        self.assertEqual(sum(len(f["variants"]) for f in narrative),18)
        self.assertEqual(sum(len(f["variants"]) for f in technical),6)
        for f in narrative:
            for v in f["variants"]:
                row=self.ledger[challenge_id("narrative_figures",f["family"],v)]
                sig=json.loads(row["edition_9_1_semantic_signature_json"])
                self.assertFalse(sig["metaphor_asserted_real_world"])
                self.assertTrue(sig["source_not_a_traditional_idiom_claim"])
                if v==5:self.assertIn(" sen ana ",row["qaroshi_full_candidate"])
        for f in technical:
            for v in f["variants"]:
                row=self.ledger[challenge_id("technical_precision",f["family"],v)]
                sig=json.loads(row["edition_9_1_semantic_signature_json"])
                self.assertFalse(sig["unsupported_q_asserted_false"])
                if v==4:
                    self.assertTrue(row["qaroshi_full_candidate"].startswith("sen wë "))
                    self.assertTrue(row["qaroshi_full_candidate"].endswith("-du."))
                if v==5:self.assertIn(" do zotenga nu eri.",row["qaroshi_full_candidate"])

if __name__=="__main__":unittest.main()
