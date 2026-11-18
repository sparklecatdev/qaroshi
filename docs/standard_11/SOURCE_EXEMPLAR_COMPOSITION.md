# Standard 11.2: evidence-gated verb composition

**Status: opt-in structural composition mode, NOT 97 additional approved general-purpose verb frames or independent speakers.** Original 25 reviewed 9.3 verb frames and original 10 noun categories remain the default. No canonical grammar, dictionary spellings, source sentences, or historical contributors are overwritten.

## Motivation

The Standard 9.3 parser is intentionally limited to 25 source-reviewed verb frames. Separately, the pre-existing [8.7 overlay](../../data/standard_8/valency_overlay_8_7.json) records **97 individual V1 subject–object exemplars**, each tied to one exact original bilingual sentence, canonical IDs, a semantic non-entailment, and explicit `human_observed=false`. Those exemplars were not previously usable in the typed parser.

`tools/grammar93/source_exemplars.py` builds a **separate opt-in grammar**, checks every exact dictionary ID and original teaching-corpus sentence, and licenses the documented `mi` actor + **only the one recorded patient** for each verb. The only productive operations beyond the historical exemplar are established elementary tense (`-te` past, `-yu` future), predicate negation, question endings, sentence resonance, reporting/unknown source, evidential operators and two-clause links. These operations generate **editorial morphology proposals**, not independently validated idiomatic uses.

## What it allows

- Source: `sen mi shiwaro-m khukhiri.` (I encrypt a message), backed by exact 8.7 ID and parallel corpus phrase ID.
- Bounded composition: `sen mi shiwaro-m khukhiri-te.` (structural past of the recorded event). This is an *editorial example*, not a new attested sentence.
- Questions: `hë mi shiwaro-m khukhiri-te he?`; negation: `sen mi shiwaro-m nu khukhiri-te.`.
- Two-clause event links using the existing 9.3 compositional syntax, without changing the source's lexical pairing.

## What it refuses

- `ti` or `sa` subjects for the 97 new verb frames. Existing examples only specify `mi`; do not silently infer generalized actor selection from an English gloss.
- Any patient not recorded for that particular verb, even if the object seems semantically plausible in English.
- An absent object, extra recipient/source/location, or an unsourced valency alternation.
- Modals, aspects, voice/passive/causative, noun derivation or unrestricted relative clauses for those 97 verbs. Their sense-specific admissibility must be reviewed separately.
- General natural-language translation, independently fluent meaning, or real speaker acceptance. `human_observed` remains false.

## Use

```sh
python -m tools.grammar93.source_exemplars
python -m tools.grammar93.cli --source-exemplars parse 'sen mi shiwaro-m khukhiri-te.'
python -m tools.grammar93.cli --source-exemplars render '{"proposition":{"type":"atom","actor":"mi","verb":"khukhiri","patient":"shiwaro","tense":"yu"}}'
python -m unittest tests.test_source_exemplars -v
node tests/sourceframes/ui.cjs
make build
```

The existing no-flag CLI remains strict and rejects the extra verbs. CLI structural results distinguish source-exemplar evidence from fully reviewed 9.3 frames.

## Wiki

The offline Wiki route `#source-frames` shows all 97 canonical verb/object pairings, their original source sentence, translation and semantic boundary, and a strictly restricted morphological experiment. Editable variants are prominently marked editorial and are **never called additional original source sentences**.

**Next:** individually review larger actor and patient classes, compare held-out semantic minimal pairs, test actual unfamiliar reader interpretation, and promote only independently adjudicated frame changes through explicit versioned standards decisions.
