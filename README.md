# Qaroshi

**A language reference, a living documentation project, and a suite of offline-first learning tools.**

**[Current consolidated 9.2 editorial grammar](docs/standard_9_2/grammar.md)** · **[9.2 validation and productivity report](docs/standard_9_2/VALIDATION_AND_PRODUCTIVITY.md)** · **[Preserved 8.0 core grammar](docs/standard_8/grammar.md)** · **[Historical 8.0 guide](README_STANDARD_8.md)** · **[Explore teaching tools](explore.html)** · **[Historical 7.0 Wiki](index.html)** · **[Evidence and archive policy](docs/maintenance/QUALITY_AND_ARCHIVE_POLICY.md)**

## Start here

The **current single-entry editorial writing reference is Standard 9.2**: [the complete consolidated grammar](docs/standard_9_2/grammar.md), containing the original 90-chapter Standard 8.0 normative core and all documented 8.1–9.1 amendments. **Standard 8.0 remains the inherited normative baseline**; newer source/sense-specific additions are explicitly labeled editorial, not independently attested. The dictionary contains **30,001 editioned lexical entries**, with precise passive agency `-za` and quantifier scope using `nëgëra`. The original Unified Standard Reference 7.0 baseline remains frozen at **30,000 historical entries, 4,383 controlled bilingual examples, 16 obligatory written resonance markers, and 26 glyphs**. Teaching-tool releases run separately through release 23. This language revision does not claim recorded independent speaker use.

| Goal | Recommended tool | What it really does |
| --- | --- | --- |
| Look up a word or rule | [Qaroshi Wiki](index.html) | Canonical lexical and grammatical reference |
| Translate a documented phrase, read, and review | [Translation & Immersion Academy (21–23)](Qaroshi_21_23_Translation_Immersion_Academy.html) | Source-aligned reference lookup and graded editorial reading, not unrestricted translation |
| Practice pronunciation or record yourself | [Spoken Language Studio (20)](Qaroshi_20_Speech_Studio.html) | Text sound guides, drills and private local recording tools; no speaker recordings supplied |
| Practice conversational grammar and roots | [Living Language Studio (18–19)](Qaroshi_18_19_Living_Language_Studio.html) | Source-linked scenarios, pronunciation, word relationships and unapproved root proposals |
| Learn useful phrases | [Everyday Communicator (17)](Qaroshi_17_Everyday_Communicator.html) | 656 controlled teaching expressions, topic search and restricted composition |
| Follow the original foundations course | [Qaroshi Academy](Qaroshi_Academy.html) | Sixteen foundation lessons and review games |

Older research utilities and corpus-generation experiments are preserved, but appear in the separate **historical/research** section of [Explore](explore.html). They are not the recommended entry point.

## Standard 8.0 · Preserved normative core (historical edition)

The [full consolidated grammar](docs/standard_8/grammar.md), [edition guide](README_STANDARD_8.md), and [source-based decision register](docs/standard_8/DECISIONS_AND_MIGRATION.md) are the **current normative language references**. The new dictionary is generated from the preserved 7.0 lexicon and the adopted `nëgëra` overlay via `python tools/standard_8/build_standard.py`. The current enriched dictionary includes per-entry sense and verb-role notes; it is not another fabricated 30,000-word expansion. See [release notes](RELEASE_STANDARD_8.md) and the [independent comprehension protocol](docs/standard_8/REVIEW_PROTOCOL.md).

## Language amendments 24–27 · grammar and lexical meaning

The **[24–27 linguistic amendment](docs/language_reform_24_27.md)** changes the language itself: it adds **`-za` for an explicit passive actor** (distinguishing it from instrumental `-shi`), refines **22 senses of existing words** and **25 verb argument frames**, clarifies negation scope and short answer fragments, and sets stricter rules for compound formation. Historical `-shi` passive-agent sentences remain readable.

