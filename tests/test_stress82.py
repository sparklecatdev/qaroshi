"""Qaroshi 8.2 expressive completeness: reproducible evidence gates."""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools/stress82"))
from build_review import build, NARROW_SENSES

def read(name):
    with (ROOT/name).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f))
def load(name):
    return json.loads((ROOT/name).read_text(encoding="utf8"))

class Stress82Review(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=build()
        cls.cases=read("data/stress82/case_adjudications_500.csv")
        cls.verbs=read("data/stress82/verb_reviews_375.csv")
        cls.probes=read("data/stress82/verb_contrast_trials_1125.csv")
        cls.lex=read("data/stress82/new_lexical_boundaries.csv")
        cls.compounds=read("data/stress82/compound_review_3108.csv")
        cls.pairs=read("data/stress82/qaroshi_minimal_pairs.csv")
        cls.passages=read("data/stress82/connected_passages.csv")
        cls.old=read("data/stress81/audit_results_500.csv")
    def test_all_original_challenge_ids(self):
        self.assertEqual(len(self.cases),500)
        self.assertEqual([r["id"] for r in self.cases],[r["id"] for r in self.old])
    def test_no_duplicate_original_english(self):
        self.assertEqual(len({r["english_target"].casefold() for r in self.cases}),500)
    def test_complete_domain_distribution(self):
        self.assertEqual(Counter(r["domain"] for r in self.cases),{d:50 for d in
            ["daily","time_motion","social_consent","quantifier_logic","evidentiality",
             "embedding_reference","counterfactual_modal","voice_valency","narrative_figures","technical_precision"]})
    def test_original_49_unchanged(self):
        for newer,older in zip(self.cases,self.old):
            self.assertEqual(newer["qaroshi_draft"],older["normative_compositional_draft"])
    def test_refrains_from_fake_translations(self):
        self.assertEqual(sum(bool(r["qaroshi_draft"]) for r in self.cases),49)
        self.assertEqual(sum(not bool(r["qaroshi_draft"]) for r in self.cases),451)
        self.assertTrue(all(r["complete_backtranslation_independently_checked"]=="no" for r in self.cases))
        self.assertTrue(all(r["new_language_gap_proven"]=="no" for r in self.cases))
    def test_every_case_has_target_specific_reason(self):
        self.assertTrue(all(r["source_grammar_feature"] and r["target_semantic_structure"] and
            r["required_next_adjudication"] for r in self.cases))
    def test_lexical_witnesses_are_real_headword_ids(self):
        canon={r["qaroshi"]:r for r in read("data/lexicon.csv")}
        for case in self.cases:
            for x in json.loads(case["lexical_candidate_witnesses_json"]):
                self.assertEqual(canon[x["qaroshi_root"]]["id"],x["canonical_id"])
                self.assertIn("NOT adjudicated",x["meaning_status"])
    def test_no_automatic_word_sense_approval(self):
        for case in self.cases:
            self.assertIn(case["coverage"],{
                "limited_normative_composition_unratified",
                "no_complete_Qaroshi_translation_yet"})
    def test_375_exact_verbs(self):
        self.assertEqual(len(self.verbs),375)
        self.assertEqual(len({r["lemma"] for r in self.verbs}),375)
        full={r["lemma"] for r in read("data/standard_8/verb_audit_400.csv")
              if r["general_frame_review"].startswith("yes")}
        self.assertTrue(full.isdisjoint({r["lemma"] for r in self.verbs}))
    def test_verb_examples_source_grounded(self):
        corpus={r["id"]:r for r in read("corpus/parallel_sentences.csv")}
        for r in self.verbs:
            if r["source_id"]:
                self.assertEqual(r["source_qaroshi"],corpus[r["source_id"]]["qaroshi"])
    def test_no_generalization_from_one_example(self):
        self.assertTrue(all(r["full_general_frame_approved_by_8_2"]=="no" for r in self.verbs))
    def test_three_probes_per_verb(self):
        self.assertEqual(len(self.probes),1125)
        self.assertEqual(Counter(r["lemma"] for r in self.probes),{r["lemma"]:3 for r in self.verbs})
        self.assertTrue(all(r["new_candidate_qaroshi"]=="" for r in self.probes))
    def test_every_new_sense_is_existing_headword(self):
        lex={r["qaroshi"]:r for r in read("data/lexicon.csv")}
        self.assertGreaterEqual(len(self.lex),10)
        for r in self.lex:
            self.assertEqual(r["canonical_id"],lex[r["lemma"]]["id"])
            self.assertIn("no",r["historical_spelling_changed"])
    def test_compound_risk_rows(self):
        self.assertEqual(len(self.compounds),3108)
        self.assertEqual(len({r["canonical_id"] for r in self.compounds}),3108)
    def test_compound_decisions_not_all_approved(self):
        self.assertGreater(sum(r["decision_status"]=="unresolved_component_polysemy" for r in self.compounds),1000)
        self.assertTrue(all(r["preserve_spelling"]=="yes" for r in self.compounds))
    def test_hundreds_real_qr_minimal_pairs(self):
        self.assertGreaterEqual(len(self.pairs),350)
        self.assertEqual(len({r["id"] for r in self.pairs}),len(self.pairs))
        for r in self.pairs:
            self.assertNotEqual(r["qaroshi_A"],r["qaroshi_B"])
            self.assertNotEqual(r["meaning_A"],r["meaning_B"])
    def test_embedded_pairs_are_doubly_recognized(self):
        from embedded_question import analyze
        for r in self.pairs:
            if r["category"]!="quantifier and focus":
                self.assertTrue(analyze(r["qaroshi_A"])["supported"])
                self.assertTrue(analyze(r["qaroshi_B"])["supported"])
    def test_dialogues_are_new_and_annotated(self):
        self.assertEqual(len({r["passage_id"] for r in self.passages}),4)
        self.assertGreaterEqual(len(self.passages),30)
        self.assertTrue(all(r["grammar_annotation"] and r["speaker_attested"]=="no" for r in self.passages))
    def test_never_claim_human_test(self):
        self.assertEqual(self.manifest["human_comprehension_test_participants"],0)
        self.assertEqual(self.manifest["independent_semantic_backtranslations"],0)
    def test_legacy_29_source_hashes(self):
        m=load("data/v14/baseline_sha256.json")["sha256"]
        self.assertEqual(len(m),29)
        for path,expected in m.items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected,path)
    def test_reproducible_generation(self):
        old={p:(ROOT/"data/stress82"/p).read_bytes()
             for p in self.manifest["generated_sha256"]}
        build()
        for p,content in old.items():
            self.assertEqual((ROOT/"data/stress82"/p).read_bytes(),content,p)
    def test_manifest_hashes_all_outputs(self):
        for p,s in self.manifest["generated_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/"data/stress82"/p).read_bytes()).hexdigest(),s,p)
    def test_not_a_stable_edition_claim(self):
        self.assertIn("candidate",self.manifest["edition"].lower())
        self.assertEqual(self.manifest["fully_general_verb_frames_newly_approved"],0)

if __name__=="__main__":
    unittest.main()
