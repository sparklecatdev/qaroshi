# Qaroshi 16.1 Root Reform: editorial checkpoint

**Status:** Reproducible development release, NOT a ratified change to canonical vocabulary. The 519-file ZIP remains available through the conversation and has not been uploaded in full to this GitHub branch.

## Actual results

- 30,000 canonical dictionary entries unchanged. 16,525 headwords audited for possible learnability and compositional paraphrases.
- 2 existing headwords have exact spelling decompositions despite being labeled headword.
- 2,662 headwords permit strict two-component proposals using primary English senses; 146 others rely on secondary senses.
- 7,749 headwords have partial semantic keyword anchors, but no licensed derivation; 5,966 have no documented decomposition.
- 3,817 OPTIONAL transparent-form proposals over 2,808 canonical target headwords. ZERO approved new forms or breaking renames.
- 2,925 potentially missing exact English semantic components; 176 recur across at least 3 headwords. Not proof that no synonym exists.
- 4 proposed spelling collisions across 9 target meanings require disambiguation.
- 1,200-headword learner ladder from reference example evidence and known compound reuse.

## Application, tests and integrity

- Self-contained Root Reform Studio with full dictionary, all audited headwords, root learning path, candidate breakdown, missing components, grammar and local editorial review with JSON export.
- 883 Python tests passed on fresh source extraction, with one expected skip for optional compiled font.
- 42 desktop/mobile Chromium interaction checks passed with zero page errors; testing used in-memory HTML and a localStorage shim because managed Chromium blocks URL navigation.
- 29 canonical baseline source SHA-256 hashes remain unchanged; grammar, 26 original glyphs and all 16 mandatory resonance markers retained.
- The local ZIP contains 519 files and passed CRC verification, 35,828,075 bytes, SHA-256 f3cdde23b0391c695b8c636378bf32cf6fcba135c910b8783e5e4ccfff2aba4c.

## Limitations

The exact English gloss split establishes a candidate structure only, not a conventional synonym, new etymology or independently confirmed speaker usage. Many long forms are not suitable as everyday replacements. Do not turn this draft into an approved standard automatically, and do not claim the complete source ZIP has been pushed to GitHub.