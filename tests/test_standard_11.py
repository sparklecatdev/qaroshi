"""Standard 11 provenance, canonical word identity and evidence status checks."""
import unittest
from pathlib import Path
from tools.standard11.assemble import assemble, readcsv

ROOT = Path(__file__).resolve().parents[1]

class Standard11Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=assemble()
        cls.words={w["qaroshi"]:w for w in readcsv("data/lexicon.csv")}
        cls.words["nëgëra"]={"id":"Q28D001"}

    def test_full_source_coverage(self):
        self.assertEqual(len(self.data["contrasts"]),30)
        self.assertEqual(len(self.data["conversation_rules"]),20)
        self.assertEqual(sum(bool(r["training"]) for r in self.data["conversation_rules"]),12)
        self.assertEqual(self.data["metrics"]["independent_reader_results"],0)
        self.assertEqual(self.data["metrics"]["new_normative_grammar"],0)

    def test_unchanged_canonical_meaning_boundaries(self):
        original={r["id"]:r for r in readcsv("data/v28_34/meaning_boundaries.csv")}
        for row in self.data["contrasts"]:
            for key in original[row["id"]]:
                if key=="status":
                    self.assertEqual(row["source_status"],original[row["id"]][key])
                else:
                    self.assertEqual(row[key],original[row["id"]][key])
            self.assertEqual(row["left_dictionary_id"],self.words[row["left"]]["id"])
            self.assertEqual(row["right_dictionary_id"],self.words[row["right"]]["id"])
            self.assertEqual(row["status"],"editorial_explanation_not_independently_validated")
            self.assertTrue(row["learner_question"].endswith("?"))

    def test_conversation_training_never_claims_external_evidence(self):
        for row in self.data["conversation_rules"]:
            self.assertEqual(row["source"],"data/v28_34/conversational_usage_rules.json")
            if row["training"]:
                self.assertEqual(row["training"]["source_id"],row["id"])
                self.assertEqual(row["training"]["status"],"editorial_training_not_blind_validation")

    def test_website_build_and_navigation_are_wired(self):
        build=(ROOT/"tools/build_wiki.py").read_text(encoding="utf-8")
        page=(ROOT/"web/qaroshi.js").read_text(encoding="utf-8")
        self.assertIn("'standard11':assemble_standard11()",build)
        self.assertIn("wiki_standard11.js",build)
        self.assertIn("case 'meaning':renderMeaning(route);break;",page)
        self.assertIn("#meaning",page)
