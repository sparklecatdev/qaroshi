# Qaroshi 8.4 · Functional language readiness and stabilization

**Status:** implemented editorial grammar refinement and reproducible audit. **Not** a declaration of general fluency, an unlimited translator, native usage, or the completion of the entire language. The authoritative 8.0 grammar and adopted 8.1 embedded-question rule remain unchanged except for the **11 narrow active-sense frames adopted in the 8.4 overlay**. The 8.3 proposal grammar is still editorial. No historical word or glyph is replaced.

## Changes made in this edition

1. Explicit new active-sense valency for 11 existing common verbs, with required roles, authorized case slots, incompatible inferences and model examples. See [8.4 core verbs](AMENDMENT_8_4_CORE_VERBS.md) and the machine-readable overlay in `data/standard_8/valency_overlay_8_4.json`.
2. A deterministic review queue containing **all 500 original unseen challenges**, including every source-backed 8.3 candidate and every missing translation. Each row records the actual blocker, verb witnesses and *blank fields for a real review decision*. It cannot silently promote a draft to verified.
3. A 400-verb ledger preserving all 25 earlier full reviewed frames, adding 11 editioned active-sense frames and identifying the other **364** priority verbs as not granted new general argument permissions.
4. A 120-item core semantic worklist anchored to actual dictionary IDs, deliberately leaving native-language definitions *unapproved and blank* until individually written and checked.
5. A 12-pair blind contrast worksheet (separate answer key) for clause-local negation, tense, ability versus permission, quantifier scope, embedded questions, care versus romance, argument roles, inclusive/exclusive pronouns, evidentiality and new limited core senses.
6. A strict **restricted** sentence-shape checker for the 11 new frames. It checks a single pronoun-subject active clause with overt case; it cannot decide whether the selected object is semantically compatible.

## Reproducible evidence

Run:

```sh
make stress84
python -m unittest tests.test_stress84 -v
python -m unittest discover -s tests -q
```

Generated outputs are in `data/stress84/` and are not stored as misleading hand-verified reference corpora.

| Evidence | Result in this edition | Interpretation |
| --- | ---: | --- |
| Unfamiliar English challenges considered | 500 | Full review ledger coverage |
| 8.3 provisional translation drafts | 96 | 49 inherited + 47 new; **none independently checked** |
| Challenges still without a complete draft | 404 | Open work, not proven unexpressible |
| Previously general reviewed priority verb frames | 25 | Old normative baseline |
| New **narrow active** verb frames | 11 | Explicit 8.4 grammar choices |
| Priority verbs without a newly approved general frame | 364 | Source-only restrictions remain |
| Indexed core words needing native explanation review | 120 | No new definition pretended complete |
| New blind minimal-pair contrasts | 12 | Materials only; no responses |
| Independent human participants | 0 | No measured comprehension |

## How to close, rather than hide, the gaps

### Expressive stress review

For each of the 404 missing cases, write an **original full Qaroshi proposition**, record real dictionary IDs and clause structure, and compare the English meanings that differ only in key truth conditions. If a direct construction is not viable, demonstrate an exact **two-or-more-sentence Qaroshi paraphrase** and account for every participant and subordinate assertion. Separate a repaired grammar rule from a rule that merely improves the translator.

For all 96 provisional drafts, check whether any English role, negation, temporal boundary, report source, modality, metaphor or causal inference was dropped. An English glossary hit is not a licensed verb frame. Only change a case to *editor-reviewed* after its actual reading has been annotated and a counterexample or independent interpretation check has been recorded. **No score is inferred from 96/500.**

### Verb semantics

For each of the other 364 priority verbs, determine exact sense boundaries, subject and patient semantic types, optional case roles, voice applicability, passive actor versus instrument, causative participant role, and explicit negative counterexamples. Store the decision and evidence under the same stable dictionary ID. The 8.4 additions are narrow decisions for 11 existing verbs, **not** automatic permission to generalize another 364. The other non-priority dictionary verbs may also need review.

### Monolingual meaning and actual usage

Use the [Qaroshi-only practice](QAROSHI_ONLY_PRACTICE_8_4.md) to check whether learners can recover meanings from Qaroshi examples and contrasts, without reading English first. Expand the 120-core worklist into independently reviewed Qaroshi-language definitions (or explicit paraphrase examples). Count *separately* (a) written definitions, (b) editorial agreement on their meaning, and (c) external comprehension. Never present synthetically generated dialogue or TTS as real participants.

### Convergence and release gate

Before announcing that Qaroshi can independently support unrestricted conversation, require: (1) broad unfamiliar composition with no information loss, (2) productive role frames covering everyday verbs, (3) non-circular Qaroshi-only explanations of new concepts, (4) long unscripted texts and two-way conversations, (5) blinded comprehension from actual consenting people, and (6) clean validation and public documentation reflecting the same grammar edition.

*These are ongoing acceptance requirements, not a numerical promise that an arbitrary dictionary or grammar chapter count will finish a living language.*
