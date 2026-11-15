import csv,json,re,unittest,sys,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from phonetics import ipa_word,guide_word,ipa_text,guide_text,sound_out_word,sound_out_text,IPA,graphemes
def rows(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
class QaroshiFinalReference(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.words=rows('data/lexicon.csv')
  cls.sentences=rows('corpus/parallel_sentences.csv')
  cls.grammar=(ROOT/'docs/grammar.md').read_text(encoding='utf-8')
  cls.html=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf-8')
 def test_dictionary_size(self):self.assertEqual(len(self.words),30000)
 def test_dictionary_headwords_unique(self):self.assertEqual(len(set(x['qaroshi'] for x in self.words)),len(self.words))
 def test_dictionary_ids_unique(self):self.assertEqual(len(set(x['id'] for x in self.words)),len(self.words))
 def test_dictionary_schema_unified(self):self.assertEqual(set(self.words[0]),{'id','qaroshi','pos','english','domain','type','components','note','ipa','reading','sound_out'})
 def test_dictionary_no_status_or_edition(self):self.assertNotIn('review',self.words[0]);self.assertNotIn('edition',self.words[0])
 def test_glosses_nonempty(self):self.assertTrue(all(x['english'].strip() for x in self.words))
 def test_dictionary_json_same(self):self.assertEqual(json.loads((ROOT/'data/lexicon.json').read_text()),self.words)
 def test_original_phrase_preserved(self):
  self.assertTrue(any(x['qaroshi']=='më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.' for x in self.sentences))
 def test_phrase_count(self):self.assertEqual(len(self.sentences),4383)
 def test_phrase_ids_unique(self):self.assertEqual(len(set(x['id'] for x in self.sentences)),4383)
 def test_phrase_json_same(self):self.assertEqual(json.loads((ROOT/'corpus/parallel_sentences.json').read_text()),self.sentences)
 def test_phrase_schema_unified(self):self.assertNotIn('edition',self.sentences[0]);self.assertIn('ipa',self.sentences[0]);self.assertIn('reading',self.sentences[0])
 def test_70_chapters(self):self.assertEqual([int(x) for x in re.findall(r'^## (\d+)\.',self.grammar,re.M)],list(range(1,91)))
 def test_glyph_inventory(self):self.assertEqual(len(list((ROOT/'assets/glyphs').glob('*.png'))),26)
 def test_resonances(self):
  obj=json.loads((ROOT/'data/resonances.json').read_text());self.assertEqual(len(obj),16)
 def test_granular_particles(self):
  obj=json.loads((ROOT/'data/grammatical_particles.json').read_text())
  self.assertEqual(len(obj),96);self.assertEqual(len({a['form'] for a in obj}),96)
  for x in obj:self.assertIn(x['form'],{a['qaroshi'] for a in self.words})
 def test_english_index(self):self.assertGreaterEqual(len(rows('data/english_index.csv')),30000)
 def test_offline_html_embed(self):
  self.assertIn('id="wiki-data"',self.html);self.assertIn('id="leftSidebar"',self.html)
  self.assertIn('id="mainContent"',self.html);self.assertIn('id="scriptInput"', (ROOT/'web/qaroshi.js').read_text())
 def test_wiki_no_review_controls(self):
  self.assertNotIn('wordStatus',self.html);self.assertNotIn('wordEdition',self.html)
  self.assertNotIn('phraseEdition',self.html);self.assertNotIn('w.review',self.html)
 def test_no_legacy_grammars(self):self.assertEqual(len(list((ROOT/'docs').glob('grammar*.md'))),1)
 def test_release_description(self):
  self.assertIn('Qaroshi Wiki · Release 17',(ROOT/'README.md').read_text())
 def test_sample_headwords(self):
  w={r['qaroshi']:r['english'] for r in self.words}
  for x in ['qaro','qaroshi','pëla','lësha','qor','sen','zha','womaro','riqosha']:
   self.assertIn(x,w)
class QaroshiIPAReference(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.words=rows('data/lexicon.csv')
  cls.sentences=rows('corpus/parallel_sentences.csv')
  cls.index=rows('data/english_index.csv')
 def test_26_phonemes(self):
  d=json.loads((ROOT/'data/phoneme_inventory.json').read_text())
  self.assertEqual(len(d),26)
  self.assertEqual(set(IPA),set(x['glyph'] for x in d))
  for item in d:self.assertEqual(item['ipa'],'/'+IPA[item['glyph']]+'/')
 def test_digraphs_one_letter(self):
  self.assertEqual(graphemes('shazhakhng'),['sh','a','zh','a','kh','ng'])
 def test_examples_ipa(self):
  self.assertEqual(ipa_word('qaroshi'),'/qa.ˈɾo.ʃi/')
  self.assertEqual(ipa_word('gëro'),'/ˈɡə.ɾo/')
  self.assertEqual(ipa_word('dërawa'),'/də.ˈɾa.wa/')
  self.assertEqual(ipa_word('mi-na'),'/ˈmi.na/')
  self.assertEqual(ipa_word('khura'),'/ˈxu.ɾa/')
  self.assertEqual(ipa_word('ti'),'/ti/')
  self.assertEqual(guide_word('lësha'),'LË-sha')
 def test_source_sentence(self):
  example='sen mi-na gëro dërawa.'
  self.assertEqual(ipa_text(example),'/sen ˈmi.na ˈɡə.ɾo də.ˈɾa.wa/')
  self.assertEqual(guide_text(example),'sen MI-na GË-ro dë-RA-wa.')
 def test_every_word_annotated_correctly(self):
  for item in self.words:
   word=item['qaroshi']
   self.assertEqual(item['ipa'],ipa_word(word),word)
   self.assertEqual(item['reading'],guide_word(word),word)
   self.assertEqual(item['sound_out'],sound_out_word(word),word)
 def test_every_sentence_annotated_correctly(self):
  for item in self.sentences:
   line=item['qaroshi']
   self.assertEqual(item['ipa'],ipa_text(line),line)
   self.assertEqual(item['reading'],guide_text(line),line)
   self.assertEqual(item['sound_out'],sound_out_text(line),line)
 def test_bilingual_index_pronunciation(self):
  words={row['qaroshi']:row for row in self.words}
  self.assertEqual(len(self.index),30768)
  for row in self.index:
   self.assertEqual(row['ipa'],words[row['qaroshi']]['ipa'])
   self.assertEqual(row['reading'],words[row['qaroshi']]['reading'])
   self.assertEqual(row['sound_out'],words[row['qaroshi']]['sound_out'])
 def test_grammatical_inventory_ipa(self):
  for file,key in [('pronouns.json','form'),('resonances.json','marker'),('morphemes.json','form'),('grammatical_particles.json','form')]:
   for x in json.loads((ROOT/'data'/file).read_text()):
    self.assertEqual(x['ipa'],ipa_word(x[key].strip('-')))
    self.assertEqual(x['reading'],guide_word(x[key].strip('-')))
    self.assertEqual(x['sound_out'],sound_out_word(x[key].strip('-')))
 def test_pronunciation_guide(self):
  t=(ROOT/'docs/pronunciation.md').read_text()
  for s in ('/qa.ˈɾo.ʃi/','/q/','/ɾ/','/ʃ/','/ŋ/','penultimate','dërawa'):
   self.assertIn(s,t)
 def test_pronunciation_wiki_coverage(self):
  html=(ROOT/'Qaroshi_Wiki.html').read_text()
  js=(ROOT/'web/qaroshi.js').read_text()
  self.assertIn('ipaText(value)',js)
  self.assertIn('pronunciation(w)',js)
  self.assertIn('pronunciation(p)',js)
  self.assertIn('D.phonemes[i].ipa',js)
  self.assertIn('Pronunciation & IPA',js)
  self.assertIn('sen mi-na gëro dërawa.',(ROOT/'docs/pronunciation.md').read_text())
  self.assertIn('"ipa":"/qa.ˈɾo.ʃi/"',html)
 def test_resonances_preserved(self):
  arr=json.loads((ROOT/'data/resonances.json').read_text())
  self.assertEqual({x['marker'] for x in arr},set('më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher'.split()))
 def test_affix_pronunciation(self):
  a=json.loads((ROOT/'data/affixes.json').read_text())
  self.assertGreaterEqual(len(a),29)
  for x in a:
   self.assertEqual(x['ipa'],ipa_word(x['form'].lstrip('-')))
   self.assertEqual(x['reading'],guide_word(x['form'].lstrip('-')))
   self.assertEqual(x['sound_out'],sound_out_word(x['form'].lstrip('-')))
 def test_no_review_badges(self):
  js=(ROOT/'web/qaroshi.js').read_text()
  for s in ('wordStatus','wordEdition','phraseEdition'):self.assertNotIn(s,js)

class LatinAlphabetReference(unittest.TestCase):
 def test_all_26_latin_letters_covered(self):
  letters=json.loads((ROOT/'data/latin_alphabet.json').read_text())
  self.assertEqual(''.join(x['latin_upper'] for x in letters),'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  self.assertEqual(len({x['english_name_ipa_us'] for x in letters}),26)
 def test_unused_latin_letters_explicit(self):
  letters=json.loads((ROOT/'data/latin_alphabet.json').read_text())
  self.assertEqual({x['latin_upper'] for x in letters if not x['in_qaroshi']},{'C','F','J','V','X'})
  self.assertEqual(sum(x['in_qaroshi'] for x in letters),21)
 def test_native_mapping_unchanged(self):
  letters=json.loads((ROOT/'data/latin_alphabet.json').read_text())
  ipa={x['glyph']:x['ipa'] for x in json.loads((ROOT/'data/phoneme_inventory.json').read_text())}
  for x in letters:
   if x['in_qaroshi']:self.assertEqual(x['qaroshi_phoneme_ipa'],ipa[x['latin_lower']])
 def test_latin_guide_and_wiki(self):
  text=(ROOT/'docs/latin_alphabet.md').read_text()
  js=(ROOT/'web/qaroshi.js').read_text()
  html=(ROOT/'Qaroshi_Wiki.html').read_text()
  self.assertIn('Latin A–Z',text)
  self.assertIn('function renderLatin()',js)
  self.assertIn("case 'latin':renderLatin()",js)
  self.assertIn('id="wiki-data"',html)
  self.assertIn('"latin_upper":"Z"',html)
 def test_base_word_counts_unchanged(self):
  self.assertEqual(len(rows('data/lexicon.csv')),30000)
  self.assertEqual(len(rows('corpus/parallel_sentences.csv')),4383)

class DictionaryPronunciationPatch(unittest.TestCase):
 def test_soundout_examples(self):
  self.assertEqual(sound_out_word('gëro'), 'GUH-roh')
  self.assertEqual(sound_out_word('dërawa'),'duh-RAH-wah')
  self.assertEqual(sound_out_word('qaroshi'),'qah-ROH-shee')
  self.assertEqual(sound_out_text('sen mi-na gëro dërawa.'),'sehn MEE-nah GUH-roh duh-RAH-wah.')
 def test_word_details_prominent(self):
  js=(ROOT/'web/qaroshi.js').read_text(encoding='utf-8')
  self.assertIn('How to pronounce ${esc(w.qaroshi)}',js)
  self.assertIn('Say it (English-style)',js)
  self.assertIn('Latin letters &amp; their Qaroshi sounds',js)
  self.assertIn('letterBreakdown(w.qaroshi)',js)
 def test_script_converter_and_phrasebook(self):
  js=(ROOT/'web/qaroshi.js').read_text(encoding='utf-8')
  self.assertIn('soundOutText(value)',js)
  self.assertIn('pronunciation(p)',js)
 def test_every_word_has_soundout(self):
  for r in rows('data/lexicon.csv'):
   self.assertTrue(r['sound_out'].strip())
 def test_unchanged_vocabulary_and_corpus_size(self):
  self.assertEqual(len(rows('data/lexicon.csv')),30000)
  self.assertEqual(len(rows('corpus/parallel_sentences.csv')),4383)

class QaroshiFifthEdition(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.words=rows('data/lexicon.csv')
  cls.phrases=rows('corpus/parallel_sentences.csv')
  cls.new=[x for x in cls.words if x['id'].startswith('Q5') and not x['id'].startswith('Q530')]
  cls.old=[x for x in cls.words if not x['id'].startswith(('Q5','Q60'))]
  cls.old_phrases=[x for x in cls.phrases[:3183] if not x['id'].startswith('S5')]
  cls.info=json.loads((ROOT/'data/legacy_standard_4_3_1_digest.json').read_text())
 @staticmethod
 def digest(rows):
  return hashlib.sha256(json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 def test_old_lexicon_byte_equivalent_records(self):
  self.assertEqual(len(self.old),11878)
  self.assertEqual(self.digest(self.old),self.info['lexicon_previous_sha256'])
 def test_old_phrasebook_byte_equivalent_records(self):
  self.assertEqual(len(self.old_phrases),2017)
  self.assertEqual(self.digest(self.old_phrases),self.info['phrasebook_previous_sha256'])
 def test_new_vocabulary_count(self):self.assertEqual(len(self.new),4854)
 def test_new_words_types(self):
  self.assertEqual(collections.Counter(x['type'] for x in self.new),{'headword':2122,'compound':2732})
 def test_total_words_and_phrases(self):
  self.assertEqual(len(self.words),30000);self.assertEqual(len(self.phrases),4383)
 def test_new_root_phonotactics(self):
  for entry in self.new:
   self.assertTrue(graphemes(entry['qaroshi']), entry['qaroshi'])
 def test_compounds_link_to_real_dictionary_words(self):
  spellings={x['qaroshi'] for x in self.words}
  for entry in self.new:
   if entry['type']=='compound':
    parts=entry['components'].split(' + ')
    self.assertEqual(len(parts),2,entry['qaroshi'])
    self.assertTrue(all(part in spellings for part in parts),entry['qaroshi'])
    self.assertEqual(entry['qaroshi'],''.join(parts),entry['qaroshi'])
 def test_new_lexemes_distinct_english_senses(self):
  glosses=[(x['english'].casefold(),x['pos']) for x in self.new]
  self.assertEqual(len(glosses),len(set(glosses)))
 def test_new_phrases_have_required_resonance(self):
  markers=set('më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher'.split())
  self.assertEqual({x['qaroshi'].split()[0] for x in self.phrases}-markers,set())
 def test_new_phrases_include_all_phonetics(self):
  for x in self.phrases[2017:]:
   self.assertEqual(x['ipa'],ipa_text(x['qaroshi']))
   self.assertEqual(x['reading'],guide_text(x['qaroshi']))
   self.assertEqual(x['sound_out'],sound_out_text(x['qaroshi']))
 def test_version_statistics_consistent(self):
  info=json.loads((ROOT/'RELEASE_INFO.json').read_text())
  stats=json.loads((ROOT/'data/statistics.json').read_text())
  for a,b,c in [('dictionary_entries',30000,'dictionary_entries'),('sentences',4383,'sentences')]:
   self.assertEqual(info[a],b);self.assertEqual(stats[c],b)
  self.assertEqual(info['native_letters'],26)
 def test_ui_contains_no_external_links(self):
  html=(ROOT/'Qaroshi_Wiki.html').read_text()
  # All runtime assets are inline and loaded without remote dependencies.
  self.assertNotIn('src="https://',html)
  self.assertNotIn('href="https://fonts',html)
  self.assertIn('class="home-hero"',(ROOT/'web/qaroshi.js').read_text())
 def test_dictionary_search_accent_insensitivity(self):
  js=(ROOT/'web/qaroshi.js').read_text()
  self.assertIn("normalize('NFD')",js)
  self.assertIn('lexicalSearch',js)
 def test_examples_use_exact_token_index(self):
  js=(ROOT/'web/qaroshi.js').read_text()
  self.assertIn('exampleByHeadword',js)
  self.assertNotIn("P.filter(p=>p.qaroshi.includes(w.qaroshi))",js)
 def test_long_words_have_collapsible_phonemes(self):
  self.assertIn('class="sound-detail"',(ROOT/'web/qaroshi.js').read_text())
 def test_original_26_glyph_images_preserved(self):
  self.assertEqual(len(list((ROOT/'assets/glyphs').glob('*.png'))),26)
 def test_all_entries_have_real_phonetic_ipa(self):
  for row in self.new:self.assertEqual(row['ipa'],ipa_word(row['qaroshi']))
 def test_english_index_tracks_all_new_words(self):
  idx=rows('data/english_index.csv');self.assertEqual(len(idx),30768)
  present={x['qaroshi'] for x in idx}
  self.assertTrue(all(x['qaroshi'] in present for x in self.new))
 def test_3k_phrasebook_has_no_missing_english(self):
  self.assertTrue(all(x['english'].strip() for x in self.phrases))
 def test_grammar_and_script_unchanged(self):
  self.assertEqual(len(re.findall(r'^## \d+\.',(ROOT/'docs/grammar.md').read_text(),flags=re.M)),90)
  self.assertEqual(len(json.loads((ROOT/'data/phoneme_inventory.json').read_text())),26)
 def test_documentation_explains_compounds_and_limitations(self):
  t=(ROOT/'docs/lexicography.md').read_text()
  for s in ('modifier–head','penultimate','corpus','IPA'):self.assertIn(s,t)

class DeepStudyEdition(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.index=json.loads((ROOT/'docs/deep_guides/guide_index.json').read_text(encoding='utf8'))
  cls.library=json.loads((ROOT/'data/learning_library.json').read_text(encoding='utf8'))
  cls.js=(ROOT/'web/qaroshi.js').read_text(encoding='utf8')
  cls.html=(ROOT/'Qaroshi_Wiki.html').read_text(encoding='utf8')
 def test_nineteen_study_pages(self):self.assertEqual(len(self.index),28)
 def test_unique_study_ids(self):self.assertEqual(len({x['id'] for x in self.index}),28)
 def test_study_paths_present(self):
  self.assertTrue(all((ROOT/x['path']).is_file() for x in self.index))
 def test_sixteen_learning_lessons(self):
  t=(ROOT/'docs/deep_guides/graded_course.md').read_text(encoding='utf8')
  self.assertEqual(len(re.findall(r'^## Lesson \d{2}',t,re.M)),16)
 def test_sixteen_course_keys(self):
  t=(ROOT/'docs/deep_guides/graded_course.md').read_text(encoding='utf8')
  self.assertEqual(t.count('Teacher answer key: open only after completing A and B'),16)
 def test_sentence_atlas_21_parses(self):
  t=(ROOT/'docs/deep_guides/sentence_atlas.md').read_text(encoding='utf8')
  self.assertEqual(len(re.findall(r'^## \d+\.',t,re.M)),21)
 def test_workbook_has_10_traps(self):
  t=(ROOT/'docs/deep_guides/workbook.md').read_text(encoding='utf8')
  self.assertEqual(len(re.findall(r'^### Trap \d+',t,re.M)),10)
 def test_workbook_mixed_assessment_36(self):
  t=(ROOT/'docs/deep_guides/workbook.md').read_text(encoding='utf8')
  part=t.split('## Mixed translation assessment',1)[1].split('<details>',1)[0]
  self.assertEqual(len(re.findall(r'^\d+\.',part,re.M)),36)
 def test_topic_guides_have_documented_examples(self):
  for x in self.index:
   t=(ROOT/x['path']).read_text(encoding='utf8')
   self.assertGreater(len(t),3500,x['id'])
 def test_example_ids_are_in_corpus(self):
  ids={x['id'] for x in rows('corpus/parallel_sentences.csv')}
  t=(ROOT/'docs/deep_guides/graded_course.md').read_text(encoding='utf8')
  self.assertTrue(set(re.findall(r'\bS(?:\d[A-Z]\d{5}|\d{6}|\d{5})\b',t))<=ids)
 def test_wiki_embeds_guide_content(self):
  for s in ('Learn Qaroshi','Start here: a structured route','Qaroshi graded course','Sentence atlas','Teacher answer key'):
   self.assertTrue(s in self.html or s in self.js,s)
 def test_wiki_learning_route(self):self.assertIn("case 'learn':renderLearn();break;",self.js)
 def test_wiki_chapter_related_guides(self):self.assertIn('class="chapter-further"',self.js)
 def test_wiki_has_answer_disclosures(self):self.assertIn(r'\u003cdetails',self.html)
 def test_integrity_counts_preserved(self):
  self.assertEqual(self.library['dictionary_unchanged'],16732)
  self.assertEqual(self.library['corpus_unchanged'],3077)
  self.assertEqual(self.library['new_grammar_rules'],0)
 def test_release_state(self):
  self.assertEqual(json.loads((ROOT/'RELEASE_INFO.json').read_text())['version'],'7.0')
 def test_study_browser_script(self):self.assertTrue((ROOT/'tools/study_smoke.py').is_file())

if __name__=='__main__': unittest.main()

