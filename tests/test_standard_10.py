"""Source provenance and human-trial integrity for Qaroshi Standard 10."""
from __future__ import annotations
import csv
import json
import tempfile
import unittest
from pathlib import Path

from tools.standard10.resources import assemble,load_csv,load_json
from tools.standard10.trial import build,score,N_ITEMS

ROOT=Path(__file__).resolve().parents[1]

class SourceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=assemble()
        cls.manifest=cls.data["manifest"]
        cls.words={x["qaroshi"]:x for x in load_csv("data/lexicon.csv")}

    def test_frozen_sources_and_editorial_status_honesty(self):
        self.assertEqual(self.manifest["canonical_words"],30000)
        self.assertEqual(len(self.words),30000)
        self.assertEqual(self.manifest["source_dialogues_original11"],49)
        self.assertEqual(self.manifest["source_dialogues_recombined18"],len(load_json("data/v18/source_linked_conversation_paths.json")))
        self.assertGreater(self.manifest["conversation_turns"],294)
        self.assertGreaterEqual(self.manifest["machine_roundtrip_drills"],1500)
        self.assertEqual(self.manifest["independent_human_reader_trials"],0)
        self.assertEqual(self.manifest["independent_human_attestations"],0)

    def test_profiles_senses_800_priority_and_5000_draft_separation(self):
        profiles=self.data["profiles"];senses=self.data["senses"]
        drafts=self.data["draft_cards"];priority=self.data["priorities"]
        self.assertGreaterEqual(len(profiles),40)
        self.assertGreaterEqual(sum(map(len,senses.values())),40)
        self.assertEqual(len(priority),800)
        self.assertGreaterEqual(len(drafts),4500)
        for word,profile in profiles.items():
            self.assertEqual(profile["classification"].startswith("individually authored"),True)
            self.assertEqual(self.words[word]["id"],next(p["source_id"] for p in load_csv("data/v12_13/core_lexical_profiles.csv") if p["qaroshi"]==word))
        for word,group in senses.items():
            for sense in group:
                self.assertEqual(sense["independent_human_attestation"],False)
                self.assertTrue(sense["source_status"])\n                self.assertEqual(sense["source"],"data/semantics/curated_senses.json")
                self.assertTrue(sense["definition"])
        for word,d in drafts.items():
            self.assertIn(d["selected_reference_gloss"].casefold(),self.words[word]["english"].casefold())
            self.assertIn("UNREVIEWED",d["status"])
            self.assertEqual(d["independent_human_attestation"],False)
            self.assertNotIn("approved",d["status"].split("UNREVIEWED")[0])

    def test_conversation_and_drill_source_exactness(self):
        scenes={d["id"]:d for d in self.data["dialogues"]}
        for original in load_json("corpus/original11/dialogues.json"):
            d=scenes["original11/"+original["id"]]
            self.assertEqual(len(d["turns"]),len(original["turns"]))
            self.assertEqual([x["qaroshi"] for x in d["turns"]],[t["qaroshi"] for t in original["turns"]])
            self.assertTrue(all("not speaker" in t["status"] for t in d["turns"]))
        for original in load_json("data/v18/source_linked_conversation_paths.json"):
            d=scenes["source18/"+original["id"]]
            self.assertEqual([x["reference_id"] for x in d["turns"]],[t.get("reference_id","") for t in original["turns"]])
        self.assertTrue(all("ONLY" in d["status"] for d in self.data["controlled_drills"]))
        self.assertEqual(
            [d["qaroshi"] for d in self.data["controlled_drills"]],
            [x["qr"] for x in load_json("data/fluency11/translation_pairs.json") if x["en"] and x["qr"]],
        )

class BlindProtocol(unittest.TestCase):
    def test_80_unique_blind_prompts_with_no_embedded_key_or_human_results(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp);manifest=build(out)
            self.assertEqual(manifest["items"],N_ITEMS)
            self.assertEqual(manifest["human_adjudications"],0)
            read=lambda name:list(csv.DictReader((out/name).open(encoding="utf-8",newline="")))
            blind=read("learner_blind_items.csv")
            teacher=read("facilitator_english_key.csv")
            response=read("empty_response_and_adjudication.csv")
            self.assertEqual(len(blind),len(teacher))
            self.assertEqual(len(blind),len(response))
            self.assertEqual(len({x["item_id"] for x in blind}),N_ITEMS)
            self.assertEqual({x["item_id"] for x in blind},{x["item_id"] for x in teacher})
            self.assertFalse(any("english" in key for key in blind[0]))
            self.assertTrue(all(x["contextual_editorial_english"] for x in teacher))
            self.assertTrue(all(not x["first_pass_english_paraphrase"] for x in response))
            self.assertTrue(all(not x["semantic_rating"] for x in response))
            with self.assertRaisesRegex(ValueError,"No completed human responses"):
                score(out/"empty_response_and_adjudication.csv")
            self.assertIn("not cryptographically", (out/"PROTOCOL.md").read_text(encoding="utf8"))

    def test_scoring_requires_filled_human_adjudication_and_rejects_duplicates(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp);build(out)
            path=out/"human_filled_TEST_ONLY.csv"
            fields=["item_id","reader_anonymous_code","first_pass_english_paraphrase",
                "adjudicator_anonymous_code","semantic_rating","reader_confirmed_no_key_access"]
            def emit(rows):
                with path.open("w",newline="",encoding="utf8") as file:
                    writer=csv.DictWriter(file,fieldnames=fields)
                    writer.writeheader();writer.writerows(rows)
            example={
                "item_id":"BL10-001","reader_anonymous_code":"SYNTHETIC-TEST-NOT-A-PERSON",
                "first_pass_english_paraphrase":"synthetic test only",
                "adjudicator_anonymous_code":"SYNTHETIC-JUDGE",
                "semantic_rating":"partial",
                "reader_confirmed_no_key_access":"unsure",
            }
            emit([example])
            result=score(path)
            self.assertEqual(result["reviewers"],1)
            self.assertEqual(result["rated_items"],1)
            self.assertIn("cannot be software authenticated",result["status"])
            emit([example,example])
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                score(path)
            emit([{**example,"semantic_rating":"automatically_verified"}])
            with self.assertRaisesRegex(ValueError,"Rating must"):
                score(path)
            emit([{**example,"reader_confirmed_no_key_access":""}])
            with self.assertRaisesRegex(ValueError,"Incomplete"):
                score(path)

if __name__=="__main__":unittest.main()
