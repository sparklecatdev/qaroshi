# Qaroshi 11: Conservative bidirectional grammar engine

The executable engine is `tools/fluency11/engine.py`. It operates on **the unchanged 30,000-entry Qaroshi dictionary** and the 4,383 previously documented parallel teaching examples. The program's purpose is to help authors and learners parse *explicitly licensed* grammatical structures without making up a plausible-looking translation when the rule is unknown.

## Grammar handled directly

- Exactly one opening resonance is required on complete independent sentences. Resonance is a stance marker, **not** a claim about truth, reliability, gender, romance, or consent.
- Noun morphology: diminutive, plural, genitive, object, locative, allative, ablative, comitative, dative and instrumental/topic suffixes. The validator rejects suffixes in the wrong order and competing endings in the same slot.
- Verb morphology: causative/passive/reciprocal/reflexive recognition; past/future, progressive/completive/habitual, ability/permission/obligation, and tender manner. English rendering of unsupported voice combinations is deliberately withheld.
- A limited English clause generator with subject pronouns, familiar nouns, basic objects, a few cases, past/future/modality, negation and polar questions.
- SOV statement and question analysis, valency safeguards, negative scope immediately preceding the predicate, evidential particles `si`, `hu`, `ye`, and a heuristic for certain explicit subordinate clauses.
- Exact lookup of documented parallel sentences before falling back to structural inference. This permits complex **reference-matched** sentences to retain their documented meaning without pretending the engine derived every nuance.

## Illustrative meanings

| Qaroshi | English meaning | Grammatical point |
|---|---|---|
| `sen mi goro-ki.` | I can fly. | `-ki` means ability |
| `sen mi goro-ho.` | I may fly. | `-ho` means permission |
| `qor mi goro-du.` | I must fly. | `-du` means obligation |
| `sen mi goro-te-se.` | I was flying. | past plus progressive |
| `hë ti mi-m dëmi-ki he?` | Can you help me? | object plus question ending |
| `sen mi kima-m nu këmë.` | I do not drink water. | `nu` negates the predicate |
| `sen mi-na gëro dërawa.` | My throat is dry. | genitive noun phrase and adjectival predicate |

Some English glosses have multiple plausible readings. `haro` can mean *good*, *safe*, or *well*, and `nashi` can express deep care without necessarily implying romantic love. `sa` is singular ungendered *they*, while `naru` and `muru` distinguish inclusive and exclusive *we*. Use context rather than asserting one reading as universally correct.

## Trust and error handling

The engine outputs `translation`, `errors`, `warnings`, `confidence`, `resonance`, `evidential`, and a segmented token-level analysis. A reference match is labelled *exact controlled reference example*. A licensed structural rendering is labelled *rule-based controlled interpretation*. Unsupported stems, ambiguous valency structures, reflexives, quote scopes and unusual embedded clauses are returned as unresolved. This is **not** unrestricted machine translation or speaker-certified fluency.

## Commands

```bash
python tools/fluency11/engine.py 'hë ti mi-m dëmi-ki he?' --direction to-en
python tools/fluency11/engine.py 'I will protect you.' --direction to-qr --resonance qor
python tools/fluency11/engine.py 'më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.' --direction to-en
```

The **offline HTML app** exposes 4,383 reference pairs plus the automatically checked productive sentence table, including optional resonance selection for practice. The Python CLI performs deeper morphology and provides explicit unresolved diagnostics. Neither tool silently assumes that a newly formed sentence is idiomatic.
