import csv
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('benchmark86', ROOT / 'tools/stress86/benchmark.py')
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def read_csv(path):
    with (ROOT / path).open(encoding='utf8', newline='') as f:
        return list(csv.DictReader(f))


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf8'))


class EverydayFrames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = read_json('data/standard_8/valency_overlay_8_6.json')
        cls.frames = {r['lemma']: r for r in cls.rows}
        cls.lex = {r['qaroshi']: r for r in read_csv('data/lexicon.csv')}
        cls.corpus = {r['id']: r for r in read_csv('corpus/parallel_sentences.csv')}
        cls.cases = read_json('data/standard_8/challenge_reviews_8_6.json')

    def test_canonical_words_and_precise_sources(self):
        self.assertEqual(len(self.rows), 19)
        self.assertEqual(len(self.frames), len(self.rows))
        prior = read_json('data/semantics/valency_frames.json') + read_json('data/standard_8/valency_overlay_8_4.json')
        self.assertFalse(set(self.frames) & {r['lemma'] for r in prior})
        for frame in self.rows:
            with self.subTest(lemma=frame['lemma']):
                lexeme = self.lex[frame['lemma']]
                self.assertEqual((lexeme['id'], lexeme['pos'], lexeme['english']),
                                 (frame['dictionary_id'], 'v', frame['dictionary_gloss']))
                source = self.corpus[frame['source_example_id']]
                self.assertEqual((source['qaroshi'], source['english']),
                                 (frame['source_sentence'], frame['source_translation']))
                self.assertIn(frame['lemma'], source['qaroshi'])
                self.assertFalse(frame['human_observed'])
                self.assertTrue(frame['semantic_boundary'])
                self.assertEqual(bool(frame['object_role']), frame['frame'] == 'V1')

    def test_original_challenges_and_structural_subset(self):
        original = {r['id']: r for r in read_csv('data/stress81/challenges_500.csv')}
        self.assertEqual(len(self.cases), 6)
        self.assertEqual(len({c['id'] for c in self.cases}), 6)
        for case in self.cases:
            with self.subTest(case=case['id']):
                self.assertEqual(original[case['id']]['english'], case['target'])
                self.assertEqual(case['status'], 'editorial_candidate_not_independently_verified')
                self.assertTrue(benchmark.evaluate(case, self.lex, self.frames))

    def test_structural_check_rejects_changed_meanings(self):
        for case in self.cases:
            self.assertFalse(benchmark.evaluate(dict(case, qaroshi=case['qaroshi'].replace('-te', '-yu')), self.lex, self.frames))
            self.assertFalse(benchmark.evaluate(dict(case, subject_id='Q000001'), self.lex, self.frames))
            self.assertFalse(benchmark.evaluate(dict(case, mode='invalid'), self.lex, self.frames))
            changed = case['qaroshi'].replace(' nu ', ' ') if case['mode'] == 'negative' else case['qaroshi'].replace(' '+case['verb'], ' nu '+case['verb'])
            self.assertFalse(benchmark.evaluate(dict(case, qaroshi=changed), self.lex, self.frames))


class WantClause(unittest.TestCase):
    def test_same_actor_and_local_negation(self):
        spec = importlib.util.spec_from_file_location('want86', ROOT / 'tools/stress86/validate_want.py')
        want = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(want)
        good = ['sen mi naro-m rëgë do mi rawëli.',
                'sen mi naro-m rëgë do mi nu rawëli.',
                'sen mi nu shërami do mi rawëli.',
                'sen mi naro-m rëgë do mi rawëli-te.']
        bad = ['sen mi naro-m rëgë do ti rawëli.',
               'sen mi naro-m rëgë do rawëli.',
               'sen mi naro-m rëgë do mi kima-m rawëli.',
               'sen mi naro-m rëgë do mi rawëli-te-yu.',
               'sen mi naro-m rëgë do mi kërawë.']
        for sentence in good:
            with self.subTest(sentence=sentence):
                result = want.analyze_want(sentence)
                self.assertEqual(result['status'], 'structural_model_match')
                self.assertEqual(result['semantic_validation'], 'not performed')
        for sentence in bad:
            with self.subTest(sentence=sentence):
                self.assertEqual(want.analyze_want(sentence)['status'], 'outside_restricted_checker')


if __name__ == '__main__':
    unittest.main()
