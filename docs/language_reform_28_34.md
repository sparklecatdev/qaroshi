# Qaroshi 28–34 · Semantic, Argument, Logic, Discourse and Word-Formation Standard

**Status:** an adopted, **additive normative supplement** to the frozen Standard 7.0 grammar and the adopted 24–27 amendment. Where they conflict, this supplement controls new 28–34 writing; historical 7.0 and 24–27 texts retain their original interpretation. **This is a design decision for a constructed language, not evidence of naturally occurring speaker usage.**

## Executive rules

1. **Keep the 30,000 legacy lexical spellings and IDs**. Introduce exactly one new function word in the *post-7.0 overlay*: `nëgëra`, “not every; not all.” The effective 28–34 inventory is therefore **30,001**, while the frozen `data/lexicon.csv` remains **30,000** for compatibility and reproducibility.
2. Keep **one sentence-initial resonance** in each complete independent written sentence. Ellipsis of recoverable constituents and bare one-word answers may remain fragments, not arbitrarily unmarked complete clauses.
3. A claim about an argument's role requires an individually reviewed verb sense or a precisely source-licensed exemplar. A single canonical example does not automatically license other cases, passives or causatives; 267 verbs remain provisionally indexed.
4. **`nëgëra NP P` means at least one relevant member of NP does *not* satisfy P**. It does not entail that anyone satisfies P. Keep `ngënao NP nu P` as *none P*. Do not replace “not all” with “none.”
5. Compounds and figurative expressions have individual lexical and contextual identities. Word adjacency, a shared English gloss, a low ambiguity score or a fanciful metaphor does not automatically generate a new official dictionary entry.
6. Technical/legal/high-stakes interpretation favors overt participants, quantifier domains, explicitly identified exceptions, narrow senses, and a non-metaphorical paraphrase.

## 28 · Core semantics and lexical precision

**800 existing dictionary entries** are now accessible in a stable, source-linked semantic priority index (`data/v28_34/core_semantic_index_800.csv`). Selection begins with the older 48 curated sense records and 25 manually checked verb frames, includes 120 learner-core roots and prioritizes actual *controlled* reference occurrences. Each record stores the original stable ID, POS, glossary meaning, source sentence IDs, and a provenance label. These are **not 800 individually approved new definitions**; most records are indexing links to existing senses. Their English glosses cannot be substituted blindly for unrelated English homonyms.

`data/v28_34/meaning_boundaries.csv` adds 30 explicitly authored semantic contrasts. They are meaning constraints, not extra lexical headwords. Notable obligatory distinctions include:

| Qaroshi forms | Difference | Mistake to avoid |
| --- | --- | --- |
| `nashi` / `mali` / `lani` | cherish / romantic love / family-type care | warmth alone does not assert romance |
| `tika` / `sëmi` | physically perceive / know | seeing is not understanding or knowing |
| `shëliro` / `zhëmi` | read / understand | reading does not entail comprehension |
| `goro` / `gura` | flying / traveling | movement does not entail mode of travel |
| `nëru` / `nëra` | rest / remain | remaining somewhere does not entail resting |
| `pëli` / `hari` | give/transfer / possess | recipient and possessor are different roles |
| `këmë` / `shëma` | drink liquid / eat food | selectional constraints matter |
| `si` / `hu` / `ye` | witnessed / reported / inferred | evidence must not be upgraded without support |
| `naru` / `muru` | inclusive we / exclusive we | the addressee's membership matters |

### Sense policy

Do not synonymize words because of overlapping English glosses. Do not import a broad English metaphor, technical sense, romantic implication or legal meaning unless a Qaroshi sense record explicitly licenses it. If an old lexical sense is actually changed, preserve the original form in an editioned migration table; *never* repurpose it silently. The existing **65 individually reviewed alternative compounds** remain 44 trials, nine holds and 12 rejections; none were adopted by this edition.

## 29 · Verb meaning and valency

A verb entry now has a distinct *frame status* and may state a required agent/experiencer, a patient/theme marked `-m`, a recipient `-tu`, a source `-de`, a goal `-gu`, a locative `-lo`, a comitative `-wa`, an instrument `-shi`, or an explicitly licensed passive actor `-za` (24–27). The underlying 7.0 suffix order remains unchanged.

