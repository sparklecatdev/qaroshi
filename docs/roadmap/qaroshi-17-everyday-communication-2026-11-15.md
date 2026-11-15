# Qaroshi 17.0: Everyday Communication checkpoint

**Date:** 2026-11-15. **Status:** Verified, source-only local development package, **not** a ratified speaker-verified language standard. The complete 562-file ZIP has NOT been pushed to this GitHub branch.

## Actual practical deliverables

- A standalone responsive offline **Everyday Communicator**, with phrase search, context/intent filters, favorites, copied text, script preview, sentence-builder drills, phrase recall and local progress export.
- **656 exact source-linked bilingual examples** with existing citation IPA/sound-outs: all 190 original phrasebook lines, all 106 so-called "living speech" teaching lines, and 360 reference 5.0 topical examples. These are documented editorial teaching examples, **not speaker-attested natural utterances**.
- **32 earlier editor-scripted scenes (192 turns)** preserved with contextual and literal reference English; 10 study units with 50 recall prompts, and 120 source-reuse-ranked core lexemes.
- A bounded **12-verb sentence builder** using controlled subject/object frames, 390 structurally checked fixtures, negative/question/tense/modal choices and verb valency constraints. It does **not** offer unrestricted human-verified translation.
- A 30,000-entry dictionary, original 26 glyph images with single-letter digraph mapping, 16 written resonance cards, phonetics and a convenient on-screen ë input key.

## Quality and unresolved rules

- All source Q-IDs and source fields match the unchanged 4,383-line reference file. **92 displayed phrase records** carry v14 review warnings. In particular, 3 original what-question phrases use `khe-m`, which the older v14 parser rejects as a case-marked question word, while 5 colloquial short-form questions without `he` are flagged by its polar-question heuristic. **These remain unchanged, conspicuously flagged rather than silently rewritten.**
- Existing editorial dialogue translations sometimes paraphrase or add narrative context. A surfaced literal translation does not guarantee semantic correctness. No real speaker survey/recordings, dialect attestations or accepted replacement roots have been created.

## Verified package and compatibility

- ZIP: `Qaroshi_17_Practical_Communication_Kit.zip` (39,431,742 bytes, 562 files), SHA-256 `87ea8269beec48dd1f5a8f86a17325430626749db73c695c0c288a432ce01199`. ZIP CRC and fresh extraction passed.
- **1,029 Python tests ran successfully, with one expected optional-compiled-font skip** from the extracted archive.
- **52 desktop/mobile Chromium browser checks passed**, no JavaScript page errors.
- A fresh extraction regenerated exactly the same standalone HTML bytes.
- **29 original canonical file SHA-256 digests matched**: original lexicon, grammar, 4,383 examples and 26 glyphs, with all 16 written resonance markers unchanged.
- Compiled font binaries are intentionally absent. The offline app uses existing glyph imagery instead.

**Do not merge as a community standard or claim full source sync.** The full 562-file package remains in the conversation artifacts. PR #2 should remain draft pending complete source publication and independent linguistic review.
