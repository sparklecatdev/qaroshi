# Qaroshi 8.2 · Expressive Completeness Stress Review

**Status: implemented source review and candidate semantic refinements, not a claim of 500 verified translations or measured fluency.**

The previous [8.1 triage](STRESS_TEST_TRIAGE_8_1.md) tested 500 unseen English challenges across 100 situations. The conservative translator abstained 500 times; separate source-grounded grammar supplied 49 provisional Qaroshi drafts. A translator declining input does **not** establish the language lacks the construction.

## Reproduce the review

Run these commands in the repository:

    python tools/standard_8/build_standard.py
    python tools/stress82/build_review.py
    python -m unittest tests.test_stress82 -q
    python -m unittest discover -s tests -q

The generator writes these deterministic files in data/stress82:

| Artifact | What it records |
| --- | --- |
| case_adjudications_500.csv | Each exact English target, grammatical/lexical obstacle, existing draft where any, status and required follow-up |
| verb_reviews_375.csv | Individual source citation, present licensing and restrictions for all 375 non-general verb entries |
| verb_contrast_trials_1125.csv | Three deliberately **unapproved** probes per verb: novel patient class, passive and causative |
| new_lexical_boundaries.csv | Manually authored narrow meanings for additional **existing** canonical compounds |
| compound_review_3108.csv | Current accepted versus still unresolved senses for every flagged compound |
| qaroshi_minimal_pairs.csv | Hundreds of Qaroshi-side grammatical contrasts with two readings and a normative rule witness |
| connected_passages.csv | Four original, annotated multi-sentence practice readings |
| passage_catalog.json and manifest.json | Source/status metadata, counts and SHA-256 checksums |

**Historic source files are never overwritten.** These are regenerated analysis artifacts, not unreviewed replacements for the Standard 8 dictionary.

## A · Translation coverage: all 500 cases adjudicated as to current evidence

Each item records its English proposition, target semantics, uncertainty, source-grounded draft or abstention, **candidate lexemes linked to real canonical dictionary IDs when an English indexing gloss matches**, and next review action. A matched English gloss is only a lookup suggestion: it is not evidence that the Qaroshi sense or verb frame is licensed in that sentence. Of the 500, **49 have source-backed compositional drafts** and **451 do not yet have complete Qaroshi translations**. The former are not independently back-translated or human-validated, and the latter cannot be called grammatical impossibilities. English targets are not independent readbacks. A completion claim would require a new Qaroshi draft, checked sense/argument licensing, and a meaning recovery test for each outstanding item.

## B · Verb behavior: 375 individually assessed records, not 375 blanket permissions

Standard 8 already contains 25 fully reviewed general verb frames. For all other 375, this edition audits the exact source and explicitly withholds unsupported patient classes, passives and causatives. Each root receives three targeted trial prompts. A documented existing utterance licenses only its stated lexical context unless individually reviewed counterexamples support broader behavior. The review is complete as a **source/status audit**, not as a fully productive valency approval.

## C · Compound disambiguation

The new constraints distinguish misleading English homonyms such as *wing root* (anatomical rather than linguistic), *knitted fabric* versus *knitted garment*, and *maintenance safety* versus guaranteed zero risk. The 3,108-row register distinguishes inherited Standard 8 decisions, newly authored narrow interpretations and entries still requiring editorial comparison. A flagged English component does not automatically make the existing canonical spelling defective. No old spelling is mass-renamed.

## D · Grammar contrasts

The paired Qaroshi constructions contrast **that vs whether** (embedded he before do), matrix versus subordinate nu, matrix final he questions versus statements, and universal versus negative/universal/existential focus. Both members of every embedded pair pass the previously adopted 8.1 *narrow* recognizer. This is strong evidence for a specific normative structural difference, not proof of all open-domain scope/relative-clause interactions.

## E · Sustained writing and comprehension protocol

Four original controlled Qaroshi practice texts have English target readings, per-line grammar rationale and an explicit parser support level. These were authored using existing lexical/grammar rules, **not recorded from real speakers**. The 265-item Standard 8 blind recognition instrument remains available separately; **no independent participants or measured interpretation results are claimed**.

## Stabilization gates

A claim of complete Standard 8.2 readiness would need all 451 remaining cases translated and independently checked, general valency decisions or deliberate restrictions for all verbs, high-impact ambiguous compounds resolved with context tests, tested nested/counterfactual/evidential constructions, and independent consent-based long-form comprehension studies. Until then the source audit is complete, the sample translations are provisional, and the **language-standard stabilization remains open**.

This release explicitly forbids converting source frequency, automated glosses, generated exercises or zero-response testing into claimed native-speaker evidence.
