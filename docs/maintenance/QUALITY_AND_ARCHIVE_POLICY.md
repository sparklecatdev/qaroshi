# Qaroshi quality, presentation and archive policy

## Distinguish three different numbers

The *canonical language* is Unified Standard Reference 7.0 (30,000 entries, 4,383 teaching references, 90 grammar chapters, 16 written resonance markers, 26 glyphs). The *teaching-tool release series* has grown through 23.0. Historical version-numbered documents, including the `RELEASE_INFO.json` 7.0 snapshot and `data/learning_library.json` 5.1 snapshot, are intentionally preserved. They are not the live website's current edition indicator.

## Current user-facing surfaces

- `index.html` is rebuilt from `Qaroshi_Wiki.html` on deploy, not copied from an outdated tracked snapshot.
- `explore.html` is the current catalog. It highlights tools 17–23 and the Wiki; historical experiments are separately collapsed.
- The compressed current apps are restored with SHA-256 checks before deploying HTML.
- Historical research tools keep working under their existing `.html` paths, including bookmarked URLs.

## Do not call old evidence a log to delete

Historical corpus files, review ledgers and earlier browser QA JSON reports may be unglamorous, but they encode reproducibility and editorial provenance. Keep them in Git. Where a file has `provisional`, `generated`, `editorial`, `review` or an old version number in its path, that does **not** authorize deletion or silent promotion to the current standard. The v15 generated corpus still contains heavy repetition, and v16–v19 paraphrases remain unapproved unless separately ratified.

Runtime logs, binary font compilations, local caches and test artifacts do **not** belong in GitHub Pages. They are excluded by the explicit `_site` staging script and normal `.gitignore` rules. The publishing workflow never uploads the whole repository root. No source content needs to be deleted to obtain a clean public website.

## Source and semantic gates

A pass is a verified preservation check, not proof that all 30,000 words are idiomatic. Maintain at minimum:

1. The 29 canonical SHA-256 source baselines; uniqueness and required fields for 30,000 words and 4,383 phrases.
2. Source-aligned release datasets and frozen correction/review status until independently approved.
3. Explicit warning that the 103 v14 translation disputes and 65 manually reviewed root alternatives are not resolved through app rendering.
4. Correct current site navigation, no broken application links, no raw JSON/CSV or log files in the Pages artifact.
5. Browser checks on desktop and mobile, with accessible focus, navigation and no application script errors.
6. A human adjudication process before making claims about naturalness, dialect, native pronunciation or measured proficiency.

## Safety of restoring archived artifacts

The v21–23 restorer validates compressed archive checksums, output HTML checksums, archive file paths and conflicts. It must **refuse to overwrite locally edited data** unless an explicit `--force` flag is supplied by a reviewer. The same principle applies when recovering older release files.

## Outstanding issues (not silently fixed)

- Independent language users have not yet supplied enough attested freeform conversations to establish idiomaticity across all domains.
- Broad IPA and sound-out approximations have not been grounded in a consented speaker recording corpus.
- Gloss-based compound overlap can hide false friends; trials and rejections must remain labeled as such.
- Translation and quizzes emphasize documented context; they are not validated open-domain translation or proficiency measurements.
- The original Wiki's optional assistant can contact an external API when configured; its privacy boundary must be explained clearly.

These open research questions are **not software regressions** and should not be disguised as completed features or fixed by deleting historical evidence.
