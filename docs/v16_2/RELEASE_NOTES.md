# Qaroshi 16.2 Release Notes

**Status:** Development milestone, backwards-compatible; no canonical lexical adoption.

This release carries forward the exact 30,000-entry reference plus the verified 16.1 source, adding an editorial/semantic decision layer. It creates no conventional idiom, naturalistic speaker record or new canonical lexeme.

## Contents

- `data/v16_2/all_3817_candidates_screened.csv`: every source proposal, senses, source word, spelling, risk codes, score and distinct status.
- `data/v16_2/individually_editorially_reviewed.csv`: 65 specifically inspected records, with detailed rationale (44 controlled trials, 9 holds, 12 rejections).
- `data/v16_2/machine_shortlist_unapproved.csv`: 1,963 machine-ranked but unreviewed suggestions.
- `data/v16_2/eight_root_decision_dossiers.csv`: 8 candidate root sense boundaries, pronunciation guesses, nearest spellings and missing-concept reuse analysis.
- `data/v16_2/reuse_before_coinage.csv`: 8 cases where existing words or suffixes should be investigated first.
- `data/v16_2/hypothetical_new_root_derivatives.csv`: 26 restricted experimental compounds.
- `data/v16_2/sixteen_grammar_and_learnability_examples.csv`: grammar-versus-vocabulary contrasts.
- `Qaroshi_16_2_Root_Standardization_Studio.html`: standalone 30,000-word dictionary and candidate comparison app with local notes and export/import.
- `tools/v16_2/`: reproducible audit, pronunciation, documentation, and app builders; Chromium check script.
- `tests/test_v16_2_lexical_decisions.py`: individual human-editorial-trial, false-friend, source-integrity and root tests.

## Pending review

There are **zero approved canonical replacements** and **zero speaker-attested newly coined roots**. The word-list learning benefit is a hypothesis requiring real speaker feedback. The source ZIP is standalone; any GitHub checkpoint is not equivalent to publication of the entire archive.