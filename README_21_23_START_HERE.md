# Qaroshi 21–23: Translation, Immersion & Learner Lab

The practical goal is to go from **finding an exact expression** to **reading connected text** to **testing recall and documenting ambiguity**, without inventing new official words or making false claims about real speakers.

## Start

Open `Qaroshi_21_23_Translation_Immersion_Academy.html` in a modern browser. This single file contains all the data required for its interface and works offline. **In a Git checkout**, first run `python tools/v21_23/restore_artifacts.py` to restore the standalone HTML and precomputed data from the committed compressed archives. GitHub Pages publishes the already-restored HTML as a normal link. On a phone, all six sections appear in an accessible two-row navigation layout. Click highlighted words anywhere to follow links to the canonical dictionary. Use Ctrl+K / Cmd+K for global search.

### 21.0 Translation & Meaning

- **5,249 documented bilingual records**: 4,383 canonical controlled reference examples, 561 lines from the independent v15 editorial anthology, and 305 lines from earlier editorial short readings. All text is preserved from its original source.
- The online/offline **browser** provides **exact-source bilingual lookup**, alternative contextual equivalents, pronunciation, related examples clearly labeled as **NOT translations**, and lexical links. It does **not** automatically invent a sentence outside the recorded examples.
- The Python command-line tool adds a **bounded morphology-aware grammar engine** from the existing v11 standard. This yields **provisional** interpretations only when the rules are supported. It explicitly abstains on unlicensed input.
- The 103 source/context translation-ambiguity cases from v14 remain on a visible review board; no proposed correction is silently ratified.

CLI:

```bash
python tools/v21_23/translator.py 'hë ti haro he?' --direction to-en
python tools/v21_23/translator.py 'I am well.' --direction to-qr
python tools/v21_23/translator.py 'I drink water.' --direction to-qr --resonance sen
```

### 22.0 Immersion Reader

- **108 pre-existing, independently authored/editorial readings** with **866 source lines**: 85 v15 pieces, 18 earlier anthology pieces and 5 curated short readings.
- Each line retains its own original bilingual pair, IPA, sound-out and provenance. Reveal English one sentence at a time, follow root links, or open the exact source phrase.
- Reading bands are **relative complexity heuristics** (35 foundation / 46 developing / 27 stretch), based on core root coverage and average sentence length. They are **not CEFR levels** or empirically calibrated reading times.

### 23.0 Learning & Assessment

- **324 four-way source-aligned recognition questions**, three for each reading. Distractors come from other sentences in the same reading.
- **12 actionable study modules** and personal completion checkboxes, plus notes for each of the 103 translation-review cases.
- Save quizzes and self-reported practice locally; export/import JSON. Nothing is uploaded to an external server.
- A quiz measures recognition of the **recorded contextual English rendering**, **not** full plot comprehension or independently verified language proficiency. A person's suggested QA note is also not ratification.

## Build and validate

Run from the project root:

```bash
python tools/v21_23/build_release.py
python -m unittest discover -s tests -q
python tools/v21_23/browser_smoke.py
```

Browser smoke testing needs Python Playwright and Chromium at `/usr/bin/chromium`; ordinary use of the HTML app does not. The source package contains prior versions, lexicon, corpus, and original glyphs without any compiled font binaries.

## GitHub integration policy

This release adds its own `v21`, `v22`, `v23` and `tools/v21_23` paths, plus a standalone compressed site. It does not replace the already-merged v18/v19/v20 releases, original wiki/academy, live contributor changes, or canonical dictionaries. Rebuilds use the original corpus in the checkout; these are not new speaker recordings or meanings.
