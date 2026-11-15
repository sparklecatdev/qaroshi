# Qaroshi Wiki · Release 14

The wiki and Academy include 30,000 dictionary entries, 4,383 examples, and 90 grammar chapters. The [semantic workbench](Qaroshi_14_Semantic_Workbench.html) provides offline editorial review tools; its proposals are not community-ratified. See [release notes](RELEASE_14_NOTES.md).

To rebuild the site, install Pillow and Mistune, then run `python3 tools/build_wiki.py` and `python3 tools/build_academy.py`.

## Historical release notes

The following describes the earlier 5.3 release; counts and version labels below are historical.

# Qaroshi · Unified Standard Reference 5.3

The Nardoragon language in one consolidated, offline-first reference, now with a significantly deeper learning library: **18,663 distinct dictionary entries**, **3,183 bilingual teaching sentences**, **70 numbered grammar chapters**, **16 mandatory written resonance markers**, and **the 26 original handwritten glyphs**.

## Start here

Open **`Qaroshi_Wiki.html`** in a modern browser. It is a **single self-contained HTML file**, with no login, libraries, web requests or tracking for the reference. The AI assistant requires an internet connection and an OpenRouter API key, which is saved unencrypted in the browser. The redesigned wiki has a persistent chapter sidebar, topic browsing, English/Qaroshi search, dictionary entry pages, clickable compound components, a phrasebook, dark mode, mobile navigation, original-script rendering and PNG export.

Every dictionary word page shows **English-style sound-out, broad IPA, stress-marked Qaroshi syllables, and a letter-by-letter sound guide**. Long words offer a collapsible letter-sound grid to keep reading comfortable. The phrasebook and native-script converter show pronunciation as well.


## Learning library · substantially expanded in 5.1

Open `Qaroshi_Wiki.html` and select **Learn Qaroshi** in the sidebar. This edition introduces a complete learning route while keeping all 18,663 dictionary entries, 3,183 teaching examples, 70 grammar chapters, 16 written resonance markers and 26 original glyphs unchanged.

**New learning materials:**

- **16 graded lessons**: each has ten existing phrasebook examples with IPA, grammar-targeted study instructions, ten active-recall exercises split between both translation directions, revealable answer keys, and form-awareness tasks.
- **16 deep topic guides**: pronunciation; resonance; sentence parsing; nouns and case; verbs; questions; clauses; evidence and scope; number/time; native writing; conversation; technical language; lexicography; grammar repair; Nardoragon social context; and a guided start.
- **21 detailed sentence parses**: role-by-role analyses including cases, suffixes, resonance, questions, quoted statements, evidence and conditional meaning.
- **Practice workbook**: ten deliberate grammatical-error diagnoses and 36 mixed sentence-translation tasks with answer key.
- **70 grammar-chapter study links**: relevant deep guide links appear below existing grammar chapters where topics align.
- **Expanded original references**: the translation, lexicography, pronunciation, native script and wiki-usage documents now include multi-step procedures, contrastive examples, and troubleshooting.

These guides *teach* the established standard rather than revising grammatical rules. All modeled Qaroshi examples in the new lessons come from exact existing corpus IDs. No changes were made to dictionary spellings, glosses, example sentences or glyphs. Broad IPA and English-style sound-out remain available on individual dictionary and example pages.

For a source-browser-friendly version, see `docs/deep_guides/index.md`, the nineteen stand-alone Markdown resources in `docs/deep_guides/`, and `data/learning_library.json`.

## Vocabulary in this edition

| Category | Count |
|:--|--:|
| Previously standardized, unchanged entries | 11,878 |
| New standalone lexical entries | 2,122 |
| New transparent modifier–head compounds | 2,732 |
| **Complete unique dictionary** | **16,732** |
| Earlier bilingual teaching sentences, unchanged | 2,017 |
| New teaching sentences | 1,060 |
| **Complete phrasebook** | **3,077** |

New vocabulary covers 35 expansion topics spanning digital infrastructure, communication, privacy, software engineering, medicine, scientific reasoning, Nardoragon flight and roost culture, economics, environmental stewardship, law, education, music, linguistics, and everyday objects.

Each standalone lexical entry is a discrete term or predicate; no ordinary inflected conjugations are included in the dictionary count. Compounds are transparently formed from existing dictionary roots, recorded in `components` and cross-linked on word pages. The documentation differentiates a lexicalized compound from a grammatical inflection; word pairs with different English labels do not automatically mean identical senses.

The new examples are deliberately controlled learning examples, not transcripts of naturally sampled Nardoragon conversations. IPA is rule-derived phonemic transcription, with **English-style approximations** kept separate from exact native sound values. This edition standardizes the written reference, not the usage rates of an independently sampled speaker community.


## Living speech and explicit vocabulary · 5.3

This edition integrates 1,931 additional headwords across 29 semantic groups, with direct curses, vulgar slang, adult clinical anatomy, sexuality, consent and relationship vocabulary alongside everyday digital, health, social and civic terms. Individual word entries include IPA, sound-out and a clear usage note. No existing 5.2 headword was edited or deleted. The new corpus includes 106 controlled sentences, all with mandatory resonance and pronunciation.

