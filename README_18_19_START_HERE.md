# Qaroshi 18.0 + 19.0 · Living Language Studio

This is one combined, **offline** everyday-language and productive-root teaching release. Start by opening **`Qaroshi_18_19_Living_Language_Studio.html`** in a browser. No network, account or external JavaScript is required.

## Navigate the studio

- **Find anything**: the top search searches conversations, documented phrases, dictionary words, grammar summaries, root proposals and practice paths. Press **Ctrl+K** or **⌘K** (or `/` outside a text box) to focus it; press Escape to close results.
- **Conversations**: 49 source-linked teaching scenes (214 turns). Every Qaroshi word with a canonical dictionary entry is an actual click-through link, and each source ID opens its original phrase record.
- **Everyday phrases**: 656 existing, documented teaching phrases, searchable by Qaroshi, English, category and ID. Follow links from phrase to words, related phrases and example conversations.
- **Grammar & meaning**: 24 existing-rule teaching summaries and 32 contextual minimal contrasts, with linked words for quick interpretation.
- **Dictionary & roots**: search all 30,000 canonical words. A word page links documented components, compounds that reuse its roots, related dictionary glosses, source usage, root-review proposals, and nearby grammar. Similar English glosses do **not** imply established synonymy.
- **Practice**: 10 guided recall paths and 30 situation-sensitive reply choices. Review your answers and open linked vocabulary. Study progress is local to your browser, with JSON export/import.
- **About**: methodology, provenance, and data controls.

The navigation works by ordinary browser **hash URLs** (examples: `#phrase/S00001`, `#word/mi`, `#talk/C18-001`, `#grammar/G18-001`, `#proposal/banuaro`, and `#practice/P18-01`). You can bookmark or copy a direct link. Breadcrumbs, Back, related links and mobile two-row navigation are built in. None of these links changes the dictionary.

## Language and provenance

The 18.0 layer organizes real, already documented grammar into a coherent conversational curriculum, including 24 rules, 32 meaning distinctions, 9 documented parser-interpretation cases, 30 answer-in-context drills and 93 exact-reference IPA reading prompts. It **does not invent spontaneous speech attestations** or automatically rewrite colloquial and question forms that disagree with older parser assumptions.

The 19.0 layer prioritizes learning existing roots and reviewing 3,817 optional transparent alternatives, retaining 44 controlled editorial trials, 9 semantic holds, 12 semantic rejections and 3,752 machine-unapproved/deferred alternatives. All 8 new-root dossiers remain proposals. **No new words or renames were automatically added to the canonical standard.**

Canonical lexicon (30,000 entries), bilingual reference (4,383 entries), 90 grammar chapters, 16 written resonance markers and 26 original native glyph images remain unchanged. Outside contributions are protected by distributing the new features in **additive v18/v19 paths**, separate from existing application files.

## Build and test

From the root of the extracted full source package:

```bash
python tools/v18_19/build_release.py
python -m unittest discover -s tests -q
python tools/v18_19/browser_smoke.py
```

The last command needs `playwright` and a local Chromium executable at `/usr/bin/chromium`; the offline HTML does not. The standalone HTML can be copied anywhere and opened without a server.

## Integrating into an existing GitHub checkout

Use `Qaroshi_18_19_Additive_Source_Patch.zip` for a **non-destructive overlay**. It contains only new versioned paths, tests and release notes, not replacement copies of your existing dictionary, wiki, or 17.0 communicator. Check your current branch first, review the path list, then extract and commit on a new branch. Do not overwrite a conflicting path if someone else has added it meanwhile. Its new build script expects the existing v15–17 source/datasets already present.
