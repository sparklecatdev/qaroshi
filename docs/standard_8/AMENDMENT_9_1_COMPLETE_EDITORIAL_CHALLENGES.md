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
