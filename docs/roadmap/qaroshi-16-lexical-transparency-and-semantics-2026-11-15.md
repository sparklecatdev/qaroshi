# Qaroshi 16.0 Semantic Atlas & Root Learnability Checkpoint

**Development archive, not a ratified language standard.** The full 493-file local ZIP is available as a conversation artifact, **not uploaded to this GitHub branch**.

## Motivation

A learner asked whether the grammar makes all the seemingly random dictionary words understandable without individual memorization. The answer, verified against the canonical `data/lexicon.csv`, is **no for all 30,000, but yes for the structure of many compounds**.

- 30,000 canonical entries: **13,379** entries typed `compound`, **16,525** typed `headword`, **96** typed `function word`.
- All 13,379 compound spellings exactly reconstruct from two documented modifier + head components; every component exists in the canonical lexicon.
- There are **1,832 distinct immediate components**; nested compounding reduces these to **1,820 unique ultimate root headwords**.
- Ranked by compound reuse, knowledge of the top 100 ultimate bases structurally unlocks 846 compounds, top 500 unlocks 5,476, top 1,000 unlocks 9,085, and all 1,820 unlock all 13,379.
- Knowing roots **does not guarantee exact technical/idiomatic meanings**. The 16,525 headwords lack the same explicit compound decomposition in the source. The audit invents no etymologies, renamings or semantic acceptance.

## 16.0 deliverables

A reproducible root-learning audit, root-ranked learning ladder CSV, 13,379-entry compound decomposition CSV, and a responsive **Root Explorer & word builder** were added to the offline 16.0 Semantic Atlas. The broader atlas documents all 30,000 canonical definitions and corpus-evidence levels, 118 word profiles (57 new), 40 literary metaphor proposals, 240 topical writing assignments, 5,000 draft senses, 1,000 draft idioms, and 223 contextual English translation variation groups. These are editorial aids, not independent speaker attestations.

## Quality gates

- **833 Python tests passed**, with one optional compiled-font test skipped in clean source-only extraction.
- **67 desktop/mobile Chromium checks passed**, with zero page errors.
- The **493-file ZIP** passed CRC and fresh extraction/retesting; SHA256 `decd449c7a0006ec51bddb1bedef5da95cfb5f998cd785c81ecdfe85f21ded4c` (32,803,210 bytes).
- **29 tracked canonical source files** remain SHA256 unchanged, including the original 30,000-word lexicon, 4,383 reference examples, 90 grammar chapters, 26 native glyph images, and 16 mandatory written resonance markers.
- No compiled font binaries are distributed.

## Outstanding linguistic requirements

Independent speaker/editor review of senses, literary idioms, authentic speech and dialect claims; a genuine naturalistic corpus rather than largely templated 15.1 text; and documented derivation or reviewed proposals for otherwise arbitrary-looking headwords. **Do not merge as an approved 16.0 language standard or claim the full ZIP is in this PR.**