The original 7.0 grammar and 29 hashed reference sources are frozen as historical baselines. The amendment takes precedence for new, precision-oriented writing without silently changing the 30,000 canonical spellings or promoting any of the 65 reviewed but unapproved replacement proposals. New validation lives in `tools/v24_27/validate.py`; older validators remain available for reproducing historical QA.

## Qaroshi 28–34 · Functional language revision

This phase changes the **language standard**, not the website: see the [28–34 normative amendment](docs/language_reform_28_34.md) and [start-here guide](README_28_34_START_HERE.md). It adds the **`nëgëra` determiner for “not all”** with formally defined scope; gives 30 exact lexical contrasts, an 800-entry source-linked learning index, 400 verb-frame records (25 fully reviewed, 108 individually source-licensed exemplars, 267 provisional), 20 conversational usage rules, a structural audit of all 13,379 canonical compounds, and a classified register of 32 existing literary conventions. **No old word spelling or ID is replaced.** The frozen 30,000-word Standard 7.0 reference plus one post-7.0 function-word overlay gives an effective **28–34 edition lexicon of 30,001**; this is a constructed-language design decision, not native usage attestation.

## Standard 9.2 · Consolidated grammar and independent structural verification

The [single **consolidated current editorial grammar**](docs/standard_9_2/grammar.md) includes all 90 inherited chapters and **ten complete editioned amendments**, with one explicit precedence table for disputed morphology, participant roles, question embedding, negation, consent, time boundaries, technical inference, and figurative scope. Historical references and source hashes are unchanged. Source-based reproducibility is enforced by `python tools/stress92/build_grammar.py --check`.

**Two separate audits, not a fabricated human validation score:** `make stress92` checks all 500 previous editorial proposals against their source speech-act requirements and lexical IDs, while independently generating **450 new cross-family two-event compositions** with a separate bounded parser and mutation tests. The new suite uses 90 unseen event pairings and contrasts after/before/overlap, reported-after and polar-before. The review lists all formal findings explicitly and makes one **versioned counterfactual-scope correction** (QS81-0336: missing `qinë`), preserving the complete 9.1 original ledger. These tests **do not certify** that a reader who has not seen English can interpret the sentences; no external reader comprehension data has been collected.

For scope, methodology and human-research readiness see [9.2 Validation & Productivity](docs/standard_9_2/VALIDATION_AND_PRODUCTIVITY.md). The old 9.1 500-draft benchmark stays intact and independently reproducible.

## Standard 9.1 · Original 500-challenge editorial draft completion

[**Standard 9.1: language grammar, sense decisions and 500-case stress completion**](docs/standard_8/AMENDMENT_9_1_COMPLETE_EDITORIAL_CHALLENGES.md) adds exact 9.1 senses and rules for all **182** prior missing editorial draft challenges, spanning real-versus-negated-until event sequence, embedded relative reference, explicit non-consent and consent revocation, technical reports, metaphorical readings, and physical instrument use.

`make stress91` reproduces **500/500 editorial candidate strings**. All **318** earlier source drafts remain archived; the current 9.1 view keeps **310** verbatim and transparently repairs **8** noncanonical consent tense/modality forms, retaining their exact originals in `prior_9_0_candidate`. Frozen baseline sources are unchanged. Automated tests and a full 500-case formal audit accompany separated Qaroshi-only blind comprehension prompts and the English scoring key. This **is not 500 independently verified translations or proof of unrestricted fluency**: none of the meanings has independent human certification, and no external readers were tested.

## Standard 9.0 · Additional productive language grammar and comprehensibility evidence

The [**9.0 productive semantics amendment**](docs/standard_8/AMENDMENT_9_0_PRODUCTIVE_SEMANTICS.md) adds explicit grammar rules for **consent withdrawal and non-consent inferred from silence**, relative clauses with participant-linked reference gaps, separate ability/permission/obligation and counterfactual-barrier scopes, reported versus verified scientific claims, technical proof insufficiency, and figurative storytelling distinct from literal assertions. Each new sense uses canonical lexical words and source IDs, retains historical senses, and has adversarial regression tests.

