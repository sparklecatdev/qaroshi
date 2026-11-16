# Qaroshi Unified Standard 8.0 · Current Language Reference

**Use this edition for new Qaroshi writing.** It consolidates the original 90 grammar chapters with the adopted 24–34 amendments, gives one 30,001-entry editioned dictionary, and adds precise decisions for verb arguments, compounds and two-quantifier scope.

For later editorial additions, also consult [8.4 core verbs](docs/standard_8/AMENDMENT_8_4_CORE_VERBS.md), [8.5 attempted actions](docs/standard_8/AMENDMENT_8_5_ATTEMPT.md), and [8.6 everyday meanings and content clauses](docs/standard_8/AMENDMENT_8_6_EVERYDAY_MEANING.md). These additions are not independent evidence of speaker use.

## The authoritative reference

- [Full current grammar, all 90 chapters](docs/standard_8/grammar.md). Its current rules are integrated in the relevant historical chapters rather than stored only in detached release notes.
- [Migration and source-status guide](docs/standard_8/DECISIONS_AND_MIGRATION.md), explaining the new case `-za`, `nëgëra`, source-limited verb permissions and preserved legacy interpretations.
- [Independent comprehension protocol](docs/standard_8/REVIEW_PROTOCOL.md). Provides a blind instrument, separated answer key and scorer without fabricating participant results.

### What is actually adopted

1. **Editioned dictionary:** All 30,000 legacy forms and stable IDs, plus `nëgëra` (Q8D001) from 28–34. The full current bilingual lexicon, with source-linked sense and argument notes, is generated as `data/standard_8/dictionary_enriched_30001.csv.gz`. A base-schema export is also produced.
2. **Voice and case:** Explicit passive actors use `-za`; instruments use `-shi` in new precise writing. Historical agentive `-shi` remains understandable.
3. **Quantifier scope:** In a simple independent clause with two overtly quantified NPs, the *leftmost quantifier is wider in scope*; case marking independently identifies subject/object. `nëgëra` is available before a quantified object `-m` under these new, narrow 8.0 restrictions. Embeddings, rhetorical questions, tense or other complex structures remain outside this restricted convention unless independently specified.
4. **Verb evidence:** Every one of the 400 highest-priority existing verbs has a recorded source review decision. **25** are general manually reviewed frames; the rest have explicit limited example permissions. No novel passive, arbitrary patient class or causative is inferred from a single editorial sentence.
5. **Compound semantics:** **40** additional individually authored narrow sense restrictions and **12** preserved rejected false-friend proposals. All **3,108** previously flagged compounds are preserved with review status, not automatically rewritten.
6. **Evaluation:** **265** blind comprehension items with a separate answer key and local scoring utility. These are available to test, but **zero independent learners have been recorded** by this release. Do not market the instrument as a measured comprehension study.

### A new meaning contrast

- `sen shërano qaro ngënao mara-m tika.` = one or more Nardoragons each see **every** relevant friend (∃ subject ∀ object).
- `sen ngënao mara-m shërano qaro tika.` = **every** relevant friend is seen by at least one Nardoragon (∀ object ∃ subject).

These are newly specified **editorial constructed examples**, not quotations from speakers. The two statements can have different truth values. They may not be simplified into the same English statement.

## Build / test from a Git checkout

```bash
python tools/standard_8/build_standard.py
python tools/standard_8/validate_current.py 'sen shërano qaro ngënao mara-m tika.'
python -m unittest tests.test_standard_8 -q
python -m unittest discover -s tests -q
```

The current source generator uses the existing standard library and the repository's preserved original lexicon/corpora. It never modifies the frozen 7.0 reference files. The repository's `make build` also runs the standard generator before the main site build.

## Data ownership and ethics

This is a **constructed-language editorial standard** with mechanically checkable grammar restrictions. The archived corpora are editorial texts, not independent evidence of spontaneous speaker use. The answer key must not be shown to blind participants; private responses should not be committed to GitHub. A real-world language comprehension study is a separate human activity and is not fabricated by this release.
