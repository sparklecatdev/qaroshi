# Qaroshi 16.2: Root Standardization & Editorial Learnability

**Release category:** Compatible editorial-development and review tooling, *not an approved standards revision*.

## The learner’s central problem

A dictionary with 30,000 words feels much larger than it needs to. Existing grammar correctly predicts inflections (e.g., `goro-te` past, `goro-ki` ability, `goro-ho` permission), and the 13,379 documented canonical compounds can often be understood by learning component roots. But 16,525 headwords lack the same official internal derivation. A proposed compound is useful only if its components have the **right senses**, its length is practical, and its meaning would be understood without an English-gloss cheat sheet.

**What we did not do:** Rename or replace a single canonical entry, claim any new word has been speaker-attested, or silently approve invented roots.

## Screening totals

| Category | Records |
|---|---:|
| Pre-existing 16.1 proposed component pairs screened | 3,817 |
| Individually editorially inspected | 65 |
| Editorial trial for further contextual testing | 44 |
| Editorial hold for ambiguity | 9 |
| Editorial rejection of misleading source senses | 12 |
| Machine-only shortlist, **not individually reviewed** | 1,963 |
| Other unreviewed items deferred | 1,789 |
| Narrow proposed root dossiers (all noncanonical) | 8 |
| Reuse-first decisions | 8 |
| Hypothetical new-root compounds for review | 26 |
| Grammar / meaning learning contrasts | 16 |
| Approved new canonical words | **0** |

The machine shortlist is intentionally NOT called a list of valid new words. The ranking can prioritize review, but it does not establish conventional usage.

## Examples from individual editorial judgments

| Existing standard | Existing meaning | Optional candidate | Editorial outcome | Why |
|---|---|---|---|---|
| `banuaro` | wing joint | `banuqamago` | trial | Wing + joint has literal compositional content; confirm the compound denotes the anatomical joint and not an artificial connector. |
| `khezhëpe` | sky map | `wenatëkaro` | trial | Sky + map is straightforward; scope of celestial chart remains to review. |
| `ngodudi` | tool bag | `palorëmara` | trial | Tool + bag is a literal carrying container; broad everyday use is plausible. |
| `lamiti` | dry throat | `dërawagëro` | trial | Dry + throat is a straightforward bodily state; test the ordinary collocation. |
| `wazola` | conversation partner | `shiraromëra` | trial | Conversation + partner is literal and useful in dialogue. |
| `nguzora` | chosen family bond | `runatëra` | trial | Chosen family + bond gives the expected general relationship; does not replace every sense of bond. |
| `zadonë` | dawn song | `lupëtashira` | trial | Dawn + song is a transparent poetic compound; do not equate it with a standardized dawn ritual. |
| `sakazo` | consent withdrawal | `mahosetëmo` | trial | Consent + withdrawal describes revocation, but may not specify legal or temporal effect. |
| `pizikha` | informed consent | `koragemaho` | hold | One form is proposed for multiple domain-specific informed-consent terms; preserve domain distinctions. |
| `këngopu` | informed consent (intimacy) | `koragemaho` | hold | Shared proposed spelling conflates distinct intimacy and research consent contexts. |
| `ngizhobi` | informed consent (research) | `koragemaho` | hold | Shared proposed spelling conflates distinct research and intimate-consent contexts. |
| `giduno` | face mask (clothes) | `meridesido` | reject | The component mask is a theatrical mask, not necessarily a cloth/medical face covering. |
| `nëqido` | mixing bowl | `debëgogëla` | reject | The component for mixing is sound mixing, not combining ingredients in a bowl. |
| `rawaro` | tail tip | `rasosebesa` | reject | The component for tip means gratuity, not the anatomical end of a tail. |
| `zhuzozha` | water meter | `kimaderalo` | reject | Musical meter cannot correctly substitute for water measuring meter. |
| `ngukhëgo` | wing grooming | `banugopawë` | reject | The available grooming headword has a harmful-abuse sense, not grooming wing feathers. |
| `ngusuqo` | tail grooming | `rasogopawë` | reject | The available grooming headword has a harmful-abuse sense, not grooming a tail. |
| `ngalerazi` | low bandwidth | `noakhuruda` | reject | Low bandwidth is a communications-capacity concept, not physical shortness; the selected adjective would mislead. |
| `ngolutuli` | low voltage | `noasuhoha` | reject | Low voltage is an electrical-potential concept, not physical shortness; the selected adjective would mislead. |
| `zudëshi` | neutral language | `yugiwëshi` | reject | Neutral + voice is not the same as neutral language; generic language and voice need distinction. |

