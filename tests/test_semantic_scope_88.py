"""8.8 exact-pattern role and scope interpretation tests (not human evidence)."""
import json
import unittest
from pathlib import Path

from tools.stress88.scope import scope
from tools.stress88.compose import verb_sentence, valency_sentence

ROOT=Path(__file__).resolve().parents[1]
SENSES=json.loads((ROOT/"data/standard_8/sense_extension_8_8.json").read_text(encoding="utf-8"))
FRAMES=json.loads((ROOT/"data/standard_8/valency_overlay_8_8.json").read_text(encoding="utf-8"))


class ExactScope88(unittest.TestCase):
    def test_new_daily_senses_keep_their_roles_and_scope(self):
        self.assertEqual(len(SENSES),5)
        for f in SENSES:
            for variant in range(1,5):
                sentence=verb_sentence(f["actor"],f["patient"],f["verb"],variant,
                                       patient_surface=f.get("patient_surface"),
                                       theme=f.get("theme"))
                with self.subTest(family=f["family"],variant=variant):
                    r=scope(sentence)
                    self.assertEqual(r["status"],"licensed_8_8_restricted")
                    self.assertEqual(r["actor"],f["actor"])
                    self.assertEqual(r["patient"],f["patient"])
                    self.assertEqual(r["theme"],f.get("theme"))
                    self.assertEqual(r["event_polarity"],"negative" if variant==2 else "positive")
                    self.assertEqual(r["event_is_asserted"],variant==1)
                    self.assertEqual(r["speech_act"],"polar_question" if variant==3 else "declarative")
                    if f.get("theme"):
                        self.assertEqual(r["recipient"],f["patient"])
                    if variant==4:
                        self.assertFalse(r["embedded_event_asserted"])
                        self.assertTrue(r["outer_speech_event_asserted"])
                        self.assertEqual((r["reported_by"],r["reported_to"]),("yano","mi"))
                    else:
                        self.assertIsNone(r["embedded_event_asserted"])

    def test_exact_voice_passive_agent_instrument_not_conflated(self):
        self.assertEqual(len(FRAMES),9)
        for frame in FRAMES:
            for variant in range(1,6):
                sentence=valency_sentence(frame,variant)
                if sentence is None:
                    self.assertIsNone(frame["tool"])
                    continue
                with self.subTest(frame=frame["id"],variant=variant):
                    r=scope(sentence)
                    self.assertEqual(r["status"],"licensed_8_8_restricted")
                    self.assertEqual(r["actor"],frame["actor"])
                    self.assertEqual(r["patient"],frame["patient"])
                    self.assertEqual(r["voice"],"passive" if variant in (2,5) else "active")
                    self.assertEqual(r["passive_agent_case"],"-za" if variant in (2,5) else None)
                    self.assertEqual(r["instrument_case"],"-shi" if variant==3 else None)
                    self.assertEqual(r["instrument"],frame["tool"] if variant==3 else None)
                    self.assertEqual(r["event_is_asserted"],variant in (1,2,3))
                    if variant==4:
                        self.assertEqual(r["event_polarity"],"negative")

    def test_focus_is_on_np_not_time(self):
        r=scope("sen dëna qaro ngëshi nëna haro.")
        self.assertEqual(r["focus"],{"constituent":"dëna qaro","kind":"exclusive-NP"})
        self.assertFalse(r["exclusive_time_focus"])
        self.assertEqual(r["time_reference"],"nëna (now)")

    def test_unlicensed_forms_abstain_instead_of_guessing(self):
        for sentence in (
            "sen mi kima-m goro-te.",
            "sen regaro pënaro-m bebëyo-za rëgë-te.",
            "sen pënaro regaro-shi rëgë-li-te.",
            "sen nëbihu-sharo tëkuta-m bëzë-shi ngigoyi-te.",
            "sen dëna qaro nëna ngëshi haro.",
            "sen taru ngibeko-m zhiseti-li-te.",
        ):
            with self.subTest(sentence=sentence):
                result=scope(sentence)
                self.assertEqual(result["status"],"outside_restricted_8_8_scope")
                self.assertFalse(result["meaning_verified"])


if __name__=="__main__":
    unittest.main()
