#!/usr/bin/env python3
"""Reproducible Qaroshi Standard 8.0 consolidation.

Preserves all 29 immutable 7.0 baseline SHA256 paths. Generates an authoritative
current consolidated reference and editioned dictionary; never asserts independent
speaker attestation or automatic general valency from a single sentence.
"""
from __future__ import annotations
import collections,csv,gzip,hashlib,io,itertools,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/standard_8';DOC=ROOT/'docs/standard_8';OUT.mkdir(parents=True,exist_ok=True);DOC.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools/standard_8'))
from scope import analyze,evaluate

def rows(name):
 with (ROOT/name).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def js(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
def csvout(path,records):
 if not records:raise AssertionError('empty '+str(path))
 with path.open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
def jsonout(path,v):path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

lex=rows('data/lexicon.csv');dictionary={r['qaroshi']:r for r in lex};corpus=rows('corpus/parallel_sentences.csv');source={r['id']:r for r in corpus};v28=rows('data/v28_34/verb_frame_inventory_400.csv');senses=js('data/semantics/curated_senses.json');manual=js('data/semantics/valency_frames.json');meaning=rows('data/v28_34/meaning_boundaries.csv');lex800=rows('data/v28_34/core_semantic_index_800.csv');oldcom=rows('data/v16/compound_decomposition_13379.csv');over=js('data/v28_34/adopted_function_words.json')
assert len(lex)==30000 and len({r['qaroshi'] for r in lex})==30000
assert len(corpus)==4383 and len(v28)==400 and len(over)==1 and over[0]['lemma']=='nëgëra'
assert len(senses)==48 and len(manual)==25 and len(meaning)==30 and len(oldcom)==13379
basehash=js('data/v14/baseline_sha256.json')['sha256'];bad=[n for n,h in basehash.items() if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h];assert not bad,bad

# A. A directly usable editioned lexicon, preserving every previous ID and byte
# of the original lexicon as input, not altering the frozen data file.
addition={'id':'Q8D001','qaroshi':over[0]['lemma'],'pos':over[0]['pos'],'english':'not every; not all',
  'domain':'Grammar and connective words','type':'edition8_function_word','components':'','note':'Post-7.0 adopted determiner, restricted to explicit nonempty quantified groups. See Standard 8.0 chapter 22/78.','ipa':over[0]['ipa'],'reading':over[0]['reading'],'sound_out':over[0]['reading']}
assert addition['qaroshi'] not in dictionary and addition['id'] not in {r['id'] for r in lex}
current=lex+[addition]
# Plain CSV is distributed compressed, and can be regenerated from originals.
text=io.StringIO(newline='');w=csv.DictWriter(text,fieldnames=list(lex[0]),lineterminator='\n');w.writeheader();w.writerows(current)
(OUT/'dictionary_30001.csv.gz').write_bytes(gzip.compress(text.getvalue().encode('utf8'),compresslevel=9,mtime=0))

# B. All 400 verbs get a decision with a direct source citation where one exists.
# These are *audited* forms, not generalized norms across object classes.
validated=[];counts=collections.Counter()
for r in v28:
 source_ids=[i.strip() for i in r['example_ids'].split('|') if i.strip()]
 documented=[]
 for sid in source_ids:
  if sid not in source:continue
  e=source[sid]
  t=re.findall(r'[a-zë]+(?:-[a-zë]+)*',e['qaroshi'].lower())
  if not t or t[0] not in {x['marker'] for x in js('data/resonances.json')}:continue
  # Find actual predicate just before question he / request ya / qinë.
  end=t[-2] if t[-1] in {'he','ya','qinë'} and len(t)>1 else t[-1]
  if end.split('-')[0]!=r['lemma']:continue
  stem=t[1:-1] if end==t[-1] else t[1:-2]
  objects=[x[:-2] for x in stem if x.endswith('-m') and x[:-2] in dictionary and dictionary[x[:-2]]['pos']=='n']
  documented.append((e,t,objects))
 documented.sort(key=lambda z:(-bool(z[2]),len(z[1]),z[0]['id']))
 best=documented[0] if documented else None
 direct=[(e,t,objs) for e,t,objs in documented if len(objs)==1 and t[1]=='mi' and t[0]=='sen']
 source_example=(direct[0] if direct else best)
 manually=r['review_status']=='normative_manual_frame_24_27'
 former=r['review_status']=='source_exemplar_limited_license'
 if manually:status='fully_reviewed_general_frame';decision='retain adopted required/optional roles unchanged';authority='general (only listed senses)'
 elif direct:status='source_licensed_exact_object_pattern';decision='license exact documented noun-object example; no generalized object class/voice';authority='exact lexical exemplar only'
 elif best:
  status='source_licensed_finite_pattern';decision='license the recorded finite construction only; do not infer an object class';authority='documented finite phrase only'
 else:
  status='needs_manual_clause_analysis';decision='withhold new valency permissions until clause or lexical reading is resolved';authority='none from this audit'
 # Every entry gets an individual decision and an explicit uncertainty boundary.
 x={'frame_id':r['frame_id'],'lemma':r['lemma'],'dictionary_id':r['dictionary_id'],'reference_gloss':r['reference_gloss'],
    'decision':status,'linguistic_rule':decision,'scope_of_authority':authority,
    'required_roles':r['reviewed_required_roles'] if manually else ('subject:mi and object:-m('+direct[0][2][0]+')' if direct else 'not generalized'),
    'licensed_optional_roles':r['reviewed_optional_roles'] if manually else 'none extrapolated',
    'example_source_id':source_example[0]['id'] if source_example else '',
    'example_qaroshi':source_example[0]['qaroshi'] if source_example else '',
    'example_english':source_example[0]['english'] if source_example else '',
    'exact_documented_object_root':direct[0][2][0] if direct else '',
    'other_source_ids':' | '.join(source_ids),
    'observed_cases':r['observed_case_counts'],
    'passive_or_causative_authority':r['passive_actor_case'] if manually else 'not licensed from examples',
    'editorial_provenance':'Source-based limited decision by Standard 8 editor; no independent speaker attestation',
    'general_frame_review':'yes, inherited from 24–27' if manually else 'no: requires human editorial generalization; source license narrow'}
 validated.append(x);counts[status]+=1
assert len(validated)==400 and len({r['dictionary_id'] for r in validated})==400
csvout(OUT/'verb_audit_400.csv',validated)
# Source-independent unseen-sentence valency probe suite: no fake ground-truth.
probes=[]
for i,r in enumerate(validated):
 if not r['example_source_id']:continue
 probes.append({'id':f'V8P-{i+1:03d}','lemma':r['lemma'],'source_id':r['example_source_id'],'qaroshi':r['example_qaroshi'],
 'documented_english':r['example_english'],'allow_exact_example':'yes',
 'allow_arbitrary_object_or_passive':'yes only if explicitly specified in older manual frame' if r['general_frame_review'].startswith('yes') else 'no',
 'independent_speaker_test':'not performed','decision':r['decision']})
csvout(OUT/'source_backed_valency_probes.csv',probes)

# C. Prioritize and make real lexical decisions on awkward compounds. These are
# explicit core-sense constraints, not a blanket acceptance of every head gloss.
COMPOUND_DECISIONS={
 'bekazoshërawëlon':('lexicalized, not transparent','Nail file means the abrasive grooming implement; the component head also means a digital file. Do not infer stored data or use this compound for a file containing nail information.'),
 'bebonawaro':('context-bounded lexical compound','Robot arm refers to a mechanical manipulator, not literally an animal foreleg.'),
 'yërawaroashërawën':('technical lexicalized compound','A software bug is a defect in instructions/behavior; no living insect is implied.'),
 'zhalarokharo':('context-bounded compound','Smoke alarm refers to a detector/alert device, not fear of smoke itself.'),
 'zhënohozhilazo':('logic-domain lexicalized compound','False dilemma describes an argument that falsely limits alternatives, not an ordinary difficult choice.'),
 'banungërawëra':('anatomy-domain compound','Wing pattern denotes spatial markings or arrangement on a wing, not necessarily recurrence over time.'),
 'banunohowa':('anatomy-domain compound','Wing safety means risk prevention concerning wings; no guarantee of zero danger.'),
 'banushënaroa':('context-bounded compound','Wing signal denotes a wing-based signaling event, not a digital transmission by default.'),
 'buzhezirërawi':('statistics-domain compound','A statistical result is an outcome of analysis, not any consequence.'),
 'buzhezishërawëhu':('statistics-domain compound','A statistical report is a document presenting analysis, not just any telling of information.'),
 'khuramorushira':('literary-domain compound','A wind story concerns wind; breath of the world is metaphorical, not physical identity.'),
 'khuranëdëzu':('cultural-domain compound','Wind gathering has a local event meaning; the wind root does not assert world-breath metaphysics.'),
 'khurarëmawe':('cultural-domain compound','Wind dance describes a dance associated with wind, not literal weather movement.'),
 'kunipapashiwaro':('privacy-domain compound','A private message means restricted intended recipients, not necessarily encryption.'),
 'kunipapashiwena':('technical-domain compound','A private network may have access controls but not automatic anonymity or encryption.'),
 'kunipapashërawëlon':('technical-domain compound','Private file describes access expectations, not a guarantee of secure storage.'),
 'kërawëmikelagu':('security-domain compound','Password compromise means unauthorized disclosure/control of an access secret, not a negotiated compromise.'),
 'kërawëminguyabo':('security-domain compound','Password failure is rejection/invalidity, not necessarily memory loss.'),
 'kërawëmirëlawë':('security-domain compound','Password risk is a possibility of security harm, not proof of compromise.'),
 'kërawëmiweheda':('security-domain compound','Password policy means rules for creating/handling secrets, not personal political policy.'),
 'banungëmarëho':('anatomy-domain compound','Wing fatigue means reduced muscle or structural function in a wing; not abstract weariness of flight culture.'),
 'banungërawëmo':('anatomy-domain compound','Wing injury is physical harm to a wing, not a figurative insult.'),
 'bapërishënoa':('interface-domain compound','A touch option is a selectable touch input/setting, not freedom to touch a person.'),
 'bayeshashimarë':('language-domain compound','A spoken dictionary is a dictionary available in spoken form, not merely words someone says aloud.'),
 'bekazoshërawëlon':('lexicalized, not transparent','Nail file is an abrasive nail-care implement, not a digital computer file; do not infer a digital head sense.'),
 'beliwëshënoa':('accessibility-domain compound','Low-vision option is an accessibility choice; not necessarily an option located physically low.'),
 'bihuzugoshëroho':('physics-domain compound','Thermal energy is physical energy, not personal stamina.'),
 'bikhimingëmarawo':('technical-domain compound','Session storage is data retained for a session, not a physical warehouse by default.'),
 'budopeshëroho':('physics-domain compound','Magnetic energy is physical energy, not personal stamina.'),
 'bowatorëlawë':('security-domain compound','Phishing risk describes security exposure, not an actual fishing hazard.'),
 'bowadorëlawë':('security-domain compound','Encryption risk relates to encryption systems/security, not proof that encryption has failed.'),
 'boshëboshungëmarawo':('technical-domain compound','Deleted storage describes a state of stored data, not a physically erased storage container.'),
 'guzayawërawi':('health-domain compound','Hydration plan specifies a hydration regimen; not any list of future activities.'),
 'guzayadëmiho':('health-domain compound','Hydration care involves meeting fluid needs; not an unconditional medical treatment claim.'),
 'buzhezirërawi':('statistics-domain compound','Statistical result is an output of statistical analysis, not a general consequence.'),
 'dudasarërawi':('ecology-domain compound','Ecological result is an ecosystem observation/outcome, not a generic consequence.'),
 'dudasashërawëhu':('ecology-domain compound','Ecological report is an account of ecological findings, not any speech to other people.'),
 'dudasamorëmi':('ecology-domain compound','Ecological study is structured examination of ecosystems, not studying anything outdoors.'),
 'buzhezimorëmi':('statistics-domain compound','Statistical study means analysis using statistics, not every careful study.'),
 'bepëqoshëna':('social-domain compound','Repair trust means rebuilding confidence; it does not imply the other party has forgiven the actor.'),
 'behuzidëmari':('agriculture-domain compound','Smallholder project relates to small-scale land ownership/operation, not physically tiny people.'),
 'bihuzugongëmarawo':('thermal-domain compound','Thermal storage means retention of heat/thermal energy, not digital information storage by default.'),
}
# Additional manually reviewed canonical-vs-proposed false friends (12 rejected
# earlier). 8.0 ratifies the existing canonical headwords, not unapproved forms.
reviews=rows('data/v16_2/individually_editorially_reviewed.csv')
rejected=[r for r in reviews if r['status']=='manual_reject']
assert len(rejected)==12
compidx={r['compound']:r for r in oldcom};lexical_decisions=[]
for name,(status,note) in sorted(COMPOUND_DECISIONS.items()):
 if name not in compidx:raise AssertionError('Missing canonical compound '+name)
 r=compidx[name]
 lexical_decisions.append({'decision_id':f'L8-{len(lexical_decisions)+1:03d}','canonical_id':r['id'],'canonical_word':name,
 'canonical_english':r['english'],'modifier':r['modifier'],'modifier_gloss':r['modifier_english'],'head':r['head'],
 'head_gloss':r['head_english'],'adopted_sense_constraint':note,
 'decision':status,'change_to_spelling':'none','evidence':'editorial semantic ruling on existing component senses; not speaker attestation'})
for r in rejected:
 lexical_decisions.append({'decision_id':f'L8-{len(lexical_decisions)+1:03d}','canonical_id':r['canonical_id'],
  'canonical_word':r['canonical_word'],'canonical_english':r['canonical_english'],
  'modifier':r['modifier'],'modifier_gloss':r['modifier_meaning'],'head':r['head'],'head_gloss':r['head_meaning'],
  'adopted_sense_constraint':r['editorial_note'],
  'decision':'retain canonical word; specifically reject '+r['candidate_form'],'change_to_spelling':'none',
  'evidence':'prior individually reviewed v16.2 rejection, preserved in 8.0'})
csvout(OUT/'lexical_decisions.csv',lexical_decisions)

# C2. Every structurally flagged compound is assigned a review queue decision
# and a clear reason, but NOT silently counted as individually adjudicated.
with gzip.open(ROOT/'data/v28_34/canonical_compound_audit_13379.csv.gz','rt',encoding='utf8') as f:
 allcomp=list(csv.DictReader(f))
priority={r['lemma']:int(r['priority_rank']) for r in lex800}
flagged=[x for x in allcomp if x['component_polysemy_gloss_flag']=='True' or x['grapheme_merge_risk']]
flagged.sort(key=lambda r:(0 if r['compound'] in COMPOUND_DECISIONS else 1,priority.get(r['compound'],999999),r['compound']))
queue=[]
for r in flagged:
 queue.append({'canonical_id':r['dictionary_id'],'word':r['compound'],'meaning':r['canonical_gloss'],'modifier':r['modifier'],
 'modifier_meanings':r['modifier_gloss'],'head':r['head'],'head_meanings':r['head_gloss'],
 'risk':'digraph+'+str(r['grapheme_merge_risk']) if r['grapheme_merge_risk'] else 'multi-sense English component gloss',
 'priority_rank':priority.get(r['compound'],'not in top 800'),
 'review_status':'adopted_narrow_sense' if r['compound'] in COMPOUND_DECISIONS else 'not independently adjudicated',
 'action':'use current dictionary meaning pending targeted semantic judgment' if r['compound'] not in COMPOUND_DECISIONS else 'apply Standard 8 lexical sense constraint',
 'preserve_spelling':'yes'})
csvout(OUT/'compound_risk_register.csv',queue)

# A2. One semantically enriched current dictionary: learner sees normative sense
# rules, source examples, verb status and compound cautions in the SAME entry.
# No source gloss is edited; additional fields are edition metadata.
sense_by_word=collections.defaultdict(list)
for x in senses:sense_by_word[x['lemma']].append(x['sense']+': '+x['definition'])
boundary_by_word=collections.defaultdict(list)
for x in meaning:
 for lemma,contrast in ((x['left'],x['right']),(x['right'],x['left'])):
  boundary_by_word[lemma].append('distinguish from '+contrast+': '+x['semantic_boundary'])
narrow={x['canonical_word']:x['adopted_sense_constraint'] for x in lexical_decisions if not x['decision'].startswith('retain canonical')}
flags={x['word']:x['review_status'] for x in queue}
lexindex={x['lemma']:x for x in lex800};verbindex={x['lemma']:x for x in validated}
enriched=[]
for x in current:
 word=x['qaroshi'];z=dict(x)
 z['edition']='8.0';z['current_lexical_status']='adopted overlay word' if word==addition['qaroshi'] else 'preserved canonical word'
 z['individually_reviewed_senses']=' | '.join(sense_by_word.get(word,[]))
 z['current_lexical_sense_constraint']=narrow.get(word,'')
 z['semantic_boundary_notes']=' | '.join(boundary_by_word.get(word,[]))
 z['controlled_example_ids']=lexindex.get(word,{}).get('source_reference_ids','')
 z['verb_role_license']=verbindex.get(word,{}).get('decision','')
 z['compound_ambiguity_status']=flags.get(word,'')
 z['source_claim']='Existing reference or adopted editorial amendment; no independent speaker attestation'
 enriched.append(z)
buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(enriched[0]),lineterminator='\n');w.writeheader();w.writerows(enriched)
(OUT/'dictionary_enriched_30001.csv.gz').write_bytes(gzip.compress(buf.getvalue().encode('utf8'),compresslevel=9,mtime=0))

