# Qaroshi Standard 9.4: complete original-English semantic requirements

**Scope:** a complete source-based, machine-readable semantic-intent ledger for the original 500 English challenge cases, including the 190 old drafts that lacked modern comparable structured annotations. No claims of independent comprehension, human attestations, or 500 certified translations.

## Why 9.4 matters

Standard 9.2 structurally examined all 500 candidate Qaroshi strings and compared structured semantic fields for 310 cases. Earlier editions left **190** candidates without comparable modern semantic signatures. Their lack of signatures is a documentation gap, not evidence they are correct.

The executable backfill in **tools/semantic94/complete.py** recovers the intended source meaning from the original immutable **tools/stress81/scenarios.py** scenario tuples, not by guessing from the Qaroshi sentence, reverse-translating an English gloss, or fabricating a speaker judgment. It does not alter any original grammar chapter, stimulus, dictionary, previously drafted surface string, or versioned correction.

Each of the 500 records has explicit English source roles and domain-specific structure: who acted, what action or patient, whether a reported claim is asserted independently, reference and time ordering, relative head/reference, condition and hypothetical consequence, permission versus actual action, physical instrument versus agent, literary nonliteral interpretation, and technical premise P versus unsupported conclusion Q.

The requirements include **controlled non-entailments**, such as permission or ability not automatically causing action, revoked consent not being reinstated by silence, report/inference not proving P, and P alone not establishing Q. They are source-grounded *intent constraints* that future review must compare with Qaroshi, not evidence that Qaroshi already expresses every condition exactly.

## What is completed

- Every original 500 English source case now has one source-based typed semantic-requirements JSON record.
- Exactly **190** cases without earlier structured modern signatures get explicit 9.4 backfilled requirements.
- The **310** previously annotated modern source candidates retain their versioned structured records, alongside the source-derived intent fields.
- The 9.2 versioned repair of the one missing counterfactual result marker qinë is retained in the current editorial view, with the 9.1 original unchanged.
- Tests ensure each backfilled source role and scenario component is drawn from its corresponding original author-controlled scenario tuple, that no English stimulus has changed, and that no rater score or spoken-language attestation was invented.

## Output and review procedure

Run:

    python tools/semantic94/complete.py
    python -m unittest tests.test_semantic_9_4 -v

Generated evidence is under **data/stress94/**:

- **source_semantic_requirements_500.csv**: every original prompt, source-side typed meaning, current 9.2 Qaroshi candidate, any earlier structured annotation, and source/equivalence status.
- **legacy_190_backfilled.csv**: exactly the older 190 with newly completed source-intent requirements.
- **independent_comprehension_review_queue.csv**: 500 separate reader/rater slots, initially blank.
- **summary.json**: counts, original-source preservation, review status, zero independent comprehension.

The next genuinely **semantic** experiment must place a randomly selected Qaroshi sentence in front of consenting respondents who did not see the English source, and ask them to independently recover referents, roles, tense, negation, permission, questions, and logical implications. Score the response against the original-English requirement after collecting it. Any failed draft should receive a source-preserving versioned correction and re-test.

A prefilled source-intent record is not an independent human paraphrase and must never be counted as one. The installed grammar engine (9.3) deliberately covers only a restricted executable subset; it cannot adjudicate free-form metaphor, quantification, and the other 9.4 source requirements by passing its limited AST tests.

**As released, the all-500 original draft benchmark remains editorial, not independently certified.** All 500 still require semantic comparison with real readers. The narrow 9.2 structural audit reached zero flags only within its implemented checks; that does not establish idiomatic language quality or truth-conditional equivalence.
