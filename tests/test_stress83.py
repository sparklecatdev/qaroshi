"""Regression suite for honest, editioned Qaroshi 8.3 completion workflow."""
import collections
import csv
import gzip
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools/stress83"))
from complete import build

def read(p):
    with (ROOT/p).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f))

class Completion83(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=build()
        cls.cases=read("data/stress83/translation_proposals_500.csv")
        cls.verbs=read("data/stress83/restricted_valency_standard_375.csv")
        cls.compounds=read("data/stress83/compound_sense_standard_3108.csv")
        cls.original=read("data/stress81/audit_results_500.csv")
        cls.lex={r["qaroshi"]:r for r in read("data/lexicon.csv")}
    def test_every_challenge_has_a_record(self):
        self.assertEqual(len(self.cases),500)
        self.assertEqual([x["id"] for x in self.cases],[x["id"] for x in self.original])
    def test_complete_100_family_coverage(self):
        self.assertEqual(len({r["family"] for r in self.cases}),100)
        self.assertEqual(set(collections.Counter(r["domain"] for r in self.cases).values()),{50})
    def test_no_spurious_language_failure_claim(self):
        self.assertTrue(all(r["language_inexpressibility_proven"]=="no" for r in self.cases))
    def test_candidate_status_not_automatically_ratifed(self):
        self.assertTrue(all(r["speaker_accepted"]=="not tested" for r in self.cases))
        self.assertTrue(all(r["independent_reverse_translation"]=="not performed" for r in self.cases))
    def test_49_prior_drafts_preserved(self):
        for a,b in zip(self.cases,self.original):
            if b["normative_compositional_draft"]:
                self.assertEqual(a["qaroshi_draft"],b["normative_compositional_draft"])
    def test_lexicon_witnesses_are_real_entries(self):
        for r in self.cases:
            if r["dictionary_lexeme_witness_json"]:
                for w in json.loads(r["dictionary_lexeme_witness_json"]):
                    if w["qr"]:
                        self.assertEqual(self.lex[w["qr"]]["id"],w["id"])
    def test_new_editorial_drafts_are_really_qaroshi(self):
        for r in self.cases:
            if r["qaroshi_draft"]:
                self.assertTrue(r["qaroshi_draft"].startswith(("sen ","hë ","më ","dal ","qor ")))
                self.assertNotIn("[",r["qaroshi_draft"])
                self.assertNotIn("]",r["qaroshi_draft"])
    def test_remaining_gaps_are_not_hidden(self):
        self.assertEqual(sum(v for v in self.manifest["translation_status_counts"].values()),500)
        self.assertFalse(self.manifest["all_challenges_human_validated"])
    def test_verb_review_covers_375(self):
        self.assertEqual(len(self.verbs),375)
        self.assertEqual(len({x["dictionary_id"] for x in self.verbs}),375)
        self.assertTrue(all(x["unrestricted_general_frame_completed"]=="no" for x in self.verbs))
    def test_verb_roles_never_imply_passive_without_review(self):
        self.assertTrue(all(x["licensed_passive"].startswith("no") for x in self.verbs))
    def test_compound_list_covers_3108(self):
        self.assertEqual(len(self.compounds),3108)
        self.assertEqual(len({x["canonical_id"] for x in self.compounds}),3108)
    def test_compounds_preserve_all_spellings(self):
        self.assertTrue(all(x["spelling_renamed"]=="no" for x in self.compounds))
    def test_compound_gloss_matches_canonical(self):
        for r in self.compounds:
            self.assertEqual(r["normative_whole_word_gloss"],self.lex[r["word"]]["english"])
    def test_no_fake_human_testing(self):
        self.assertEqual(self.manifest["human_comprehension_participants"],0)
    def test_source_integrity(self):
        frozen=json.loads((ROOT/"data/v14/baseline_sha256.json").read_text())["sha256"]
        self.assertEqual(len(frozen),29)
        for p,d in frozen.items():
            self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),d,p)
    def test_generated_output_hashes(self):
        for p,d in self.manifest["generated_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/"data/stress83"/p).read_bytes()).hexdigest(),d,p)
    def test_deterministic_rebuild(self):
        first={p:(ROOT/"data/stress83"/p).read_bytes() for p in self.manifest["generated_sha256"]}
        build()
        second={p:(ROOT/"data/stress83"/p).read_bytes() for p in self.manifest["generated_sha256"]}
        self.assertEqual(first,second)

if __name__=="__main__":
    unittest.main()