# D. Compositional two-quantifier formal scope (new adopted rule) + checkable
# truth tables: surface order determines scope, case determines roles.
examples=[];counter=0
for first,second in itertools.product(('ngënao','shërano','nëgëra'),repeat=2):
 if first==second=='nëgëra':continue
 for roles in ('SO','OS'):
  tokens=[first,'qaro'+('-m' if roles[0]=='O' else ''),second,'mara'+('-m' if roles[1]=='O' else '')]
  if roles=='OS':tokens=[first,'mara-m',second,'qaro']
  for neg in (False,True):
   if neg and 'nëgëra' in (first,second):continue
   sentence='sen '+' '.join(tokens)+(' nu' if neg else '')+' tika.'
   res=analyze(sentence)
   if not res['supported']:raise AssertionError((sentence,res))
   counter+=1
   examples.append({'id':f'Q8S-{counter:03d}','qaroshi':sentence,'logical_form':res['logical_form'],
    'surface_roles':'+'.join(res['roles']),'source':'original Standard 8 norm-setting editorial example, not prior corpus',
    'constraint':'wide scope is the leftmost quantifier; no scope crossing outside this simple independent clause'})
jsonout(OUT/'complex_scope_examples.json',examples)
# Test relation truth-values across all 2x2 matrices to expose genuine ambiguity
truth=[]
for bits in itertools.product((False,True),repeat=4):
 matrix=[list(bits[:2]),list(bits[2:])]
 values={}
 for q1,q2 in itertools.product(('ngënao','shërano','nëgëra'),repeat=2):
  if q1==q2=='nëgëra':continue
  for direct in ('yes','no'):
   try:values[f'{q1}|{q2}|{direct}']=evaluate(f'{q1}|{q2}|{direct}|no',matrix)
   except Exception:raise
 truth.append({'relation_bits':''.join(str(int(b)) for b in bits),'results':values})