**Authoritative frames:** the 25 previously manually specified frames in `data/semantics/valency_frames.json`. The supplement does not broaden their argument sets. For example:

- `goro`: intransitive flyer. No extra `-m` patient merely because English sometimes says “fly a plane.” That reading needs a separate, explicitly reviewed lexical sense.
- `gura`: traveler plus licensed goal `-gu`, source `-de`, location `-lo`; don't invent a destination direct object.
- `pëli`: transfer verb with a direct-object theme `-m` and recipient `-tu`. Giving is not the same as possessing (`hari`).
- `këmë`: consumption of liquid; `shëma`: consumption of food. Coercion or metaphor cannot override selection rules silently.
- A transitive passive may specify the demoted agent with `-za` when its frame licenses passive. Instrumental `-shi` does not replace it in precision writing, while historical passive agentive `-shi` remains readable.

**Source-linked analysis queue:** `data/v28_34/verb_frame_inventory_400.csv` contains 400 existing verbs. The 25 full reviewed frames are marked `normative_manual_frame_24_27`. An additional **108 individually selected source exemplars** are marked `source_exemplar_limited_license`: in each, a complete documented sentence unambiguously uses a named existing noun object in `-m` with that verb, and that *exact object-bearing construction* is licensed. This does **not** license all possible patient classes, passives or causatives. The remaining **267** entries are corpus-indexed only, tagged `corpus_observed_provisional_roles`, with no approved required/optional roles. That observation is neither all required roles nor all allowed roles. A *generalized* frame becomes authoritative **only after individual selectional, argument and voice review**; machine extraction must not write normative fields automatically.

### Productive argument alterations

- `V-ru` causes an event. For an originally intransitive verb, the caused participant becomes the lower-clause agent/patient; for a transitive root, do not silently drop either participant. Explicitly state or review argument licensing when the simple 7.0 construction cannot disambiguate.
- `V-li` demotes the actor; only **reviewed passivizable senses** may take `-li`. A passive `-za` identifies an actor, not an instrument. Avoid allowing `V-li` for bare weather/activity verbs merely because a suffix is morphologically possible.
- `V-wo` requires a genuinely plural interacting subject; `V-ne` is reflexive. Neither is inferred solely from spelling resemblance.
- One voice suffix occupies one voice slot; no stacking two voice suffixes by concatenation. Ordinary tense, aspect and modality limits stay as defined in chapters 6–7, 27–30 and 74.
- A verb may have multiple individually numbered senses/frames. A lexical gloss such as “break” needs a *causative vs inchoative* choice: the broken subject is not automatically the actor that caused the break. Until explicitly reviewed, give the two propositions as separate clear clauses rather than guessing an unlicensed valency switch.

## 30 · Quantifier logic and scope

The standard retains existing `ngënao` (every), `shërano` (some), `nura` (nobody), `ngëshi` (only), `tëmiri` (even), `bëso` (also), `zhoro` (still), and conditional `shoru` (unless). **Only one additional lexical determiner is adopted:**

> **`nëgëra`** /nə.ˈɡə.ɾa/ (det.) = *not every; not all*. It appears immediately **before** the quantified noun phrase, as with `ngënao`. In a simple positive distributive clause, it asserts a counterexample and presupposes a nonempty contextually selected domain: **∃x∈D ¬P(x)**. It does **not** assert ∃x∈D P(x). Its spelling uses only original native glyphs, and it is not a replacement for an existing lexeme.

