# Qaroshi Standard 8.1 · 500-Sentence Stress Test and Minor Grammar Repair

**Current project:** Qaroshi Unified Standard 8.0, with the newly adopted [8.1 embedded-question and clause-local negation amendment](docs/standard_8/AMENDMENT_8_1_EMBEDDED_POLAR.md). This release adds no unrelated UI and does not rewrite the historical lexicon.

## What was actually tested

- **500 distinct, previously unindexed English challenges**, authored as **100 distinct scenarios × five controlled grammatical transformations**, equally distributed across **ten topical/structural domains**.
- Evaluated against the existing conservative English→Qaroshi translator, *without using nearest-neighbor examples as translations*. The translator abstained on **all 500**. That means its tested compositional reach is inadequate; it is **not proof Qaroshi cannot express the concepts**.
- A separate baseline of **30 documented English/Qaroshi pairs passed 30/30 exact-match retrieval controls**, confirming that the harness accesses the repository correctly.
- **49 of the 500** (quantification with documented nominal and adjectival roots) have **new source-lexeme-backed editorial composition drafts** using the already adopted grammar. They are not independently evaluated natural-language translations. **451** remain without a source-licensed complete draft here.
- **0 independently tested human respondents**, **0 verified open-domain translation successes**. No fake fluency score, fabricated speaker testimony, or unrestricted translation claim.

### Files

| File | Purpose |
| --- | --- |
| [`data/stress81/challenges_500.csv`](data/stress81/challenges_500.csv) | 500 English prompts, source category, feature and scenario-family ID |
| [`data/stress81/audit_results_500.csv`](data/stress81/audit_results_500.csv) | One record per prompt, translator result, source-linked draft where available, honest evidence status |
| [`data/stress81/audit_summary.json`](data/stress81/audit_summary.json) | Reproducible machine summary of results and limitations |
| [`data/stress81/positive_controls_30.csv`](data/stress81/positive_controls_30.csv) | 30 known source pairs used to verify retrieval, not counted among 500 unseen prompts |
| [`docs/standard_8/AMENDMENT_8_1_EMBEDDED_POLAR.md`](docs/standard_8/AMENDMENT_8_1_EMBEDDED_POLAR.md) | Adopted clarification on polar embedded clauses and scope |
| [`docs/standard_8/STRESS_TEST_TRIAGE_8_1.md`](docs/standard_8/STRESS_TEST_TRIAGE_8_1.md) | Prioritized findings, supported repairs and unresolved cases |

## Actual new rule

`he` immediately **before** content boundary `do` introduces *whether P* in an embedded polar question; a **separate final** `he` asks a matrix question. Local preverbal `nu` negates its own predicate only.

- `sen sa haro do mi sëmi.` = I know **that** they are well.
- `sen sa haro he do mi sëmi.` = I know **whether** they are well.
- `sen sa haro he do mi nu sëmi.` = I **don't know whether** they are well.
- `sen sa nu haro do mi sëmi.` = I know that they **aren't well**.

This resolves a previously underspecified contrast without a new word or phoneme, and avoids falsely turning *I don't know whether P* into *I know not-P*.

## Reproduce

```bash
python tools/stress81/run_audit.py
python tools/stress81/embedded_question.py 'sen sa haro he do mi nu sëmi.'
python -m unittest discover -s tests -p test_stress81.py -v
python -m unittest discover -s tests -q
```

The stress tests intentionally preserve a **high abstention rate** rather than inventing translations. They can be extended by independent source-grounded speaker review, but the still-unresolved cases must not be relabeled successful merely to improve a chart.
