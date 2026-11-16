# Qaroshi full-project hygiene and UX audit · 2026-11-15

## Scope

Reviewed the latest GitHub `main` tree after the v21–23 merge, plus the complete local v21–23 source archive and its prior release assets. Checked canonical data integrity, version labels, reproducibility, browser entry points, app provenance, historical logs and public deployment packaging. This is a source/system audit, **not** a claim that 30,000 lexemes have been independently validated by speakers.

## Corrected this pass

- Current homepage and README no longer present version 17 as the latest tool edition. **Reference Standard 7.0** and **teaching tools through 23** are explicitly distinguished.
- Added a clean, searchable `explore.html` hub. Current apps are easy to find, while research/historical tools live in a collapsed section; existing deep links remain valid.
- Links from the Wiki can now reach the latest translation academy, speech studio, conversation studio and overall catalog.
- GitHub Pages stages only verified HTML applications. It no longer uploads raw CSV/JSON corpora, source code, historical QA reports or local logs into the publicly browsable site artifact. Historical files remain in Git unchanged.
- The 21–23 artifact restorer verifies SHA-256 of both compressed packages and resulting HTML, rejects duplicate/unsafe paths, and refuses silent overwrite of edited local data unless `--force` is explicitly requested.
- Added reproducible source integrity, documentation/catalog and offline browser checks to CI.
- Updated primary documentation to the latest verified tool series and clarified that old release manifests are historical snapshots.

## Verified in the local source checkout

| Gate | Result |
| --- | --- |
| Canonical words | 30,000 unique headword spellings |
| Controlled bilingual reference | 4,383 unique source IDs |
| Grammar sections | 90 sequential chapters |
| Required written resonance markers | 16 |
| Source glyph artworks | 26 |
| Historical SHA-256 source baseline | 29 of 29 unchanged |
| GitHub Pages app targets | 10 documented targets verified in staging |
| Curated Pages output | 19 HTML pages; no CSV/JSON/source/log files |
| Python unit suite | 1,101 passing, one optional-font skip |
| Desktop and mobile portal checks | 56 passed, no JavaScript page errors |
| Precomputed app checksums | 18/19, 20 and 21–23 matched |

## What was *not* deleted or falsely resolved

Prior versions, procedural corpus outputs, review decisions and versioned browser reports are retained as research evidence. The 103 historical translation review cases and 65 editorial root-review decisions remain visible and unratified; these are not mere stale logs. No canonical spelling, gloss, phonology, grammar rule, example or original glyph changed.

The substantive remaining quality frontier is independent human review: speaker pronunciation and idiom naturalness, blind compound comprehension, and translation/proficiency validation. Software QA cannot certify these by itself.
