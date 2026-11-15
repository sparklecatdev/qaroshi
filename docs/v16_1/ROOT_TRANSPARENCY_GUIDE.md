# Qaroshi 16.1: Less memorization through transparent roots

## Executive answer

**Grammar does not let you guess every base word.** Qaroshi already has 13,379 canonical transparent modifier–head compounds, but 16,525 entries are labeled headwords with no official component analysis. This update audits every such headword, generates proposed ways to express some technical concepts with established roots, and identifies missing common building blocks. None of the proposals is automatically accepted as a new standard spelling.

## Verified categories (all 16,525 labeled headwords)

| Result | Headwords | Meaning |
|---|---:|---|
| Established headword spelling matches two dictionary stems | 2 | Possible metadata reclassification, not a new word |
| Complete split using the primary meanings of both components | 2,662 | Exact modifier–head editorial proposal |
| Complete split requires a secondary dictionary sense | 146 | Higher ambiguity risk; review carefully |
| Some documented meaning clues, no licensed complete form | 7,749 | Teach related words, do not coin from guesses |
| No documented component analysis | 5,966 | Learn as conventional roots pending reviewed analysis |

The candidate catalog has **3,817 alternative suggestions** for **2,808 canonical headwords**, including multiple choices for some English glosses. Only one default alternative per headword appears in the simple browser view; all alternatives appear in the CSV. The two existing-forms cases do not produce any new proposed spelling.

## Grounded examples from the canonical dictionary

| Canonical word | Canonical meaning | Proposed transparent segmentation | Review status |
|---|---|---|---|
| `banuaro` | wing joint | banu (wing) + qamago (joint) → **banuqamago** | primary_gloss_candidate |
| `bamusu` | fire hydrant | punushu (fire) + zhidayëni (hydrant) → **punushuzhidayëni** | primary_gloss_candidate |
| `babalu` | patch management | khugola (patch (software)) + hëzhore (management) → **khugolahëzhore** | primary_gloss_candidate |
| `baragë` | mutual agreement | qanëtohu (mutual) + këmu (agreement) → **qanëtohukëmu** | primary_gloss_candidate |
| `bebumo` | industrial safety | qulonë (industrial) + nohowa (safety) → **qulonënohowa** | primary_gloss_candidate |
| `bebira` | laboratory equipment | sugewa (laboratory) + rëwuze (equipment) → **sugewarëwuze** | primary_gloss_candidate |
| `betasho` | quality control | zhuyokhula (quality) + pudihoto (control) → **zhuyokhulapudihoto** | primary_gloss_candidate |
| `dahokhoge` | water quality | kima (water) + zhuyokhula (quality) → **kimazhuyokhula** | primary_gloss_candidate |
| `limabo` | weather station | lugoqa (weather) + pagaze (station) → **lugoqapagaze** | primary_gloss_candidate |
| `benusë` | emotional boundary | payeti (emotional) + noha (boundary) → **payetinoha** | primary_gloss_candidate |
| `bewëru` | wing strain | banu (wing) + gungango (strain (injury)) → **banugungango** | primary_gloss_candidate |
| `goro` | fly; move through the air | No documented derivation | no_documented_derivation |
| `banuwa` | wing membrane | banu=wing | semantic_anchors_only |
| `qaroshishimarë` | Qaroshi dictionary | qaroshi + shimarë | preexisting_compoundlike_headword |
| `pizikha` | informed consent | korage (informed) + maho (consent) → **koragemaho** | primary_gloss_candidate |

**Caution:** An English label like “fire” can be a secondary gloss of a source word meaning “flame,” and those are not guaranteed interchangeable. The default rank favors **primary** component senses and the full CSV flags secondary-sense possibilities. Parenthetical sense restrictions still need review.

## Productivity without a brand-new word for everything

1. **Core words are conventional.** A learner must remember that `goro` means fly. Grammar can then generate `goro-te` (flew), `goro-ki` (able to fly), `goro-ho` (permitted to fly). It cannot infer the root meaning from phonemes.
2. **Original compounds are already productive.** Learn the component roots and you can understand the structure of 13,379 existing modifier–head compounds. The baseline 16.0 study maps 1,820 ultimate base roots used inside them. The exact specialized meaning is not always a simple sum.
3. **Some independent technical headwords can be paraphrased.** `banuaro` is the established word for wing joint. The proposed spelling `banuqamago` transparently uses `banu` wing + `qamago` joint, but is **not yet canonical** and might be more cumbersome in ordinary speech.
4. **Do not invent hidden syllable meanings.** `banuwa` means wing membrane, but that does not automatically license interpreting `-wa` as a suffix meaning membrane. In the real grammar, `-wa` is a comitative case suffix when used with a hyphen.
5. **Avoid the giant-word trap.** Long compounds should be shown with visible component boundaries in teaching tools. If a shorter canonical headword is commonly used, teach it alongside its transparent explanation rather than forcibly replacing it.

