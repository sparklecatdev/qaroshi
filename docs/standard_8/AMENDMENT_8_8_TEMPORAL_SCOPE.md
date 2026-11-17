# Qaroshi 8.8 · Two-event temporal clause scope

This amendment clarifies the **already documented** `ana` (after), `ëna` (before), `yaro` (when/while), and `torëne` (until endpoint) clauses without adding any new alphabet symbols, altering any historical dictionary entries, or claiming naturalistic validation.

## Event-ordering template

For precision writing, when the subordinate clause is explicitly introduced before the main clause, use:

`RESONANCE CONNECTIVE SUBORDINATE-SUBJECT ... SUBORDINATE-PREDICATE, MATRIX-SUBJECT ... MATRIX-PREDICATE.`

Only one opening resonance applies to the entire sentence. No second register is introduced after the comma. Both finite predicates retain their own independent tense, aspect, negation, and case roles. The connective determines the relation of the *matrix* event to the *subordinate* event:

| Connector | Relation between events | Restricted illustrative example |
| --- | --- | --- |
| `ana` | Matrix happens **after** subordinate | `sen ana sa goro-te, mi nëru-te.` = After they flew, I rested |
| `ëna` | Matrix happens **before** subordinate | `sen ëna sa goro-te, mi nëru-te.` = Before they flew, I rested |
| `yaro` | Matrix overlaps subordinate in time | `sen yaro sa goro-te-se, mi nëru-te-se.` = While they were flying, I was resting |
| `torëne` | Matrix state holds up to a specified endpoint | `sen torëne sa goro-te, mi nu nëru-te.` = I did not rest until they flew, without asserting that I rested afterward |

These illustrate **a reusable grammatical construction** using existing documented verb roots and arguments. They do not by themselves translate the stress test's arbitrary couriers, bridges, ferries, captains, and instruments. Those still need their own lexical frames and source-verified event descriptions.

## Semantics that must survive translation

- **After** cannot be replaced with **before** without reversing the event ordering. Both clauses have their own subjects; switching them changes the truth conditions.
- **While** is an overlap relation, not necessarily simultaneous beginning or simultaneous ending. The restrictive examples use progressive `-se` in both clauses to make overlap explicit. Other event shapes require further sense-specific review.
- **Negative until** is particularly hazardous. An English `not P until Q` often suggests that P happened after Q, but that is not guaranteed by the bare restricted Qaroshi scope. State the later positive P in another clause if it is an asserted fact. Do not infer that Q caused P.
- **Tense** `-te` is past relative to its clause's reference time, not evidence that one clause was completed *because* of the other. Aspect `-mo` would mark completion explicitly where licensed.
- **Questions** about ordering need documented matrix-question scope. The new restricted recognizer does not accept them, so the unsolved question variants in the original challenge set are not silently promoted.

## Machine check and limits

`python -m tools.stress88.temporal "sen ana sa goro-te, mi nëru-te."`

The checker accepts only overt subject pronouns `mi`, `ti`, or `sa`, three already-established intransitive verbs (`goro`, `nëru`, `shërami`), two finite time suffixes, a narrow range of aspect suffixes, and a two-clause sentence with the specified boundary punctuation. It rejects unrecognized forms instead of guessing. It is **not** a general Qaroshi parser, has no human comprehension evaluations, and does not establish whether a particular invented conversation sounds natural.

The stress test remains **135 unverified candidate strings out of 500** with 365 prompts lacking full candidates. This construction improves the language specification but deliberately does **not** increase that count without properly translated lexical participant/event frames.