Run `make stress90` for the original **500 unchanged challenges**: the current 9.0 evidence contains **318 editorial candidate strings**, up from **190 in 8.9**; **182 remain without full candidate drafts**. All **190 inherited candidates** receive an additional conservative formal audit. A separate blind-reading instrument, English scoring key and unresolved-case queue are generated. The released **318 are not independently certified** as natural, meaning-preserving translations; **zero** real participants have been assessed. Frozen lexical, corpus and earlier contributor files are preserved.

## Standard 8.9 · Source-grounded composition and independent review preparation

[**8.9 event composition, attitude scope and grammar rules**](docs/standard_8/AMENDMENT_8_9_EVENT_COMPOSITION.md) extend explicitly licensed event propositions across witnessed, reported, inferred, embedded-question and unasserted-content clauses; document two-event timing, past counterfactual anaphora and narrowly typed passives. The release also corrects three inherited reported-source ambiguities.

Run `make stress89` to generate an up-to-date **500-case candidate ledger** and a **separate 135-item Qaroshi-only blind-comprehension packet plus answer key**, with precise source ids, role requirements, failures and unresolved cases. Only a genuinely full editorial composition can raise draft coverage; **there are zero independently collected comprehension results**. Lexicon, grammar archives, 26 glyphs, original corpus and contributor changes remain frozen.

## Standard 8.8 · More semantic productivity (editorial)

The **[8.8 meaning and grammar amendment](docs/standard_8/AMENDMENT_8_8_SEMANTIC_PRODUCTIVITY.md)** and **[two-event temporal scope clarification](docs/standard_8/AMENDMENT_8_8_TEMPORAL_SCOPE.md)** defines five narrowly interpreted everyday sense/role families, nine precise passive/actor/instrument licensing sets, a source-to-recipient frame for “I was told that P,” and a fully articulated noun-focus-plus-present-time construction. It adds **39** new full editorial proposals to the existing adversarial set and audits the semantic requirements of **all 500** challenging English sentences. Earlier lexical spellings and frozen reference sources are unchanged.

Run `make stress88` to regenerate the honest 500-case ledger. This is not complete translation: the resulting **135 candidate strings are unverified**, **365 cases remain without a full candidate**, and independent comprehension results remain **zero**. Contextually narrowed alternatives are recorded but never counted as exact translations.

## Standard 8.4 · Narrow productive core and functional-readiness evidence

**[8.4 functional readiness and open gaps](docs/standard_8/FUNCTIONAL_READINESS_8_4.md)** · **[11 explicit core verb frames](docs/standard_8/AMENDMENT_8_4_CORE_VERBS.md)** · **[Qaroshi-only practice](docs/standard_8/QAROSHI_ONLY_PRACTICE_8_4.md)**

This edition adopts **11 deliberately narrow active verb frames** for existing high-use words, adding to the 25 previously manually reviewed general frames. It provides a reproducible 500-case review queue (**96 provisional drafts, 404 without complete drafts**), 400 verb decision cards, 120 core-word meaning review cards, and 12 blind grammar contrasts. It **does not** certify broad translation, generalize the remaining 364 priority verb frames or fabricate any real comprehension scores. Run `make stress84`; the older Standard 8.0 grammar plus adopted 8.1 clarification still governs unaffected constructions.

## Standard 8.3 · Source-grounded expression and lexicography

The [8.3 consolidated working grammar](docs/standard_8/grammar_8_3.md) includes the 8.1 embedded-polar interpretation and the current compound sense policy; historical 8.0 files remain intact. [Read the 8.3 coverage ledger](docs/standard_8/EXPRESSIVE_COVERAGE_8_3.md). Run `make stress83` to generate 500 item-specific translation proposals (only source-grounded drafts are filled), 375 restricted verb decisions, a 3,108-word canonical sense register, and a blind comprehension instrument with its answer key separate. **The edition is an editorial candidate, not independently measured fluency.**

