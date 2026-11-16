"""8.4 structural regression: evidence and narrowly adopted editorial rules."""
import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/stress84"))
from build_readiness import build, CONTRASTS
from validate_core import analyze


def read_csv(rel):
    with (ROOT / rel).open(encoding="utf8", newline="") as fp:
        return list(csv.DictReader(fp))


class Readiness84(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = build()
        cls.frames = json.loads((ROOT / "data/standard_8/valency_overlay_8_4.json").read_text(encoding="utf8"))
        cls.cases = read_csv("data/stress84/case_review_queue_500.csv")
        cls.verbs = read_csv("data/stress84/verb_frame_cards_400.csv")
        cls.core = read_csv("data/stress84/core_semantic_cards_120.csv")

    def test_coverage_not_marketed_as_complete(self):
        self.assertEqual(len(self.cases), 500)
        self.assertEqual(self.manifest["editorial_drafts_not_independently_validated"], 96)
        self.assertEqual(self.manifest["challenges_without_complete_draft"], 404)
        self.assertFalse(self.manifest["fully_general_translation_certified"])
        self.assertFalse(self.manifest["all_404_remaining_translated"])
        self.assertEqual(self.manifest["real_independent_test_participants"], 0)
        self.assertTrue(all(r["human_backtranslation"] == "not performed" for r in self.cases))

    def test_core_11_exist_and_do_not_collide_with_25(self):
        self.assertEqual(len(self.frames), 11)
        self.assertEqual(len(self.verbs), 400)
        self.assertEqual(len(self.core), 120)
        self.assertEqual(self.manifest["prior_reviewed_general_frames"], 25)
        self.assertEqual(self.manifest["new_narrow_active_frames_defined"], 11)
        self.assertEqual(self.manifest["priority_verbs_still_without_general_frames"], 364)
        self.assertEqual(sum(r["8_4_frame_status"] == "8_4_defined_active_frame_only" for r in self.verbs), 11)
        self.assertEqual(len({f["lemma"] for f in self.frames}), 11)
        self.assertTrue(all(not f["human_observed"] for f in self.frames))

    def test_each_model_fits_its_exact_active_frame(self):
        for frame in self.frames:
            with self.subTest(lemma=frame["lemma"]):
                result = analyze(frame["model_sentence"])
                self.assertEqual(result["status"], "structural_model_match", result)

    def test_negative_grammatical_cases_are_rejected(self):
        examples = [
            "sen mi kima-m shërami.",   # intransitive sleep with object
            "sen mi rëgë.",            # missing required object
            "sen mi naro-m rëgë-li.",  # unapproved passive
            "sen mi naro-m rëgë-ki-ho.",  # mutually exclusive modals
            "sen mi naro-m rëgë-mo-te.",  # wrong suffix ordering
            "sen mi naro-m mara-tu rëgë.",  # unlicensed recipient
            "sen mi rëgë naro-m.",     # not predicate-final
        ]
        for line in examples:
            with self.subTest(sentence=line):
                self.assertNotEqual(analyze(line)["status"], "structural_model_match")

    def test_contrast_questions_and_key_separate(self):
        q = read_csv("data/stress84/blind_contrast_questions.csv")
        k = read_csv("data/stress84/separate_blind_answer_key.csv")
        self.assertEqual(len(q), len(CONTRASTS))
        self.assertEqual(len(k), len(q))
        self.assertEqual({r["id"] for r in q}, {r["id"] for r in k})
        self.assertTrue(all(r["response_A_or_B"] == "" for r in q))
        self.assertTrue(all("correct" not in r for r in q))
        self.assertTrue(all(r["status"] == "unadministered" for r in k))

    def test_stable_edited_source_baselines(self):
        prior = json.loads((ROOT / "data/v14/baseline_sha256.json").read_text(encoding="utf8"))["sha256"]
        self.assertEqual(len(prior), 29)
        for rel, digest in prior.items():
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest)

    def test_generated_digests_and_nonfictional_human_evidence(self):
        for name, digest in self.manifest["source_hashes"].items():
            p = ROOT / "data/stress84" / name
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), digest)
        self.assertTrue(all(r["native_definition_approved"] == "no"
                            for r in self.core))
        self.assertTrue(all(r["independent_comprehension"] == "not performed"
                            for r in self.verbs))


if __name__ == "__main__":
    unittest.main()
