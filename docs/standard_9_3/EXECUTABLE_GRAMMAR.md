# Qaroshi Standard 9.3: typed compositional grammar engine

**Status:** reusable, bounded editorial grammar engine, NOT an unrestricted Qaroshi parser, an English translator, or independent human-comprehension evidence.

The source of truth for the implementation is **tools/grammar93/engine.py** and its explicit selectional licenses in **data/standard_9_3/grammar_licenses.json**. The original 8.0 grammar and 25 vetted V0/V1/V2 frames in **data/semantics/valency_frames.json** are preserved unchanged.

## What it does

Unlike the earlier 500-case challenge translations, the 9.3 engine does not decode by matching fixed whole-sentence strings or original English stimuli. It constructs a typed AST with actors, patients, recipients, locations, goals, source roles, tense, aspect, polarity, modality and speech-act operators. It then renders canonical Qaroshi and separately parses that written sentence back into typed structure.

The engine covers **all 25 existing reviewed verb lemmas** but only a documented subset of their lexical roles using **ten permitted nominal forms**. Semantic classes and role admissibility are checked; source meanings are not inferred from a coincidental English gloss. V0 rejects a direct object. V1 requires an object when required by the exact frame. V2 giving requires both the physical object and its distinct recipient.

It models active basic finite predicates with exact suffix order **ROOT → TENSE → ASPECT → MODAL**, negation immediately before the finite predicate, mandatory opening resonance, polar questions ending with he?, separately attributed reports, ignorance about an embedded whether-clause, evidential markers, and binary clause connections after, before, when, if, and past counterfactual with the explicit result marker qinë.

The parser **refuses** missing or duplicated roles, reversed suffix order, inappropriate patient categories, unsupported roots, mismatched quotation/question delimiters, and unsupported passives rather than guessing a translation. A verb licensed as transitive does not thereby become automatically passive or causative; those require a separate sense-specific review.

## Use it as a command-line grammar tool

Parse a Qaroshi sentence:

    python -m tools.grammar93.cli parse 'sen mi mara-m tika-te.'

Compose one from explicit typed roles (JSON):

    python -m tools.grammar93.cli render '{"proposition":{"type":"atom","actor":"mi","verb":"tika","patient":"mara","tense":"te"}}'

The tool returns structured semantics and an acceptance/rejection status. This is **not** an independently verified English paraphrase.

A concrete V2 example is the licensed water-giving construction: **sen mi mara-tu kima-m pëli-te.** It keeps recipient mara distinct from patient kima. Reversing the case roles is a rejected input, not an alternative wording. For reported information, **sen mi mara-m tika-te do yano mi-tu shiri-te.** means an unspecified person told the speaker about the embedded sight event, without asserting the sight event independently as fact.

## Productivity evidence

Run:

    python tools/grammar93/benchmark.py
    python -m unittest tests.test_grammar_9_3 -v

The generator systematically varies permitted participants, all reviewed verb lemmas, tense, aspect, negation, modal slot, evidence, direct questioning, reported/unknown content, and **cross-verb** temporal and conditional ASTs. A separate parser must exactly recover every generated AST, rather than re-executing an English-to-Qaroshi template.

A CSV artifact contains all generated structures, Qaroshi surfaces, and recovered truth-condition metadata. Negative tests mutate cases, verb valency, modal ordering, reported source, literal polar questions and conditional scopes. The tests provide bounded structural evidence, **not** a demonstration of actual natural conversation, idiomatic semantics or complete grammar coverage.

## Unresolved, deliberately excluded language behavior

The restricted parser does not generally cover all 30,001 lexical items, open noun-derivation, all recognized passives, ellipsis, quantifiers, full relative clauses, free quotation or arbitrary recursion. These are not automatically impossible for Qaroshi. The current engine abstains where no typed license has been approved.

The complete compiled Standard 9.2 editorial grammar remains authoritative for approved reference rules. This 9.3 engine is an executable **subset**, not a new source of broad normative grammar rules. No human respondents were recruited, no independent backtranslations were collected, and software success cannot certify independent comprehension.
