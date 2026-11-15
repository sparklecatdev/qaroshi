# Qaroshi formal grammar and interpretation guide

This expands the Standard 7.0 descriptions. The earlier 90 chapters remain the canonical baseline; examples here document rule interactions and edge cases rather than redefining the language.

## Sentence model

A complete, independently written sentence starts with exactly one of the 16 resonance particles. The marker scopes over the whole sentence, including unquoted subordinate clauses. A separately quoted complete sentence has its own marker. The marker is pragmatic: it signals the speaker's interpersonal stance, but does not on its own establish whether the proposition is true.

Neutral clause order is **resonance – discourse framing – topic – subject – time – object – obliques – negation – predicate – evidential – speech-act marker**. Qaroshi is SOV, not a word-by-word replacement for English. Explicitly case-marked objects may move for contrast, while clause-internal morphology still signals their role.

- `sen mi kima-m këmë.` I drink water.
- `sen mi-na mara kima-m këmë.` My friend drinks water.
- `hë ti haro he?` Are you well?
- `qor mi ti-m daru-yu.` I will protect you.

## Nominal morphology

The canonical order is **root + derivation + endearment + number + case + topic**. Plural `-ri` comes before the case ending, and a single noun may not receive competing case endings such as `-m-lo`. Possessors marked `-na` precede the possessed phrase; the noun is not automatically plural or definite. Other primary cases: `-m` direct object, `-lo` location, `-gu` goal, `-de` source, `-wa` companionship, `-tu` recipient, `-shi` means or passive agent. Topic `-së` follows any case.

`mara-ri-m` = friends as direct object; `mara-m-ri` violates suffix order. `mi-na naro` = my home, not “home me.” Demonstratives, descriptive adjectives, and numerals follow the previously defined noun-phrase positions in the main grammar.

## Verbal morphology

**Root + voice + tense + aspect + modality + manner** is the order. Voice is one of `-ru` causative, `-li` passive, `-wo` reciprocal, or `-ne` reflexive. Tense is unmarked present, `-te` past, or `-yu` future. Aspect, at most one per finite verb, is `-se` progressive, `-mo` completive, or `-në` habitual. Modality, at most one, is `-ki` ability, `-ho` permission, or `-du` obligation. Tender manner `-la` is last where licensed.

- `sen sa shiri-te-se.` They were speaking.
- `sen sa shiri-yu-mo.` They will have finished speaking relative to a future reference point.
- `sen sa goro-ki.` They can fly.
- `sen sa goro-ho.` They may fly (permission, not physical capacity).
- `qor sa goro-du.` They must fly (obligation).

No suffix says “both must and can” by stacking `-du-ki`. Use multiple clauses to distinguish obligation and capacity. An English sentence with “can” is ambiguous unless ability and permission are resolved first.

## Scope and logical precision

`nu` directly precedes the predicate it negates. `sen mi kima-m nu këmë.` says I do not drink water, not that I drink something else. `sen mi nu shiri-ki.` means I cannot speak, not “I can choose not to speak.” To negate an embedded claim, place negation inside that clause, not after its reporting predicate. Focus and quantifiers (`only`, `at least`, `every`) require a clear alternative set in context. Translate “everyone didn't leave” with explicit scope, since English can mean nobody left or not everyone left.

An evidential `si` means witnessed, `hu` reported, `ye` inferred. It does not guarantee truth. `sen sa goro-te hu.` does not mean the speaker directly saw the flight; `sen sa goro-te si.` asserts direct observation. Keep uncertainty and evidence separate from emotional resonance.

## Clauses and quotations

Coordinators join units of similar rank (`ara`, `nao`, `oru`). `ro` gives a reason, `ko` introduces intended purpose, `wë` introduces a condition, `uro` a concession, `yaro` overlapping time, `ëna/ana` event order, and `do` a reported proposition. A subordinate clause inherits the opening resonance; an independent quotation keeps its own. The condition “if X” does not assert X, and a purpose “so that Y” does not guarantee Y occurred.

- `dal wë sa goro-yu, mi sa-m tika-yu.` If they fly, I will see them.
- `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.` Please never die so you can stay with me forever.

Independent polar questions end in `he`; requests/commands end in `ya`, but the two endings do not combine as one clause. A question mark does not replace the question particle. In complex dialogue, write separately marked sentences to switch resonance, rather than inserting a second marker mid-clause.

## Referential clarity and pragmatics

`sa` is singular ungendered they; `sari` is plural. Inclusive `naru` means speaker with addressee, exclusive `muru` means speaker with others but without addressee. Subject omission is possible only if the intended referent is recoverable. If two participants could both be `sa`, repeat names or noun phrases in technical, legal, or emotionally sensitive passages. A warm register never overrides a refusal; the form of a question does not imply consent.

## Structural validation vs linguistic judgment

A checker can verify suffix slots, lexical roots, sentence-initial markers, and obvious incompatible endings. It cannot prove that a long sentence has the intended truth conditions, that a metaphor is idiomatic, or that consent and interpersonal meaning are appropriate. Any novel constructions should be independently reviewed with both well-formed and minimally different ungrammatical sentences.