## Standard 8.2 candidate · Expressive completeness review

[Read the 8.2 item-by-item language review](docs/standard_8/EXPRESSIVE_COMPLETENESS_8_2.md). Rebuild the 500 stress-test decisions, all 375 restricted verb audits, 1,125 valency review trials, the 3,108-compound triage, hundreds of Qaroshi grammatical minimal pairs, and four annotated connected practice readings with `make stress82`. **49 original stress prompts have unratified rule-based drafts; 451 still lack complete Qaroshi translations.** No independent comprehension or general valency approval is fabricated. Standard 8.0 plus the adopted 8.1 embedded-question clarification remains the normative language; 8.2 is an evidence-limited refinement candidate.

## Standard 8.1 · Adversarial language stress test

**[Read the 500-sentence audit and 8.1 grammar amendment](README_STANDARD_8_1_STRESS.md)** · [Prioritized linguistic triage](docs/standard_8/STRESS_TEST_TRIAGE_8_1.md) · [Embedded-question rule](docs/standard_8/AMENDMENT_8_1_EMBEDDED_POLAR.md)

A controlled adversarial set of **500 previously unindexed English prompts** (100 semantic scenarios × five transformations, ten domains) exposed a critical limit of the existing English→Qaroshi software: **500/500 abstentions**, while 30/30 source-lookup controls passed. **49** prompts now have narrowly source-grounded compositional drafts; the other **451** are not falsely labeled solved. A new adopted rule establishes `he do` for embedded *whether* questions and keeps inner and outer `nu` scopes separate. No native-speaker or unrestricted-translation success is claimed; original dictionaries and grammar sources remain preserved.

## Evidence and limitations

- **Canonical:** spelling, written morphology, the reference grammar and original glyphs. Standardized documents do not imply naturally occurring community use.
- **Editorial:** example dialogues, translations, idioms and connected readings. Much of the corpus is procedurally generated or derived from controlled templates, so size is not a reliable measure of distinct conversational coverage.
- **Provisional:** alternative transparent compounds, candidate roots and semantic review records. They are **not** adopted into the dictionary without independent review.
- **Not yet established:** independently attested natural usage, native-speaker pronunciation, regional dialect frequencies, external learner fluency scores, and open-domain translation accuracy. A text IPA guide or local voice recording interface is not an authoritative speech corpus.

The Wiki includes an **optional AI assistant** that uses an external OpenRouter service when you explicitly configure it with your own API key. The offline dictionary, learning tools and static reference do not require that integration. Treat credentials and personal review notes as private; check individual app settings before sharing a browser or exporting local data.

## Build and test

Python 3.10+ and the dependencies in `requirements.txt` are required for the Wiki and Academy builders.

```bash
python -m pip install -r requirements.txt
make build
python tools/maintenance/build_pages.py --check
python -m unittest discover -s tests -q
```

To stage the curated GitHub Pages output locally:

```bash
python tools/maintenance/build_pages.py
```

This builds `_site/` from published HTML applications only, restoring v18–23 compressed standalone pages with checksum verification. It excludes raw corpora, source code, archived test reports, local logs and intermediate data **from the public website**, while leaving all historical source files in Git. The developer source is still available for audit and reproducibility.

You can also regenerate the individual releases using `tools/v18_19/build_release.py`, `tools/v20/build_release.py`, or `tools/v21_23/build_release.py`. Some source builders intentionally retain old numbered reference names: these are historical snapshots, **not the latest release status**. `RELEASE_INFO.json` describes the earlier unified 7.0 reference; `data/site_catalog.json` identifies the current public tool collection.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [COMMUNITY_REVIEW.md](COMMUNITY_REVIEW.md). Changes to the canonical lexicon or grammar require explicit review and preservation checks. New speaker or learner evidence must be consented and described accurately, without invented attestations.
