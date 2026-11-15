"""Generate reproducible human-readable release guides from real audited data."""
import json,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'data/v16_1'

def csvrows(path):
 with (P/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
r=json.loads((P/'audit_report.json').read_text(encoding='utf8'))
g=json.loads((P/'root_gap_manifest.json').read_text(encoding='utf8'))
c=json.loads((P/'collision_report.json').read_text(encoding='utf8'))
words={x['qaroshi']:x for x in csvrows('headword_learnability_audit_16525.csv')}
cases=['banuaro','bamusu','babalu','baragë','bebumo','bebira','betasho','dahokhoge','limabo','benusë','bewëru','goro','banuwa','qaroshishimarë','pizikha']
lines=['# Qaroshi 16.1: Less memorization through transparent roots','',
 '## Executive answer','',
 '**Grammar does not let you guess every base word.** Qaroshi already has 13,379 canonical transparent modifier–head compounds, but 16,525 entries are labeled headwords with no official component analysis. This update audits every such headword, generates proposed ways to express some technical concepts with established roots, and identifies missing common building blocks. None of the proposals is automatically accepted as a new standard spelling.','',
 '## Verified categories (all 16,525 labeled headwords)','',
 '| Result | Headwords | Meaning |','|---|---:|---|',
 f"| Established headword spelling matches two dictionary stems | {r['existing_headwords_matching_two_component_spellings']:,} | Possible metadata reclassification, not a new word |",
 f"| Complete split using the primary meanings of both components | {r['primary_gloss_candidates']:,} | Exact modifier–head editorial proposal |",
 f"| Complete split requires a secondary dictionary sense | {r['secondary_sense_candidates']:,} | Higher ambiguity risk; review carefully |",
 f"| Some documented meaning clues, no licensed complete form | {r['count_by_status']['semantic_anchors_only']:,} | Teach related words, do not coin from guesses |",
 f"| No documented component analysis | {r['count_by_status']['no_documented_derivation']:,} | Learn as conventional roots pending reviewed analysis |",
 '',f"The candidate catalog has **{r['exact_split_proposal_rows']:,} alternative suggestions** for **{r['headwords_with_any_exact_split']:,} canonical headwords**, including multiple choices for some English glosses. Only one default alternative per headword appears in the simple browser view; all alternatives appear in the CSV. The two existing-forms cases do not produce any new proposed spelling.",
 '', '## Grounded examples from the canonical dictionary','',
 '| Canonical word | Canonical meaning | Proposed transparent segmentation | Review status |','|---|---|---|---|']
for word in cases:
 if word not in words:continue
 x=words[word];parts=(x['proposed_modifier']+' ('+x['modifier_meaning']+') + '+x['proposed_head']+' ('+x['head_meaning']+') → **'+x['proposed_transparent_form']+'**' if x['proposed_transparent_form'] else x['possible_existing_component_sequence'] or x['grounded_english_anchors'] or 'No documented derivation')
 lines.append(f"| `{x['qaroshi']}` | {x['english']} | {parts.replace('|','/')} | {x['analysis_status']} |")
lines+=['','**Caution:** An English label like “fire” can be a secondary gloss of a source word meaning “flame,” and those are not guaranteed interchangeable. The default rank favors **primary** component senses and the full CSV flags secondary-sense possibilities. Parenthetical sense restrictions still need review.','',
 '## Productivity without a brand-new word for everything','',
 '1. **Core words are conventional.** A learner must remember that `goro` means fly. Grammar can then generate `goro-te` (flew), `goro-ki` (able to fly), `goro-ho` (permitted to fly). It cannot infer the root meaning from phonemes.',
 '2. **Original compounds are already productive.** Learn the component roots and you can understand the structure of 13,379 existing modifier–head compounds. The baseline 16.0 study maps 1,820 ultimate base roots used inside them. The exact specialized meaning is not always a simple sum.',
 '3. **Some independent technical headwords can be paraphrased.** `banuaro` is the established word for wing joint. The proposed spelling `banuqamago` transparently uses `banu` wing + `qamago` joint, but is **not yet canonical** and might be more cumbersome in ordinary speech.',
 '4. **Do not invent hidden syllable meanings.** `banuwa` means wing membrane, but that does not automatically license interpreting `-wa` as a suffix meaning membrane. In the real grammar, `-wa` is a comitative case suffix when used with a hyphen.',
 '5. **Avoid the giant-word trap.** Long compounds should be shown with visible component boundaries in teaching tools. If a shorter canonical headword is commonly used, teach it alongside its transparent explanation rather than forcibly replacing it.','',
 '## Which *new concepts* would reduce memorization?','',
 f"Across the English glosses, **{g['unique_missing_english_concept_gaps']:,} lexical component gaps** were identified; **{g['gaps_affecting_3_or_more_headwords']:,}** affect at least three headwords. These are *missing exact English gloss anchors*, not proof that Qaroshi lacks an equivalent synonym.",'',
 '| Missing English concept | Role | Potential headwords helped |','|---|---|---:|']
for row in g['top_20']:
 lines.append(f"| {row['english']} | {row['role'].replace('_',' ')} | {row['headwords']} |")
lines+=['', 'For instance, the exact root concept **membrane** is missing in the audit and affects `banuwa` (wing membrane), `qapewa` (eardrum membrane), `wëroba` (waterproof membrane) and `zeyedo` (cell membrane). Rather than creating four unrelated words, reviewers could identify an existing equivalent or propose **one reusable word for membrane**. No new phonological root was automatically coined here.', '',
 f"## Ambiguous candidate collisions",'',f"**{c['cross_headword_candidate_collisions']}** candidate spellings would map to **{c['affected_headword_candidates']}** distinct canonical targets. This includes cases where a broad word would conceal important distinctions (for example different senses of informed consent). See `data/v16_1/proposal_collision_review.csv`. These aliases must remain unapproved until distinctions are tested.",'',
 '## Adoption protocol', '',
 '1. Start with the exact canonical entry, its historical user-facing gloss, and its independent/contextual evidence.',
 '2. Try a licensed modifier–head composition using existing primary-sense roots. Compare at least two alternative component choices when multiple senses are available.',
 '3. Verify that the component spelling does not collide with an established word or another proposed sense; check pronunciation and native glyph segmentation.',
 '4. Show the proposed spelling in at least three independently written Qaroshi sentences with distinct contexts, formal vs conversational usage, and faithful English back-translations.',
 '5. Have an editor decide whether the compound is a paraphrase, an approved synonym, or only an explanation. Document reviewer and rationale; do not infer acceptance from automated tests.',
 '6. Preserve the original canonical spelling as an alias whenever a new formal standard is approved; publish a versioned migration and regression tests.',
 '', '## Why no sweeping mass rename?', '',
 'Because most headwords are not fully predictable and because existing short forms may be more useful than an extremely long transparent technical form. A language should be learnable *and* practical. Automatically turning thousands of dictionary items into unreviewed compounds would replace one kind of arbitrariness with another.',
 '', '## Included machine-readable materials', '',
 '- `headword_learnability_audit_16525.csv`: every headword, classification, evidence, top candidate and anchors.',
 '- `strict_modifier_head_candidates.csv`: every full exact-split candidate (multiple per headword), with dictionary components.',
 '- `headword_learning_priority_16525.csv`: all headwords ranked by usage/reference evidence and compound reuse.',
 '- `prioritized_core_1200.csv`: suggested first 1,200 supported base words for study.',
 '- `root_gap_priorities.csv`: missing English concept anchors ranked by headword reuse, without new Qaroshi coinages.',
 '- `proposal_collision_review.csv`: candidate form conflicts across canonical meanings.',
 '- `Qaroshi_16_1_Root_Reform_Studio.html`: offline learning, searching and review decisions.',
 '', '## Claims we do NOT make', '',
 'This release does not attest speaker consensus, a new etymology, fluent speaker sentences, new grammatical suffixes, ratified synonymy, or zero-knowledge inference for all 30,000 dictionary forms. The original 30,000-entry dictionary, 90 grammar chapters, 16 written resonance markers and 26 glyphs remain unchanged.','']
(ROOT/'Qaroshi_16_1_Root_Transparency_Guide.md').write_text('\n'.join(lines),encoding='utf8')
protocol='''# Editorial root and paraphrase review protocol

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
'''
(ROOT/'docs/v16_1').mkdir(exist_ok=True)
(ROOT/'docs/v16_1/REVIEW_PROTOCOL.md').write_text(protocol,encoding='utf8')
print('Guides built',len(lines),'lines')
