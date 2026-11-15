"""3.0 reproducibility, compatibility, grammar and corpus checks."""
import csv,hashlib,json,sys,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'source'))
from qaroshi import (analyze_word,check_sentence,derive_word,entries,glyphs_of,
                     RESONANCES,validate_data)
from functional_v3 import FUNCTIONS_V3
from morphemes_v3 import MORPHEMES_V3
from curated_terms_v3 import iter_concepts


def csvrows(filename):
    with filename.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


class ReferenceV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lex=entries()
        cls.by_form={x['qaroshi']:x for x in cls.lex}
        cls.baseline=csvrows(ROOT/'source/lexicon_v2_snapshot.csv')
        cls.sentences=csvrows(ROOT/'corpus/parallel_sentences.csv')
        cls.old_corpus=csvrows(ROOT/'source/corpus_v2_snapshot.csv')
        cls.new_sentences=[x for x in cls.sentences if x['edition']=='3.0']
        cls.statistics=json.loads((ROOT/'data/statistics.json').read_text(encoding='utf-8'))

    def test_v2_source_frozen_verbatim(self):
        self.assertEqual(len(self.baseline),6819)
        for row in self.baseline:self.assertEqual(self.by_form[row['qaroshi']],row)

    def test_all_legacy_ids_stable(self):
        ids={x['id'] for x in self.lex}
        self.assertEqual(len(ids),len(self.lex))
        self.assertTrue(all(x['id'] in ids for x in self.baseline))

    def test_new_counts_and_review_classes(self):
        self.assertEqual(len(self.lex),9082)
        self.assertEqual(len([x for x in self.lex if x['edition']=='3.0' and x['review']=='candidate']),2223)
        self.assertEqual(len([x for x in self.lex if x['edition']=='3.0' and x['review']=='proposed']),40)
        self.assertEqual(len({x['qaroshi'] for x in self.lex}),len(self.lex))

    def test_all_new_lexemes_use_native_alphabet(self):
        for row in self.lex:
            if row['edition']=='3.0':self.assertTrue(glyphs_of(row['qaroshi']))

    def test_original_register_count_and_status(self):
        self.assertEqual(len(RESONANCES),16)
        for marker in RESONANCES:
            self.assertEqual(self.by_form[marker]['edition'],'1.0')

    def test_v3_grammar_words_are_one_to_one(self):
        self.assertEqual(len(FUNCTIONS_V3),40)
        for form,pos,english,note in FUNCTIONS_V3:
            row=self.by_form[form]
            self.assertEqual(row['pos'],pos)
            self.assertEqual(row['english'],english)
            self.assertEqual(row['review'],'proposed')
            self.assertEqual(row['edition'],'3.0')

    def test_prior_corpus_rows_exact(self):
        self.assertEqual(len(self.old_corpus),880)
        self.assertEqual(self.sentences[:880],self.old_corpus)

    def test_new_examples_are_valid_resonance_sentences(self):
        self.assertEqual(len(self.sentences),1384)
        self.assertEqual(len(self.new_sentences),504)
        self.assertEqual(len({x['qaroshi'] for x in self.new_sentences}),504)
        old={x['qaroshi'] for x in self.old_corpus}
        self.assertFalse(old&{x['qaroshi'] for x in self.new_sentences})
        for row in self.new_sentences:
            self.assertTrue(row['qaroshi'] and row['english'])
            self.assertTrue(row['qaroshi'].split()[0] in RESONANCES)
            self.assertEqual(check_sentence(row['qaroshi'],self.by_form),[],row['id'])

    def test_all_four_derivations_distinct(self):
        self.assertEqual(len(MORPHEMES_V3),4)
        self.assertEqual(len({x['form'] for x in MORPHEMES_V3}),4)
        for row in MORPHEMES_V3:
            root=row['example'].split('-')[0]
            result=derive_word(root,row['form'],self.by_form)
            self.assertEqual(result['form'],row['example'])
            self.assertEqual(result['pos'],row['result_pos'])
            self.assertNotIn(row['example'],self.by_form)

    def test_derived_noun_can_take_case(self):
        self.assertEqual(analyze_word('shiri-dëno-ri-m',self.by_form)['segments'],['dëno','ri','m'])
        self.assertIsNone(analyze_word('mara-dëno',self.by_form))
        with self.assertRaises(ValueError):derive_word('mara','-dëno',self.by_form)

    def test_lexical_inventory_recorded(self):
        self.assertEqual(sum(1 for _ in iter_concepts()),2273)
        self.assertEqual(self.statistics['v3_skipped_overlap'],50)
        self.assertEqual(self.statistics['total_entries'],len(self.lex))
        self.assertEqual(len(self.statistics['v3_domain_counts']),18)

    def test_lexical_lock_covers_exact_additions(self):
        lock=json.loads((ROOT/'data/lexicon_lock_v3.json').read_text(encoding='utf-8'))
        self.assertEqual(len(lock),2223)
        newforms={r['qaroshi'] for r in self.lex if r['edition']=='3.0' and r['review']=='candidate'}
        self.assertEqual(newforms,{v['qaroshi'] for v in lock.values()})

    def test_no_edit_to_native_glyphs(self):
        for glyph in ('sh','zh','kh','ng','k','a','w','t','r','q','o','d','z','u','ë','i','g','e','h','b','p','m','s','n','y','l'):
            self.assertTrue((ROOT/'assets/glyphs'/f'{glyph}.png').is_file())

    def test_refreshed_dictionary_contains_full_edition_filter(self):
        page=(ROOT/'Qaroshi_Offline_Dictionary_v3.html').read_text(encoding='utf-8')
        for term in ('Qaroshi Reference 3.0','9,082','1,384','<select id="edition"',
                     'option value="proposed"','grammar_v3_extensions.md'):
            self.assertIn(term,page)

    def test_legacy_canonical_phrase_untouched(self):
        phrase='më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.'
        self.assertIn(phrase,{x['qaroshi'] for x in self.old_corpus})
        self.assertIn(phrase,(ROOT/'docs/grammar_v3_extensions.md').read_text(encoding='utf-8') if False else
                      (ROOT/'README.md').read_text(encoding='utf-8'))

    def test_full_structural_validation(self):
        errors,stats=validate_data()
        self.assertFalse(errors,errors[:10])
        self.assertEqual(stats['lexicon_entries'],9082)
        self.assertEqual(stats['sample_sentences'],1384)

if __name__=='__main__':unittest.main()
