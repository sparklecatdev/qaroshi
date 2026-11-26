#!/usr/bin/env python3
"""Qaroshi 16.2: meaning-first editorial proposals, never lexical auto-acceptance."""
from __future__ import annotations
import csv,json,re,hashlib,collections,math
from pathlib import Path
try:
 from rapidfuzz.distance import Levenshtein
except ImportError:
 class Levenshtein:
  @staticmethod
  def distance(a,b):
   row=list(range(len(b)+1))
   for i,c in enumerate(a,1):
    nextrow=[i]
    for j,d in enumerate(b,1):nextrow.append(min(nextrow[-1]+1,row[j]+1,row[j-1]+(c!=d)))
    row=nextrow
   return row[-1]
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v16_2';OUT.mkdir(parents=True,exist_ok=True)

def readcsv(p):
 with open(p,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def savecsv(p,rows):
 assert rows, p
 with open(OUT/p,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def primary(s):return s.split(';')[0].strip()
lex=readcsv(ROOT/'data/lexicon.csv');word={x['qaroshi']:x for x in lex}
orig=readcsv(ROOT/'data/v16_1/strict_modifier_head_candidates.csv')
rootfreq={x['root']:int(x['compounds_using_base_root']) for x in readcsv(ROOT/'data/v16/productive_root_learning_ladder.csv')}
evidence={x['qaroshi']:x for x in readcsv(ROOT/'data/v16/lexical_evidence_index_30000.csv')}
core={x['qaroshi'] for x in readcsv(ROOT/'data/v16_1/prioritized_core_1200.csv')}
# These judgements are *editorial screenings of proposed PARAPHRASES*, not standard lexical approvals.
# One entry for a single target may apply to the most defensible proposed form only.
EDITORIAL={
'banuaro':('trial','Wing + joint has literal compositional content; confirm the compound denotes the anatomical joint and not an artificial connector.'),
'khezhizë':('trial','Route/path + number is literal; confirm the same sense of numbering used on signs.'),
'ngodudi':('trial','Tool + bag is a literal carrying container; broad everyday use is plausible.'),
'lamiti':('trial','Dry + throat is a straightforward bodily state; test the ordinary collocation.'),
'helangëkhë':('trial','Sky + song is a literal poetic phrase, not automatically the conventional title of a genre.'),
'khengizë':('trial','Sky + festival is transparent but festival naming is culturally dependent.'),
'wakhuru':('trial','Star + festival can describe a festival about stars; cultural meaning remains open.'),
'zadonë':('trial','Dawn + song is a transparent poetic compound; do not equate it with a standardized dawn ritual.'),
'qopeshe':('trial','Moon + gathering has a literal descriptive reading; verify gathering sense and context.'),
'nguzora':('trial','Chosen family + bond gives the expected general relationship; does not replace every sense of bond.'),
'shakhëzha':('trial','Identity + expression aligns with expression of identity, subject to sociolinguistic context.'),
'shazano':('trial','Identity + disclosure aligns with openly sharing identity; privacy connotation must be checked.'),
'wimenga':('trial','Identity + affirmation makes sense as a relational act; is not automatically a legal affirming document.'),
'sakazo':('trial','Consent + withdrawal describes revocation, but may not specify legal or temporal effect.'),
'ngumokhu':('trial','Group + ownership can describe collective ownership; does not guarantee a legal ownership structure.'),
'shoketa':('trial','Pain + scale is plausible for a pain-assessment scale; not an automatic numerical measure.'),
'wazola':('trial','Conversation + partner is literal and useful in dialogue.'),
'dazuho':('trial','Group + conversation is compositional, useful as a phrase for a multiparty discussion.'),
'ngugomo':('trial','Flight + formation may describe spatial formation while flying.'),
'shëbëzo':('trial','Custom + emoji is literal for a user-created emoji asset.'),
'mëwesë':('trial','Joint + pain is literal, but the broad word is not a clinical diagnosis.'),
'bëlezhëwe':('trial','Food + forest is transparent as a food-producing forest, but the technical permaculture meaning is specialized.'),
'zesëwu':('trial','Face + towel is a clear household object phrase.'),
'zanëta':('trial','Leader + election describes an election to select a leader, but not its voting system.'),
'qulata':('trial','Door + hinge is a literal mechanical relationship, if hinge is the correct component sense.'),
'khezhëpe':('trial','Sky + map is straightforward; scope of celestial chart remains to review.'),
'shuhëde':('trial','Promise + ring is literal jewelry, not automatically an engagement ring.'),
'shahido':('trial','Personal + identity is meaningful but must not imply government ID.'),
'khubowe':('trial','Roommate + agreement makes sense; verify whether written agreement is implied.'),
'duniyu':('trial','Relationship + boundary is a natural metaphorical phrase if boundary sense extends socially.'),
'zabëshe':('trial','Privacy + boundary is a clear conceptual phrase, subject to the correct privacy domain.'),
'gugige':('trial','Informed + agreement is compositional; approval and consent remain distinct notions.'),
'kituwori':('trial','Clear + expectation is a descriptive phrase; register needs testing.'),
'qubëza':('trial','Personal + comfort is transparent and useful in everyday speech.'),
'ngukinga':('trial','Flight + practice is literal for repeated exercises in flight.'),
'romera':('hold','Distributive reading may be grammatical jargon; literal English split does not ensure the intended grammatical sense.'),
'pizikha':('hold','One form is proposed for multiple domain-specific informed-consent terms; preserve domain distinctions.'),
'këngopu':('hold','Shared proposed spelling conflates distinct intimacy and research consent contexts.'),
'ngizhobi':('hold','Shared proposed spelling conflates distinct research and intimate-consent contexts.'),
'rawaro':('reject','The component for tip means gratuity, not the anatomical end of a tail.'),
'nëqido':('reject','The component for mixing is sound mixing, not combining ingredients in a bowl.'),
'giduno':('reject','The component mask is a theatrical mask, not necessarily a cloth/medical face covering.'),
'ngukhëgo':('reject','The available grooming headword has a harmful-abuse sense, not grooming wing feathers.'),
'ngusuqo':('reject','The available grooming headword has a harmful-abuse sense, not grooming a tail.'),
'andango':('reject','A lexical surface resemblance is not evidence of meaning; do not promote a form without source validation.'),
'nguyota':('reject','The source uses philosophical space, not necessarily available physical wing room.'),
'nëdongu':('reject','The component display is a screen, not necessarily a body-language wing display.'),
'beliwë':('reject','Short is not the semantic equivalent of low visual acuity.'),
'ngolutuli':('reject','Low voltage is an electrical-potential concept, not physical shortness; the selected adjective would mislead.'),
'ngalerazi':('reject','Low bandwidth is a communications-capacity concept, not physical shortness; the selected adjective would mislead.'),
'pezhurëbo':('hold','Branch protection could be software development or literal tree protection; require domain-specific interpretation.'),
'bonge':('hold','Platform block is specialized; soft-block may mean more than a soft + block combination.'),
'zezhëbu':('hold','Hard-block is platform-specific; block has multiple literal senses.'),
'dadogo':('trial','Mistaken + identity describes a mistaken identity, without assuming a legal identity record.'),
'dela':('trial','Gender + identity is transparent as a social-identity compound, but definitions require human nuance review.'),
'korewo':('hold','Check source components carefully before treating a technical phrase as an ordinary compound.'),
'zudëshi':('reject','Neutral + voice is not the same as neutral language; generic language and voice need distinction.'),
'shëteza':('trial','Development + branch is plausibly compositional for software version-control branches.'),
'wibiha':('hold','Backwards translation is ambiguous without source and target-language context.'),
'kazuqo':('trial','Text-to-speech + voice has a literal technical interpretation; model vs voice distinction remains.'),
'khëshëluyu':('hold','Apology voice may be an apology register, not the same as apology language.'),
'shapoho':('trial','Name + privacy describes restricting name disclosure.'),
'shaboka':('hold','Existing component for change may refer to philosophical change, not a legal name change.'),
'zuzhëyo':('trial','Prospective + memory is a plausible technical term, though training examples should distinguish prospective from retrospective recall.'),
'ngisaga':('hold','Academic credit hour requires institution-specific credit sense, not general credit or clock time.'),
'zazozha':('trial','Transaction + boundary is a literal technical phrase; clarify the data-integrity context.'),
'zakume':('trial','Resonance + frequency is transparent for acoustics; not an emotional resonance sense.'),
'zhegiza':('trial','Updraft + corridor can describe a geographic route for lift, context-dependent.'),
'zhuzozha':('reject','Musical meter cannot correctly substitute for water measuring meter.'),
}
# Additional semantic false friends are detected by source parenthetical meaning restrictions.
FALSE_SENSE={'musical': ['meter (music)','mixing (music)','rest (music)','scale (music)','ratio (social)'],
'physical':['tip (gratuity)','grooming (abuse)','space (philosophy)','display (screen)','mask (theater)','short']}
collisions=collections.defaultdict(set)
for r in orig:collisions[r['candidate_form']].add(r['canonical_word'])
head_review=collections.Counter()
rows=[];manual=[];guarded=[]
for r in orig:
 target=word[r['canonical_word']];a=word[r['component_1']];b=word[r['component_2']]
 form=r['candidate_form'];p=r['components_match_primary_glosses']=='true';syllables=sum(1 for x in form if x in 'aeiouë')
 e=evidence.get(a['qaroshi'],{});f=evidence.get(b['qaroshi'],{})
 occa=int(e.get('controlled_reference_occurrences') or 0)+int(e.get('original_editorial_occurrences') or 0)
 occb=int(f.get('controlled_reference_occurrences') or 0)+int(f.get('original_editorial_occurrences') or 0)
 len_delta=len(form)-len(target['qaroshi'])
 poly=any('(' in primary(z['english']) or ')' in primary(z['english']) for z in (a,b))
 qual=any('(' in z['english'].split(';')[0] for z in (a,b))
 ambig=len(collisions[form])>1
 contained=bool(word.get(form))
 score=round(60+(32 if p else -25)+(8 if not qual else -22)+(8 if not ambig else -26)+(10 if len(form)<=14 else 0)-max(0,len(form)-15)*4-max(0,len_delta)*1.4+min(12,math.log1p(rootfreq.get(a['qaroshi'],0)+rootfreq.get(b['qaroshi'],0))*4)+min(9,math.log1p(occa+occb)*3),1)
 cues=[]
 if not p:cues.append('secondary_component_sense')
 if qual:cues.append('sense_qualifier_on_component')
 if ambig:cues.append('multi_target_collision')
 if contained:cues.append('canonical_form_collision_or_match')
 if len(form)>18:cues.append('long_for_spoken_use')
 if len_delta>7:cues.append('substantially_longer_than_canonical')
 if syllables>7:cues.append('many_syllables')
 if not occa and not occb:cues.append('components_unseen_in_reference')
 ed=EDITORIAL.get(r['canonical_word'])
 # Human editorial screening targets the shortest primary-sense option for each selected headword.
 manual_primary=(r['candidate_number']=='1')
 decision=ed[0] if ed and manual_primary else 'unreviewed'
 note=ed[1] if ed and manual_primary else 'Screening only: confirm semantic scope and conversational use before deciding.'
 if decision=='reject':head_review['manually_rejected']+=1
 if decision=='trial':head_review['manually_trial']+=1
 if decision=='hold':head_review['manually_hold']+=1
 if decision=='unreviewed' and p and score>=105 and not ambig and not qual and len(form)<=16:
  automated='screened_shortlist_not_reviewed'
 else: automated='defer_for_editorial_attention'
 status='manual_'+decision if decision!='unreviewed' else automated
 out={'canonical_id':target['id'],'canonical_word':r['canonical_word'],'canonical_english':target['english'],
 'candidate_form':form,'modifier':r['component_1'],'modifier_meaning':a['english'],
 'head':r['component_2'],'head_meaning':b['english'],
 'candidate_number':r['candidate_number'],'gloss_alignment':('primary' if p else 'secondary'),
 'syllable_approx':syllables,'canonical_chars':len(target['qaroshi']),'candidate_chars':len(form),
 'difference_in_length':len_delta,'corpus_uses_of_components':occa+occb,
 'compound_reuse_of_components':rootfreq.get(a['qaroshi'],0)+rootfreq.get(b['qaroshi'],0),
 'collision_target_count':len(collisions[form]),'risk_codes':' | '.join(cues) or 'general_naturalness_unverified',
 'machine_score':score,'status':status,'editorial_note':note,'is_canonical':'no' if not contained else 'potential_existing_form_check',
 'independently_speaker_attested':'no','proposed_for_dictionary_acceptance':'no','local_reviewer_decision':'pending','reviewer_notes':''}
 rows.append(out)
 if decision!='unreviewed':manual.append(out)
 if automated=='screened_shortlist_not_reviewed' and decision=='unreviewed':guarded.append(out)
savecandidate='ALL'
savecsv('all_3817_candidates_screened.csv',rows)
savecsv('individually_editorially_reviewed.csv',manual)
savecsv('machine_shortlist_unapproved.csv',sorted(guarded,key=lambda x:-x['machine_score']))
# Root-gap research: distinguish lack of an exact noun gloss from missing all available semantic resources.
# Suggested new roots are *explicitly invented placeholders*. Reusing a known root is the default.
ROOT_PROPOSALS=[
('generic physical credential card','mashëwo','n','Flat physical credential or payment token, not a graphics circuit board','card','card','8','new_root_candidate','Distinguish payment/ID/gift cards from computer expansion cards; avoid blanket adoption.'),
('personal handwritten signature','tëwaya','n','Personal handwritten/marked assent or identity sign, not a cryptographic signature','signature','signature','7','new_root_candidate','Do not use this for time signatures or cryptographic digital signatures.'),
('discourse context','leshëro','n','Background information required to interpret an utterance, not physical setting','context','context','5','new_root_candidate','Keep situational context distinct from textual surroundings and historical context.'),
('statistical bias','bëgawiro','n','Systematic skew affecting an inference or estimator, not a mere preference','bias','bias','7','new_root_candidate','Use narrow technical sense; do not collapse prejudicial bias and sampling error.'),
('written annotation note','shinëmora','n','Short written annotation attached to a source, not a musical pitch','note','note','7','new_root_candidate','Avoid musical notes, notifications and short personal messages unless independently reviewed.'),
('numeric threshold','gakënu','n','Numerical cutoff or decision boundary, not a physical doorway sill','threshold','threshold','7','new_root_candidate','Technical threshold does not imply clinical or regulatory validation.'),
('formal public notice','pulëma','n','Formal written notice or announcement intended for recipients','notice','notice','5','new_root_candidate','Not a verb meaning to notice; legal service requirements vary.'),
('recurrent cycle noun','wëdaro','n','Repeating sequence/process taken as a noun, distinguished from the documented verb rekesi','cycle','cycle','10','defer_coinage_due_existing_verb','Try existing rekesi and documented -rëma derivation first; a new root is costly.'),
]
rootrows=[]
words=list(word)
for concept,q,pos,definition,keyword,gloss,count,status,note in ROOT_PROPOSALS:
 close=sorted(((Levenshtein.distance(q,w),w) for w in words),key=lambda z:(z[0],z[1]))[:3]
 assert q not in word
 rootrows.append({'concept':concept,'tentative_form':q,'part_of_speech':pos,'narrow_proposed_sense':definition,
 'recurring_gap_keyword':keyword,'gap_existing_headwords':count,
 'nearest_existing_forms':' | '.join(f'{a} (distance {n})' for n,a in close),
 'phonotactic_comment':'CV-oriented spelling using only canonical letters; expert pronunciation review required',
 'proposal_status':status,'review_comment':note,'canonical_entry_created':'no','independent_attestation':'none','decision':'not_accepted','reader_review_notes':''})
savecsv('eight_root_decision_dossiers.csv',rootrows)
reuse=[
('cycle (verb)','rekesi','Existing canonical verb means cycle; investigate noun usage and -rëma event nominalization before new root.'),
('aid / helpful instrument','dëmi','Canonical verb help; -këlë instrument suffix may give a device reading, requires valency review.'),
('self / reflexivity','-ne','Documented reflexive voice suffix. Do not invent one generic self root for every construction.'),
('greeting as interjection','ha','Canonical greeting interjection. A greeting event noun is not automatically the same form.'),
('established information','mëna','Canonical fact/established information covers only a subset of information senses.'),
('human consent','maho','Already denotes freely given consent; avoid new blanket synonym for agreement.'),
('call as telephone vs animal sound','no single stem','Separate contact/communication and animal vocalization; do not force one new universal root.'),
('name as lexical item','lëru','Canonical name stem may be usable for name-related compounds; check exact domain.'),
]
savecsv('reuse_before_coinage.csv',[{'concept':k,'canonical_resource':q,'editorial_rationale':s,'review_state':'provisional research guidance'} for k,q,s in reuse])
# Test-use examples: speculative roots used as *headwords only in a proposal table*;
# do not present these combinations as approved dictionary forms or as speaker attestations.
from collections import defaultdict
semantic=defaultdict(list)
for x in lex:
 if x['type']=='headword' and x['pos'] in ('adj','n'):
  for gl in x['english'].split(';'):
   name=re.sub(r'\([^)]*\)','',gl).strip().casefold()
   if name and not '(' in gl and len(name.split())<3:semantic[name].append(x)
examples=[]
for item in rootrows:
 base=item['tentative_form'];key=item['recurring_gap_keyword']
 targets=[x for x in lex if x['type']=='headword' and x['pos']=='n' and primary(x['english']).casefold().endswith(' '+key)]
 for target in targets:
  # A narrow proposed root must not be stretched into a homonymous English sense.
  allowed={
   'card':('loyalty card','gift card','fare card','debit card','payment card','credit card'),
   'signature':('legal signature','petition signature','package signature'),
   'context':('shared context','missing context','background context','historical context'),
   'bias':('selection bias','sampling bias','publication bias','response bias','measurement bias','reporting bias'),
   'note':('context note','dictionary editorial note','editor\'s note','correction note','dialect note','release note'),
   'threshold':('decision threshold','p-value threshold','compressor threshold','statistical significance threshold'),
   'notice':('legal notice','accessibility notice','compliance notice','moderation notice','attribution notice','roadwork notice'),
   'cycle':(),
  }
  if primary(target['english']).casefold() not in allowed.get(key,()):continue
  phrase=primary(target['english']).casefold()
  left=phrase[:-(len(key)+1)].strip()
  choices=semantic.get(left,[])
  if not choices:continue
  comp=sorted(choices,key=lambda z:(len(z['qaroshi']),z['qaroshi']))[0]
  proposed=comp['qaroshi']+base
  if proposed in word:continue
  examples.append({'source_headword':target['qaroshi'],'source_english':target['english'],
   'draft_modifier':comp['qaroshi'],'modifier_english':comp['english'],
   'new_root_proposal':base,'draft_compositional_paraphrase':proposed,
   'candidate_not_standard':'true','validation':'spelling and English-gloss components only; no independent meaning acceptance',
   'human_review':'pending'})
savecsv('hypothetical_new_root_derivatives.csv',examples)
# Semantic teaching contrasts reflect *documented grammar*, not proposed coinage.
lessons=[
 ('Known lexical base','banu','wing','The lexical meaning must be learned; grammar cannot infer it from the spelling.'),
 ('Transparent candidate','banuqamago','wing joint','Proposed modifier banu + head qamago; not a synonym until review.'),
 ('Direct-object case','banu-m','wing as object','Case suffix -m is grammatical, not a new dictionary entry.'),
 ('Locative case','naro-lo','at home','Case -lo marks location; do not infer the base meaning from the suffix.'),
 ('Comitative case','ti-wa','with you','Case -wa encodes accompaniment, not an English pronoun substitution.'),
 ('Plural after base','mara-ri','friends','Nominal plural -ri is productive.'),
 ('Verb past','goro-te','flew','Past -te attaches to a known verb.'),
 ('Verb permission','goro-ho','may fly','Permission -ho is not ability -ki.'),
 ('Verb ability','goro-ki','can fly','Ability -ki differs from permission.'),
 ('Verb habitual','goro-në','flies habitually','The habitual ending is aspect, not a new lexeme.'),
 ('Causative','goro-ru','cause to fly','Causative marks changed valency, not a new root.'),
 ('Instrument','dëmi-këlë','helping instrument','Only an exploratory productive derivation: application and semantic suitability require review.'),
 ('Event noun','rekesi-rëma','cycling occurrence','Event nominalizer, not a confirmed generic noun for cycle.'),
 ('Resonance register','sen mi kima-m këmë.','I drink water.','Every complete sentence requires an initial resonance marker.'),
 ('SOV sentence','sen naru qaroshi-m shiri.','We speak Qaroshi.','The direct object precedes the verb in ordinary clauses.'),
 ('Adjective order','sen ti haro.','You are well.','Adjective predication does not require present-tense copula.'),
]
savecsv('sixteen_grammar_and_learnability_examples.csv',[{'topic':a,'qaroshi':b,'english':c,'comment':d,'source_status':'canonical example or explicitly labeled proposal'} for a,b,c,d in lessons])
# Report with explicit provenance and unresolved review scope
summary={
 'canonical_entries_unchanged':len(lex),'all_candidate_rows':len(rows),'manual_editorial_review_rows':len(manual),
 'manual_trial_count':head_review['manually_trial'],'manual_hold_count':head_review['manually_hold'],'manual_reject_count':head_review['manually_rejected'],
 'automatic_unreviewed_shortlist_count':len(guarded),'candidate_forms_for_independent_acceptance':0,
 'hypothetical_new_root_derivatives':len(examples),'learning_contrasts':len(lessons),'root_decision_dossiers':len(rootrows),'new_roots_added_to_canonical_dictionary':0,'reuse_before_coinage_analyses':len(reuse),
 'canonical_lexicon_sha256':hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest(),
 'limitations':['Exact English gloss splits are not proof of natural Qaroshi meaning.',
 'Manual editorial trial labels are *not* independent speaker acceptance.',
 'Coined root proposals are noncanonical and add memorization cost unless justified.',
 'Long compounds are less practical in everyday conversation even when interpretable.',
 'Some existing vocabulary is conventional and legitimately requires memorization.',
 'A screened shortlist is not a reviewed approval list.']}
(OUT/'review_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
