# Qaroshi 14.0: Editorial review protocol

## Three separate kinds of check

1. **Structural:** source letters and native word forms, morphological suffix slot conflicts, question endings, and simple argument-role mismatches. These can often be checked with repeatable software rules.
2. **Translation alignment:** source features such as negation, modality and evidential source must be understood in the English rendering. Short conversational replies can be elliptical and still correct in context, so an automatic English cue mismatch is *not* necessarily a translation error.
3. **Naturalness / community convention:** whether an idiom is established or a sentence sounds spontaneous cannot be determined by source dictionary membership, generated text, or a grammar parser.

## Triage first, approve separately

The v12–13 audit had 103 flagged corpus rows, of which 84 included an earlier grammar-engine coverage limitation. The 14.0 audit preserves all 103 and adds a more precise rule classification. It does not auto-approve any translation. Rows have a stable `audit_id`, original and proposed English, explanation, and blank reviewer fields.

A useful review sequence for each row is: **read its source scene and adjacent turns**; identify all original morphemes; propose a strict standalone English gloss; compare the contextual English; decide whether it is a legitimate conversational inference or a semantic disagreement; if needed, revise either source or English and record why. If multiple meanings survive, mark the interpretation *ambiguous* rather than inventing certainty.

### Meaning-candidate decision rubric

For each proposed idiom or sense:
- Cite the unchanged source dictionary headword and grammatical category.
- Provide a contextual example that actually selects the claimed meaning, not a generic “I see X” sentence for a nonvisual abstract noun.
- Document any noun/verb argument-frame restrictions, synonym contrasts, and potential false friends.
- For figurative language, contrast literal versus intended figurative interpretation and specify a context in which the metaphor should *not* be used.
- Distinguish **editorial acceptance** (project standardization choice) from **speaker attestation** (recorded usage by consenting speakers). These are independent axes.

Use `accepted / needs_revision / rejected / uncertain` only after a reviewer has recorded reasoning. **The release starts with zero approved entries.** The offline audit dashboard stores personal review edits locally and offers JSON export, not a centralized community approval system.

## Reproducibility and QA

```bash
python tools/v14/build_audit.py
python -m unittest discover -s tests -q
python tools/v14/test_browser.py
```

The original `data/lexicon.csv`, `corpus/parallel_sentences.csv`, `docs/grammar.md`, and `assets/glyphs/*.png` must remain byte-for-byte identical to release 13.0. Alterations require a separate reviewed standards migration and compatibility tests.