jsonout(OUT/'formal_scope_truth_models.json',truth)

# E. Answer key is a distinct file, making actual blind review possible.
# Correct English is sourced from corpus for the valency tasks, while the
# quantitatively novel constructions explicitly remain editorial exercises.
tasks=[];answers=[]
def task(kind,q,ans,foil_a,foil_b,provenance,source_id=''):
 idx=len(tasks)+1;key=f'C8-{idx:04d}'
 # Rotate correct slot deterministically so identical ordering is not learned.
 choices=[ans,foil_a,foil_b];spin=(idx*7)%3;choices=choices[spin:]+choices[:spin]
 answer='ABC'[choices.index(ans)]
 tasks.append({'id':key,'category':kind,'qaroshi':q,'option_A':choices[0],'option_B':choices[1],'option_C':choices[2],
  'source_id':source_id,'provenance':provenance,'independent_testing_status':'not administered'})
 answers.append({'id':key,'correct':answer,'expected_interpretation':ans,'source_id':source_id})
for r in validated[:200]:
 if not r['example_source_id']:continue
 right=r['example_english'];q=r['example_qaroshi']
 task('verb_argument',q,right,'A different person performs the action.','No action takes place.', 'exact controlled source bilingual reference',r['example_source_id'])
for r in examples[:40]:
 q=r['qaroshi'];right=r['logical_form'];task('quantifier_scope',q,right,'All participants perform the predicate.','No participants perform the predicate.','editorial new rule test; formal semantic interpretation')
