# Qaroshi Standard 8.1 · Embedded Questions and Clause-Local Negation

**Status:** adopted **minor grammatical clarification** to the current unified Standard 8.0. It does not replace any existing native glyph, lexeme, written resonance marker, case ending, valency frame, or frozen historical corpus. It applies to new precisely written Qaroshi and explains an edge case left ambiguous by Standard 8.0 chapter 73. This is a *constructed-language normative decision*, not attested speaker behavior.

## Problem uncovered by the 500-sentence challenge

Standard 8.0 chapter 73 already permits `do` as a content-clause boundary and `he` as the direct polar-question ending. It did **not** unequivocally identify the scope of a polar-question `he` inside a complement: a writer trying to express *I do not know whether they are well* could be mistaken for asking a top-level question or negating the embedded claim. A genuine `whether P` is **not equivalent** to either `that P` or `that not P`.

## Adopted clause-boundary rule

In a finite content complement, **`he` directly before `do` marks an embedded yes/no question**. The matrix statement continues after `do`. An independent matrix yes/no question ends with a *different*, final `he` **after** its matrix predicate.

For simple positive/negative complements with explicit participants:

```text
[RESONANCE] [embedded subject] [nu?] [embedded predicate] [he?] do
            [matrix subject]   [nu?] [matrix predicate] [he?]
```

The bracketed `he` immediately before `do` yields **whether P**. Its absence yields **that P**. Final matrix `he` asks whether the *matrix statement* is true. If both appear, they have **different clause scopes**, not two competing readings of the same sentence. Do **not** write a new resonance inside this dependent complement: the independent outer sentence already has one. Quoted independent speech remains a separate exception with its own written resonance under chapter 84.

`nu` remains attached to the next **local predicate** only. A `nu` before a matrix verb never negates the embedded proposition; a `nu` inside the complement never negates the speaker's knowledge. Speakers must name referents rather than elide them when ambiguity matters. This rule does not permit arbitrary extra `he` markers, nested `do` clauses, unlicensed verb frames, or stacked negators.

### Minimum contrast set

| Qaroshi | Precise English interpretation | Note |
| --- | --- | --- |
| `sen sa haro do mi sëmi.` | I know that they are well. | Declarative complement |
| `sen sa haro he do mi sëmi.` | I know whether they are well. | Knowing the answer does not claim they are well |
| `sen sa haro he do mi nu sëmi.` | I do not know whether they are well. | Matrix negation only |
| `sen sa nu haro do mi sëmi.` | I know that they are not well. | Embedded predicate negation only |
| `sen sa haro do mi nu sëmi.` | I do not know that they are well. | Lack of knowledge does not assert they are unwell |
| `sen sa nu haro he do mi sëmi.` | I know whether they are not well. | Embedded negative *question*, not a matrix negative |
| `hë sa haro he do mi sëmi he?` | Do I know whether they are well? | Inner `he` before `do`; outer `he` at sentence end |
| `sen sa haro he do ti nu sëmi.` | You do not know whether they are well. | Matrix person changed, same scope |

**Knowledge semantics:** `sëmi` is the existing verb *know / possess reliable knowledge*. `know that P` presents P as known; `know whether P` means the answer to the polar question is known but does **not** assert which alternative is true. `not know whether P` says nothing about P's truth. This clarification is intended to prevent fabricated assertions from translating “I don't know whether…” into “I know that not…”.

### Restrictions and compatible readings

- Only a **single** unquoted, bounded `do` complement is specified here. Multiple embeddings, multiple quantifiers, counterfactual complements, focus, or disputed reference require full manual clause analysis.
- The formal `he do` rule applies to a polar complement. For embedded *wh*-questions, use their already documented interrogative forms and preserve constituent roles; this amendment does not authorize an invented wh-marker.
- Earlier 7.0 and 8.0 texts that use two full sentences or quotation remain readable; they are **not** automatically rewritten.
- A parser with a smaller lexical whitelist can still correctly decline a grammatical sentence. The reference implementation in `tools/stress81/embedded_question.py` deliberately covers only pronouns, the documented simple predicates `haro` / `goro`, and the attested matrix verb `sëmi`. That limit is software coverage, **not a universal language restriction**.

### How to test it

The 8.1 regression suite compares *that* versus *whether*, matrix versus embedded `nu`, matrix versus embedded `he`, and malformed boundary cases. It intentionally refuses nested or structurally unsupported input. A human comprehender test is still required before claims of intuitive spoken usage.

## Status of the 500-sentence audit

The original 500 challenges cover **100 distinct situations** transformed five ways in ten domains and do not exactly duplicate the indexed prior English example sentences. The old English-to-Qaroshi tool abstained on **500/500** unfamiliar prompts; **30/30** known-source retrieval controls passed. We separately constructed **49 rule-backed, dictionary-grounded quantifier drafts** from the 500. None is labeled a speaker-verified translation. The remaining **451** have no verified complete translation in this audit. **Abstention is not evidence that Qaroshi lacks the underlying grammar.**

The challenge set, all per-item tool outcomes, positive controls and machine-readable summary are in `data/stress81/`. The exercise is not a proficiency experiment: **zero independent respondents** and no reliable open-domain accuracy estimate. Future revisions should fix the highest-priority ambiguities *only after* case-by-case semantic analysis, with source references and independent comprehension checks where possible.
