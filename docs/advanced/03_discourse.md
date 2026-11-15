# Discourse, conversation, politeness and pragmatic inference

A language is not only a set of isolated well-formed sentences. Qaroshi has a mature **typed-resonance** system that makes sentence stance visible, but interlocutors still have to manage turn-taking, reference, repair, disagreement, uncertainty and personal boundaries. The guidance below specifies how those mechanisms interact, while distinguishing strict grammar from ordinary pragmatic preference.

## 1. Turns are not sentences

A chat message may contain three independent sentences, each with its own resonance marker. One written paragraph can contain several sentences, and one sentence can contain subordinate clauses. `zha ha, mara! hë ti haro he? më mi ti-m nashi.` = Hello, friend! Are you well? I cherish you. The markers `zha`, `hë`, and `më` each govern their own sentence. In contrast, the `ko` purpose clause of `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.` inherits the single opening `më`.

For conversation logs, **each turn** should be associated with speaker identity, optional addressee, register, topic and discourse relation to the previous turn. A new speaker does not automatically share the previous speaker's evidential source or emotional intention.

## 2. Resonance as a grammatical commitment

Sixteen possible markers are mandatory, including `sen` neutral, `më` affectionate, `zha` playful, `qor` solemn, `hë` curious, `lën` shy, `sur` grieving, `rak` angry, `khar` alarmed, `yë` surprised, `nëm` peaceful, `wen` longing, `dal` determined, `rëm` proud, `hol` grateful and `zher` doubtful. None is a lexical translation of “I feel X.” The same objective proposition may have different interactional consequences under different resonances. `qor mi ti-m daru-yu.` solemnly promises protection; `më mi ti-m daru-yu.` gives the same basic futurity but a gentler frame.

**Safety and consent override mood.** A warm register does not signal consent. An angry register does not inherently cancel a true statement. A question in `hë` may remain intrusive, and a promise in `qor` may be insincere. Resonance states the speaker's presentation, not an externally verified mental state.

## 3. Adjacency pairs

An **adjacency pair** is a first move that makes a response relevant: greeting→greeting, question→answer, offer→accept/refuse, apology→acknowledgment, request→grant/decline, correction→confirmation. Qaroshi does not require the response to repeat the first sentence's resonance. `hë ti haro he?` / `më mi haro.` is a suitable curiosity→warm reply. `më pëla mi-wa nëra ya.` / `nëm mi nu nëra-ki.` is a request followed by a calm refusal based on inability. The second speaker's autonomy remains visible in the shift of register.

## 4. Repair and correction

`qëlo` marks a correction of a previous mishearing; it typically follows resonance as a stance particle. A repair should identify which item is being corrected. `sen qëlo mi kima-m këmë.` = Correction: I drink water. If the listener cannot identify the corrected proposition, restate the mistaken claim or quote it separately. Distinguish **self-repair** (speaker revises their own statement) from **other-repair** (listener requests clarification); neither grants license to change another speaker's words in an archival transcript.

A natural exchange:

> `hë ti kima-m këmë he?` — Do you drink water?
>
> `sen mi kima-m këmë.` — I drink water.
>
> `hë hëwo ti kima-m sëna këmë he?` — Clarifying: do you always drink water?
>
> `sen qëlo mi kima-m nëna këmë.` — Correction: I'm drinking water *now*.

This is a **controlled teaching dialogue**. It is not a transcript of a historical speaker.

## 5. Politeness without rank or gender

`pëla` expresses courtesy, and `lan` softens a request to emphasize that refusal is possible. `pëshu` is a pressure-free invitation. The pronouns do not require gender. More formal stances are typically built through full referential phrases, explicit evidence, and avoidance of unexplained ellipsis, not by using a separate compulsory honorific class.

`më pëla mi-wa nëra ya.` = Please stay with me. `sen mi nu mahori.` = I do not consent. The latter is sufficient as a boundary statement; it does not require an explanation or a softening particle. Formal politeness must never erase the direct meaning of `nu`, `noharo`, `mahori` or other consent-related vocabulary.

## 6. Humor, irony, sarcasm and insults

Written resonance can *cue* a humorous or ironic reading but cannot prove that the words are ironic. `zha` ordinarily suggests playfulness, while `rak` can frame anger. An obviously ironic assertion can still require shared situational knowledge; outsiders may misread it. If precise interpretation matters, explicitly label the statement as joking or explain the contradiction in a following sentence. Insults are socially context-dependent: a term can be playful among consenting friends and threatening in a different setting. Profanity has intensity and addressee targets; an expletive aimed at a mishap is different from a slur aimed at a person.

## 7. Topics and information status

`-së` marks an overt topic: `sen kima-m-së mi këmë.` = As for water, I drink it. A new topic should be declared if the antecedent could reasonably be confused, especially in long texts. Given information is more naturally pronominal or elided; new information often has an explicit noun. `shënao` means “same” only when the relevant antecedent is known. `tëshi` marks a topic transition, not a new syntactic resonance.

## 8. Reported speech and quotation ethics

`do` closes a content clause, while literal quotation is **not** the same as a paraphrase. `hëra` can state that a paraphrase is being offered. `bëlaro` attributes a perspective to someone else. Distinguish what the quoted person actually said, what the speaker inferred, and what the narrator endorses. A long quotation should preserve its source sentence markers inside quote boundaries, while the enclosing **independent narration** has its own leading resonance. This means a written transcription may visibly contain several resonance markers: each belongs to a quoted sentence, not a second marker in the narrator's clause.

## 9. Texting conventions

In full orthography, the marker is never dropped. In very rapid chat, a missing marker is clearly labeled **nonstandard abbreviation**, not equivalent to a neutral `sen`. The most accessible convention is to type the full marker anyway: it adds only a word. Multiple messages in the same emotional register still each require their own marker if they are separate sentences. An emoji can enrich the affect but does not replace a typed marker.

## 10. Disagreement without contradiction

Two statements can disagree about one **frame** while being consistent about another. `sen sa goro-ki.` (ability) and `zher sa nu goro-ho.` (permission denied) can both be true. “I know you can fly” and “I don't think you should” are not competing facts about ability. A robust interpreter identifies whether a disagreement concerns evidence, confidence, values, permission, reference time, or literal proposition before declaring a contradiction.

## 11. Discourse annotation protocol

For each turn, record: `turn_id`, `speaker`, `qaroshi`, `english`, `resonance`, `speech_act`, `topic`, `information_status`, `evidence_type`, `tone_note`, `response_to`, and `literal_vs_implicature`. Do not infer an unseen user's private feelings merely from a marker. The linked corpus uses this structure in simplified form for educational evaluation.

## 12. Extended conversation test

Take any five-turn interaction and ask: Does each complete utterance have a resonance? Can every pronoun resolve to a unique antecedent? Are questions answered, refused or postponed? Is the boundary between direct quotation and paraphrase visible? Do the words make a commitment not supported by the original? Have consent and refusal been preserved exactly? If one of those answers is uncertain, annotate the uncertainty or rewrite before treating the exchange as a reference translation.