for r in lexical_decisions[:45]:
 task('lexical_sense',r['canonical_word'],r['canonical_english'],r['modifier_gloss']+' + '+r['head_gloss']+' (all senses asserted)',
  'The expression has no established dictionary meaning.','canonical noun headword vs misleading English component homonym',r['canonical_id'])
assert len(tasks)>=220
csvout(OUT/'blind_comprehension_prompts.csv',tasks);csvout(OUT/'sealed_answer_key.csv',answers)

# A. Consolidated true current reference. 90 historical chapters are present,
# with superseding normative notes integrated at relevant locations, and one
# current editioned dictionary. Never edit the hash-locked old grammar.
old=(ROOT/'docs/grammar.md').read_text(encoding='utf8')
assert sum(1 for x in re.finditer(r'^## \d+\.',old,re.M))==90
notes={
7:"**Standard 8.0 override (adopted):** In finite passive clauses `-za` explicitly marks the demoted actor; `-shi` marks the instrument/means. Legacy passive-actor `-shi` is understood in archived sources but not recommended for new exact writing. A nominal receives at most one case. An active finite verb cannot license an actor in `-za`. See the reviewed voice conditions in Chapter 74.",
22:"**Standard 8.0 override (adopted):** `nëgëra` is the editioned quantifier *not every / not all*; it precedes its quantified NP and has the counterexample truth condition ∃x∈D ¬P(x), with D nonempty. It does not entail that any x satisfies P. Two explicitly quantified nominal phrases in a simple unembedded SOV clause take **linear surface scope** (leftmost quantified NP widest), while `-m` still marks semantic object independently of position. In plain discourse without overt quantifiers this rule makes no scope claims.",
24:"**Standard 8.0 clarification:** Wh-question particles and quantified phrases retain their own positions. A direct question with final `he` is not licensed by the simple declarative two-quantifier interpreter; do not use a declarative parse for an answer-seeking question.",
28:"**Standard 8.0 clarification:** For an overt passive agent choose `-za`; reserve `-shi` for instrument. Source-cited examples have only their recorded object class licensed, unless a manually reviewed verb sense authorizes broader arguments.",
30:"**Standard 8.0 disambiguation:** Morphological segmentation is done against the current 30,001-word editioned lexicon, which is a frozen 30,000-entry baseline plus `nëgëra` (Q8D001). Hyphens retain their existing case and verb meaning. Historical roots are not silently recomputed from English glosses.",
71:"**Standard 8.0 scope:** A two-quantifier construction has exactly two overt quantified noun phrases (one subject, one `-m` object) and a simple final lexical verb. The leftmost quantified phrase binds wider; case-marked object topicalization therefore changes the *formal scope order*, never the argument role. A sentence with embeddings or ordinary discourse topics requires an independent clause analysis and is not automatically interpretable by the simple-scope checker.",
74:"**Standard 8.0 licensing:** The current valency inventory is `data/standard_8/verb_audit_400.csv`. Twenty-five inherited frames have general reviewed licenses. Other entries have individually documented *examples*, not blanket morphological/passive/causative licenses. Do not infer any new passive or object class from an editorial parallel example; adopt a full frame only through a recorded selectional review.",
76:"**Standard 8.0 negation scope:** Ordinary predicate `nu` is immediately preverbal. For two overt quantified noun phrases the surface-first quantifier has widest scope; predicate `nu` scopes inside both. `nëgëra` already negates universal force and is not combinable with predicate `nu` in the restricted two-quantifier construction. In other constructions state scope by overt individual clauses and report unresolved ambiguity.",
78:"**Standard 8.0 quantifiers:** The adopted `nëgëra` is distinct from both `ngënao NP nu P` (*none*) and `shërano NP P` (*some*). In a two-quantifier simple clause, bind leftmost NP outside the rightmost. Example: `sen shërano qaro ngënao mara-m tika.` is ∃qaro ∀mara see(qaro,mara); `sen ngënao mara-m shërano qaro tika.` is ∀mara ∃qaro see(qaro,mara). These differ. The examples are normative editorial constructions, not independent recorded speech.",
79:"**Standard 8.0 valency restriction:** Voice and modality retain original slot order. A source-licensed object case for a verb does not automatically license that verb's `-li` passive or `-ru` causative; those require a reviewed argument structure.",
83:"**Standard 8.0 conversation:** Full independent written sentences retain one opening resonance. Single-word replies and bare labels may be fragments. Omitted participants are only safe with one recoverable referent, not when consent, identity or actor responsibility is disputed.",
86:"**Standard 8.0 pronunciation:** Existing native digraphs `sh`, `zh`, `kh`, `ng` remain distinct graphemes. Proposed or recorded compounds are not respelled due to an English gloss. Spoken connected-speech simplification does not create an alternate written word.",
88:"**Standard 8.0 word senses:** Words with overlapping English definitions are not automatically Qaroshi synonyms. The current sense constraints in `data/standard_8/lexical_decisions.csv` and `data/semantics/curated_senses.json` control their explicitly reviewed meanings. Unreviewed compounds keep documented lexical glosses, with compositional interpretations labeled provisional.",
89:"**Standard 8.0 idioms:** Existing literary figures remain editorial conventions, not universally traditional idioms. Irony must have a recoverable contextual frame and cannot be inferred from resonance alone. Literal high-stakes use takes precedence unless figurative scope is marked.",
}
currentgrammar=old.replace('Unified Standard Reference 4.2','**Current unified normative grammar: Standard 8.0 (2026)**',1).replace('**70 integrated chapters · 26 native letters · 16 mandatory written resonance markers**','**90 consolidated chapters · 26 native letters · 16 mandatory written resonance markers · 30,001 editioned lexemes**',1)
# Resolve older prose that became contradictory after adopted amendments.
# These substitutions apply ONLY to generated Standard 8, never the frozen source.
currentgrammar=currentgrammar.replace(
 "| `-shi` | instrumental | using / by means of | `banu-shi`, using wings |",
 "| `-shi` | instrumental | using / by means of | `banu-shi`, using wings |\n| `-za` | passive agent | by an explicit actor (requires passive `-li`) | `mara-za`, by a friend |",1)
