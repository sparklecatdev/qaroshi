# Using the current Qaroshi Wiki (9.5)

Open `Qaroshi_Wiki.html` locally, or use the public `index.html` page. The Wiki is a **self-contained, offline-first** reference; its core dictionary, current grammar, interactive workshop and semantic case explorer need no account or network.

## Where to start

The sidebar keeps five primary tasks visible: **Overview**, **Dictionary**, **Write & inspect sentences**, **Learn Qaroshi**, and **Meaning & examples**. The current grammar, topics, phrasebook and native script are immediately below. All individual chapters, deep topic guides, older research workbenches and teaching apps are available in collapsed sections, not removed.

Use the upper search to find dictionary words, examples or chapter text. Press `/` to focus the search. Use `#dictionary` for full lexical search, or `#categories` to browse a small set of subject groups. Expanding an area reveals the original topic labels. Typing a topic name searches across all areas. Historic links such as `#word/gëro`, `#grammar/02` and `#dictionary?domain=...` remain valid.

## Source-linked conversation uses and actual editorial review (10.1)

Each dictionary page can now show a separate **This word in conversation** section. These lines come from existing editorial scenes with their source labels and speaker turns intact. They are not new source-corpus attestations; original teaching sentences still appear separately.

The [editorial review desk](index.html#editorial) lets language editors review all 800 highest-priority lexemes, inspect prior definitions, meaning boundaries, original teaching examples and candidate cards, record what needs checking, and export local-only proposals. It never changes authoritative meanings or marks approval.

An independent [blind-reader study](index.html#validation) uses a separate offline learner-only HTML file generated with `tools/standard10/reader_html.py`. People provide anonymous first-pass paraphrases without seeing the English editorial key. A facilitator then uses `tools/standard10/adjudicate.py` to prepare a private, still-unrated worksheet for a separate human adjudicator. No results are fabricated, and no participant information is uploaded by the Wiki.

## Semantic definitions, conversations and controlled examples in Standard 10

The Dictionary's **Definition and sense notes** section now separates previously authored core descriptions and restrictions from inherited normative/editorial polysemy, the 800-word prioritized evidence inventory, and unreviewed candidate cards. A selected English translation word is NOT automatically another Qaroshi sense. The candidate cards remain collapsed and visibly unreviewed.

Open **Conversations** at #conversations to browse connected editorial dialogues. Each scene tells you the situation and shows speaker turns in Qaroshi, with optional English reveal. Words link directly to full dictionary guides. **Original editorial** scenes and **source phrase recombinations** are distinguished, and neither is presented as observed spontaneous conversation or independent native usage. A literal English parser gloss, where one was recorded, is shown separately from the contextual editorial English.

Open **Controlled drills** at #drills for preexisting 1,572 generated/roundtripped practice sentences. Reveal answers, switch input language, and search common expressions. These are NOT independently checked translations. Prefer the canonical phrasebook for original controlled examples.

Open **Independent comprehension** at #validation to learn how to run an actual blind human-reading study. The 80-item prompt generation, facilitator answer key and response/scoring tools live in the repository and are kept separate in CI artifacts. There have been **zero independent human validations** so far; the Wiki does not expose participant tracking or make fake research claims. See [the Standard 10 reference](../docs/standard_10/README.md) for study procedures.

## Full dictionary entries: meaning, structure and real context

Every word page now opens with the **recorded meaning first**, followed immediately by pronunciation, semantic class, and a **How to use this word** explanation tied to its part of speech and the actual grammar. For common word classes the page gives safe grammatical templates and shows regular word forms (cases, tense, and similar). These are clearly labeled **illustrations, not independently attested complete sentences**.

The **This word in context** section shows source teaching examples when the whole headword or its licensed suffix form occurs. The word is highlighted, the suffixes are explained, and you can open the original parallel sentence. For words without a recorded example, the page says so and directs readers to the relevant documented sentence patterns. Editorial challenge proposals remain in an expandable, distinctly marked section.

Compounds now show their **real component headwords and their individual definitions**, not just a formula. The whole compound keeps its own source gloss rather than assuming the English result is a literal sum. Word articles link to source-specific particle rules, resonance meanings, 25 reviewed valency frames, lessons, flashcards, and the original 26-glyph native alphabet where relevant.

## Ranked dictionary search and source-linked word families

The **Dictionary** now ranks complete Qaroshi spellings and English definitions before partial matches. Multiple words are treated as a combined query, not an indiscriminate list of anything containing one common word. Topic and part-of-speech filters are available under a collapsed disclosure. Searches ignore accents while always displaying exact canonical spelling.

Each word page explains recorded component words, links to compounds that explicitly cite it as a component, and distinguishes **matching English glosses** from **topically neighboring entries**. These relationships do not prove interchangeability or supply an antonym database; unsupported synonym/antonym assertions are intentionally omitted. A word also links straight to practice or the source-reviewed sentence workshop when applicable.

## Study words and sentences without leaving the Wiki

Open `#practice` or use **Practice words & phrases** from the sidebar. Review source dictionary cards, or switch to source teaching-sentence cards. Choose the recall direction, reveal the editorial answer, and mark whether you recalled it. The exercise shows IPA and approximate sound-out values when available. Progress lasts only for the current page session; it is not stored or transmitted.

Open any dictionary entry and choose **Study this word with flashcards** to put that headword first in a focused session. This is voluntary self-practice, **not** human-certified translation accuracy or a blind comprehension study. For detailed pronunciation and native glyph conversion, continue to the built-in `#latin`, `#script`, `#guide/pronunciation` pages.

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