See `docs/living_speech.md` for a dedicated guide to neutral/clinical versus slang/vulgar registers, consent and boundaries, and example translations. `data/living_speech_additions.csv` is the new-word layer, while `data/living_speech_by_register.csv` provides a register-oriented index. The wiki offers one combined searchable dictionary.

The Academy includes the new words in its searchable dictionary, but keeps explicit/adult/profanity terms out of **random games by default**. Learners can opt into mature practice with a local preference. Ordinary lessons remain the same source-backed 16-lesson sequence.

## Data and guides

- `data/lexicon.csv` / `data/lexicon.json`: unified dictionary with stable identifiers, POS, gloss, domain, root components, usage notes, IPA, reading, and sound-out.
- `data/english_index.csv`: reverse search index including multi-gloss aliases.
- `data/expansion_report.json`: added vocabulary counts and template audit.
- `data/legacy_standard_4_3_1_digest.json`: integrity fingerprint of the complete previous vocabulary and corpus, excluding new 5.0 records.
- `corpus/parallel_sentences.csv` / `.json`: sentence-level English and Qaroshi examples and phonetics.
- `docs/grammar.md`: the canonical 70-chapter grammar, unchanged in its rules.
- `docs/deep_guides/`: sixteen topic manuals, sixteen-lesson course, annotated sentence atlas, exercises and answer keys.
- `docs/lexicography.md`: word formation, derivation, semantic scope and editorial usage.
- `docs/pronunciation.md`, `docs/latin_alphabet.md`, `docs/phonology_and_script.md`: phonetics, Romanization and native writing.
- `assets/glyphs/`: original 26 glyph images, unchanged.
- `web/qaroshi.css`, `web/qaroshi.js`: editable, dependency-free wiki interface source.
- `tools/expand_lexicon_v5.py`: reproducible lexical expansion methodology. **It expects version 4.3.1 source tables as input, and must not be run twice on the same expanded dictionary.**
- `tools/build_wiki.py`: regenerate the standalone HTML, embedding all learning guides.
- `tools/deepen_guides.py`: reproducibly builds guided lessons and example-based learning documents from the existing reference corpus.
- `tools/study_smoke.py`: optional separate end-to-end browser tests for guide pages and mobile behavior.
- `tools/phonetics.py`: deterministic pronunciation functions.
- `tests/test_reference.py`: validation and regression checks.
- `tools/browser_smoke.py`: optional Chromium UI smoke test (requires Playwright).

## Build and test

Requires Python 3.10+ and `Pillow` and `mistune` to regenerate the HTML:

```bash
python -m pip install -r requirements.txt
make build
make test
python tools/phonetics.py 'sen mi-na gëro dërawa.'
# Optional, when Playwright + Chromium are available:
python tools/browser_smoke.py
```

`Qaroshi_Wiki.html` itself needs only a current web browser. The Python tools are unnecessary for everyday reading.

## Pronunciation and integrity

Original words, full glosses, pronunciation records and bilingual examples from 4.3.1 are preserved unmodified. New entries also have complete IPA and sound-out data. Every complete Qaroshi sentence, including examples, begins with one of the 16 resonance markers.

The original handwritten glyph artwork remains the property of its rights holder; no separate copyright license is assumed. This package is a reference archive, not a claim of relicensing the original artwork.

This release is **not a GitHub push**. Copy its files into the repository when ready to publish the update.

## Release relationship

5.1 is a pedagogical enrichment of unified reference 5.0. It is **not** a vocabulary or phonology change . The learning guide is source-backed to the internal reference, not a claim of real-world speaker attestation or universal natural-language parity.

## Academy 5.3 · Interactive language learning

This package also includes **`Qaroshi_Academy.html`**, a second completely standalone offline HTML application, linked from the wiki sidebar. It is a practical learning companion to the reference, not a replacement for the dictionary or full grammar.

- **16 guided lessons**, each with ten established reference sentences, a complete lesson text, phonetics, and a five-question comprehension check.
- **Eight mini-games**: word recognition, reverse vocabulary retrieval, sentence translation, suffixes, written resonance, original-script decoding, word-order construction and IPA recognition.
- **Skyflight**, a ten-question mixed challenge with soft hearts and no timer.
- **Spaced review**, saved words, progress/XP, a beginner-to-complete-dictionary difficulty selector, and local JSON progress import/export.
- **16 in-depth manuals**, full 16,732-entry dictionary, and all 3,077 corpus sentences embedded for fully offline use.
- The original 26 native glyphs, 16 mandatory written resonance markers and existing phonetics are preserved unchanged.

Open `Qaroshi_Academy.html` to play. Read `docs/academy.md` for game rules, accessibility/privacy limitations and regeneration commands. Rebuild with `python tools/build_academy.py`.

**5.2 adds only learning software and documentation.** The dictionary, phrasebook and grammar remain those of Standard 5.1; there is no new lexical content. GitHub is not modified by this archive.
