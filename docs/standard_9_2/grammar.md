# Qaroshi Unified Editorial Reference 9.2

**Current single-entry grammar reference for writing and implementation.** This edition consolidates the 90-chapter Standard 8.0 grammatical reference and all subsequently documented language amendments, through Standard 9.1, into one searchable document. All cited source chapters and historical editions remain unchanged. The 9.2 document is the **current editorial interpretation** for new precision-oriented writing. Neither individual lexical senses nor full candidate translations are represented as independently attested by human speakers.

**Adoption boundary:** The 8.0 core grammar and the specifically adopted 8.1 embedded polar rule are the inherited normative baseline. Later 8.4–9.1 constructions are versioned **editorial licenses for exact documented roles and senses**. They are part of this *editorial working reference* but have not been externally verified. A newer editorial license overrides an older narrow *example* only where it explicitly states a bounded replacement. It never automatically widens unrelated verb argument frames, compounds, passives or modalities.

**Navigation:** All 90 complete chapters appear below in their original chapter-number order, followed in the same file by 8.1, 8.4–9.1 amendments. This page, rather than ten separate tabs, is the master reference. For the machine-readable license registry and exceptions, see [amendment registry](../../data/standard_9_2/amendment_registry.json). The unmodified source files are linked at the head of each appendix. Long examples in source appendices retain their historical version; the explicit corrections immediately below govern current 9.2 editorial writing.

## Current high-priority decisions and conflict resolution

| Topic | Current 9.2 editorial interpretation | Non-equivalent or prohibited reading |
| --- | --- | --- |
| Opening resonance | One opening resonance per independent sentence; nested quotations contain their **own** separately marked sentences | Never silently insert a second outer resonance into a subordinate clause |
| Morphology | **ROOT → voice/valency → tense → aspect → modality → tender manner** | `-ki-te`, `-ho-te`, `-du-te` are noncanonical; **`-te-ki`, `-te-ho`, `-te-du`** are allowed when the verb licenses that meaning |
| Predicate negation | `nu` immediately before the lexical predicate; negation of a reporting or knowing **matrix** remains distinct from negation of embedded content | `mi nu shërawëhu` ("I make no claim") is not `mi shërawëhu` ("I claim not-P") |
| Direct and embedded polar | Direct `hë ... he?` (or appropriate opening register), embedded `P he do KNOW/ASK` | Do not use a sentence-final `he?` where an embedded `whether` is intended |
| Quantifier | `nëgëra` has *not all* force; predicate `nu` is a different scope operator. In the restricted two-NP construction surface-first quantifier binds wider. | Neither `not all` nor `not necessarily` means `none` or `all not` |
| Passive, instrument, causative | Passive `-li`; overt passive agent `-za`; actual physical instrument `-shi`. Every alternation requires an **exact verb/sense license** | `-shi` is never the new precise passive agent; a licensed V1 does not license blanket passive or causative |
| Relative reference | `[CLAUSE sha] HEAD` with a known subject or patient gap. Matrix case stays on HEAD. | A nearby NP or sender is not automatically the missing relative argument |
| Report/inference/knowing | Direct witness `si`, source-to-recipient report `P do yano mi-tu shiri-te`, inference `ye`, ignorance `P he do mi nu sëmi` have separate truth conditions. | An unverified report or a conjecture is not narration that P actually happened |
| Time, **not until** | `torëne` negative phase **and a second affirmative later event** for English *P did not happen until Q* when later P is entailed. | A negative interval by itself does not establish actual later P, and no temporal conjunction entails causation |
| Modal logic | Potential `-ki` ≠ permission `-ho` ≠ obligation `-du`. `wë P,Q` does not assert P; `wënu P,Q qinë` keeps unreal antecedent/result separate from actual world. | Ability does not imply permission; obligation does not imply success; counterfactual outcomes are not reported facts |
| Consent | Asking, offered action, explicit `«nu.»`, silent departure, prior grant, and withdrawal are **distinct events**; a later withdrawal cancels the specific earlier grant before the action opportunity. | Silence, ability, permission requests, or past consent do **not** automatically license the action |
| Technical claims | **P reported**, **P possible**, **P independently verified**, **if P then recommendation**, **P alone doesn't prove Q** are distinct speech acts. | A failed network link does not establish cyberattack; an unsigned agreement alone doesn't prove legal invalidity |
| Fiction and metaphor | `gëmano` establishes fictive scope; full direct quotes `toru «sen ...»` preserve quoted resonance. New imagery is editorial creative writing. | Personified trees/roads are not literal agents; a poetic interpretation is not a standard traditional idiom |
| Lexical overlay | Only approved-to-draft, **exact** 8.4–9.1 source/sense additions apply to their defined roles; rejected 9.1 experimental lexemes `not_adopted` must not be used | No new senses inferred merely from English gloss coincidences; canonical 30,001 spelling entries aren't rewritten |

### Eight historical 9.0 consent errors

Previous 9.0 drafts **QS81-0105, -0110, -0115, -0120, -0125, -0135, -0140, -0150** put `-ki` before past `-te`. The 9.1 working view corrected precisely those strings to `-te-ki` and preserved the historical originals in `prior_9_0_candidate`. Never copy `-ki-te` from an archived example as normative 9.2 morphology. [Source decision](../../data/standard_8/consent_morphology_corrections_9_1.json).

### New 9.2 correction: counterfactual consequence marker

The independent structural audit found one inherited 8.3/9.1 sentence, **QS81-0336**, with a proper past counterfactual antecedent but an unmarked result. Its original archival wording was `sen wënu regaro pënaro-m rëgë-te, yarowe wërawë-te.`. The current **9.2 editorial view** is `sen wënu regaro pënaro-m rëgë-te, yarowe wërawë-te qinë.`. This follows Chapter 21's explicit `qinë` result marker and preserves the earlier source string byte-for-byte in the `prior_9_1_editorial_candidate` field. See [versioned repair decision](../../data/standard_9_2/semantic_repairs.json). This is a **structural correction**, not independent attestation of the entire sentence's meaning.

### Scope of claims, what is still missing

The 9.1 stress generator produces **500/500 editorial draft strings** for a fixed original English test. It does **not** prove that 500 meanings are faithfully and idiomatically expressed by unrelated humans, or that arbitrary novel combinations are licensed. The independent 9.2 semantic audit records structure and evidence coverage separately from human semantic equivalence. The independent held-out *software* stress suite tests new lexical-event **pairs**; it is a bounded compositional model, not a general grammar parser, a translator, or a human blind comprehension study. **Number of independently collected human backtranslations: 0.**

## Complete Standard 8.0 grammar: chapters 1–90

The text of the inherited 90 chapters follows intact. Where an old example conflicts with a narrowly adopted later editorial correction, the current-decision table above and the relevant newer amendment govern new editorial writing; historical source remains visible rather than rewritten.

---

# Qaroshi Unified Standard 8.0 · Authoritative Current Grammar

**Language-standard release:** 8.0. This consolidated teaching and normative edition includes the full 90 historical grammar chapters with directly integrated current rulings and a compatible post-7.0 lexical overlay. Its older source is frozen at `docs/grammar.md` for historical reproducibility. The current dictionary is `data/standard_8/dictionary_enriched_30001.csv.gz`; a base-schema compatibility export is `data/standard_8/dictionary_30001.csv.gz`.

**Precedence:** Standard 8.0 chapter rulings govern new use; for unaffected constructions the 7.0 chapter text remains in force. 24–27 supplied explicit passive agency `-za`; 28–34 supplied `nëgëra` and scope distinctions. Legacy documents remain interpretable in their contemporary editions. No new speaker dialect or real-world attestation is claimed.

**What this edition does not claim:** 400 complete generalized verb paradigms, all 3,108 ambiguous compounds individually resolved, native speaker pronunciation evidence, or completed independent comprehension experiments. Every verb and compound entry has a recorded status; do not promote provisional evidence to canonical grammar by inference.