**The important failures:** “meter” for music is not a water measuring meter; “tip” as a gratuity is not an animal-tail tip; “grooming” used for abuse cannot be presumed to mean ordinary feather or tail care. Such expressions are clearly rejected in the trial register. Similar parenthetical domain senses across the other candidates remain under manual review.

## Why only 65 individual semantic judgments?

An explicit note was written for each of these forms with an independent testable boundary. Another 1,963 forms pass a cheap gloss/length/component heuristic, but automatically labeling those as “approved natural Qaroshi” would repeat the very error this revision is designed to fix.

## Eight minimal missing-root dossiers

The draft *root spellings* are invented. They are not historical etymologies, canonical lexemes, or guaranteed learnable words. Productive payoff must justify any extra memorization burden.

| Concept | Trial form | Citation IPA (machine generated) | Status | Narrow definition |
|---|---|---|---|---|
| generic physical credential card | `mashëwo` | `/ma.ˈʃə.wo/` | new_root_candidate | Flat physical credential or payment token, not a graphics circuit board |
| personal handwritten signature | `tëwaya` | `/tə.ˈwa.ja/` | new_root_candidate | Personal handwritten/marked assent or identity sign, not a cryptographic signature |
| discourse context | `leshëro` | `/le.ˈʃə.ɾo/` | new_root_candidate | Background information required to interpret an utterance, not physical setting |
| statistical bias | `bëgawiro` | `/bə.ɡa.ˈwi.ɾo/` | new_root_candidate | Systematic skew affecting an inference or estimator, not a mere preference |
| written annotation note | `shinëmora` | `/ʃi.nə.ˈmo.ɾa/` | new_root_candidate | Short written annotation attached to a source, not a musical pitch |
| numeric threshold | `gakënu` | `/ɡa.ˈkə.nu/` | new_root_candidate | Numerical cutoff or decision boundary, not a physical doorway sill |
| formal public notice | `pulëma` | `/pu.ˈlə.ma/` | new_root_candidate | Formal written notice or announcement intended for recipients |
| recurrent cycle noun | `wëdaro` | `/wə.ˈda.ɾo/` | defer_coinage_due_existing_verb | Repeating sequence/process taken as a noun, distinguished from the documented verb rekesi |

### Reuse existing structure first

- `rekesi` is already a canonical **verb** meaning cycle. A noun for recurring cycles requires POS and derivation review; `rekesi-rëma` literally indicates a cycling *event*, not automatically every technical cycle.
- `dëmi` means help/assist and the existing instrument suffix `-këlë` may support a helping device. Do not promote that combination to a standardized noun without testing its meaning.
- The reflexive suffix `-ne` already helps with self-directed verbal actions. It does not mean every English word containing “self” should be turned into the same pseudo-root.
- `ha` is an existing hello/greeting interjection; `maho` already denotes consent; `mëna` means fact/established information. Reuse these when their recorded meaning genuinely fits.
- “Call” has human telephone/contact and animal vocalization senses. One new universal translation would conflate them; it is deliberately not coined here.

The proposed generic card root is restricted to physical identity/payment tokens, excluding computer memory cards. The proposed signature root is for handwritten personal marks, excluding musical time signatures and cryptographic signatures. The proposed cycle noun root is **deferred** because the canonical verb and derivational rules need review first.

## Semantic review procedure

1. Compare the English source meaning with the **entire primary gloss of both component roots**, not merely overlapping English letters.
2. Check polysemy, technical qualifiers, grammatical POS, and word-formation order.
3. Reject misleading meanings even when the spelling concatenates perfectly.
4. Test the candidate in at least three **independently written** Qaroshi contexts and request an unaided interpretation from another person. Those human observations do not exist yet.
5. Compare the time, ambiguity, and memory cost of the proposed compound with the existing short word. A longer transparent expression can be useful as an explanation without replacing the word used in ordinary speech.
6. Record the review outcome and supporting contexts; only then consider an optional glossary note, accepted parallel expression, or formal lexical change.

## Reproducibility and compatibility

Run from the extracted `Qaroshi/` directory:

```bash
python tools/v16_2/build_reform.py
python tools/v16_2/build_pronunciation.py
python tools/v16_2/build_studio.py
python -m unittest discover -s tests -q
```

The offline Studio displays **30,000 canonical dictionary entries** and the complete 3,817-variant review board. User notes are stored locally and export/import as JSON. No external API is required.

**Limitations:** The 16.1 generated source alternatives are hypotheses. Manual editorial screening by one author is not an empirical speaker study. No standard forms were altered. A word cannot be inferred merely from its letters if it is a genuine independent root.