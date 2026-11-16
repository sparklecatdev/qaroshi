# Protocol for future independent Qaroshi comprehension review

This protocol is ready for actual researchers/learners, but **no such sessions are claimed** in this release.

1. Obtain participant consent and explain that the reference is an experimental constructed language; permit withdrawal and deletion of recordings.
2. Choose a source text by ID and present the Qaroshi **without English or root glosses**.
3. Record the participant's own interpretation separately from the existing editorial English. Keep “could infer”, “literal”, and “unclear” distinct.
4. For selected word-building proposals, present source forms first without disclosing the English target; ask for literal reading and perceived ambiguity.
5. For speech, record only with explicit permission; keep metadata (pronunciation environment and accent familiarity) separate from identity and private audio.
6. Assess by an independent reviewer familiar with the published source grammar; do not grade using a machine translation as an unquestionable authority.
7. Version any ratified changes to grammar/lexicon explicitly after review. A vote or a score is not itself sufficient evidence of semantic correctness.

Recommended non-sensitive fields: `session_code,source_id,prompt_type,independent_response,uncertainty,reviewer_assessment,consent_recorded,review_status`. Do **not** put names, emails, phone numbers, raw recordings or personal identifiers into repository test fixtures.

## Empirical acceptance criteria

Before expanding a previously unapproved variant into the canonical dictionary: obtain multiple independently written contexts, demonstrate unaided correct interpretation from people not shown its English gloss, check ambiguity against existing entries, and document a reviewer decision. Machine heuristic rank is never a substitute for this step.