**Jump to the chapters:** [Case/voice](#7-voice-and-valency) · [Quantification](#22-quantifiers-distributivity-and-scope) · [Argument frames](#74-verb-frames-and-participant-roles) · [Negation](#76-negation-and-focus-scope) · [Connected speech](#86-connected-speech-and-phrasal-stress) · [Polysemy](#88-polysemy-senses-and-valency).

---

## Historical 7.0 grammar, consolidated with later amendments

**Current unified normative grammar: Standard 8.0 (2026)**

**90 consolidated chapters · 26 native letters · 16 mandatory written resonance markers · 30,001 editioned lexemes**

This is one continuous grammar reference. Chapter numbers are stable for wiki linking.

## 1. Writing and sound

Qaroshi has 26 distinct written letters: **k, a, w, t, r, q, o, d, sh, z, u, ë, i, g, kh, zh, e, ng, h, b, p, m, s, n, y, l**. This is their glyph order on the original letter chart. The standard Romanization uses two characters for **sh, zh, kh, ng**, but each one represents a *single native glyph*. The vowels are **a /a/, e /e/, i /i/, o /o/, u /u/, ë /ə/**. The six vowel qualities are not interchangeable: `mara` and `mëra` are different words.

**Other notable sounds:** `q` is the back-of-mouth /q/; `kh` is /x/; `sh` is /ʃ/; `zh` is /ʒ/; `ng` is /ŋ/; `y` is /j/; `r` is /ɾ/ in broad IPA (a tap; a deliberate roll [r] is also possible). Most consonants sound as they do in a broad, careful Latin transcription. Stress normally falls on the penultimate syllable: **qa-RO-shi**, **NA-ro**, **LË-sha**. The demonstrative `dëna` is **DË-na**.

Ordinary syllables have shape **(C)(r/l/w/y)V(C)**. The common final consonants are `m, n, ng, r, l`; short grammatical particles, expressive words, and certain compounds allow additional final consonants (such as the register `rak`). In rapid speaking, identical vowels at a word boundary may coalesce, but written forms remain unchanged. No accent mark is used to indicate stress: the diaeresis in `ë` marks a *different vowel*.

**Native writing:** left-to-right, top-to-bottom, space between words. Hyphens in reference materials divide grammatical parts: `ti-m`, `goro-te-se`. **They are not separate written glyphs** and can be omitted in fluent text. In ordinary digital Qaroshi, Romanized text and original-glyph text are both acceptable. Native-script lettering follows the one-sound-to-one-glyph principle. Standard punctuation is optional in native script, but helpful in Romanized writing.

## 2. Resonance: obligatory typed register

The first independent word of **every sentence** is its resonance particle. It declares how the utterance should be received emotionally and socially. There are **16 recognized registers**:

| Marker | Register | Typical use |
|---|---|---|
| `më` | Warm Hum | affection, tenderness, reassurance, vulnerability |
| `zha` | Bright Trill | excitement, play, delight, lighthearted teasing |
| `qor` | Deep Resonance | oaths, serious protection, solemn declarations |
| `sen` | Still Voice | ordinary facts, neutral presentation |
| `hë` | Seeking Call | open inquiry, curiosity, sincere questions |
| `lën` | Hidden Hum | bashfulness, confession, shyness |
| `sur` | Falling Song | sadness, loss, mourning |
| `rak` | Rough Growl | anger, defiance, resistance |
| `khar` | Sharp Cry | fear, urgent warning, alarm |
| `yë` | Rising Echo | surprise, sudden discovery, wonder |
| `nëm` | Quiet Breath | calm, relief, peace, contentment |
| `wen` | Distant Call | missing someone, longing, wistfulness |
| `dal` | Firm Pulse | commitment, resolve, persistence |
| `rëm` | High Crest | pride, triumph, celebration |
| `hol` | Open Heart | thanks, appreciation, acknowledgment |
| `zher` | Broken Echo | suspicion, uncertainty, disbelief |

**Resonance is neither tense nor punctuation.** All registers can be used for statements, questions, or requests. For example, `hë ti haro he?` is a curious “Are you okay?”, while `khar ti haro he?` is an alarmed “Are you okay?”. `sen` is mandatory when the intended tone really is neutral.

**Scope:** one marker governs its entire sentence, including subordinate clauses. A second register cannot be added midway through that sentence. Start a new sentence to change register. A separately quoted *complete* sentence retains its own required marker; its marker belongs to the quoted sentence, not the surrounding one.

- `më ti lësha.` — You are cute. (affectionate)
- `zha ti lësha!` — You're cute! (playful)
- `qor mi ti-m daru-yu.` — I will protect you. (solemn)
- `sen qaro-ri goro.` — Nardoragons fly. (neutral)
- `lën mi ti-m nashi.` — I love you deeply. (shy confession)

## 3. Sentence skeleton

A standard independent clause is built in the following order:

**REGISTER — (discourse particle) — (topic) — SUBJECT — (time) — (object) — (other role phrases) — (manner) — (NEGATION) — PREDICATE — (evidence) — (speech-act ending)**.

Qaroshi is **Subject–Object–Verb (SOV)**. Direct objects normally have the ending `-m`, so their grammatical role remains clear even if time and location phrases are moved for emphasis. All ordinary complements precede the final verb. A time phrase can appear early or late before the verb. Particles marked optional above are omitted when unneeded. Subjects may be dropped only when a previous sentence or the situation makes them completely clear.

- `sen mi kima-m këmë.` — I drink water.
- `sen sa yami-lo nëru-te.` — They rested at night.
- `më mi ti-m nashi.` — I cherish you.
- `sen naru qaroshi-m shiri.` — We (including you) speak Qaroshi.

**Adjective and noun predicates do not need “am/is/are” in the present:** `sen ti haro.` = “You are well”; `sen sa mara.` = “They are a friend.” For existence and past/future identity, use `eri` (“exist/be”): `sen sa naro-lo eri-te.` = “They were at home.”

## 4. Noun phrases and number

Nouns have no obligatory article, gender, or class. `qaro` may mean “a Nardoragon,” “the Nardoragon,” or the species generally. Context decides. An overt plural uses `-ri`: `qaro-ri` = Nardoragons; `mara-ri` = friends. Numerals follow nouns: `qaro po` = two Nardoragons, with plural `-ri` optional after an explicit count.

**Adjectives follow their noun.** Numbers follow adjectives when both appear: `qaro zaki po` = two powerful Nardoragons. Demonstratives stand before the noun: `dëna qaro` = this Nardoragon; `tënaro qaro` = that Nardoragon near you; `rënao qaro` = that distant Nardoragon. A possessor comes before its noun: `mi-na naro` = my home.

Noun-building follows this order: **ROOT + (derivational ending) + (endearment) + (plural) + (case) + (topic)**. Thus `mara-lë-ri-m` = dear friends as an object; `qaro-ri-lo` = among/at the Nardoragons; `mara-ri-m-së` = as for the friends (in their role as object).

### Noun endings

| Ending | Name | Meaning | Example |
|---|---|---|---|
| `-ri` | plural | more than one | `mara-ri`, friends |
| `-m` | object | direct object | `ti-m`, you (as object) |
| `-na` | genitive | of / belonging to | `mi-na naro`, my home |
| `-lo` | locative | at / in / on, according to context | `naro-lo`, at home |
| `-gu` | allative | toward / into | `naro-gu`, toward home |
| `-de` | ablative | from / out of | `naro-de`, from home |
| `-wa` | comitative | together with | `mi-wa`, with me |
| `-tu` | dative | to / for a recipient | `mara-tu`, to a friend |
| `-shi` | instrumental | using / by means of | `banu-shi`, using wings |
| `-za` | passive agent | by an explicit actor (requires passive `-li`) | `mara-za`, by a friend |
| `-së` | topic | as for; regarding | `qaro-së`, regarding Nardoragons |
| `-lë` | diminutive | dear / little / affectionate | `mara-lë`, dear friend |

The topic ending is outermost and can follow a case. One noun phrase has **at most one case ending**; for two distinct relations, use two phrases, not a string of competing cases. Possessors marked `-na` precede their possessed noun and are not the same as the subject. `sen mi-na mara kima-m këmë.` = My friend drinks water.

## 5. Pronouns, reference, and possession

| Pronoun | Meaning | Notes |
|---|---|---|
| `mi` | I, me | singular first person |
| `ti` | you | singular, informal or neutral |
| `sa` | they | singular, no grammatical gender |
| `naru` | we | inclusive: I + you (and perhaps others) |
| `muru` | we | exclusive: I + others, *not* you |
| `tiri` | you all | plural second person |
| `sari` | they | plural third person |

Pronouns take ordinary case endings: `mi-na` (my), `ti-m` (you as object), `sari-wa` (with them). There are no gendered pronouns; relationship terms similarly have no automatic gender. To mean “have,” use `hari` with an object: `sen mi mara-m hari.` = I have a friend. To mean “belong to,” use `shënawo` and the dative possessor: `sen dëna shërohë ti-tu shënawo.` = This thing belongs to you.

**Core demonstratives:** `dëna` “this (near me)”; `tënaro` “that (near you)”; `rënao` “that (farther away)”. They may stand alone when the referent is obvious. `shënao` = the same one; `larëno` = a different one.

## 6. Verbs: time, viewpoint, and ability

A Qaroshi verb does not change for person or number. The present/general tense has **no suffix**. Past is `-te`; future is `-yu`. The aspect suffix says how the action unfolds: `-se` progressive (“in progress”), `-mo` completive (“reached its endpoint”), `-në` habitual (“regularly/usually”). Only one of these three aspects is used on the same finite verb.

**Canonical verb ending sequence:** **ROOT + (voice/valency) + (tense) + (aspect) + (modality) + (tender manner)**.

| Ending | Type | Meaning | Example |
|---|---|---|---|
| `-te` | past | action before reference time | `shiri-te`, spoke |
| `-yu` | future | action after reference time | `shiri-yu`, will speak |
| `-se` | progressive | action underway | `shiri-se`, is speaking |
| `-mo` | completive | action completed | `shiri-te-mo`, finished speaking |
| `-në` | habitual | routinely; repeatedly | `goro-në`, routinely flies |
| `-ki` | potential | can; able to | `nëra-ki`, can stay |
| `-ho` | permissive | may; permitted to | `goro-ho`, may fly |
| `-du` | necessity | must; required to | `daru-du`, must protect |
| `-la` | tender manner | gently; with care | `shiri-la`, speak gently |

**Tense and aspect both matter.** `sen sa shiri-te-se.` = They were speaking. `sen sa shiri-yu-se.` = They will be speaking. `sen sa shiri-te-mo.` = They had finished speaking. `sen mi goro-në.` = I fly habitually. `qor mi ti-m daru-yu-du.` = I will have to protect you.

**Modal limits:** only one of `-ki, -ho, -du` appears per verb. To express both ability and obligation, use coordinated or subordinate clauses. **Tender -la** is available after tense/aspect/modality: `më mi ti-m daru-yu-ki-la.` = I will be able to protect you, tenderly. The tender suffix describes the manner or social stance, not romantic attraction.

## 7. Voice and valency

**Standard 8.0 override (adopted):** In finite passive clauses `-za` explicitly marks the demoted actor; `-shi` marks the instrument/means. Legacy passive-actor `-shi` is understood in archived sources but not recommended for new exact writing. A nominal receives at most one case. An active finite verb cannot license an actor in `-za`. See the reviewed voice conditions in Chapter 74.

Verbal derivation changes who does what. It appears **immediately after the root**, before tense and aspect.

| Ending | Function | Interpretation |
|---|---|---|
| `-ru` | causative | cause someone to do the root action |
| `-li` | passive | undergo the action; agent need not be stated |
| `-wo` | reciprocal | do the action to one another (plural subject) |
| `-ne` | reflexive | perform an action on oneself |

Examples: `sen mi qaro-m goro-ru.` = I make the Nardoragon fly. `sen naro daru-li-te.` = The home was protected. `më naru nashi-wo.` = We cherish one another. `tika-li` = “be seen”; `sen sa tika-li-te.` = “They were seen.”

**Voice selection:** use at most one voice/valency suffix on an ordinary finite verb. A passive can omit the agent. In current Standard 8.0, identify the agent of a passive with `-za`: `sen naro mara-za daru-li-te.` = The home was protected by a friend. Older writing may use agentive `-shi` for this role, but that ambiguous reading is legacy-only for new precise usage, where `-shi` marks the physical instrument.

## 8. Negation and requests

Place `nu` **directly before the predicate** (the whole conjugated verb, or the predicate adjective/noun). It negates the following predicate, not the entire preceding noun phrase. `sen mi nu shiri.` = I do not speak. `sen ti nu haro.` = You are not well. **Never** can be expressed either with `zëna` or with `sëna nu` (“always not”); the latter is common in emotionally insistent requests.

Commands and requests end with **`ya`**, after any evidential (though commands seldom need evidence). The addressee is often omitted but can be stated for clarity. `dal naro-gu gura ya!` = Go home! `më pëla mi-wa nëra ya.` = Please stay with me. A negative imperative is `nu` + verb + `ya`: `më pëla nu zëru ya.` = Please don't die.

`pëla` (“please”) is a politeness word, normally after the resonance and before the clause. `lan` can soften a request further when the other person is free to refuse: `më pëla, ti mi-tu shiri lan ya.` = Please speak to me, if you'd like. `ya` and the yes/no-question ending `he` are **not combined in the same clause**.

## 9. Questions

An ordinary yes/no question ends in **`he`**. The resonance still comes first. `hë ti haro he?` = Are you well? `khar ti haro he?` = Are you okay?! (alarm). `sen sa goro-ki he?` = Can they fly? Yes/no answers can be `shë` (yes) or `nu` (no), although replies that are full sentences need a resonance marker of their own.

Question words appear *where their answers would go*, and the clause also ends with `he`:

| Form | Question |
|---|---|
| `meya` | who |
| `khe` | what |
| `lona` | where |
| `yeta` | when |
| `shoro` | why |
| `hara` | how |
| `ruki` | which |
| `zëli` | how much / how many |
| `khema` | what kind |

`hë ti lona-lo nëra he?` = Where do you stay? In conversational Qaroshi, question words that already encode a location do **not** usually require a case suffix: **prefer** `hë ti lona nëra he?` for “Where do you stay?” `hë ti khe-m shëma he?` = What are you eating? `hë ti shoro wori he?` = Why do you wander? `hë dëna khe he?` = What is this?

**Rhetorical questions** may use any register. `zher` highlights doubt, `rak` challenges, and `yë` marks shocked discovery. None of these replaces the terminal `he`.

## 10. Evidence and certainty

Qaroshi distinguishes the source of a claim from how emotionally it is presented. An **optional** evidential follows the verb and precedes `he` if the utterance is a question:

- `si` — speaker directly saw, heard, or otherwise witnessed it.
- `hu` — speaker was told or learned it from a report.
- `ye` — inference, appearance, calculation, or plausible conclusion.

`sen qaro-ri goro-te si.` = Nardoragons flew, I witnessed it. `sen qaro-ri goro-te hu.` = Nardoragons flew, someone told me. `zher qaro-ri goro-te ye.` = It appears Nardoragons flew, but I'm uncertain.

**No evidential** is a neutral assertion with the source unspecified. Evidence particles cannot replace a verb and do not count as resonance markers. Adverbs `sëro` (perhaps), `gara` (exactly), and `ngara` (approximately) can refine certainty or precision.

## 11. Linking ideas and complex sentences

Qaroshi keeps **one opening resonance marker for the complete sentence**, however many clauses it contains. The main verb remains final in its own clause. A subordinate clause introduced by a conjunction can come first or after the main clause as sense demands. In Romanization, commas make clause boundaries visible.

| Connector | Meaning | Typical example |
|---|---|---|
| `ara` | and | joins two clauses or noun phrases |
| `oru` | or | states alternatives |
| `nao` | but | contrast |
| `ro` | because | reason |
| `ko` | so that | purpose |
| `wë` | if | condition |
| `uro` | although | concession |
| `yaro` | when | time overlap |
| `ëna` | before | earlier than event |
| `ana` | after | later than event |
| `do` | that | reported proposition or content clause |

Examples:

- `sen mi shiri ara sa shëliro.` — I speak and they read.
- `më mi ti-m nashi nao mi wërahë nu nëra-ki.` — I cherish you, but I cannot stay nearby.
- `sen mi nëru, ro mi ngëmarëho-m hari.` — I rest because I am exhausted (literally “I have exhaustion”).
- `sen wë kima khararo, mi kima-m nu këmë-yu.` — If the water is dangerous, I will not drink it.
- `dal wë sa goro-yu, mi sa-m tika-yu.` — If they fly, I will see them.
- `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.` — Please never die, so you can stay with me forever.

**Conditionals** use `wë` followed by a regular clause; Qaroshi does not require an additional “then” particle. Hypothetical or contrary-to-fact situations can be marked by `ye` (inferred/non-witnessed) and past-tense morphology, but their exact interpretation comes from context: `sen wë mi goro-ki, mi wena-gu gura-yu ye.` = If I could fly, I would travel into the sky (hypothetically). The `-yu` form here signals a projected consequence, not a guaranteed fact.

**Relative clauses** stand before the noun they describe and finish with the marker `sha`: `[mi tika-te sha] mara` = “the friend whom I saw.” In a whole sentence: `më mi [mi tika-te sha] mara-m nashi.` = I cherish the friend whom I saw. Square brackets are explanation marks only and are not native punctuation. A relative clause inherits the sentence's resonance and does not get an independent marker.

**Content clauses** end in `do`: `sen [sa haro do] mi sëmi.` = I know that they are well. In ordinary speech, the content clause is placed before the matrix subject or its final verb: `sen sa haro do mi sëmi.` The complementizer is a boundary, not a claim of proof.

## 12. Comparing, intensifying, and modifying

Adjectives follow nouns: `qaro zaki` “strong Nardoragon”. Comparative adverbs immediately precede the adjective:

- `mela` + adjective = more [adjective].
- `rela` + adjective = less [adjective].
- `samu` + adjective = most [adjective].
- `rala` + adjective = least [adjective].
- `tëno` introduces the comparison target (“than”).

`sen qaro mela zaki tëno mara.` = A Nardoragon is stronger than a friend. `më ti samu lësha.` = You are the cutest. `sen dëna naro rela ngaroa tëno tënaro naro.` = This home is less heavy than that home.

Degree adverbs follow the resonance and normally appear just before the quality they describe. `luma` reinforces truth (“indeed”), `këra` restricts (“only”), `shërao` adds (“also”), `gara` and `ngara` specify precision or approximation. Repetition of a quality is possible in poetic speech, but normal grammar favors degree adverbs rather than duplication.

## 13. Time, place, and direction

A time noun takes `-lo` when meaning “at/during”: `yami-lo` = at night; `shëraho-lo` = in the morning; `wëro-lo` = during the year. Time adverbs such as `nëna` (now), `tera` (already), `yure` (soon), and `doma` (later) do not need cases.

Directional cases indicate the **relationship** without relying on separate prepositions: `naro-lo` at home, `naro-gu` toward home, `naro-de` from home, `naro-wa` with the home (usually means accompanying the home as a mobile object), and `naro-shi` using the home as an instrument (rare). For a destination plus a source: `sen mi naro-de kimara-gu gura.` = I travel from home toward the waterside refuge.

`wërahë` means nearby; `harurë` means far away. Spatial nouns such as `larë` (above), `noro` (below), `qëra` (front), `gëra` (behind), and `yëra` (middle) can take `-lo`: `naro-na larë-lo` = on top of the home.

## 14. Deriving new words

Productive word-building lets a compact dictionary name new realities. In compounds the **modifier comes first, head last**. The last root usually determines the object's category: `qaro + shi → qaroshi` “Nardoragon-language”; `zhalo + shi → zhaloshi` “fire-voice, powerful roar”; `wena + banu → wenabanu` “sky-wing”; `qaro + shimarë → qaroshimarë` “Nardoragon dictionary,” while **`qaroshishimarë`** specifies “Qaroshi-language dictionary.” Both are compositional, but the second is the explicit language-specific term in the lexicon.

### Productive endings

| Ending | Attached to | Result |
|---|---|---|
| `-mi` | action or role root | agent / person associated: `daru-mi`, protector |
| `-ra` | noun | place or region associated: `naro-ra`, settlement |
| `-ma` | verb | event or action noun: `goro-ma`, flying as an activity |
| `-rë` | adjective | abstract quality noun: `zaki-rë`, strength |
| `-no` | noun | collection or group: `mara-no`, friend-circle |
| `-lë` | noun | dear/little; affectionate form: `qaro-lë`, dear Nardoragon |
| `-ri` | noun | plural |

All endings are made of existing Qaroshi letters. Hyphens separate morphemes only in Romanized teaching text. Speakers can coin a new compound and still be understood, but a compound's specialized dictionary meaning should not be assumed unless usage establishes it. Avoid building ambiguous compounds when an existing independent word is clearer.

## 15. Base-six numbers and measurement

The traditional numeral system is **base six**. Its digit words are `ën` 0, `ka` 1, `po` 2, `dë` 3, `zhu` 4, `rë` 5. The unit **`zhe`** means 6 and **`zhewa`** means 36. Multipliers stand *before* place-value words, and remainder units follow them:

| Qaroshi | Decimal | Base-six notation |
|---|---:|---|
| `ën` | 0 | 0 |
| `ka` | 1 | 1 |
| `po` | 2 | 2 |
| `dë` | 3 | 3 |
| `zhu` | 4 | 4 |
| `rë` | 5 | 5 |
| `zhe` | 6 | 10 |
| `zhe ka` | 7 | 11 |
| `po zhe` | 12 | 20 |
| `po zhe dë` | 15 | 23 |
| `zhu zhe ka` | 25 | 41 |
| `zhewa` | 36 | 100 |
| `zhewa zhe ka` | 43 | 111 |
| `po zhewa dë zhe rë` | 95 | 235 |

The multiplier `ka` (=1) is normally omitted before `zhe` and `zhewa`. Greater powers use repeating compound `zhewa zhe`? **Avoid ambiguity**: for numbers beyond 215, the extended place word **`zhewawa`** means 216 (base-six 1000). Larger powers can be coined by adding `wa` once per further sixfold place step, but in formal technical writing a base-six numeral such as `1023₆` may be clearer. Ordinary writing uses digits when exact large values matter. Numeral expressions come after the noun they count: `qaro dë` = three Nardoragons.

## 16. Politeness, promises, and social meaning

Qaroshi uses resonance instead of obligatory gendered or rank-based honorifics. Social intent is carried by the opening marker, by ordinary words such as `pëla` (please), and by the optional request-softener `lan`. A serious promise normally takes `qor` or `dal`; gratitude often takes `hol`, but these are defaults of **meaning**, not restrictions. Consent should be stated plainly: `maho` is freely given agreement; `noharo` is refusal. A positive resonance never overrides the explicit content of a refusal.

`nashi` denotes durable care or cherishing. It **does not by itself imply romance**. `mali` is romantic love; `lani` is familial or kinship-based love. `mara` is a friend, `mëra` a beloved companion or partner whose relationship type comes from context. These lexical distinctions make affection precise without gender marking.

Examples:

- `më mi ti-m nashi.` — I cherish you deeply.
- `lën mi ti-m mali.` — I love you romantically. (shy admission)
- `hol mi ti-m holë.` — I thank you.
- `qor mi ti-m daru-yu.` — I will protect you.
- `sen mi nu mahori.` — I do not consent.
- `më pëla ti mi-wa nëra ya.` — Please stay with me.

## 17. Standard sentence patterns

| Function | Qaroshi | English |
|---|---|---|
| neutral statement | `sen sa haro.` | They are well. |
| identity | `sen sa qaro.` | They are a Nardoragon. |
| negative | `sen sa nu haro.` | They are not well. |
| past | `sen sa goro-te.` | They flew. |
| future | `sen sa goro-yu.` | They will fly. |
| progressive | `sen sa goro-se.` | They are flying. |
| past progressive | `sen sa goro-te-se.` | They were flying. |
| habitual | `sen sa goro-në.` | They regularly fly. |
| able to | `sen sa goro-ki.` | They can fly. |
| allowed to | `sen sa goro-ho.` | They may fly. |
| must | `qor sa goro-du.` | They must fly. |
| object | `sen mi ti-m tika.` | I see you. |
| possession | `sen mi-na naro haro.` | My home is good. |
| with | `më mi ti-wa nëra.` | I stay with you. |
| recipient | `sen mi mara-tu kima-m pëli.` | I give water to a friend. |
| direction | `sen mi naro-gu gura.` | I go toward home. |
| source | `sen mi naro-de gura.` | I go away from home. |
| evidence | `sen sa goro-te si.` | They flew; I saw it. |
| question | `hë sa haro he?` | Are they well? |
| request | `më pëla nëra ya.` | Please stay. |
| negative request | `më pëla nu gura ya.` | Please don't leave. |
| comparison | `sen sa mela zaki tëno mi.` | They are stronger than I am. |
| purpose | `më ti mi-wa nëra, ko mi haro.` | You stay with me so that I feel safe. |

## 18. Common pitfalls and resolution rules

1. **A typed sentence with no resonance particle is incomplete.** `Ti haro.` is only a fragment in standard written Qaroshi; `sen ti haro.` is complete.
2. **`më` contains ë, not `eë`.** `meë` is a transcription error, not another register.
3. **`sh` is one letter in the native alphabet.** Likewise `zh`, `kh`, and `ng`. A Romanized native-sign converter must use longest-match parsing.
4. **`naru` includes the listener; `muru` excludes the listener.** This is not optional social nuance.
5. **`nu` goes immediately before its predicate.** For “never die,” write `sëna nu zëru` or use `zëna zëru` (“die at no time”) when an unambiguous negative-time adverb is preferred.
6. **Questions keep `he` regardless of register.** `hë` begins a sentence; `he` ends a question. They are different forms and sounds.
7. **A suffix is not a separate word.** `mi-wa` can be written `miwa` in native script, but `mi wa` would be two unconnected words.
8. **Only one main tense and one aspect suffix per finite verb.** `shiri-te-yu` is not a standard form.
9. **Do not confuse inclusive and exclusive pronouns.** `naru` ≠ `muru`.
10. **Use a new sentence when the resonance changes.** Clauses in one sentence inherit the first marker.
11. **Do not read the register as a literal English word.** `më` is not a separate spoken “love” in the translation; it expresses the frame of the whole sentence.
12. **Romanized punctuation isn't a native letter.** Commas and question marks help readers; the required register particle and terminal `he`/`ya` carry the grammatical load.

## 19. Quick reference

**Sentence:** REGISTER + subject + (object-m) + (time/place/case phrases) + `nu`? + verb + `si/hu/ye`? + `he/ya`?  
**Noun:** root + derivation + `-lë`? + `-ri`? + case + `-së`?  
**Verb:** root + voice? + (`-te` or `-yu`)? + (`-se` or `-mo` or `-në`)? + (`-ki` or `-ho` or `-du`)? + `-la`?  
**Negation:** `nu` immediately before the predicate.  
**Yes/no question:** terminal `he`.  
**Request or command:** terminal `ya`; courteous `pëla`, optionally softened with `lan`.  
**Evidence:** `si` witnessed, `hu` reported, `ye` inferred.  
**Compound:** modifier + head; **noun adjectives come after the noun**.  
**Numbers:** base six.  
**Emotions:** 16 typed resonance markers; exactly one per complete sentence.

---

# PART II — ADVANCED GRAMMAR

The following sections extend, rather than replace, the preceding standard. Where this document distinguishes **mandatory** from **optional**, that distinction is grammatical. A resonance marker remains obligatory at the beginning of every independent sentence even in email, code comments, legal text, lists, and chat. Labels, fragments, isolated dictionary forms, addresses, headings and code tokens are not full sentences and need no register.

## 20. Formal sentence model and attachment

A complete independent declarative or interrogative sentence has the following high-level structure:

`RESONANCE [DISCOURSE] [TOPIC] [ARGUMENTS + ADJUNCTS] [NEGATION] PREDICATE [MODAL PARTICLE] [EVIDENTIAL] [SPEECH ACT]`

Here `[]` denotes optional syntactic slots, **not literal punctuation**. A quotation may contain an independent sentence with its own resonance. The final predicate of each clause is the structural anchor; word order remains predominantly subject–object–verb. Case endings allow an argument to move for topic or contrast, but movement does not change its case. The opening resonance is not the emotional state of the *subject*. It identifies the speaker's intended social frame of the utterance.

**Example:** `hë ti kima-m këmë-te he?` = Did you drink water? The register `hë` frames a sincere inquiry; `ti` is subject; `kima-m` is direct object; `këmë-te` is past predicate; terminal `he` makes the clause interrogative.

**No particles may precede resonance in an ordinary full sentence.** In dialogue, speaker names and timestamps are metadata rather than part of the Qaroshi sentence: `Sari [18:12]: më ti lësha.` In quotation, the quoted utterance begins a new sentence in its own speech domain and therefore has its own resonance.

**Clause boundaries.** Conjunctions `ara` (and), `nao` (but), `ro` (because), `ko` (so that), `wë` (if), `uro` (although), `yaro` (when), `ana` (after) and `ëna` (before) preserve normal predicate-final order within their clauses. They do not license a second opening register. The original `wë` remains valid for real, open, or unknown conditions.

## 21. Real conditionals, counterfactuals, concessions, wishes

The standard distinguishes four useful conditional types:

| Type | Marker | Semantics | Example |
|---|---|---|---|
| Real/open | `wë` | antecedent is possible, speaker does not assert its truth | `sen wë sa goro, mi sa-m tika-yu.` “If they fly, I will see them.” |
| Counterfactual | `wënu` | antecedent is treated as not actual at the relevant time | `sen wënu mi goro-ki, mi wena-gu gura-yu qinë.` “If I could fly, I would travel into the sky.” |
| Even if | `dasha` | consequent is asserted independently of whether antecedent holds | `dal dasha sa nu goro, mi sa-m daru-yu.` “Even if they do not fly, I will protect them.” |
| Unless | `shoru` | consequence applies if the stated exception fails | `sen shoru sa goro, mi naro-lo nëra-yu.` “Unless they fly, I will remain at home.” |

`qinë` is a **clause-final counterfactual-result marker**. It follows the predicate and precedes optional evidential; it is not a new tense or register. The predicate may use `-yu` for a projected result, but the *counterfactuality* comes from `wënu ... qinë`, not from future morphology. A real conditional takes no special consequent ending. Counterfactual *past time* can be indicated using `-te` within its subordinate clause; this does not change `wënu`.

`yëmë` is an **optative** (a wish or blessing). It occurs immediately after the mandatory resonance and before the clause: `më yëmë ti haro.` = “May you be well.” It is not an imperative: it does not require `ya`, does not oblige the addressee, and can concern events outside anyone's control. `qor yëmë naru sëna haro.` can be a solemn wish for lasting safety. When the addressee can act, use a request with `pëla ... ya` instead.

## 22. Quantifiers, distributivity and scope

**Standard 8.0 override (adopted):** `nëgëra` is the editioned quantifier *not every / not all*; it precedes its quantified NP and has the counterexample truth condition ∃x∈D ¬P(x), with D nonempty. It does not entail that any x satisfies P. Two explicitly quantified nominal phrases in a simple unembedded SOV clause take **linear surface scope** (leftmost quantified NP widest), while `-m` still marks semantic object independently of position. In plain discourse without overt quantifiers this rule makes no scope claims.

Quantifiers normally precede the noun phrase they quantify unless an established modifier has a different conventional position. The existing `ngënao` means “every/each without exception.” The newer `gawo` means “both of two,” while `nashu` means “together as one group,” without distributing the predicate over each member. `nura` is an independent “nobody/no one” pronoun; `yano` means “somebody/someone.” `miyo` means generic “one, people generally,” without picking a specific individual.

| Qaroshi | Translation | Interpretation |
|---|---|---|
| `sen ngënao qaro goro.` | Every Nardoragon flies. | universal, distributive |
| `sen gawo qaro-ri goro.` | Both Nardoragons fly. | two participants |
| `sen nashu qaro-ri goro.` | The Nardoragons fly as a group. | collective event |
| `sen yano naro-lo eri.` | Someone is at home. | existential indefinite |
| `sen nura naro-lo eri.` | Nobody is at home. | inherently negative quantifier |
| `sen miyo mara-m nashi.` | People generally cherish friends. | generic statement |

Do not add a second negator to `nura` unless a deliberately narrow logical scope is required. `nura nu eri` risks a double-negation reading and should not be used for ordinary “nobody exists.” `ngënao ... nu P` means “every ... not P” (none do P), whereas `nu ngënao` is not an accepted way of expressing “not every.” To negate universality itself, use current `nëgëra` immediately before the quantified NP; exceptions with `zërë` and contextual quantity phrases remain useful when the domain is disputed. This avoids ambiguity in technical writing.

`zërë` occurs after the excluded constituent: `sen qaro-ri, sa zërë, goro.` = “The Nardoragons, except for them, fly.” It does not add a separate resonance marker. If the exclusion is crucial to a precise legal or scientific statement, explicitly identify the excluded noun phrase; an ambiguous pronoun is insufficient.

## 23. Focus, topic, and shared knowledge

The established topic suffix `-së` is different from **contrastive focus** `rëshi`. The topic establishes what the sentence is about; focus asserts that a constituent is being singled out from alternatives. `rëshi` immediately follows a case-marked or unmarked constituent, and is normally used **at most once per clause**.

- `sen naro-së, mi naro-m daru.` = “As for the home, I protect the home.” (Topic, a repeated object for clarity.)
- `sen mi naro-m rëshi daru.` = “It is the home that I protect.” (Contrasting home with other possible objects.)
- `sen mi rëshi naro-m daru.` = “It is *I* who protect the home.” (Contrasting the subject.)

`nësho` is a speaker-facing discourse particle, placed after resonance, that signals the proposition is already established in the conversation. `shëgi` signals a corrective or unexpected fact. `hëla` marks an assertion as the speaker's evaluation rather than a claim to impartial consensus. These are separate from the evidentials `si`, `hu`, `ye` because they do not claim how knowledge was acquired.

- `sen nësho mi qaro.` = “As already established, I am a Nardoragon.”
- `sen shëgi sa haro.` = “In fact, they are well.”
- `zher hëla sa haro.` = “In my view, they are well, though I am doubtful.”

`shëto` is a corrective expression (rather/instead); it is used between alternatives or in a new sentence. An entire earlier clause does not need to be repeated if the correction is clear in context.

## 24. Asking, answering, and embedding questions

**Standard 8.0 clarification:** Wh-question particles and quantified phrases retain their own positions. A direct question with final `he` is not licensed by the simple declarative two-quantifier interpreter; do not use a declarative parse for an answer-seeking question.

A normal direct polar question ends in `he`, with any resonance the speaker chooses. A **confirmation tag** `hëmi` ends a sentence when the speaker leans toward believing the proposition: `hë sa haro hëmi?` = “They're well, right?” It **replaces**, rather than precedes, `he`. This prevents `he hëmi` double-marking.

`qona` introduces an **embedded polar question**, meaning “whether”; it does not ask the addressee a direct question. `sen sa haro qona mi sëmi.` = “I know whether they are well.” In this construction, the embedded `sa haro` contains no `he`, because only the matrix utterance determines speech act. A direct question *about* knowledge is `hë sa haro qona ti sëmi he?` = “Do you know whether they are well?” The one terminal `he` belongs to the entire independent sentence.

A content question uses the original interrogative word (`meya`, `khe`, `lona`, `yeta`, `shoro`, `hara`, `ruki`, `zëli`, `khema`). Do not move all wh-words to the front as in English; they stay where their answers would normally appear. `hë ti khe-m shëma-te he?` = “What did you eat?” (Object `khe-m` occupies the object slot.)

**Answers as fragments:** dictionary labels, single words, acknowledgments, and UI tokens can be written without resonance. A complete answer is a new sentence and requires one. For example `shë` (“yes”) can stand alone as a fragment, while `sen mi haro.` (“I am well”) must be marked.

## 25. Reporting, quoted speech and evidence

The original quotative complementizer `do` marks the end of a proposition treated as content. `toru` explicitly introduces direct quotation, which is treated as a nested utterance. It takes the following shape in reference transliteration:

`OUTER REGISTER + outer subject + toru «INNER REGISTER + inner sentence.» + matrix speech verb`

For example, `sen sa toru «më mi ti-m nashi.» shiri-te.` = They said, “I cherish you deeply.” The quoted sentence retains `më` because it is an actual complete utterance inside a quote, while the outer report begins with `sen`. The quotation glyphs are modern punctuation, not alphabet letters. A *paraphrase* does not need a nested independent register: `sen sa mi haro do shiri-te.` = They said that I was well (with tense set by context).

An optional clause-final evidential marks how the **outer speaker** knows the claim: `si` direct evidence, `hu` reported evidence, `ye` inference. Only one basic evidential is attached to a single evidential slot. If a story uses multiple layers of reported evidence, make the quotation layers explicit; do not stack `si hu ye`. `lëshu` marks customary or culturally received knowledge as a distinct source label: `sen qaro-ri goro lëshu.` = “By customary knowledge, Nardoragons fly.” It may be used when describing an established practice, but it is not a scientific proof marker. The same position as an ordinary evidential is used, so do not stack `lëshu` and `si` on one clause.

**No evidential remains an ordinary unmarked claim.** Absence of `si` should not be translated as uncertainty, and `ye` should not automatically be translated as “I doubt it.” Doubt is commonly expressed with the resonance `zher`, the adverb `sëro`, or explicit lexical content.

## 26. Additional noun and derivational structures

The grammar includes one spatial case and several derivational patterns:

| Form | Category | Function | Template |
|---|---|---|---|
| `-nga` | noun case | along/through/via; **perlative** | `naro-nga`, through the home |
| `-wë` | noun derivation | a kind or subclass of the noun | `qaro-wë`, a type of Nardoragon |
| `-këlë` | verb derivation | tool/instrument used for the action | `shiroli-këlë`, writing implement |
| `-rëma` | verb derivation | one occurrence of an action | `goro-rëma`, an instance of flying |
| `-sharo` | activity derivation | trained practitioner/specialist | `shiroli-sharo`, professional scribe |

A case ending is chosen from a mutually exclusive slot: `-m`, `-na`, `-lo`, `-gu`, `-de`, `-wa`, `-tu`, `-shi`, or **`-nga`**. The endearment/diminutive `-lë` is not a case, and the topic `-së` can be outermost. Thus `mara-lë-ri-nga` is a possible noun phrase (“through/along the dear friends”) if the intended traversal interpretation is coherent, but `mara-lo-nga` has competing cases and is not ordinary Qaroshi.

Do not treat **derivation** as **inflection**. Inflection changes grammatical function (e.g. `-ri` plural; `-te` past), while derivation creates a lexeme with a predictable general meaning. A specialized lexeme can differ from its compositional meaning if the lexicon documents it. The dictionary explicitly distinguishes transparent compounds from atomic headwords.

## 27. Verbal semantics, modality and temporal interpretation

`-te` orders an event before the reference time, `-yu` after; neither claims an action actually occurred unless the larger sentence asserts that event. The aspect slot remains limited to **one** of `-se` (progressive), `-mo` (completive), `-në` (habitual), or zero (neutral). The modal slot remains limited to **one** of `-ki` (ability), `-ho` (permission), `-du` (necessity), or zero. The interpersonal manner `-la` follows those. `qinë` is separate from verb inflection and is restricted to counterfactual consequents.

The most important contrasts are: `goro-te` = flew; `goro-te-se` = was flying; `goro-te-mo` = had finished flying; `goro-në` = regularly flies; `goro-ki` = can fly; `goro-yu-ki` = will be able to fly; `goro-yu-du` = will have to fly; `goro-ru-te` = caused someone to fly. Negation `nu` immediately precedes the **whole predicate word**, not an internal suffix: `sen mi nu goro-yu-ki.` = “I will not be able to fly.”

A conditional, wish, reported command, or quoted tense can have a reference time different from the speaker's present. For a translation, prefer an explicit temporal adverb if time reference is ambiguous. Do not invent a new inflectional form for English “might have been going to” until its intended modality and temporal anchoring are clear; use clauses or suitable lexical paraphrases instead.

## 28. Ditransitives, instruments, locations and possessors

**Standard 8.0 clarification:** For an overt passive agent choose `-za`; reserve `-shi` for instrument. Source-cited examples have only their recorded object class licensed, unless a manually reviewed verb sense authorizes broader arguments.

A recipient normally takes `-tu`, a theme (transferred thing) takes `-m`, and the verb is final: `sen mi mara-tu kima-m pëli.` = “I give water to a friend.” When an instrument is present, it takes `-shi`: `sen mi shiroli-këlë-shi shina-m shiroli.` = “I write a word using a writing instrument.” Historical texts also used `-shi` for a passive agent, but current precision writing uses `-za` for the actor and reserves `-shi` for the instrument.

A possessor `-na` precedes the possessed noun. `mi-na banu` means “my wing” regardless of whether a wing is removable or permanent. The possessive relation is not automatically ownership: family, memories and body parts all use `-na`. For ownership in a legal context, use the explicit verb `shënawo` (“belong to”) instead of inferring legal title from `-na` alone.

Location `-lo` is general “in/at/on”; to distinguish a physical surface from an interior, use the established spatial nouns (`larë`, `noro`, `qëra`, `gëra`, `yëra`) as needed. For motion, distinguish `-gu` destination, `-de` source, `-nga` path. One noun receives one case; multiple roles are expressed by multiple noun phrases.

## 29. Nominal predicates, identity, existence and tense

Qaroshi ordinarily omits a present-tense copula with a noun or adjective: `sen sa qaro.` = “They are a Nardoragon”; `sen sa haro.` = “They are safe.” For existence and locating a referent, `eri` is available: `sen sa naro-lo eri.` = “They are at home.” A past or future *identity* claim can use `eri-te` / `eri-yu` with its complement understood from context; do not attach tense suffixes directly to every adjective as though it were a verb. For especially precise translation, present a full clause rather than an isolated adjective ending.

Adjectives normally follow their nouns (`qaro lësha`, cute Nardoragon), but the same lexical adjective can serve as a predicate (`sen qaro lësha.`, the Nardoragon is cute). Comparative adverbs `mela` more, `rela` less, `samu` most, `rala` least precede an adjective. The comparison target follows `tëno`.

## 30. Morphological segmentation and ambiguity resolution

**Standard 8.0 disambiguation:** Morphological segmentation is done against the current 30,001-word editioned lexicon, which is a frozen 30,000-entry baseline plus `nëgëra` (Q8D001). Hyphens retain their existing case and verb meaning. Historical roots are not silently recomputed from English glosses.

Romanized teaching text may insert hyphens at affix boundaries; fluent writing may join them. Segmentation of `goro-te-se` is `goro` (fly) + `-te` (past) + `-se` (progressive). The lexical root must be resolved from a dictionary where possible; do not indiscriminately strip familiar sequences from an unrecognized word. For example, a headword ending in the letters `te` may be a full root rather than a past-tense verb. The interpreter should prefer an exact lexicon match before an inflectional analysis.

The maximal verb pattern is `ROOT + [VOICE] + [TENSE] + [ASPECT] + [MODAL] + [-la]`. At most one suffix from each bracketed class is allowed. The maximal noun pattern is `ROOT + [DERIVATION] + [-lë] + [-ri] + [CASE] + [-së]`. Extra multiple derivations should not be assumed productive unless documented. Dashes inside an already established root are part of the citation spelling in reference materials.

The 26-glyph alphabet is fixed. `sh`, `zh`, `kh`, and `ng` are each one **native letter**, despite containing two Latin characters. The letter `ë` is a separate vowel and must not be silently corrected to `e`. Names and loanwords are transliterated only after identifying their intended sounds; a direct English letter-by-letter replacement often fails.

## 31. Speech levels, interpersonal address and boundaries

The 16 sentence-initial resonance markers specify emotional/social delivery. They do **not** imply consent, truth, social rank, intimacy, a gender role, or an obligation. A formal document may frequently use `sen`, but any legitimate register is available if the content requires it. `keho` optionally precedes an addressed name or title to signal particular respect, without altering pronouns or grammatical number. `pëlë` is a deferential “please, if acceptable”; `pëla` is the ordinary polite request form.

`më pëla, ti mi-wa nëra ya.` = “Please stay with me.” This requests an action. `më yëmë ti mi-wa nëra.` = “May you stay with me.” This expresses a wish. Neither sentence assumes the other party has agreed. A reply of refusal (`nu` as a fragment or a full explicitly negative sentence) stands regardless of the request's Warm Hum resonance.

An affectionate resonance can express deep friendship, family, or romantic closeness. Use lexical expressions (`mali`, `lani`, `nashi`) to distinguish the relationship rather than assuming one from `më`. A solemn `qor` commitment may be sincere without being an enforceable contract. In a legal document, employ explicit terms for promise, obligation, deadline, parties and consequences.

## 32. Large quantities, technical notation and world dates

Traditional quantities use base six, with digits `ën` (0), `ka` (1), `po` (2), `dë` (3), `zhu` (4), `rë` (5), and `zhe` (6), `zhewa` (36), `zhewawa` (216). **Technical notation** may use ordinary decimal Arabic digits when interoperability matters, and should label the base if mixed in a single document: `101₆` vs `101₁₀`. A positional base-six representation of 100 decimal is `244₆` (2×36 + 4×6 + 4), while `100₁₀` is the usual international decimal spelling. Do not read `244` in an unlabeled scientific report as definitely base six.

ISO 8601 dates (`2026-11-14`) and 24-hour times (`19:46`) are permitted as technical notations, not new native alphabet glyphs. Units such as meters, seconds, volts, bytes, and degrees can use familiar international abbreviations as *quoted technical symbols* within a Qaroshi text. These abbreviations are not native letters and do not violate the 26-letter phoneme system because they are not spelled-out Qaroshi lexemes. Decimal separators, sign conventions and precision should be specified for machine interchange.

## 33. Modern vocabulary, semantics and loanwords

A glossary entry documents **one intended sense**, not every possible English meaning of a spelling. For instance, financial `interest (finance)` and general `interest (curiosity)` are different senses and may require separate Qaroshi headwords. Compound terms are head-final (modifier then head) and the lexicon notes constituent analysis where documented. A special compound meaning must be treated as a convention, not mechanically derived from English spelling.

Formal translation should prefer an unambiguous gloss, retain grammatical register, preserve negation and quantifier scope, and tag unsupported idioms rather than silently improvising. Modern acronyms, product names, usernames, file paths and code literals can be preserved as **quoted foreign text**, which is not interpreted by the Qaroshi word parser. Foreign passages do not require a Qaroshi resonance unless they are themselves complete Qaroshi sentences.

## 34. Document grammar, digital communication, and syntax validation

Every complete sentence in a Qaroshi article, chat message, subtitle or formal letter starts with one of the 16 resonance markers. A title or metadata field without an independent finite predicate is a fragment and need not start with one. Within a list, each item that constitutes a full sentence has its own resonance. Inside a complete quoted Qaroshi sentence, the quoted message has its own marker. Text in an ASCII-only environment should encode native `ë` reversibly; simply replacing `ë` with `e` can change lexical identity. UTF-8 is the preferred interchange encoding.

A validator may reliably check: legal graphemes, recognized resonance markers, duplicate headwords, suffix order, basic sentence openings, case conflicts, and malformed question endings. **It cannot guarantee meaning**, factual truth, idiomaticity, or a complete parse of unrestricted text. For example, knowing that `ti` and `haro` are dictionary words is not sufficient to determine every possible subordinate-clause attachment. Conscientious manual review is required for literary and legal translation.

## 35. Standard grammatical vocabulary

| Form | Function | Specific rule |
|---|---|---|
| `wënu` | counterfactual conditional | replaces `wë` for contrary-to-fact antecedents |
| `qinë` | counterfactual result | closes projected consequent after predicate |
| `yëmë` | optative | after resonance, before wish-clause |
| `rëshi` | contrastive focus | follows focused constituent |
| `nashu` | collective quantifier | before group noun |
| `gawo` | both (exactly two) | before countable noun phrase |
| `nura` | nobody | negative pronoun, no obligatory additional `nu` |
| `yano` | someone | indefinite animate pronoun |
| `miyo` | generic person | unbounded generic subject |
| `qona` | embedded whether | closes embedded polar interrogative proposition |
| `hëmi` | confirmation question | replaces final `he` |
| `toru` | direct speech introducer | quote has its own complete resonance |
| `tara` | until | temporal clause connector |
| `dasha` | even if | concessive hypothetical connector |
| `shoru` | unless | exception to conditional consequence |
| `nësho` | shared-ground discourse | after resonance |
| `shëgi` | corrective fact | after resonance |
| `hëla` | subjective stance | after resonance |
| `shëto` | corrective replacement | between alternatives, or standalone correction |
| `zërë` | except for | follows excluded phrase |
| `neshë` | regardless whether | introduces unconditional concession |
| `lëshu` | customary source | evidential slot; not stacked with `si/hu/ye` |
| `pëlë` | deferential please | request softener; no gender inference |
| `keho` | respect address | precedes addressed name/kin term |

**Conservative use principle:** If an advanced construction could be interpreted in several different ways, favor an additional clear clause over an untested stack of affixes or particles. The main function of the Qaroshi reference is expressive precision rather than maximum morphological density.

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

The established subordinators `wë` (“if”), `wënu` (counterfactual “if”), `ko` (“so that”), `ro` (“because”), `yaro` (“when”), `tara` (“until”), `dasha` (“even if”) and `shoru` (“unless”) remain unchanged. Additional connectors distinguish:

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

The aspect suffixes are: `-se` ongoing, `-mo` completed, `-në` habitual. Separate **preverbal particles** provide finer viewpoint distinctions:

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

Qaroshi uses `rëshi` for contrastive focus and `gawo` / `nashu` for “both” and group-level quantification. Additional forms include:

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

The prior evidentials remain `si` (direct witness), `hu` (reported) and `ye` (inferred), with `lëshu` (customary knowledge). More specific evidence markers are:

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

`mi`, `ti`, `sa`, `naru`, `muru`, `tiri`, and `sari` retain their the reference meanings. The inclusive/exclusive first-person plural contrast is especially important in cross-group cooperation: `naru` includes the addressee and `muru` excludes them. No pronoun marks gender or sexuality. Kinship, chosen family, individual identity, and legal relationship are all lexical matters, not forced pronoun distinctions.

A singular Nardoragon's name does not change the meaning of `sa`; use lexical references to disambiguate multiple participants. Use `-na` for possession, `-tu` for a recipient, and `-wa` for companionship. In sentences such as `më mi ti-wa nëra-yu.`, `ti-wa` says **with you**, not ownership of you. Pronouns in borrowed material should be interpreted in their original context before translation.

## 43. Distinguishing refusals, invitations and commitments

A request normally closes with `ya` and may use polite `pëla`. A question normally closes with `he`. In either case, an emotional or deferential resonance does not create a hidden obligation. A direct statement of a promise should state its action and conditions clearly rather than presuming that `qor` by itself is a contractual commitment. `nëto` can soften a refusal, but the refusal remains valid. `pëshu` explicitly rejects the assumption that a friendly invitation requires reciprocation.

For agreement with limitations, state those limitations using `wë` or `bëna`, optionally beginning with stance `shërawono`. Formal agreements must still identify parties, scope, times, enforcement conditions and whether the commitment is revocable. Literal interpretations matter most for agreements involving resources, bodies, consent, or residence.

## 44. Nardoragon cultural and physical vocabulary

The expanded lexicon makes finer distinctions between *roost*, *nursery*, *clutchmate*, *roostmate*, *flight mentor*, *apprentice*, *shared flight plan*, *safe landing signal*, *molt season*, *assisted first flight*, *communal lookout*, and *protected nesting area*. These are named experiences and practices, not grammatical gender classes. Terms such as *mournful flight* and *hatchling comfort call* can be used literally or as culturally meaningful expressions depending on context.

Qaroshi does not assign moral value to wing length, scale pattern, first-flight age, nesting structure, or other biological variation. Describing ability should distinguish *physical capacity*, *permission*, *safety conditions* and *social custom*: `-ki` means able, `-ho` means permitted, `-du` means required. The terms are not substitutes for one another.

## 45. Contemporary science, computing and AI terminology

Specialized words are recorded under distinct senses even when an English spelling is ambiguous. For example, **privacy** in ethics, **data privacy** in computing, and **privacy policy** as a document are not identical words. Technical concepts added include *prompt injection*, *differential privacy*, *local inference*, *inference latency*, *hardware security keys*, *cryptographic signatures*, *aerodynamics*, *clinical uncertainty*, *causal inference*, *statistical power*, and *stellar parallax*. The dictionary marks their English semantic scopes explicitly.

Reference terms do not automatically denote an exact model/product/brand. Proper names, API tokens, formulas, code, usernames, and unique identifiers can remain quoted foreign strings. No machine tool should automatically replace them by approximate Qaroshi sounds. A formal paper can retain internationally recognized decimal numerals, ISO dates, and scientific notation as *technical symbols* without adding letters to the 26 native-letter inventory.

## 46. Complex written documents

A full sentence starts with exactly one resonance marker, even in text chat, academic writing, captions, subtitles, UI copy or official correspondence. A label without a finite predicate (e.g. "Date", "Table 1", or a two-word heading) is a **fragment** and may omit resonance. Directly quoted **complete Qaroshi sentences** have their own resonance because they are independent utterances. Subordinate clauses introduced by `ko`, `wë`, `ro`, `tëwaro`, etc. inherit the enclosing resonance; do **not** place a fresh resonance at every comma.

One consequence is that strings with foreign material need a tokenizer that distinguishes quoted literal segments from regular Qaroshi sentences. Technical acronyms in a code block are not native 26-glyph Qaroshi lexemes. UTF-8 must be preserved, especially the six-way vowel inventory and the letter `ë`.

## 47. Dictionary organization and lexical categories

Qaroshi headwords are grouped by semantic domain and part of speech, with one principal English definition for each entry. Compounds preserve their documented components, while single-root terms are listed as independent headwords. The English index can point to the same Qaroshi entry under several senses.

The complete dictionary is a unified reference. Its stable IDs distinguish entries even when their concepts share a broad English meaning. New vocabulary may enter later editions by extending the dictionary without redefining existing entries silently.

## 48. Direction for a spoken Qaroshi corpus

A strong next step is collecting community-reviewed utterances in real scenarios: apologies and boundary repair, formal petitions, technical documentation, emergency flight calls, stories and songs, affection across different relationships, and ordinary chores. Track the sentence, resonance, speaker-intended meaning, word segmentation, lexical senses, regional voice style, and reviewer notes. Where several natural phrasings compete, document them instead of silently overwriting one with another. Versioned changes should preserve prior attested usage and make semantic drift visible.

## 49. Productive word formation and derivational boundaries

The 2.0 word-formation system remains valid, including `-mi` agent, `-ma` action noun, `-ra` associated place, `-rë` abstract quality, `-no` group, `-wë` taxonomic subtype, `-këlë` tool, `-rëma` event token, and `-sharo` professional specialist. Four additional **transparent derivations** are:

| Derivation | Root category → result | Compositional meaning | Example |
|---|---|---|---|
| `-dëno` | verb → noun | place or setting of an action | `shiri-dëno`: speaking venue |
| `-nëro` | verb → noun | result of an action | `shiri-nëro`: a speech product |
| `-khëno` | noun → noun | coordinated system of items or people | `mara-khëno`: organized friendship network |
| `-zëma` | verb → noun | trace or evidence that an action happened | `goro-zëma`: a trace of flight |

These are **derivational**, not verb conjugations and not replacements for noun cases. A derived form is built from one recognized root and one documented derivational ending. Its reading is transparently compositional until a distinct conventional sense is recorded and independently reviewed. A productive derivation does not automatically become a new headword; the lexicon lists conventional forms separately.

Rule priority in parsing: look for an **exact dictionary headword first**, then try the known, hyphen-separated teaching morphology, then offer compositional analysis. Do not strip a suffix from a legitimate dictionary root simply because its final letters happen to resemble a derivation. This guards against accidental semantic collisions.

## 50. Reference interchange and stable identifiers

Standard Qaroshi reference data is distributed as Unicode-normalized UTF-8 CSV and JSON. Every dictionary entry has a stable identifier, headword, word class, English gloss and semantic domain.

Romanized forms are normalized to NFC. Native-script letter conversion treats `sh`, `zh`, `kh` and `ng` as indivisible letters. Corpus records use stable sentence identifiers and each complete Qaroshi sentence begins with a written resonance marker.

When maintaining the reference, preserve prior lexical spellings and document any true corrections in the release notes.

## 51. Typed resonance and the discourse layer

Every independent sentence opens with exactly **one** resonance marker. The same 16 markers remain mandatory: `më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher`. An independent sentence cannot have a blank or inferred register even in short messages. For a message with multiple complete sentences, repeat the marker on each sentence.

Qaroshi has an **optional discourse frame slot directly after resonance**, usually one marker. Its function is to clarify whether a sentence quotes, corrects, summarizes or speaks from a given perspective. A discourse frame **does not replace** resonance and **does not change the truth of an assertion**.

`më qëmari ti lësha.` = From my affectionate perspective, you're cute.

`sen dënaro mi ti-m daru-yu.` = Correction: I will protect you.

Core order: `RESONANCE [FRAME] [TOPIC] [CLAUSE...] [EVIDENCE] [CONFIDENCE] [QUESTION/REQUEST END]`.

## 52. Verbatim quotations and paraphrases

`qëhano` frames the following words as a **direct quotation**. `wëlëmi` frames them as a **paraphrase**. The speaker must not combine both on the same reported span. Quoted material is not necessarily endorsed by the quoting speaker. If a verbatim quoted passage is a complete Qaroshi sentence, that quoted sentence retains its own resonance marker in the citation. Quoted **fragments** do not require one.

`sen qëhano mi ti-m nashi.` = Exact words follow: “I deeply cherish you.” (Fragment display.)

`sen wëlëmi mi ti-m nashi.` = Paraphrased: the speaker deeply cherishes you.

The Latin quotation marks `« »` are optional editorial punctuation, not two new glyph letters.

## 53. Explicit correction and repair

`dënaro` means *I correct my preceding claim*. The next clause supersedes the relevant earlier statement; the corrected proposition does not magically erase the earlier message. In continuous discourse the corrected content should be as specific as possible. `heshë` in the reference marks a correction of **misheard words**; `dënaro` is a correction of the **speaker's prior statement**, so the two are not interchangeable.

`sen dënaro mi ti-m daru-yu.` = Correction: I will protect you.

A new independent correction sentence still begins with its own resonance marker, even when it follows another marked sentence immediately.

## 54. Open questions and nonfinal assertions

`shurëmi` says the issue remains **unresolved**. It does not mean “maybe yes” or “maybe no,” and it is distinct from the speaker being personally doubtful (`zher` resonance). The particle is appropriate in research, mediation, and uncertain planning.

`zher shurëmi sa haro.` = It remains unresolved whether they are well.

For a literal question use final `he` when applicable. Do not treat `shurëmi` as question punctuation.

## 55. Assertive force, evidence, and withheld sources

`lëhona` marks **emphasis only**. It increases force, never certainty. `tënarë` announces a source **withheld for privacy**, not an independently verified source. Retain `si` (witnessed), `hu` (reported), `ye` (inferred), and the more specific evidentials where supported. The optional frames cannot upgrade a statement's evidence.

`qor lëhona mi ti-m daru-yu.` = Emphatically, I will protect you.

`sen tënarë sa goro-te hu.` = According to an unidentified report, they flew.

A source-withheld marker is not a citation and should never be used to invent or conceal evidence.

## 56. Fiction, simulation, and counter-to-expectation frames

`gëmano` signals **fictional or simulated** scope. A proposition within this scope is not an assertion about the real world. `zënare` marks that an actual or claimed event **contradicts earlier expectations**; it does not by itself encode who expected what. `yë` remains the *felt surprise* resonance.

`sen gëmano mi goro-ki.` = In a simulated scenario, I can fly.

`yë zënare sa goro-te si.` = Surprisingly, against expectation, I saw them fly.

The `wënu` counterfactual conditional from the reference remains distinct: it relates unreal conditions to consequences.

## 57. Source perspective, self-perspective, and other viewpoints

`qëmari` locates the statement in the **speaker's own perspective**, especially useful in opinion, aesthetics and emotional interpretation. `bëlaro` attributes a **viewpoint to someone else**, without implying agreement. The reported person or source should be identified from context or a neighboring clause.

`më qëmari ti lësha.` = To me, you are cute.

`sen bëlaro sa haro.` = In another person's view, they are well.

These particles are not evidential markers and cannot replace an actual source when one is needed.

## 58. Relative time boundaries

Temporal adverbs precede the predicate in the usual SOV clause. `rënogi` means *up to now* and focuses a past-to-present interval; `sëwëna` means *from now onward*. Both differ from `sëna` (*always; forever*), which has no inherent start at the current moment.

`sen mi naro-lo rënogi nëra.` = Up to now I remain home.

`dal mi ti-m sëwëna daru-yu.` = From now on, I will protect you.

For **time bounds** rather than point times: `zhëqaro` = *not earlier than* and `mërëlo` = *not later than*. They precede the reference time expression and do not imply a timestamp is known exactly.

## 59. The “by,” “since,” “until,” and “whenever” clauses

These conjunctions introduce complete subordinate clauses, which inherit the independent sentence's opening resonance:

| Marker | Meaning | Distinguishing rule |
|---|---|---|
| `hëgoro` | by the time that | Matrix event completes no later than boundary |
| `wërano` | whenever | Recurrence over relevant occasions |
| `torëne` | until | State continues up to endpoint |
| `mëlëno` | since | Interval begins at subordinate past event |

`sen hëgoro ti goro-te, mi nëru-te-mo.` = By the time you flew, I had finished resting.

`sen wërano ti goro, mi ti-m tika-në.` = Whenever you fly, I habitually see you.

## 60. Conditional premises and restricted scope

`zhëwëra` introduces an **evidential premise**. `tëwëro` introduces a **premise accepted for current reasoning**. `khënari` means **only insofar as** and limits a rule to a specific scope. None is interchangeable with the simple hypothetical condition `wë`.

`sen tëwëro ti haro, mi ti-wa goro-yu.` = Given that you are well, I'll fly with you.

`sen khënari ti haro, mi ti-wa goro-yu.` = I will fly with you only to the extent that you are well.

In nested conditions, prefer explicit commas and avoid relying on English-style “if and only if,” which is not encoded by one of these forms alone.

## 61. Distribution and exclusion

`nëzha` is a **determiner** preceding a noun: each member is considered separately. This contrasts with the general collective interpretation of a plural noun. `gëwëmi` is a **postposition** following the excluded noun or noun phrase: *except for*. Whether the exception applies to subjects, objects or a larger quantified group must be made clear by position and surrounding words.

`sen nëzha qaro goro.` = Each Nardoragon flies individually.

The existing noun suffix `-ri` is still ordinary plural, not a substitute for a distributive marker.

## 62. Approximate limits versus exact quantities

`shëwëri` before a numeral conveys an **approximate upper bound**. Keep it separate from the reference's exact lower/upper/exact quantifiers. Traditional Qaroshi numerals remain base six; for scientific data, conventional Arabic numerals may be borrowed as technical notation without changing the 26-letter alphabet.

`sen shëwëri po qaro-ri goro.` = Roughly no more than two Nardoragons fly.

Upper bound is not an estimate of equality; “at most about two” allows fewer.

## 63. Restricted audiences and intended recipients

`hanori` explicitly states **the listener** is the utterance's social recipient, even if grammatical third-person subjects occur. `rëgëmi` states a sentence is **not addressed to everyone present**, without claiming privacy or secrecy. Both occupy the post-resonance frame slot.

`më hanori mi ti-m nashi.` = Addressing you specifically, I care deeply for you.

Audience markers do **not** replace the morphological recipient `-tu`, which encodes an argument of the verb.

## 64. Rhetorical versus sincere questions

`yëhano` makes an otherwise question-formed sentence explicitly **rhetorical**, and the final `he` remains. With sincere questions, use the normal `hë` Seeking Call resonance without the rhetorical frame. A playful rhetorical question can use `zha`; resonance and rhetorical force are independent.

`hë yëhano ti haro he?` = Rhetorically, “Are you well?”

When a genuine answer is expected, omit `yëhano` and preserve final `he`.

## 65. Consent-friendly requests and qualified promises

`tëqoro` says **this request can freely be refused**. It is a discourse stance, not an automatic grant of consent; a response must still be obtained when actual consent is required. `këmëro` makes a promise **explicitly conditional**, and the condition must be stated in the same or clearly linked clause.

`më tëqoro ti mi-wa goro ya.` = You're invited to fly with me, with no pressure to agree.

`qor këmëro wë ti goro, mi ti-m daru-yu.` = If you fly, I promise to protect you.

Unqualified solemn promises continue to use `qor` with ordinary future morphology; conditional frames avoid accidental overpromising.

## 66. Summaries and side comments

`wëharu` marks a **summary**, not necessarily the final sentence of the conversation. `mëgoro` marks a **side note**, allowing the listener to treat the content as related but not central. Neither authorizes skipping mandatory sentence-initial resonance on later sentences.

`sen wëharu mi qaroshi-m shiri.` = In summary, I speak Qaroshi.

`zha mëgoro mi qaroshi-m shiri.` = A playful side note: I speak Qaroshi.

## 67. Lexicalized event predicates

The lexicon includes specialized single-root predicates corresponding to specified English actions such as *request a reasonable accommodation* or *review an editorial correction*. These are **lexicalized event predicates** for instructional clarity, not evidence that every English verb–object phrase should become one Qaroshi root. Such a predicate generally does **not** take another copy of its English-internal object.

The conservative sentence templates use `sen mi VERB-yu.` = “I will [event]” and `hë ti VERB-yu he?` = “Will you [event]?” More compositional native expressions using an existing verb plus a marked object should be preferred when semantically adequate. Where a compositional expression is clearer, the ordinary verb-plus-object construction is preferred.

## 68. Unified standard lexical forms

All headwords and grammatical particles in the current dictionary belong to one integrated Qaroshi reference. Dictionary entries do not require special grammatical treatment based on when they were entered.

The reference distinguishes a lexical headword from a productive compound and a grammatical function word. New forms are checked against existing spellings, and grammatical particles occupy the positions set out in the relevant chapters.

Dictionary inclusion describes the standardized meaning and spelling in this reference, not the frequency with which speakers use a term.

## 69. Writing conventions for technical and digital contexts

Native Qaroshi is written left-to-right using the original 26 glyphs; `sh`, `zh`, `kh` and `ng` are single letters. Romanization should normalize to Unicode NFC. A hyphen is an **editorial morphology separator**, and Latin punctuation and Arabic digits are **technical marks**, not additions to the native alphabet. The offline reader converts Romanized text into the original glyph artwork and supports copying or exporting rendered text.

Imported filenames, program identifiers, domain names, and literal quotations may be displayed in their source scripts and tagged as external tokens. A parser must never silently reinterpret those tokens as Qaroshi headwords. Automated word checking is partial and should not claim to verify semantics, discourse intention or correctness of an entire translation.

## 70. Translation practice and long-term language coverage

Qaroshi has its own lexical system and clause structure. Natural translation preserves information structure, speaker stance, grammatical scope and mandatory written resonance rather than replacing words one by one.

Technical and specialized vocabulary is available in the unified dictionary. Some English expressions still require paraphrase or explanatory clauses. The translation guide describes how to handle such cases without borrowing English syntax wholesale.

The reference is a descriptive and pedagogical standard; broad dictionary coverage should not be confused with a measured frequency corpus.


## 71. Clause topology and the finite predicate

**Standard 8.0 scope:** A two-quantifier construction has exactly two overt quantified noun phrases (one subject, one `-m` object) and a simple final lexical verb. The leftmost quantified phrase binds wider; case-marked object topicalization therefore changes the *formal scope order*, never the argument role. A sentence with embeddings or ordinary discourse topics requires an independent clause analysis and is not automatically interpretable by the simple-scope checker.

An independent sentence starts with exactly one resonance. The usual clause order is **[stance] [topic] [time] subject [recipient] [object] [adverbial] predicate [mirative] [evidential] [confidence] [question/request final]**. Case-marked constituents may be topicalized when their grammatical roles remain clear. The position of `nu` is not flexible: it immediately precedes its own predicate. The postpredicate material is grammatical and does not contradict the subject–object–verb default.

`sen mi kima-m këmë.` = I drink water. `sen kima-m-së mi këmë.` = As for water, I drink it. An utterance with an omitted recoverable subject remains resonance-marked. This chapter does not authorize moving the object marker to an adjective or dropping suffixes in formal writing.

**Further reading:** `docs/advanced/01_syntax.md`.


## 72. Relative clauses and reference gaps

A relative clause is prenominal and ends with `sha`; its missing argument is interpreted as the head noun. `[mi tika-te sha] mara` means the friend whom I saw. In `më mi [mi tika-te sha] mara-m nashi.`, the matrix case attaches to `mara`, not to the internal verb. A relative inherits its sentence's resonance and does not open with an independent marker.

When more than one relative argument could be understood as missing, prefer a new independent sentence with a demonstrative. Do not map English “who,” “which,” and “that” into separate compulsory relative markers without evidence.

**Further reading:** `docs/advanced/01_syntax.md`.


## 73. Content clauses and embedded questions

A content clause is bounded by `do`. In `sen sa haro do mi sëmi.`, the claim “they are well” is the thing known. The content clause does not itself establish the narrator's source or confidence. An embedded question is distinguishable from a direct question through the matrix verb and clause boundary; if two `he` finals create potential ambiguity, render the embedded material as an explicit quote or two sentences.

Every quoted independent sentence retains its own resonance as part of the quotation; that marker is not a second marker opening the narrator's independent clause.

**Further reading:** `docs/advanced/01_syntax.md`.


## 74. Verb frames and participant roles

**Standard 8.0 licensing:** The current valency inventory is `data/standard_8/verb_audit_400.csv`. Twenty-five inherited frames have general reviewed licenses. Other entries have individually documented *examples*, not blanket morphological/passive/causative licenses. Do not infer any new passive or object class from an editorial parallel example; adopt a full frame only through a recorded selectional review.

Document each verb's usual arguments. **V0** verbs need no object (`sen sa goro.`); **V1** verbs take an object (`sen mi ti-m tika.`); **V2** transfer verbs can take recipient and object (`sen mi mara-tu kima-m pëli.`). Source `-de`, goal `-gu`, place `-lo`, instrument `-shi`, and comitative `-wa` identify different semantic roles.

The table `data/semantics/valency_frames.json` supplies curated frames for frequent roots; it is not a universal automatic inference for 30,000 dictionary entries. A verb's English gloss alone cannot determine its Qaroshi case frame.

**Further reading:** `docs/advanced/01_syntax.md`.


## 75. Topic, focus and information structure

The topic suffix `-së` flags what the clause is about and comes after any case suffix. The information status of a referent is **not** automatically determined by the presence or absence of `-së`; established topics can remain unmarked. A focus particle such as `ngëshi` follows the constituent whose alternatives are restricted.

Topic continuity permits ellipsis of recoverable subjects in dialogue, but long-form written texts should renew noun references when a competing singular `sa` or new character appears. `qëlo` repairs a prior utterance; it does not erase the original from a quotation.

**Further reading:** `docs/advanced/01_syntax.md`.


## 76. Negation and focus scope

**Standard 8.0 negation scope:** Ordinary predicate `nu` is immediately preverbal. For two overt quantified noun phrases the surface-first quantifier has widest scope; predicate `nu` scopes inside both. `nëgëra` already negates universal force and is not combinable with predicate `nu` in the restricted two-quantifier construction. In other constructions state scope by overt individual clauses and report unresolved ambiguity.

`nu` immediately precedes the verb or adjective predicate it negates. `sen mi kima-m nu këmë.` means I do not drink water; it does not assert which other drink I consume. A focused negative can be ambiguous about whether the negation applies to the focal alternative or the whole exclusivity claim. Split the proposition into two sentences if the distinction matters.

`zëna` (never) or `sëna nu V` (always not V) provides temporal non-occurrence. Never treat non-occurrence, refusal, inability and prohibition as synonyms.

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 77. Scalarity, comparisons and alternatives

The degree markers `mela`, `rela`, `samu`, `rala` precede the adjective. `tëno` introduces the standard of comparison. `ngëshi` (only), `bëso` (also) and `tëmiri` (even) rely on a contextually salient comparison set. Their use affects what is implied about alternatives without changing the noun's base dictionary meaning.

In a comparison, name the two entities explicitly when otherwise ambiguous, and avoid treating “not good” as a definite lexical opposite of “good.”

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 78. Quantifiers and distributivity

**Standard 8.0 quantifiers:** The adopted `nëgëra` is distinct from both `ngënao NP nu P` (*none*) and `shërano NP P` (*some*). In a two-quantifier simple clause, bind leftmost NP outside the rightmost. Example: `sen shërano qaro ngënao mara-m tika.` is ∃qaro ∀mara see(qaro,mara); `sen ngënao mara-m shërano qaro tika.` is ∀mara ∃qaro see(qaro,mara). These differ. The examples are normative editorial constructions, not independent recorded speech.

Numerals follow nouns; numeral bounds `qësho`, `rëshu`, `nëmi` occur before the numeral. `qaro-ri qësho po` = at least two Nardoragons. A plural sentence does not itself guarantee whether its action is collective or individual. Where scope matters, use explicit collective/distributive forms and independent clauses to prevent “not all” from being mistaken for “none.”

The traditional number system is base six; in mathematical or scientific text, attach explicit base notation to digits when a value would otherwise be misinterpreted.

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 79. Ability, permission and obligation

**Standard 8.0 valency restriction:** Voice and modality retain original slot order. A source-licensed object case for a verb does not automatically license that verb's `-li` passive or `-ru` causative; those require a reviewed argument structure.

`-ki` is dynamic potential/ability, `-ho` permission, and `-du` necessity. They are alternatives in the modality slot, not interchangeable English “can/may/must” variants. `sen sa goro-ki.` = They can fly; `sen sa goro-ho.` = They may fly; `qor sa goro-du.` = They must fly.

An emotionally warm register does not grant permission, and a speaker's promised future action does not establish its success. If a source combines two modals, use clausal coordination or a descriptive predication rather than stacking both modal suffixes.

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 80. Evidentiality, mirativity and confidence

`si` witnessed, `hu` reported and `ye` inferred remain core evidentials. `shëku` remembers a prior observation, `wërusha` cites an instrument or measurement, `rëhu` cites an archive, and `lëshu` expresses customary knowledge. At most one evidential belongs to a finite clause. Mirative `yëqo` may precede evidential; confidence `sëki` or `qëru` follows it.

A source marker explains **how the speaker obtained the claim**, not whether the claim is necessarily true. Do not use a serious resonance to substitute for evidence.

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 81. Open, future and counterfactual conditions

`wë` introduces an if-clause; `bëna` means provided that/as long as. A conditional's antecedent is not asserted by being uttered. Future `-yu` commonly appears in projected consequences. `ye` is an inferential evidential and cannot by itself encode “contrary to known fact.”

For past counterfactuals with real consequences, state what actually happened in a separate sentence if the context does not already establish it. Purpose `ko` marks intention and never guarantees fulfillment.

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 82. Reference time and aspectual viewpoint

Tense `-te` and `-yu` locate an event before or after reference time; aspect `-se` views an ongoing event, `-mo` a completed event, and `-në` a habit. The order remains root–voice–tense–aspect–modal–manner. A clause may describe an interrupted action, a habit no longer held, or a completed act without specifying any resultant state.

Do not infer arrival from `goro-te-mo` merely because the flight finished. Temporal adverbs can refine a clause without changing the main tense suffix.

**Further reading:** `docs/advanced/02_scope_logic.md`.


## 83. Adjacency pairs, turn-taking and repairs

**Standard 8.0 conversation:** Full independent written sentences retain one opening resonance. Single-word replies and bare labels may be fragments. Omitted participants are only safe with one recoverable referent, not when consent, identity or actor responsibility is disputed.

In dialogue, a first move makes a reply relevant: questions invite answers, requests invite granting or declining, and apologies invite acknowledgment. A turn may contain several independent sentences, each marked separately. An omitted subject in a short answer is licensed by recoverable discourse context, not by a conjugation ending.

`qëlo` marks repair of a mistaken utterance. A correction should name the disputed material when the speaker could otherwise be misunderstood. An unanswered request must not be reinterpreted as granted consent.

**Further reading:** `docs/advanced/03_discourse.md`.


## 84. Quotation, attribution and paraphrase

`hëra` marks a paraphrase; it does not claim verbatim quotation. `bëlaro` signals another person's perspective. A quoted complete sentence keeps its quoted resonance marker, while the narrating sentence also has an independent one outside the quotation.

Editors should preserve what was stated, what was inferred, and who supplied which source. A quotation with no documented source should not acquire false certainty from the translator.

**Further reading:** `docs/advanced/03_discourse.md`.


## 85. Register, politeness and direct refusal

Qaroshi registers are typed resonance choices, not social caste or gender classes. `pëla` marks courteous appeal; `lan` and `pëshu` can lower pressure. These cues never overrule explicit `nu`, `noharo` or `mahori`. A direct refusal may be one complete sentence with its own resonance; it need not justify itself.

Profanity and intimate language also have lexical register. Clinical, vulgar, playful and abusive terms should be distinguished in reference notes; a swear directed at circumstances is not necessarily an insult to a person.

**Further reading:** `docs/advanced/03_discourse.md`.


## 86. Connected speech and phrasal stress

**Standard 8.0 pronunciation:** Existing native digraphs `sh`, `zh`, `kh`, `ng` remain distinct graphemes. Proposed or recorded compounds are not respelled due to an English gloss. Spoken connected-speech simplification does not create an alternate written word.

Dictionary IPA is **phonemic**, derived from the six vowels and twenty consonants of the 26-glyph inventory. Primary lexical stress is normally penultimate. In fluent speech, focus may change *phrasal prominence* without changing the lexical syllable segmentation. `sh`, `zh`, `kh`, and `ng` each represent one native letter.

A speaker may produce casual boundary reductions, but the standard does not mandate an unrecorded universal sandhi rule. Do not silently change canonical IPA or spelling based on English-like vowel reductions.

**Further reading:** `docs/advanced/04_phonology.md`.


## 87. Allophony and phonotactic constraint

Potential context-dependent adjustments, such as nasal place coarticulation, are treated as **phonetic expectations**, not mandatory spelling changes or evidence of new phonemes. `/q/` contrasts with `/k/` and `/x/`, `/ɾ/` with English-like approximants, and `/n/` with `/ŋ/`. This distinction holds across all resonances.

Foreign names containing letters absent from native Qaroshi should remain visibly quoted or be transliterated by an explicit, individually justified adaptation. Do not invent native glyphs without altering the alphabet standard.

**Further reading:** `docs/advanced/04_phonology.md`.


## 88. Polysemy, senses and valency

**Standard 8.0 word senses:** Words with overlapping English definitions are not automatically Qaroshi synonyms. The current sense constraints in `data/standard_8/lexical_decisions.csv` and `data/semantics/curated_senses.json` control their explicitly reviewed meanings. Unreviewed compounds keep documented lexical glosses, with compositional interpretations labeled provisional.

A form may possess related senses, and a semantic frame specifies which participants are expected. `naro` may denote a dwelling/nest/shelter; `nashi` care does not entail `mali` romantic love. Sense records should cite the same stable dictionary identifier when they describe one lexical form, not create phantom new headwords.

`data/semantics/curated_senses.json` and `valency_frames.json` document high-frequency cases with explicit sense and argument notes. They do not claim to have fully sense-tagged all 30,000 dictionary entries.

**Further reading:** `docs/advanced/05_lexical_semantics.md`.


## 89. Idioms, collocation and figurative extension

**Standard 8.0 idioms:** Existing literary figures remain editorial conventions, not universally traditional idioms. Irony must have a recoverable contextual frame and cannot be inferred from resonance alone. Literal high-stakes use takes precedence unless figurative scope is marked.

A collocation is a conventional pairing (`kima-m këmë`), an idiom has an established meaning beyond its component words, and a fresh metaphor relies on creative interpretation. They should not be lumped together in a word-count statistic. Productive compounds usually put the modifier before the lexical head; an individual compound's specialist meaning may narrow through usage.

A technical translator should expand an opaque metaphor rather than give it false precision. Native-speaker evidence would be required before claiming a newly proposed saying is historically traditional or common.

**Further reading:** `docs/advanced/05_lexical_semantics.md`.


## 90. Genre conventions and textual coherence

Casual dialogue permits recoverable ellipsis; narrative needs consistent reference time; science requires evidential discipline; technical instructions require clear actors and ordered steps; legal and consent texts must distinguish ability, authority, refusal and obligation. Poetry may intentionally deviate but should mark creative usage as such.

The extended connected corpus provides controlled multi-turn dialogues and short narratives, with speaker and discourse annotations. Its exercises support analysis, not claims about corpus frequency or dialect distribution.

**Further reading:** `docs/advanced/06_genres.md`.

---

## Edition appendix 8.1 (adopted)

Source: [docs/standard_8/AMENDMENT_8_1_EMBEDDED_POLAR.md](../../docs/standard_8/AMENDMENT_8_1_EMBEDDED_POLAR.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Qaroshi Standard 8.1 · Embedded Questions and Clause-Local Negation

**Status:** adopted **minor grammatical clarification** to the current unified Standard 8.0. It does not replace any existing native glyph, lexeme, written resonance marker, case ending, valency frame, or frozen historical corpus. It applies to new precisely written Qaroshi and explains an edge case left ambiguous by Standard 8.0 chapter 73. This is a *constructed-language normative decision*, not attested speaker behavior.

## Problem uncovered by the 500-sentence challenge

Standard 8.0 chapter 73 already permits `do` as a content-clause boundary and `he` as the direct polar-question ending. It did **not** unequivocally identify the scope of a polar-question `he` inside a complement: a writer trying to express *I do not know whether they are well* could be mistaken for asking a top-level question or negating the embedded claim. A genuine `whether P` is **not equivalent** to either `that P` or `that not P`.

## Adopted clause-boundary rule

In a finite content complement, **`he` directly before `do` marks an embedded yes/no question**. The matrix statement continues after `do`. An independent matrix yes/no question ends with a *different*, final `he` **after** its matrix predicate.

For simple positive/negative complements with explicit participants:

```text
[RESONANCE] [embedded subject] [nu?] [embedded predicate] [he?] do
            [matrix subject]   [nu?] [matrix predicate] [he?]
```

The bracketed `he` immediately before `do` yields **whether P**. Its absence yields **that P**. Final matrix `he` asks whether the *matrix statement* is true. If both appear, they have **different clause scopes**, not two competing readings of the same sentence. Do **not** write a new resonance inside this dependent complement: the independent outer sentence already has one. Quoted independent speech remains a separate exception with its own written resonance under chapter 84.

`nu` remains attached to the next **local predicate** only. A `nu` before a matrix verb never negates the embedded proposition; a `nu` inside the complement never negates the speaker's knowledge. Speakers must name referents rather than elide them when ambiguity matters. This rule does not permit arbitrary extra `he` markers, nested `do` clauses, unlicensed verb frames, or stacked negators.

### Minimum contrast set

| Qaroshi | Precise English interpretation | Note |
| --- | --- | --- |
| `sen sa haro do mi sëmi.` | I know that they are well. | Declarative complement |
| `sen sa haro he do mi sëmi.` | I know whether they are well. | Knowing the answer does not claim they are well |
| `sen sa haro he do mi nu sëmi.` | I do not know whether they are well. | Matrix negation only |
| `sen sa nu haro do mi sëmi.` | I know that they are not well. | Embedded predicate negation only |
| `sen sa haro do mi nu sëmi.` | I do not know that they are well. | Lack of knowledge does not assert they are unwell |
| `sen sa nu haro he do mi sëmi.` | I know whether they are not well. | Embedded negative *question*, not a matrix negative |
| `hë sa haro he do mi sëmi he?` | Do I know whether they are well? | Inner `he` before `do`; outer `he` at sentence end |
| `sen sa haro he do ti nu sëmi.` | You do not know whether they are well. | Matrix person changed, same scope |

**Knowledge semantics:** `sëmi` is the existing verb *know / possess reliable knowledge*. `know that P` presents P as known; `know whether P` means the answer to the polar question is known but does **not** assert which alternative is true. `not know whether P` says nothing about P's truth. This clarification is intended to prevent fabricated assertions from translating “I don't know whether…” into “I know that not…”.

### Restrictions and compatible readings

- Only a **single** unquoted, bounded `do` complement is specified here. Multiple embeddings, multiple quantifiers, counterfactual complements, focus, or disputed reference require full manual clause analysis.
- The formal `he do` rule applies to a polar complement. For embedded *wh*-questions, use their already documented interrogative forms and preserve constituent roles; this amendment does not authorize an invented wh-marker.
- Earlier 7.0 and 8.0 texts that use two full sentences or quotation remain readable; they are **not** automatically rewritten.
- A parser with a smaller lexical whitelist can still correctly decline a grammatical sentence. The reference implementation in `tools/stress81/embedded_question.py` deliberately covers only pronouns, the documented simple predicates `haro` / `goro`, and the attested matrix verb `sëmi`. That limit is software coverage, **not a universal language restriction**.

### How to test it

The 8.1 regression suite compares *that* versus *whether*, matrix versus embedded `nu`, matrix versus embedded `he`, and malformed boundary cases. It intentionally refuses nested or structurally unsupported input. A human comprehender test is still required before claims of intuitive spoken usage.

## Status of the 500-sentence audit

The original 500 challenges cover **100 distinct situations** transformed five ways in ten domains and do not exactly duplicate the indexed prior English example sentences. The old English-to-Qaroshi tool abstained on **500/500** unfamiliar prompts; **30/30** known-source retrieval controls passed. We separately constructed **49 rule-backed, dictionary-grounded quantifier drafts** from the 500. None is labeled a speaker-verified translation. The remaining **451** have no verified complete translation in this audit. **Abstention is not evidence that Qaroshi lacks the underlying grammar.**

The challenge set, all per-item tool outcomes, positive controls and machine-readable summary are in `data/stress81/`. The exercise is not a proficiency experiment: **zero independent respondents** and no reliable open-domain accuracy estimate. Future revisions should fix the highest-priority ambiguities *only after* case-by-case semantic analysis, with source references and independent comprehension checks where possible.

---

## Edition appendix 8.4 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_4_CORE_VERBS.md](../../docs/standard_8/AMENDMENT_8_4_CORE_VERBS.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Qaroshi Standard 8.4 · Productive Core Verb Amendment

**Editioned editorial norm, effective for new 8.4 writing.** This document adds **11 explicit narrow active-sense argument frames** to the existing 25 individually reviewed frames. These are deliberate constructed-language rules, **not attested human usage**. They do not grant generic passive or causative morphology.

The frozen 7.0 lexicon and all earlier standard documents remain untouched. Historical readings remain governed by their contemporary editions. For new 8.4 writing, this overlay controls the listed exact senses only. If another old gloss permits a different sense, that separate sense has not been silently generalized.

## 8.4 licensed frames

| Lemma | Frame | Core semantic boundary | Canonical model (editorial) |
| --- | --- | --- | --- |
| `rëgë` | V1 | repair; restore function to an existing damaged or nonfunctional thing | `sen mi naro-m rëgë.` |
| `shiwari` | V1 | send or transmit a message or movable item | `sen mi mara-tu kima-m shiwari.` |
| `shërami` | V0 | sleep | `sen mi shërami.` |
| `rëmi` | V1 | learn a language, topic, or skill | `sen mi qaroshi-m rëmi.` |
| `shirali` | V0 | sing or perform vocally | `sen mi shirali.` |
| `pënari` | V1 | use or employ a resource for a purpose | `sen mi kima-m pënari.` |
| `wënoa` | V1 | miss or long for someone absent | `wen mi ti-m wënoa.` |
| `kërawë` | V0 | try or make an attempt, with the action unspecified | `sen mi kërawë.` |
| `yëli` | V0 | shine or emit visible light | `sen sa yëli.` |
| `sharoni` | V1 | need or require a thing | `sen mi kima-m sharoni.` |
| `eri` | V0 | exist or be present | `sen sa eri.` |

## Role-licensing and semantic precision

### rëgë: V1

- Defined sense: repair; restore function to an existing damaged or nonfunctional thing.
- Required: subject:repairer; object:-m (thing being repaired).
- Optional: instrument:-shi.
- **Do not infer:** The repair action does not entail success unless completion or result is explicitly stated.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi naro-m rëgë.`.

### shiwari: V1

- Defined sense: send or transmit a message or movable item.
- Required: subject:sender; object:-m (message or item).
- Optional: recipient:-tu.
- **Do not infer:** Sending does not assert receipt, reading, or agreement.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi mara-tu kima-m shiwari.`.

### shërami: V0

- Defined sense: sleep.
- Required: subject:sleeper.
- Optional: location:-lo.
- **Do not infer:** Sleep is not the same as resting; the sense does not take a direct object.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi shërami.`.

### rëmi: V1

- Defined sense: learn a language, topic, or skill.
- Required: subject:learner; object:-m (subject learned).
- Optional: none introduced.
- **Do not infer:** Learning does not by itself imply expertise or completed mastery.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi qaroshi-m rëmi.`.

### shirali: V0

- Defined sense: sing or perform vocally.
- Required: subject:singer.
- Optional: none introduced.
- **Do not infer:** A song-title/theme as a direct object is not licensed in this sense without a distinct reviewed frame.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi shirali.`.

### pënari: V1

- Defined sense: use or employ a resource for a purpose.
- Required: subject:user; object:-m (thing used).
- Optional: none introduced.
- **Do not infer:** Using is not owning, creating, or successfully achieving a purpose.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi kima-m pënari.`.

### wënoa: V1

- Defined sense: miss or long for someone absent.
- Required: subject:experiencer; object:-m (missed individual).
- Optional: none introduced.
- **Do not infer:** Missing someone does not automatically assert romance.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `wen mi ti-m wënoa.`.

### kërawë: V0

- Defined sense: try or make an attempt, with the action unspecified.
- Required: subject:attempter.
- Optional: none introduced.
- **Do not infer:** Attempting is not succeeding; no unspecified infinitival or do-complement frame is granted.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi kërawë.`.

### yëli: V0

- Defined sense: shine or emit visible light.
- Required: subject:light-emitting entity.
- Optional: none introduced.
- **Do not infer:** A literal glowing entity is not automatically a person or a metaphor for happiness.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen sa yëli.`.

### sharoni: V1

- Defined sense: need or require a thing.
- Required: subject:needer; object:-m (needed thing).
- Optional: none introduced.
- **Do not infer:** Need does not entail legal obligation; do not infer -du modality.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen mi kima-m sharoni.`.

### eri: V0

- Defined sense: exist or be present.
- Required: subject:existing entity.
- Optional: location:-lo.
- **Do not infer:** Existence is not interchangeable with every copula or possessive reading.
- Voice: active sense only; neither `-li` nor `-ru` is automatically licensed.
- Editorial model: `sen sa eri.`.


## Conformance

- The role marker `-m` indicates an object but **does not prove** its semantic class belongs with every verb. Use the sense-specific restrictions above.
- Keep `-tu` for a recipient and `-shi` for an actual instrument; do not substitute them for the target of another verb.
- All forms retain the existing resonance marker, stem spelling, tense, aspect and case-order rules.
- These 11 frames raise the **defined narrow core** from 25 to 36; the other existing verbs are neither deleted nor automatically generalized. Review the 8.4 generated 500-case ledger before declaring open-ended translation coverage.
- A separate independent comprehension test is needed before asserting that speakers find these conventional or natural.

---

## Edition appendix 8.5 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_5_ATTEMPT.md](../../docs/standard_8/AMENDMENT_8_5_ATTEMPT.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Qaroshi 8.5 · Attempted actions

This editorial extension adds a content-clause frame to `kërawë` (try), alongside its 8.4 unspecified-action frame. It uses the existing `do` boundary and does not change historical texts. These are designed examples, not observed speech.

## Form and meaning

`RESONANCE [SUBJECT ... PREDICATE do] SUBJECT kërawë` expresses an attempt by the matrix subject to bring about the embedded action. The embedded clause precedes the matrix subject and has an overt subject; both subjects must denote the same individual or group. The embedded clause has no independent resonance. Its predicate and arguments follow their own existing frame. Matrix tense, aspect, modality, and negation belong to `kërawë`; embedded negation belongs immediately before the embedded predicate. Use an explicit subject in each clause even if it is repeated.

* `sen mi naro-m rëgë do mi kërawë.` — I try to repair the dwelling. Neither repair nor success is asserted.
* `sen mi naro-m rëgë do mi nu kërawë.` — I do not try to repair the dwelling. This says nothing about whether repair happens.
* `sen mi nu shërami do mi kërawë.` — I try not to sleep. This does not assert that I stay awake.
* `sen mi naro-m rëgë do mi kërawë-te.` — I tried to repair the dwelling; the attempt is past, with no claim of success.

The embedded clause describes the intended action, not a reported fact. An embedded future tense does not itself imply success. A different embedded actor, passive or causative `kërawë`, an embedded question, and omitted subjects are outside this frame; use another documented construction rather than assume their interpretation. Ordinary pronouns can be ambiguous in context: repeat a clear nominal reference where needed. This extension does not establish a general complement frame for other verbs.

## Evidence and limits

The accompanying restricted checker and contrast tests cover four illustrated readings and malformed structures, not unrestricted Qaroshi or semantic compatibility. No independent comprehension or spontaneous use has been measured. The 8.4 ledger's 404 undrafted cases and 96 unverified drafts are unchanged; these examples are not a score on those challenges. Broader verb frames, reference tracking and independent review remain open.

---

## Edition appendix 8.6 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_6_EVERYDAY_MEANING.md](../../docs/standard_8/AMENDMENT_8_6_EVERYDAY_MEANING.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Standard 8.6 · Everyday actions and content

This edition adds 19 narrow active frames for new writing. They are editorial decisions based on the canonical dictionary and earlier controlled teaching sentences, not independent observations of speakers. The examples below retain their original source IDs; imperative subjects may be omitted under the existing grammar. These definitions neither replace earlier frames nor grant passive or causative forms. A source example can contain an adjunct that is not part of the defined frame.

V1 takes a subject and one `-m` object of the stated class. V0 has a subject and no expressed object in this sense. Omission of a V1 object is not licensed by this table. A V0 definition does not forbid a separately documented sense with an object. Normal tense, aspect, resonance and local `nu` rules apply; past does not mean completed or successful. Glosses and translations below identify the intended reading rather than all possible uses of a word.

| Lemma (dictionary ID) | Frame and object or subject class | Boundary | Existing teaching example and source |
| --- | --- | --- | --- |
| `holë` (Q001456) | V1: person thanked | Thanking does not imply repayment or agreement. | `hol mi ti-m holë.` — Thank you. (S00015) |
| `mëlë` (Q002303) | V1: person or thing liked | Liking does not imply romantic love. | `më mi ti-m mëlë.` — I like you. (S00031) |
| `mërali` (Q002309) | V1: person embraced | Permission to hug is not an actual hug. | `hë mi ti-m mërali-ho he?` — May I hug you? (S00032) |
| `këmiro` (Q001973) | V1: person or thing recalled | Remembering a person or thing does not assert that a proposition about it is true. | `lën mi ti-na meri-m këmiro.` — I remember your face. (S00036) |
| `ngëmiro` (Q002838) | V1: person or thing forgotten | Forgetting a person or thing does not assert that the person or thing has ceased to exist. | `më pëla mi-m nu ngëmiro ya.` — Please don't forget me. (S00039) |
| `dëmi` (Q000933) | V1: person assisted | Helping does not imply that the person succeeded. | `hol ti mi-m dëmi-te.` — You helped me, thank you. (S00040) |
| `rawëli` (Q003883) | V1: thing desired | Desire does not establish possession or receipt. | `sen mi këmi-m rawëli.` — I want food. (S00070) |
| `rëliwa` (Q004143) | V1: physical door, window or other opening | An opening action does not assert what goes through it. | `dal raro-m rëliwa ya.` — Open the door. (S00072) |
| `shëliroa` (Q004467) | V1: physical door, window or other opening | Closing does not entail locking. | `dal weru-m shëliroa ya.` — Close the window. (S00073) |
| `shëmiroli` (Q004493) | V1: thing washed with water | Washing does not entail that the object becomes completely clean. | `sen mi shëroa-m shëmiroli.` — I wash the blanket. (S00076) |
| `shëmiwa` (Q004496) | V1: thing shared | Sharing does not require every recipient to receive an equal portion. | `sen mi kërawëmi-m nu shëmiwa-yu.` — I won't share my password. (S00126) |
| `shënariwo` (Q004515) | V0: subject: waiter | Waiting does not entail that the expected event occurs. | `sen mi shënariwo-yu.` — I will wait. (S00071) |
| `shëruwi` (Q004628) | V0: subject: successful actor | The unspecified achievement is not identified by this frame. | `rëm mi shëruwi-te.` — I succeeded! (S00053) |
| `yënawë` (Q005989) | V0: subject: rising entity | Rising does not specify a destination. | `yë yela yënawë-se.` — The moon is rising! (S00092) |
| `rëmë` (Q004156) | V0: subject: counter | Counting does not identify what was counted. | `sen mi rëmë-se.` — I am counting. (S00131) |
| `ngëmë` (Q002842) | V0: subject: calculator | Calculating does not guarantee a correct result. | `hë ti ngëmë-ki he?` — Can you calculate? (S00132) |
| `rëmo` (Q004155) | V0: subject: celebrant | Celebrating does not specify the occasion. | `zha naru dëmaro-lo rëmo.` — We celebrate at the festival. (S00183) |
| `rënali` (Q004160) | V0: subject: dancer | Dancing does not imply a partner or audience. | `zha naru rënali.` — We dance together. (S00186) |
| `zhëmi` (Q006558) | V0: subject: understander | The understood content is unspecified in this frame. | `lën mi nu zhëmi.` — I don't understand. (S00017) |

## Belief and hope as content

The existing phrasebook supplies `sen sa goro-yu do mi shërawë.` (“I believe they will fly”, S00114) and `wen ti nëra do mi rënawë.` (“I hope you stay”, S00038). For these two **content-clause senses**, the explicit subject and finite predicate precede `do`; the matrix subject and predicate follow it. One initial resonance governs the sentence. The embedded clause is propositional content, not a second independently asserted sentence. The actors can differ. This rule adds no general permission for arbitrary verbs, nested content clauses, embedded questions or missing subjects.

* `sen sa goro-yu do mi shërawë.` — I believe they will fly. The belief itself does not establish flight or truth.
* `sen sa goro-yu do mi nu shërawë.` — I do not believe they will fly. This does not by itself say I believe they will not fly.
* `sen sa nu goro-yu do mi shërawë.` — I believe they will not fly. The negation is inside the content.
* `wen ti nëra do mi rënawë.` — I hope you stay. The hope does not establish that you stay or that I can cause it.
* `wen ti nëra do mi nu rënawë.` — I do not hope that you stay; this does not by itself say I hope you leave.
* `wen ti nu nëra do mi rënawë.` — I hope you do not stay. The negation is inside the content.

Matrix `nu` negates the attitude; embedded `nu` negates the embedded predicate. Matrix and embedded tense belong to their respective predicates. A future content clause describes a future event relative to its context; it does not imply that the event occurs. This content frame does not define the interpretation of a nominal object of either verb.

## Wanting to act

In addition to the thing-desired frame, new writing may use `RESONANCE [SUBJECT ... PREDICATE do] SUBJECT rawëli` for wanting to perform an action. Both overt subjects must denote the same individual or group, as in the 8.5 attempted-action frame. The embedded action is desired, not asserted; wanting it does not imply intending, trying, being able or succeeding. This extension does not define wanting another person to act, an embedded question, or arbitrary nested clauses.

* `sen mi naro-m rëgë do mi rawëli.` — I want to repair the dwelling.
* `sen mi naro-m rëgë do mi nu rawëli.` — I do not want to repair it; this alone does not mean that I want it to remain damaged.
* `sen mi nu shërami do mi rawëli.` — I want not to sleep; this does not assert that I stay awake.

The scope, overt-subject and tense rules of the 8.5 construction apply; ordinary pronouns may still need clarification in context. A restricted checker covers only overt pronoun subjects, one content boundary and the 8.4 core embedded predicates. It does not judge naturalness or meaning.

## Challenge review and limits

Six existing challenge drafts (QS81-0001–0003 and QS81-0006–0008) now have the required narrow wash or close frame and explicit editorial review records in `data/standard_8/challenge_reviews_8_6.json`. They cover affirmative, locally negated and polar-question versions of two past events. These are still unverified candidates, not independent back-translations or a demonstrated success rate. The reported-speech and counterfactual variants remain open. The frozen 8.4 ledger's 96 drafts and 404 undrafted targets are unchanged. Independent comprehension, discourse, many other verbs and open-domain translation remain untested.

---

## Edition appendix 8.7 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_7_PRODUCTIVE_ACTIONS.md](../../docs/standard_8/AMENDMENT_8_7_PRODUCTIVE_ACTIONS.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# 8.7: productive everyday actions

This editorial addition records 97 further active V1 uses, each anchored to an existing dictionary verb and an existing editorial example with an overt `-m` object. They extend the 8.4 and 8.6 overlays without changing earlier entries or frozen baselines. The source examples are constructed editorial material, not independently observed speech.

## Using these frames

In the restricted model `RESONANCE SUBJECT OBJECT-m [nu] VERB`, the subject is the participant performing or experiencing the action and the object is the participant or thing in the listed role. Existing tense, aspect, modal and tender suffixes may compose in the standard order. `nu` immediately before the predicate negates the action; final `he` marks a polar question. An overt noun plural precedes case (`-ri-m`). For example:

* `sen mi shiwaro-m khukhiri.` — I encrypt a message (source S00251).
* `sen ti shiwaro-ri-m nu khukhiri-yu he?` — Will you not encrypt messages? This is a newly composed editorial example; the negative question does not assert encryption.
* `sen mi shërawëlon-m khungëmi-te.` — I saved a file. The file need not have a separate backup.

Each role below is a narrow characterization of its source example, not permission for arbitrary objects of the same general kind. The dictionary gloss “book a ticket” and the existing example “book a flight” differ in specificity; the flight example is retained with that limitation, without asserting every travel reservation is licensed. Where the dictionary word describes a successful result, negating that verb does not say whether an attempt occurred. These entries do not add passive, causative, recipient, instrument, or complement permissions. They do not assert a time, result, or actor beyond the sentence's grammar and lexical meaning.

The `tools/stress87/validate.py` checker recognizes only a transparent subset: an overt pronoun subject, one dictionary noun or pronoun object (optionally plural), one of these predicates, optional local negation, optional `he`, and a restricted suffix sequence. Its match means **form only**: it does not check the object role, truth conditions, translation, naturalness, or wider grammar. A sentence outside this subset is not thereby ungrammatical. In particular it does not analyze noun subjects, omitted hyphens, other grammatical roles, or arbitrary embedding.

## Source-linked roles and limits

The full source sentence, dictionary IDs and translation are preserved in [the machine-readable overlay](../../data/standard_8/valency_overlay_8_7.json). Boundaries describe what is *not* entailed; they are not additional claims about what happened.

| Verb | Dictionary gloss | Example object role | Boundary | Source |
| --- | --- | --- | --- | --- |
| `shëroli` | translate; carry meaning between languages | language or material translated | Translation does not guarantee accuracy or identify the target language. | S00133 |
| `khushësi` | install software | software installed | Installation does not guarantee that the software runs correctly. | S00236 |
| `bozilu` | reset a password | password reset | Resetting does not imply that the account is secure. | S00241 |
| `khukhiri` | encrypt | message encrypted | Encryption does not guarantee that the recipient can decrypt the message. | S00251 |
| `khungëtu` | decrypt | message decrypted | Decryption does not imply that its contents are true. | S00256 |
| `khuwohu` | open a file | file opened | Opening a file does not imply that it was read or edited. | S00261 |
| `khungëmi` | save a file | file saved | Saving does not imply that a backup exists elsewhere. | S00266 |
| `khuwëshu` | rename a file | file renamed | Renaming does not imply that its contents changed. | S00271 |
| `khungëgu` | delete a file | file deleted | Deletion does not imply that all copies have disappeared. | S00276 |
| `khuziru` | restore a file | file restored | Restoring a file does not imply that it is complete or correct. | S00281 |
| `khuziqu` | copy a file | file copied | Copying does not imply that the original was removed. | S00286 |
| `khunikhu` | archive data | file archived | Archiving does not imply that the file is permanently retained. | S00291 |
| `khupizhi` | search a folder | folder searched | Searching a folder does not imply that the sought item was found. | S00296 |
| `khugëhi` | compile | source code compiled | Compilation does not imply that the program is correct. | S00301 |
| `khurëni` | review code | source code reviewed | Review does not imply approval or the discovery of every defect. | S00306 |
| `beqishi` | diagnose a fault | software fault diagnosed | Diagnosis does not imply repair. | S00316 |
| `khurëngi` | test software | software release tested | Testing does not prove that the release is defect-free. | S00321 |
| `khukhëmi` | benchmark | computer benchmarked | Benchmarking does not imply that the computer is fast. | S00326 |
| `khuseru` | configure | router configured | Configuration does not guarantee connectivity or security. | S00336 |
| `bowewi` | host a server | server hosted | Hosting does not imply that the server is publicly accessible. | S00341 |
| `khushëzu` | restart | server restarted | Restarting does not imply that a fault was fixed. | S00346 |
| `borumu` | filter packets | network packets filtered | Filtering does not by itself say which packets are allowed. | S00351 |
| `khuzhaqi` | query a database | database queried | A query does not guarantee a useful result. | S00356 |
| `khubezi` | restore data | backup restored | Restoration does not prove the backup was complete. | S00361 |
| `deqori` | edit a photo | photograph edited | Editing does not imply publication or permission to publish. | S00371 |
| `denuzu` | review a film | film reviewed | Reviewing does not imply a favorable judgment. | S00381 |
| `deraru` | publish a book | book published | Publication does not imply that anyone has read the book. | S00386 |
| `demamu` | listen to music | music listened to | Listening does not imply liking or understanding. | S00391 |
| `deqëqi` | publish a song | song published | Publication does not imply that anyone has heard the song. | S00396 |
| `demënu` | create art | painting created | Creating does not imply exhibiting or selling the painting. | S00401 |
| `deseri` | critique art | artwork critiqued | Critique does not imply a negative judgment. | S00406 |
| `demomu` | tell a story | story told | Telling a story does not assert that it is true. | S00411 |
| `deqoyi` | read poetry | poetry read | Reading does not imply memorization or agreement. | S00416 |
| `subimu` | cite a source | research paper cited | Citation does not imply endorsement or verification. | S00421 |
| `ngigamu` | investigate | research question investigated | Investigation does not guarantee an answer. | S00426 |
| `sugënu` | test a prediction | hypothesis tested | Testing does not imply confirmation. | S00431 |
| `zohowi` | verify a calculation | calculation verified | Verification does not specify the method used. | S00436 |
| `zoshëzu` | reduce a fraction | fraction reduced | Reduction does not specify the representation used. | S00446 |
| `zosuqi` | solve an equation | equation solved | Solving does not identify the solution. | S00451 |
| `zomunu` | check a proof | proof checked | Checking does not assert that the proof is valid. | S00456 |
| `surashu` | publish research | research paper published | Publication does not establish the truth of its claims. | S00466 |
| `bemati` | measure precisely | pressure measured | Measurement does not give a value or unit by itself. | S00476 |
| `sunaku` | measure temperature | temperature measured | Measurement does not give a value or unit by itself. | S00481 |
| `zosozhu` | measure an angle | angle measured | Measurement does not give a value or unit by itself. | S00486 |
| `zohoyi` | measure an area | area measured | Measurement does not give a value or unit by itself. | S00491 |
| `guselu` | measure blood pressure | blood pressure measured | Measurement alone does not establish a diagnosis. | S00496 |
| `gusulu` | alleviate symptoms | symptoms alleviated | Alleviation does not imply that their cause is cured. | S00501 |
| `gushëqi` | clean a wound | wound cleaned | Cleaning does not imply that the wound has healed. | S00506 |
| `gunayi` | bandage a wound | wound bandaged | Bandaging does not imply that the wound has healed. | S00511 |
| `guhini` | prescribe medication | medicine prescribed | Prescribing does not imply that medicine was taken. | S00516 |
| `gusuru` | care for a patient | patient cared for | Care does not guarantee recovery. | S00521 |
| `guqaki` | examine medically | patient examined medically | Examination does not itself provide a diagnosis. | S00526 |
| `kerodu` | reassure | person reassured | Reassuring someone does not establish that all danger has gone. | S00541 |
| `mëli` | comfort; soothe | person comforted | Comforting does not guarantee relief. | S00546 |
| `keguyi` | respect | person respected | Respect does not imply agreement with every decision. | S00551 |
| `ketangi` | respect boundaries | boundary respected | Respecting a boundary does not imply the boundary is permanent. | S00561 |
| `keshobu` | accept an invitation | invitation accepted | Acceptance does not imply that attendance occurred. | S00566 |
| `kezhingu` | decline an invitation | invitation declined | Declining an invitation does not imply hostility. | S00571 |
| `wenganu` | enact policy | policy enacted | Enactment does not imply effective implementation. | S00586 |
| `wemomi` | repeal a law | law repealed | Repeal does not establish whether prior conduct was lawful. | S00591 |
| `werëhi` | elect | candidate elected | Election does not imply that the candidate has taken office. | S00596 |
| `wewëtu` | organize a protest | protest organized | Organizing does not imply that the protest took place. | S00606 |
| `sebilu` | convert currency | currency converted | Conversion does not specify an exchange rate. | S00611 |
| `sezhikhi` | save money | money saved | Saving does not specify an amount or guarantee safety. | S00616 |
| `serepu` | spend money | money spent | Spending does not imply that the purchase was worthwhile. | S00621 |
| `seropi` | repay | loan repaid | Repayment does not itself say who lent the money. | S00626 |
| `senëni` | refund | purchase refunded | A refund does not imply that the original payment was fraudulent. | S00631 |
| `semawu` | negotiate price | price negotiated | Negotiation does not imply agreement. | S00646 |
| `rezhisi` | drive | car driven | Driving does not imply arrival at a destination. | S00661 |
| `relapi` | rent a car | car rented | Renting does not transfer ownership. | S00666 |
| `luditu` | climb a mountain | mountain climbed | Climbing does not by itself identify the route taken. | S00676 |
| `lurezhu` | cross a river | river crossed | Crossing does not specify the means of travel. | S00681 |
| `repoqu` | cross a road | road crossed | Crossing does not specify whether a marked crossing was used. | S00686 |
| `reshuli` | navigate a route | route navigated | Navigating does not imply arrival on time. | S00696 |
| `reweshu` | book a ticket | flight booked | The source applies the ticket-booking verb to a flight; booking does not imply that the flight occurred. | S00701 |
| `retëku` | reserve a seat | seat reserved | Reserving does not imply that the seat was used. | S00706 |
| `tëpopu` | clean a house | house cleaned | Cleaning does not imply every part is spotless. | S00711 |
| `tënipi` | tidy a room | room tidied | Tidying does not imply washing or disinfection. | S00716 |
| `tëhakhi` | paint a wall | wall painted | Painting does not specify its color. | S00721 |
| `tëdiru` | assemble furniture | furniture assembled | Assembly does not imply that it is sturdy. | S00726 |
| `tënisi` | make a bed | bed made | Making a bed does not imply that anyone slept in it. | S00731 |
| `gizuku` | wash clothing | clothing washed | Washing does not imply that the clothing is dry. | S00736 |
| `giburi` | polish shoes | shoes polished | Polishing does not imply that the shoes were repaired. | S00741 |
| `gireru` | sew | shirt sewn | Sewing does not specify who will wear the shirt. | S00751 |
| `nëshongu` | prepare a meal | food prepared | Preparing food does not imply that it was eaten. | S00756 |
| `zhalëwa` | cook; heat food to prepare it | meal cooked | Cooking does not imply that the meal was eaten. | S00761 |
| `nëkati` | follow a recipe | recipe followed | Following a recipe does not guarantee a successful dish. | S00766 |
| `nëqobi` | measure ingredients | ingredient measured | Measurement does not state a quantity. | S00771 |
| `nëgegi` | peel a vegetable | vegetable peeled | Peeling does not imply that it was cooked. | S00776 |
| `ngidoti` | submit homework | assignment submitted | Submission does not imply acceptance or a passing grade. | S00791 |
| `ngirihi` | pass an exam | exam passed | Passing does not imply a perfect score. | S00801 |
| `ngihuzhi` | fail an exam | exam failed | Failure does not identify the reason or score. | S00806 |
| `deshemu` | write poetry | poem written | Writing does not imply publication. | S00821 |
| `nguyeqi` | groom wings | wing groomed | Grooming does not imply medical treatment. | S00826 |
| `ngukeri` | guard a nest | nest guarded | Guarding does not guarantee that no harm occurs. | S00831 |
| `ngupiqu` | repair wing membrane | wing membrane repaired | Repair does not specify the technique used. | S00836 |
| `ngumawi` | share a roost | roost shared | Sharing does not imply equal ownership. | S00846 |

## Measurement and limits

`python tools/stress87/benchmark.py` reports recognition of the 97 source examples and transparent positive and negative forms generated from those same examples. These checks exercise suffix order, case forms, negation and questions, but are not held out, are not a semantic accuracy measurement and do not demonstrate independent learner comprehension. The earlier 404 undrafted challenges and unreviewed senses remain open; this release does not claim the language is complete or independently attested.

---

## Edition appendix 8.8A (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_8_SEMANTIC_PRODUCTIVITY.md](../../docs/standard_8/AMENDMENT_8_8_SEMANTIC_PRODUCTIVITY.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Standard 8.8: bounded semantic productivity, reported sources, and contrastive roles

**Status:** newly adopted editorial constructions, **not** independent human attestation. They extend the 8.4, 8.6 and 8.7 narrow senses. The 7.0 lexical baseline, 8.0 grammar, 8.1 embedded-polar amendment, script and preexisting corpus are preserved verbatim.

This amendment responds to the **actual 500-challenge stress set**, not generic sentence templates invented after seeing an evaluation score. The fixed English prompts are in `data/stress81/challenges_500.csv`. The reproducible proposed Qaroshi versions and truth-condition checklist are generated by `python tools/stress88/compose.py` into `data/stress88/case_evidence_500.csv`.

## 1. Indirect reported speech: a *person told me P*

The earlier grammar's `P do SUBJECT shiri-te` construction reports propositional content without independently asserting P. Here we license the precise extended **reported-source and recipient frame**, restricted to a declarative proposition and the speech predicate `shiri`:

`RESONANCE P do yano mi-tu shiri-te.`

Here `P` contains an overt subject and licensed predicate, `yano` is **an unspecified person** (not automatically a group or a named source), and `mi-tu` is **the speaker as addressee**. Thus the outer sentence commits to someone telling the speaker that P, but **does not commit to P being true or witnessed**. Do not use mere evidential `hu` in place of `mi-tu`: reported evidence alone does not identify who received the message. Do not put a second resonance on the embedded proposition.

* `sen nënugo gëla-m shëmiroli-te do yano mi-tu shiri-te.` = I was told that the cook washed the bowl.
* `sen shuna tëzhoza-m shëliroa-te do yano mi-tu shiri-te.` = I was told that the neighbor closed the gate.
* `sen taru ngibeko-m zhiseti-te do yano mi-tu shiri-te.` = I was told that the child hid the notebook.

**Counterexample:** `sen taru ngibeko-m zhiseti-te si.` asserts witnessing the action rather than the fact of being told; it is **not** a valid paraphrase for the third example.

This is an editorially defined construction for `yano` as indefinite source and `mi-tu` as recipient. A different speaker, addressee, embedded question, negative report, or nested quotation requires its own review. No automatic promotion of all forms of `shiri` is implied.

## 2. Five newly licensed everyday senses and professional roles

Existing canonical spellings and historical senses remain unchanged. These are deliberately adopted **editorial constructions** with the following exact senses and role limitations. A historical specialized sense does not automatically license these extensions: the new usage is explicitly stated here.

| English scenario | Existing root(s) used | New narrowly declared meaning |
| --- | --- | --- |
| Musician packs an instrument | `rewoti` (Q004079), `pëyingo`, `kidishitë` | `rewoti` (historically “pack luggage”) may take a musical instrument as the item packed for transport |
| Gardener waters seedlings | `tëzhida` (garden), `pëli` (give), `zerëzhika` (seedlings), `kima` (water) | `tëzhida-mi` is a gardener professionally tending a garden; the *recipient* seedlings take `-tu`, actual water transferred takes `-m`, followed by `pëli` |
| Child hides notebook | `zhiseti` (Q006472), `taru`, `ngibeko` | `zhiseti` (historically “hide a feeling”) newly licenses concealment of a physical notebook |
| Shopkeeper counts coins | `sebenga` (merchant), `rëmë` (count), `setola` (coin) | New retail-shopkeeper reading of `sebenga`; `rëmë` gains V1 coin-counting, with plural `setola-ri-m` |
| Traveler loses ticket | `gura` (travel), `shënami` (lose), `renguqa` (historically transport ticket) | `gura-mi` derives traveler; `renguqa` gains an editorial broad **ticket-credential** sense (entry, service or transport ticket), leaving its transport-specific sense intact |

The `-mi` occupation derivation follows the productive action/role morphology already defined in the consolidated grammar. It does not mean every person associated with a garden is automatically professionally employed as a gardener; that is the **new narrowed occupational sense** in this construction. The `-sharo` derivation below identifies a trained practitioner or specialist of a verb-root activity.

Examples in new 8.8 usage:

| English target | Full Qaroshi editorial candidate |
| --- | --- |
| The musician packed the instrument. | `sen pëyingo kidishitë-m rewoti-te.` |
| The gardener watered the seedlings. | `sen tëzhida-mi zerëzhika-tu kima-m pëli-te.` |
| The child hid the notebook. | `sen taru ngibeko-m zhiseti-te.` |
| The shopkeeper counted the coins. | `sen sebenga setola-ri-m rëmë-te.` |
| The traveler lost the ticket. | `sen gura-mi renguqa-m shënami-te.` |

Negative versions put `nu` immediately before the predicate. Questions use initial question resonance and the matrix `he?`. An indirect report of one of these propositions uses the *full source+recipient* construction in section 1 and does not assert that proposition is true. No passive or causative for these five action senses is licensed here.

**Semantic limits:** “water” is an event of delivering actual water to seedlings, not a promise that they thrive; “count” does not imply correct total; “hide” does not guarantee permanent invisibility; “pack” does not imply arrival. The new ticket-credential sense is a **language design decision**, not a claim that every historical use of `renguqa` already meant every kind of ticket. If “ticket” means a police citation rather than access or service credential, the translation needs a separate sense.

## 3. Nine exact passive and instrument licenses

The earlier standard requires a verb-specific voice license, not generic `-li` for every verb. This edition adopts **nine specified active/passive roles**. It establishes new lexical-sense and participant-class rules. Individual English sentence challenges can be composed only when all the roles really are the ones shown here.

| Root | Licensed actor | Licensed patient | Licensed instrument (if any) |
| --- | --- | --- | --- |
| `rëgë` repair | `regaro` mechanic | `pënaro` engine | `bebëyo` wrench |
| `ngigoyi` clean an appliance | `nëbihu-sharo` baker | `tëkuta` oven | `gëruza` cleaning brush |
| `debokhu` paint | `tëzhida-mi` gardener | `tëgaba` fence | *no particular roller licensed* |
| `bekedu` calibrate | `pëyuzha` technician | `bengeka` sensor | not specified |
| `tëmengi` decorate | `pëkhëba` artist | `ngëroa` wall | not specified |
| `khuziqu` copy a document | `khunikhu-sharo` archivist | `zonësongi` document | `khukhodo` scanner |
| `shëruwawe` alter | `gizuwa` tailor | `gikhoto` coat | `gibika` needle |
| `shëmiroli` wash | `rezhago` driver | `yarowe` vehicle | *no particular hose licensed* |
| `pasizo` secure | `zashëzhena` worker | `raro` door | *no particular steel lock licensed* |

Professional actors are derived only where justified: `nëbihu` (bake) + `-sharo` (specialist) for baker, and `khunikhu` (archive) + `-sharo` for archivist. The garden role above uses a separately declared occupational sense. A `-sharo` derivation is not an assertion about a particular individual's qualifications.

For each exact role set the grammar now permits:

* `sen ACTOR PATIENT-m VERB-te.` Active past action.
* `sen PATIENT ACTOR-za VERB-li-te.` Passive with the actual actor identified. **`-za` is the agent, not `-shi`.**
* `sen ACTOR PATIENT-m INSTRUMENT-shi VERB-te.` Active action performed with an explicitly licensed physical tool **only when listed**.
* `sen ACTOR PATIENT-m nu VERB-te.` Negative past assertion, not proof of attempted action.
* `hë PATIENT ACTOR-za VERB-li-te he?` Passive polar question with the agent inside question scope.

The instrument in the English stress prompts is often more specific than the root available in the historical lexicon. Unsupported instrument versions are therefore **not counted**: a “painting implement” is not necessarily a roller, and a “fastening tool” is not necessarily a steel lock. Likewise, securing a door via `pasizo` does not prove it is locked, and cleaning an oven does not establish sterilization. Prior unrelated patient classes are not silently generalized.

## 4. Closing the focus-plus-now exception

The 8.1 stress test previously left `QS81-0155` unresolved because it includes **exclusive noun-phrase focus** and a **present time adjunct**:

`sen dëna qaro ngëshi nëna haro.`

Meaning: **Only this Nardoragon is well right now.**

`dëna qaro ngëshi` restricts the chosen Nardoragon NP among individuals. `nëna` locates well-being at the current reference time. The sentence does **not** mean “this Nardoragon is well only now,” nor “this Nardoragon is only well,” because the exclusive focus is attached to the NP rather than the time or predicate. The source lexicon and grammar already document `qaro`, `haro`, `dëna`, `ngëshi`, and `nëna`; this edition certifies their particular composition as a new **editorial candidate**, not a speaker-confirmed sentence.

## 5. Scope, contrasts and unfinished challenges

For each of the ten original semantic domains, the generator now records a separate five-way list of **required meaning components** (reported sources, chronological ordering, permission vs ability, counterfactual result, patient vs instrument, metaphor vs literal assertion, scientific inference, etc.). Every one of the 500 prompts gets a row, whether or not a candidate exists. Source gaps are never hidden by truncating an English clause.

The 8.8 output expects **135 complete editorial candidate strings** (96 previously proposed plus 39 new) and **365 without any complete draft**. The 22 previously drafted selected voice/valency examples receive a new narrow explicit role license and **18 additional voice/valency candidates** cover previously undrafted challenges. The three revised inherited reported-information candidates retain their historical provenance. New everyday senses add 20 full editorial candidates and the present-time quantifier composition adds one. This is additive candidate coverage, not a reader-rated validity score.

**Human comprehension results: zero.** The proposed candidates may still need sense disambiguation or correction. The other 365 challenges remain open. The existence of formal tests shows consistency with the editorial specification, not full natural-language proficiency or truth-conditional equivalence measured by independent readers.

## 6. Exact-pattern semantic scope checker

The machine-readable validator `tools/stress88/scope.py` is a **restricted exact-pattern scope interpreter** for the new 8.8 examples. It preserves actor/patient distinction, specialized recipient vs direct-object roles, passive agent `-za` vs instrument `-shi`, matrix question versus assertion, and assertion of *telling that P* versus assertion of P. For one edited example, it rejects a string rather than projecting arbitrary meanings onto a familiar affix sequence.

Try `python -m tools.stress88.scope "sen taru ngibeko-m zhiseti-te."`. The output is **not** a general Qaroshi parse, a proof of English equivalence, or independent reader testimony. Exact mismatch results are deliberately reported as outside this specific checker, not ungrammatical.

## Reproduction and integrity

```sh
python tools/stress88/compose.py
python -m unittest tests.test_standard_8_8 -v
python -m unittest discover -s tests -q
```

Outputs are generated under the ignored `data/stress88/` directory; never overwrite the frozen baseline CSVs or archival manifests to make a score improve. Preserve all earlier contributors' files and preserve the separate independently-run comprehension gate.

---

## Edition appendix 8.8B (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_8_TEMPORAL_SCOPE.md](../../docs/standard_8/AMENDMENT_8_8_TEMPORAL_SCOPE.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Qaroshi 8.8 · Two-event temporal clause scope

This amendment clarifies the **already documented** `ana` (after), `ëna` (before), `yaro` (when/while), and `torëne` (until endpoint) clauses without adding any new alphabet symbols, altering any historical dictionary entries, or claiming naturalistic validation.

## Event-ordering template

For precision writing, when the subordinate clause is explicitly introduced before the main clause, use:

`RESONANCE CONNECTIVE SUBORDINATE-SUBJECT ... SUBORDINATE-PREDICATE, MATRIX-SUBJECT ... MATRIX-PREDICATE.`

Only one opening resonance applies to the entire sentence. No second register is introduced after the comma. Both finite predicates retain their own independent tense, aspect, negation, and case roles. The connective determines the relation of the *matrix* event to the *subordinate* event:

| Connector | Relation between events | Restricted illustrative example |
| --- | --- | --- |
| `ana` | Matrix happens **after** subordinate | `sen ana sa goro-te, mi nëru-te.` = After they flew, I rested |
| `ëna` | Matrix happens **before** subordinate | `sen ëna sa goro-te, mi nëru-te.` = Before they flew, I rested |
| `yaro` | Matrix overlaps subordinate in time | `sen yaro sa goro-te-se, mi nëru-te-se.` = While they were flying, I was resting |
| `torëne` | Matrix state holds up to a specified endpoint | `sen torëne sa goro-te, mi nu nëru-te.` = I did not rest until they flew, without asserting that I rested afterward |

These illustrate **a reusable grammatical construction** using existing documented verb roots and arguments. They do not by themselves translate the stress test's arbitrary couriers, bridges, ferries, captains, and instruments. Those still need their own lexical frames and source-verified event descriptions.

## Semantics that must survive translation

- **After** cannot be replaced with **before** without reversing the event ordering. Both clauses have their own subjects; switching them changes the truth conditions.
- **While** is an overlap relation, not necessarily simultaneous beginning or simultaneous ending. The restrictive examples use progressive `-se` in both clauses to make overlap explicit. Other event shapes require further sense-specific review.
- **Negative until** is particularly hazardous. An English `not P until Q` often suggests that P happened after Q, but that is not guaranteed by the bare restricted Qaroshi scope. State the later positive P in another clause if it is an asserted fact. Do not infer that Q caused P.
- **Tense** `-te` is past relative to its clause's reference time, not evidence that one clause was completed *because* of the other. Aspect `-mo` would mark completion explicitly where licensed.
- **Questions** about ordering need documented matrix-question scope. The new restricted recognizer does not accept them, so the unsolved question variants in the original challenge set are not silently promoted.

## Machine check and limits

`python -m tools.stress88.temporal "sen ana sa goro-te, mi nëru-te."`

The checker accepts only overt subject pronouns `mi`, `ti`, or `sa`, three already-established intransitive verbs (`goro`, `nëru`, `shërami`), two finite time suffixes, a narrow range of aspect suffixes, and a two-clause sentence with the specified boundary punctuation. It rejects unrecognized forms instead of guessing. It is **not** a general Qaroshi parser, has no human comprehension evaluations, and does not establish whether a particular invented conversation sounds natural.

The stress test remains **135 unverified candidate strings out of 500** with 365 prompts lacking full candidates. This construction improves the language specification but deliberately does **not** increase that count without properly translated lexical participant/event frames.

---

## Edition appendix 8.9 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_8_9_EVENT_COMPOSITION.md](../../docs/standard_8/AMENDMENT_8_9_EVENT_COMPOSITION.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Qaroshi 8.9: compositional meaning, evidence, and truth conditions

**Status:** editioned editorial language decisions and audit materials. These are not attested native-speaker grammar, independent back-translations, or a general English↔Qaroshi translator. They extend the previous 8.0–8.8 material while keeping all frozen lexical, example, glyph and release-manifest baselines unchanged.

The original challenge texts are fixed in `data/stress81/challenges_500.csv`. The new reproducible outputs are in `data/stress89/case_evidence_500.csv` and `composition_summary.json` after running `python tools/stress89/compose.py`. Count **complete editorial candidate sentences**, not validated meaning equivalents. A candidate is not counted when a participant, tense scope, material instrument, lexical referent or proposition is missing.

## I. Source-licensed event propositions can combine with knowledge, reporting and evidence

For one individually licensed finite proposition `P`, a writer may use:

| Construction | Event/knowledge entailment | Example using the existing server/restart roots |
| --- | --- | --- |
| `sen P si.` | Speaker directly witnessed P, presents P as occurring | `sen khuzhaso khushëzu-te si.` |
| `sen P do yano mi-tu shiri-te.` | Someone told the speaker that P, but P is not asserted true by that report | `sen khuzhaso khushëzu-te do yano mi-tu shiri-te.` |
| `sen P ye.` | Speaker presents P as inferred, not directly seen; grounds and certainty may be contextual | `sen khuzhaso khushëzu-te ye.` |
| `sen P he do mi nu sëmi.` | Speaker does not know **whether** P, not “knows P did not occur” | `sen khuzhaso khushëzu-te he do mi nu sëmi.` |
| `sen P do mi nu shërawëhu.` | Speaker **does not assert** P; says nothing about whether P is actually true or false | `sen khuzuha zhimabu-te do mi nu shërawëhu.` |

These templates compose prior `si`/`ye`, 8.1 `he do`, 8.8 recipient-marked reporting, and a new **restricted content-claim sense** of `shërawëhu` (“report/tell information”). The fifth form explicitly negates the **matrix assertion act**, not the embedded event. `sen P do mi shërawëhu-te` is a report of P and is NOT licensed by this amendment as a universal synonym for objective truth. A passive event inside P cannot be generated unless the particular lexical sense licenses that passive.

The following exact event frames receive new explicitly limited senses; the structured source words and dictionary IDs are preserved in `data/standard_8/evidential_propositions_8_9.json` and `epistemic_nonassertions_8_9.json`:

- `khuzhaso khushëzu-te`: a server restarts (new inchoative V0, not proof that recovery succeeded).
- `pëqukho pëqukho-na morushira-m shëruwawe-te`: the witness changed **their own** story (specific co-reference of repeated witness role in this frame, not general permission to equate any two NPs).
- `taru shi-m këroli-te`: the child recognized the voice (auditory identification; no assertion that the child was correct).
- `përuyo rëmëra-m wuzëwu-te`: the scientist repeated the **measurement procedure**, not necessarily its numerical result.
- `waroho noha-m retibu-te`: an animal crossed a physical boundary. This is an explicitly **new inclusive-zoological** sense of `waroho` and physical-perimeter sense of `noha`, not a silent rewrite of the older “non-sentient creature” and permission-boundary meanings.

Seven more events receive narrowly documented “I am not claiming P” frames. For example `sen kheriniyu wusëngu-li-te do mi nu shërawëhu.` does **not** assert that the meeting was canceled, whereas `sen kheriniyu nu wusëngu-li-te.` would negate cancellation. The two forms must not be interchanged.

## II. Fully scoped multi-event order

Edition 8.9 permits a **restricted polar question about before-order**:

`hë ëna SUBORDINATE-PROP, MATRIX-PROP he?`

The final `he?` takes scope over the proposed event ordering; the preposed `ëna` clause does not independently ask a question. This is distinct from an embedded `he do` complement. It is only extended to frame-licensed event propositions; nothing here licenses arbitrary passive senses or omitted referents.

Likewise `ana` marks matrix-after-subordinate and `yaro` overlap. The new canonical scenario bindings are recorded in `motion_frames_8_9.json`: crossing a river followed by bridge inspection, boarding a ferry before fog clears, and museum visitors entering before an exhibition begins or after doors open. The set includes **unresolved** negative-until cases deliberately, because `not until` can imply a later positive event that the bare endpoint marker `torëne` does not assert. Do not add that event silently to achieve superficial benchmark coverage.

Newly adopted lexical meanings here are narrow: `rikanga` can be a general courier (historically inter-roost), `qumoki` can inspect a bridge as a structure, and `wuzhagi` can describe a storm ending. `pësënga` can refer to a tourist as a leisure visitor at a museum, and inchoative door-opening and exhibition-beginning are licensed for the listed source roots. Those editorial choices are testable rules rather than evidence that speakers already use them.

## III. Contrafactual anaphora and exact participants

A counterfactual past antecedent introduced by `wënu` is treated as nonactual, and its projected consequent ends with `qinë`. Both clauses keep distinct roles and previous-time morphology. This edition explicitly licenses:

- `sen wënu nënugo gëla-m shëmiroli-te, dëra gëla-m pënari-te qinë.` = If the cook had washed the bowl, the guest would have used it. Repeating `gëla` makes the English **it** refer to the same bowl.
- `sen wënu shuna tëzhoza-m shëliroa-te, zemobo këna-lo nëra-te qinë.` = If the neighbor had closed the gate, the dog would have stayed inside. `këna-lo` names a deictic interior without inventing a specific room or house.

The hypothetical consequent is **not** an assertion about what actually happened. Do not equate `-te` with completed success or `-yu` alone with a counterfactual.

## IV. Instruments, agents, and exact roles

The separate `conditional_and_voice_8_9.json` licenses a specialized table-assembly carpenter frame built with `tëdiru-sharo` (trained furniture assembler) and `nama` (table). It also licenses an ordinary water hose as the physical tool `qoheku-shi` in the specific vehicle-washing example. In a passive, `-za` still marks the real agent; in an active instrumented action, `-shi` marks the tool. Neither suffix may substitute for the other. No general passive or generic tool license follows from these examples.

## V. Meaning audit of the inherited 135 drafts

`python tools/stress89/audit.py` generates **all 500 structural audit records** and a **135-item Qaroshi-only blind packet** with a separate answer key. Its checks deliberately distinguish:

- exact restricted model matches (evidence of local structure, not truth-conditional equivalence),
- limited quantifier-rule matches,
- candidates requiring deeper manual sense review,
- concrete review flags, and
- missing draft proposals.

The inherited 8.8 review identifies three specific source-reporting risks: `QS81-0202`, `QS81-0222`, and `QS81-0227`. The newer 8.9 drafts replace their ungrounded or underspecified hearsay descriptions with **`do yano mi-tu shiri-te`**, naming an indefinite source and the first-person recipient. The historical versions stay in `prior_8_8_candidate` so the correction is auditable.

These reviews are not independent human back-translations. **No participant has been recruited, scored, or claimed.** The answer key cannot be given to a blind respondent, and a reviewer should record literal English, grammatical roles, lexical disagreements, comprehension confidence and whether the original English entails anything absent from the Qaroshi.

## VI. Consent, refusal, and offered-action content (8.9)

Eight explicitly delimited everyday permission-action frames now extend the adopted question and speech forms. They are defined in [`consent_action_frames_8_9.json`](../../data/standard_8/consent_action_frames_8_9.json), with stable lexicon IDs, actor and recipient roles, and narrow action senses. **Consent is a meaningful action by the consenting party; an attempt to ask for permission is neither permission nor consent.**

The three permitted constructions are:

| Meaning | Restricted template | Truth conditions |
| --- | --- | --- |
| A asks B whether A may P | `sen A [OBJECT]-m VERB-ho he do A B-tu sharoa-te.` | The request occurred; no answer or permission asserted. `he` is the *embedded* polar operator immediately before `do` |
| B explicitly refuses when A asks whether A may P | `sen yaro A [OBJECT]-m VERB-ho he do A B-tu sharoa-te, B toru «nu.» shiri-te.` | A permission request and B's explicit “no” occurred. The direct quoted `nu.` is a **fragment**, not a complete new sentence with an omitted resonance |
| A offered to P and B declined | `sen A [OBJECT]-m VERB do A B-tu pëli-te nao B noharo-te.` | A proposed an action to B, then B declined. `pëli` acquires a restricted **propositional offer-to-act** frame; `noharo` is licensed as an intransitive refusal of the immediately preceding offer |

These are **new editorial grammar licenses** for listed action frames, *not* an assertion that every verb or any grammatical-looking quoted fragment works in the same construction. For families that involve goal `-gu` rather than object `-m`, retain that role. The actor in the embedded action remains the requester/offerer; the addressee stays the person who may refuse. The offer form does not assert the proposed action occurred. The refusal construction does not assert that a refusal was respected, or that a prior broader consent was withdrawn. Silence is never accepted as evidence of agreement.

Examples:

- `sen ruwa relomo-m sezhoshi-ho he do ruwa pësënga-tu sharoa-te.` = The host asked the visitor whether the host could borrow the bicycle. **Question, not consent.**
- `sen yaro mara tikashë-m shëmiwa-ho he do mara shuna-tu sharoa-te, shuna toru «nu.» shiri-te.` = The neighbor said no when the friend asked whether the friend could share the photograph.
- `sen përoda shiraro-m khunginu do përoda pëpuwo-tu pëli-te nao pëpuwo noharo-te.` = The organizer offered to record the conversation, but the volunteer declined.

The eight source-anchored actor/action pairs are host borrowing a bicycle, friend sharing a photograph, teacher reading a private letter, dancer changing choreography, organizer recording a conversation, medic entering a room, moderator publishing a message, and researcher retaining an audio recording. A private written letter uses the transparent `kunipapa` + `shilë` compound in this new *epistolary letter* reading, rather than silently equating a phonological written character with correspondence. A medic can use the trained-practitioner derivation `guqaki-sharo`; the spelling `guqaki` itself is preserved.

Two scenarios (artist displaying portrait, traveler using a **spare** bed) remain deliberately out of scope because their exact result/object senses have not been defined. **Variants 4 and 5** for all eight adopted scenarios also remain unresolved: silent departure must not confer permission, and withdrawal of previously granted consent requires explicit temporal and reference tracking. Those 26 additional cases are *not* counted as solved.

## VII. Release gate

`python tools/stress89/compose.py` and `python tools/stress89/audit.py` must pass, along with the full tests, syntax-scope counterexamples, existing integrity audit, and frozen source hash checks. Run the full GitHub Action; never manually overwrite the old 8.8 evidence file or release baseline to make candidate counts improve.

A future claim of a self-sufficient, generally fluent language needs independent readers recovering novel multi-clause meanings and communication without English. Current exact candidate counts, failures and review flags belong to generated machine-readable summaries, not a fabricated claim of completion.

---

## Edition appendix 9.0 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_9_0_PRODUCTIVE_SEMANTICS.md](../../docs/standard_8/AMENDMENT_9_0_PRODUCTIVE_SEMANTICS.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Standard 9.0 · Productive semantic scope and reference (editorial edition)

**Status: new, narrowly adopted editorial constructions.** This does not establish a full translator, human-validated semantic equivalence or independent speaker comprehension. The historical 7.0 lexicon and corpus, 8.0 authoritative consolidated grammar, 8.1 embedded-polar ruling, prior 8.4–8.9 addenda and archived release hashes remain unchanged. This document extends the grammar with explicit source-linked meanings rather than rewriting earlier definitions.

To reproduce the entire original adversarial set, run `python tools/stress90/compose.py`, then `python tools/stress90/audit.py`. The former generates exact English stimulus → proposed Qaroshi ledger rows; the latter checks candidate **form**, produces an independent-reader blind packet with a separate key, and retains an unanswered case list. **All candidate translations remain editorial proposals** until independent review proves otherwise.

## 1. Permission: speech, silence, and later withdrawal

The 8.9 distinction between asking, refusing, and offering now extends to two more interactions across the eight separately licensed action frames in `consent_action_frames_8_9.json`.

**Silence does not license a permission inference.** Assert B's departure on its own, then negate A's *belief in the conditional* that B departing permits the action:

```qaroshi
sen pësënga shëlahe dëru-te.
sen wë pësënga shëlahe dëru-te, ruwa relomo-m sezhoshi-ho do ruwa nu shërawë-te.
```

This editorially says “The visitor left silently; the host did **not** treat that as permission to borrow the bicycle.” The first sentence asserts a departure. The second negates the inference, not the action or the actual existence of permission from a different source. It does **not** say the visitor said no, physically prevented borrowing, or granted consent.

**Past consent, revocation, and a potential opportunity are different events.**

```qaroshi
sen ruwa relomo-m sezhoshi-ho do pësënga terawo ruwa-tu maho-m hëzhohe-te.
sen ëna ruwa relomo-m sezhoshi-ki-te, pësënga dëna maho-m keleyu-te.
```

The visitor previously granted the host consent **to borrow this bicycle**, then withdrew *that same* consent before the host could perform the action. The previous consent is real; the action is only a potential opportunity and is **not asserted completed**. `dëna maho` reidentifies the same previous consent, not an unrelated permission. The time ordering is explicit. It does not license any universal consent from silence or permanent consent from a prior yes. This is a bounded construction; do not transfer it to arbitrary unreviewed verb senses.

## 2. Prenominal relative gaps with matrix scope

The 8.0 rule `[RELATIVE-CLAUSE sha] HEAD` is now explicitly composable with a full matrix proposition, a thought, a negated embedded polar question, an open conditional, and a causal reason. The head must identify the missing argument of its relative clause, as **subject** or **patient** in that *exactly specified* frame. Do not insert a second resonance inside an ordinary unquoted relative.

For the newly licensed person/call/morning frame:

```qaroshi
sen ëna lukhela wërawë-te, terayaro bobala-m shiwari-te sha shara dëru-te.
sen ëna lukhela wërawë-te, terayaro bobala-m shiwari-te sha shara dëru-te do mi tëmiro-te.
sen ëna lukhela wërawë-te, terayaro bobala-m shiwari-te sha shara dëru-te he do mi nu sëmi.
```

They respectively **assert** that the person who placed a voice call yesterday left before sunrise, say **I think** that this happened, and state **I do not know whether** it happened. Only the first has an unqualified matrix event assertion. The relative does not refer to the sunrise or the content of a call, and `he do` must not be confused with the final `he?` of a direct question.

The edition records five exact head-gap scenario families: a person who called, a machine repaired by an engineer, a dog that followed a cyclist, a message deleted by a moderator, and a medicine requested by a patient. Some scenarios also license consequence or cause combinations. Others deliberately lack the required whole-proposition meanings. Full source IDs, roles, scope and lexical sense decisions are in `data/standard_8/relative_frames_9_0.json`.

A causal clause `P ro REASON` asserts its reason in addition to P. A conditional `wë P, Q-yu` does **not** assert P; Q is a projected consequence. An attributed thought `P do mi tëmiro-te` also does not assert P as fact. In the forwarded-message family the new explicit prior-time boundary keeps **forwarding before deletion**, not merely “both occurred.”

## 3. Modal barriers: five mutually distinct truth conditions

From one source-licensed action and one full obstacle proposition, the language now consistently distinguishes:

| Frame | Shape | Interpretation |
| --- | --- | --- |
| Past counterfactual | `sen wënu ACTION-te, CONSEQUENCE-te qinë.` | A contrary-to-fact action with projected result |
| Dynamic ability | `sen ACTION-te-ki nao BARRIER.` | Ability despite an actual barrier; no assertion that ACTION happened |
| Permission | `sen ACTION-te-ho uro BARRIER.` | ACTION is allowed; neither ability nor performance follows |
| Necessity | `sen ACTION-te-du dëshu BARRIER.` | ACTION is required despite a barrier; actual completion does not follow |
| Hypothetical barrier change | `sen wë BARRIER do shërawewa eri-yu, ACTION-yu.` | If the barrier condition changes, ACTION is projected; not proof the change occurs or is beneficial |

Here `-ki` = ability, `-ho` = permission, `-du` = obligation; they are in the modality slot *after tense* when tense is shown. The existential clause on `shërawewa` is a new **propositional-state-change** construction. A change in the barrier does not automatically entail that the barrier is eliminated. This is especially important for “would X if the barrier changed,” which does not specify *how* the obstacle changes.

The initial adopted frames are a courier delivering correspondence while an address is unreadable, a student solving an equation despite missing variables, and a mechanic repairing an engine while a required part is absent. The earlier independently edited counterfactual `QS81-0336` is **retained unchanged** and not counted as a newly drafted form. See `modal_barrier_frames_9_0.json`.

## 4. Scientific claims: report, second observer, possibility, advice, and a blocked conclusion

For any **listed** technical proposition P in `technical_propositions_9_0.json`, the following constructions have different logical consequences:

| Pattern | Reading |
| --- | --- |
| `sen P do zhikasasho shërawëhu-te.` | A report *states* P, without narrator endorsing P |
| `sen P do larëno subali-mi khunikhu-te.` | A second scientific observer *recorded* P, not evidence P is objectively correct |
| `sen P do këraro nao P do tequyu nu shërawëhe-li-te.` | P is **possible**, but has not been **independently verified** |
| `sen wë P, RECOMMENDATION-du.` | **If** P, an action **should** be done; does not say the action occurred |
| `sen P. sen P do ngëshi zhëwëra, Q do zotenga nu eri.` | **P is a fact** but P **alone** does not provide sufficient proof of Q |

The last is a new restricted **nonentailment** construction: `ngëshi` isolates P as the *sole offered evidential premise* and `zotenga nu eri` denies a proof link from that premise to Q. It does **not** say Q is false or that no other evidence could prove Q. The separate initial sentence establishes P as fact because the English target explicitly says “the fact that P.” Without that first sentence, the same proposition may instead be treated as a hypothetical premise.

Ten technical scenario families now have a source-grounded P: battery overheating, an incomplete audit log, dropped network connection, contaminated laboratory sample, copied encrypted file, drifting temperature sensor, an erroneous patient record, bridge corrosion revealed by inspection, telescope recording a faint signal, and an unsigned contract. Recommendations and unsupported conclusions are included **only where full lexical and semantic frames are licensed**. Unlicensed cases remain empty; a copy does not prove decryption, a record error does not prove dishonesty, and detected corrosion does not prove structural collapse.

The explicit source IDs include derived transparent compounds (audit+log, network+connection, laboratory+sample), past participles, physical process extensions, and qualified non-agentive passives. Those additions do not make arbitrary inanimate arguments or all passive forms grammatical.

## 5. Figurative language and corrections to a literal reading

A **newly written metaphor** must not automatically be elevated to a traditional idiom. In `literary_frames_9_0.json`, exact lexical images from seven original story challenges are treated as **editorial personification** with corresponding written attribution and reader repair.

| Structure | Meaning |
| --- | --- |
| `sen gëmano P.` | P holds **in a fictional story**, not in the real world |
| `sen shirimi toru «sen P.» shiroli-te.` | A narrator **wrote** that exact quoted Qaroshi sentence |
| `sen deshemu-mi toru «sen P.» INTERPRETATION do shërawiwo-te.` | A poet used those words to **suggest a literary interpretation**, not a literal event |
| `sen shënaweho toru «sen P.» LITERAL do nu shërawëhu-te.` | The quoted sentence **does not assert** the literal-world reading |
| `sen pëyeno toru «sen P.» gëmodo shëliro-te. sen ana pëyeno gëmodo shëliro-te, pëyeno zhiqomo-m peziholë-te.` | A reader **initially interpreted the quote literally and later corrected that reading** |

Narrator as a written storyteller (`shirimi`), poet (`deshemu-mi`, from “write poetry”), and correction of a reading are new **narrow** editorial valency decisions. Quotes of full Qaroshi sentences keep their **own internal resonance**. The outer narrator does not have a second *unquoted* register. The distinction between exact words `toru` and paraphrase remains in place.

The seven recorded images include forest guarding secrets, clock disputing with silence, river carrying a thousand memories, town holding its breath, mountain refusing to move, old house remembering every winter, and road forgetting travelers. The river's “one thousand” is precise: `zhu zhewawa dë zhewa zhu zhe zhu` = 4×216 + 3×36 + 4×6 + 4 = **1000 decimal**. Where a source interpretation or the literal counterexample cannot be lexicalized without added assumptions, variants 3 or 4 are withheld. Narrative cases with no whole image composition remain unresolved.

## 6. Inherited drafts, adversarial testing and comprehension

These files keep the original English challenge identity unchanged:

- `data/stress90/case_evidence_500.csv`: every original English item, previous candidate, new candidate when licensed, canonical IDs, scope signature and explicit abstention.
- `data/stress90/formal_review_500.csv`: *formal* review of all 500 rows, including the 190 inherited editorial drafts. No human translation scores are filled in.
- `data/stress90/unresolved_cases.csv`: each case without a full candidate, meaning components required, and explicit absence of proof that it is impossible.
- `data/stress90/blind_qaroshi_only.csv`: all currently drafted Qaroshi candidates as stimuli, without English answers or correct meanings.
- `data/stress90/private_english_answer_key.csv`: same stable case IDs with the original English and reviewer rubric; **never give this to blind participants**.

The tests check inheritance, exact source IDs, clause scope, participant case, source attribution, conditional modality, negation, figurative vs literal assertion, and nonentailment. A strict string match is evidence of an editorial grammar rule, **not** independent communication or backtranslation.

**No independent readers have been assessed by this release.** A reliable comprehension result requires consenting, separately recruited readers who did not write or see the English prompts, then independent scoring of actor, patient, event polarity, reference, timing, uncertainty, source and excluded entailments. Those outputs must be recorded before claiming the language can operate without reference to English.

## 7. Controlled reproducibility

```sh
python tools/stress90/compose.py
python tools/stress90/audit.py
python -m unittest discover -s tests -q
python tools/maintenance/audit_repository.py --site
```

Only new editorial overlay files are added. The 8.0 dictionary, 7.0 historical lexicon, stored examples, frozen benchmarks, prior contributors' assets and old manifests must not be modified to force a score improvement.

---

## Edition appendix 9.1 (restricted editorial)

Source: [docs/standard_8/AMENDMENT_9_1_COMPLETE_EDITORIAL_CHALLENGES.md](../../docs/standard_8/AMENDMENT_9_1_COMPLETE_EDITORIAL_CHALLENGES.md). Original archived wording is retained; the opening 9.2 conflict table takes precedence for new editorial writing.

# Standard 9.1 · The 500 challenge editorial completion pass

**Status: editorial addendum, not human-attested language proficiency.** This extension documents exact new language decisions for the 182 previously undrafted English adversarial items. It does not replace the frozen Standard 7.0 corpus or the 8.0 canonical dictionary and grammar, and it does not retroactively make the earlier 318 candidates independently correct.

The five original variants of each of 100 scenarios, including awkwardly written original English prompts, remain unchanged in `tools/stress81/scenarios.py`. The new `tools/stress91/compose.py` runs the full historical chain, preserves every previous edition's completed draft in its versioned **source ledger**, and supplies full candidates for the previous 182 empty entries. In the 9.1 view, **310 inherited drafts remain byte-for-byte unchanged** and **8 inherited consent drafts receive an explicitly recorded tense/modality correction**; every original remains in `prior_9_0_candidate` and the immutable 9.0 results. The corresponding vocabulary, role choices, selectional restrictions and truth-condition decisions are all versioned under `data/standard_8/*_9_1.json`.

## 1. Eventive negation and the English "not until" construction

Previous documents already distinguished `ana` (after), `ëna` (before), `yaro` (when/overlap), and `torëne` (until). The missing challenge was **not P until Q**: it is not equivalent to simply writing a negated P ending at Q, because the ordinary English reading normally commits to eventual P. The restricted 9.1 pattern is:

```qaroshi
sen torëne Q-te, ACTOR OBJECT nu P-te.
sen ana Q-te, ACTOR OBJECT P-te.
```

The first full sentence asserts absence of the event through the relevant pre-Q interval. The second independently asserts a **later occurrence of the same action**, following the **same endpoint event**, with a new sentence-initial resonance. The repeated source-controlled endpoint is anaphoric to its immediately previous mention; a new marker `aru` would indicate a repeat endpoint event rather than anaphoric reuse.

For example, the earlier adopted courier crossing can now be stated as:

```qaroshi
sen torëne lushënga wuzhagi-te, rikanga kimaro-m nu lurezhu-te.
sen ana lushënga wuzhagi-te, rikanga kimaro-m lurezhu-te.
```

This means the courier did not cross the river until the storm ended, and later did cross. The sentence neither asserts that the storm **caused** crossing nor that the crossing occurred immediately after the storm ended. Two independent resonance markers are required because there are two separate sentences. A simple `sen torëne ... nu lurezhu-te.` without the positive-event sentence is **not** a complete answer to this original English target.

The same licensed pattern covers ferry boarding, mountain summit reaching, ambulance departure, bicycle passing, aircraft landing, tourist entry, hikers returning to camp, a train stopping, and rescue teams approaching a cliff, using explicit per-event actor, goal, patient and time roles recorded in `motion_frames_9_1.json`. The other four temporal variants preserve `ana`, `ëna`, `yaro`, and the polar `hë ... he?` with no hidden additional clause register.

## 2. Everyday roles and genuine past counterfactuals

An everyday positive action `S O-m V-te` has four distinct speech-act uses, not merely four spellings: observed/asserted action, asserted non-occurrence `S O-m nu V-te`, a sincere direct polar question `hë S O-m V-te he?`, and someone reporting content `sen S O-m V-te do yano mi-tu shiri-te.` A report is *not* the narrator's independent verification.

The past contrary-to-fact template remains `sen wënu P-te, Q-te qinë.`: Q is **projected**, not an actual reported result. When the English consequent uses *it*, *they*, or some other anaphor, the chosen specific item is repeated or explicitly linked in the frame instead of fabricating a new referent.

The 9.1 additions define missing-key discovery, baking bread that burned, watering seedlings, packing an instrument, forgetting directions, hiding a notebook, counting coins, and losing a ticket. The corresponding specialized actor and action roles have separately named sources and selectional limits. For example `punushu-zhëmiwa` denotes *damaging bread by burning/scorching*, not normal toasting, and `shëntaku` hides a physical notebook rather than metaphorically hiding a feeling.

## 3. Productive semantic extensions without corrupting the dictionary

The new file `editorial_lexicon_9_1.json` declares **proposed** sense extensions, transparent derivations, and a few new roots where no precise canonical word was found. Each entry lists a specific Qaroshi form, lexical category, gloss, definition, actual source IDs where relevant, and `independently_attested: false`. Entries with `status: not_adopted` are rejected experiments and cannot be used as an approved 9.1 headword.

Word formation keeps the established **modifier–head** order and known derivations `-mi` participant, `-sharo` specialist, `-dëno` place, `-nëro` action result, `-këlë` instrument, `-ma` event and `-rë` property noun. Thus `tëzhida-mi` (gardener), `lëngazho-sharo` (bread baker), `rewunu-mi` (traveler), `luringi-dëno` (campsite), and `shiwari-nëro` (sent parcel) are transparent derivations used with **specific adopted meanings**, not proofs that every possible compound has the same conventional meaning.

The few explicitly coined roots, such as `gëngora` (a bell), `shëngaru` (cause a bell to ring), `shëwarono` (exhibit a portrait), `këshëru` (develop a structural crack), `zësharo` (last item in a sequence), and `tëwërano` (a paint roller), fill independently documented semantic gaps. Their existence as 9.1 editorial entries is **not** an assertion that Qaroshi speakers have adopted these words. Exact word forms and status should be taught to learners as proposed until validation.

No original dictionary ID, 7.0 lexical entry, historical example, old grammar chapter, 26-symbol glyph chart or 16-register inventory is overwritten. Old meanings (e.g. a bell distinct from a key ring, an artistic portrait distinct from a digital post, or a garden hose distinct from a paint roller) are not silently replaced by new generalized English glosses.

## 4. Reusable participant and clause reference rules

The other relative-clause additions cover:

- the book that a **student** borrowed, and the **same book's** final page;
- a **correspondence letter** that arrived without a name, and a warning it contained;
- a song that a **choir** rehearsed, shorter **than expectation** rather than simply short;
- a photograph that a traveler saved and that depicted the *wrong* mountain;
- a story that the children invented and that confused adults through **two different characters with identical names**.

The relative gap corresponds to the noun head in `[RELATIVE sha] HEAD`. The gap can be subject or object as separately documented; it never automatically transfers to an embedded narrator, nearby participant, or unrelated possessed object. After relative clause and head, 9.1 conservatively composes an assertive matrix, speaker thought, unknown polar knowledge, a real conditional with projected consequence, or a causal explanation. These are different truth conditions.

A causal reason `ro REASON` is asserted as explanatory content; a `wë P, Q` is contingent and does **not** assert P. The English original's "if ... would" doesn't license an immediate real-world action by any participant. Previously adopted 9.0 relative frames remain untouched; 9.1 adds only the missing variants and source-specific head-gap patterns.

## 5. Ability, permission, obligation, barriers and real-world commitments

For the remaining counterfactual/modality sets, the 9.0 distinction is maintained:

| Construction | Event in real world? | Modality |
| --- | --- | --- |
| `wënu ACTION-te, CONSEQUENCE-te qinë` | No actual consequence asserted | Past counterfactual |
| `ACTION-te-ki nao BARRIER` | Ability but not actual performance | Ability |
| `ACTION-te-ho uro BARRIER` | Permission but not ability or performance | Permission |
| `ACTION-te-du dëshu BARRIER` | Requirement but not actual performance | Necessity |
| `wë BARRIER do shërawewa eri-yu, ACTION-yu` | Conditional change *only* | Open hypothetical |

Seven source-specific scenarios add early train tickets, repairing a damaged tree, avoiding a storm with unavailable radar, replacing a damaged book, finishing a concert despite electric failure, opening a shelter with misplaced keys, and reaching an island against a strong current. An adverse or unavailable barrier is a separate proposition and **cannot** be silently dropped. **A change in a barrier is not necessarily the barrier's removal.** This matters for the original awkward English prompts that say, for example, "if the tickets were sold out changed." We preserve their exact wording while recording the intended *change of that stated condition* as a bounded editorial hypothesis. Any intended alternate reading still requires editorial/human adjudication.

## 6. Human participants, physical tools, evidence and reporting

Two social-consent families add a portrait displayed to a customer and a spare bed used by a traveler. Each distinguishes asking the owner, an explicit **no**, an offered action that is **declined**, silence being **insufficient to grant consent**, and active withdrawal of previously granted action-specific consent before the action could occur. No request, proposal, silence, ability or former agreement licenses future use after withdrawal.

Five remaining active instrument cases name actual material objects and keep the agent, patient and tool separate: a gardener uses a paint roller, a technician uses a reference measurement device, an artist uses pigmented tiles, a carpenter uses wooden pegs, and a worker uses a steel lock. **`-shi` means instrument**, not a passive agent; **`-za` means agent** in a licensed passive. The mere fact that an actor exists does not give an instrument object causal agency or independent intention.

The new evidential frames preserve the event-specific literal meaning for an already-open window, a comet becoming hidden by cloud, a parcel arriving yesterday, a bridge cracking overnight, and a dancer missing a stage cue. These compose four distinct views: speaker witnessed, another person told the speaker, speaker inferred, and speaker does not know whether the event occurred. Three alternate propositions (parcel returned, musical conductor stopped playing, sensor detected movement) are used only in **matrix nonassertions**, not in claims that those events did **not** happen.

## 7. Fiction and technical proof limitations

The literary expansions include a sky swallowing its final light, a storm knocking on a door, and a fire painting a room gold. **`gëmano`** keeps the image within fiction; **`toru «sen ...»`** preserves a complete quoted utterance and its internal resonance. A poet's *suggested meaning* is different from a narrator's exact quoted wording, and an editorial denial of a literal reading is not proof that such a physical event happened. Two earlier literary images also receive missing interpretive readings: the house shaped by history and the forgotten road.

The final six technical proposals explicitly cover a safety circuit stopping battery charging, why overheating does **not** prove a defective charger, why network dropout does **not** prove a server attack, a telescope signal requiring noise exclusion, why a weak signal does **not** prove extraterrestrial origin, and why an unsigned contract does **not** automatically establish legal invalidity.

For a technical conclusion, an expression `P do ngëshi zhëwëra, Q do zotenga nu eri` rejects *P alone being sufficient proof of Q*. It **never** asserts that Q is false or impossible. Similarly, `if P, action-du` gives a *conditional recommendation*, not proof the recommendation was followed. No claims of specific legal enforceability or scientific confirmation are made from an English sentence that lacks those facts.

## 8. Versioned repair of eight inherited suffix-order mistakes

The expanded formal review found eight pre-existing 9.0 consent-revocation candidates with **`-ki-te`** (“ability, then past”), which contradicts the Standard 8.0 verb ordering **root–voice–tense–aspect–modal**. The 9.1 active-view spelling is **`-te-ki`** (“past, then potential ability”), for `QS81-0105`, `0110`, `0115`, `0120`, `0125`, `0135`, `0140`, and `0150`. The exact original forms are preserved in `prior_9_0_candidate` and the unmodified 9.0 source ledger. This is a **versioned editorial correction**, not a native-speaker attestation. The complete replacement rule, rationale, and eight precise affected case IDs are recorded in `consent_morphology_corrections_9_1.json`, and regression tests verify both the old and corrected versions. It does **not** add eight new English challenges or inflate the 500/500 draft count.

## 9. Benchmark and independent-validation obligations

The **500/500** number, once the 9.1 builder passes, counts only **complete editorial candidate strings** with source-bound grammatical decisions. It is **not** a passing comprehension score, a certified translation score, or evidence of active everyday fluency. There are zero independent readers, zero human backtranslations and zero independently certified meanings at the time of this edition.

The release builds:

- `data/stress91/case_evidence_500.csv`: one row per unchanged English prompt, each inherited form preserved in `prior_9_0_candidate`, all 182 previously empty cases filled, and the 8 revised inherited forms identified with an explicit morphology correction reason;
- `data/stress91/formal_review_500.csv`: case-level basic formal flags, English requirements and editorial status;
- `data/stress91/blind_qaroshi_500.csv`: **Qaroshi-only** reading stimuli with no English answers;
- `data/stress91/private_reviewer_english_key_500.csv`: separate original English and a component-based scoring rubric;
- `data/stress91/review_summary.json`: counts with no fictitious readers or claimed independent scores.

A genuinely independent test must present sentences without the English key to consenting readers who did not author the candidate translations. Ask each reader to identify agent, recipient, reference identity, time order, actual/hypothetical status, speech act, and uncertainty before seeing any target. The reviewer scores disagreements and ambiguous readings against the isolated original English. Failing translations should be revised and re-tested with fresh independent readers; the editorial form score is not a substitute.

**Reproduce:**

```sh
make stress91
python -m unittest discover -s tests -q
python tools/maintenance/audit_repository.py --site
```

The output must remain reproducible without modifying the frozen baseline source files. A successful CI run establishes *software regression and editorial ledger integrity only*. Independent language viability is still a separate real-world research question.
