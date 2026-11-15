# Translation quality method for the new editorial corpus

The review script `tools/v12_13/quality_checks.py` compares 689 source sentences with their contextual English editorial readings. It flags a possible issue when visible grammatical features are not explicit in the English rendering. It also notes when the 11.0 grammar engine declines a literal translation.

These are **review hints**. For example, an English answer “I can” may encode ability `-ki` even without a following verb, and “I disagree” can correctly render the Qaroshi negation of “agree.” A source utterance with `he` must be read as a question even if a narrator's English sentence says “I asked whether...” in indirect speech; such sentences were revised in this edition to keep the independent question overt. The 103 flagged lines should be examined in their surrounding story, not automatically rewritten to satisfy a string match.

A trustworthy translation release needs two separate reading fields:

1. **Literal/interlinear reading:** the words, semantic roles, cases, tense/aspect/modality, negation scope and evidential markers explicitly supplied.
2. **Contextual English:** a coherent natural-language version that may recover antecedents or implied context; any non-entailing additions should be transparent.

The machine-parsed field is not a ground truth reference. It is useful when a grammar construction belongs to its supported finite SOV subset, but may leave complex clauses unresolved. The semantic profile review and new separate texts should be used to develop unseen human-checked evaluation data rather than evaluating the translator on examples it already memorized.

## Scope traps

- `-ki` ability vs `-ho` permission vs `-du` obligation.
- `hu` reported vs `si` witnessed vs `ye` inferred. An evidential does not prove the claim.
- `naru` inclusive we vs `muru` exclusive we.
- `nu` must negate the intended predicate rather than an unrelated noun or speaker stance.
- A native textual resonance marker conveys social framing, not grammatical gender or a factual endorsement.
- `nashi` can express care that is not romantic or sexual.
- `naro` as dwelling is not automatically `runa` as chosen family.

After review, add newly accepted minimal contrasts to the regression suite and record any grammar change with an explicit compatibility note. Preserve all existing lexeme IDs and original glyphs unless a reviewed revision specifically authorizes a change.
