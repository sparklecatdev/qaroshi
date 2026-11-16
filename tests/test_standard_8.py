"""Current Standard 8 integrity and no-fabrication acceptance tests."""
import csv,gzip,hashlib,importlib.util,json,subprocess,sys,unittest,itertools
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def csvrows(p):
 with Path(p).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
sys.path.insert(0,str(ROOT/'tools/standard_8'))
from scope import analyze,evaluate
from score_comprehension import blank,score

class StandardEight(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.m=json.loads((ROOT/'data/standard_8/release_manifest.json').read_text())
  cls.verb=csvrows(ROOT/'data/standard_8/verb_audit_400.csv')
  cls.comp=csvrows(ROOT/'data/standard_8/compound_risk_register.csv')
  cls.lexdec=csvrows(ROOT/'data/standard_8/lexical_decisions.csv')
  cls.scope=json.loads((ROOT/'data/standard_8/complex_scope_examples.json').read_text())
  cls.truth=json.loads((ROOT/'data/standard_8/formal_scope_truth_models.json').read_text())
  cls.prompt=csvrows(ROOT/'data/standard_8/blind_comprehension_prompts.csv')
  cls.key=csvrows(ROOT/'data/standard_8/sealed_answer_key.csv')
  cls.oldlex=csvrows(ROOT/'data/lexicon.csv')
  with gzip.open(ROOT/'data/standard_8/dictionary_30001.csv.gz','rt',encoding='utf8') as f:
   cls.newlex=list(csv.DictReader(f))
  cls.oldcorpus={r['id']:r for r in csvrows(ROOT/'corpus/parallel_sentences.csv')}
  with gzip.open(ROOT/'data/standard_8/dictionary_enriched_30001.csv.gz','rt',encoding='utf8') as f:
   cls.enriched=list(csv.DictReader(f))

 def test_dictionary_preserves_all_30000_entries(self):
  self.assertEqual(len(self.oldlex),30000);self.assertEqual(self.newlex[:30000],self.oldlex)
 def test_overlay_one_new_word(self):
  self.assertEqual(len(self.newlex),30001);self.assertEqual(self.newlex[-1]['qaroshi'],'nëgëra');self.assertEqual(self.newlex[-1]['id'],'Q8D001')
 def test_no_duplicate_id_or_spelling(self):
  for key in ('id','qaroshi'):self.assertEqual(len(set(x[key] for x in self.newlex)),len(self.newlex))
 def test_legacy_29_source_hashes_intact(self):
  data=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())['sha256'];self.assertEqual(len(data),29)
  for path,sha in data.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha,path)
 def test_consolidated_90_chapters(self):
  import re
  s=(ROOT/'docs/standard_8/grammar.md').read_text(encoding='utf8');numbers=[int(x) for x in re.findall(r'^## (\d+)\.',s,re.M)]
  self.assertEqual(numbers,list(range(1,91)));self.assertIn('30,001',s)
 def test_key_supersessions_integrated_in_main_grammar(self):
  s=(ROOT/'docs/standard_8/grammar.md').read_text(encoding='utf8');
  for t in ('`-za`','`nëgëra`','linear surface scope','individually documented','historical'):
   with self.subTest(term=t):self.assertIn(t,s)
 def test_400_exact_verb_decisions(self):
  self.assertEqual(len(self.verb),400);self.assertEqual(len({x['lemma'] for x in self.verb}),400)
 def test_25_manual_frames_remain_reviewed(self):
  self.assertEqual(sum(r['decision']=='fully_reviewed_general_frame' for r in self.verb),25)
 def test_other_375_no_general_claim(self):
  self.assertEqual(sum(x['general_frame_review'].startswith('no') for x in self.verb),375)
 def test_all_examples_have_exact_corpus_citations(self):
  for x in self.verb:
   if x['example_source_id']:
    z=self.oldcorpus[x['example_source_id']]
    self.assertEqual(z['qaroshi'],x['example_qaroshi'])
    self.assertEqual(z['english'],x['example_english'])
 def test_verb_review_status_specific(self):
  self.assertEqual(Counter(x['decision'] for x in self.verb),self.m['verb_decisions'])
 def test_at_least_375_verb_sources_checked(self):
  self.assertGreaterEqual(sum(bool(x['example_source_id']) for x in self.verb),375)
 def test_compound_review_queue(self):
  self.assertEqual(len(self.comp),3108);self.assertEqual(len({x['canonical_id'] for x in self.comp}),3108)
 def test_lexical_editorial_decisions(self):
  self.assertEqual(len(self.lexdec),52)
  self.assertEqual(sum('retain canonical' in x['decision'] for x in self.lexdec),12)
 def test_confusing_nail_file_explicitly_disambiguated(self):
  x=next(y for y in self.lexdec if y['canonical_word']=='bekazoshërawëlon')
  self.assertIn('abrasive',x['adopted_sense_constraint']);self.assertIn('digital',x['adopted_sense_constraint'])
 def test_no_spelling_renames(self):
  self.assertTrue(all(x['change_to_spelling']=='none' for x in self.lexdec))
 def test_all_24_compositional_scope_examples(self):
  self.assertEqual(len(self.scope),24)
  for s in self.scope:self.assertEqual(analyze(s['qaroshi'])['logical_form'],s['logical_form'])
 def test_surface_order_changes_scopal_meaning(self):
  a=analyze('sen shërano qaro ngënao mara-m tika.')
  b=analyze('sen ngënao mara-m shërano qaro tika.')
  self.assertTrue(a['supported'] and b['supported']);self.assertNotEqual(a['logical_form'],b['logical_form'])
 def test_quantifier_scope_truth_differs(self):
  m=[[True,False],[False,True]]
  self.assertFalse(evaluate('shërano|ngënao|yes|no',m))
  self.assertTrue(evaluate('ngënao|shërano|no|no',m))
 def test_finite_models_cover_all_binary_2x2_relations(self):
  self.assertEqual(len(self.truth),16)
  self.assertEqual(len({x['relation_bits'] for x in self.truth}),16)
 def test_scope_outside_support_abstains(self):
  bad=['sen shërano qaro goro.','sen nëgëra qaro nëgëra mara-m tika.',
   'sen shërano qaro ngënao mara-m nu tika-yu.',
   'sen ngënao qaro shërano mara tika.',
   'sen wë shërano qaro ngënao mara-m tika.']
  for x in bad:
   with self.subTest(x=x):self.assertFalse(analyze(x)['supported'])
 def test_correct_case_and_inverted_scope(self):
  self.assertEqual(analyze('sen ngënao mara-m shërano qaro tika.')['roles'],['object','subject'])
 def test_comprehension_prompts_and_key_separate(self):
  self.assertEqual(len(self.prompt),len(self.key));self.assertGreaterEqual(len(self.prompt),250)
  self.assertEqual({x['id'] for x in self.prompt},{x['id'] for x in self.key})
  self.assertTrue(all('correct' not in x for x in self.prompt))
 def test_all_study_answers_present_as_choices(self):
  by={x['id']:x for x in self.key}
  for q in self.prompt:
   self.assertEqual(q['option_'+by[q['id']]['correct']],by[q['id']]['expected_interpretation'])
 def test_no_fake_comprehension_results(self):
  self.assertEqual(self.m['independent_human_test_responses'],0)
  self.assertTrue(all(x['independent_testing_status']=='not administered' for x in self.prompt))
 def test_reviewer_scorer_rejects_no_responses(self):
  import tempfile
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'blank.csv';self.assertEqual(blank(p),len(self.prompt))
   with self.assertRaisesRegex(ValueError,'No responses'):score(p)
 def test_reviewer_scorer_with_real_input(self):
  import tempfile
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'responses.csv';q=self.prompt[0];key=self.key[0]
   with p.open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=['id','choice','reviewer_anonymous_code','comment']);w.writeheader();w.writerow({'id':q['id'],'choice':key['correct'],'reviewer_anonymous_code':'example-anon','comment':''})
   result=score(p);self.assertEqual(result['reviewers'],1);self.assertEqual(result['results'][0]['overall_accuracy'],1.0)
 def test_generated_hashes_match(self):
  for name,hashval in self.m['data_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),hashval,name)
 def test_closed_world_relation_domain_errors(self):
  for f,mat in [('ngënao|shërano|yes|no',[]),('ngënao|shërano|yes|no',[[True],[True,False]])]:
   with self.assertRaises(ValueError):evaluate(f,mat)
 def test_rectangular_inverse_role_order(self):
  m=[[True,False,True],[True,True,False]] # 2 subjects x 3 objects; column 0 has both true
  self.assertTrue(evaluate('shërano|ngënao|no|no',m))
 def test_enriched_dictionary_source_annotations(self):
  self.assertEqual(len(self.enriched),30001)
  by={x['qaroshi']:x for x in self.enriched}
  self.assertIn('abrasive',by['bekazoshërawëlon']['current_lexical_sense_constraint'])
  self.assertTrue(by['tika']['verb_role_license'])
  self.assertIn('nëgëra',by)
 def test_current_reference_removes_obsolete_agent_instruction(self):
  grammar=(ROOT/'docs/standard_8/grammar.md').read_text(encoding='utf8')
  self.assertNotIn('If you need to identify the agent of a passive, use `-shi`',grammar)
  self.assertIn('| `-za` | passive agent',grammar)
 def test_full_deterministic_rebuild(self):
  # The build is deterministic; its own manifest lists output SHA-256 values.
  before={k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in self.m['data_sha256']}
  subprocess.run([sys.executable,str(ROOT/'tools/standard_8/build_standard.py')],check=True,cwd=ROOT,stdout=subprocess.DEVNULL)
  after={k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in self.m['data_sha256']}
  self.assertEqual(before,after)
 def test_release_has_no_independent_attestation(self):
  s=(ROOT/'docs/standard_8/REVIEW_PROTOCOL.md').read_text(encoding='utf8')
  self.assertIn('zero',s);self.assertIn('blind',s)

if __name__=='__main__':unittest.main()