currentgrammar=currentgrammar.replace(
 "If you need to identify the agent of a passive, use `-shi`: `sen naro mara-shi daru-li-te.` = The home was protected by a friend. In speech this instrumental agent use is permitted, but `-shi` also means a physical instrument, so context matters.",
 "In current Standard 8.0, identify the agent of a passive with `-za`: `sen naro mara-za daru-li-te.` = The home was protected by a friend. Older writing may use agentive `-shi` for this role, but that ambiguous reading is legacy-only for new precise usage, where `-shi` marks the physical instrument.",1)
currentgrammar=currentgrammar.replace(
 "The instrumental `-shi` can also identify a passive agent in established usage; in potentially confusing sentences, avoid a passive or add more descriptive information about agency.",
 "Historical texts also used `-shi` for a passive agent, but current precision writing uses `-za` for the actor and reserves `-shi` for the instrument.",1)
currentgrammar=currentgrammar.replace(
 "To negate the universality itself, use an explicit exception (`zërë` + excluded phrase), a contextual quantity phrase, or a contrasting sentence.",
 "To negate universality itself, use current `nëgëra` immediately before the quantified NP; exceptions with `zërë` and contextual quantity phrases remain useful when the domain is disputed.",1)
# Preserve all chapters while adding current rulings directly after corresponding
# chapter headings (rather than scattering amendments across several PDFs).
for n,textnote in notes.items():
 pattern=re.compile(r'^(## '+str(n)+r'\.[^\n]+\n)',re.M)
 assert len(pattern.findall(currentgrammar))==1,n
 currentgrammar=pattern.sub(lambda m:m.group(1)+'\n'+textnote+'\n',currentgrammar,count=1)
