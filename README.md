# Qaroshi • Standard Reference 3.0

**The Nardoragon language** · 26 native glyphs · 16 obligatory typed resonance registers · primarily SOV syntax · traditional base-six numerals

Qaroshi has its own script, lexicon, social register system, and productive word-building rules. Standard Reference 3.0 expands both specialized language and conversational nuance while preserving the entire prior standard as a frozen baseline. The glossary distinguishes established forms from newer terminology proposed for usage review.

## Reference at a glance

| Component | Count | Notes |
|---|---:|---|
| **All dictionary entries** | **9,082** | No duplicate Qaroshi headwords |
| Preserved Reference 2.0 entries | 6,819 | Entire CSV snapshot preserved, including 853 original 1.0 headwords |
| New specialized lexical candidates (3.0) | 2,223 | 18 conceptual fields, each with explicit semantic gloss |
| New proposed grammar function words (3.0) | 40 | Time, evidence, focus, scope, discourse and consent |
| Total bilingual examples | **1,384** | 880 previous rows preserved, 504 new controlled examples |
| New documented derivations | 4 | Productive formations, *not* counted as new dictionary entries |
| Native handwritten glyphs | 26 | Original supplied images retained |
| Mandatory sentence-initial resonances | 16 | Same inventory as 1.0 and 2.0 |

**Status matters:** a new `candidate` entry has a documented English sense and stable proposed Romanization. It is **not** evidence of naturally attested speech. The 40 new grammar forms are `proposed` until reviewed. This project does not claim modern-language parity solely because thousands of entries exist.

## The central grammar rule

Every independent Qaroshi sentence begins with exactly one of the 16 **typed** resonance markers, including ordinary text messages. A subordinate clause inherits the sentence's opening resonance. `sen` is the neutral, factual register; `më` affectionate; `zha` playful; `qor` solemn; `hë` seeking information. The other eleven register particles remain documented in `docs/grammar.md` and `data/resonances.json`.

> `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.`  
> “Please never die so you can stay with me forever.”

The canonical wording has not changed. Qaroshi retains its Subject–Object–Verb order, noun case `-m`, past `-te`, future `-yu`, ability `-ki`, predicate negation `nu`, and all previously documented morphology.

## What's new in Reference 3.0?

- **Nardoragon culture:** detailed roosts, landing customs, flight mentorship, hatchling care, formation etiquette and commemorations.
- **Flight mechanics:** aerodynamics, thermals, navigation, altitude safety, weather hazards and emergency landings.
- **Social nuance:** boundaries, trust repair, affectionate friendship, grief, mutual obligations, encouragement and autonomy.
- **Specialist communication:** accessibility, human rights, medical consent, scientific uncertainty, statistics and research integrity.
- **Modern technology:** security engineering, end-to-end encryption verification, privacy, machine learning, cryptographic trust and AI evaluation.
- **Formal grammar:** event phases (not yet, no longer, about to), clausal conditional distinctions, precision quantity, document vs witnessed evidence, confidence and conversational repair.
- **Productive word formation:** four derivations for venues, outcomes, systems and evidence traces.

The 3.0 glossary entries are spread across 18 named semantic domains. Open the searchable site or CSV to see each exact entry and its review status.

## File layout

| Path | Contents |
|---|---|
| `Qaroshi_Offline_Dictionary_v3.html` | Fully offline English/Qaroshi lookup, version/status filters, phrase search, and handwritten native glyph converter |
| `data/lexicon.csv`, `data/lexicon.json` | All 9,082 entries, with stable IDs, origin, POS, exact gloss, review status and domain |
| `data/english_index.csv` | English-to-Qaroshi index including edition and review status |
| `data/grammatical_particles_v3.json` | 40 proposed grammatical function words |
| `data/morphemes_v3.json` | Four transparent derivations and their input classes |
| `data/lexicon_lock_v3.json`, `data/domain_prefixes_v3.json` | Reproducible new candidate spellings and their lexical families |
| `data/v3_lexical_review_queue.csv` | Only the 2,223 new lexical candidates awaiting review |
| `data/v3_skipped_senses.csv` | Overlapping already-covered concepts not double-counted |
| `corpus/parallel_sentences.csv`, `.json` | All 1,384 bilingual examples, with edition and pattern |
| `docs/grammar.md` | Unchanged 35-section Reference 2.0 grammar |
| `docs/grammar_v3_extensions.md` | Added sections 36–50 covering the 3.0 grammar |
| `docs/translation.md`, `docs/lexicography.md` | Editorial and translation procedures |
| `docs/roadmap.md`, `docs/release_notes_v3.md` | Further parity work and change summary |
| `assets/glyphs/*.png`, `assets/alphabet_reference.png` | Original 26-glyph Nardoragon script |
| `tools/qaroshi.py` | Lookup, morphology, derivations, rendered glyph images, validation |
| `source/lexicon_v2_snapshot.csv`, `source/corpus_v2_snapshot.csv` | Frozen source baseline that 3.0 must never silently overwrite |
| `source/curated_terms_v3.py`, `source/functional_v3.py` | Auditable new vocabulary concepts and proposed grammar |
| `tests/` | Regression tests, source preservation, corpus and script validation |

## Use it locally

Requires Python 3.10 or newer. `Pillow` is required for generating native-script PNGs. Open the HTML directly for offline use without installing anything.

```bash
python tools/qaroshi.py lookup "aerodynamics"
python tools/qaroshi.py lookup "roostmate"
python tools/qaroshi.py morph mara --pos noun --endear --plural --case m
python tools/qaroshi.py morph goro --pos verb --tense te --aspect se
python tools/qaroshi.py derive shiri --suffix=-dëno
python tools/qaroshi.py check "më mi ti-m nashi."
python tools/qaroshi.py render "më ti lësha." --output cute.png
python tools/qaroshi.py validate
python -m unittest discover -s tests -v
```

### Rebuild the complete project

```bash
make build
make validate
make test
```

The build reads **the frozen 2.0 dictionary and corpus snapshots**, not a generator that might change their existing spellings. The 3.0 locked candidate forms are deterministic. New concepts are not allowed to collide with an existing Qaroshi word; existing source IDs remain unchanged when lexemes are added.

### Review policy and community contributions

See `CONTRIBUTING.md`, `docs/lexicography.md`, and `docs/grammar_v3_extensions.md` before promoting words or grammar proposals. Disagreements about meaning, dialect, register, or naturalness should be documented, not silently overwritten. The native alphabet is provided as original image artwork rather than an installable font or assigned Unicode character set.

**Publication:** This ZIP does not automatically change a GitHub repository. The source artwork and code have no chosen license in this draft; verify contributor permissions and select a license before public distribution.
