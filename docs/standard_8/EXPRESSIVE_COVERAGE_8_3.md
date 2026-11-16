# Qaroshi 8.3: Editorial Completeness and Evidence Ledger

This edition reviews the remaining expressive-coverage gaps **without falsifying lexical meaning or independent language testing**.

## Translation review: 500 targets

Run the 8.3 builder to produce a detailed CSV of all 500 original 8.1 English challenges. Every case records its semantic target, existing 8.1 draft if present, dictionary-ID lexical witnesses, any new source-anchored construction, and its actual limits. New candidate sentences are editorial hypotheses, not speaker-validated translations. If the present dictionary and grammar do not license all elements, the case stays visibly unresolved, not filled with imaginary words.

## Verb behavior: 375 restricted entries

Each restricted verb receives a typed recorded construction, source evidence, any observed object root, and an explicit exclusion of previously unlicensed passive/causative/alternate patients. The 25 general manual frames remain authoritative. An editorial linguist could adopt more general frames in the future, but the framework will not claim approval without actually specifying the rule and its counterexamples.

## Compound lexicography: 3,108 flags

The canonical whole-word gloss controls the dictionary meaning of each flagged compound. Its components may have additional English homonyms but do not export those unrelated meanings automatically. Existing individual sense decisions are retained. This completes a **dictionary interpretation policy**, not independent contextual validation of every word.

## Formal grammar and semantic stress

Preserve the adopted distinctions between not all versus none, evidence source versus truth, passive actor versus instrument, permission versus ability, and matrix versus embedded negation. The 8.2 suite of Qaroshi-side minimal pairs remains a formal reference with a documented applicability boundary. The 8.3 stress review connects new proposals to actual dictionary headwords and refuses to certify contextual meaning from a gloss alone.

## Connected readings and blind comprehension

The 8.2 annotated readings remain original editorial compositions. The 8.3 generator creates a separate recognition sheet and answer key for available proposed translations. They have no human respondents by default. Running code cannot create independent linguistic attestation or test real comprehension.

## Remaining acceptance requirements

All 500 English propositions still need complete, independently semantically checked Qaroshi translations; restricted verb alternations need actual review; unresolved compound contextual ambiguity needs reader evidence; spontaneous speech and longer texts need real consenting learners. Those gates are not magically satisfied by a script. This is a reproducible editorial completion attempt, not a false certification of natural fluency.

## Commands

    make stress83
    python -m unittest tests.test_stress83 -q
    python -m unittest discover -s tests -q
