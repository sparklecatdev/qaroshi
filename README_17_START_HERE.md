# Qaroshi 17.0 · Everyday Communicator

**Start with:** `Qaroshi_17_Everyday_Communicator.html`. Open it on the Qaroshi website. It includes a searchable 30,000-entry dictionary and the original 26 glyph images.

## What this release actually provides

- **656 exact documented reference phrases**: all 190 original phrasebook lines, all 106 later "living speech" teaching lines, plus 360 additional compact topical references. Each retains its exact Q-reference identifier, original Qaroshi, contextual English, broad citation IPA, sound-out and editorial provenance.
- **32 coherent scripted conversations / 192 speaker turns** drawn without rewriting from earlier editorial dialogue examples. The reader separates contextual English from explicit literal/reference renderings and never calls these speaker-attested.
- **10 practical study units / 50 recall prompts**, selected from documented original phrasebook references, with locally saved completion progress.
- **390 structurally checked restricted sentence-builder practice fixtures**: safe SOV patterns with a small explicit list of permitted verb–object roles. A generated explanatory English gloss is not a guarantee of natural speech or general translation ability.
- **120 source-derived core-lemma learning cards**, ranked by reuse in the 190 original phrasebook examples, not selected by speculative etymology.
- **Full 30,000-entry dictionary**, 16 resonances, original 26 glyphs including the single-letter digraphs, pronunciation guidance, phrase search, favorites, mobile layout, scene-by-scene roleplay, local progress export.
- A transparent quality ledger: **92 of 656 displayed phrases carry v14 review warnings**, including **8 core examples that the old structural checker disagrees with**. The data remains exactly as written in the canonical bilingual source; these are unresolved flags, not automatic evidence of error.

## Four practical starting phrases

| English | Qaroshi | Why it matters |
|---|---|---|
| Hello, friend! | `zha ha, mara!` | Friendly opening with cheerful written resonance |
| Are you well? | `hë ti haro he?` | Question requires direct marker `he` |
| I don't understand. | `lën mi nu zhëmi.` | Clear repair strategy |
| Please speak slowly. | `më pëla ngëlawe shiri ya.` | Polite direct request |
| I do not consent. | `sen mi nu mahori.` | Plain boundary, not just a tone marker |
| I need help! | `khar mi dëmiwa-m sharoni.` | Alarm marker plus explicit request |

## Why grammar alone cannot solve everything

The written opening resonance is required on independent sentences. Qaroshi's regular noun cases and verb suffixes let you produce many additional words and patterns, but the dictionary's core headwords still need to be learned. Root-paraphrase alternatives from v16.1/v16.2 are not automatically accepted. The new app does not enable unapproved forms as official vocabulary.

## Known limitations

1. These phrase records were **curated from existing editorial reference files**, not independently recorded from spontaneous Qaroshi speakers. Editorial phrasebook translations still require expert checks before native-level idiomaticity claims.
2. Eight core reference lines conflict with a narrow v14 structural check (three `khe-m` question-word forms and five colloquial fragment questions without `he`). They are kept for fidelity and conspicuously marked for review. Some other phrases have evidential/complex-clause review flags.
3. Builder English is a *gloss*. It cannot freely interpret arbitrary text or handle complex negated questions; such questions are labeled as needing contextual interpretation.
4. No speech audio, actual mobile keyboard installer, or external professional proficiency certificate is supplied.
5. The learning tracker uses browser-local storage only and may not persist in private/incognito contexts. It collects no remote analytics.

## Running checks

From the project root:

```bash
python tools/v17/build_practical.py
python -m unittest discover -s tests -q
python tools/v17/browser_smoke.py
```

Browser testing requires a system Chromium and the `playwright` Python package; other tests do not. The source distribution deliberately excludes compiled font binaries.
