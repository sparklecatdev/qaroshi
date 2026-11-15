# Qaroshi Standard Reference 3.0: Advanced Grammar and Discourse

**Scope:** This document extends, rather than replaces, `docs/grammar.md` (Standard Reference 2.0). All 16 mandatory, typed sentence-initial resonance markers, 26 native glyphs, core SOV clause structure, noun cases, and verb suffix ordering remain unchanged. New 3.0 forms are marked **proposed standardization** pending usage review. The examples are controlled illustrative sentences, not independently attested speech.

## 36. The principle of layered meaning

Every independent Qaroshi sentence expresses several separable dimensions:

1. **Resonance**: how the speaker wants the full sentence to be received emotionally and socially (required).
2. **Proposition**: the event, action, state or relationship being asserted, denied, questioned or requested.
3. **Time and viewpoint**: reference time and temporal unfolding, with the existing tense/aspect suffixes and optional preverbal operators.
4. **Information structure**: topic, focus, alternatives and numerical scope.
5. **Provenance**: witnessed, reported, recalled, measured, inferred or sourced from a document.
6. **Confidence**: how sure the speaker is, distinguished from how the proposition was learned.
7. **Speech act**: assertion, question, instruction, request, wish, refusal, quotation or negotiation.

These dimensions are **not interchangeable**. An affectionate `më` sentence is not automatically true; a serious `qor` sentence is not automatically a promise; a high-confidence claim is not necessarily witnessed; a request does not establish consent. For example, `më ti lësha.` and `zha ti lësha!` have identical propositional content but different written resonances.

### One-sentence ordering diagram

```text
RESONANCE
  [one discourse/translation stance]
  [topic]
  SUBJECT  [object-m] [other case phrases] [bound number expressions]
  [preverb aspect/continuation] [nu]
  PREDICATE(-voice-tense-aspect-modal-manner)
  [mirative] [one evidential] [one confidence particle] [he / ya / other act final]
```

This is a template, not a mechanical guarantee that all conceivable word sequences have a valid interpretation. Clause-level subordinate connectors may introduce an additional predicate; each finite predicate keeps its local argument and postpredicate material. The opening resonance governs the entire sentence until the next sentence boundary.

## 37. Temporal overlap, immediate succession, precaution and purpose

The established subordinators `wë` (“if”), `wënu` (counterfactual “if”), `ko` (“so that”), `ro` (“because”), `yaro` (“when”), `tara` (“until”), `dasha` (“even if”) and `shoru` (“unless”) remain unchanged. Edition 3.0 makes more distinctions with additional connectors:

| Connector | Interpretation | What it does **not** imply |
|---|---|---|
| `tëwaro` | while / during the time that | neither event must cause the other |
| `huwë` | immediately after / as soon as | no long interval is assumed |
| `bëna` | as long as / throughout the relevant condition | not identical to one-time hypothetical `wë` |
| `kheso` | in case, as a precaution | anticipated event has not necessarily happened |
| `qësu` | rather than an alternative clause | alternatives need not be mutually impossible |
| `ngësha` | instead of a planned action | the skipped action is not said to occur |
| `tërashi` | as a result of a causal circumstance | no speaker intention or purpose required |
| `dëshu` | even though, contrary to expectation | does not negate the concession's event |
| `zuwë` | so that an unwanted outcome will not occur | not a guarantee of success |
| `hëshu` | whether or not, covering both alternatives | no commitment to which alternative is true |

Examples:

- `sen tëwaro mi nëru, ti shiri.`: “While I rest, you speak.” Two actions overlap; the sentence has **only one** `sen`.
- `sen huwë mi nëru-mo, mi shiri-yu.`: “As soon as I finish resting, I will speak.” Completion is expressed by old suffix `-mo` and future by `-yu`.
- `sen bëna mi haro, mi goro-yu.`: “As long as I am well, I will fly.” Continued condition, not a counterfactual assumption.
- `sen kheso sa goro-yu, mi naro-lo nëra-yu.`: “In case they fly, I will stay at home.” Preparing for an event does not assert it.
- `sen zuwë ti nu zëru, mi ti-m daru-yu.`: “I will protect you so that you do not die.” The negative purpose clause has an ordinary preverbal `nu`.
- `sen hëshu ti goro-yu, mi naro-lo nëra-yu.`: “Whether or not you fly, I will stay at home.” The condition covers both possible outcomes.

