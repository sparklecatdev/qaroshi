#!/usr/bin/env python3
"""Build the bilingual sentence corpus, preserving Standard 1.0 attestations."""
from __future__ import annotations
import csv,json,random,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
lex=list(csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf-8-sig')))
old=list(csv.DictReader((ROOT/'source/Qaroshi_Phrasebook_190.csv').open(encoding='utf-8-sig')))
lookup={}
for row in lex:
    parts=[x.strip().lower() for x in row['english'].split(';')]
    for alias in parts:
        lookup.setdefault((alias,row['pos']),row['qaroshi'])

def word(eng,pos):
    return lookup.get((eng.lower(),pos))

def english_verb(phrase):
    # The dictionary gloss for a transitive verb can name its usual object
    # (e.g. 'repair a vehicle'). Drop that illustrative object in a sentence
    # where the actual object is supplied separately.
    exceptions={'listen to music':'listen to',
                'care for a patient':'care for',
                'care for a hatchling':'care for',
                'prepare a meal':'prepare',
                'follow a recipe':'follow',
                'take a selfie':'take',
                'book a ticket':'book',
                'archive data':'archive'}
    return exceptions.get(phrase,phrase.split()[0])

# Every pair is a deliberately selected transitive verb + object sense.
PAIRS='''
computer|use|a computer
document|read|a document
word|write|a word
message|send|a message
friend|protect|a friend
water|drink|water
food|eat|food
book|read|a book
song|sing|a song
computer|repair|a computer
software|install software|software
password|reset a password|a password
password|protect|a password
message|encrypt|a message
message|decrypt|a message
file|open a file|a file
file|save a file|a file
file|rename a file|a file
file|delete a file|a file
file|restore a file|a file
file|copy a file|a file
file|archive data|a file
folder (computing)|search a folder|a folder
source code|compile|source code
source code|review code|source code
code review|document code|a code review
software bug|diagnose a fault|a software bug
software release|test software|a software release
programming|learn|programming
computer|benchmark|a computer
keyboard|repair|a keyboard
router|configure|a router
server|host a server|a server
server|restart|a server
network packet|filter packets|network packets
database|query a database|a database
data|encrypt|data
data|store data|data
data|retrieve data|data
backup|restore data|a backup
record (database)|index data|a database record
photo editing|learn|photo editing
photograph|edit a photo|a photograph
photograph|take a selfie|a photograph
film|review a film|a film
book|publish a book|a book
music|listen to music|music
song|publish a song|a song
painting|create art|a painting
artwork|critique art|an artwork
story|tell a story|a story
poetry|read poetry|poetry
research paper|cite a source|a research paper
research question|investigate|a research question
hypothesis|test a prediction|a hypothesis
formula|derive a formula|a formula
calculation|verify a calculation|a calculation
number|count items|a number
fraction|reduce a fraction|a fraction
equation|solve an equation|an equation
proof|check a proof|a proof
graph (computing)|graph a function|a graph
research paper|publish research|a research paper
instrument|calibrate an instrument|an instrument
chemical sample|test software|a chemical sample
pressure|measure precisely|pressure
temperature|measure temperature|temperature
angle|measure an angle|an angle
area|measure an area|an area
blood pressure|measure blood pressure|blood pressure
symptom|alleviate symptoms|symptoms
wound|clean a wound|a wound
wound|bandage a wound|a wound
medicine|prescribe medication|medicine
patient|care for a patient|a patient
patient|examine medically|a patient
medical record|protect|a medical record
health|protect|health
friend|reassure|a friend
friend|comfort|a friend
spouse|respect|a spouse
relationship|protect|a relationship
boundary|respect boundaries|a boundary
invitation|accept an invitation|an invitation
invitation|decline an invitation|an invitation
contract|sign a contract|a contract
passport|protect|a passport
identity document|verify a transaction|an identity document
crime|investigate legally|a crime
policy|enact policy|a policy
law|repeal a law|a law
candidate|elect|a candidate
candidate (election)|elect|a candidate
protest|organize a protest|a protest
currency|convert currency|currency
money|save money|money
money|spend money|money
loan|repay|a loan
purchase|refund|a purchase
receipt|archive data|a receipt
invoice|invoice|an invoice
item|buy|an item
item|sell|an item
price|negotiate price|a price
payment|verify a transaction|a payment
vehicle|repair|a vehicle
car|drive|a car
car|rent a car|a car
boat|repair|a boat
mountain|climb a mountain|a mountain
river|cross a river|a river
road|cross a road|a road
map|read|a map
route|navigate a route|a route
flight|book a ticket|a flight
seat|reserve a seat|a seat
home|clean a house|a home
room|tidy a room|a room
wall|paint a wall|a wall
furniture|assemble furniture|furniture
bed|make a bed|a bed
clothing|wash clothing|clothing
shoes|polish shoes|shoes
ring (jewelry)|resize a ring|a ring
shirt|sew|a shirt
food|prepare a meal|food
meal|cook|a meal
recipe|follow a recipe|a recipe
ingredient|measure ingredients|an ingredient
vegetable|peel a vegetable|a vegetable
plant|water houseplants|a plant
letter|write|a letter
letter|read|a letter
assignment|submit homework|an assignment
course|register for a course|a course
exam|pass an exam|an exam
exam|fail an exam|an exam
language|learn a language|a language
language|translate between languages|a language
poem|write poetry|a poem
musical instrument|tune an instrument|a musical instrument
wing|groom wings|a wing
nest|guard a nest|a nest
hatchling|care for a hatchling|a hatchling
wing membrane|repair wing membrane|a wing membrane
sky|navigate by stars|the sky
roost|share a roost|a roost
'''.strip().splitlines()
# The source language has lexicalized verbs that can include their own object;
# for an overt Qaroshi direct object we select only *simple transitive predicate* forms.
# Multiword English captions are naturalized as finite predicates (not double-objects).
PRONOUNS={'mi':'I','ti':'you'}
rows=[]
for r in old:
    rows.append({'id':f'S{len(rows)+1:05d}','domain':r['domain'],
                 'qaroshi':r['qaroshi'],'english':r['english'],'note':r['note'],
                 'edition':'1.0','pattern':'original phrasebook'})

skipped=[]
for line in PAIRS:
    noun,verb,object_en=line.split('|')
    n=word(noun,'n');v=word(verb,'v')
    if not n or not v:
        skipped.append((noun,verb,'missing noun' if not n else 'missing verb'))
        continue
    # The first person and the object are overt. In these controlled examples
    # the English gloss is the natural translation of the selected verb lemma.
    ev=english_verb(verb)
    forms=[
        ('sen',f'sen mi {n}-m {v}.',f'I {ev} {object_en}.','Present factual statement'),
        ('sen',f'sen mi {n}-m {v}-yu.',f'I will {ev} {object_en}.','Future statement'),
        ('hë',f'hë ti {n}-m {v}-te he?',f'Did you {ev} {object_en}?','Past polar question'),
        ('sen',f'sen mi {n}-m nu {v}.',f'I do not {ev} {object_en}.','Predicate negation'),
        ('dal',f'dal {n}-m {v} ya!',f'{ev.capitalize()} {object_en}!','Imperative'),
    ]
    for _,q,e,note in forms:
        rows.append({'id':f'S{len(rows)+1:05d}','domain':'Controlled modern vocabulary',
                     'qaroshi':q,'english':e,'note':note,
                     'edition':'2.0','pattern':'controlled SOV paradigms'})
# Advanced syntax examples, carefully chosen with established grammar roots.
ADVANCED=[
('Counterfactuals','sen wënu mi goro-ki, mi wena-gu gura-yu qinë.','If I could fly, I would travel into the sky.','Counterfactual condition and consequent'),
('Optatives','më yëmë ti haro.','May you be safe.','Wishing, not commanding'),
('Optatives','qor yëmë naru sëna haro.','May we all remain safe forever.','Solemn optative with inclusive we'),
('Concessive conditions','dal dasha sa nu goro, mi sa-m daru-yu.','Even if they do not fly, I will protect them.','Even-if condition'),
('Unless','sen shoru sa goro, mi naro-lo nëra-yu.','Unless they fly, I will stay home.','Negative exception condition'),
('Focus','sen mi naro-m rëshi daru.','It is the home that I protect.','Focused object with -m'),
('Focus','sen mi rëshi naro-m daru.','It is I who protect the home.','Focused subject'),
('Collective','sen nashu qaro-ri goro.','The Nardoragons fly together as a group.','Collective quantification'),
('Distributive','sen ngënao qaro goro.','Every Nardoragon flies.','Universal quantifier'),
('Two members','sen gawo qaro-ri goro.','Both Nardoragons fly.','Exactly two'),
('Negative quantifier','sen nura naro-lo eri.','Nobody is at home.','Negative pronoun'),
('Indefinite','sen yano naro-lo eri.','Someone is at home.','Indefinite pronoun'),
('Confirmation','hë sa haro hëmi?','They are okay, right?','Confirmation-tag question'),
('Embedded questions','sen sa haro qona mi sëmi.','I know whether they are well.','Embedded whether with no he'),
('Embedded questions','hë sa haro qona ti sëmi he?','Do you know whether they are well?','Matrix question has one he'),
('Customary source','sen qaro-ri goro lëshu.','By customary knowledge, Nardoragons fly.','Customary-source evidential'),
('Shared ground','sen nësho mi qaro.','As already established, I am a Nardoragon.','Previously shared information'),
('Correction','sen shëgi sa haro.','In fact, they are well.','Unexpected or corrective fact'),
('Opinion','zher hëla sa haro.','In my view, they are well, although I am uncertain.','Epistemic opinion and doubtful register'),
('Politeness','më pëlë ti mi-wa nëra ya.','Please stay with me, if it is acceptable.','Deferential request'),
('Native identity','sen sa qaro.','They are a Nardoragon.','Identity nominal predicate'),
('Native identity','sen sa naro-lo eri-te.','They were at home.','Past existential predicate'),
('Relatives','më mi mi tika-te sha mara-m nashi.','I cherish the friend whom I saw.','Relative before head noun'),
('Ditransitives','sen mi mara-tu kima-m pëli.','I give water to a friend.','Recipient and theme cases'),
('Negation','më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.','Please never die so you can stay with me forever.','Preserved established sentence'),
('Resonance contrast','lën mi ti-m nashi.','I cherish you. (shyly)','Shy confession'),
('Resonance contrast','wen mi ti-m nashi.','I cherish you. (with longing)','Longing'),
('Resonance contrast','qor mi ti-m nashi.','I cherish you. (solemnly)','Serious declaration'),
('Resonance contrast','zha ti lësha!','You are cute! (playfully)','Playful register'),
('Technical notation','sen mi sëna haro.','I am always safe.','Time adverb and predicate'),
]
for dom,q,e,note in ADVANCED:
    rows.append({'id':f'S{len(rows)+1:05d}','domain':dom,'qaroshi':q,
                 'english':e,'note':note,'edition':'2.0','pattern':'advanced grammar'})
with (ROOT/'corpus/parallel_sentences.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
(ROOT/'corpus/parallel_sentences.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'corpus/coverage.json').write_text(json.dumps({'original_sentences':len(old),'new_sentences':len(rows)-len(old),'total_sentences':len(rows),'lexical_pairs_used':(len(rows)-len(old)-len(ADVANCED))//5,'lexical_pairs_skipped':skipped},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'total':len(rows),'original':len(old),'controlled_pairs_used':(len(rows)-len(old)-len(ADVANCED))//5,'skipped':len(skipped)})
print('First skipped:',skipped[:25])
