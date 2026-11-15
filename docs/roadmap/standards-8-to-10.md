# Qaroshi Standards 8–10: development roadmap

This document records the ordered worklist for the next Qaroshi standards. It is a **development plan**, not an assertion that the complete language project or every task has been finished.

## Preserved baseline

The local Standard 7.0 source has 30,000 lexical entries, 4,383 bilingual examples, 90 grammar chapters, 26 original handwritten glyphs, and 16 mandatory sentence-initial written resonance markers. These should remain backwards-compatible unless an explicitly documented standards change is approved.

## 8.0 Natural fluency

- [x] Document extended clause syntax and morphological suffix-order rules.
- [ ] Resolve lexical/grammatical ambiguity through independent language review.
- [ ] Document attested conversational contractions and fillers.
- [ ] Independently define and review 1,000 idioms, including literal meaning, figurative meaning, context and limits.
- [ ] Curate at least 5,000 detailed sense records, with distinctions among synonyms and antonyms.
- [ ] Write or collect 1,000 independent coherent conversations. Controlled rephrasings of a small base set do not count as independent conversations.
- [ ] Build a 100,000-word corpus of coherent connected Qaroshi text, counting source text tokens only and recording provenance.
- [x] Build a structural test bank with more than 2,000 positive and negative cases. Local development has 4,200 test fixtures.

## 9.0 Writing and pronunciation

- [ ] Complete community review of native script spelling and punctuation.
- [x] Produce an experimental installable font from all 26 existing glyphs.
- [ ] Package tested native desktop and mobile keyboard layouts. The development kit currently includes a browser keyboard and Linux XKB source map.
- [x] Document segmental phonology, stress and possible connected-speech reductions.
- [ ] Obtain 3,000 consented and licensed speaker recordings; browser TTS is **not** an authentic speaker recording.
- [ ] Describe regional accents and dialects only after collecting actual usage examples.
- [x] Add optional synthetic approximation playback to word pages; IPA remains the primary pronunciation reference.

The experimental font uses temporary Unicode Private Use Area code points U+E000–U+E019. These are *not* official Unicode assignments and require a mapping/font for exchange.

## 10.0 Language ecosystem

- [ ] Extend the Academy to a fully interactive advanced-learning curriculum; a 24-lesson textbook and an offline Study Studio companion exist locally.
- [x] Add more focused minigames alongside the earlier Academy practice modes.
- [ ] Validate a general English ↔ Qaroshi sentence translator; dictionary-assisted lookup and interlinear glossing are available, but **not** full machine translation.
- [ ] Build full syntactic and semantic grammar checking. The present checker verifies known written resonance and suffix rules only.
- [x] Compile a 24-lesson textbook with the earlier 90-chapter reference as an appendix.
- [ ] Expand the edited literary and explanatory corpus substantially.
- [ ] Ground cultural and historical accounts in documented sources and community contributions.
- [ ] Deploy and maintain contribution templates and an editorial review process.
- [ ] Publish the entire validated current source archive and maintain release notes on GitHub.

## Contributor standards

For new lexemes, include IPA, full sense, part of speech, usage limitations, and an example with mandatory resonance. For grammar changes, include minimal pairs and backwards-compatibility tests. For corpus and audio contributions, record consent and license. Never promote synthetic prose or computer voices as independently attested speech.

Related task-tracking issue: #1.
