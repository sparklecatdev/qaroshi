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

## VI. Release gate

`python tools/stress89/compose.py` and `python tools/stress89/audit.py` must pass, along with the full tests, syntax-scope counterexamples, existing integrity audit, and frozen source hash checks. Run the full GitHub Action; never manually overwrite the old 8.8 evidence file or release baseline to make candidate counts improve.

A future claim of a self-sufficient, generally fluent language needs independent readers recovering novel multi-clause meanings and communication without English. Current exact candidate counts, failures and review flags belong to generated machine-readable summaries, not a fabricated claim of completion.
