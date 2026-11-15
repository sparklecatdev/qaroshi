# Qaroshi 15.0: Natural Conversation & Literature

## Summary

This release expands the independently *scripted* editorial conversation library and publishes a searchable English–Qaroshi reading collection. It adds a reproducible corpus pipeline, cross-release index, IPA and sound-outs, source-language-only token counts, duplicate-sentence/translation-variation QA, and browser review tools.

## Verified additions

| Measure | 15.0 new | Cumulative editorial library |
|---|---:|---:|
| Conversations | 73 | 176 |
| Prose/reading pieces | 12 | 35 |
| Aligned sentences/turns | 561 | 1,594 |
| Qaroshi whitespace tokens | 2,419 | 6,828 |
| Distinct Qaroshi sentence surfaces | 312 | 771 |
| Speaker-attested contributions | 0 | 0 |

The 15.0 dataset has **441 dialogue turns** and **120 prose sentences**. All passed the v14 automated surface/translation-risk screen without flags. However, **347 of the 561 new occurrences** are instances of forms appearing more than once, and **48 new-source surface forms** have different contextual English renderings. Across the cumulative editorial library there are **223** translation-variation groups. These are priorities for editorial review, not proof of errors.

## Provenance and genre

Every new piece has its own title, premise, genre and ordered sequence. The earlier 11 and 12–13 development texts are included in the browser as separate prior releases, but the repetitive 1,000-variant practice corpus is NOT counted as independent work. The original 26 native signs, 16 mandatory written resonance markers and core dictionary have not been altered.

The new dialogue subjects cover archives, trust, travel safety, gifts, weather, literature, painting, song, market life, friendship, consent, language learning, navigation, ecology and more. Prose includes travel log, short fiction, language-learning and ethics essays, archival reflection and epistolary writing.

## Offline library capabilities

- Filters by conversation versus literature, release and genre
- Searches titles, premises, Qaroshi and English text
- Sentence-by-sentence reading with IPA and optional English reveal
- Clicking words opens a 30,000-entry dictionary; one click from a word entry opens concordance search
- Private per-piece editorial notes, exportable as JSON
- Light/dark mode, responsive layout, screen-reader labels and no network requests

## Validation

The source corpus contains 561 new line records, 561 surface-valid lines, and 0 v14 machine flags following correction of double-object recipient forms. New tests check provenance, counts, IPA, sentence syntax, baseline dictionary preservation, and exclusion of templated dialogues from independent counts. The browser interaction smoke test covers desktop and mobile flows. The ZIP excludes raw font binaries.

## Unfinished roadmap goals

**824 additional non-template conversations** would be necessary to reach the *numerical* 1,000 target, before independent linguistic acceptance. The current **6,828 editorial tokens** are **93,172 below a 100,000-token numerical threshold**. Those counts are only a planning aid: the original requirement was a genuinely naturalistic writing corpus, and a word count alone does not establish that. Editor and speaker review, literary breadth and multi-paragraph syntactic variety remain unfinished.

The next milestone is a speaker/community editorial review protocol with real contributions and careful paragraph-level linguistic revision. Neither new language forms nor distribution license terms are silently invented.
