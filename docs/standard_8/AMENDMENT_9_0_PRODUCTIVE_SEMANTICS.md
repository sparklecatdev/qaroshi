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