## Which *new concepts* would reduce memorization?

Across the English glosses, **2,925 lexical component gaps** were identified; **176** affect at least three headwords. These are *missing exact English gloss anchors*, not proof that Qaroshi lacks an equivalent synonym.

| Missing English concept | Role | Potential headwords helped |
|---|---|---:|
| sexual | missing modifier | 23 |
| call | missing noun head | 16 |
| self | missing modifier | 16 |
| cycle | missing noun head | 10 |
| aid | missing noun head | 9 |
| card | missing noun head | 8 |
| bias | missing noun head | 7 |
| clearance | missing noun head | 7 |
| note | missing noun head | 7 |
| signature | missing noun head | 7 |
| allocation | missing noun head | 6 |
| approval | missing noun head | 6 |
| attempt | missing noun head | 6 |
| crossing | missing noun head | 6 |
| greeting | missing noun head | 6 |
| marker | missing noun head | 6 |
| stain | missing noun head | 6 |
| adjustment | missing noun head | 5 |
| break | missing noun head | 5 |
| computing | missing noun head | 5 |

For instance, the exact root concept **membrane** is missing in the audit and affects `banuwa` (wing membrane), `qapewa` (eardrum membrane), `wëroba` (waterproof membrane) and `zeyedo` (cell membrane). Rather than creating four unrelated words, reviewers could identify an existing equivalent or propose **one reusable word for membrane**. No new phonological root was automatically coined here.

## Ambiguous candidate collisions

**4** candidate spellings would map to **9** distinct canonical targets. This includes cases where a broad word would conceal important distinctions (for example different senses of informed consent). See `data/v16_1/proposal_collision_review.csv`. These aliases must remain unapproved until distinctions are tested.

## Adoption protocol

1. Start with the exact canonical entry, its historical user-facing gloss, and its independent/contextual evidence.
2. Try a licensed modifier–head composition using existing primary-sense roots. Compare at least two alternative component choices when multiple senses are available.
3. Verify that the component spelling does not collide with an established word or another proposed sense; check pronunciation and native glyph segmentation.
4. Show the proposed spelling in at least three independently written Qaroshi sentences with distinct contexts, formal vs conversational usage, and faithful English back-translations.
5. Have an editor decide whether the compound is a paraphrase, an approved synonym, or only an explanation. Document reviewer and rationale; do not infer acceptance from automated tests.
6. Preserve the original canonical spelling as an alias whenever a new formal standard is approved; publish a versioned migration and regression tests.

## Why no sweeping mass rename?

Because most headwords are not fully predictable and because existing short forms may be more useful than an extremely long transparent technical form. A language should be learnable *and* practical. Automatically turning thousands of dictionary items into unreviewed compounds would replace one kind of arbitrariness with another.

## Included machine-readable materials

- `headword_learnability_audit_16525.csv`: every headword, classification, evidence, top candidate and anchors.
- `strict_modifier_head_candidates.csv`: every full exact-split candidate (multiple per headword), with dictionary components.
- `headword_learning_priority_16525.csv`: all headwords ranked by usage/reference evidence and compound reuse.
- `prioritized_core_1200.csv`: suggested first 1,200 supported base words for study.
- `root_gap_priorities.csv`: missing English concept anchors ranked by headword reuse, without new Qaroshi coinages.
- `proposal_collision_review.csv`: candidate form conflicts across canonical meanings.
- `Qaroshi_16_1_Root_Reform_Studio.html`: offline learning, searching and review decisions.

## Claims we do NOT make

This release does not attest speaker consensus, a new etymology, fluent speaker sentences, new grammatical suffixes, ratified synonymy, or zero-knowledge inference for all 30,000 dictionary forms. The original 30,000-entry dictionary, 90 grammar chapters, 16 written resonance markers and 26 glyphs remain unchanged.