# Qaroshi · Unified Standard Reference 4.1

**The Nardoragon language**, documented in one unified dictionary, grammar and phrasebook.

## Read the wiki

Open **`Qaroshi_Wiki.html`** in a browser. The file is fully offline and contains the 11,878-entry bilingual dictionary, 2,017 example sentences, all 70 grammar chapters, and the original 26-symbol native writing system. The interface has a wiki-style sidebar, built-in search, topic browsing, a chapter list, dark mode, mobile navigation and native-script PNG export.

## Main reference files

- `data/lexicon.csv` and `.json`: the complete unified dictionary.
- `data/english_index.csv`: English-to-Qaroshi index.
- `data/grammatical_particles.json`: all grammatical function forms in one list.
- `corpus/parallel_sentences.csv` and `.json`: complete phrasebook.
- `docs/grammar.md`: all **70** numbered chapters in one volume.
- `docs/lexicography.md`, `docs/translation.md`, `docs/phonology_and_script.md`: supporting references.
- `assets/`: original Nardoragon glyph artwork.
- `tools/build_wiki.py`: rebuild the self-contained HTML file.
- `tests/test_reference.py`: release consistency tests.

## Build and check

Python 3.10+, Pillow, mistune. Run `python -m pip install -r requirements.txt`, then `make build` and `make test`. The delivered HTML requires only a modern browser.

All documented headwords and grammar forms are presented as part of the **single current reference**, without separate review-state filters. This is a reference edition, not a claim that every documented expression is attested in everyday speech.

No GitHub push is included in this release. Rights to original glyph artwork and project code have not been separately licensed for redistribution.