### Real vs counterfactual vs optative

`wë` leaves the truth of a condition open. `wënu` signals that the condition is contrary to the speaker's chosen reference world, and `qinë` flags the consequent as counterfactual. Neither should be used merely for a polite ordinary question. `yëmë` continues to express a wish or blessing without imposing an obligation.

## 38. Event phases beyond suffix aspect

The suffix set from edition 2.0 remains **unchanged**: `-se` ongoing, `-mo` completed, `-në` habitual. Edition 3.0 proposes separate **preverbal particles** for finer viewpoint distinctions:

| Particle | Semantic scope | Position |
|---|---|---|
| `wëshi` | imminent, about to happen | before predicate |
| `shëtë` | recently completed / just finished | before predicate, ordinarily with past `-te` |
| `zhoro` | still underway | before predicate, may combine with progressive `-se` |
| `mënoro` | not yet occurred by reference point | directly before `nu` + predicate |
| `nësha` | no longer occurs after earlier positive period | directly before `nu` + predicate |

These particles occupy **one event-phase slot**, so two such particles cannot be stacked on one predicate. They do not introduce a new tense or resonance. The following contrasts are important:

- `sen mi bozaga-m wëshi koniri.`: “I am about to review a threat model.” (Imminence does not promise completion.)
- `sen mi bozaga-m shëtë koniri-te.`: “I just finished reviewing a threat model.” (Recent completion, past reference.)
- `sen mi bozaga-m zhoro koniri-se.`: “I am still reviewing a threat model.” (Continuative event.)
- `sen mi bozaga-m mënoro nu koniri.`: “I have not reviewed the threat model yet.” (Non-occurrence so far, later review is possible.)
- `sen mi bozaga-m nësha nu koniri.`: “I no longer review the threat model.” (Ceased practice, not merely delayed.)

These words do not replace existing temporal adverbs `sëna` (“always/forever”), `nëna` (“now”), or the morphological past and future. Tense and phase together establish temporal perspective.

## 39. Focus scope and quantitative precision

Edition 2.0 has `rëshi` for contrastive focus and `gawo` / `nashu` for “both” and group-level quantification. Edition 3.0 introduces:

- `ngëshi`: “only”; directly follows the **focused constituent**.
- `bëso`: “also”; follows a constituent added to the understood alternatives.
- `tëmiri`: “even”; follows an unexpected member of the comparison set.
- `qësho`: “at least”; comes immediately before a following numeral.
- `rëshu`: “at most”; comes immediately before a following numeral.
- `nëmi`: “exactly”; comes immediately before a following numeral.

**Preserve noun–numeral order.** The ordinary phrase is `qaro po` (“two Nardoragons”), not `po qaro`. With a bound, the form is `qaro-ri qësho po` (“at least two Nardoragons”): noun, optional plural, bound particle, numeral. No new numeral glyphs or numeric bases are introduced.

- `sen dëna qaro ngëshi haro.`: “Only this Nardoragon is well.”
- `sen dëna qaro bëso haro.`: “This Nardoragon is also well.”
- `sen dëna qaro tëmiri haro.`: “Even this Nardoragon is well.”
- `sen qaro-ri qësho po goro.`: “At least two Nardoragons fly.”
- `sen qaro-ri rëshu po goro.`: “At most two Nardoragons fly.”
- `sen qaro-ri nëmi po goro.`: “Exactly two Nardoragons fly.”

A negation such as `nu` interacts with focus. If the intended reading is “it is not the case that **only** X ...”, the speaker should use clear clause segmentation or reword instead of relying on a potentially ambiguous single-sentence order. A translator must preserve the intended alternative set, not guess it.

## 40. Evidence, surprise and confidence are separate

The prior evidentials remain `si` (direct witness), `hu` (reported) and `ye` (inferred), with `lëshu` (customary knowledge). Edition 3.0 proposes more specific sources:

| Particle | Source type | Contrast |
|---|---|---|
| `shëku` | directly remembered experience | retrospective memory rather than ongoing direct perception `si` |
| `wërusha` | calibrated instrument, observation record or computation | measurement rather than naked inference `ye` |
| `rëhu` | written document / archive | narrower than broad reported `hu` |

At most **one evidential** occurs per finite clause. Two independent pieces of evidence should be communicated in two clauses or explicitly described with source nouns, not by piling evidentials onto a single verb.

The **mirative** `yëqo` marks an unexpected discovery and occurs *before* an optional evidential. It does not tell the reader what the source was. `sëki` (“tentatively asserted; low confidence”) and `qëru` (“high confidence, short of certainty”) occur *after* an evidential, at most one per clause. Do not confuse `qëru` with absolute proof or `sëki` with lack of evidence.

Recommended postpredicate order: `PREDICATE — [yëqo] — [one evidential] — [sëki or qëru] — [question/act final]`.

- `sen sa goro-te shëku.` “I remember witnessing that they flew.”
- `sen sa goro-te wërusha.` “Measurements indicate that they flew.”
- `sen sa goro-te rëhu.` “An archival source says they flew.”
- `yë sa goro-te yëqo si.` “Surprisingly, I witnessed them fly.”
- `zher sa goro-te ye sëki.` “They may have flown, but I am not confident.”
- `sen sa goro-te si qëru.` “I witnessed their flight, and I am highly confident.”

A legal or scientific translation must distinguish direct observation, citation of a prior study, an instrument reading, and statistical inference. If a source statement does not warrant the evidential's meaning, choose a broader form or use no evidential.

## 41. Typed discourse stances and conversational repair

A **stance particle** may follow the mandatory resonance and precede the topic or main subject. They are optional, and **not additional resonances**. When several could apply, write separate sentences rather than stacking opaque intentions. Stance is an interpretive cue, not a claim of universal permission.

| Particle | Discourse function |
|---|---|
| `shëmoshi` | an approximate translation is being supplied |
| `hëra` | the speaker is paraphrasing rather than quoting verbatim |
| `rëmëlo` | the speaker claims to represent a group *by agreement* |
| `pënu` | checking permission before approaching sensitive subject |
| `nëto` | gentle refusal without shame or explanation owed |
| `qëlo` | repair of an earlier mishearing |
| `tëshi` | the discussion is shifting to a new topic |
| `yëmiri` | the proposal remains open, not a final agreement |
| `bëshi` | speaker explicitly declines expert authority |
| `shërawono` | acceptance depends on the condition in this sentence |
| `hëwo` | seeks clarification, not agreement/consent |
| `mëri` | opt-in emotional check-in |
| `pëshu` | pressure-free invitation or request; no obligation implied |

Examples:

- `hë hëwo ti haro he?` “Are you well? I am asking for clarification.”
- `më pëshu mi ti-m nashi.` “I cherish you, without demanding reciprocation.”
- `nëm nëto mi nu shiri.` “I prefer not to speak.”
- `sen hëra mi qaroshi-m shiri.` “I am paraphrasing in Qaroshi.”
- `qor rëmëlo naru qaro-ri-m daru-yu.` “By the group's agreement, we will protect the Nardoragons.”

Important ethical distinction: **a resonance cannot override consent or a refusal**. A response using `nëto` does not mean “convince me,” just as `më` does not necessarily imply romance. In interpreting real messages, the explicit semantic content outranks assumptions about speaker intentions.

## 42. Reference, person and shared membership

`mi`, `ti`, `sa`, `naru`, `muru`, `tiri`, and `sari` retain their Reference 1.0/2.0 meanings. The inclusive/exclusive first-person plural contrast is especially important in cross-group cooperation: `naru` includes the addressee and `muru` excludes them. No pronoun marks gender or sexuality. Kinship, chosen family, individual identity, and legal relationship are all lexical matters, not forced pronoun distinctions.

