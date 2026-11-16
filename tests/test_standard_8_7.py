import csv
import json
import unittest
from pathlib import Path

from tools.stress87.validate import analyze
from tools.stress87.benchmark import cases

ROOT = Path(__file__).resolve().parents[1]
FRAMES = json.loads((ROOT / "data/standard_8/valency_overlay_8_7.json").read_text(encoding="utf-8"))


class EditorialEvidence(unittest.TestCase):
    def test_sources_and_dictionary(self):
        with (ROOT / "data/lexicon.csv").open(encoding="utf-8", newline="") as source:
            lexicon = {row["id"]: row for row in csv.DictReader(source)}
        with (ROOT / "corpus/parallel_sentences.csv").open(encoding="utf-8", newline="") as source:
            corpus = {row["id"]: row for row in csv.DictReader(source)}
        self.assertEqual(len(FRAMES), 97)
        for key in ("id", "lemma", "source_example_id"):
            self.assertEqual(len({row[key] for row in FRAMES}), len(FRAMES))
        previous = set()
        for name in ("data/semantics/valency_frames.json", "data/standard_8/valency_overlay_8_4.json", "data/standard_8/valency_overlay_8_6.json"):
            previous.update(row["lemma"] for row in json.loads((ROOT / name).read_text(encoding="utf-8")))
        self.assertFalse(previous.intersection(row["lemma"] for row in FRAMES))
        for row in FRAMES:
            with self.subTest(frame=row["id"]):
                verb, noun = lexicon[row["dictionary_id"]], lexicon[row["attested_object_dictionary_id"]]
                source = corpus[row["source_example_id"]]
                self.assertEqual((verb["qaroshi"], verb["pos"], verb["english"]), (row["lemma"], "v", row["dictionary_gloss"]))
                self.assertEqual((noun["qaroshi"], noun["pos"]), (row["attested_object"], "n"))
                self.assertEqual((source["qaroshi"], source["english"]), (row["source_sentence"], row["source_translation"]))
                self.assertEqual(row["frame"], "V1")
                self.assertFalse(row["human_observed"])
                self.assertTrue(row["semantic_boundary"])
                self.assertEqual(analyze(source["qaroshi"])["frame_id"], row["id"])

    def test_generated_structural_contrasts(self):
        for group, sentence, expected in cases():
            with self.subTest(group=group, sentence=sentence):
                self.assertEqual(analyze(sentence)["status"] == "structural_model_match", expected)

    def test_neither_general_grammar_nor_meaning_is_claimed(self):
        self.assertEqual(analyze("sen mi shiwaro-m khukhiri.")["semantic_validation"], "not performed")
        # A real noun can still be an implausible object for a given verb.
        self.assertEqual(analyze("sen mi mara-m khukhiri.")["status"], "structural_model_match")
        for sentence in ("sen mi shiwaro-m khukhiri..", "sen mi nu shiwaro-m khukhiri.",
                         "sen mi shiwaro-m shiwaro-m khukhiri.", "sen mi shiwaro-m khukhiri-he.",
                         "sen mi shiwaro-m khukhiri nu.", "sen mi shiwaro-m khukhiri-za."):
            with self.subTest(sentence=sentence):
                self.assertEqual(analyze(sentence)["status"], "outside_restricted_checker")


if __name__ == "__main__":
    unittest.main()