| Qaroshi | English | Logical reading | Independent implication |
| --- | --- | --- | --- |
| `sen ngënao qaro goro.` | Every Nardoragon flies | ∀x∈D P(x) | none fail to fly |
| `sen ngënao qaro nu goro.` | No Nardoragon flies | ∀x∈D ¬P(x) | none fly |
| `sen nëgëra qaro goro.` | Not every Nardoragon flies | ∃x∈D ¬P(x) | at least one does not fly; **some may still fly or none may fly** |
| `sen shërano qaro goro.` | Some Nardoragon flies | ∃x∈D P(x) | at least one flies, no upper bound |
| `sen shërano qaro nu goro.` | Some Nardoragon does not fly | ∃x∈D ¬P(x) | equivalent truth condition to `nëgëra` in this restricted context |
| `sen dëna qaro ngëshi haro.` | Only this Nardoragon is well | P(focus), no relevant alternative P | identify the comparison class |
| `sen dëna qaro tëmiri haro.` | Even this Nardoragon is well | P(focus) + unexpectedness | scalar implication is not a separate fact |
| `sen nëgëra qaro haro.` | Not every Nardoragon is well | ∃x∈D ¬well(x) | adjective predicates are licensed too |

**Restrictions:** do not write `nu nëgëra` as a double negation or append simple `nu` after `nëgëra` to mean “not all.” If a scope relation is contested, identify the domain, topic and exceptions explicitly. Bare plural is not collective/distributive by default. The existing `qësho` / `rëshu` / `nëmi` before a numeral remain minimum/maximum/exact quantity. Numerals still follow nouns; base-six notation must be clarified where needed.

`shoru P, Q` (“unless P, Q”) means ¬P ⇒ Q. **It does not** assert P ⇒ ¬Q; that extra biconditional is an English-to-Qaroshi mistranslation. A focused `ngëshi` follows its constituent, not an arbitrary preceding negator. Do not equate “not only X” with “only not X.”

The restricted rule interpreter `tools/v28_34/reform_core.py` recognizes simple positive and predicate-negated **one-quantifier** subject clauses with a documented verb or adjective. It **abstains on embeddings, multiple quantifiers, competing reference frames and unsupported NP structure**. Its finite model truth tables explicitly differentiate “not all,” “none,” “some,” “only one,” “at least,” “at most” and “exactly.” This is a principled limit, not a false claim to full translation.

## 31 · Conversational grammar

The independent written sentence still starts with **exactly one** of the 16 resonances, including neutral `sen`; neither slang nor chat length automatically licenses a missing resonance. The licensed informal forms are:

- **Recoverable fragments:** a one-word `shë` or `nu` directly answering a salient question, short greetings, labels and interjections may omit full-clause structure. `sen shë.` and `qor nu.` remain complete forms; a fragment is not simply a malformed sentence.
- **Zero subject:** permitted only when the immediately relevant discourse has **one** unambiguous referent. Repeat the noun, name or relevant pronoun where two people could be `sa` or where consent/agency is material.
- **Repair of facts:** `dënaro` introduces the speaker’s corrected proposition; `qëlo` repairs a mishearing. Quoted mistakes remain distinguishable from corrected content.
- **Discourse mode:** `qëhano` is verbatim citation, `wëlëmi` paraphrase; do not stack both over one span. An evidential `hu` for reporting cannot be upgraded to directly witnessed `si` without support.
- **Agreement and refusal:** resonance is not consent. An unanswered request, a warm tone, or an invitation never means yes. Permission `-ho`, ability `-ki` and obligation `-du` remain separate.
- **Social variation:** `pëla` / `pëlë`, `lan`, `pëshu` and `tëqoro` may reduce pressure; they do not make a compulsory request into a promise. Informal *register* changes what is optional in fragments and word choice, not the phoneme inventory or base grammar.

All 20 authorial, contrastive usage clarifications are encoded in `data/v28_34/conversational_usage_rules.json`. Do not claim an observed youth dialect or independently attested slang without speaker evidence.

## 32 · Productive morphology and sound

The **13,379 canonical compounds** remain unchanged. Concatenation is **not** a generic dictionary-addition operation. For a new candidate to be licensed, it needs: a documented modifier sense, a documented head sense, correct POS/selection, a narrow distinguishable meaning, no collision with an existing spelling, no accidental regrouping into a different `sh`/`zh`/`kh`/`ng` digraph, usable pronunciation and a reviewed source context. Preserve established spelling even if the learner uses a temporary visible boundary to explain it.

