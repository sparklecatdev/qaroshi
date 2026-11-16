"""Qaroshi 24–27: real morphological addition plus canonical lexical sense refinements."""
import csv
import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/v24_27'))
from fluency11.engine import word_analysis,CASES,NSLOTS,LEX
from validate import validate_sentence

class LinguisticReformTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grammar=(ROOT/'docs/grammar.md').read_text(encoding='utf8')
        with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f:
            cls.lex={r['qaroshi']:r for r in csv.DictReader(f)}
        cls.senses=json.loads((ROOT/'data/semantics/curated_senses.json').read_text(encoding='utf8'))
        cls.frames=json.loads((ROOT/'data/semantics/valency_frames.json').read_text(encoding='utf8'))
        with (ROOT/'data/semantics/lexical_migration_decisions_24_27.csv').open(encoding='utf8',newline='') as f:
            cls.decisions=list(csv.DictReader(f))

    def test_01_dictionary_size_and_no_suffix_as_root(self):
        self.assertEqual(len(self.lex),30000)
        self.assertNotIn('za',self.lex)
    def test_02_grammar_90_chapters(self):
        self.assertEqual([int(x) for x in re.findall(r'^## (\d+)\.',self.grammar,re.M)],list(range(1,91)))
    def test_03_passive_case_in_nominal_slot(self):
        self.assertEqual(CASES['za'],'passive_agent')
        self.assertEqual(NSLOTS['za'],NSLOTS['shi'])
    def test_04_case_with_plural(self):
        a=word_analysis('mara-ri-za');self.assertFalse(a['errors']);self.assertEqual(a['features']['case'],'passive_agent');self.assertEqual(a['features']['number'],'plural')
    def test_05_case_then_topic(self):
        a=word_analysis('mara-za-së');self.assertFalse(a['errors']);self.assertTrue(a['features']['topic'])
    def test_06_one_case_per_noun(self):
        a=word_analysis('mara-za-shi');self.assertTrue(a['errors'])
    def test_07_simple_passive_agent_valid(self):
        r=validate_sentence('sen naro mara-za daru-li-te.');self.assertTrue(r['valid_surface'],r['findings'])
    def test_08_instrument_remains_valid(self):
        r=validate_sentence('sen naro banu-shi daru-li-te.');self.assertTrue(r['valid_surface'])
    def test_09_legacy_ambiguous_warns(self):
        r=validate_sentence('sen naro mara-shi daru-li-te.');self.assertTrue(r['valid_surface']);self.assertIn('R24-002',[x['rule_id'] for x in r['findings']])
    def test_10_active_agent_case_rejected(self):
        r=validate_sentence('sen mi mara-za daru-te.');self.assertFalse(r['valid_surface']);self.assertIn('R24-001',[x['rule_id'] for x in r['findings']])
    def test_11_double_case_rejected(self):
        r=validate_sentence('sen naro mara-za-shi daru-li-te.');self.assertFalse(r['valid_surface']);self.assertIn('R24-005',[x['rule_id'] for x in r['findings']])
    def test_12_multiclause_scope_not_guessed(self):
        r=validate_sentence('sen naro mara-za daru-li-te ara mi goro.');self.assertIn('R24-003',[x['rule_id'] for x in r['findings']]);self.assertNotIn('R24-001',[x['rule_id'] for x in r['findings']])
    def test_13_preexisting_senses_prefix_preserved(self):
        self.assertEqual(len(self.senses),48)
        self.assertEqual([x['id'] for x in self.senses[:26]],[f'LS{i:03d}' for i in range(1,27)])
        self.assertTrue(all(x['status']!='normative semantic clarification 24-27; existing spelling retained' for x in self.senses[:26]))
    def test_14_new_senses_bind_to_existing_ids(self):
        self.assertEqual(len(self.senses[26:]),22)
        for x in self.senses:
            self.assertEqual(x['dict_id'],self.lex[x['lemma']]['id'])
        self.assertEqual(len({x['id'] for x in self.senses}),48)
    def test_15_high_risk_meaning_distinctions(self):
        names={x['lemma']:x['definition'].lower() for x in self.senses[26:]}
        for w,term in [('nashi','romantic'),('tika','knowing'),('mahori','silence'),('pëli','recipient'),('noa','bandwidth')]:
            self.assertIn(term,names[w])
    def test_16_valency_table_preserved(self):
        self.assertEqual(len(self.frames),25)
        for f in self.frames:
            self.assertEqual(f['dict_id'],self.lex[f['lemma']]['id'])
            self.assertTrue(f['required_roles'])
            self.assertIn('disallowed_inferences',f)
    def test_17_transfer_argument_structure(self):
        f=next(x for x in self.frames if x['lemma']=='pëli')
        self.assertIn('object:-m',f['required_roles']);self.assertIn('recipient:-tu',f['required_roles'])
    def test_18_transitive_passive_agents(self):
        for f in self.frames:
            if f['frame']!='V0':self.assertIn('-za',f['passive_agent_case'])
    def test_19_root_decisions_no_adoption(self):
        self.assertEqual(len(self.decisions),65)
        self.assertEqual(Counter(x['decision'] for x in self.decisions),{'trial_no_adoption':44,'hold_ambiguity':9,'rejected_false_friend':12})
        self.assertTrue(all(x['canonical_replacement']=='no' for x in self.decisions))
    def test_20_canonical_root_id_integrity(self):
        for x in self.decisions:self.assertEqual(self.lex[x['existing_word']]['id'],x['existing_word_id'])
    def test_21_language_document_is_normative(self):
        s=(ROOT/'docs/language_reform_24_27.md').read_text()
        for heading in ['24. Explicit passive agency','25. Semantic and argument-structure','26. Negation','27. Morphology']:
            self.assertIn(heading,s)
    def test_22_unapproved_proposals_remain_unapproved(self):
        with (ROOT/'data/v16_2/individually_editorially_reviewed.csv').open(encoding='utf8') as f:
            review=list(csv.DictReader(f))
        self.assertTrue(all(x['proposed_for_dictionary_acceptance']=='no' for x in review))
    def test_23_no_new_phonemes(self):
        a=json.loads((ROOT/'data/phoneme_inventory.json').read_text());self.assertEqual(len(a),26)
    def test_24_negation_scope_documented(self):
        self.assertIn('sen ngënao qaro nu goro.',(ROOT/'docs/language_reform_24_27.md').read_text())
        self.assertIn('sen nura goro.',(ROOT/'docs/language_reform_24_27.md').read_text())
    def test_25_historical_agent_compatibility(self):
        self.assertIn('sen naro mara-shi daru-li-te.',self.grammar)
        self.assertNotIn('old case retired',self.grammar)

if __name__=='__main__':unittest.main()
