# Qaroshi Standard 11.0: meaning and conversational clarity pilot

**Status:** Editorial learning improvement, not independent human attestation, new normative grammar, a new dictionary edition, or an unrestricted translator. The preserved 8.0 core and consolidated 9.2 editorial interpretation continue to govern.

## Implemented work

- Thirty new case-specific interpretive explanations tied one-for-one to the thirty existing 28–34 semantic boundaries. Each includes a comprehension question and a forbidden inference. Existing source status is displayed separately from new unvalidated teaching commentary.
- Twenty new situational conversation exercises tied to the existing twenty usage rules. They distinguish ambiguity, self-repair, hearing-repair, short replies, topic change, reported evidence, and consent.
- Exact-morphology source matching to the frozen 4,383-sentence teaching corpus: each lexical contrast links an actual recorded example when one exists and displays an explicit missing-example state otherwise. No examples are fabricated or claimed to be native-speaker use.
- An offline interactive Wiki Meaning workshop (route #meaning). Learners can search both teaching collections, open canonical word pages, compare meanings, and reveal the editorial answer after attempting the exercise.
- Build-time source provenance checks and regressions. No original spellings, corpus lines, glyphs or older contributors' work are rewritten.

## Linguistic interpretation sequence

1. Find sentence boundaries and the initial resonance. A fragment and an independent finite sentence are different constructions.
2. Identify all participants and case roles. When two referents compete, require an explicit noun instead of guessing which pronoun was intended.
3. Match the verb to its *exact licensed meaning and role structure*, not to any vaguely similar English translation.
4. Recover clause and quantifier scope. Distinguish negation, not all, none, questions, modalities and counterfactuals.
5. Separate lexical assertion from speaker intention: a warm resonance does not make a claim romantic, grant consent or establish truth.
6. Distinguish firsthand, reported and inferred information. A report does not assert its embedded claim as an independently verified fact.
7. Preserve the target of a correction. Hearing repair, claim revision, paraphrase and verbatim quotation are different discourse acts.
8. Ask for clarification if the sentence admits multiple readings. Never silently invent an argument, timeline or implicature.

This sequence consolidates *existing* Qaroshi source decisions; it is not a general license to extend all verbs or an adopted new particle.

## What remains unproven

The targets of 1,000 individually reviewed core words, 250 reviewed productive verb frames, 100 natural independently authored dialogues and actual first-pass blind-reading outcomes are **not** met by automatically generating rows. Existing resources include a core 800-word editorial queue, twenty-five fully reviewed verb frames, and a reader-only 80-item study kit. Real editors and consented independent learners must review and submit results before expanding claims.

## Verify

Run:
    python -m tools.standard11.assemble
    python -m unittest tests.test_standard_11 -v
    python -m unittest discover -s tests -q
    node tests/standard11/ui.cjs
    make build

Data provenance: data/v28_34/meaning_boundaries.csv and data/v28_34/conversational_usage_rules.json. New commentary: data/standard_11/contrast_guides.json and data/standard_11/dialogue_challenges.json. See also docs/standard_10/README.md for the existing privacy-respecting independent-reader protocol.
