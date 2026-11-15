# Qaroshi 14.0: Language Consistency

**Status:** Tested editorial tooling and QA release. **Not** a community-ratified new standard, automatic acceptance of idioms, or proof of fluent natural usage.

## What to open

- **`Qaroshi_14_Semantic_Workbench.html`** is the new self-contained, offline editorial review dashboard. It includes corpus translation QA, competing contextual renderings, the prioritized 1,000-idiom and 5,000-sense queues, 20 grammar decisions and a browser grammar checker. Review decisions remain local and can be exported as JSON.
- **`Qaroshi_12_13_Language_Studio.html`** is the prior connected-writing and semantic learning environment, preserved.
- **`Qaroshi_Fluency_11.html`** contains the earlier bounded translation and learning tools, preserved.
- **`Qaroshi_Wiki.html`** and **`Qaroshi_Academy.html`** retain the earlier reference and study resources.

## Verified coverage

| Measure | Result |
|---|---:|
| Corpus rows screened against documented rules | **689** |
| Earlier translation flags preserved for audit | **103** |
| High-priority translation flags | **28** |
| Editorial standalone proposals, including earlier engine suggestions | **42** |
| Manually written candidate revision rationales | **28** |
| Distinct source strings with multiple contextual English renderings | **115** |
| Figurative-expression candidates prioritized | **1,000** |
| Source-linked sense cards prioritized | **5,000** |
| Explicit structural/semantic interpretation decisions | **20** |
| Explainable validation rule categories | **20** |
| New generated positive/negative grammar regression vectors | **442** |
| Python tests passing | **759** |
| Desktop/mobile browser checks passing | **27** |

All original canonical data remain unchanged: **30,000 word entries**, **4,383 parallel sentences**, **90 grammar chapters**, **26 source glyph images**, and **16 sentence-initial written resonance markers**. A set of **29 SHA-256 checksums** tracks the dictionary, corpus, grammar and original glyph images; the new project files were compared with the 12.0–13.0 release.

## New source files

- `tools/v14/semantic_validator.py`: deterministic structural and translation-risk analysis with rule IDs, scope notes and warnings.
- `tools/v14/build_audit.py`: reproducible audit of previous QA flags and candidate meanings, preserving the original source files.
- `tools/v14/build_rulebook.py`: extracts the 20 decision records and baseline SHA-256 fingerprints.
- `tools/v14/build_regression.py`: regenerates the 442 checked grammar vectors.
- `tools/v14/build_workbench.py`: rebuilds the standalone web app from its CSS, JavaScript and data.
- `tools/v14/test_browser.py`: local desktop/mobile Chromium smoke tests.
- `tests/test_standard14.py`: new structural, provenance and rule-alignment regression tests.
- `docs/v14/FORMAL_DECISIONS.md`: working interpretation register, contrasted examples, and unresolved scope issues.
- `docs/v14/AUDIT_FINDINGS.md`: transparent review priorities and specific discrepancy examples.
- `docs/v14/REVIEW_WORKFLOW.md`: editorial decision process and independent-review boundaries.

## What this does NOT establish

A high priority label is a request to investigate, not a declaration that an idiom, definition, or literary translation is incorrect. The review dashboards start with **zero new accepted idioms or senses**, and no human speaker attestation. A simple word-form checker does not establish deep semantic scope, unstated references or dialect conventions.

**14.0's software QA and prioritization goals are met.** Full linguistic acceptance, correction of all 103 contextual translations, and community standard approval remain separate editorial work.

## Build / check

From the extracted project folder:

```bash
python tools/v14/build_audit.py
python tools/v14/build_rulebook.py
python tools/v14/build_regression.py
python tools/v14/build_workbench.py
python -m unittest discover -s tests -q
python tools/v14/test_browser.py
python tools/v14/semantic_validator.py 'sen mi goro-ki.' --english 'I can fly.' --pretty
```

No compiled fonts are distributed in this release ZIP. Local native font building remains available via the prior source script with separately installed dependencies and original glyph PNGs.
