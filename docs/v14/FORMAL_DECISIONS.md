# Qaroshi 14.0: Language Consistency Decision Register

**Scope:** This is an editorial consistency addendum derived from the unchanged, documented Qaroshi Standard 7.0–13.0 references. It is not new speaker evidence, a retroactive claim that the rules have been accepted by a community, or a replacement for the original 90-chapter grammar.

## Consistency principles

An **orthographic or morphological error** can sometimes be determined mechanically. A **semantic ambiguity** needs a context and potentially a reader. A **translation discrepancy** must not automatically be labeled wrong when it can represent dialogue ellipsis or literary paraphrase. A **conventional idiom** cannot be ratified merely because its components parse.

### Recorded structural interpretations

| Decision | Interpretation | Minimal contrast | Source | Status |
|---|---|---|---|---|
| D14-01 | A complete written independent sentence starts with one of the original 16 resonance markers | `sen mi goro.` vs `mi goro.` | Original resonance chapter and 8.0 addendum | Preserved written norm |
| D14-02 | A resonance expresses pragmatic stance, not the truth or evidential confidence of its proposition | `më mi goro.` vs `sen mi goro.` | 8.0 conversation guide | Preserved editorial interpretation |
| D14-03 | In nominal morphology, plural `-ri` precedes case `-m`; case slots compete | `mara-ri-m` vs `mara-m-ri` | 8.0 grammar | Preserved morphology |
| D14-04 | Verb voice, tense, aspect, modality, and optional manner are ordered slots | `goro-te-se` vs `goro-se-te` | 8.0 grammar | Preserved morphology |
| D14-05 | Past `-te` and future `-yu` cannot be simultaneously stacked in one tense slot | `goro-te` vs `goro-te-yu` | 8.0 grammar | Preserved morphology |
| D14-06 | Progressive `-se`, completive `-mo`, habitual `-në` compete within the aspect slot | `goro-te-se` vs `goro-se-mo` | 8.0 grammar | Preserved morphology |
| D14-07 | Ability `-ki`, permission `-ho`, and obligation `-du` are *different meanings* and occupy one slot | `goro-ki` vs `goro-ho` vs `goro-du` | 8.0 grammar / 13.0 lexical profiles | Preserved morphology and semantic distinction |
| D14-08 | A negator `nu` immediately preceding a predicate negates that predicate's proposition | `mi nu shiri` vs `mi shiri` | 8.0 grammar | Preserved semantic rule |
| D14-09 | A polar question ends in `he`; a request/command uses `ya`, never both in one independent finite clause | `hë ti haro he?` vs `hë ti haro ya?` | 8.0 question guide | Preserved written rule; context may distinguish requests |
| D14-10 | Direct observation `si`, reported `hu`, inferred `ye` indicate **information source**, not truth | `sa goro-te si` vs `sa goro-te hu` | 8.0 grammar / 13.0 pragmatics | Preserved semantic distinction |
| D14-11 | An evidential is placed after the finite predicate, before a final question/request particle in a simple clause | `tika-te si he?` vs `tika-te he si?` | 8.0 grammar | Editorial syntax specification; needs full quote-scope testing |
| D14-12 | Direct objects use `-m`, recipients `-tu`, companions `-wa`; one suffix cannot represent all these roles | `ti-tu kima-m pëli-yu` vs `ti-m kima-m pëli-yu` | 8.0 case chapter / 11.0 translation engine | Preserved semantic roles; some ditransitive structures remain unreviewed |
| D14-13 | English *you* and *them* are not interchangeable when source explicitly marks `ti-wa` | `mi ti-wa nëra-yu` vs `mi sa-wa nëra-yu` | Canonical pronoun reference | Strong editorial correction candidate; review in discourse |
| D14-14 | A single sentence can be literally accurate but omit evidence, aspect, or interpersonal tone in a natural contextual translation | `sen mi goro-ki.` → “I can fly.” / “I can.” with prior context | 11.0 translator and 12.0 corpus | Translation-policy interpretation |
| D14-15 | If an engine cannot parse a sentence, that does **not** establish the sentence is ungrammatical | `zher mi nu këmiro.` is a simple negative even when its English gloss is elliptical | 11.0 engine coverage audit | Corrected audit policy |
| D14-16 | Contextually supplied quantifiers, extra motives, and added agents should be annotated separately from literal translation | “I will buy the book” vs “Possibly, but I want to ask something first” | 12.0 editorial corpus QA | Review rule, not automatic source rewriting |
| D14-17 | Quoted independent sentences may have their own resonance; a random mid-clause marker does not start a new argument | Independent quote `“më mi ti-m nashi.”` | 8.0 quotation guide | Editorial recommendation; full implementation pending |
| D14-18 | Conditionals `wë`, purpose `ko`, reasons `ro` and reports `do` delimit propositions whose scope can change truth conditions | “If X, Y” does not assert X | 8.0 scope/logic | Preserved semantics; full formal parser pending |
| D14-19 | A negative followed by a positive claim in the same conversation might be a correction or update, not automatically a contradiction | “I didn't see it.” / “I did see it after looking again.” | 8.0 discourse guide | Review-only discourse detection |
| D14-20 | Contextual paraphrases, and unapproved candidate idioms/sense notes, never silently overwrite canonical entries | All 30,000 dictionary entries retained | Original source-preservation policy | Explicit release quality requirement |

## Unresolved questions requiring editorial or speaker decisions

1. Precise scope of overt `nu` in multi-clause coordination, quotation and nested modality, including multiple negators.
2. Which of the nominal case-marked phrases can be freely reordered and which require unambiguous discourse topics.
3. Valency behavior for verbs beyond the curated 11.0 translation set, especially objectless use of ordinarily transitive verbs and multi-recipient constructions.
4. Definite, generic, collective, and abstract-noun semantics when an English dictionary gloss has several readings.
5. Contrast between direct-observation `si` on a question and a statement, and reporting or inference about somebody else's observation.
6. Speaker-dependent reductions, slang, and literary resonances; without actual speaker contributions these are editorial hypotheses.
7. Interoperable native-script punctuation and tested keyboard behavior on operating systems.

**Do not mark these resolved because an automated test passes.** Tests verify the consistency of the *documented model*, not independent social usage.

## Data outputs

- `data/v14/translation_review_103.csv`: each earlier 12.0–13.0 flagged line with a review classification, source context, optional suggested standalone rendering, and empty approval fields.
- `data/v14/translation_screening_689.csv`: comprehensive corpus audit, including unflagged entries that remain unreviewed.
- `data/v14/translation_variant_clusters.csv`: competing contextual English renderings of identical Qaroshi source strings. Variation is not automatically a contradiction.
- `data/v14/idiom_review_1000.csv` and `data/v14/sense_review_5000.csv`: full lexical review register, prioritized by explicit evidence risk.
- `data/v14/discourse_repair_candidates.csv`: machine-generated possible polarity repair pairs, if any.
- `tools/v14/semantic_validator.py`: explainable rule execution and optional contextual-translation cue analysis.
