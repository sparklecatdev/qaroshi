#!/usr/bin/env python3
"""Build Qaroshi 20.0 Spoken Language Practice Kit from versioned canonical sources.

This creates RECORDING PROMPTS, not speaker audio or attested dialects. Audio
recording is private and entirely user initiated in the standalone web app.
"""
from __future__ import annotations
import csv,json,hashlib,collections,sys,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/v20';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools'))
from phonetics import graphemes,syllabify,guide_word,ipa_word,sound_out_word,IPA,VOWELS

def readcsv(path):
 with (ROOT/path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def savecsv(name,items):
 assert items
 with (OUT/name).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
def savejson(name,items):
 (OUT/name).write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def slug(s):return re.sub(r'[^a-z0-9-]+','-',s.lower()).strip('-')

lex=readcsv('data/lexicon.csv');byword={r['qaroshi']:r for r in lex};phrases=readcsv('data/v17/everyday_phrases.csv');resonance=json.loads((ROOT/'data/resonances.json').read_text(encoding='utf8'))
phonemes=json.loads((ROOT/'data/phoneme_inventory.json').read_text(encoding='utf8'))
existing_drills=json.loads((ROOT/'data/phonology/drills.json').read_text(encoding='utf8'))
rootcurriculum=readcsv('data/v19/productive_root_curriculum.csv')
assert len(lex)==30000 and len(phrases)==656 and len(phonemes)==26 and len(resonance)==16
assert len({r['glyph'] for r in phonemes})==26
assert len(rootcurriculum)>=1900

ART={
'a':('open central/front unrounded vowel','Keep the vowel pure; do not add an English glide.'),
'e':('mid-close front unrounded vowel','A pure /e/, not a diphthong or schwa.'),
'i':('close front unrounded vowel','Keep the tongue high at the front.'),
'o':('mid-close back rounded vowel','Keep /o/ steady, without adding /ʊ/.'),
'u':('close back rounded vowel','Lips rounded, tongue high and back.'),
'ë':('mid central schwa','The separate vowel /ə/ can carry lexical stress.'),
'k':('voiceless velar stop','Touch the rear tongue to the soft palate.'),
'q':('voiceless uvular stop','Place the closure farther back than /k/.'),
'kh':('voiceless velar fricative','Continuous breath friction like Scots loch, not /k/ + /h/.'),
'sh':('voiceless postalveolar fricative','One native letter; like English ship.'),
'zh':('voiced postalveolar fricative','One native letter; like the sound in measure.'),
'ng':('voiced velar nasal','One native letter, /ŋ/ without a following /g/.'),
'r':('alveolar tap','One brief tap /ɾ/, not an English r approximant.'),
'l':('alveolar lateral approximant','Air flows along the sides of the tongue.'),
'w':('voiced labial-velar approximant','Lip rounding plus a raised back tongue.'),
'y':('palatal approximant','Consonant /j/ as in yes.'),
'h':('voiceless glottal fricative','Gentle glottal breath; preserve when written.'),
'g':('voiced velar stop','Hard g /ɡ/ in all contexts.'),
'b':('voiced bilabial stop','Both lips close; then voice the release.'),
'p':('voiceless bilabial stop','Both lips close; release without voicing.'),
'd':('voiced alveolar stop','Tongue meets the ridge behind the teeth.'),
't':('voiceless alveolar stop','Tongue meets the ridge behind the teeth.'),
'm':('voiced bilabial nasal','Air escapes through the nose with lips together.'),
'n':('voiced alveolar nasal','Air escapes through the nose with tongue at alveolar ridge.'),
's':('voiceless alveolar fricative','Hissing friction nearer the teeth.'),
'z':('voiced alveolar fricative','Voiced partner of /s/.'),
}
assert set(ART)==set(r['glyph'] for r in phonemes)

# One short documented word example for each letter. Do not invent mock lexemes.
byletter=collections.defaultdict(list)
for x in existing_drills:
 if x['word'] in byword and x['letter'] in ART:byletter[x['letter']].append(x)
phoneme_cards=[]
for i,p in enumerate(phonemes,1):
 g=p['glyph'];opts=byletter.get(g,[])
 opts=sorted(opts,key=lambda r:(len(r['word']),r['word']))
 if not opts:
  opts=sorted(({'word':r['qaroshi'],'english':r['english'],'dict_id':r['id']} for r in lex if g in graphemes(r['qaroshi'])),key=lambda x:(len(x['word']),x['word']))
 x=opts[0];w=byword[x['word']]
 phoneme_cards.append({'number':i,'symbol':g,'ipa':p['ipa'],'class':'vowel' if p['is_vowel'] else 'consonant',
 'articulation':ART[g][0],'coaching':ART[g][1],'example_word':w['qaroshi'],'example_gloss':w['english'],
 'example_source_id':w['id'],'example_ipa':w['ipa'],'reading':w['reading'],'sound_out':w['sound_out'],
 'authority':'existing 26-symbol inventory and canonical lexicon; no independent audio recordings'})
savecsv('phoneme_reference_26.csv',phoneme_cards)

# Exactly one changed sound per pair. These are real canonical lexical items,
# NOT invented minimal pairs or fabricated natural conversation examples.
focus=[('q','k'),('sh','zh'),('ë','e'),('i','e'),('ng','n'),('r','l'),('o','u'),('g','k'),('s','sh'),('a','ë'),('p','b'),('t','d')]
word_by_g={tuple(graphemes(r['qaroshi'])):r for r in lex if r['type']=='headword' and r['pos'] in ('n','v','adj') and len(graphemes(r['qaroshi']))<=8 and len(r['english'])<=68}
pairs=[];seen_pairs=set()
for a,b in focus:
 candidates=[]
 for letters,source in word_by_g.items():
  for j,g in enumerate(letters):
   if g!=a:continue
   other=letters[:j]+(b,)+letters[j+1:]
   if other not in word_by_g:continue
   target=word_by_g[other];key=(source['qaroshi'],target['qaroshi'])
   if key in seen_pairs:continue
   candidates.append((len(source['qaroshi'])+len(target['qaroshi']),source,target,j))
 candidates.sort(key=lambda x:(x[0],x[1]['qaroshi'],x[2]['qaroshi']))
 for _,x,y,j in candidates[:12]:
  seen_pairs.add((x['qaroshi'],y['qaroshi']))
  pairs.append({'id':f'MP20-{len(pairs)+1:03d}','contrast':a+' / '+b,'word_a':x['qaroshi'],'english_a':x['english'],
   'ipa_a':x['ipa'],'source_a':x['id'],'word_b':y['qaroshi'],'english_b':y['english'],
   'ipa_b':y['ipa'],'source_b':y['id'],'changed_grapheme_index':j,
   'attestation':'both words in canonical lexicon; pairing is a teaching exercise, not recorded speech'})
assert len(pairs)>=75,len(pairs)
savecsv('lexical_sound_contrasts.csv',pairs)

# Exactly 3000 recording tasks. 656 source phrases, 2344 canonical WORDS.
# The word set favors previously prioritized core roots and recurrent compound
# stems. Every prompt has an immutable ID and the source spelling / IPA.
queue=[]
for i,p in enumerate(phrases,1):
 queue.append({'record_id':f'RC20-{i:04d}','kind':'documented_phrase','source_id':p['id'],
 'qaroshi':p['qaroshi'],'english':p['english'],'broad_ipa':p['ipa'],'sound_out':p['sound_out'],
 'domain':p['category'],'resonance':p['qaroshi'].split()[0], 'default_timing':'read carefully, respect the phrase boundary; no scripted pitch shape',
 'speaker_recorded':'no','speaker_validated':'no','audio_path':'','consent_status':'not_collected','qc_status':'not_started'})
seen=set();ranked=[]
for r in rootcurriculum:
 if r['root'] in byword and r['root'] not in seen:seen.add(r['root']);ranked.append(byword[r['root']])
for row in lex:
 if row['type']=='headword' and row['qaroshi'] not in seen and row['pos'] in ('n','v','adj','adv','interj'):
  seen.add(row['qaroshi']);ranked.append(row)
need=3000-len(queue)
assert len(ranked)>=need
for row in ranked[:need]:
 i=len(queue)+1
 queue.append({'record_id':f'RC20-{i:04d}','kind':'canonical_word','source_id':row['id'],
 'qaroshi':row['qaroshi'],'english':row['english'],'broad_ipa':row['ipa'],'sound_out':row['sound_out'],
 'domain':row['domain'],'resonance':'','default_timing':'say the citation form with penultimate stress if multisyllabic',
 'speaker_recorded':'no','speaker_validated':'no','audio_path':'','consent_status':'not_collected','qc_status':'not_started'})
assert len(queue)==3000 and len({r['source_id'] for r in queue})==3000
savecsv('recording_queue_3000.csv',queue)

# 120 stress examples across 1-5 syllables from actual current dictionary.
syllable_examples=collections.defaultdict(list)
for r in ranked:
 count=len(syllabify(r['qaroshi']))
 if 2<=count<=5 and len(r['english'])<=70 and len(syllable_examples[count])<32:
  syllable_examples[count].append(r)
stress=[]
for size,rows in sorted(syllable_examples.items()):
 for row in rows[:30]:
  s=syllabify(row['qaroshi']);stress.append({'id':f'ST20-{len(stress)+1:03d}','source_id':row['id'],'qaroshi':row['qaroshi'],
   'english':row['english'],'ipa':row['ipa'],'syllables':len(s),'stress_index_zero_based':len(s)-2,
   'syllable_guide':guide_word(row['qaroshi']),'sound_out':row['sound_out'],
   'teaching_note':'Citation stress is penultimate; suffixes count toward syllables, not separate pauses.'})
assert len(stress)>=100
savecsv('citation_stress_drills.csv',stress)

# A grounded display of the sixteen written registers in connected speech.
# Some have only one source phrase and we show that honestly.
source_sentences=readcsv('corpus/parallel_sentences.csv')
byres=collections.defaultdict(list)
for x in source_sentences:
 marker=x['qaroshi'].split()[0]
 if marker in {r['marker'] for r in resonance}:byres[marker].append(x)
res_cues=[]
for m in resonance:
 for p in byres[m['marker']][:min(8,len(byres[m['marker']]))]:
  res_cues.append({'id':f'PR20-{len(res_cues)+1:03d}','register':m['marker'],'register_name':m['name'],'register_meaning':m['meaning'],
   'reference_id':p['id'],'qaroshi':p['qaroshi'],'english':p['english'],'ipa':p['ipa'],'sound_out':p['sound_out'],
   'instruction':'Say the resonance marker as an ordinary pronounced word. Convey its documented pragmatic stance without inventing a mandated pitch curve.',
   'evidence':'editorial reference example; pitch/acoustics have not been measured'})
assert {x['register'] for x in res_cues}=={x['marker'] for x in resonance}
savecsv('resonance_delivery_prompts.csv',res_cues)

# Connected-speech boundaries are guidance rather than unobserved acoustic facts.
connected=[]
for p in phrases:
 if 3<=len(p['qaroshi'].split())<=11 and len(connected)<140:
  toks=p['qaroshi'].split()
  connected.append({'id':f'CS20-{len(connected)+1:03d}','source_id':p['id'],'qaroshi':p['qaroshi'],'english':p['english'],
    'broad_ipa':p['ipa'],'reading':p['reading'],'word_count':len(toks),'opening_resonance':toks[0],
    'task':'Keep lexical segments distinct, use natural breath groups at punctuation; do not pause mechanically at learner morpheme hyphens.',
    'source_status':'controlled teaching sentence; no verified connected-speech recording'})
savecsv('connected_speech_140.csv',connected)

# 14-day training plan uses unique reference IDs and references actual drill entries.
syllids=[x['id'] for x in stress];pairids=[x['id'] for x in pairs];phraseids=[x['record_id'] for x in queue[:656]]
program=[]
for day in range(1,15):
 program.append({'day':day,'name':(['Vowel contrast','Back consonants','Digraphs','Syllabification','Stress and ë','Vowel stability',
 'Case and suffixes','Requests and consent','Questions and answers','Resonance delivery','Connected speech','Self-recording','Repair and clarity','Full interaction rehearsal'][day-1]),
 'phoneme_focus':[(x['symbol']) for x in phoneme_cards[(day-1)*2:(day-1)*2+2]],
 'stress_drills':syllids[(day-1)*8:day*8],'sound_contrasts':pairids[((day-1)*6)%len(pairids):((day-1)*6)%len(pairids)+6],
 'record_prompts':phraseids[(day-1)*10:day*10],
 'done_criterion':'Read and self-record selected examples, reflect on stress and segment accuracy; no automatic proficiency credential.'})
savejson('14_day_speech_course.json',program)

# A QA profile for audio metadata, not a claim of scoring the speaker's language.
qc={
 'version':'20.0','recording_status':'empty until a human explicitly records and consents',
 'recommended_format':['audio/webm;codecs=opus','audio/ogg;codecs=opus','audio/mp4'],
 'min_duration_seconds':0.2,'max_duration_seconds':120.0,'max_peak_dbfs':-0.2,'quiet_peak_dbfs':-50.0,
 'silent_rms_dbfs':-43.0,'human_review_fields':['actual_word_matches_prompt','segmental_clarity','word_stress','intonation_appropriateness','background_noise','permission_to_share'],
 'explicit_consent_required':True,'default_storage':'local browser memory; download-only export; no remote upload',
 'dialects':'unverified until independent recordings and observed linguistic differences exist',
 'voice_models':'none; the studio contains no native TTS or invented reference audio'}
savejson('audio_review_policy.json',qc)

manifest={'release':'Qaroshi 20.0 Spoken Language & Pronunciation','status':'completed offline learner tools; no speaker corpus asserted',
 'recording_prompts':len(queue),'documented_phrase_prompts':len(phrases),'canonical_word_prompts':need,
 'phoneme_cards':len(phoneme_cards),'real_lexical_sound_pairs':len(pairs),'stress_drills':len(stress),
 'resonance_prompts':len(res_cues),'connected_speech_drills':len(connected),'course_days':len(program),
 'canon_lexicon_count':len(lex),'existing_reference_sentences':len(source_sentences),
 'canonical_changed':False,'actual_audio_recordings_included':0,'speakers_approved':0,
 'phoneme_inventory_signature':hashlib.sha256((ROOT/'data/phoneme_inventory.json').read_bytes()).hexdigest(),
 'canonical_lexicon_sha256':hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest(),
 'longstanding_conventions':'26 symbols, penultimate stress, six vowel qualities, four native digraph letters; citation IPA not narrow phonetic acoustics'}
savejson('release_manifest.json',manifest)

# Compact app payload. The full 3k queue and all 26 grapheme samples remain embedded
# so the offline application works directly without a server.
appdata={'phonemes':phoneme_cards,'pairs':pairs,'stress':stress,'resonance':res_cues,
 'connected':connected,'queue':[{k:r[k] for k in ('record_id','kind','source_id','qaroshi','english','broad_ipa','sound_out','resonance')} for r in queue],
 'course':program,'qc':qc,'manifest':manifest}
s=(ROOT/'tools/v20/app_template.html').read_text(encoding='utf8')
assert s.count('/*__SPEECH_PAYLOAD__*/')==1
encoded=json.dumps(appdata,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
s=s.replace('/*__SPEECH_PAYLOAD__*/',encoded)
site=ROOT/'Qaroshi_20_Speech_Studio.html'
site.write_text(s,encoding='utf8')
manifest['site_html_sha256']=hashlib.sha256(site.read_bytes()).hexdigest()
manifest['site_html_bytes']=site.stat().st_size
savejson('release_manifest.json',manifest)
print(json.dumps({**manifest,'app_bytes':len(s.encode('utf8'))},ensure_ascii=False,indent=2))
