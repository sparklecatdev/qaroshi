# Qaroshi 13.0: Semantic review and acceptance protocol

**Current status:** Editorial development, not a speaker-ratified expansion of the canonical dictionary.

Qaroshi 13.0 preserves the same 30,000 dictionary entries. This release does not mint extra independently accepted headwords, nor does it automatically canonize the 1,000 earlier figurative candidates or the 5,000 mechanically drafted sense cards. It makes their limits inspectable and adds stronger, individually written examples.

## What the audit actually establishes

The 1,000 candidate idiom constructions have been checked against the 26-letter transliteration and canonical headwords, plus allowed word endings. **454 candidates** are flagged for semantic/collocational caution. A candidate with no warning still **requires a separate language judgement**. A productive pattern like “protect X with a wing” does not automatically become 40 separate conventionalized idioms when X is replaced with 40 abstract nouns.

The 5,000 candidate sense cards have been checked against the original dictionary IDs, parts of speech and source glosses. **4,791 cards** need more work, generally because the teaching examples are mechanically chosen (for example, “I see [abstract noun]”), or because verb valency is unclear. This is **not** evidence that the 4,791 original definitions are wrong.

The new **61 core profiles** were individually written around important meaning distinctions. Examples include:

- `mara` means a friend or trusted peer; `runa` means chosen family/community; `naro` means home or nesting place. These are related concepts, **not interchangeable synonyms**.
- `nashi` can mean deep affection or cherishing. It is not necessarily romantic, sexual or reciprocal, while `rawëli` more generally expresses wanting or desiring.
- `ronaro` refers to hearing; `shiroawe` to listening attentively. Detection does not entail attention or understanding.
- `sëma` concerns truth, `sëmi` knowledge, `shërawë` belief, and `shëna` trust. Treating them as equivalent creates real mistranslations.
- `goro-ki` expresses ability, `goro-ho` permission, `goro-du` obligation, and `goro-yu` future. Neither ability nor desire grants permission.
- The evidentials `si` (witnessed), `hu` (reported), and `ye` (inferred) describe source of knowledge, not a proof of truth.

The **40 new detailed metaphors** are independently drafted editorial interpretations. Each has a literal rendering, a proposed figurative meaning, a plausible use situation, and an example of where that interpretation should *not* be assumed. They remain **proposals**, not attested traditional Nardoragon sayings.

## Reviewer workflow

1. Choose a candidate from `data/v12_13/idiom_1000_quality_triage.csv` or `data/v12_13/sense_5000_quality_triage.csv`.
2. Check the original headword or components against `data/lexicon.csv`. Do not trust the English gloss alone when multiple meanings exist.
3. Explain the syntactic roles: subject, object `-m`, recipient `-tu`, location `-lo`, goal `-gu`, source `-de`, companion `-wa`, verb tense/aspect/modality and resonance.
4. Give both a **supporting context** and a **counterexample** in which the suggested translation would be wrong.
5. If two roots appear synonymous, give a minimal sentence pair and describe the semantic restriction that makes the pair non-interchangeable.
6. Label the output as *editorial accepted for a draft*, *revision required*, or *rejected as a conventional expression*. Do not label it “speaker attested” without a dated, licensed speaker example.
7. Record provenance, review date and reviewer consent if public credit is intended. Keep identifying personal information out of the public corpus.

## What cannot be counted as completed

Automatically generating 5,000 dictionary labels, or copying an English word into a formulaic example, does not establish 5,000 individually reviewed senses. A morphological parser does not establish metaphor naturalness. A negative sentence like `sen mi nu shiri.` (I do not speak) has different consequences from `sen mi shiri-ki.` (I can speak), and replacing one with the other for a fluent-looking translation is an error.

The editorial review queue in `Qaroshi_12_13_Language_Studio.html` stores decisions in the local browser and can export them. These are drafts requiring provenance and independent review before standardization.
