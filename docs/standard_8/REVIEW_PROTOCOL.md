# Standard 8.0: Independent comprehension and lexical review protocol

This standard **provides** a complete 265-question blind instrument but does **not pretend** anyone has already taken it. It is intentionally a separate, opt-in procedure with reproducible scoring, not a requirement that future contributors surrender personal data.

## Purpose and scope

Test whether unfamiliar readers can distinguish documented sentence meanings, the surface scope of two quantifiers, and lexicalized compound senses. Do not use the recognition score as proof that someone can speak, translate freely, or understand spontaneous audio. Participants must not receive `sealed_answer_key.csv` before the test.

## Prepare and administer

1. Use the immutable editioned `data/standard_8/blind_comprehension_prompts.csv` and generate a response sheet using `python tools/standard_8/score_comprehension.py --blank responses.csv`.
2. Recruit at least five independent consenting learners, ideally including novices. Record only anonymous reviewer IDs, which must be distinct within the private response file; no real names, recordings, identifiers or addresses are needed.
3. Explain that some constructions are newly authored, not observed from spontaneous speakers; offer a way to decline without penalty. Randomize prompt order per participant and avoid explaining the target contrast during the test.
4. Collect exactly one of `A`, `B`, `C` per completed item, with an optional free-text uncertainty note. The items include source-matched translations, reconstructed syntax and editorial norm-setting cases. Preserve each item’s provenance.
5. Score by `python tools/standard_8/score_comprehension.py --responses responses.csv --out private_report.json`. Keep raw response files and private reports out of the repository unless contributors explicitly authorize publication of anonymized aggregates.
6. Review confusion by category and item, using the **original Qaroshi construction** rather than treating low scores as evidence the learner is deficient. A bad distractor or editorial English gloss can cause a false positive.

## Before adopting further language changes

- For verb roles, present at least three previously unseen examples per candidate sense (different objects where possible), plus counterexamples with disallowed role classes. Rate consistency separately from grammatical accuracy.
- For compound components, ask independent participants to interpret the form *before* revealing its canonical English gloss. Compare the specific literal reading, lexicalized interpretation, and alternate domain senses. No automatic replacement from a machine gloss.
- For logic, test truth conditions with both distributive and counterexample scenarios, including one setting where not all P but **none** P.
- For speaking, consented human audio would be required for phonetic generalization. This written instrument does not validate pronunciation or dialect.
- A review decision requires recorded reviewer agreement, counterexamples, a migration/compatibility plan, and a human editorial signoff. No new headword spelling is silently published by this research protocol.

**Status:** the instrument and scorer are complete, administered respondents = **zero**. This count must not be represented as a completed independent proficiency study.
