#!/usr/bin/env python3
"""Build Qaroshi 18.0 + 19.0 teaching corpus and offline studio.

Requires no network. Leaves the 30k canonical lexicon, grammar and v14-v17
resources unchanged; stores only versioned additions. No automatic semantic
acceptance or natural-speaker attestation is claimed.
"""
from __future__ import annotations
import collections, csv, hashlib, json, re, sys, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D18=ROOT/'data/v18';D19=ROOT/'data/v19';APP=ROOT/'Qaroshi_18_19_Living_Language_Studio.html'
for p in [D18,D19]:p.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(ROOT/'tools/v18_19'))
from content import SCENARIOS,CONTRASTS,REGISTER_RULES,PATHS
from interaction_cases import ROLEPLAY

def readcsv(rel):
 with (ROOT/rel).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def emitcsv(path,rows):
 if not rows:raise ValueError('no rows: '+str(path))
 with path.open('w',encoding='utf-8',newline='') as f:
  out=csv.DictWriter(f,fieldnames=list(rows[0]));out.writeheader();out.writerows(rows)
def emitjson(path,val):path.write_text(json.dumps(val,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

phrases=readcsv('data/v17/everyday_phrases.csv')
lookup={p['id']:p for p in phrases}
lexemes=readcsv('data/lexicon.csv')
lex={p['qaroshi']:p for p in lexemes}
assert len(lexemes)==30000 and len(lookup)==656
for word in lex:assert unicodedata.is_normalized('NFC',word),word

scenes=[];all_sids=[]
for i,(title,domain,context,sids) in enumerate(SCENARIOS,1):
 assert len(sids)>=3 and len(sids)==len(list(sids)),title
 assert all(s in lookup for s in sids),(title,sids)
 turns=[]
 for j,sid in enumerate(sids):
  r=lookup[sid];turns.append({'speaker':('A' if j%2==0 else 'B'),'reference_id':sid,'qaroshi':r['qaroshi'],
    'english':r['english'],'ipa':r['ipa'],'sound_out':r['sound_out'],'review_rules':r['review_rules'],
    'provenance':'exact documented bilingual reference phrase; scenario ordering editorial'})
 scenes.append({'id':f'C18-{i:03d}','title':title,'domain':domain,'context':context,
  'provenance':'editorial teaching scenario assembled from documented phrases; not an observed conversation',
  'turns':turns})
 all_sids.extend(sids)
assert len({x['title'] for x in scenes})==len(scenes)

contrasts=[]
for i,(theme,a,b,note) in enumerate(CONTRASTS,1):
 assert a in lookup and b in lookup and a!=b
 contrasts.append({'id':f'M18-{i:03d}','theme':theme,'left_id':a,'right_id':b,
  'left_qaroshi':lookup[a]['qaroshi'],'left_english':lookup[a]['english'],
  'right_qaroshi':lookup[b]['qaroshi'],'right_english':lookup[b]['english'],
  'instruction':note,'provenance':'original v17 documented reference phrases, annotated editorial comparison'})

rules=[]
for i,(name,topic,note,good,bad,source) in enumerate(REGISTER_RULES,1):
 rules.append({'id':f'G18-{i:03d}','name':name,'topic':topic,'rule':note,'supported_example':good,
  'contrast_or_nonpreferred_example':bad,'source':source,'status':'reviewed pedagogical restatement; canonical grammar unchanged'})

paths=[]
for i,(title,ids) in enumerate(PATHS,1):
 assert all(s in lookup for s in ids)
 paths.append({'id':f'P18-{i:02d}','title':title,'source_ids':ids,'answers':[{'english':lookup[s]['english'],'qaroshi':lookup[s]['qaroshi'],'ipa':lookup[s]['ipa']} for s in ids]})

# The v14 validator has an old, documented false-positive for case-marked
# khe-m. Keep examples byte-for-byte and encode a narrow checker exception.
protected=['S00019','S00099','S00104']
for p in phrases:
 if p['id'] in protected:assert 'khe-m' in p['qaroshi'] or 'ruki ' in p['qaroshi']
parser_cases=[]
for s in protected:
 r=lookup[s];parser_cases.append({'source_id':s,'qaroshi':r['qaroshi'],'rule':'wh-argument case suffix; grammar §36',
 'decision':'reference-protected; do not replace with unmarked khe or discard as malformed',
 'status':'parser erratum, not canonical change'})
for s in ['S00003','S00107','S00108','S00139']:
 r=lookup[s];parser_cases.append({'source_id':s,'qaroshi':r['qaroshi'],'rule':'terminal question he',
 'decision':'retain he in full independent questions','status':'canonical grammar'})
for s in ['S00011','S00012']:
 r=lookup[s];parser_cases.append({'source_id':s,'qaroshi':r['qaroshi'],'rule':'minimal reply',
 'decision':'source full response can have resonance; bare shë/nu may be fragment',
 'status':'canonical grammar'})

emitjson(D18/'source_linked_conversation_paths.json',scenes)
emitcsv(D18/'meaning_contrasts.csv',contrasts)
emitcsv(D18/'pragmatic_register_rules.csv',rules)
emitjson(D18/'ten_practical_paths.json',paths)
emitcsv(D18/'grammar_parser_errata.csv',parser_cases)

# Practical adjacency-pair drills are deliberately context-dependent.
roleplays=[]
for i,(title,context,prompt,choices,correct,reason) in enumerate(ROLEPLAY,1):
 assert len(set(choices))==3 and correct in choices and prompt in lookup
 for sid in choices:assert sid in lookup
 roleplays.append({'id':f'R18-{i:03d}','title':title,'context':context,
   'prompt_id':prompt,'prompt_q':lookup[prompt]['qaroshi'],'prompt_en':lookup[prompt]['english'],
   'choices':[{'id':sid,'qaroshi':lookup[sid]['qaroshi'],'english':lookup[sid]['english']} for sid in choices],
   'correct_id':correct,'reason':reason,
   'status':'editorial context-specific response drill based on exact reference sentences'})
emitjson(D18/'contextual_reply_drills.json',roleplays)
# Pronunciation reading practice includes no synthetic audio. Every exact IPA
# and sound-out is copied from the reference. Spoken naturalness is not claimed.
practice_ids=list(dict.fromkeys([s for scene in SCENARIOS for s in scene[3]]))
reading=[]
for i,sid in enumerate(practice_ids,1):
 r=lookup[sid]
 reading.append({'id':f'PH18-{i:03d}','reference_id':sid,'english':r['english'],
  'qaroshi':r['qaroshi'],'broad_ipa':r['ipa'],'sound_out':r['sound_out'],
  'rhythm_instruction':'Read the documented stressed syllables and question/request ending. Do not invent dropped resonance markers.',
  'human_audio_available':'no'})
emitcsv(D18/'pronunciation_reading_93.csv',reading)


candidates=readcsv('data/v16_2/all_3817_candidates_screened.csv')
reviewed=readcsv('data/v16_2/individually_editorially_reviewed.csv')
roots=readcsv('data/v16/productive_root_learning_ladder.csv')
compounds=readcsv('data/v16/compound_decomposition_13379.csv')
root_proposals=readcsv('data/v16_2/eight_root_decision_dossiers.csv')
base120=readcsv('data/v17/core_learning_120.csv')
assert len(candidates)==3817 and len(reviewed)==65 and len(root_proposals)==8
assert len(compounds)==13379
review_by={(r['canonical_id'],r['candidate_form']):r for r in reviewed}

# Editorial evidence is primary. Numeric machine heuristics NEVER auto-approve.
priority=[]
for r in candidates:
 manual=review_by.get((r['canonical_id'],r['candidate_form']))
 status=(manual or r)['status']
 risks=[x.strip() for x in r['risk_codes'].split('|') if x.strip()]
 risk_score=len(risks)*2+(5 if int(r['collision_target_count'] or 0)>1 else 0)+(
  3 if 'secondary_component_sense' in risks else 0)
 tier={'manual_trial':'trial_only','manual_hold':'semantic_hold','manual_reject':'blocked_false_friend',
       'screened_shortlist_not_reviewed':'machine_priority_unapproved',
       'defer_for_editorial_attention':'deferred_unreviewed'}.get(status,'deferred_unreviewed')
 action= ('Do not use as a replacement. Explain which component sense is wrong.' if tier=='blocked_false_friend'
  else 'Contrast with the other meanings before considering a teaching paraphrase.' if tier=='semantic_hold'
  else 'Use only as an explicitly labeled trial paraphrase; never silently replace the canonical form.' if tier=='trial_only'
  else 'Only a machine proposal: request independent contextual interpretation and lexical review.')
 priority.append({'canonical_id':r['canonical_id'],'canonical_word':r['canonical_word'],
 'canonical_english':r['canonical_english'],'candidate_form':r['candidate_form'],'modifier':r['modifier'],
 'modifier_meaning':r['modifier_meaning'],'head':r['head'],'head_meaning':r['head_meaning'],
 'review_tier':tier,'risk_score':risk_score,'risk_codes':r['risk_codes'],'canonical_chars':r['canonical_chars'],
 'candidate_chars':r['candidate_chars'],'candidate_number':r['candidate_number'],
 'editorial_basis':(manual or r)['editorial_note'],'teaching_action':action,
 'speaker_attested':'no','canonical_adoption':'no'})
assert len(priority)==3817

# A ranked learning path: begin with v17 everyday words, then prioritize
# productive bases by recorded number of compounds using them.
core_order=[];seen=set()
for r in base120:
 w=r['root']
 if w not in seen:seen.add(w);core_order.append(w)
for r in roots:
 w=r['root']
 if w not in seen and w in lex:
  seen.add(w);core_order.append(w)
# All 1,820 documented ultimate roots are contained in the root graph. Some
# of the 120 practical roots need not be ultimate compound bases.
compound_base={w.strip() for r in compounds for w in r['ultimate_base_roots'].split('+')}
assert len(compound_base)==1820,len(compound_base)
for r in roots:
 if r['root'] in compound_base:continue
 raise AssertionError('root ladder contains unexpected root '+r['root'])
assert compound_base.issubset(seen)

compound_sets=[set(x.strip() for x in r['ultimate_base_roots'].split('+')) for r in compounds]
checkpoints=[120,200,400,600,1000,1200,len(core_order)]
coverage={n:sum(s.issubset(set(core_order[:n])) for s in compound_sets) for n in checkpoints}
ladder=[]
reuse={r['root']:int(r['compounds_using_base_root']) for r in roots}
for i,w in enumerate(core_order,1):
 r=lex[w];ladder.append({'rank':i,'root':w,'english':r['english'],'pos':r['pos'],'ipa':r['ipa'],
 'sound_out':r['sound_out'],'tier':('daily_core' if i<=120 else 'productive_extension' if i<=400 else 'reference'),
 'compound_reuse':reuse.get(w,0),'canonically_existing':'yes','speaker_attestation_claim':'none'})

# Human interpretation tests have prompts, not fake feedback or measurements.
# No new words are accepted as a result of this script.
interp=[]
chosen=[]
for tier,limit in [('trial_only',44),('semantic_hold',9),('blocked_false_friend',12),('machine_priority_unapproved',80)]:
 selected=[r for r in priority if r['review_tier']==tier][:limit]
 chosen+=selected
for i,r in enumerate(chosen,1):
 interp.append({'id':f'H19-{i:03d}','source_headword':r['canonical_word'],'target_meaning':r['canonical_english'],
 'test_form':r['candidate_form'],'component_a':r['modifier'],'component_a_primary_gloss':r['modifier_meaning'],
 'component_b':r['head'],'component_b_primary_gloss':r['head_meaning'],
 'review_tier':r['review_tier'],'independent_prompt':'Without seeing target meaning, write a literal reading, possible ambiguity, and whether you would use it in context.',
 'judgment_status':'pending external interpretation; editorial status not community ratification'})

emitcsv(D19/'reviewed_and_screened_3817.csv',priority)
emitcsv(D19/'productive_root_curriculum.csv',ladder)
emitcsv(D19/'interpretation_trials.csv',interp)
# Retain eight human-readable unapproved concepts; do not coin others.
emitcsv(D19/'unapproved_root_dossiers.csv',root_proposals)

manifest={
 'release':'18.0+19.0','canonical_dictionary':30000,'canonical_examples':4383,
 'source_anchored_dialogue_scenarios':len(scenes),'scenario_turns':sum(len(s['turns']) for s in scenes),
 'distinct_source_phrase_ids_in_scenarios':len(set(all_sids)),
 'editorial_contrasts':len(contrasts),'pragmatic_grammar_rules':len(rules),
 'structured_practice_paths':len(paths),'parser_errata':len(parser_cases),
 'contextual_reply_drills':len(roleplays),'pronunciation_readings':len(reading),
 'semantics_candidate_proposals':len(priority),
 'manual_review_records':len(reviewed),
 'review_tiers':dict(collections.Counter(r['review_tier'] for r in priority)),
 'unapproved_root_dossiers':len(root_proposals),
 'root_curriculum_entries':len(ladder),'ultimate_productive_roots':len(compound_base),
 'compound_coverage_by_learned_roots':coverage,
 'canonical_words_added_or_replaced':0,
 'release_policy':'pedagogical usage layer; source-aligned teaching only; no spontaneous-speaker claims',
 'outside_changes_policy':'all v18/19 files are in new versioned paths; existing source files remain untouched',
}
emitjson(ROOT/'data/v18_19_manifest.json',manifest)
# Source data stays explicitly separated by provenance/status.
mini_lex=[{'w':r['qaroshi'],'g':r['english'],'p':r['pos'],'id':r['id'],'ipa':r['ipa'],'s':r['sound_out'],
 't':r['type'],'c':r['components']} for r in lexemes]
mini_phrase=[{'id':r['id'],'q':r['qaroshi'],'e':r['english'],'ipa':r['ipa'],'sound':r['sound_out'],'cat':r['category'],'risk':r['review_rules']} for r in phrases]
mini_review=[{'w':r['canonical_word'],'g':r['canonical_english'],'f':r['candidate_form'],'m':r['modifier'],'mg':r['modifier_meaning'],
 'h':r['head'],'hg':r['head_meaning'],'tier':r['review_tier'],'why':r['editorial_basis'],'risks':r['risk_codes']} for r in priority]
mini_roots=[{'w':r['root'],'g':r['english'],'n':r['compound_reuse'],'ipa':r['ipa'],'tier':r['tier']} for r in ladder]
resonances=json.loads((ROOT/'data/resonances.json').read_text(encoding='utf-8'))
data={'scenes':scenes,'contrasts':contrasts,'rules':rules,'paths':paths,'lex':mini_lex,'phrase':mini_phrase,
      'review':mini_review,'roots':mini_roots,'rootDossiers':root_proposals,'resonance':resonances,'replyDrills':roleplays,'pronunciation':reading,'manifest':manifest}

template=(ROOT/'tools/v18_19/app_template.html').read_text(encoding='utf-8')
assert template.count('__QAROSHI_PAYLOAD__')==1
encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
APP.write_text(template.replace('__QAROSHI_PAYLOAD__',encoded),encoding='utf-8')
print(json.dumps({'html_bytes':APP.stat().st_size,'manifest':manifest},ensure_ascii=False,indent=2))