front='''# Qaroshi Unified Standard 8.0 · Authoritative Current Grammar

**Language-standard release:** 8.0. This consolidated teaching and normative edition includes the full 90 historical grammar chapters with directly integrated current rulings and a compatible post-7.0 lexical overlay. Its older source is frozen at `docs/grammar.md` for historical reproducibility. The current dictionary is `data/standard_8/dictionary_enriched_30001.csv.gz`; a base-schema compatibility export is `data/standard_8/dictionary_30001.csv.gz`.

**Precedence:** Standard 8.0 chapter rulings govern new use; for unaffected constructions the 7.0 chapter text remains in force. 24–27 supplied explicit passive agency `-za`; 28–34 supplied `nëgëra` and scope distinctions. Legacy documents remain interpretable in their contemporary editions. No new speaker dialect or real-world attestation is claimed.

**What this edition does not claim:** 400 complete generalized verb paradigms, all 3,108 ambiguous compounds individually resolved, native speaker pronunciation evidence, or completed independent comprehension experiments. Every verb and compound entry has a recorded status; do not promote provisional evidence to canonical grammar by inference.

**Jump to the chapters:** [Case/voice](#7-voice-and-valency) · [Quantification](#22-quantifiers-distributivity-and-scope) · [Argument frames](#74-verb-frames-and-participant-roles) · [Negation](#76-negation-and-focus-scope) · [Connected speech](#86-connected-speech-and-phrasal-stress) · [Polysemy](#88-polysemy-senses-and-valency).

---

'''
# Avoid a nested duplicate H1 and add a new reference title without altering history.
currentgrammar=re.sub(r'^# Qaroshi — Complete Grammar\n','## Historical 7.0 grammar, consolidated with later amendments\n',currentgrammar,count=1)
(DOC/'grammar.md').write_text(front+currentgrammar,encoding='utf8')

manifest={'release':'Qaroshi Unified Standard 8.0','policy':'current normative consolidated reference; historic standard 7.0 remains immutable',
 'historic_dictionary':30000,'new_edition_headwords':1,'current_dictionary':len(current),'historic_examples':4383,
 'chapters':90,'current_chapter_rulings':len(notes),'checked_verb_entries':len(validated),'verb_decisions':dict(counts),
 'lexical_narrow_sense_decisions':len(COMPOUND_DECISIONS),'prior_false_friend_rejections':len(rejected),
 'compound_risk_rows':len(queue),'new_two_quantifier_examples':len(examples),
 'truth_model_cases':len(truth),'blind_trial_items':len(tasks),'baseline_hashes_verified':len(basehash),
 'independent_human_test_responses':0,'canonical_spellings_overwritten':0,
 'data_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted([*OUT.glob('*'),DOC/'grammar.md']) if p.name!='release_manifest.json'}}
jsonout(OUT/'release_manifest.json',manifest)
print(json.dumps({k:v for k,v in manifest.items() if not isinstance(v,dict)},indent=2))
