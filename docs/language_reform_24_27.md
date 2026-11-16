# Qaroshi Linguistic Amendments 24–27

**Status:** new normative **supplement** to the frozen 7.0 grammar, adopted with preservation of established spellings and historical texts. The original `docs/grammar.md` remains byte-for-byte frozen because its hash is a historical source baseline. Where it describes a legacy passive agent, this supplement establishes the new preferred form without deleting the old one. **Not** new natural-language speaker evidence, dialect norms, or a replacement for the 90-chapter grammar.

## 24. Explicit passive agency (substantive grammatical addition)

The established instrumental case `-shi` was used both for a tool and as a passive actor. This is a structural ambiguity with real translation consequences. The revision establishes one **new productive bound case**: `-za` = **agent of an overt passive (`-li`)**. Its phonological spelling is `z` + `a`, both already part of the native alphabet. It occupies the **same case slot** as `-m`, `-tu`, `-shi`, etc. It cannot stack with another case, cannot stand on a finite verb, and cannot mark the active subject. The finite predicate must be marked passive (`-li` before tense/aspect/mood endings).

| Qaroshi | Interpretation | Status |
|---|---|---|
| `sen mi naro-m daru-te.` | I protected the home. | Existing active construction |
| `sen naro daru-li-te.` | The home was protected; actor not specified. | Existing passive |
| `sen naro mara-za daru-li-te.` | The home was protected **by a friend**. | **New preferred explicit agent** |
| `sen naro banu-shi daru-li-te.` | The home was protected **using wings**; agent unspecified. | Instrument, not passive actor |
| `sen naro mara-shi daru-li-te.` | Historically: protected by a friend; could also be read as means. | Legacy, allowed with review warning |
| `sen mi mara-za daru-te.` | Incorrect: active predicate with passive-agent case. | Unlicensed |
| `sen naro mara-za-shi daru-li-te.` | Incorrect: two competing cases on one noun. | Unlicensed |

**Scope restrictions:** one agent `-za` per elementary passive clause; additional human participants must have other syntactic roles. A passive cannot also carry a direct object merely to re-add its demoted patient. In multi-clause sentences the case belongs to the clause containing its own passive verb; a flat lexical scanner cannot infer all clause boundaries. Existing 7.0 writing and controlled corpora are preserved. `-shi` is not deleted or globally reinterpreted: legacy uses continue to be readable, and clear instrumental meanings stay unchanged.

## 25. Semantic and argument-structure repair (normative lexical refinements)

We are **not** changing the written forms or stable dictionary IDs of 30,000 entries. We are clarifying what frequent **existing words actually mean**, which is a real change to their lexical licensing conditions.

- **22 detailed sense additions** in `data/semantics/curated_senses.json` distinguish old forms with exclusions. Examples: `nashi` (deep cherishing) does not encode `mali` (romance); `lani` is family-style care, not attraction; `tika` (see) does not entail `sëmi` (know), and `shëliro` (read) does not entail comprehension.
- **25 checked predicate frames** in `data/semantics/valency_frames.json` now name required and optional roles, rejected argument inferences, and passive-agent constraints. `pëli` takes a theme `-m` and recipient `-tu`; `gura` chooses a goal `-gu`, source `-de` or location `-lo`, not an invented direct object. `këmë` (drink) ordinarily takes liquid, `shëma` (eat) food. Stance particles and evidentials never change these argument slots.
- **65 individual proposed compound repairs** are preserved with explicit decisions in `data/semantics/lexical_migration_decisions_24_27.csv`: 44 *trial only*, 9 *hold*, 12 *rejected*. There are **zero adopted headword replacements** in this update. Rejected examples are not silently restored as approved terms. In particular, `noa` “low” cannot automatically mean low visual acuity or electrical voltage, and “tip” as a gratuity cannot mean an anatomical tail tip.

Every later lexical reform must maintain an ID migration table, an old/new spelling conflict analysis and reference corpus compatibility. Mass-renaming opaque terms because a proposed compound *looks* compositional would damage predictability rather than improve it.

## 26. Negation, scope and casual discourse (normative clarification)

- `nu` directly precedes and negates the finite predicate. `sen mi kima-m nu këmë.` = I do not drink water; this does not imply I drink another liquid.
- `sen ngënao qaro nu goro.` asserts each Nardoragon does not fly (none fly), **not** “not all fly.” `sen nura goro.` uses the negative subject *nobody* without redundant `nu`. To express “not everyone,” make exceptions or contrast explicit in a separate complete marked clause rather than invent a moveable logical negator.
- A complete written independent clause **still starts with one of the 16 resonance markers**. A single-word `shë` (“yes”) or `nu` (“no”) may be used as a contextual short **answer fragment** when the previous question makes it recoverable. Bare inflected finite clauses do not become legitimate unmarked sentences just because the speaker is being casual.
- Contextual omission must not erase participants where the referent is contested or consent relevant. Questions, requests and warm stances **do not count as consent**. An unanswered question should never be translated as an affirmative.

## 27. Morphology and phonotactic consistency (normative clarification)

- Established compounds retain **their recorded spellings and component semantics**. Modifier precedes head when an accepted compound uses that transparent structure. String concatenation of two dictionary entries is a *hypothesis*, not an automatic new word.
- The four digraphs `sh`, `zh`, `kh`, `ng` remain indivisible native letters in the established analysis; the alphabet retains **26 graphemes**. Hyphens/centered dots may show morphological boundaries pedagogically but do not change official headwords.
- The normal stress is **penultimate**; ordinary boundary vowel coalescence in rapid speech is optional phonetic realization, **not** license for changed canonical orthography or an added vowel phoneme. A compound with ambiguous graphemic segmentation requires explicit lexical analysis, not invented pronunciation rules.
- Existing 13,379 documented canonical compounds remain unchanged. The 3,817 screened alternatives are still proposals; their component senses must match the intended meaning before any future adoption.

## Compatibility and effective scope

Preserved: all 30,000 dictionary IDs, original English glosses, 4,383 canonical bilingual lines, 90 chapter numbers, the 16 resonance particles, 26 glyph images, and previous released app/tool artifacts. Updated: preferred passive-agent case `-za`, 22 semantic sense records, 25 refined verb frames, the **additive normative grammar supplement** and compatible new validator. The frozen original grammar and original v14 validator remain unchanged for source preservation. Older passages with agentive `-shi` remain *accepted legacy*. This avoids invalidating earlier narrative texts while making future authors less likely to confuse an actor with an instrument.

These changes are authored language-standard decisions, **not** independently observed speaker use. The conservative validator handles a simple independent clause and reports unknown multi-clause scope as requiring review. It does not certify idiomatic fluency.
