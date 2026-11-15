# Qaroshi 14.0: Audit Findings and Editorial Priorities

**Release type:** structural and translation-risk assessment, with editorial correction proposals. No original dictionary, source grammar, glyph, or parallel-example rows were modified.

## 1. Translation consistency

The 12.0–13.0 bilingual editorial collection contains **689 sentence rows**, of which **103 had previously been flagged**. The 14.0 system retains those 103 records in `data/v14/translation_review_103.csv` and screens all 689 in `data/v14/translation_screening_689.csv`.

Priority of the **103 previously flagged** lines:

| Priority | Rows | Interpretation |
|---|---:|---|
| High | 28 | Contextual English may add or alter a participant, intended speech act, grammatical feature or significant proposition |
| Medium | 7 | An overt modal or evidential distinction may be underexpressed in a standalone translation |
| Low | 68 | Typically an old engine-coverage limitation or contextual ellipsis; not a confirmed error |

The report contains **28 individual editorial correction proposals** and **14 suggestions from previous parser interpretations**, for a total of **42 candidate standalone translations**. These are proposals, *not edits to the original source*. A human editor must review each suggestion against its scene context.

All 689 source sentences passed the validator's **limited surface-form rules**. This does not prove their syntax, semantics, pragmatics or naturalness correct. The old audit's 84 grammar-engine-declined lines should not be counted as 84 ungrammatical sentences.

### Illustrative candidate corrections

- **q12-a-price-too-low, turn 2:** `sen mi shima-m pëmi-yu.` means an unqualified future book purchase in the available grammar. “Possibly, but I want to ask something first” adds a qualification and a second intention. Candidate standalone English: **“I will buy the book.”** The original can remain as contextual narration, but should not be presented as a strict translation without an annotation.
- **q12-the-word-forever, turn 2:** `zher mi sëna nu sëmi.` uses subject **mi** (“I”), whereas “No one knows what forever means in practice” makes a broader generalization. This requires either a revised Qaroshi proposition or a note that the English is editorial commentary.
- **lit12-what-a-promise-can-contain, sentence 6:** `qor mi nënayaro ti-wa nëra-yu.` has **ti-wa** (“with you”), but the contextual English says “with them.” Proposed standalone English: **“I will stay with you today.”** Pronoun distinctions matter even in literary translation.
- **q12-the-dispute-about-a-rumor, turn 4:** `hë ti shiwaro-m shëliro-te si he?` asks about reading a message and includes direct-observation evidential **si**. The literal standalone reading should preserve whether the observation was first-hand, while contextual “Did you actually read it?” may be sufficient within the preceding exchange.
- **q12-a-friend-at-the-doorway, turn 4:** `lën mi ti-wa nu nëru-yu.` explicitly denies future rest *with you*. “I'd rather be alone right now” is plausible pragmatically but adds a present-time preference and should be annotated as a contextual paraphrase.

## 2. Repeated Qaroshi strings and translation variation

**115 same-source groups** have two or more different contextual English renderings. A simple example such as “I can fly” / “I can” can be natural when the omitted verb has already been mentioned. Other cases might change agent, polarity or degree. The exported group table is a **review index**, not a list of established contradictions. Automated semantic equivalence would need a richer parser and independently reviewed reference readings.

The separate discourse repair detector makes no arbitrary claims of logical contradiction in the original conversations: it returns review candidates only when a simple same-speaker, same-predicate polarity contrast is found.

## 3. Idioms: all 1,000 candidates retained

The earlier 25 metaphor families each contributed 40 lexical combinations. Fourteen low/medium/high risk categories are **heuristic review priorities**, not acceptance scores. Across the full list:

| Priority | Entries | Why |
|---|---:|---|
| High | 440 | Abstract metaphor productivity, impossible perceptual readings, or selectional conflict |
| Medium | 14 | Multiple possible source glosses or sense restrictions |
| Low | 546 | No special heuristic risk, but still unverified for conventional meaning |

**Zero** of these candidates has been approved by an independent speaker/community process. The full inventory remains available as an editable editorial register, with an explicit next-test instruction for each candidate.

## 4. Senses: all 5,000 cards retained

The main weakness is not that thousands of words are *wrong*, but that generic examples fail to demonstrate which meaning or verb frame is actually licensed. For example, “I see low vision” does not reliably establish that the word for low vision is a visually perceptible direct object. Revised examples should show the distinction in actual context.

| Priority | Entries | Review needed |
|---|---:|---|
| High | 4,079 | Abstract “see X” examples or unresolved verb argument frame |
| Medium | 712 | Generic adjective predicates potentially misselect subjects |
| Low | 209 | No heuristic risk; independent contextual review still needed |

**4,791** sense cards are medium or high priority, but that does **not** mean their source definitions are false. No synonym, antonym, polysemy or sense boundary has been auto-approved. All 5,000 canonical headword records remain unchanged.

## 5. Morphology and grammar

The addendum documents **20 explicit decisions** and **20 executable audit rule categories**. A new suite of **442 case, tense, aspect, modality, negation and clause-form regression vectors** checks allowed versus disallowed forms. The original 90 grammar chapters are untouched. Rules that cannot be resolved from the source alone, such as deeply nested negative scope and cross-clause anaphora, remain open in `FORMAL_DECISIONS.md`.

## 6. Next editorial gate

Before any phrase or sense is promoted into the canonical language reference, record the source example, a standalone reading, a natural contextual translation, a plausible counterexample, relevant grammar constraints, review rationale and an explicit acceptance decision. For observed dialects or speaker idioms, record independently consented usage evidence. A code test or the presence of a draft note is never sufficient as attestation.
