#!/usr/bin/env python3
"""Build long-form Qaroshi learning guides and source-backed drills.

Uses only existing Unified Standard 5.0 words, corpus and grammar rules.
Version 5.1 deepens pedagogy without changing vocabulary or grammar.
"""
from pathlib import Path
import csv, re, json, textwrap, collections
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/deep_guides';DOC.mkdir(exist_ok=True,parents=True)
with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:
    CORPUS=list(csv.DictReader(f))
PHRASE={p['id']:p for p in CORPUS}
WORD={x['qaroshi']:x for x in csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf8',newline=''))}

# Each teaching guide is grounded in the indicated existing grammar chapters.
# The IDs here are also stable offline wiki navigation destinations.
GUIDES={
'getting_started':('Start here: a structured route to Qaroshi','1–5, 8–11',r'''
## What a learner should understand first

Qaroshi is not English with a replacement alphabet. Learning a word does not teach the placement of its grammatical role. In particular, the sentence-initial resonance, case suffixes, and clause-final verb combine to convey information which English often spreads across word order and prepositions. The quickest route to reading fluency is to master **one complete, well-formed sentence** before memorizing large vocabulary lists.

A practical learning sequence is: (1) identify glyphs and Romanization; (2) select an opening resonance; (3) identify who acts and what receives the action; (4) put the verb at the end; (5) add tense, aspect and case endings; (6) connect clauses; (7) practice literal glossing before writing natural English. You can read a conversation before you can write one, and you can write controlled examples before you can write idiomatic prose. Treat these as distinct skills.

## A first-sentence checklist

1. Is it a complete Qaroshi sentence rather than a title or fragment? A complete sentence begins with **exactly one** resonance marker, including `sen` for plain facts.
2. Which participant is the grammatical subject? `mi`, `ti`, `sa`, `naru` and `muru` do different jobs. The distinction between inclusive and exclusive *we* is not optional meaning.
3. Is there a direct object? If so, check its `-m`. Possession (`-na`) and recipient (`-tu`) answer different questions.
4. Is the predicate a verb, noun or adjective? Present noun/adjective predicates do not require an English-like copula.
5. Does a time ending or speech-act particle belong here? `-te` is past, `-yu` future, `he` question, `ya` request. These should not be scattered into arbitrary positions.
6. Does the sentence have its own evidence marker? `si`, `hu`, `ye` say how it is known; they do not substitute for resonance.

## Three ways of reading one line

Read `më mi ti-m nashi.` in three passes: (a) recognize `më` as Warm Hum, (b) identify `mi` as actor and `ti-m` as object, then (c) identify `nashi` as the predicate of deep care. A **word-for-word gloss** is “warm-register / I / you-object / cherish-deeply.” A **grammatical translation** is “I cherish you deeply.” An **interpretive translation** can mention the affectionate delivery, but must not automatically convert this into romance; Warm Hum and `nashi` are compatible with several forms of closeness.

## Study rhythm and self-check

For each lesson below: read the rule, read the Qaroshi and IPA aloud, hide the English and translate, then hide the Qaroshi and reconstruct. After that, change one grammatical feature and predict what changes in meaning. Revisit the same sentence on later days; recognition is easier than independent production, and repeating only recognition can hide gaps. An answer counts as correct only if the sentence-initial resonance and all relevant suffixes are accounted for.

## How to use this wiki

Use **Dictionary** to check senses and sound-out, **Grammar** for the normative rule, **Phrasebook** for attested-in-reference teaching examples, **Native script** for the letter mapping, and **Guided course** for staged practice. Full Markdown materials are in the release archive. The search box finds words, grammar and example text, but it is not an unrestricted translation engine. If multiple analyses are possible, preserve the ambiguity rather than choosing a convenient English interpretation.
'''),
'pronunciation_lab':('Pronunciation laboratory: phonemes, stress, and rhythm','1, 30, 48',r'''
## What Romanization does and does not do

Every Qaroshi native letter has a stable broad phonemic value. The Romanized sequences `sh`, `zh`, `kh`, and `ng` are each **one** native letter, not two consonants to pronounce separately. `ë` is the sixth vowel, /ə/, and never a decorative variant of `e` /e/. English letter names (for example “Q” /kjuː/) are not the sounds made by the Qaroshi Romanized letters; the Latin A–Z guide is a separate reference.

To pronounce a headword accurately, first segment it into native letters, next identify vowel nuclei, and finally apply the usual penultimate-syllable stress. For `qaroshi`, the broad reading is /qa.ˈɾo.ʃi/. Stress is on **ro**, not the first syllable. Hyphens in examples such as `mi-na` mark morphology for learners; they are not pronounced as a pause and are not separate glyphs.

## The vowels: six distinct targets

Keep `a /a/` open; `e /e/` is a pure front mid vowel without the English off-glide; `i /i/` is like a sustained high front vowel; `o /o/` is pure rounded mid; `u /u/` is high back rounded; and `ë /ə/` is a relaxed central vowel. English-style sound-out is a rough bridge, never an exact substitute for IPA, especially for `e`, `o`, and `ë`. A learner who collapses `e` with `ë` risks producing another written lexical form. Practice each vowel as an independent held sound before adding consonants.

## Consonants that require extra practice

`q /q/` is a voiceless stop made farther back than `k /k/`, not English “qu”; `kh /x/` is a continuous velar fricative, not the English /k/+/h/ sequence. `r /ɾ/` is a single tap of the tongue; a deliberate trill can occur, but should not turn a short tap into an English approximant /ɹ/. `ng /ŋ/` represents one nasal; avoid adding a final hard /g/. `sh /ʃ/` and `zh /ʒ/` distinguish voiceless from voiced postalveolar frication. Say them alone, then in short known words.

## Stress and parsing

A syllable typically has shape `(C)(r/l/w/y)V(C)`. When a word has two or more syllables, the normal lexical stress falls on the penultimate syllable. The reference's stress-marked reading capitalizes the stressed syllable; this capitalization is **not** part of normal Qaroshi spelling. A one-syllable particle need not show a special capitalized stress. Derived forms can shift the stress position because the full citation word is the basis of the pronunciation guide.

## A five-minute drill

Take `qaro`, `qaroshi`, `gëro`, `dërawa`, `khura`, and `nashi`. For each word, cover the IPA, predict the sound from letters, then check the dictionary. Repeat using the original glyphs in the script converter. Next read a complete sentence smoothly, keeping case endings attached to their roots and not adding extra English schwa vowels after final consonants. The written resonance tells you intended discourse delivery, not an obligatory pitch contour or exact measured acoustic resonance.

## What cannot be inferred from the transcription

The broad IPA is rule-based. It does not prove accent distribution, social variation, vocal range, coarticulation in casual speech, or a recorded native pronunciation for every word. The standard orthography supplies phonemes and predicted stress, while acoustic and dialect descriptions require other kinds of evidence. The wiki therefore distinguishes IPA from approximate sound-out and avoids inventing exception pronunciations for names.
'''),
'resonance_mastery':('Resonance mastery: writing emotion into grammar','2, 16, 31, 36, 40–43, 51',r'''
## A marker is grammatical, not decorative

In Qaroshi, every complete independent sentence begins with exactly one of sixteen written resonance markers. This applies to neutral descriptions, loving words, technical instructions, texts, questions and formal declarations. A completely neutral document may repeat `sen` at the start of sentence after sentence. Omitting a marker in a full sentence is not “more casual”; it makes the sentence nonstandard. By contrast, a bare dictionary headword, a heading, a label or an incomplete message fragment does not automatically count as a full sentence.

A marker has **sentence scope**: it frames all the clauses within the sentence, including a `ko` purpose clause or a `ro` reason clause. If emotional stance needs to change halfway through an utterance, close the sentence and begin another. A separately quoted complete Qaroshi sentence retains its own opening marker inside the quotation. There is no second mandatory register marker after a subordinate conjunction.

## Meaning, intention, and interpersonal boundary

The resonance marks *intended delivery*, not an objective diagnosis of the speaker's feelings. `më` conveys tenderness, `zha` lively excitement, and `qor` solemn gravity, but these do not by themselves establish romantic interest, permission, agreement, or legally binding promises. A statement spoken with anger may be true or false; a statement spoken calmly may be cautious or misleading. This distinction matters in Nardoragon social writing, where expressive framing is grammatically visible.

The sixteen options group into useful families: social closeness (`më`, `lën`, `hol`, `wen`); energy or surprise (`zha`, `yë`, `rëm`); public seriousness (`qor`, `dal`, `sen`); threat or conflict (`khar`, `rak`, `zher`); and inward states (`nëm`, `sur`, `hë`). These are practical teaching groupings, not extra grammatical classes. If two appear to fit, decide the speaker's communicative intent: gratitude (`hol`) is not necessarily joy (`zha`), and an alarmed question (`khar`) need not sound sincerely inquisitive (`hë`).

## Cross-register comparisons

Change only the first word of `ti lësha.` and the lexical proposition remains a compliment: `më ti lësha.` is tender; `zha ti lësha!` playful; `lën ti lësha.` shy. The marker does not alter word order, conjugation, possession or the semantic meaning of `lësha`. In translation, it can be carried in narration (“she said shyly”), punctuation, dialogue tags or a note where English has no equivalent mandatory category. Avoid replacing a resonant compliment with different factual content just to convey the mood.

## Requests and consent

`më pëla mi-wa nëra ya.` means “Please stay with me,” while `më yëmë ti mi-wa nëra.` means something closer to “May you stay with me.” The first asks for an action; the second voices a wish. Neither guarantees the addressee's consent. The optional softener `lan` can make a request explicitly easy to decline. If someone responds with refusal, the earlier Warm Hum framing does not cancel their answer.

## Editing a multi-sentence message

Write one resonance per independent sentence before choosing punctuation. Then make sure every quote that is itself a complete Qaroshi sentence has its own marker. Check whether the emotional frame truly applies to both clauses of a connected sentence; if not, split it. Also distinguish resonance from evidentiality (`si/hu/ye`) and speaker confidence: expressing uncertainty through `zher` does not itself establish whether the speaker witnessed the event.
'''),
'sentence_anatomy':('Sentence anatomy and interlinear parsing','3, 18–20, 28–30',r'''
## The default order

The standard template is `REGISTER — SUBJECT — OBJECT — other roles — VERB`, with optional topic, time, manner, negation, evidential and speech-act material in the established positions. It is important not to assume that a word in the English translation occupies the same position in Qaroshi. `sen mi kima-m këmë.` is not “I drink water” word-for-word: it is `sen` [neutral] + `mi` [I] + `kima-m` [water-as-object] + `këmë` [drink]. The noun's case ending identifies its syntactic function.

A learner's literal gloss can use tags: **REG** resonance, **SUBJ** subject, **OBJ** object, **GEN** possessor, **LOC** location, **DAT** recipient, **PST** past, **FUT** future, **PROG** progressive, **Q** direct question, **REQ** command/request. These labels are analytic teaching symbols, not Qaroshi words. They are especially useful when an English version has to reorder a sentence heavily.

## Three complete parses

`sen mi-na mara kima-m këmë.` → `sen` [REG], `mi-na` [my-GEN], `mara` [friend-SUBJ], `kima-m` [water-OBJ], `këmë` [drink]. Literal “my friend water drinks”; natural “My friend drinks water.” Notice that `mi-na` is **not** the subject, despite coming before the subject.

`sen mi mara-tu kima-m pëli.` → `sen` [REG], `mi` [SUBJ], `mara-tu` [friend-DAT], `kima-m` [water-OBJ], `pëli` [give]. The subject is the giver, the recipient is the friend and the transferred item is the water. Do not place the dative where the direct object belongs.

`më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.` → warm [REG]; politeness; subject `ti`; `sëna` always; negation `nu`; predicate `zëru`; request `ya`; purpose connector `ko`; subject `ti`; `mi-wa` with me; `sëna` forever; `nëra-ki` able-to-stay. The second clause inherits the opening resonance. It is a purpose clause, not a new independent sentence.

## Distinguish free words and suffixes

`mi-na` is one grammatical unit based on a pronoun. The hyphen is a teaching aid, so the syntax treats it as a phrase rather than separate freestanding `na`. Similarly `goro-te-se` is one finite predicate, not three separate words. Resolve complete dictionary headwords before stripping apparent endings: a root can coincidentally end with letters that resemble a suffix.

## Four-pass parsing protocol

First locate the resonance and any clause boundaries. Next identify the finite predicate or predicate adjective/noun. Third mark case-bearing noun phrases and pronouns; fourth interpret tense, aspect, modality and evidential. Only then turn the result into idiomatic English. This method prevents “English-shaped” translations which look plausible but reverse agent and patient, drop negation or omit whether a statement was inferred.

## Distinguish fragments from full sentences

Dictionary entries and chapter headings are not independent assertions and may lack a resonance. A full message such as “I rest” should not. In connected writing a new sentence begins with a fresh resonance even when the previous sentence used the same register. This remains true for captions and subtitle sentences.
'''),
'nouns_cases':('Nouns, possession, reference, and case','4–5, 12–13, 22, 26, 28–29',r'''
## Why case is more than a preposition

Qaroshi uses suffixes to state relations directly on noun phrases. The basic contrast is `-m` direct patient/theme, `-na` possessor, `-lo` location, `-gu` destination, `-de` source, `-wa` accompaniment, `-tu` recipient, and `-shi` instrument or passive agent. A noun phrase normally bears **one case**, and the outer topic `-së` can follow that case. Mixing `-lo` and `-gu` on the same noun to mean “at and toward” is not standard; express two relations with separate phrases or a fuller clause.

## Building a noun phrase safely

Begin with the root, add a documented derivational element if needed, optionally add affectionate `-lë`, optionally plural `-ri`, then one case, then optional topic `-së`. `mara-lë-ri-m` therefore means dear friends as a direct object. Do not interpret the hyphens as additional spoken syllables. The order matters: a learner who places plural after case is no longer following the noun template.

## Possession is not legal ownership

`mi-na banu` “my wing” and `mi-na mara` “my friend” use the same genitive relation even though neither means a property title. `mi-na naro` means “my home” without resolving whether the speaker owns, rents, occupies or belongs to it. For an explicit legal ownership assertion, use the dedicated verb `shënawo` in context. This distinction prevents a translation from accidentally asserting legal facts that the Qaroshi construction does not encode.

## Numbers, definiteness and adjectives

No obligatory articles distinguish English *a* from *the*. `qaro` can be referential or generic depending on context. Plural `-ri` is normally available when relevant, but may be omitted when an explicit numeral already establishes count. Attributive adjectives follow their nouns, while demonstratives precede them. `dëna qaro zaki` = “this strong Nardoragon”; `qaro zaki po` = “two strong Nardoragons.” When a noun itself is the predicate of a present identity sentence, no separate present copula is needed.

## Body, companionship and movement

Locations are general: `naro-lo` may mean in/at/on home depending on context. Use spatial relational nouns to sharpen the scene, such as `naro-na larë-lo` for on top of the home. `-gu` is movement toward a destination, not a synonym of `-lo`. `-wa` says together with, and should not be used for a tool merely because English says “with a pen”: a tool takes `-shi`.

## Cases in translation

When translating from English, ask “What is the semantic role?” rather than “Which English preposition appears?” English *with* can mean companionship (“with a friend,” `-wa`) or means (“with a pen,” `-shi`). English *to* can mean recipient (`-tu`) or direction (`-gu`). Qaroshi makes this difference overt and the contrast should survive an English gloss or a teaching parse.
'''),
'verb_workshop':('Verb workshop: tense, aspect, voice, modality','6–8, 21, 27, 30, 38',r'''
## A predictable slot structure

The standard finite verb template is `ROOT + [VOICE] + [TENSE] + [ASPECT] + [MODALITY] + [TENDER MANNER]`. Brackets denote optional categories, not literal writing. The ordinary suffix choices are voice/valency `-ru` causative, `-li` passive, `-wo` reciprocal, `-ne` reflexive; tense `-te` past or `-yu` future; aspect `-se` ongoing, `-mo` completed, or `-në` habitual; modality `-ki` can, `-ho` may, or `-du` must; tender manner `-la`. Use at most one member of each mutually exclusive category in an ordinary predicate.

## Tense and aspect do different work

`goro` means to fly, or flies in a present/general clause. `goro-te` is past flight; `goro-yu` future flight. `goro-se` reports an action in progress at the contextual reference time. `goro-te-se` is past ongoing; `goro-te-mo` gives a completed event viewed from the past. `goro-në` is habitual flight and is not interchangeable with `goro-se`. One event can be habitual without being in progress at the present moment.

## Modals and responsibility

`-ki` encodes ability or possibility in the documented potential use, `-ho` permission, and `-du` need/necessity. They are not three degrees of the same idea. “Can leave,” “may leave,” and “must leave” can differ enormously in medicine, law or interpersonal boundaries. The form `goro-yu-du` is “will have to fly,” not a future progressive. To express several modal notions, use separate clauses instead of stacking incompatible suffixes into one verb.

## Voice and who acts

Causative `-ru` adds a causing participant; passive `-li` promotes the affected argument and can omit the agent; reciprocal `-wo` means action among participants; reflexive `-ne` points the action back toward the actor. Compare `sen mi qaro-m goro-ru.` (“I make the Nardoragon fly”) and `sen naro daru-li-te.` (“The home was protected”). The two sentences do not have parallel roles even if the English auxiliary verbs feel similar.

## Negation has an exact attachment site

`nu` goes immediately before the **whole predicate**, including any suffixes. `sen mi nu goro-yu-ki.` means the speaker will not be able to fly. Do not insert `nu` between `goro` and `-ki`; an affixed form is a single predicate. An adjectival predicate can also be negated (`sen ti nu haro.`). “Never” can use `zëna` or the emphatic `sëna nu` construction, which remains “always not” in a literal gloss.

## Four transformation checks

Start with `sen mi shërami.` (I sleep). Change past: `sen mi shërami-te.` (I slept). Change past progressive: `sen mi shërami-te-se.` (I was sleeping). Change habitual: `sen mi shërami-në.` (I sleep regularly). Observe how the subject and resonance stay unchanged; only the grammatical view of the event moves. A student should be able to justify each suffix aloud before writing an English paraphrase.
'''),
'asking_and_negating':('Questions, requests, negatives, and boundaries','8–9, 24, 31, 41, 64–65',r'''
## Asking is different from asserting

A direct ordinary yes/no question ends in `he`. A question word normally stands in the position of the missing information: `meya` who, `khe` what, `lona` where, `yeta` when, `shoro` why, `hara` how, `ruki` which, `zëli` how much/many. Many everyday questions use `hë` as the resonance because they seek information, but a frightened question may begin with `khar`; the question still requires its closing interrogative marker.

## In-situ questions

Qaroshi is not English-style question-word-fronting. In `hë ti khe-m tika he?`, `khe-m` means “what” occupying the direct-object slot. The ending `-m` is crucial: the question asks what the addressee sees, not who is doing the seeing. For a location question, `lona` often already carries the intended location meaning and conversational usage prefers `hë ti lona nëra he?` without an additional case suffix.

## Direct vs embedded questions

The proposition inside “I know whether…” is **not** itself a direct question. The complement `qona` signals embedded polar alternative. In `sen sa haro qona mi sëmi.`, the uncertainty is embedded inside a statement. Adding a standalone `he` inside every content clause would confuse independent speech-act marking with a dependent question. Similarly, a quoted *complete* Qaroshi question is its own sentence and therefore has its own resonance and `he` inside the quotation.

## Negative statements and negative requests

Negation `nu` directly precedes the predicate: `sen mi nu shiri.` = I do not speak. In requests `nu` remains next to the predicate and the sentence receives `ya` at the end: `më pëla nu zëru ya.` = Please don't die. The marker `ya` is not combined with the same clause's yes/no question marker `he`; if you are asking permission, ask a question rather than disguising a command as one.

## Social boundaries remain explicit

Resonance never overrides a refusal. `më` can be tender without entailing agreement. `pëla` is polite, and `pëlë` is more deferential, but neither means “the other person consented.” `lan` is an optional softening element usable where the addressee is free to decline. Translation should preserve that openness rather than overstate commitment.

## Confirming and repairing an answer

Direct `he` questions differ from the confirmation form `hëmi` and the rhetorical or hesitant strategies in later grammar chapters. An error can be corrected using the documented correction discourse forms, without changing the resonance mid-sentence. For an English translation, avoid treating every question as rhetorical or every alarmed `khar` as an accusation; context and explicit particles carry the distinction.
'''),
'clauses_and_counterfactuals':('Complex clauses: because, so that, if, although','11, 20–21, 24–25, 37, 55–60',r'''
## A clause is not automatically a sentence

Qaroshi permits several clauses under one opening resonance. A dependent clause introduced by `ko` (purpose), `ro` (reason), `wë` (ordinary if), `uro` (although), `yaro` (when), `ana` (after), or `ëna` (before) inherits the register of the independent sentence. The finite predicate in each clause remains at the end of **its own clause**, even when that clause is placed first. A comma in Romanization often helps a reader see the boundary; it is not a new native letter.

## Reason, purpose and condition

English “because” reports an explanatory cause; `ro` is the reason connector. English “so that” expresses a goal; `ko` introduces purpose. An ordinary `wë` condition is compatible with a realistic contingency. Do not translate these as synonyms: “I flew because I saw you,” “I flew so that I could see you,” and “If I fly, I will see you” assert very different relationships. The canonical plea `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.` clearly separates the requested action from the hoped-for purpose.

## Real vs unreal premises

`wë` introduces ordinary conditional uncertainty: the event may occur. `wënu` explicitly identifies a counterfactual premise. A consequence can end with `qinë` to make the unreal-result reading explicit: `sen wënu mi goro-ki, mi wena-gu gura-yu qinë.` = “If I could fly, I would travel into the sky.” This avoids relying only on broad tense plus inferred evidence to get the English would/could distinction. An *even if* concession and an *unless* exception have their own particles and do not reduce to a simple positive `wë`.

## Information inside information

A reported proposition is introduced/closed according to the documented content-clause structure with `do`, while an embedded yes/no alternative can be introduced with `qona`. A relative clause comes before the noun it describes and ends with `sha`. These are not interchangeable: one describes a **noun**, one supplies the **content** of thinking/speaking, and one embeds a **question**. Square brackets often used in pedagogical examples mark constituent boundaries; they are not native alphabet marks.

## Time relative to an event

Temporal connectors support before/after/when, and advanced clauses add since/until/by/whenever boundaries. These are logical relations between events, not all the same as putting `-te` on a verb. Use a time noun/adverb and a temporal clause when the exact anchor matters. A report about a past schedule may use a future-oriented form relative to a past reference time; the translator must recover the reference time from the whole construction.

## Read a multi-clause sentence in layers

Locate the single resonance. Split at the conjunction into clauses, but keep each predicate with its own arguments. Decide whether the relation is cause, purpose, concession, condition or time. Identify whether a condition is counterfactual. Finally combine the translated pieces into natural English, preserving any evidential or stance particles that apply to the whole utterance.
'''),
'evidence_information':('Evidence, information structure, uncertainty, and scope','10, 22–25, 39–41, 51–57, 61–64',r'''
## Three independent questions

A careful Qaroshi statement answers three questions separately: **What is being claimed? How does the speaker know it? How does the speaker frame saying it?** The predicate answers the first; an optional evidential such as `si`, `hu` or `ye` addresses the second; sentence-initial resonance addresses the third. `zher` signals suspicious/uncertain delivery, but does not tell you whether the claim was witnessed. `sen` presents a neutral sentence, but does not guarantee it was independently confirmed.

## The evidential trio

`si` means the speaker directly witnessed/sensed the event. `hu` means reported or learned from another source. `ye` means inferred or calculated. In `sen sa goro-te si.` / `sen sa goro-te hu.` / `zher sa goro-te ye.`, the base event is flight in the past, but the source and speaker stance differ. The evidential follows the predicate and precedes `he` if the sentence is an independent question.

## Certainty is a separate axis

A witnessed event may be recalled uncertainly; an inference may be highly confident. Use degree or uncertainty expressions when the strength of belief matters. Do not make `hu` automatically mean false or `ye` automatically mean weak. For modern scientific or technical translation, preserve whether something is measured, estimated, reported, assumed or predicted, because these are often substantive claims.

## Topic, focus and alternative sets

A topic ending `-së` frames what is being talked about; it does not itself make a noun an object. Focus devices can contrast one alternative with another (“this one, not that one”) or limit a claim to a subset. Quantifiers such as *all*, *each*, *both*, *no one* and *except* interact with negation and comparison. Translate their scope deliberately: “Not everyone arrived” need not mean “Everyone failed to arrive.” A smooth English sentence is not acceptable if it reverses these distinctions.

## Reported versus exact speech

Quoting a previous speaker word-for-word differs from paraphrasing that speaker. The later grammar distinguishes an exact-quotation introducer from a paraphrase indicator, and the quoted Qaroshi sentence keeps its own required resonance. If quoting a foreign-language sentence, keep it as foreign text rather than forcing a fake Qaroshi opening marker on that foreign sentence. In research, journalism and legal reporting this distinction changes what the author is claiming to know.

## When in doubt

In translation, preserve a documented ambiguity rather than silently assigning a narrower interpretation. An English note (“apparently,” “according to the report,” “I saw”) is often more faithful than dropping the evidential or treating it as a lexical part of the action. Conversely, avoid inserting a certainty level merely because a statement begins with a dramatic resonance.
'''),
'number_time':('Numbers, calendars, measurements, and technical notation','13, 15, 32, 58–62',r'''
## Two number-writing contexts

Qaroshi has a traditional base-six numerical system. The small lexical numerals include `ën` zero, `ka` one, `po` two, `dë` three, `zhu` four, `rë` five; `zhe` names six, `zhewa` thirty-six, and `zhewawa` two hundred sixteen. In a technical document, international Arabic numerals are also acceptable as notation. A bare digit string is ambiguous about radix if the context might mix systems, so annotate bases when precision matters.

## Working a conversion rather than guessing

To read `244₆`, compute `2×6² + 4×6¹ + 4×6⁰ = 72 + 24 + 4 = 100₁₀`. To express 100 decimal in base six, divide by six: 100 gives quotient 16 remainder 4; 16 gives quotient 2 remainder 4; 2 gives quotient 0 remainder 2. Read the remainders in reverse, yielding `244₆`. This mathematical equivalence does not mean that the everyday spoken Qaroshi name of the number is obtained by reading an international digit string as an English word.

## Dates, times and measured quantities

ISO 8601 dates and 24-hour clocks are permitted as technical notation; `2026-11-14` and `19:46` are metadata representations, not additions to the 26 native alphabet. The unit abbreviations `m`, `s`, `V`, `GB`, and so forth can remain quoted international technical symbols where interoperability is important. Do not silently re-interpret physical units as ordinary Qaroshi headwords: a letter symbol in a formula is not automatically the native letter with the same Latin shape.

## Exactness, approximation, and upper/lower limits

Precision is part of semantics. The ordinary adverbs `gara` exact and `ngara` approximate show different commitments. “At least,” “at most,” “about,” “under,” “over,” and “exactly” cannot all collapse into a single number phrase if used in a scientific claim or deadline. Later grammar chapters distinguish approximation and quantitative boundaries. An honest translation keeps the qualifier even when the number remains in familiar Arabic digits.

## Time as event relation

Calendar time, event time, and grammatical tense are separate. A past event can be relevant to a future deadline, and “until the meeting” expresses a boundary rather than the tense of the action alone. Use documented connectors for since, until, before, after, and whenever. When a clock time alone does not settle whether something happened, avoid inferring the tense from the timestamp without a contextual reference point.

## Check an unfamiliar measurement

Identify the measured physical quantity, the unit, the numeral base, the conversion factor, and the degree of certainty. Write them into the English gloss explicitly. If a software or scientific interface expects decimal numbers, preserve its notation in a quotation or technical field; do not turn every numeral into a culturally stylized spoken phrase in data exchange.
'''),
'writing_script':('Native script, transliteration, typography, and names','1, 30, 33–34, 46, 50, 69',r'''
## An alphabet of sounds

The original Nardoragon script consists of 26 handwritten glyphs. Each native glyph corresponds to one unit of the Qaroshi phoneme inventory, even when Romanization writes it as two characters (`sh`, `zh`, `kh`, `ng`). This makes the native alphabet a phonemic writing system, not a character-by-character cipher for English. Qaroshi Romanization is a representation of Qaroshi sounds; English spelling is not a safe input to the native-glyph converter.

## Procedure for transliterating a Qaroshi word

Normalize text to Unicode NFC, split Romanized writing into the longest recognized graphemes, preserving the four multi-letter native graphemes as indivisible units, then replace each with its corresponding original image glyph. Preserve word boundaries, ordinary punctuation and explicitly quoted foreign material as separate text/notation. If a word contains a Latin letter not in the Qaroshi native inventory, report it instead of silently inventing a native equivalent.

## Marking grammatical boundaries

Teaching text often uses hyphens in `mi-na`, `mara-tu`, `goro-te-se` to expose morphemes. These are **not** extra letters or obligatory native punctuation and can be omitted in fluent writing. A linguist can retain them in an interlinear edition to show structure, but a normal message need not expose all suffix boundaries. Conversely, hyphen omission can make some analyses less obvious; the dictionary and grammatical context must decide where the stem ends.

## Letter identity versus calligraphic freedom

The glyph artwork contains crossings and loops that distinguish original forms. Writing may stretch or stylize them, but different letter forms should remain recognizable, especially those mapped to distinct vowels `e` and `ë`, or consonants `k` and `q`. If a visual font is eventually produced, it must be checked against all 26 shapes and actual character boundaries, not merely against decorative sample words.

## Names and foreign quotation

A proper name has a pronunciation in its source language, and a faithful Qaroshi transcription must start from that pronunciation rather than blindly turning each English letter into an unrelated Qaroshi glyph. Foreign product names, handles, file paths, code, and addresses can remain quoted external strings in technical writing. Such quoted strings do not extend the alphabet or require Qaroshi phonotactic repair unless the writer intentionally adapts the name as a Qaroshi word.

## Reliable file exchange

UTF-8 is preferred, and `ë` should not be replaced with `e` as a convenience. For ASCII-only systems, specify a reversible escaping/transliteration scheme rather than silently losing information. The offline wiki can produce a visual PNG of native glyph text; this is an image, not yet a Unicode-encoded editable native-font string. Keep Romanized originals when machine searching, accessibility and copy/paste matter.
'''),
'conversation_social':('Conversation skills: relationships, care, and boundaries','16, 31, 40–43, 63–66',r'''
## Conversational intent has several layers

A natural message contains more than a dictionary predicate. Qaroshi can distinguish social stance with obligatory resonance, politeness with `pëla` or `pëlë`, the speech act with `he` or `ya`, and a consent-sensitive softener such as `lan`. The combination lets a Nardoragon ask a question with concern, make a serious promise while grateful, or decline without changing grammatical gender. It is important not to overread the register alone as an admission of romance or legal commitment.

## Greetings and openings

`zha ha, mara!` is a lively greeting; `nëm ha, mara.` is calm. A greeting fragment used by itself has a conventional discourse role, while complete follow-up sentences carry their own opening resonance. A friendly exchange may move through curiosity (`hë`), thanks (`hol`), and tenderness (`më`) in separate complete sentences, because each independent sentence requires one marker.

## Affection is semantically specific

`nashi` signifies deep care and need not be romantic. `mali` is available when romantic love is specifically intended; `lani` expresses familial love. `më` frames tenderness, while `wen` conveys missing or longing. Words and resonance cooperate but do not replace each other. Translating “I cherish you deeply” as “I am in love with you” would add a stronger relationship claim than `nashi` alone supports.

## Questions about permission

Permission and ability are different predicates. `hë mi ti-m mërali-ho he?` asks whether the speaker may hug the other person; the permissive `-ho` matters. It should not be silently replaced by ability `-ki`. Where the addressee can refuse, polite framing makes that social fact transparent. A reply denying permission must be honored even if the earlier request was affectionate or playful.

## Promises, plans and wishes

`qor mi ti-m daru-yu.` means “I will protect you” with solemn delivery. `dal` would highlight resolve and action; `më` would foreground tenderness. A wish using `yëmë` is different from an offer, command or commitment. In formal contexts, use explicit lexical content for who promises what, when and under what condition; a serious resonance does not automatically create a legal contract.

## Interpreting short replies

Some conversational fragments such as `shë` yes and `nu` no stand alone in speech. When presented as complete written sentences, the reference examples give them a resonance (`sen shë.`, `qor nu.`). Distinguish the particle `nu` used as a negative answer from the same particle directly before a finite predicate. A learner should not rewrite a refusal into agreement merely to make a conversation seem smoother.
'''),
'modern_technical':('Modern technical Qaroshi: precise prose and terminology','32–34, 45–47, 50, 62, 68–70',r'''
## Specialized words need specialized definitions

The unified lexicon covers computation, privacy, medicine, engineering, science, public life and other contemporary topics. Many long words are transparent modifier–head compounds; their last member identifies the head concept, while preceding material narrows it. An English gloss does not give unrestricted permission to use the term for every English homonym. “Interest” as borrowing cost and “interest” as personal curiosity are separate senses; preserve the specialized one actually named by the entry.

## What to leave unchanged in code and data

In a technical document, code fragments, command flags, IP addresses, file paths, hashes, international units and product names may remain quoted external strings. Do not send arbitrary English or code through the original-glyph converter, because it maps phonemes, not English keyboard characters. For accessibility, include textual Romanization beside a native-script screenshot; a glyph PNG by itself is not machine-readable Qaroshi.

## How to write a verifiable instruction

Separate a statement of fact from a request to act. A technical imperative requires an opening resonance (often `sen` or `dal` according to tone), explicit participants/objects where safety depends on them, and a proper command `ya` rather than simply ending with a verb. Preserve preconditions, time limits, permissions, uncertainty and irreversible consequences in separate clauses if necessary. A tone marker is not a substitute for expressing a concrete precondition.

## Reporting results and sources

Engineering notes should distinguish a directly observed result (`si`), a result reported by another system or observer (`hu`), and an inference (`ye`). A test passing and a hypothesis seeming plausible are not identical. In statistics and scientific reports, `gara` exactly and `ngara` approximately matter, and equations should retain internationally understood notation when precision/interoperability requires it.

## Glossing modern idioms

A long technical English noun phrase may be most naturally represented by a standard Qaroshi compound, but new semantic combinations can also need a relative or content clause. Check the dictionary for an exact sense before coining a transparent compound. Avoid inventing a word merely by concatenating English concepts in arbitrary order. Existing compounds are lexical items with stable components, not promises that every combination of roots is idiomatic.

## Translation and QA checklist

Before publication, verify the dictionary entry, POS, head/modifier boundaries, glyph-valid spelling, broad IPA, suffix order, scope of negation, evidence type, numeral base, and intent. For documentation, include a literal gloss or short translator note wherever a reader could confuse ability, permission, requirement, approximation, ownership or reported evidence. This is more important than producing overly literal sentence rhythm.
'''),
'dictionary_compounding':('Dictionary mastery: senses, compounds, and morphology','14, 26, 30, 33, 35, 47, 49–50, 67–68',r'''
## Not every string is a new dictionary word

A dictionary **headword** is a lexical item; a **compound** may have a specialized conventionally documented meaning; a **grammatical inflection** is produced from a headword and an ending. `goro`, `goro-te`, and `goro-te-se` should not be counted as three unrelated lexical senses simply because the surface strings differ. Conversely, `qaroshi` has a lexicalized meaning tied to the language and is not merely a random phonetic concatenation.

## Read compound structure right-to-left

In ordinary modifier–head compounds the last element is the semantic head. `qaro + shi` literally combines Nardoragon with voice/language to name Qaroshi. The left component refines the head. A multi-part compound may be semantically more specialized than the literal root meanings; the dictionary's recorded gloss is authoritative for the entry. Do not automatically assume an English calque with similar-looking components has the same technical meaning.

## Anatomy of a dictionary article

Each entry provides a spelling, part of speech, English gloss, topic/domain, pronunciation (broad IPA, stressed syllables and English-like sound-out), and any recorded component or note. A gloss is not a full encyclopedic description or a list of every possible use. Related-entry links are topical neighbors and **not necessarily synonyms**. A dictionary word with no exact example in the phrasebook is still a word; the missing example should not be replaced by a claim of attested context.

## Word class matters

An English keyword may correspond to a Qaroshi noun in one sense and a verb/adjective in another. In translation, first decide the target grammatical function. A word labeled as a noun cannot automatically be dropped into a verbal predicate because English permits “to message” from “message.” Use a recorded verb or a documented derivational rule where possible. Do not stack productive suffixes beyond the permitted templates as if every formal combination were independently licensed.

## How to evaluate a new sense

Check (1) whether a dictionary headword already expresses the meaning, (2) whether the requested English is polysemous, (3) whether a documented modifier–head compound provides the intended sense, and (4) whether a clause expresses it more accurately. A new entry should have a clear one-sentence definition, POS, domain, component breakdown if compounded, a reproducible phonetic representation, and an example of usage. Duplicate spellings with conflicting senses require explicit homonym handling, not accidental overwrite.

## Search without confusing forms

The wiki's dictionary lookup is spelling- and gloss-based, with accent-tolerant search. Searching `gero` can find `gëro`, but this convenience does not make the spellings equivalent in Qaroshi orthography. In actual written language, `e` and `ë` are distinct. The native script converter likewise expects a valid Qaroshi form, not a spelling approximation from an English keyboard.
'''),
'editing_troubleshooting':('Grammar clinic: debugging a difficult sentence','17–20, 27–30, 34, 39, 47, 70',r'''
## Diagnose in a fixed order

When a sentence feels wrong, inspect its structure before changing vocabulary. The recommended order is resonance → clause boundaries → subjects → object/case roles → predicate form → negation → evidential and question/request ending. This hierarchy catches many errors that English-trained writers miss. A grammatical-looking translation can still be semantically wrong if it swaps who acted and who was affected.

## Problem: the sentence has no resonance

A complete sentence beginning directly with `mi` or `ti` is missing the obligatory opening marker. Choose a register from intended delivery. For a matter-of-fact statement use `sen`; for affectionate vulnerability use `më`; for a real information-seeking question `hë` is often appropriate. Do not confuse the first `hë` with final interrogative `he`: they are different forms and fill different slots.

## Problem: too many suffixes

A finite verb admits one voice, one tense, one aspect, one modality and an optional tender-manner suffix in the documented order. Stacking two competing modal or aspect endings in one verb is not ordinary standard syntax. Express nuanced combined modalities with separate clauses or appropriate lexical material. A noun similarly takes only one case; several roles require several phrases.

## Problem: English word order leaks through

“Give water to a friend” can be represented as subject + recipient-dative + water-object + give. An English-influenced “I give water friend” omits role suffixes and is hard to parse. Move the predicate to the end of its clause and label noun phrase roles explicitly. Pronouns take the same case endings as other nominals.

## Problem: the wrong kind of question

Direct interrogative `he` belongs at the end of a question, whereas embedded `qona` or reported content `do` is used inside a larger statement. A request uses `ya`, not `he`, and a wish uses the optative construction rather than an imperative. Keep the intended speech act stable before choosing a suffix or punctuation mark.

## Problem: semantic over-translation

`mi-na` is association/possession, not automatically legal ownership; `më` is affection, not automatically romance; `hu` is reported evidence, not automatically unreliability; `-ki` potential, `-ho` permission and `-du` necessity are not interchangeable. Whenever an English translation adds a claim that none of the original words carry, revise it or mark it as interpretation rather than literal meaning.

## A final annotation pass

Write a literal segmented gloss and align it token-by-token with the Qaroshi. If each case, suffix, register and connector has no explanation in the analysis, investigate. Then write one natural English sentence preserving the same facts, limits, uncertainty and interpersonal intent. A clean parse is stronger evidence than the sentence merely sounding plausible in English.
'''),
'culture_pragmatics':('Nardoragon communication and interpretive context','2, 16, 31, 36, 41–44, 51, 63–65',r'''
## What can be described responsibly

The Qaroshi reference documents distinctive Nardoragon terms for bodies, wings, tails, aerial movement, roosts, shelter and close relationships. It also documents typed resonance as a grammatical convention. These facts allow grounded interpretation of example sentences; they do not establish a complete empirical ethnography of all Nardoragon communities. Avoid inferring a universal rite, caste system, spiritual belief or specific social history merely from one dictionary term.

## Wings, shelter, and space

Terms such as `banu` wing, `raso` tail, `wena` sky, `naro` home and the movement `goro` fly are central to Nardoragon expression. Directional cases (`-gu`, `-de`, `-lo`) make a flight route easier to specify than a vague English preposition. Distinguish aerial motion (`goro`) from generic travel (`gura`) where the action matters. A request to stay (`nëra`) is not itself an instruction to land or remain physically immobile.

## Chosen family and relationships

`runa` chosen family and `mara` friend represent social relationships without inherent grammatical gender. `nashi` deep care may apply in family, friendship or romance; `mali` and `lani` are more specific lexical choices. Written resonance can mark tenderness or longing even when the relationship term is generic. Do not treat a tender message as proof of exclusive partnership.

## Respect and directness

Respect can be expressed lexically, through deferential request forms and through choosing the social stance in resonance. An authoritative or solemn `qor` statement is not necessarily an order. A soft `më` request can still create pressure unless it explicitly leaves room for refusal. Good translation preserves the actual request, wish, warning, promise or refusal rather than converting every caring message into a command.

## Interpreting Nardoragon art or poetry

Literary uses of `zhaloshi` (fire-voice) or `wenabanu` (sky-wing) may take on metaphorical associations, but a dictionary only records their basic documented meaning. In poetic translation, it is legitimate to show literal components in a note and provide a natural metaphorical line, provided the note clearly separates inference from lexicon. Resonance is especially important in a poem where two otherwise identical sentences can convey longing versus joy.

## Documentation boundaries

A language manual can teach how a form is written, sounded out and parsed without claiming a complete observation of how every Nardoragon actually speaks. Accent, frequency, regional dialect, ceremonial usage and oral performance remain distinct from rule-based pronunciation and literary interpretation. Preserve those distinctions as Qaroshi scholarship and writing grow.
'''),
}

# The existing standard phrasebook is the source of all graded exercises.
SECTIONS={
'getting_started':['S00001','S00003','S00004','S00013','S00021','S00033','S00064','S00079'],
'pronunciation_lab':['S00021','S00035','S00064','S00080','S00094','S00097','S00098','S00103'],
'resonance_mastery':['S00021','S00022','S00023','S00024','S00027','S00034','S00043','S00048'],
'sentence_anatomy':['S00024','S00034','S00035','S00064','S00082','S00085','S00086','S00095'],
'nouns_cases':['S00009','S00030','S00033','S00036','S00037','S00064','S00082','S00085','S00086','S00087','S00088'],
'verb_workshop':['S00014','S00034','S00059','S00060','S00061','S00062','S00071','S00080','S00092','S00095'],
'asking_and_negating':['S00003','S00005','S00013','S00019','S00032','S00035','S00056','S00089','S00098','S00099','S00100'],
'clauses_and_counterfactuals':['S00035','S00038','S00095','S00096','S00097','S00851','S00852','S00853'],
'evidence_information':['S00095','S00096','S00097','S00034','S00047','S00056','S00079','S00085'],
'number_time':['S00059','S00060','S00061','S00062','S00094','S00101'],
'writing_script':['S00001','S00003','S00021','S00035','S00064','S00079','S00095','S00104'],
'conversation_social':['S00001','S00002','S00015','S00016','S00024','S00025','S00026','S00032','S00034','S00055'],
'modern_technical':['S00191','S00192','S00193','S500001','S500002','S500003','S5V00001','S5V00002'],
'dictionary_compounding':['S00013','S00014','S00037','S00079','S00085','S00191','S500001','S500002'],
'editing_troubleshooting':['S00003','S00004','S00005','S00034','S00035','S00060','S00061','S00095','S00096','S00097'],
'culture_pragmatics':['S00024','S00026','S00029','S00033','S00037','S00079','S00082','S00085','S00094'],
}

index=[]
for slug,(title,chapters,raw) in GUIDES.items():
  example_ids=SECTIONS[slug]
  assert all(x in PHRASE for x in example_ids),[x for x in example_ids if x not in PHRASE]
  lines=[f'# {title}', '',f'> **Deep reference** · Related grammar chapters: {chapters} · All examples below are from the unified Qaroshi phrasebook.', '', textwrap.dedent(raw).strip(),'', '## Read and listen mentally: annotated reference examples','']
  for eid in example_ids:
    p=PHRASE[eid]
    lines+=[f'### {eid}: {p["english"]}',f'**Qaroshi:** `{p["qaroshi"]}`',f'**IPA:** `{p["ipa"]}` · **Stress guide:** `{p["reading"]}` · **Sound-out:** `{p["sound_out"]}`',f'**Usage note:** {p["note"] or "Refer to the grammar chapter for the construction and its scope."}','','']
  lines+=['## Guided retrieval practice','','These exercises use exactly the forms shown above. First cover the answer, then write the full sentence with its resonance, case endings, and closing particles. Verify spelling against the dictionary rather than guessing from English.','']
  for i,eid in enumerate(example_ids[:6],1):
    p=PHRASE[eid]
    lines.append(f'{i}. Translate into Qaroshi: **{p["english"]}**')
  lines+=['','<details><summary>Answer key: reveal after trying</summary>','']
  for i,eid in enumerate(example_ids[:6],1):
    p=PHRASE[eid]
    lines.append(f'{i}. `{p["qaroshi"]}` · {p["ipa"]}')
  lines+=['','</details>','','## Study checkpoint','','Before leaving this chapter, explain in your own words how its central grammatical distinction changes the truth conditions or social intention of a sentence. Then alter **one** feature of an example (resonance, tense, case, negation, evidential, or speech act) and check the resulting form in the 70-chapter grammar. A good translation must preserve what was said and how it was framed.','']
  (DOC/f'{slug}.md').write_text('\n'.join(lines),encoding='utf8')
  index.append({'id':slug,'title':title,'chapters':chapters,'examples':len(example_ids),'path':f'docs/deep_guides/{slug}.md'})

# Make a progressive 16-lesson course, each using ten selected existing sentences.
COURSE=[
('Recognize a complete sentence','Resonance, greetings, short assertions', ['S00001','S00002','S00003','S00004','S00005','S00006','S00007','S00008','S00011','S00012']),
('Names, identity, and speaking','Present noun predicates, pronouns, who speaks', ['S00009','S00010','S00013','S00014','S00017','S00018','S00019','S00020','S00021','S00022']),
('Care and interpersonal stance','Warm Hum, romantic/familial senses, requests', ['S00023','S00024','S00025','S00026','S00027','S00028','S00029','S00030','S00031','S00032']),
('Requests, wishes, and commitment','Politeness, command ending, future, purpose', ['S00033','S00034','S00035','S00036','S00037','S00038','S00039','S00040','S00050','S00055']),
('State and emotion','Adjective predicates, emotion vocabulary, negation', ['S00041','S00042','S00043','S00044','S00045','S00046','S00047','S00048','S00049','S00056']),
('Tense and habituality','The suffixes -te, -se, -në; habit vs ongoing', ['S00051','S00052','S00053','S00059','S00060','S00061','S00062','S00071','S00074','S00078']),
('Food, objects, and daily life','Direct objects and everyday predicates', ['S00063','S00064','S00065','S00066','S00067','S00068','S00069','S00070','S00072','S00073']),
('Wings, weather, and the sky','Nardoragon body, instrument and plural cases', ['S00079','S00080','S00081','S00082','S00083','S00084','S00085','S00092','S00093','S00094']),
('Location and movement','-lo, -gu, -de and wh-questions', ['S00074','S00075','S00086','S00087','S00088','S00089','S00090','S00091','S00100','S00101']),
('Evidence and reports','si, hu, ye and resonance contrasts', ['S00095','S00096','S00097','S00098','S00099','S00102','S00103','S00104','S00047','S00056']),
('Question structures','Direct questions vs embedded forms', ['S00003','S00009','S00013','S00019','S00032','S00056','S00098','S00099','S00100','S00105']),
('Digital vocabulary I','SOV paradigms with modern devices', ['S00191','S00192','S00193','S500001','S500002','S500003','S400024','S400025','S5V00001','S5V00002']),
('Complex predicate morphology','Ability, future, past, lexical actions', ['S00034','S00051','S00059','S00060','S00061','S00062','S00080','S00095','S5V00001','S5V00003']),
('Nuance in technical assertions','Precise modern concepts and careful evidence', ['S300469','S300470','S300471','S400182','S400183','S400184','S500001','S500002','S500003','S00097']),
('Advanced clause relations','Counterfactuals, optatives, controlled embedded meaning', ['S00851','S00852','S00853','S400593','S400594','S400595','S00035','S00038','S00095','S00096']),
('Fluent editing and comparison','Apply all grammar layers deliberately', ['S00003','S00024','S00032','S00034','S00035','S00061','S00085','S00097','S00851','S400595']),
]
# One lesson includes a reading worksheet and both types of retrieval exercises.
parts=['# Qaroshi graded course · 16 detailed lessons','','A complete route from first sentence to nuanced technical and literary translation. This is a **learning workbook**, not a proficiency certification or a claim about native-speaker frequency. Every modeled sentence is reproduced from the unified phrasebook, with stable IDs, phonetics and established English glosses.','','## How to use each lesson','','Read the goal, identify the grammar forms, and work through the comprehension table. Cover the English and translate from Qaroshi; cover Qaroshi and reconstruct from English. Repeat as spaced practice, and always check the opening resonance and speech-act ending. Each lesson includes a teacher key, so a self-learner can verify each whole sentence.','']
for n,(title,skill,ids) in enumerate(COURSE,1):
  parts += [f'## Lesson {n:02d} · {title}', '',f'**Target skills:** {skill}. **Source:** existing reference sentences {", ".join(ids)}.','',
  '### Learning procedure','',
  '1. Read all ten examples aloud, using the IPA as the precise phoneme guide and capitals in the reading as a stress cue.','2. Mark the first word of each complete sentence; explain its register rather than simply calling it “tone.”','3. Underline subject and direct object where relevant. Parse hyphenated suffixes before translating.','4. For every verb, state whether it is unmarked, past, future, ongoing, habitual, able, permitted or obligatory.','5. Translate the full sentence into natural English; retain questions, requests, evidentials and participant roles.','',
  '### Reading examples','', '| ID | Qaroshi | English | IPA |','|---|---|---|---|']
  for eid in ids:
    p=PHRASE[eid]
    parts.append(f'| {eid} | `{p["qaroshi"]}` | {p["english"].replace("|","/")} | `{p["ipa"]}` |')
  parts+=['','### Check your understanding','',
    'A. Without looking at the English column, translate the following. Keep informational content and speech act, not merely a loose paraphrase.','']
  for j,eid in enumerate(ids[:5],1): parts.append(f'{j}. `{PHRASE[eid]["qaroshi"]}`')
  parts+=['','B. Translate into **complete Qaroshi sentences**, including written resonance and grammar endings.','']
  for j,eid in enumerate(ids[5:],1):parts.append(f'{j}. {PHRASE[eid]["english"]}')
  parts+=['','<details><summary>Teacher answer key: open only after completing A and B</summary>','','**A. Qaroshi → English**']
  for j,eid in enumerate(ids[:5],1):parts.append(f'{j}. {PHRASE[eid]["english"]}')
  parts+=['','**B. English → Qaroshi**']
  for j,eid in enumerate(ids[5:],1):parts.append(f'{j}. `{PHRASE[eid]["qaroshi"]}` · `{PHRASE[eid]["reading"]}`')
  parts+=['','</details>','','### Form-awareness task','','Choose two models above. Change **only** the resonance and explain what stays literally true. Then choose a third, and alter an applicable verb ending or noun case in accordance with the grammar; identify which English meaning would change. Do not improvise a new ending if the original already has an incompatible member of that category.','','---','']
(DOC/'graded_course.md').write_text('\n'.join(parts),encoding='utf8')
index.insert(0,{'id':'graded_course','title':'Guided course · 16 lessons','chapters':'all','examples':160,'path':'docs/deep_guides/graded_course.md'})

# A practice book focused on error diagnosis, with sourced answers.
troubles=[
('`mi ti-m nashi.`','Missing resonance at the beginning; use the register appropriate to intention; `më mi ti-m nashi.` models affection.'),
('`hë ti haro.`','If a direct yes/no question is intended, add terminal `he`: `hë ti haro he?`. Otherwise the utterance is an incomplete question model.'),
('`sen mi -te goro.`','The tense suffix attaches after the verb root, not as a separate word: `sen mi goro-te.`'),
('`sen mi qaro-gu gura.`','This denotes travel toward a Nardoragon. If the intent is travel *from* them, the case is `-de`; do not confuse the two.'),
('`më mi ti-m nashi he ya.`','A question ending and a request ending do not coexist on the same clause. Choose the intended speech act.'),
('`sen mi nu-te goro.`','Negation `nu` is a separate particle immediately before the entire inflected predicate, not an internal verbal suffix.'),
('`sen qaro-ri goro-te hu si.`','Do not stack competing basic source-of-evidence endings as though they were conjugations; clarify whether the information is witnessed or reported.'),
('`më mi ti-m nashi. ti haro.`','The second full sentence needs a new resonance: e.g. `më ti haro.` when it too is affectionate.'),
('`sen mi mara-lo kima-m pëli.`','If the friend receives water, use dative `-tu`, not locative `-lo`: `sen mi mara-tu kima-m pëli.`'),
('`më pëla ti nu zëru he?`','A request uses `ya`; a genuine yes/no question uses `he`. Do not treat punctuation as a substitute.'),
]
wb=['# Qaroshi practice and editing workbook','','This workbook is meant to be used **after** the 16-lesson course. It includes 10 error diagnoses, a grammar-to-English checklist, and a 36-sentence mixed assessment drawn from the established phrasebook. Do not use the mistakes below as valid speech models.','',
'## The editor’s ten traps','','For each deliberately flawed line, identify the error and explain why the suggested correction is more accurate. Some examples are schematic, and the critique explicitly notes when context determines the right revision.','']
for i,(bad,correct) in enumerate(troubles,1):wb+= [f'### Trap {i}',f'**Check this line:** {bad}',f'**Diagnosis:** {correct}','']
wb+=['## Mixed translation assessment','','Translate these without the adjacent English. The source IDs allow direct comparison to the online/offline phrasebook, but the key below is the fastest way to self-check.','']
assess_ids=['S00003','S00005','S00009','S00013','S00024','S00027','S00032','S00033','S00034','S00035','S00045','S00056','S00059','S00060','S00061','S00062','S00064','S00074','S00079','S00082','S00085','S00086','S00087','S00088','S00095','S00096','S00097','S00098','S00099','S00100','S00101','S00103','S00851','S00852','S400593','S400595']
for i,eid in enumerate(assess_ids,1):wb.append(f'{i}. `{PHRASE[eid]["qaroshi"]}`')
wb+=['','<details><summary>36-sentence answer key</summary>','']
for i,eid in enumerate(assess_ids,1):wb.append(f'{i}. **{PHRASE[eid]["english"]}** · {eid}')
wb+=['','</details>','','## Rubric for self-evaluation','','A fully accurate answer preserves participants, direction and possession; event time/aspect; ability versus permission versus obligation; negation and quantifier scope; sentence-initial resonance; speech-act ending; and evidence attribution. Natural English wording can vary while these grammatical distinctions remain constant. Partial credit is appropriate for correct semantic content when the emotional frame is omitted, but that omission should still be noticed in the analysis.','']
(DOC/'workbook.md').write_text('\n'.join(wb),encoding='utf8')
index.append({'id':'workbook','title':'Practice workbook · 46 checks','chapters':'all','examples':36,'path':'docs/deep_guides/workbook.md'})

# A detailed 3-way segmented reference, using only canonical examples.
parse_ids=['S00003','S00024','S00032','S00033','S00034','S00035','S00059','S00060','S00061','S00062','S00064','S00079','S00082','S00085','S00086','S00087','S00095','S00096','S00097','S00851','S00852']
analyses={
'S00003':'`hë` inquiry resonance; `ti` second-person subject; `haro` adjective predicate “well”; `he` direct yes/no question ending. No present “are” is required.',
'S00024':'`më` Warm Hum; `mi` subject; `ti-m` second-person object; `nashi` lexical predicate of deep care. Warm Hum does not prove romance.',
'S00032':'`hë` inquiry register; `mi` subject; `ti-m` object; `mërali-ho` hug + permission `-ho`; `he` asks for permission, not physical ability.',
'S00033':'`më` affectionate delivery; `pëla` please; `mi-wa` “with me” comitative; `nëra` remain; `ya` request ending. Unlike an English wish, this directly requests staying.',
'S00034':'`qor` solemn commitment; `mi` subject; `ti-m` patient; `daru-yu` protect + future. A promise needs its actual content, not just solemn resonance.',
'S00035':'One opening `më` covers both clauses. `sëna nu zëru ya` is emphatic negative request; `ko` introduces the purpose; `mi-wa` with me; `nëra-ki` “able to stay.”',
'S00059':'`sen` neutral; `mi` subject; `shërami-yu` sleep + future. Time reference is after contextually relevant now.',
'S00060':'`sen` neutral; `mi` subject; `shërami-te` sleep + past. Nothing in the suffix alone says whether the event was completed in a special viewpoint.',
'S00061':'`sen` neutral; `mi` subject; `shërami-te-se` sleep + past + progressive. The event is viewed as ongoing in the past.',
'S00062':'`sen` neutral; `mi` subject; `shërami-në` habitual; a recurring pattern is asserted, not necessarily activity right now.',
'S00064':'`sen` neutral; `mi` subject; `kima-m` water direct object; `këmë` verb drink. Object-before-verb order.',
'S00079':'`sen` neutral; `qaro-ri` plural subject; `goro` fly. A general assertion has no overt tense suffix.',
'S00082':'`sen` neutral; `sa` subject; `banu-shi` wing + instrument; `goro` fly. `-shi` is means here, not a companion.',
'S00085':'`sen` neutral; `naru` inclusive we; `sëra-ri-m` stars plural and direct object; `wena-lo` location in the sky; `tika` see.',
'S00086':'`sen` neutral; `mi` subject; `naro-gu` goal toward home; `gura` travel. Do not substitute locative when motion toward is intended.',
'S00087':'`sen` neutral; `mi` subject; `naro-de` source away from home; `gura` travel. The contrast to `-gu` changes direction.',
'S00095':'`sen` neutral; `sa` subject; `goro-te` flew; `si` firsthand evidential. This is a past event with witnessed support.',
'S00096':'`sen` neutral; `sa` subject; `goro-te` flew; `hu` reported evidential. The source changed, not the event.',
'S00097':'`zher` uncertain/suspicious stance; `sa` subject; `goro-te` past; `ye` inferential evidential. Stance and source remain distinct categories.',
'S00851':'`sen` neutral; `wënu` counterfactual premise; `goro-ki` can fly; consequent `gura-yu` will travel; `qinë` marks unreal projected result.',
'S00852':'`më` Warm Hum; `yëmë` optative wish; `ti` subject; `haro` safe/well predicate. This is a wish, not a direct imperative.',
}
ps=['# Detailed sentence anatomy atlas','','Twenty-one source-backed parses selected to show grammar in context. The Qaroshi sentence, its unchanged canonical translation, and the broad IPA are given beside a human-readable morphological analysis. The analyses describe grammatical meaning, not new dictionary entries.','','## How to read the atlas','','Read each original aloud. Cover the English and state what case and verb endings you can identify. Then check the grammatical analysis and compare the natural English. Finally repeat the line without hyphens to ensure that you do not treat teaching separators as separate native letters.','']
for n,eid in enumerate(parse_ids,1):
 p=PHRASE[eid];ps+=[f'## {n}. {p["english"]}', '',f'**Original:** `{p["qaroshi"]}`',f'**IPA:** `{p["ipa"]}` · **Stress:** `{p["reading"]}`',f'**Analysis:** {analyses[eid]}','',f'**Natural English:** {p["english"]}','','---','']
(DOC/'sentence_atlas.md').write_text('\n'.join(ps),encoding='utf8')
index.insert(1,{'id':'sentence_atlas','title':'Sentence atlas · 21 full parses','chapters':'all','examples':21,'path':'docs/deep_guides/sentence_atlas.md'})

# A roadmap index includes source citations to the original standard by chapter ID.
contents=['# Qaroshi learning library · unified reference 5.1','','This learning library supplies step-by-step interpretation of the same established Qaroshi 5.0 grammar. The dictionary, native letters, phonetics, 16 registers and 70 canonical grammar chapters are unchanged. Lesson translations are sourced to the existing corpus IDs; the additional explanations are pedagogical commentary, not alterations to the rules.','','## Suggested order','','1. Read **Start here** and **Pronunciation laboratory**.','2. Work through **Guided course, lessons 1–8**.','3. Study **Resonance**, **Sentence anatomy**, **Nouns/cases**, and **Verb workshop**.','4. Work through **Guided course, lessons 9–16**, using **Questions**, **Clauses**, and **Evidence** as needed.','5. Read **Translation**, **Dictionary mastery**, **Technical writing** and **Native script** for polished production.','6. Test yourself with the **Practice workbook**, then use the **Sentence atlas** to repair persistent errors.','','## Complete guide catalog','','| Guide | What it teaches | Related grammar |','|---|---|---|']
for row in index:contents.append(f'| [{row["title"]}]({row["id"]}.md) | Worked examples and recall practice ({row["examples"]} reference lines/tasks) | {row["chapters"]} |')
(DOC/'index.md').write_text('\n'.join(contents)+'\n',encoding='utf8')
(DOC/'guide_index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
# Release introspection metadata.
stat={'edition':'Unified Standard 5.1 — Deep Guide Edition', 'guides':len(index),'guided_lessons':len(COURSE),'atlas_parses':len(parse_ids),'workbook_sentence_tasks':len(assess_ids),'dictionary_unchanged':len(WORD),'corpus_unchanged':len(CORPUS),'new_grammar_rules':0, 'all_examples_from_reference_corpus':True}
(ROOT/'data/learning_library.json').write_text(json.dumps(stat,indent=2),encoding='utf8')
print(json.dumps(stat,indent=2))
