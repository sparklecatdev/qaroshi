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
