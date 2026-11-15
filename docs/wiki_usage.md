# Using the Qaroshi offline wiki

Open `Qaroshi_Wiki.html` directly in a current browser. Nothing needs an account or network connection.

The left sidebar browses topics and 70 grammar chapters. The top search looks through dictionary definitions, grammar and sentence examples. Press `/` to focus search. Press Escape to close the mobile sidebar. Browse the Dictionary page for detailed filters; it searches English meanings and Qaroshi spelling, including unaccented search approximations such as `gero` → `gëro`.

Open a word to see its definition, prominent English-style sound-out, broad IPA, native script, grammatical metadata, example sentences, related terms, and clickable components (when it is a compound). Extended letter-by-letter pronunciation can be opened from a details control.

The Native script page converts **Romanized Qaroshi into handwritten glyphs**, not English into Qaroshi; it can export PNG. The Latin A–Z guide describes English letter-name pronunciations separately from native Qaroshi phonemes. The moon/sun button switches appearance without connecting to a service.

The CSV, JSON, and Markdown files in the package are suitable for editing or further linguistic analysis. Build the standalone HTML with `python tools/build_wiki.py` after changing reference files.


## Learning in the wiki, not just looking up words

The **Learn Qaroshi** sidebar section contains a staged sixteen-lesson course, sixteen topic manuals, twenty-one worked sentence parses, and a practice workbook. The best order is to begin with Start here and the Pronunciation laboratory, complete lessons 1–8, read the Nouns/Cases and Verb workshop guides, complete lessons 9–16, and finish with the workbook. Every practice answer is tied to an existing sentence in the canonical phrasebook, so a learner can inspect its original context and pronunciation on the corresponding phrase page.

The **Grammar** section remains normative: opening a grammar chapter now also shows links to relevant deeper guides. The **Dictionary** remains the reference for exact lexemes, suffix-like spellings, and Romanized pronunciation, and the original glyph converter is the place to check native writing. The deep guides explain and teach the standard; they do not add a second competing grammar.

### How to self-test

Hide the English column in a course lesson and translate Qaroshi from its IPA and written text. Next hide Qaroshi and reconstruct the entire sentence from English. Check the first resonance, each case suffix, predicate suffix, negation, and final `he` or `ya` before opening the answer key. The workbook's diagnosis questions contain deliberately **incorrect** forms for editing practice, which should not be copied as normal Qaroshi sentences.

### Finding your place on mobile

Open the menu button at the upper right. The same learning and grammar links are present in the mobile sidebar, and the sidebar closes after navigation. Long lesson tables are scrollable within their reading section where necessary; the page itself should not become wider than the viewport. The `/#learn` view is the index for all training materials and is readable offline.