The generated `canonical_compound_audit_13379.csv.gz` covers **every existing canonical compound** (spellings, component IDs, component glosses, boundary, structural flags). It found **two** forms in which a component boundary can be parsed as a different native digraph *and* the English component glosses contain a semicolon, plus **3,106** further multigloss semantic-review flags. These are **review priorities**, not proven defects or automatically invalid words. A standard might allow a lexicalized exception even where purely productive concatenation would be ambiguous; record that exception explicitly instead of changing an established word.

The 26 letters, 6 phonemic vowels, original digraph inventory, default penultimate stress and optional rapid-speech vowel coalescence remain. Allophonic expectations do not authorize new canonical spellings. An imported personal name may remain quoted if no approved transliteration conveys the distinction.

## 33 · Idiom, rhetoric and literary style

A **literal collocation** has compositionally predictable meaning; an **editorial literary convention** has a documented nonliteral reading in an identified context; a **fresh metaphor** is a creative interpretation not thereby incorporated into the dictionary. These are different types of evidence.

All **32 existing figurative expressions** are indexed in `data/v28_34/literary_conventions_32.json` with their original words and original meanings, interpretive categories, restrictions and explicit *editorial literary* status. Examples:

- `nëm banu nëra.` literally “The wing rests,” used in the existing reference as a literary image of voluntary restraint; it **does not** turn every statement about resting wings into an idiom.
- `qor zhalo nu zëru.` literally “The fire does not die,” a literary image of persistence, not a guarantee of immortality.
- `wen mi sëra-m tika.` literally “I see the star,” referring to a distant goal in its editorial context; outside it, the literal reading remains possible.

**Irony and humor:** `yëhano` can frame an intentionally rhetorical question and `shëgi` marks contrary expectation, but neither reverses a proposition’s truth automatically. Avoid inventing a generic “sarcasm particle” that cannot be distinguished from evidence or resonance. Humor depends on context; a translator must preserve the literal assertion, state the possible rhetorical implication, and avoid presenting it as a certified cultural saying.

## 34 · Consistency, migration and conformance

**Precedence** (latest for explicitly conflicting matters): 28–34 supplement → 24–27 supplement → frozen 7.0 grammar → earlier reference/archival proposals. New preferred forms are meant for *new* writing; old texts keep their source meaning unless separately corrected. In particular, historical passive-agent `-shi` is readable, while the new explicit passive agent is `-za`.

**Test and editorial review requirements:**

1. Verify all 29 frozen original source SHA-256 values before and after a build; assert 30,000 frozen lexical IDs and 4,383 original sentences unchanged.
2. Verify new spellings are unique against the old lexicon and composed entirely of the original 26 graphemes. A newly adopted overlay word has an editioned ID and phonemic IPA.
3. Check each adopted rule with a positive example, a similar-looking counterexample, and its true scope. Inference and non-entailments are essential test cases.
4. For valency, store an exact corpus source and a review state for every observation. Only individually reviewed generalized roles or the *exact* documented exemplar become normative; no machine-generated blanket rules.
5. All compound migration proposals need old/new ID mapping, component-sense evidence, collision checks, minimally contrasting example sentences, a legacy alias plan and human adjudication.
6. Discourse and idiom claims must distinguish *documented editor-created convention* from independently observed speaker frequencies, regional dialect or traditional culture.
7. The 24–27 passive-agent case, 90 grammar chapters, 16 written resonances, original numeral system and old 30,000-word dictionary stay stable. No unreviewed headword replacement or invented attested speech.

**Machine-readable conformance:** `tools/v28_34/build_release.py` deterministically builds the data overlays and `tools/v28_34/reform_core.py` validates the adopted quantifier in its limited simple-clause scope. `tests/test_v28_34_language.py` exercises the language rules, actual source mappings, formal finite-domain semantics and compatibility. A failed parse in unsupported syntax means **manual review**, not that the language can never express the idea.

**Acceptance boundary:** this is a substantial, working *constructed-language norm and analysis package*. It is **not** a claim that 800 word senses or 400 verb frames were independently reviewed, that a machine has certified idiomaticity, or that natural speakers of Qaroshi were recorded. Those are separate empirical research steps, not something software or mass-generated examples can substitute for.
