# Qaroshi Standard 8.0: Decision register, interpretation and compatibility

## The single current reference

New writing should use [the consolidated grammar](grammar.md) and the `data/standard_8/dictionary_30001.csv.gz` editioned dictionary. The current grammar contains all **90** historical chapters with additional current-norm rulings inserted at relevant chapters. In particular, `-za` is the overt passive actor case, `-shi` is instrumental for new precise writing, and `nëgëra` is the adopted non-universal quantifier. The current 30,001-entry lexicon is exactly the preserved 30,000 historical headwords plus the editioned determiner `Q8D001`.

## What has been decided

- **Verbs:** 25 earlier fully reviewed verb-sense frames remain general authorities. All 375 other indexed verbs have individual source-grounded review decisions. A cited controlled sentence authorizes exactly its documented construction; it does not create a productive passive or a new class of patients. `verb_audit_400.csv` gives the status and best exact source per lemma. Any broader frame is a *separate future lexical decision*. No uncertainty is buried as an unrestricted norm.
- **Compounds:** 40 individually reasoned existing-word sense restrictions, together with 12 earlier rejected false-friend replacements, are in `lexical_decisions.csv`. All 3,108 previously flagged compounds are prioritized in `compound_risk_register.csv`. A flagged English multi-gloss is a review risk, not a claim of defective spelling. All canonical forms remain unchanged.
- **Scope:** new simple **two-quantifier** clauses with two overt counted NPs have deterministic **surface-first widest** scope and independent subject/object marking. This new Standard 8.0 permission extends `nëgëra` from 28–34 subject-only use to an **overt `-m` object** when every structural restriction is met. Embedded, focused, modal, time-shifted, rhetorical and multiply nested clauses require explicit decomposition; the included `scope.py` refuses to guess.
- **Comprehension:** the language can now be independently evaluated with 265 blind recognition items and a separate answer key. No external human responses have been measured. Thus there is no claim of empirically demonstrated naturalness.

## Migration and backwards reading

- All prior stable IDs, spelling, original examples, original source SHA-256 and chapter numbers remain untouched. The historical 7.0 reference and 24–34 amendment files remain available to reproduce old publications.
- Historical passive-agent `-shi` retains its historically documented interpretation in older context. New exact writing uses `-za`. The old text is **not mass-rewritten** because some earlier `-shi` cases actually mean instruments.
- Older `ngënao ... nu P` means all not P (none), never new `nëgëra ... P` (not all). Reconstruct domain and scope explicitly when translating.
- Compounds with misleading component homonyms retain lexicalized canonical meanings. Example: `bekazoshërawëlon` denotes an abrasive nail-care file in the current dictionary; its head also has a digital-file sense, which must not be inferred from the canonical compound.
- Source-derived status is not the same as a spoken usage convention. The historical corpus contains heavily repeated editorial patterns. Version 8 preserves these as provenance, not as independent attestations.

## Remaining human-linguistic evidence

Observed naturalness, spontaneous speech, learner comprehension, oral pronunciation, and conventional metaphors **cannot be completed by an offline code/build process without real participants**. The protocol and scoring system are prepared, but no fake speaker judgments or external validation results are entered.