A singular Nardoragon's name does not change the meaning of `sa`; use lexical references to disambiguate multiple participants. Use `-na` for possession, `-tu` for a recipient, and `-wa` for companionship. In sentences such as `më mi ti-wa nëra-yu.`, `ti-wa` says **with you**, not ownership of you. Pronouns in borrowed material should be interpreted in their original context before translation.

## 43. Distinguishing refusals, invitations and commitments

A request normally closes with `ya` and may use polite `pëla`. A question normally closes with `he`. In either case, an emotional or deferential resonance does not create a hidden obligation. A direct statement of a promise should state its action and conditions clearly rather than presuming that `qor` by itself is a contractual commitment. `nëto` can soften a refusal, but the refusal remains valid. `pëshu` explicitly rejects the assumption that a friendly invitation requires reciprocation.

For agreement with limitations, state those limitations using `wë` or `bëna`, optionally beginning with stance `shërawono`. Formal agreements must still identify parties, scope, times, enforcement conditions and whether the commitment is revocable. Literal interpretations matter most for agreements involving resources, bodies, consent, or residence.

## 44. Nardoragon cultural and physical vocabulary

The expanded lexicon makes finer distinctions between *roost*, *nursery*, *clutchmate*, *roostmate*, *flight mentor*, *apprentice*, *shared flight plan*, *safe landing signal*, *molt season*, *assisted first flight*, *communal lookout*, and *protected nesting area*. These are named experiences and practices, not grammatical gender classes. Terms such as *mournful flight* and *hatchling comfort call* can be used literally or as culturally meaningful expressions depending on context.

Qaroshi does not assign moral value to wing length, scale pattern, first-flight age, nesting structure, or other biological variation. Describing ability should distinguish *physical capacity*, *permission*, *safety conditions* and *social custom*: `-ki` means able, `-ho` means permitted, `-du` means required. The terms are not substitutes for one another.

## 45. Contemporary science, computing and AI terminology

Specialized words are recorded under distinct senses even when an English spelling is ambiguous. For example, **privacy** in ethics, **data privacy** in computing, and **privacy policy** as a document are not identical words. Technical concepts added in 3.0 include *prompt injection*, *differential privacy*, *local inference*, *inference latency*, *hardware security keys*, *cryptographic signatures*, *aerodynamics*, *clinical uncertainty*, *causal inference*, *statistical power*, and *stellar parallax*. The dictionary marks their English semantic scopes explicitly.

Reference terms do not automatically denote an exact model/product/brand. Proper names, API tokens, formulas, code, usernames, and unique identifiers can remain quoted foreign strings. No machine tool should automatically replace them by approximate Qaroshi sounds. A formal paper can retain internationally recognized decimal numerals, ISO dates, and scientific notation as *technical symbols* without adding letters to the 26 native-letter inventory.

## 46. Complex written documents

A full sentence starts with exactly one resonance marker, even in text chat, academic writing, captions, subtitles, UI copy or official correspondence. A label without a finite predicate (e.g. "Date", "Table 1", or a two-word heading) is a **fragment** and may omit resonance. Directly quoted **complete Qaroshi sentences** have their own resonance because they are independent utterances. Subordinate clauses introduced by `ko`, `wë`, `ro`, `tëwaro`, etc. inherit the enclosing resonance; do **not** place a fresh resonance at every comma.

One consequence is that strings with foreign material need a tokenizer that distinguishes quoted literal segments from regular Qaroshi sentences. Technical acronyms in a code block are not native 26-glyph Qaroshi lexemes. UTF-8 must be preserved, especially the six-way vowel inventory and the letter `ë`.

## 47. Dictionary statuses and editorial safeguards

The package intentionally distinguishes three strata:

- **1.0 established**: original 853 definitions retained word-for-word.
- **2.0 candidate / standardized**: the 5,942 added candidate lexical items and 24 explicitly standardized grammatical entries from Reference 2.0; no previous headword may be reassigned.
- **3.0 candidate / proposed**: new semantic senses and 40 new syntax/discourse forms. They are published for use and review, not misrepresented as corpus-attested terms.

