# Qaroshi 18 + 19 GitHub sync notes

This additive branch preserves current upstream files and adds the 18/19 conversational-grammar, root-review, searchable-phrase and cross-linking sources. No existing main-branch path was overwritten.

## Getting the standalone offline studio

The full HTML is preserved **byte-for-byte** in `Qaroshi_18_19_Living_Language_Studio.html.gz`. The plain HTML file was too large for the upload gateway, so this branch stores a deterministic gzip plus the exact source builder. To restore the original file:

```bash
python tools/v18_19/restore_site.py
```

or rebuild it from the source code and dictionary data:

```bash
python tools/v18_19/build_release.py
```

Either route creates `Qaroshi_18_19_Living_Language_Studio.html` at the repository root. The archived HTML has SHA-256 `08531faa297c44e8cbad7339fa3619178438403b549be1118974f4f9ffb1deeb`.

## Quality and compatibility

- Preserve the upstream 30,000-word lexicon, 4,383 bilingual reference sentences, 90 grammar chapters, 16 mandatory written resonances and 26 original glyphs.
- The 18/19 app uses 49 teaching conversations, 32 meaning contrasts, 24 pragmatic register rules, 656 source-linked phrases, 3,817 explicitly unapproved root candidates and the prior 17.0 dictionary materials.
- No source word or root proposal is automatically adopted.
- The 18/19 test module restores the checked-in gzip if the plain HTML has not yet been built, then validates app content, source data and integrity.
- Test from a clean checkout using `python -m unittest discover -s tests -q`; for browser checks, use `python tools/v18_19/browser_smoke.py` with its documented Chromium dependencies.

The compressed asset is a distribution convenience, **not a claim that the GitHub branch contains an uncompressed HTML blob**. The Python builder remains the human-reviewable source of truth.
