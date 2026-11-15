#!/usr/bin/env python3
"""Compile an editorially honest semantic handbook from reference + authored reviews."""
from pathlib import Path
import csv,json,collections
R=Path(__file__).resolve().parents[2]
def read(name):
 with (R/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
manifest=json.loads((R/'data/v16/semantic_atlas_manifest.json').read_text(encoding='utf8'))
new=read('data/v16/new_core_lexical_profiles.csv');prior=read('data/v12_13/core_lexical_profiles.csv')
met=read('data/v12_13/original_metaphors.csv')
risks=read('data/v14/translation_review_103.csv')
lex=read('data/v16/lexical_evidence_index_30000.csv')
senses=read('data/v16/sense_editorial_5000.csv')
idioms=read('data/v16/idiom_editorial_1000.csv')
cat=read('data/v16/domain_coverage_240.csv')
lines=['# Qaroshi 16.0 · Semantic Dictionary & Corpus Quality Handbook','',
 '> **Editorial development reference.** This handbook does not create approved senses, establish fixed idioms, or claim independent speaker or dialect evidence. It preserves the inherited 30,000-entry canonical dictionary and its grammar.','',
 '## 1. Evidence summary','',
 f'- **{len(lex):,}** existing canonical entries, including **{manifest["canonical_compound_entries"]:,}** transparent compounds.','',
 f'- **{manifest["lexemes_with_original_editorial_occurrence"]:,}** different headwords appear in separately drafted editorial writing; **{manifest["lexemes_with_controlled_reference_occurrence"]:,}** appear in controlled bilingual reference examples. These forms are not speaker-attested.','',
 f'- **{len(senses):,}** draft sense cards and **{len(idioms):,}** proposed figurative expressions require independent review.','',
 f'- **{len(new)}** new individually written lexical clarifications complement **{len(prior)}** previously written profiles.','',
 '- The 15.1 procedural 200,000+ token extension remains useful for drills, not as proof of naturalistic language use.','',
 '### Data-source hierarchy','',
 'A canonical headword establishes a published orthographic/lexical entry. A controlled example demonstrates a draft grammar construction. An independently scripted editorial dialogue offers a constructed context. A procedural template is suitable for software coverage. **None alone establishes a community convention or field attestation.**','',
 '### Specific audit findings','',
 '- **4,388 / 5,000** older sense cards have no usage illustration in either the controlled parallel reference or the separately drafted corpus. Their source *definitions* are not thereby disproven.','',
 '- **1,000 / 1,000** idiom candidates have zero exact occurrences in the separately drafted editorial corpus. This does not prove they cannot become idioms.','',
 f'- **{manifest["original_editorial_translation_variation_groups"]}** groups of identical Qaroshi source sentences have varying contextual English renderings. Contextual paraphrase is not automatically a contradiction.','',
 '## 2. Editorial meaning profiles','',
 'Each profile states a plausible narrower reading consistent with the inherited lexicon and warns where inference should stop. It is **not** automatically ratified.','']
for x in prior:
 lines+=['### '+x['qaroshi']+' · '+x['canonical_gloss'],'',
  '**Editorial interpretation:** '+x['editorial_sense_definition'],'',
  '**Usage restriction:** '+x['grammatical_or_semantic_restriction'],'',
  '**Contrast:** '+x['contrast_or_false_friend'],'',
  '**Example (editorial):** `'+x['qaroshi_example']+'` · '+x['english_example_contextual'],'']
for x in new:
 lines+=['### '+x['qaroshi']+' · '+x['canonical_gloss_unmodified'],'',
  '**Proposed explanation:** '+x['editorial_definition_proposal'],'',
  '**Usage restriction:** '+x['restriction_and_usage_boundary'],'',
  '**Contrast:** '+x['contrast_or_false_friend'],'',
  '**Previously written example (unattested):** `'+x['example_qaroshi']+'` · '+x['example_english'],'',
  '**Earlier source:** '+x['example_source_id'],'']
lines+=['## 3. Figurative language: 40 grounded literary proposals','',
 'These **forty** independently drafted metaphoric readings already existed in the 12–13 release; they are regrouped here with literal/context/counterexample notes. They should not be called established idioms.','']
for x in met:
 lines+=['### '+x['title']+' · '+x['id'],'',
  '**Qaroshi:** `'+x['qaroshi']+'`','',
  '**Literal:** '+x['literal_translation'],'',
  '**Proposed figurative reading:** '+x['proposed_figurative_meaning'],'',
  '**Context:** '+x['usage_context'],'',
  '**Counterexample / restriction:** '+x['counterexample_and_restriction'],'']
lines+=['## 4. Examples of unresolved source–English consistency','',
 'The examples below were flagged during 14.0 review. “Proposed standalone English” is a **candidate correction**, not an accepted erratum.','']
for x in risks[:24]:
 lines+=['### '+x['audit_id']+' · '+x['piece_id'],'',
  '- Qaroshi: `'+x['qaroshi']+'`',
  '- Contextual English: '+x['english_contextual'],
  '- Suggested stand-alone reading: '+(x['proposed_standalone_english'] or '(none supplied)'),
  '- Reason to review: '+(x['editorial_reason'] or x['legacy_flags']),
  '- Decision: **unreviewed**','']
lines+=['## 5. Domain coverage: 240 subject areas','',
 '| Domain | Entries | In drafted writing | In controlled reference | Transparent compounds |','|---|---:|---:|---:|---:|']
for x in cat:
 lines.append('| '+x['domain'].replace('|','/')+' | '+x['canonical_entries']+' | '+x['lexical_items_in_original_editorial']+' | '+x['lexical_items_in_controlled_reference']+' | '+x['compound_entries']+' |')
lines+=['',
 '## 6. Review and publication procedure','',
 '1. Read the source dictionary entry, POS, canonical first gloss and compound components.','2. Inspect editorial and controlled usage independently; do not treat procedural frequency as naturalness.','3. Compare competing meanings against full context, participant roles, clause scopes and evidential markings.','4. Add **negative examples** showing when a tempting English paraphrase is too broad.','5. For a new sense, distinguish an English paraphrase of one meaning from a genuinely distinct lexical meaning.','6. For an idiom, provide clear, externally accepted conventional usage. An untested metaphor remains a proposal.','7. Record source, independent reviewer, date, decision, corrected translation, and evidence; reject or revise claims without erasing history.','8. Only a separately versioned standardization decision can update the canonical lexicon.','',
 '## 7. Output files','',
 '`data/v16/lexical_evidence_index_30000.csv` provides the full 30,000-entry evidence graph; `sense_editorial_5000.csv` and `idiom_editorial_1000.csv` are editable queues. `editorial_translation_variants.csv` tracks 223 context differences. `coverage_writing_briefs_240.csv` contains writing **assignments**, not written prose. `Qaroshi_16_Semantic_Atlas.html` provides a full offline review UI and progress backup.','',
 '## 8. Honest completion gate','',
 '**Development tasks completed:** reproducible evidence index, triage queues, 57 new manually written lexical clarification profiles, semantic contrast library, 240 topical writing assignments, offline review UI, provenance-aware documentation and tests.','',
 '**Still pending:** independent acceptance of 5,000 senses and 1,000 idioms, speech-community evidence, source/English adjudication, and high-quality non-templated writing covering all 240 domains. Word count alone does not resolve those tasks.','']
out=R/'Qaroshi_16_Semantic_Handbook.md';out.write_text('\n'.join(lines),encoding='utf8')
print('handbook',out,len(lines),'lines',out.stat().st_size,'bytes')
