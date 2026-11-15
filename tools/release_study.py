from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
r=root/'README.md';src=r.read_text(encoding='utf8')
src=src.replace('Unified Standard Reference 5.0','Unified Standard Reference 5.1').replace('Standard Reference 5.0','Standard Reference 5.1')
src=src.replace('The Nardoragon language in one consolidated, offline-first reference:', 'The Nardoragon language in one consolidated, offline-first reference, now with a significantly deeper learning library:')
chunk='''
## Learning library · substantially expanded in 5.1

Open `Qaroshi_Wiki.html` and select **Learn Qaroshi** in the sidebar. This edition introduces a complete learning route while keeping all 16,732 dictionary entries, 3,077 teaching examples, 70 grammar chapters, 16 written resonance markers and 26 original glyphs unchanged.

**New learning materials:**

- **16 graded lessons**: each has ten existing phrasebook examples with IPA, grammar-targeted study instructions, ten active-recall exercises split between both translation directions, revealable answer keys, and form-awareness tasks.
- **16 deep topic guides**: pronunciation; resonance; sentence parsing; nouns and case; verbs; questions; clauses; evidence and scope; number/time; native writing; conversation; technical language; lexicography; grammar repair; Nardoragon social context; and a guided start.
- **21 detailed sentence parses**: role-by-role analyses including cases, suffixes, resonance, questions, quoted statements, evidence and conditional meaning.
- **Practice workbook**: ten deliberate grammatical-error diagnoses and 36 mixed sentence-translation tasks with answer key.
- **70 grammar-chapter study links**: relevant deep guide links appear below existing grammar chapters where topics align.
- **Expanded original references**: the translation, lexicography, pronunciation, native script and wiki-usage documents now include multi-step procedures, contrastive examples, and troubleshooting.

These guides *teach* the established standard rather than revising grammatical rules. All modeled Qaroshi examples in the new lessons come from exact existing corpus IDs. No changes were made to dictionary spellings, glosses, example sentences or glyphs. Broad IPA and English-style sound-out remain available on individual dictionary and example pages.

For a source-browser-friendly version, see `docs/deep_guides/index.md`, the nineteen stand-alone Markdown resources in `docs/deep_guides/`, and `data/learning_library.json`.

'''
src=src.replace('## Vocabulary in this edition',chunk+'## Vocabulary in this edition')
src=src.replace('- `docs/grammar.md`: the canonical 70-chapter grammar, unchanged in its rules.', '- `docs/grammar.md`: the canonical 70-chapter grammar, unchanged in its rules.\n- `docs/deep_guides/`: sixteen topic manuals, sixteen-lesson course, annotated sentence atlas, exercises and answer keys.')
src=src.replace('- `tools/build_wiki.py`: regenerate the standalone HTML.', '- `tools/build_wiki.py`: regenerate the standalone HTML, embedding all learning guides.\n- `tools/deepen_guides.py`: reproducibly builds guided lessons and example-based learning documents from the existing reference corpus.\n- `tools/study_smoke.py`: optional separate end-to-end browser tests for guide pages and mobile behavior.')
src += '\n## Release relationship\n\n5.1 is a pedagogical enrichment of unified reference 5.0. It is **not** a vocabulary or phonology change and has not been pushed to GitHub. The learning guide is source-backed to the internal reference, not a claim of real-world speaker attestation or universal natural-language parity.\n'
r.write_text(src,encoding='utf8')
notes=root/'docs/release_notes.md';t=notes.read_text(encoding='utf8');t=t.replace('Qaroshi Standard 5.0 · Release notes','Qaroshi Standard 5.1 · Deep learning edition')
t=t.replace('## Dictionary and corpus', '''## New in the deep learning edition

- Nineteen integrated learning resources: a 16-lesson progressive course, 16 deep topical guides (including the start guide), a 21-sentence interlinear analysis atlas, and a 46-item editing and translation workbook (ten error diagnoses plus 36 translation questions).
- Every lesson uses ten unchanged corpus examples with IPA and full answer keys. Relevant deep guides appear as links from grammar chapters and the new sidebar Learning section.
- Source guides (translation, writing, pronunciation, lexicography, wiki usage) are substantially longer and feature step-by-step procedures and comparisons.
- Old dictionary words, existing example rows, phoneme inventory, native glyphs, grammar rules and sentence-initial resonance inventory are unchanged.
- All new illustrative sentences in the graded course and atlas are drawn from stable internal corpus references. Deliberately incorrect examples in the editing workbook are explicitly labeled as mistakes.

## Dictionary and corpus''')
notes.write_text(t,encoding='utf8')
info=root/'RELEASE_INFO.json';obj=json.loads(info.read_text(encoding='utf8'));obj.update({'standard':'Qaroshi Unified Standard Reference 5.1','version':'5.1','release_focus':'deep learning guides','new_dictionary_entries':0,'new_example_sentences':0,'guided_lessons':16,'deep_topic_guides':16,'learning_library_resources':19,'annotated_sentence_parses':21,'mixed_workbook_translation_tasks':36,'error_diagnosis_tasks':10});obj['interface']['style']='reading-first, responsive wiki with deep-learning library';info.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('updated metadata')
