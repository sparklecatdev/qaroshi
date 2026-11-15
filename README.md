# Qaroshi · Unified Standard Reference 5.0

The Nardoragon language in one consolidated, offline-first reference: **16,732 distinct dictionary entries**, **3,077 bilingual teaching sentences**, **70 numbered grammar chapters**, **16 mandatory written resonance markers**, and **the 26 original handwritten glyphs**.

## Start here

Open **`index.html`** in a modern browser. It is a **single self-contained HTML file**, with no login or external libraries required for the reference. The AI assistant requires an internet connection and an OpenRouter API key. The redesigned wiki has a persistent chapter sidebar, topic browsing, English/Qaroshi search, dictionary entry pages, clickable compound components, a phrasebook, dark mode, mobile navigation, original-script rendering and PNG export.

Every dictionary word page shows **English-style sound-out, broad IPA, stress-marked Qaroshi syllables, and a letter-by-letter sound guide**. Long words offer a collapsible letter-sound grid to keep reading comfortable. The phrasebook and native-script converter show pronunciation as well.

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

## Data and guides

- `data/lexicon.csv` / `data/lexicon.json`: unified dictionary with stable identifiers, POS, gloss, domain, root components, usage notes, IPA, reading, and sound-out.
- `data/english_index.csv`: reverse search index including multi-gloss aliases.
- `data/expansion_report.json`: added vocabulary counts and template audit.
- `data/legacy_standard_4_3_1_digest.json`: integrity fingerprint of the complete previous vocabulary and corpus, excluding new 5.0 records.
- `corpus/parallel_sentences.csv` / `.json`: sentence-level English and Qaroshi examples and phonetics.
- `docs/grammar.md`: the canonical 70-chapter grammar, unchanged in its rules.
- `docs/lexicography.md`: word formation, derivation, semantic scope and editorial usage.
- `docs/pronunciation.md`, `docs/latin_alphabet.md`, `docs/phonology_and_script.md`: phonetics, Romanization and native writing.
- `assets/glyphs/`: original 26 glyph images, unchanged.
- `web/qaroshi.css`, `web/qaroshi.js`: editable, dependency-free wiki interface source.
- `tools/expand_lexicon_v5.py`: reproducible lexical expansion methodology. **It expects version 4.3.1 source tables as input, and must not be run twice on the same expanded dictionary.**
- `tools/build_wiki.py`: regenerate the standalone HTML.
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

`index.html` itself needs only a current web browser. The Python tools are unnecessary for everyday reading.

## Pronunciation and integrity

Original words, full glosses, pronunciation records and bilingual examples from 4.3.1 are preserved unmodified. New entries also have complete IPA and sound-out data. Every complete Qaroshi sentence, including examples, begins with one of the 16 resonance markers.

The original handwritten glyph artwork remains the property of its rights holder; no separate copyright license is assumed. This package is a reference archive, not a claim of relicensing the original artwork.

The AI assistant requires an internet connection and an OpenRouter API key.
