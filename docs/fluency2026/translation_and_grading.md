# Translation and grammar-checking validation

## Policy

The glossary tool must never pretend that a dictionary match is an accurate full sentence translation. Qaroshi uses SOV structure, obligatory written resonance, noun case marking, tense/aspect/mood affixes, and evidence particles. English does not preserve these distinctions automatically.

## Implemented check levels

1. **Lexical recognition:** exact source lemma, part of speech, source definition, IPA and optional spelling suggestions.
2. **Structural word morphology:** licensed suffix ordering and conflicting case/tense/aspect/modal slots.
3. **Sentence boundary:** mandatory resonance, ordinary question marker `he`, punctuation warnings.
4. **Interlinear gloss:** transparent word-by-word treatment of explicitly present case and verb suffixes.
5. **Bounded translation:** a small known subject–object–verb subset with an explicit caution; unknown inputs receive glosses and warnings rather than fabricated sentences.

## Not yet verified

Complete semantic scope, all complex quotation patterns, idiomaticity, dialectal variants, naturalness, and arbitrary English ↔ Qaroshi translation. Passing structural checks is **not** evidence that the intended meaning is the only meaning.

## Reviewer protocol

For each independently curated test item record: original text, intended English reading, alternate plausible readings, lexical constraints, grammar rule, expected validator result, one minimally changed ill-formed counterpart and two separate reviewer decisions. For semantic scope, test both affirmative/negative polarity and witnessed/reported/inferred cases. Do not allow an automatic parser to serve as its own independent oracle.
