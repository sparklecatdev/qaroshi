# Qaroshi • Standard Reference 2.0

**The Nardoragon language** · 26 native glyphs · 16 mandatory written resonance registers · predominantly SOV syntax · traditional base-six numerals

Qaroshi is documented here as a living, extensible language with its own script, grammar, lexicon, cultural expressions, and register system. The repository separates previously established vocabulary from newer terminology that still needs speaker review, linguistic testing, and usage examples.

## Reference statistics

| Corpus component | Quantity | Meaning |
|---|---:|---|
| Lexicon entries | **6,819** | Unique Qaroshi headwords, transparent compounds, and function words |
| Preserved established entries | **853** | Reference 1.0 spellings, glosses, and parts of speech unchanged |
| New grammatical function words | **24** | Explicitly standardized in the 2.0 grammar |
| New lexical candidates | **5,942** | Glossed concepts spanning modern technical and everyday usage |
| Transparent compounds among candidates | **234** | Modifier–head constructions with constituent analysis |
| Corpus sentences | **880** | 190 original, 660 controlled patterns, 30 advanced examples |
| Native glyphs | **26** | Original handwritten forms, including four multi-character Romanizations |
| Typed resonance registers | **16** | Mandatory initial marker on every complete sentence |
| Automated tests | **17** | Dataset integrity, script coverage, morphology and preserved canon |

**Important:** 5,942 terminology entries are marked *candidate*, not independently attested historical usage. Many are reserved Romanized forms assigned through the reproducible lexical-family builder, not words validated by a speaker community. Formal grammar and original headwords are documented separately. This distinction matters for reaching genuine modern-language expressiveness rather than just inflating a word count.

## Quick reference

Every complete sentence begins with one written resonance marker, such as `më` (Warm Hum), `zha` (Bright Trill), `sen` (neutral), `qor` (solemn), or `hë` (inquiry). There are 16 in total. Sentences are generally **Subject–Object–Verb**; direct objects take `-m`; past `-te`, future `-yu`, ability `-ki`, and predicate negation `nu` before the verb.

> `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.`  
> “Please never die so you can stay with me forever.”

That established sentence is retained without alteration. The original glyph chart and individual character artwork are under `assets/`.

## Repository map

| Path | Purpose |
|---|---|
| `docs/grammar.md` | 35-section grammar including advanced syntax and new markers |
| `docs/lexicography.md` | Editorial policy, semantic senses, usage status and revision rules |
| `docs/translation.md` | Translation procedure and annotated examples |
| `docs/roadmap.md` | Capabilities still needed for parity with contemporary languages |
| `docs/phonology_and_script.md` | Sounds, handwriting conventions, Romanization, and glyph rendering |
| `data/lexicon.csv`, `data/lexicon.json` | Searchable source-of-truth lexicon |
| `data/english_index.csv` | Reverse English index with explicit senses |
| `data/resonances.json` | All 16 registers |
| `data/pronouns.json` | Pronouns and inclusivity distinctions |
| `data/grammatical_particles_v2.json` | 24 new fixed grammatical entries |
| `data/lexicon_lock.json` | Stable assigned spellings across future revisions |
| `corpus/parallel_sentences.csv` | Bilingual reference and controlled examples |
| `assets/glyphs/*.png` | Original 26 native letter glyphs |
| `Qaroshi_Offline_Dictionary_v2.html` | Self-contained offline search and glyph converter |
| `tools/` | Reproducible build, lexical search, morphological formatting, PNG rendering, validation |
| `tests/` | Integrity and regression tests |
| `source/` | Immutable 1.0 sources and curated concept inventory |

## Try it

```bash
# Requires Python 3.10+, plus Pillow for the optional PNG renderer.
python tools/qaroshi.py lookup "resonance"
python tools/qaroshi.py lookup "nashi"
python tools/qaroshi.py morph mara --pos noun --endear --plural --case m
python tools/qaroshi.py morph goro --pos verb --tense te --aspect se
python tools/qaroshi.py check "më mi ti-m nashi."
python tools/qaroshi.py render "më ti lësha." --output cute.png
python tools/qaroshi.py validate
python -m unittest discover -s tests -v
```

Or open `Qaroshi_Offline_Dictionary_v2.html` directly in a browser. It does not require a server or online connection, and can search English meanings and Qaroshi forms. The **native converter** maps Qaroshi spelling to the original glyph artwork; it is not a general English-to-Qaroshi machine translator.

### Rebuild reference data

```bash
python tools/build_lexicon.py
python tools/build_metadata.py
python tools/build_corpus.py
python tools/build_dictionary_site.py
python -m unittest discover -s tests
```

The `data/lexicon_lock.json` and `data/domain_prefixes.json` files should be committed and treated as editorial change-control files. Existing words must not silently change spelling when new terms are added.

## Canonical status and edition policy

- **Established:** original Reference 1.0 data. Do not reassign these forms or senses.
- **Standardized:** explicitly documented new grammatical markers.
- **Candidate:** well-defined lexical senses awaiting pronunciation, usage, ambiguity, and cultural review.
- **Compound:** a lexical form built transparently from two attested or documented roots; constituents are recorded.

The 16 resonance markers, inclusive/exclusive distinction (`naru` vs. `muru`), and 26 glyph inventory are core constraints. Complete sentences need exactly one opening resonance. A quotation that contains a complete Qaroshi sentence has its own opening register inside the quotation.

## Scope and limitations

The dictionary covers thousands of modern concepts, but it is **not yet a fully attested, community-reviewed everyday language at natural-language parity**. The remaining work includes spontaneous dialogue recordings, idioms, semantic drift, pronunciation variation, regional registers, productivity testing, discourse annotation, natural parallel text, and a keyboard-ready font/IME for the native script. See `docs/roadmap.md`.

The existing script is represented by image artwork, **not assigned Unicode code points**. For programmatic interchange use UTF-8 Romanization or a sequence of the 26 glyph IDs, and display the art with the included renderer.

## Contributing and publishing

See [CONTRIBUTING.md](CONTRIBUTING.md). This directory is prepared for GitHub with source files, tests, sample workflows, and change-control rules. **No GitHub remote or push has been performed by this package build.** The original alphabet is user-supplied artwork; confirm permission and choose a license before publishing it publicly. A license has intentionally not been assigned for the project owner.
