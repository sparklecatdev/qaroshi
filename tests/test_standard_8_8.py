"""Edition 8.8 source-linked grammar and evidence regression.

This suite deliberately does not claim meaning was checked by speakers.
"""
from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from tools.stress88.compose import run, rows, verb_sentence, valency_sentence

ROOT = Path(__file__).resolve().parents[1]


class Standard88(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = run()
        cls.cases = {r["id"]:r for r in rows(ROOT/"data/stress88/case_evidence_500.csv")}
        cls.frames = json.loads((ROOT/"data/standard_8/valency_overlay_8_8.json").read_text(encoding="utf8"))
        cls.extensions = json.loads((ROOT/"data/standard_8/sense_extension_8_8.json").read_text(encoding="utf8"))

    def test_full_coverage_of_evidence_not_claim_of_full_translations(self):
        self.assertEqual(len(self.cases), 500)
        self.assertEqual(len(self.frames), 9)
        self.assertEqual(len(self.extensions), 5)
        self.assertEqual(self.summary["prior_editorial_candidates"], 96)
        self.assertEqual(self.summary["editorial_candidates_now"], 135)
        self.assertEqual(self.summary["net_new_complete_candidate_strings"], 39)
        self.assertEqual(self.summary["still_without_full_candidate"], 365)
        self.assertFalse(self.summary["language_complete"])
        self.assertFalse(self.summary["translation_certified"])
        self.assertEqual(self.summary["human_verified"], 0)
        for x in self.cases.values():
            self.assertTrue(x["required_semantic_factors"])
            self.assertEqual(x["human_backtranslation"], "not performed")
            self.assertEqual(x["external_comprehension"], "not performed")
            self.assertEqual(x["proven_language_impossibility"], "no")

    def test_new_narrow_extensions_are_dictionary_anchored(self):
        with (ROOT/"data/lexicon.csv").open(encoding="utf8",newline="") as fp:
            lex={x["id"]:x for x in csv.DictReader(fp)}
        self.assertEqual(len(self.extensions), len({x["id"] for x in self.extensions}))
        self.assertEqual(len(self.frames), len({x["id"] for x in self.frames}))
        for x in self.frames:
            for root, id_, pos in (
                ("root", "root_id", "v"),
                ("actor", "actor_id", "n"),
                ("patient", "patient_id", "n"),
            ):
                if x.get(id_):
                    self.assertEqual((lex[x[id_]]["qaroshi"],lex[x[id_]]["pos"]),
                                     (x[root],pos))
            if x.get("actor_base_id"):
                base=lex[x["actor_base_id"]]
                self.assertEqual(base["qaroshi"],x["actor_base"])
                self.assertEqual(x["actor"],x["actor_base"]+("-sharo" if "-sharo" in x["actor_derivation"] else "-mi"))
            if x["tool"]:
                self.assertEqual((lex[x["tool_id"]]["qaroshi"],lex[x["tool_id"]]["pos"]),
                                 (x["tool"],"n"))
            self.assertFalse(x["human_observed"])
            self.assertIn("passive",x["license"])
        for x in self.extensions:
            for root, id_, pos in (
                ("verb","verb_id","v"),
                ("patient","patient_id","n"),
            ):
                if x.get(id_):
                    self.assertEqual((lex[x[id_]]["qaroshi"],lex[x[id_]]["pos"]),(x[root],pos))
                else:
                    self.assertIn(x[root], {r["qaroshi"] for r in lex.values() if r["pos"]==pos})
            if x.get("actor_id"):
                self.assertEqual((lex[x["actor_id"]]["qaroshi"],lex[x["actor_id"]]["pos"]),
                                 (x["actor"],"n"))
            if x.get("actor_base_id"):
                self.assertEqual(lex[x["actor_base_id"]]["qaroshi"], x["actor_base"])
            if x.get("theme"):
                self.assertIn(x["theme"], {r["qaroshi"] for r in lex.values() if r["pos"]=="n"})
        self.assertEqual(lex["Q004079"]["english"],"pack luggage")
        self.assertEqual(lex["Q006472"]["english"],"hide a feeling")

    def test_new_daily_senses_are_complete_candidate_strings(self):
        for f in self.extensions:
            for v in range(1,5):
                num=(f["family"]-1)*5+v
                id_=f"QS81-{num:04d}"
                r=self.cases[id_]
                self.assertEqual(r["qaroshi_full_candidate"],verb_sentence(
                    f["actor"],f["patient"],f["verb"],v,
                    patient_surface=f.get("patient_surface"),theme=f.get("theme")))
                self.assertEqual(r["candidate_status"],
                                 "new_8_8_editorial_full_composition_not_independently_validated")
                self.assertIn(f["id"],r["witness_ids"])
                self.assertNotIn("-li",r["qaroshi_full_candidate"])
                if v==4:
                    self.assertIn(" do yano mi-tu shiri-te.",r["qaroshi_full_candidate"])

    def test_ticket_polysemy_is_explicit_not_inherited_unreviewed(self):
        f=next(x for x in self.extensions if x["family"]==10)
        self.assertIn("general ticket-credential",f["license"])
        self.assertIn("earlier transport-ticket sense",f["boundary"])
        for v in range(1,5):
            r=self.cases[f"QS81-{45+v:04d}"]
            self.assertTrue(r["qaroshi_full_candidate"].startswith(("sen gura-mi", "hë gura-mi")))
            self.assertEqual(r["candidate_status"],
                "new_8_8_editorial_full_composition_not_independently_validated")

    def test_old_reported_info_has_indefinite_source_and_addressee(self):
        for i in (4,9,34):
            r=self.cases[f"QS81-{i:04d}"]
            self.assertTrue(r["qaroshi_full_candidate"].endswith("do yano mi-tu shiri-te."))
            self.assertEqual(r["candidate_status"],"revised_inherited_source_reporting_editorial_draft")
        # Never conflate a hearsay evidential with a specified recipient.
        self.assertNotIn(" hu", self.cases["QS81-0004"]["qaroshi_full_candidate"])

    def test_quantifier_missing_timing_and_focus_are_composed(self):
        q=self.cases["QS81-0155"]
        self.assertEqual(q["english"],"Only this Nardoragon is well right now.")
        self.assertEqual(q["qaroshi_full_candidate"],"sen dëna qaro ngëshi nëna haro.")
        self.assertIn("not the well-being property or time",q["editorial_scope_warning"])
        # Existing 49 challenge drafts are untouched.
        for i in range(151,201):
            if i==155: continue
            r=self.cases[f"QS81-{i:04d}"]
            self.assertTrue(r["qaroshi_full_candidate"])
            self.assertEqual(r["candidate_status"],"inherited_unverified_editorial_draft")

    def test_voice_and_instrument_roles_have_full_specific_license(self):
        for f in self.frames:
            base=350+(f["family"]-1)*5
            for v in range(1,6):
                r=self.cases[f"QS81-{base+v:04d}"]
                expected=valency_sentence(f,v)
                if expected is None:
                    self.assertEqual(r["qaroshi_full_candidate"],"")
                    self.assertNotEqual(r["candidate_status"],"8_8_specific_actor_patient_voice_license_unverified")
                    continue
                self.assertEqual(r["qaroshi_full_candidate"],expected)
                self.assertEqual(r["candidate_status"],"8_8_specific_actor_patient_voice_license_unverified")
                if v in (2,5):
                    self.assertIn(f["actor"]+"-za",expected)
                    self.assertIn(f["root"]+"-li-te",expected)
                    self.assertNotIn("-shi",expected)
                elif v==3:
                    self.assertIn(f["tool"]+"-shi",expected)
                    self.assertNotIn(f["actor"]+"-za",expected)
                elif v==4:
                    self.assertIn(" nu "+f["root"]+"-te",expected)
        # Generator refuses instrument where no explicit tool sense is licensed.
        self.assertIsNone(valency_sentence(self.frames[1],3))

    def test_no_unlicensed_scope_upgrade(self):
        # These English cases require genuine new grammar and/or meaning.
        for id_ in ("QS81-0051","QS81-0101","QS81-0251","QS81-0302",
                    "QS81-0401","QS81-0451"):
            x=self.cases[id_]
            self.assertFalse(x["qaroshi_full_candidate"])
            self.assertTrue(x["required_semantic_factors"])

if __name__ == "__main__":
    unittest.main()