Each dictionary entry specifies **one principal English sense**, a part of speech, an editorial domain, a version origin, and a review status. English senses can overlap across semantic domains when those are genuinely different contexts (e.g. legal consent versus interpersonal consent). One-to-one English glossing is a pedagogical simplification, not a promise that translation is always reversible. Newly proposed lexemes are assigned stable lockfile spellings, but their semantic and sociolinguistic review remains open.

### Avoid these errors

- Never drop the initial resonance because a statement seems emotionally neutral; use `sen`.
- Never replace a second nested clause with a second opening resonance.
- Never treat `ë` as ornamentation or normalize it to plain `e`.
- Never substitute evidential `si` for the stronger-looking but actually different `wërusha` or `rëhu`.
- Never apply `nu` twice to express “never,” “not yet,” or an `unless` clause.
- Never interpret written `më` as a guarantee of affection being romantic, or written `qor` as automatic legal authority.
- Never assert that 9,000 dictionary records alone imply full parity with languages that have centuries of idiom and millions of naturally occurring utterances.

## 48. Direction for a spoken Qaroshi corpus

A strong next step is collecting community-reviewed utterances in real scenarios: apologies and boundary repair, formal petitions, technical documentation, emergency flight calls, stories and songs, affection across different relationships, and ordinary chores. Track the sentence, resonance, speaker-intended meaning, word segmentation, lexical senses, regional voice style, and reviewer notes. Where several natural phrasings compete, document them instead of silently overwriting one with another. Versioned changes should preserve prior attested usage and make semantic drift visible.

## 49. Productive word formation and derivational boundaries

The 2.0 word-formation system remains valid, including `-mi` agent, `-ma` action noun, `-ra` associated place, `-rë` abstract quality, `-no` group, `-wë` taxonomic subtype, `-këlë` tool, `-rëma` event token, and `-sharo` professional specialist. Edition 3.0 proposes four additional **transparent derivations**:

| Derivation | Root category → result | Compositional meaning | Example |
|---|---|---|---|
| `-dëno` | verb → noun | place or setting of an action | `shiri-dëno`: speaking venue |
| `-nëro` | verb → noun | result of an action | `shiri-nëro`: a speech product |
| `-khëno` | noun → noun | coordinated system of items or people | `mara-khëno`: organized friendship network |
| `-zëma` | verb → noun | trace or evidence that an action happened | `goro-zëma`: a trace of flight |

These are **derivational**, not verb conjugations and not replacements for noun cases. A derived form is built from one recognized root and one documented derivational ending. Its reading is transparently compositional until a distinct conventional sense is recorded and independently reviewed. The software's `derive` command can propose these forms, but mere generation does **not** insert them into the 9,082-entry lemma dictionary.

Rule priority in parsing: look for an **exact dictionary headword first**, then try the known, hyphen-separated teaching morphology, then offer compositional analysis. Do not strip a suffix from a legitimate dictionary root simply because its final letters happen to resemble a derivation. This guards against accidental semantic collisions.

## 50. Versioning, citations and exchange formats

Qaroshi uses NFC-normalized UTF-8 for modern text interchange. The native script still comprises 26 handwritten glyphs, including single letters `sh`, `zh`, `kh` and `ng` in Romanization. The new 3.0 words do not expand the native alphabet. A reference may include Arabic numerals, code identifiers and foreign proper names as technical strings outside ordinary Qaroshi grapheme validation.

Source and lexical edition are not the same as approval. A row tagged `edition=3.0` and `review=candidate` means that the *concept* is documented but the form may receive linguistic feedback. A row tagged `review=proposed` is an explicit grammar proposal. The `source/lexicon_v2_snapshot.csv` and `source/corpus_v2_snapshot.csv` files give an exact reproducibility baseline. A later editor should **never silently modify the first 6,819 dictionary entries or the first 880 corpus rows**. Corrections, deprecations, dialectal alternatives and disputed senses should be versioned and annotated.

A complete translation workflow should record the English source, Qaroshi output, resonance choice and why it was chosen, lexical review status, intentionally preserved loanwords, ambiguous source passages, and an editor or speaker review outcome. This prevents an attractive-looking but semantically unsupported translation from being mistaken for authoritative cultural language use.
