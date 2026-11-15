"""Non-attestation / backwards-compatibility gates for the 18+19 teaching layer."""
import csv
import gzip
import hashlib
import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D18 = ROOT / 'data/v18'
D19 = ROOT / 'data/v19'
MANIFEST = ROOT / 'data/v18_19_manifest.json'
APP = ROOT / 'Qaroshi_18_19_Living_Language_Studio.html'

def rows(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

class LivingLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Restore the byte-identical standalone studio from its checked-in gzip.
        if not APP.exists():
            archive = ROOT / 'Qaroshi_18_19_Living_Language_Studio.html.gz'
            content = gzip.decompress(archive.read_bytes())
            expected = '08531faa297c44e8cbad7339fa3619178438403b549be1118974f4f9ffb1deeb'
            assert hashlib.sha256(content).hexdigest() == expected, 'Studio archive checksum mismatch'
            APP.write_bytes(content)
        cls.m = json.loads(MANIFEST.read_text(encoding='utf-8'))
        cls.dialogues = json.loads((D18/'source_linked_conversation_paths.json').read_text(encoding='utf-8'))
        cls.rules = rows(D18/'pragmatic_register_rules.csv')
        cls.contrasts = rows(D18/'meaning_contrasts.csv')
        cls.review = rows(D19/'reviewed_and_screened_3817.csv')
        cls.lex = rows(ROOT/'data/lexicon.csv')
        cls.lexmap = {r['qaroshi']:r for r in cls.lex}
        cls.h = APP.read_text(encoding='utf-8')
        cls.payload = json.loads(cls.h.split('<script id="qaroshi-payload" type="application/json">',1)[1].split('</script>',1)[0])

    def test_01_canonical_dictionary_size(self):
        self.assertEqual(len(self.lex), 30000)
    def test_02_canonical_examples_size(self):
        self.assertEqual(len(rows(ROOT/'corpus/parallel_sentences.csv')), 4383)
    def test_03_scene_counts(self):
        self.assertEqual(len(self.dialogues),49)
        self.assertEqual(sum(len(x['turns']) for x in self.dialogues),214)
    def test_04_scene_phrases_source_aligned(self):
        phrase = {x['id']:x for x in self.payload['phrase']}
        for scene in self.dialogues:
            for turn in scene['turns']:
                self.assertEqual(turn['qaroshi'],phrase[turn['reference_id']]['q'])
                self.assertEqual(turn['english'],phrase[turn['reference_id']]['e'])
    def test_05_contrast_count_and_ids(self):
        self.assertEqual(len(self.contrasts),32)
        self.assertEqual(len({c['id'] for c in self.contrasts}),32)
    def test_06_rule_count_and_ids(self):
        self.assertEqual(len(self.rules),24)
        self.assertEqual(len({r['id'] for r in self.rules}),24)
    def test_07_no_root_promotion(self):
        self.assertEqual(self.m['canonical_words_added_or_replaced'],0)
        self.assertEqual(sum(x['canonical_adoption']=='yes' for x in self.review),0)
    def test_08_review_count_and_breakdown(self):
        self.assertEqual(len(self.review),3817)
        self.assertEqual(Counter(x['review_tier'] for x in self.review),self.m['review_tiers'])
    def test_09_false_friend_rejections_remain(self):
        self.assertEqual(sum(x['review_tier']=='blocked_false_friend' for x in self.review),12)
        self.assertTrue(all('Do not' in x['teaching_action'] for x in self.review if x['review_tier']=='blocked_false_friend'))
    def test_10_root_curriculum(self):
        paths=rows(D19/'productive_root_curriculum.csv')
        self.assertEqual(len(paths),1914)
        self.assertEqual(len({x['root'] for x in paths}),len(paths))
        self.assertTrue(all(x['root'] in self.lexmap for x in paths))
    def test_11_resonance_preserved(self):
        self.assertEqual(len(json.loads((ROOT/'data/resonances.json').read_text(encoding='utf8'))),16)
    def test_12_app_search_links_present(self):
        for key in ('id="global-search"','id="global-results"','id="breadcrumbs"','id="nav-back"'):
            self.assertIn(key,self.h)
    def test_13_app_phrase_index(self):
        for key in ('id="tab-phrases"','id="phrase-search"','id="phrase-detail"'):
            self.assertIn(key,self.h)
        self.assertEqual(len(self.payload['phrase']),656)
    def test_14_app_semantic_crossrefs(self):
        for key in ('function wordLine','function showWord','function showPhrase','function applyRoute','componentUse'):
            self.assertIn(key,self.h)
    def test_15_dictionary_matches_payload(self):
        self.assertEqual(len(self.payload['lex']),len(self.lex))
        self.assertEqual(self.payload['lex'][0]['w'],self.lex[0]['qaroshi'])
    def test_16_pronunciation_grounded(self):
        phon=rows(D18/'pronunciation_reading_93.csv')
        self.assertEqual(len(phon),93)
        self.assertTrue(all(x['human_audio_available']=='no' for x in phon))
    def test_17_study_paths_and_reply_drills(self):
        self.assertEqual(len(self.payload['paths']),10)
        self.assertEqual(len(self.payload['replyDrills']),30)
    def test_18_source_review_distinction(self):
        self.assertIn('not independently attested',self.h)
        self.assertIn('not approved replacements',self.h)
    def test_19_native_symbol_mapping_preserved(self):
        glyphs=list((ROOT/'assets/glyphs').glob('*.png'))
        self.assertGreaterEqual(len(glyphs),26)
    def test_20_offline_no_external_script_tags(self):
        self.assertNotIn('<script src="http',self.h)
        self.assertNotIn('https://cdn.',self.h)

if __name__=='__main__':unittest.main()
