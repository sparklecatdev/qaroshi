#!/usr/bin/env python3
"""Build offline, source-transparent v21/22/23 Translation, Reader, Practice.

Does not revise canonical Qaroshi, ratify editorial claims, or simulate real
learner outcomes. Source/reference alignments are preserved byte for byte.
"""
from __future__ import annotations
import collections, csv, hashlib, json, random, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D21=ROOT/'data/v21';D22=ROOT/'data/v22';D23=ROOT/'data/v23'
for d in [D21,D22,D23]:d.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools/v21_23'))
from translator import records, norm, interpret

def readcsv(rel):
    with (ROOT/rel).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def emit(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def emitcsv(path,rows):
    if not rows:raise ValueError('empty csv')
    with path.open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

lex=readcsv('data/lexicon.csv');assert len(lex)==30000
lexmap={r['qaroshi']:r for r in lex}
parallel=readcsv('corpus/parallel_sentences.csv');assert len(parallel)==4383
source_rows=records();source_q=collections.defaultdict(list);source_e=collections.defaultdict(list)
for r in source_rows:source_q[norm(r['qaroshi'])].append(r);source_e[norm(r['english'])].append(r)
core=set(x['root'] for x in readcsv('data/v17/core_learning_120.csv'))
qa=readcsv('data/v14/translation_review_103.csv')
assert len(qa)==103
qa_by_q=collections.defaultdict(list)
for row in qa:qa_by_q[norm(row['qaroshi'])].append(row)

# No fabricated corpus. Three separate previously authored editorial sources.
readings=[]
for x in json.loads((ROOT/'corpus/v15/pieces.json').read_text(encoding='utf8')):
    readings.append({'id':x['id'],'title':x['title'],'genre':x['genre'],'premise':x['premise'],'kind':x['kind'],
        'provenance':'v15 independently drafted editorial writing, not speaker-attested or human-adjudicated',
        'source_path':'corpus/v15/pieces.json','lines':[{'id':l['id'],'speaker':l['speaker'],
        'qaroshi':l['qaroshi'],'english':l['english_contextual'],'ipa':l['ipa'],'sound_out':l['sound_out'],
        'review_status':l.get('review_state','editorial draft')} for l in x['lines']]})
for i,x in enumerate(json.loads((ROOT/'corpus/v12_13/anthology_12.json').read_text(encoding='utf8')),1):
    readings.append({'id':f'earlier-12-{i:02}','title':x['title'],'genre':x['genre'],'premise':x['premise'],'kind':'literature',
        'provenance':'earlier editorial anthology, not speaker-attested, contextual English is not always literal',
        'source_path':'corpus/v12_13/anthology_12.json','lines':[{'id':f'earlier-12-{i:02}-{j:02}',
        'speaker':'NARRATOR','qaroshi':l['qaroshi'],'english':l['english_editorial'],'ipa':l['ipa'],
        'sound_out':l['sound_out'],'literal':l.get('literal_engine_translation'),
        'review_status':l.get('review_status','editorial')} for j,l in enumerate(x['sentences'],1)]})
for x in json.loads((ROOT/'corpus/curated/short_readings.json').read_text(encoding='utf8')):
    readings.append({'id':x['id'],'title':x['title'],'genre':'curated short reading','premise':x['premise'],'kind':'literature',
        'provenance':'earlier structurally checked editorial short reading, not speaker-attested',
        'source_path':'corpus/curated/short_readings.json','lines':[{'id':f"{x['id']}-{l['number']}",
        'speaker':'NARRATOR','qaroshi':l['qaroshi'],'english':l['english'],'ipa':l['ipa'],
        'sound_out':l['sound_out'],'review_status':l.get('status','editorial')} for l in x['sentences']]})
assert len(readings)==108,len(readings)
assert len({r['id'] for r in readings})==len(readings)

# Learning stages are relative editorial difficulty proxies, NOT certified CEFR.
sys.path.insert(0,str(ROOT/'tools/fluency11'))
from engine import words, word_analysis, RESONANCES, FUNCTIONS, CONNECTORS
for reading in readings:
    sentences=reading['lines'];count=sum(len(words(x['qaroshi'])) for x in sentences)
    roots=[];unknown=set()
    for line in sentences:
        for w in words(line['qaroshi']):
            if w in RESONANCES or w in FUNCTIONS or w in CONNECTORS:continue
            a=word_analysis(w)
            if a.get('known'):roots.append(a['root'])
            else:unknown.add(w)
    unique=set(roots);familiar=unique.intersection(core)
    # Relative graded reading; no claims about human reading time.
    difficulty=round(min(1,(len(unique)-len(familiar))/max(1,len(unique))*.65 + (count/len(sentences))/20*.35),4)
    band='foundation' if difficulty<.16 else 'developing' if difficulty<.255 else 'stretch'
    flags=[r['audit_id'] for x in sentences for r in qa_by_q.get(norm(x['qaroshi']),[])]
    reading.update({'line_count':len(sentences),'qaroshi_tokens':count,'unique_known_roots':len(unique),
        'core_120_roots':len(familiar),'unknown_reference_forms':sorted(unknown),
        'difficulty_proxy':difficulty,'reading_band':band,
        'editorial_translation_flags':sorted(set(flags))})
    assert all(x['qaroshi'] and x['english'] for x in sentences)

# Stable 3-task exercise bank per piece. This checks matching a line to the
# documented contextual rendering, NOT independently comprehending a plot.
quizzes=[]
for reader in readings:
    lines=reader['lines'];rng=random.Random(int(hashlib.sha256(reader['id'].encode()).hexdigest()[:12],16))
    eligible=[i for i,x in enumerate(lines) if len({t['english'] for t in lines})>=4]
    if not eligible:continue
    chosen=sorted(set([0,len(lines)//2,len(lines)-1]))[:3]
    if len(chosen)<3:chosen=(list(range(min(3,len(lines)))))
    for j,idx in enumerate(chosen):
        target=lines[idx]
        pool=list(dict.fromkeys(x['english'] for i,x in enumerate(lines) if i!=idx and x['english']!=target['english']))
        if len(pool)<3:continue
        distractors=rng.sample(pool,3)
        choices=[target['english'],*distractors];rng.shuffle(choices)
        quizzes.append({'id':f"{reader['id']}-Q{j+1}",'reading_id':reader['id'],'line_id':target['id'],
           'skill':'source-aligned sentence recognition','prompt':'Which source-context English rendering belongs to this Qaroshi line?',
           'qaroshi':target['qaroshi'],'options':choices,'answer_index':choices.index(target['english']),
           'context_sentence_number':idx+1,'explanation':'Matched to the original editorial translation of this exact line; additional context could change a standalone rendering.',
           'not_external_validity':'Internal editorial recall quiz, not verified independent comprehension'})
assert len(quizzes)>=300,len(quizzes)

# A ledger of 103 unadjudicated old translation discrepancies; no false fixes.
review_ledger=[]
for row in qa:
    review_ledger.append({'id':row['audit_id'],'qaroshi':row['qaroshi'],'source_contextual_english':row['english_contextual'],
      'suggested_standalone_english_unapproved':row['proposed_standalone_english'],
      'interpretation_category':row['interpretation_category'],'reason':row['editorial_reason'],
      'human_approved':row['human_semantic_approved'],'decision':row['editorial_decision'],
      'instruction':'Compare what is overtly encoded with what English adds; do not automatically ratify the suggested correction.'})

# Controlled audit showing where source text resolves and engine declines.
audit=[]
for p in parallel:
    result=interpret(p['qaroshi'],'to-en')
    assert result['translation'] is not None and result['variants']
    audit.append({'id':p['id'],'status':result['status'],'alternatives':len(result['variants']),
        'qa_notes':len(result['review_flags'])})

emit(D21/'translation_reference_index.json',source_rows)
emit(D21/'editorial_discrepancy_ledger_103.json',review_ledger)
emit(D21/'reference_translation_audit.json',audit)
emit(D22/'graded_editorial_readers_108.json',readings)
emit(D23/'source_matching_quizzes.json',quizzes)

training_modules=[
 {'id':'T01','title':'Find an exact documented expression','concept':'Exact lookup versus a related example','practice':'Search for hë ti haro he? and compare the source ID.'},
 {'id':'T02','title':'Permission is not ability','concept':'-ho vs -ki','practice':'Compare documented examples for can and may.'},
 {'id':'T03','title':'Consent is explicit','concept':'Explicit refusal, not warm resonance','practice':'Compare consent question, affirmative, and refusal.'},
 {'id':'T04','title':'Who witnessed it?','concept':'si, hu, ye','practice':'Check evidence particles and never promote a rumor to observation.'},
 {'id':'T05','title':'What was actually said?','concept':'Contextual English paraphrase versus overt Qaroshi','practice':'Inspect one of the 103 flagged review cases.'},
 {'id':'T06','title':'Read a short story','concept':'Source-aligned translation reveals','practice':'Read the first foundation-level literature piece without English, then reveal.'},
 {'id':'T07','title':'Resolve unfamiliar words','concept':'Root, inflection and dictionary sense','practice':'Click words in the reader; compare them with documented components.'},
 {'id':'T08','title':'Watch your translation uncertainty','concept':'Abstain on unsupported structures','practice':'Try a complex English question: the offline tool must not hallucinate a translation.'},
 {'id':'T09','title':'Follow a narrative','concept':'The next line changes reference and assumptions','practice':'Read a dialogue and check changes of subject and evidence.'},
 {'id':'T10','title':'Build reading speed','concept':'Recognize recurring canonical roots','practice':'Use the study set from a story and reveal only unknown words.'},
 {'id':'T11','title':'Practice contextual English','concept':'Source-matching, not independent translation certification','practice':'Finish three source-line recognition questions for a story.'},
 {'id':'T12','title':'Audit your own progress','concept':'Evidence and self-assessment limits','practice':'Export your score sheet and identify which skills were actually tested.'},
]
emit(D23/'twelve_lesson_learning_path.json',training_modules)

manifest={'name':'Qaroshi 21.0 + 22.0 + 23.0 Translation, Immersion and Learner Lab',
 'release_date':'2026-11-15','canonical_words':30000,'canonical_bilingual_reference_pairs':4383,
 'v15_editorial_lines':sum(len(x['lines']) for x in readings if x['source_path']=='corpus/v15/pieces.json'),
 'source_records_indexed':len(source_rows),'editorial_readings':len(readings),
 'reading_lines':sum(len(x['lines']) for x in readings),
 'reading_bands':dict(collections.Counter(x['reading_band'] for x in readings)),
 'source_matching_questions':len(quizzes),'course_units':len(training_modules),
 'preexisting_translation_review_cases':len(qa),
 'new_canonical_words':0,'new_spontaneous_speaker_attestations':0,'verified_independent_learner_scores':0,
 'source_policy':'Controlled corpus + archived editorial narrative; no invented speaker data, no unapproved meaning replacement',
 'translation_policy':'Exact references take priority. Unsupported input abstains. Rule-engine generation is provisional via Python CLI.',
 'assessment_policy':'Quizzes score source translation recognition, not full comprehension, general proficiency, or independent translation ability'}
emit(ROOT/'data/v21_23_release_manifest.json',manifest)

# Curated dictionary payload; all known glosses remain canonical and the UI
# uses word links and case/tense explanation, but offers no invented definitions.
web_lex=[{'w':r['qaroshi'],'g':r['english'],'pos':r['pos'],'ipa':r['ipa'],'type':r['type'],'components':r['components']} for r in lex]
web_rows=[{'id':r['id'],'q':r['qaroshi'],'e':r['english'],'kind':r['kind'],'source':r['source'],'ipa':r['ipa'],'sound':r['sound_out']} for r in source_rows]
web_qa=[{'q':r['qaroshi'],'id':r['id'],'reason':r['reason'],'category':r['interpretation_category'], 'source_english':r['source_contextual_english'], 'proposed_english':r['suggested_standalone_english_unapproved']} for r in review_ledger]
payload={'lex':web_lex,'refs':web_rows,'readings':readings,'quizzes':quizzes,
 'review':web_qa,'course':training_modules,'manifest':manifest,
 'resonances':json.loads((ROOT/'data/resonances.json').read_text(encoding='utf8'))}
T=(ROOT/'tools/v21_23/app_template.html').read_text(encoding='utf8')
assert T.count('__QAROSHI_21_23_DATA__')==1
blob=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
out=ROOT/'Qaroshi_21_23_Translation_Immersion_Academy.html'
out.write_text(T.replace('__QAROSHI_21_23_DATA__',blob),encoding='utf8')
manifest['standalone_html_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
manifest['standalone_html_bytes']=out.stat().st_size
emit(ROOT/'data/v21_23_release_manifest.json',manifest)
print(json.dumps({'manifest':manifest,'html_bytes':out.stat().st_size},ensure_ascii=False,indent=2))
