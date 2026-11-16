"""Restricted attempt-frame contrasts; structural matching is not comprehension."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools/stress85"))
from validate_attempt import analyze_attempt


class AttemptFrame(unittest.TestCase):
    def test_documented_contrasts(self):
        for sentence in (
            "sen mi naro-m rëgë do mi kërawë.",
            "sen mi naro-m rëgë do mi nu kërawë.",
            "sen mi nu shërami do mi kërawë.",
            "sen mi naro-m rëgë do mi kërawë-te.",
        ):
            with self.subTest(sentence=sentence):
                self.assertEqual(analyze_attempt(sentence)["status"], "structural_model_match")

    def test_unlicensed_and_malformed(self):
        for sentence in (
            "sen mi naro-m rëgë do ti kërawë.",
            "sen mi naro-m rëgë mi kërawë.",
            "sen mi naro-m rëgë do mi kërawë-li.",
            "sen mi naro-m shërami do mi kërawë.",
            "sen mi naro-m rëgë do mi naro-m kërawë.",
            "sen mi naro-m rëgë do do mi kërawë.",
        ):
            with self.subTest(sentence=sentence):
                self.assertNotEqual(analyze_attempt(sentence)["status"], "structural_model_match")
