# Using the current Qaroshi Wiki (9.5)

Open `Qaroshi_Wiki.html` locally, or use the public `index.html` page. The Wiki is a **self-contained, offline-first** reference; its core dictionary, current grammar, interactive workshop and semantic case explorer need no account or network.

## Where to start

The sidebar keeps five primary tasks visible: **Overview**, **Dictionary**, **Write & inspect sentences**, **Learn Qaroshi**, and **Meaning & examples**. The current grammar, topics, phrasebook and native script are immediately below. All individual chapters, deep topic guides, older research workbenches and teaching apps are available in collapsed sections, not removed.

Use the upper search to find dictionary words, examples or chapter text. Press `/` to focus the search. Use `#dictionary` for full lexical search, or `#categories` to browse a small set of subject groups. Expanding an area reveals the original topic labels. Typing a topic name searches across all areas. Historic links such as `#word/gëro`, `#grammar/02` and `#dictionary?domain=...` remain valid.

## The new browser sentence workshop

Open `#workshop`. The **Build a sentence** tab offers guided verb/subject/role selectors, tense, aspect, modality, negation, resonance, and optional second events. A chosen verb reveals only licensed object or recipient types. Press **Compose Qaroshi** to generate and examine the exact grammatical structure. Select **Inspect Qaroshi** to parse an existing sentence in the reviewed subset and see who did what, role markers, evidence source, conditional status, and whether the matrix event is asserted.

The workshop implements **25 source-reviewed verb frames and 10 explicitly typed noun forms**, based on the same 9.3 licenses as the Python reference engine. It intentionally rejects unknown words, unlicensed object types, noncanonical suffix ordering and other unsupported constructions. **A rejection does not imply the broader language cannot express the sentence.** No AI model, API key or server round trip is used for workshop parsing.

## Current grammar and semantic cases

Open `#standard` for the current 9.2 conflict-resolution guide and ten full 8.1–9.1 amendment documents, with all 90 original normative chapters linked through `#grammar`. The original sources remain available through the GitHub repository.

Open `#cases` for **all 500** source-grounded editorial challenge proposals. Search by QS81 case ID, original English, proposed Qaroshi or domain. Each record has a stable individual link, e.g. `#case/QS81-0336`, and shows the current 9.2 corrected editorial draft where applicable. Source English roles are visible as intended meanings. **These are not independently verified translations.** A language learner can try reading the Qaroshi first and compare their interpretation to the source, but that is not a certified human-study result.

## Pronunciation and archive

Open a word for English-style sound-out, IPA, native glyphs, source definition, compound components and related words. The **Native script** page converts Romanized Qaroshi to the original glyphs, not English to Qaroshi, and supports image export. The Academy, spoken-language studio, translation immersion tools and older releases remain accessible through the collapsed sidebar's specialist section and `explore.html`.

## Reproduce the Wiki

```sh
make build
node tests/wiki95/grammar_browser.cjs
python -m unittest tests.test_wiki_9_5 -v
```

All source language files and historical release HTML remain intact. The 9.5 build assembles live 9.3 browser licenses and source 9.4 semantic records into the self-contained Wiki; the site publication step does **not** expose raw datasets.
