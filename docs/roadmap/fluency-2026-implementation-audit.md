# Qaroshi Standards 8–10: Full-checklist implementation audit

**Scope:** all 24 checklist items have been investigated and acted on where implementable, but **not all are fully achieved**. The purpose of this record is to make the gap between software delivery, proposed language usage, and genuine speaker/community evidence explicit.

The canonical lexicon remains 30,000 entries and the initial 90 grammar chapters are preserved. No new automatically generated figurative phrases have been promoted to canonical dictionary entries.

## Completed software/artifact milestones

- 4,200 earlier structural grammar fixtures are retained and the new suite adds explicit regression checks.
- 1,000 **editorial figurative candidates**, built from 25 image families × 40 existing abstract anchors, each with an interpretation, literal rendering, context, example, phonetics and a clearly visible review flag.
- 5,000 **draft semantic cards** derived from unchanged dictionary headwords, with gloss, part of speech, grammatical frame hints, pronunciation and illustrative examples.
- 1,000 **controlled practice dialogues**, 26 turns each, 26,000 annotated utterances, **123,000 Qaroshi source tokens** by whitespace/token counting. This is synthetic pedagogical text, not naturalistic independent speaker dialogue.
- New browsable `Qaroshi_Fluency_Lab.html`: figurative search, sense cards, 1,000-dialogue explorer, hidden/revealed translations, meaning quiz, score locally saved and mobile navigation.
- 3,000-item recording **request manifest** and an audio/dialect ethics and review protocol. **Zero human recordings collected**.
- Source to compile the user's original 26 glyph PNGs into a temporary-PUA TrueType font, plus experimental cross-platform Keyman source and browser keyboard. The installed-platform source is **not** certified on every operating system.
- Conservative `qaroshi_cli.py` for structural checks, glossary lookup, spelling suggestions and translations of a narrow, explicitly defined sentence subset. It does not pretend to be fluent arbitrary translation.
- The pre-existing 24-lesson textbook, Academy, Wiki, literature reader, native script tools and contributor templates are kept in this development kit.

## Ordered checklist

| Task | Status | Evidence / outstanding work |
|---|---|---|
| 8.01 Advanced sentence grammar | Implemented, limited scope | `docs/8_fluency/formal_grammar.md`, 90 baseline chapters; independent semantic review remains valuable |
| 8.02 Resolve all ambiguities | Partial | Structural checks, no proof of complete semantics or naturalness |
| 8.03 Slang, fillers, contractions | Partial | Conversation guide; independently documented real usage needed |
| 8.04 1,000 idioms | **Draft inventory only** | 1,000 image-based candidates from 25 families, **not** 1,000 accepted independent idioms |
| 8.05 Detailed 5,000 word senses | **Draft inventory only** | 5,000 structured cards, not human-verified polysemy or contrast |
| 8.06 1,000 natural conversations | **Controlled practice only** | 1,000 lexical variations of a 26-turn guided exchange, not independent spontaneous conversations |
| 8.07 100,000 connected-text words | **Controlled token count met** | 123,000 Qaroshi tokens in controlled scripts; independently authored natural writing still outstanding |
| 8.08 2,000+ grammar tests | Implemented structurally | 4,200 fixture bank retained, release-specific regression suite added |
| 9.01 Native spelling and punctuation | Partial | Orthography proposal; community standardization pending |
| 9.02 Installable font | Buildable locally | 26 user-glyph vector font builder tested; source supplied, font binary not redistributed |
| 9.03 Native keyboards | Partial | Browser keyboard, Linux XKB map and experimental Keyman source; native platform installation testing pending |
| 9.04 Phonological processes | Documented proposal | Phonology guide and IPA mapping; field/lab speech evidence pending |
| 9.05 3,000 human audio recordings | **Unmet** | Zero recordings; 3,000-item collection plan and consent protocol |
| 9.06 Document real dialects | **Unmet** | Collection and validation procedure, no empirical speaker data |
| 9.07 Pronunciation playback | Implemented approximation | Browser-synthesized reading, explicitly not a recording of a Qaroshi speaker |
| 10.01 Advanced Academy | Partial | Academy, 24-lesson textbook, new Fluency Lab; advanced mastery validation and full interactive pathway pending |
| 10.02 New minigames | Implemented | Existing Academy and new contextual meaning challenge |
| 10.03 General bidirectional translation | **Unmet as general MT** | Narrow sentence templates and bilingual glossary tooling, otherwise gives interlinear meaning only |
| 10.04 Comprehensive grammar checker | Partial | Structural and suffix validation; arbitrary semantics and pragmatics not certified |
| 10.05 Complete textbook | Implemented reference draft | 24-lesson textbook and grammar appendix, more teacher review desirable |
| 10.06 Large literary corpus | Partial | Existing literature reader and controlled dialogue corpus; independently authored literary depth pending |
| 10.07 Culture and language history | Partial | Explicitly editorial cultural usage guide; history cannot be inferred from nothing |
| 10.08 Community contribution workflows | Implemented offline; online partial | Templates/protocols and GitHub issue, editorial community needed |
| 10.09 Publish everything to GitHub | Partial | GitHub development PR and roadmap docs; complete binary/local archive not yet uploaded as a GitHub release |

### Why these distinctions matter

A language's **expressive capacity** is not established by lexical counts, generated examples, or a grammar checker alone. Conventionalized idioms, authentic dialects, and human-pronounced audio require speakers who consent and can review the material. Even high-quality editorial Qaroshi prose should not be mislabeled as an ethnographic record.

### Recommended process for finalization

1. Review 25 figurative construction families for grammar and cultural plausibility, then vet and accept or reject each expression individually.
2. Review each semantic card for argument restrictions, multiple meanings, contrastive minimal pairs and example naturalness.
3. Commission independent dialogues and a non-templated 100,000-word corpus from contributors.
4. Collect consented speech recordings with two human reviewers and stable licenses.
5. Test Keyman installers on Windows, macOS, Linux, Android, and iOS; publish accessible installation instructions and reproducible checksums.
6. Run blind translation tests with separate English and Qaroshi reviewers, then refine the checker and teaching materials.
7. Merge approved components through GitHub review while preserving backwards compatibility.