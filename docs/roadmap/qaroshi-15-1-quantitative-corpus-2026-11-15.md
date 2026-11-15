# Qaroshi 15.1: quantitative corpus scale-up, with naturalness limits

Date: 2026-11-15. **Development release only, not a ratified naturalistic corpus.**

## Reproducible local artifact
The completed local source-only ZIP is named `Qaroshi_15_1_Corpus_Scaleup.zip`, SHA-256 `1a6934562a52297f6980675e25206d814660751e6d357e6cc6451901ef474c90` (28,810,549 bytes; 461 files). It was validated by ZIP CRC, fresh extraction and regeneration. **The ZIP itself and its 461 files have not been uploaded to this GitHub PR**.

## Numerically achieved
- Exactly **1,000 different conversation transcripts**: 176 previously separately drafted editorial conversations and 824 newly procedurally composed scenario instances.
- **205 prose/reading pieces**: 35 separately drafted editorial pieces and 170 procedurally composed narrator sequences.
- **211,366 Qaroshi-only whitespace source tokens**: 6,828 from separately drafted editorial material and 204,538 from procedural composition. English, IPA, labels and the old 123,000-token repetitive teaching-drill inventory are excluded.
- **47,655** aligned utterances; **10,415** exact distinct Qaroshi sentence forms; **43,327 repeated sentence occurrences (90.92%)**.
- **1,988** conditional or coordination clauses are flagged with Standard-14 `R14-010` for semantic scope review; **231** exact-source/contextual-English variation groups require attention.
- **Zero** speaker attestations or independent human-approved translations.

## Tooling
A new offline Corpus Atlas separates original editorial and synthesized content by default, with searchable Qaroshi/English, word-level 30,000-headword reference, concordance, translation reveal, local notes and export. The archive includes deterministic generators, complete parallel CSV, JSONL source texts, context QA worksheets and written human review gates.

## Tests and preservation
- **791 Python tests run successfully** (one optional compiled-font test skipped after clean extraction).
- **20 desktop/mobile Chromium checks passed**, zero page errors.
- **29 canonical reference files** were SHA-256 verified unchanged, including the 30,000-entry lexicon, 4,383 reference examples, grammar, original 26 glyph images and 16 obligatory resonance markers.
- Font binaries excluded from shared archive.

## Remaining qualitative standard
**This does not achieve 1,000 independently written natural conversations or a naturally diverse 100,000-word corpus.** The 824 scripts and 170 prose pieces were algorithmically composed from limited discourse frames, with pronounced repetition. They are viable controlled learning/review fixtures, but not a speaker-backed standard. The PR should remain draft until full source upload, independent literary rewriting and semantic/community review.

Tracked work: PR #2, Issue #1.