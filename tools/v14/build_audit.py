#!/usr/bin/env python3
"""Qaroshi 14.0 editable risk registers and explainable audit summaries.

Uses existing v12/13 material unchanged. A flag is NOT a finding of error.
"""
from __future__ import annotations
import collections, csv, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v14'; OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools/v14'))
from semantic_validator import validate_sentence,possible_repair_pairs, CODE, words
sys.path.insert(0,str(ROOT/'tools/fluency11'))
from engine import parse_qaroshi


def read(name):
 with (ROOT/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

def write(name, rows):
 rows=list(rows)
 if not rows:return
 with (OUT/name).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Suggestions are deliberately manual and explicitly only candidate English,
# not an update to original literary context, grammar, or dictionary.
EDITORIAL_EXAMPLES={
 'q12-the-borrowed-compass|5':('I do not know this compass.','The original adds the idea of being able to *use* the instrument, which is not overt.','source_expands_verb'),
 'q12-the-festival-without-a-song|2':('Did you lose the song?','The source directly names shira (song); the English elides its antecedent.','contextual_ellipsis'),
 'q12-the-festival-without-a-song|4':('I do not know the song.','The source does not directly encode learning by heart or never.','semantic_enrichment'),
 'q12-a-lost-page-in-the-library|3':('I do not know the book.','The English is a why-question; the Qaroshi is a negative declarative.','speech_act_mismatch'),
 'q12-a-lost-page-in-the-library|6':('I can remember the story.','The source -ki marks ability, while the English asserts partial success.','modal_strength_shift'),
 'q12-a-broken-window-at-dusk|4':('I cannot repair the window.','Being unable alone is an inference; the source denies the ability without qualification.','semantic_enrichment'),
 'q12-the-apology-without-an-excuse|6':('I will not speak today.','The English adds the whole-thing restriction absent from the Qaroshi.','semantic_enrichment'),
 'q12-a-price-too-low|2':('I will buy the book.','The English says possibly and adds another intention; the source is an unqualified future.','commitment_shift'),
 'q12-a-price-too-low|4':('You are allowed to ask the question.','-ho marks permission; isolated You may is possible ellipsis but lacks the predicate.','contextual_ellipsis'),
 'q12-the-inherited-feather|2':('Do you remember the feather?','The source does not directly express where it came from.','semantic_enrichment'),
 'q12-the-library-s-last-hour|8':('I will give the book tomorrow.','Giving a book is not equivalent to bringing it back without destination context.','verb_argument_shift'),
 'q12-the-private-map|3':('Did you read the friend’s message?','mara-na denotes friend’s, not explicitly our friend.','ownership_enrichment'),
 'q12-a-water-jar-of-questions|6':('I do not know the truth.','Not every truth suggests quantified partial knowledge; no such quantifier appears.','quantifier_enrichment'),
 'q12-the-dispute-about-a-rumor|4':('Did you personally read the message?','The witnessed si evidential is best preserved for standalone translation.','evidential_underspecified'),
 'q12-rest-before-the-exam|5':('I cannot remember the memory.','The English hides the ability suffix and implies a temporary time limitation.','modal_strength_shift'),
 'q12-the-missing-medicine|5':('I do not know the medicine.','Which medicine is correct is an additional question/selection relation.','semantic_enrichment'),
 'q12-a-friend-at-the-doorway|4':('I will not rest with you.','Preference to be alone is a contextual inference, not the overt negative future statement.','pragmatic_ellipsis'),
 'q12-the-diary-s-blank-page|3':('I did not remember the memory.','Some of it is missing is a contextual conclusion, not a direct equivalent.','semantic_enrichment'),
 'q12-the-letter-never-sent|3':('I did not send the message.','The English reply omits the explicit negative past and supplies an emotional motivation.','pragmatic_ellipsis'),
 'q12-the-word-forever|2':('I do not know forever.','The English changes the grammatical subject from I to no one and adds a broad universal claim.','participant_and_quantifier_shift'),
 'q12-a-quiet-victory|3':('I can remember the memory.','The source encodes ability, but mostly is an inferred degree.','modal_strength_shift'),
 'lit12-the-honest-report|11':('I do not know them.','sa-m is an object pronoun; what happened is not an overt object phrase.','reference_shift'),
 'lit12-what-a-promise-can-contain|6':('I will stay with you today.','ti-wa means with you, whereas the English says with them.','pronoun_conflict'),
 'lit12-the-river-without-an-answer|8':('I remembered a memory.','This is closer to source form but pragmatically redundant; a revised Qaroshi sentence may be better.','lexical_redundancy'),
 'lit12-the-weather-and-the-story|12':('Do you know the truth?','The source subject is ti (you); narrator is supplied by context, not source grammar.','reference_shift'),
 'lit12-the-old-painting|9':('I did not know the painting.','The English adds all details and understand, neither independently established by the surface form.','semantic_enrichment'),
 'lit12-the-door-and-the-difference|7':('I did not know the doorway.','Infer permission is an entire pragmatic argument not encoded by this clause.','semantic_enrichment'),
 'lit12-the-classroom-of-questions|2':('I learn Qaroshi.','Study is a plausible context-dependent paraphrase but not guaranteed by bare rëmi.','near_synonym_review'),
}

qa=read('data/v12_13/dialogue_literature_translation_qa.csv')
assert len(qa)==689
screened=[];flagged=[];allcounts=collections.Counter()
for index,x in enumerate(qa,1):
 audit_id=f'QA14-{index:04}'
 key=x['piece_id']+'|'+str(x['turn'])
 analysis=validate_sentence(x['qaroshi'], x['english_contextual'],context_id=key)
 findings=[y for y in analysis['findings'] if y['kind']=='translation-risk']
 if not analysis['valid_surface']:allcounts['surface_errors']+=1
 ids=sorted({f['rule_id'] for f in findings})
 original=x['flags'].strip()
 # Heuristic legacy engine coverage is not an intrinsic semantic defect.
 isflag=bool(original)
 if not isflag:
  classification='no_legacy_risk_flag: still unreviewed editorial translation'
 elif 'R14-018' in ids or 'R14-016' in ids:
  classification='high: participant or sentence-mood mismatch candidate'
 elif key in EDITORIAL_EXAMPLES:
  classification='high: source/context discrepancy or meaningful ellipsis requires review'
 elif any(i in ids for i in ('R14-011','R14-012','R14-013','R14-014')):
  classification='medium: overt grammar underexpressed in contextual English'
 elif 'R14-015' in ids:
  classification='medium: evidence source not explicit in standalone English'
 elif 'grammar engine declined literal translation' in original:
  classification='low: engine-coverage limitation; no source error established'
 else:classification='low: ambiguous contextual alignment for editorial review'
 proposal,why,kind=EDITORIAL_EXAMPLES.get(key,('','No standalone correction proposed; evaluate the source, discourse context, and English gloss together.','unclassified'))
 if not proposal and x['engine_interpretation'].strip():
  proposal=x['engine_interpretation']
  why='Earlier grammar engine produced a controlled literal interpretation; this is a starting point, not a final correction.'
  kind='engine_interpretation_only'
 row={
  'audit_id':audit_id,'source':x['source'],'piece_id':x['piece_id'],'turn':x['turn'],
  'qaroshi':x['qaroshi'],'english_contextual':x['english_contextual'],
  'previous_engine_interpretation':x['engine_interpretation'],
  'legacy_flags':original,'new_rule_ids':'; '.join(ids),
  'priority_and_scope':classification,'interpretation_category':kind,
  'proposed_standalone_english':proposal,'editorial_reason':why,
  'surface_check':'pass' if analysis['valid_surface'] else 'needs repair',
  'machine_screened':'yes','human_semantic_approved':'no','reviewer':'','editorial_decision':'unreviewed',
  'revised_qaroshi':'','revised_english':'','decision_rationale':''
 }
 screened.append(row)
 if isflag:flagged.append(row)
 allcounts.update(ids)
assert len(flagged)==103, len(flagged)
write('translation_screening_689.csv',screened)
write('translation_review_103.csv',flagged)

repeated=collections.defaultdict(list)
for row in screened:repeated[row['qaroshi']].append(row)
paraphrase_groups=[]
for q,items in repeated.items():
 eng=sorted({x['english_contextual'] for x in items})
 if len(eng)>1:
  paraphrase_groups.append({'qaroshi':q,'references':'; '.join(f"{x['piece_id']}:{x['turn']}" for x in items),
                           'distinct_english_count':len(eng),'contextual_renderings':' | '.join(eng),
                           'interpretation':'variation among translations; may be contextually legitimate',
                           'review_status':'not evaluated'})
write('translation_variant_clusters.csv',paraphrase_groups)

original_idioms=read('data/v12_13/idiom_1000_quality_triage.csv')
idiom_src={r['id']:r for r in read('data/editorial/idiom_candidates_1000.csv')}
idioms=[]
for x in original_idioms:
 risk=x['editorial_semantic_risks'];src=idiom_src[x['id']]
 sem='high' if 'figurative seeing/reading' in risk or 'abstract metaphor' in risk else 'medium' if risk else 'low'
 if 'seeing/reading' in risk:action='Check whether this noun is a perceptible or quoted abstract entity; provide a context showing metaphor vs literal use.'
 elif 'abstract metaphor' in risk:action='Evaluate if the anchor can plausibly occur in this image family; compare a literal and metaphorical scene.'
 elif 'multiword source gloss' in risk:action='Resolve competing source glosses and choose the relevant sense before accepting the expression.'
 else:action='Verify corpus occurrence, phrase conventionality and possible figurative reading with actual users; morphology alone is insufficient.'
 idioms.append({'id':x['id'],'family':x['family'],'qaroshi_expression':src['qaroshi_expression'],
 'anchor':x['anchor'],'source_meaning':x['source_meaning'],'earlier_risk':risk,
 'priority':sem,'editorial_test':action,'status':'not conventionalized / human review required',
 'speaker_evidence':'none','reviewer':'','decision':'unreviewed','notes':''})
assert len(idioms)==1000
write('idiom_review_1000.csv',idioms)

sense_src={r['sense_id']:r for r in read('data/editorial/sense_cards_5000.csv')}
profile={r['qaroshi']:r for r in read('data/v12_13/core_lexical_profiles.csv')}
base_senses=read('data/v12_13/sense_5000_quality_triage.csv')
senses=[]
for x in base_senses:
 sid=x['sense_id'];draft=sense_src[sid]
 risk=x['editorial_usage_risk']
 if 'generic see-object' in risk:
  severity='high';action='Replace generic “I see X” with a contextually licensed action and verify that the object can be perceived literally.'
 elif 'argument structure/valency' in risk:
  severity='high';action='Document subject, possible direct object, recipient, and grammatical restrictions; bare-subject examples do not establish valency.'
 elif 'generic home predicate' in risk:
  severity='medium';action='Choose a semantically appropriate subject rather than assuming any adjective modifies a home.'
 else:
  severity='low';action='Review the source sense boundary and example in context; no heuristic problem was found.'
 if x['lemma'] in profile:
  severity='high' if severity=='low' else severity
  action+=' See separately drafted profile '+profile[x['lemma']]['id']+' for a contrastive constraint.'
 senses.append({'sense_id':sid,'lemma':x['lemma'],'source_definition':x['source_definition'],
 'source_pos':x['source_pos'],'domain':draft['domain'],'draft_example':draft['candidate_example'],
 'draft_english':draft['candidate_example_en'],'earlier_risk':risk,
 'priority':severity,'review_action':action,'curated_profile_id':x['curated_core_profile_id'],
 'status':'dictionary gloss confirmed; contextual meaning not accepted',
 'independently_validated_sense':'no','reviewer':'','decision':'unreviewed',
 'suggested_new_example':'','synonyms_approved':'','antonyms_approved':'','argument_frame_approved':'','notes':''})
assert len(senses)==5000
write('sense_review_5000.csv',senses)

# Discourse-level candidates, not demonstrated logical inconsistencies.
scenes=json.loads((ROOT/'corpus/v12_13/dialogues_12.json').read_text(encoding='utf8'))
repairs=[]
for scene in scenes:
 for item in possible_repair_pairs(scene['turns']):
  repairs.append({'piece_id':scene['id'],**item,'reviewer':'','decision':'unreviewed'})
write('discourse_repair_candidates.csv',repairs)

manifest={
 'release':'14.0 language consistency - computational editorial review',
 'source_corpus_rows':len(screened),'legacy_flagged_rows':len(flagged),
 'translation_standalone_proposals':sum(bool(r['proposed_standalone_english']) for r in flagged),
 'manual_editorial_proposals':sum(r['interpretation_category'] not in ('engine_interpretation_only','unclassified') for r in flagged),
 'scope_flagged_after_v14_rules':sum(bool(r['new_rule_ids']) for r in flagged),
 'translation_variant_clusters':len(paraphrase_groups),'possible_discourse_repair_pairs':len(repairs),
 'idiom_candidates_reviewed_for_risk':len(idioms),
 'idiom_priorities':dict(collections.Counter(r['priority'] for r in idioms)),
 'idiom_culturally_approved':0,
 'sense_cards_reviewed_for_risk':len(senses),'sense_priorities':dict(collections.Counter(r['priority'] for r in senses)),
 'sense_cards_independently_approved':0,
 'validation_rule_count':len(CODE),
 'new_findings_on_689':dict(allcounts),
 'IMPORTANT':'Automatic review is structural and triage only: 0 independent speaker or semantic acceptances; no original language source was rewritten.'
}
(OUT/'audit_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(manifest,indent=2,ensure_ascii=False))
