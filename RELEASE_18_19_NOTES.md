# Release notes · Qaroshi 18.0 + 19.0 · Conversation and Root Learning

## Product update

One standalone, mobile-responsive **Living Language Studio** combines an existing-grammar conversational reference with a reviewed lexical-transparency learning path. It includes a unified search, six completely navigable sections, links from Qaroshi words into the 30,000-entry dictionary, clickable phrase provenance IDs, component and compound cross-references, nearby semantic glosses (explicitly not certified synonyms), related practice paths, and direct/bookmarkable links.

**18.0 content:** 49 editorial conversation pathways / 214 documented turns, 24 pragmatic rule summaries, 32 minimal meaning contrasts, 9 parser-interpretation records, 30 context-reply drills, 10 progressive recall paths, and 93 original-reference pronunciation readings.

**19.0 content:** 1,914 canonically existing learner roots in a ranked curriculum; 13,379 pre-existing compounds accessible through component lookup; 3,817 source-grounded transparent-form proposals in separate review tiers (44 manual trial, 9 manual hold, 12 manual reject, 1,963 machine-shortlisted without human approval and 1,789 deferred); 8 unapproved root decision dossiers and 145 contextual interpretation-trial prompts. The acceptance status of **all** suggestions remains unchanged.

**Navigation expansion:** responsive two-row mobile tabs; global search across six content types with keyboard shortcut; dedicated 656-reference phrase browser; breadcrumb trail and local Back control; actual hash links to individual words, phrases, scenarios, rules, and learning units; clickable documented word components, compounds and contextual source examples; and quick-start links for newcomers.

## Validation

- Baseline reference dictionary, controlled examples, grammar and glyph sources verified against the 29 original SHA-256 records.
- 1,049 automated Python tests passed with one expected optional-compiled-font skip in the normal checkout run.
- 70 desktop/mobile offline browser navigation checks passed, with no JavaScript page errors.
- The standalone HTML is reproducibly rebuilt from Python source + embedded JSON data. No outside network calls and no compiled fonts are distributed.

## Editorial evidence boundary

This work makes the established documented grammar and vocabulary easier to navigate and practice. Dialogues are composed from editorial source phrases, not field recordings or independently observed spontaneous speaker behavior. English gloss overlap does not establish conventional synonymy, and the unapproved root and compound proposals are not silently promoted into dictionary headwords. The app can teach and inspect the documented language without fabricating attestation.

## Integration policy

This release creates new v18/v19 source paths and a new HTML app. It does not replace `main`'s existing wiki, 17.0 communicator, independent contributor work, grammar, lexicon, glyphs or legacy corpora. A separate additive-only archive is provided for safe PR review.
