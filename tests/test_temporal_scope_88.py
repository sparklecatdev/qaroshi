"""Restricted temporal ordering tests: no open-domain or human claims."""
import unittest
from tools.stress88.temporal import analyze, parse_clause


class TemporalScope88(unittest.TestCase):
    def test_after_is_not_before(self):
        after=analyze("sen ana sa goro-te, mi nëru-te.")
        before=analyze("sen ëna sa goro-te, mi nëru-te.")
        self.assertEqual(after["status"],"licensed_temporal_88_restricted")
        self.assertEqual(before["status"],"licensed_temporal_88_restricted")
        self.assertEqual(after["relation"],"matrix_after_subordinate")
        self.assertEqual(before["relation"],"matrix_before_subordinate")
        self.assertEqual(after["subordinate"]["subject"],"sa")
        self.assertEqual(after["matrix"]["subject"],"mi")
        self.assertEqual(after["matrix"]["verb"],"nëru")

    def test_overlapping_requires_progressive_intervals(self):
        ok=analyze("sen yaro sa goro-te-se, mi nëru-te-se.")
        self.assertEqual(ok["relation"],"overlap")
        for s in ("sen yaro sa goro-te, mi nëru-te-se.",
                  "sen yaro sa goro-te-se, mi nëru-te.",
                  "sen yaro sa goro-te-mo, mi nëru-te-se."):
            with self.subTest(s=s):
                self.assertEqual(analyze(s)["status"],"outside_temporal_88_restricted_checker")

    def test_negative_until_does_not_add_later_event(self):
        x=analyze("sen torëne sa goro-te, mi nu nëru-te.")
        self.assertEqual(x["relation"],"matrix_holds_until_subordinate_boundary")
        self.assertTrue(x["matrix"]["negative"])
        self.assertFalse(x["matrix_after_boundary_asserted"])
        self.assertIn("does not by itself assert",x["implicature_limit"])
        self.assertNotEqual(x["matrix"]["subject"],x["subordinate"]["subject"])

    def test_invalid_scope_and_double_registration_abstain(self):
        for s in ("sen ana sa goro-te mi nëru-te.",
                  "sen ana sa goro-te, sen mi nëru-te.",
                  "sen ana sa goro-te, mi nëru-te he?",
                  "sen ana sa goro-te, mi pëli-te.",
                  "sen ana sa goro-te, mi nëru-te, ti goro-te.",
                  "sen ana sa goro-te-se, mi nu nu nëru-te.",
                  "hë ëna sa goro-te, mi nëru-te."):
            with self.subTest(s=s):
                self.assertEqual(analyze(s)["status"],"outside_temporal_88_restricted_checker")

    def test_time_aspect_and_voice_are_not_inferred(self):
        x=parse_clause("ti nu shërami-yu-se")
        self.assertEqual(x["subject"],"ti")
        self.assertEqual(x["past_or_future"],"future")
        self.assertTrue(x["negative"])
        self.assertEqual(x["aspect"],"se")
        self.assertIsNone(parse_clause("ti shërami-li-yu-se"))


if __name__=="__main__":
    unittest.main()
