# Editorial root and paraphrase review protocol

**Stage 0: Machine suggestion**. Exact two-part split of an English primary/secondary gloss into existing named dictionary roots. This only establishes the feasibility of building that spelling. No speaker naturalness has been inferred.

**Stage 1: Source definition**. Review original dictionary ID, gloss, domain, syntactic category, IPA and baseline corpus evidence. If the word is polysemous, distinguish the intended sense explicitly.

**Stage 2: Compositional reading**. Confirm modifier–head order and that each chosen root means the intended concept IN THAT CONTEXT. If a component uses a secondary sense, require additional examples. If a component has parenthetical domain restrictions, check them closely.

**Stage 3: Interoperability**. Check for collisions against the canonical dictionary and among proposals. Do not approve candidate spellings in `proposal_collision_review.csv` until readers can tell their distinct meanings apart. Respect the 26 glyph source inventory and 16 required opening resonance markers; no new suffixes are authorized.

**Stage 4: Usage**. Independently draft at least three context-distinct full sentences; each has written resonance, correct nominal/verb endings and argument roles, IPA, literal gloss, intended English reading and explicit notes about meaning NOT implied.

**Stage 5: Human sign-off**. Record reviewer, evidence source, date, approval status and any competing candidate. One person's editorial judgment establishes an editorial decision, not empirical speaker-community consensus. Continue collecting independent feedback.

**Stage 6: Publish as additive alias if approved**. Do not silently alter or remove old canonical words. Any officially accepted alias needs a separate migration appendix and versioned tests. A rejected form may remain in the audit record but never in the canonical dictionary.

## Learning curriculum

Learn common roots by contextual importance, then learn productive suffix slots (case, tense, modality), then study canonical compounds as modifier + head, then use optional transparent paraphrases only when clearly marked as proposals. Explain why unknown headwords cannot be guessed from sound.

The offline application saves review notes and decisions to the browser's local storage; it does not upload them or mutate the canonical files. JSON export provides a portable record.
