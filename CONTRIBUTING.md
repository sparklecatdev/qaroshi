# Contributing to the Qaroshi Reference

Qaroshi's strength depends on consistent usage, not sheer glossary volume. New entries should be specific, nonredundant, pronounceable, and compatible with the 26 native glyphs.

## Proposal checklist

1. Search `data/lexicon.csv` (English and Qaroshi) for an established word or transparent compound.
2. Identify the intended English **sense**, not an ambiguous isolated word. For example, technical *charge* (electric) differs from *charge* (payment) or *charge* (accusation).
3. Supply part of speech, semantic field, precise definition, and at least two complete Qaroshi example sentences with their mandatory initial resonance marker.
4. Mark whether the word is atomic, compounded, an ordinary derivation, or a borrowed proper term. For a compound, identify each existing constituent.
5. Verify that the Romanization contains only the original 26 phonemes (`sh`, `zh`, `kh`, `ng` count as single letters).
6. Check case, tense, modality, negation, and evidential scope. Do not change an established 1.0 headword to fix a new collision.
7. Run `python -m unittest discover -s tests` and `python tools/qaroshi.py validate`.
8. For a proposed change to grammar, provide minimal pairs or counterexamples, not just an English description.

## Editorial priority

A community-attested phrase with clear context is stronger evidence than a machine-generated synonym list. Prioritize common conversational roots, idioms, demonstrative/reference clarity, valency frames, collocations, particles, technical precision, and naturally varying sentence structure.

## Changes and stability

The lexicon uses a **locked spelling ledger** (`data/lexicon_lock.json`). Do not delete or regenerate it. A correction that genuinely requires a spelling change should have a documented migration alias and a release note. An old phrasebook expression must remain understandable after an update. All accepted grammar examples must include a resonance marker and an English translation.

The `source/Qaroshi_Dictionary_853.csv` and `source/Qaroshi_Phrasebook_190.csv` files are canonical snapshots. Propose changes in new, clearly labeled data files, not by quietly modifying preserved originals. If a previously attested gloss is discovered to be contradictory, document the discrepancy, rationale and effective edition.

## Review labels

- `established`: unchanged Reference 1.0.
- `standardized`: explicit 2.0 grammar.
- `candidate`: concept and form present, pronunciation/usage review outstanding.

A reviewer can promote a candidate to standard status only after resolving collisions, semantics, syntax examples and compositional transparency. Promotion must be reflected in the lock ledger and release notes.

## Script and licensing

Native glyph artwork originates from the original 26-character sheet. Do not upload anyone else's lettering as a replacement without permission. This repository intentionally has **no declared license yet**; a project owner should select a license and verify permissions for contributed images before a public GitHub release.
