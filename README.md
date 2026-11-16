# Qaroshi

**A language reference, a living documentation project, and a suite of offline-first learning tools.**

**[Unified Standard 8.0 grammar](docs/standard_8/grammar.md)** · **[Current edition guide](README_STANDARD_8.md)** · **[Explore teaching tools](explore.html)** · **[Historical 7.0 Wiki](index.html)** · **[Evidence and archive policy](docs/maintenance/QUALITY_AND_ARCHIVE_POLICY.md)**

## Start here

The **current normative language edition is Unified Standard 8.0**: [one consolidated 90-chapter grammar](docs/standard_8/grammar.md), **30,001 editioned lexical entries**, explicit passive agency `-za`, and quantified scope with `nëgëra`. The original Unified Standard Reference 7.0 baseline remains frozen at **30,000 historical entries, 4,383 controlled bilingual examples, 16 obligatory written resonance markers, and 26 glyphs**. Teaching-tool releases run separately through release 23. This language revision does not claim recorded independent speaker use.

| Goal | Recommended tool | What it really does |
| --- | --- | --- |
| Look up a word or rule | [Qaroshi Wiki](index.html) | Canonical lexical and grammatical reference |
| Translate a documented phrase, read, and review | [Translation & Immersion Academy (21–23)](Qaroshi_21_23_Translation_Immersion_Academy.html) | Source-aligned reference lookup and graded editorial reading, not unrestricted translation |
| Practice pronunciation or record yourself | [Spoken Language Studio (20)](Qaroshi_20_Speech_Studio.html) | Text sound guides, drills and private local recording tools; no speaker recordings supplied |
| Practice conversational grammar and roots | [Living Language Studio (18–19)](Qaroshi_18_19_Living_Language_Studio.html) | Source-linked scenarios, pronunciation, word relationships and unapproved root proposals |
| Learn useful phrases | [Everyday Communicator (17)](Qaroshi_17_Everyday_Communicator.html) | 656 controlled teaching expressions, topic search and restricted composition |
| Follow the original foundations course | [Qaroshi Academy](Qaroshi_Academy.html) | Sixteen foundation lessons and review games |

Older research utilities and corpus-generation experiments are preserved, but appear in the separate **historical/research** section of [Explore](explore.html). They are not the recommended entry point.

## Standard 8.0 · Current language edition

The [full consolidated grammar](docs/standard_8/grammar.md), [edition guide](README_STANDARD_8.md), and [source-based decision register](docs/standard_8/DECISIONS_AND_MIGRATION.md) are the **current normative language references**. The new dictionary is generated from the preserved 7.0 lexicon and the adopted `nëgëra` overlay via `python tools/standard_8/build_standard.py`. The current enriched dictionary includes per-entry sense and verb-role notes; it is not another fabricated 30,000-word expansion. See [release notes](RELEASE_STANDARD_8.md) and the [independent comprehension protocol](docs/standard_8/REVIEW_PROTOCOL.md).

## Language amendments 24–27 · grammar and lexical meaning

The **[24–27 linguistic amendment](docs/language_reform_24_27.md)** changes the language itself: it adds **`-za` for an explicit passive actor** (distinguishing it from instrumental `-shi`), refines **22 senses of existing words** and **25 verb argument frames**, clarifies negation scope and short answer fragments, and sets stricter rules for compound formation. Historical `-shi` passive-agent sentences remain readable.

The original 7.0 grammar and 29 hashed reference sources are frozen as historical baselines. The amendment takes precedence for new, precision-oriented writing without silently changing the 30,000 canonical spellings or promoting any of the 65 reviewed but unapproved replacement proposals. New validation lives in `tools/v24_27/validate.py`; older validators remain available for reproducing historical QA.

## Qaroshi 28–34 · Functional language revision

This phase changes the **language standard**, not the website: see the [28–34 normative amendment](docs/language_reform_28_34.md) and [start-here guide](README_28_34_START_HERE.md). It adds the **`nëgëra` determiner for “not all”** with formally defined scope; gives 30 exact lexical contrasts, an 800-entry source-linked learning index, 400 verb-frame records (25 fully reviewed, 108 individually source-licensed exemplars, 267 provisional), 20 conversational usage rules, a structural audit of all 13,379 canonical compounds, and a classified register of 32 existing literary conventions. **No old word spelling or ID is replaced.** The frozen 30,000-word Standard 7.0 reference plus one post-7.0 function-word overlay gives an effective **28–34 edition lexicon of 30,001**; this is a constructed-language design decision, not native usage attestation.

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
