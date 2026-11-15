#!/usr/bin/env python3
"""Curated editorial Qaroshi dialogues with distinct conversational situations.

Authored separately here, not shuffled from one question/repair template; native
speaker/idiomaticity approval is still a separate editorial milestone.
"""
from pathlib import Path
import json, csv, sys, hashlib, re
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/fluency11')]
from phonetics import ipa_text, sound_out_text
from engine import parse_qaroshi, word_analysis, RESONANCES, words

# Each line is separately authored: speaker | Qaroshi | loose contextual English.
# The English translations include discourse inference not directly entailed by each line.
SCENES=[
('a-window-at-night','A window at night','A watcher tries to decide if a distant light is a star or a warning', '''
A|nëm mi yami-lo sëra-m tika.|I see a star at night.
B|hë ti sëra-m tika-te si he?|Did you see the star yourself?
A|sen mi sëra-m tika-te si.|Yes, I personally saw the star.
B|zher mi sëra-m nu tika-te.|I did not see it.
A|më mi ti-wa nëra-yu.|I will stay with you.
B|sen naru sëra-m tika-yu.|We will look for the star together.
'''),
('the-missing-message','The missing message','One friend confuses sending a message with receiving it', '''
A|sen mi shiwaro-m shiwari-te.|I sent a message.
B|hë ti mi-tu shiwaro-m shiwari-te he?|Did you send the message to me?
A|sen mi ti-tu shiwaro-m shiwari-te.|I sent it to you.
B|lën mi shiwaro-m nu tika-te.|I did not see the message.
A|sen mi shiwaro-m shiwari-yu.|I will send it again.
B|hol mi ti-m holë.|Thanks, I appreciate you.
'''),
('permission-to-leave','Permission to leave','A young flier asks before departing a shared roost', '''
A|hë mi goro-ho he?|Am I permitted to fly?
B|sen ti goro-ki.|You are physically able to fly.
A|zher mi goro-ho he?|But am I permitted to fly?
B|qor ti goro-ho.|You have permission.
A|zha mi goro-yu.|Then I will fly!
B|më mi ti-m daru-yu.|I will keep you safe.
'''),
('a-day-of-rest','A day of rest','Two people choose rest rather than another journey', '''
A|hë ti goro-yu he?|Will you fly?
B|sur mi shërohi.|I am tired.
A|hë ti naro-lo nëru-yu he?|Will you rest at home?
B|nëm mi naro-lo nëru-yu.|I will rest at home.
A|më mi ti-wa nëra-yu.|I will stay with you.
B|hol mi ti-m holë.|Thank you for caring.
'''),
('the-borrowed-book','A borrowed book','A friend wants to return a borrowed book after reading', '''
A|hë ti shima-m shëliro-te he?|Did you read the book?
B|sen mi shima-m shëliro-te.|I read the book.
A|hë ti shima-m hari he?|Do you still have it?
B|sen mi shima-m hari.|I have the book.
A|më mi shima-m shëliro-yu.|I would like to read the book.
B|sen mi ti-tu shima-m pëli-yu.|I will give it to you.
'''),
('an-unwanted-journey','An unwanted journey','A companion declines an invitation without giving an excuse', '''
A|hë ti mi-wa goro-yu he?|Will you fly with me?
B|sen mi nu goro-yu.|I am not going to fly.
A|hë ti shërohi he?|Are you tired?
B|sen mi nu shërohi.|I am not tired.
A|më mi ti-m nashi.|I care about you.
B|nëm mi naro-lo nëra-yu.|I will stay at home.
'''),
('reported-flight','A reported flight','A reporter distinguishes a witnessed event from a rumor', '''
A|hë ti qaro-m tika-te he?|Did you see the Nardoragon?
B|sen sa goro-te hu.|I heard they flew.
A|zher ti sa-m nu tika-te.|You did not see them yourself.
B|sen mi sa-m nu tika-te.|I did not see them.
A|hë ti sa-m sharoa-yu he?|Will you ask them?
B|dal mi sa-m sharoa-yu.|I will ask them.
'''),
('a-frightening-storm','A frightening storm','A storm forces an immediate change in plans', '''
A|khar mi lushënga-m tika.|I see a storm!
B|hë ti lushënga-m tika-te si he?|Did you see it directly?
A|sen mi lushënga-m tika-te si.|Yes, I witnessed it.
B|qor ti nu goro ya.|Do not fly.
A|sen mi naro-lo nëra-yu.|I will stay home.
B|nëm naru nëru-yu.|We can rest together.
'''),
('the-repair-promise','The repair promise','Someone refuses to promise a repair they cannot perform', '''
A|rak shenaro shëmoa.|The device is broken!
B|hë ti shenaro-m rëgë-ki he?|Can you repair it?
A|zher mi shenaro-m nu rëgë-ki.|I cannot repair it.
B|hë ti mi-m dëmi-ki he?|Can you help me otherwise?
A|më mi ti-m dëmi-yu.|I will help you.
B|hol mi ti-m holë.|Thank you for helping.
'''),
('a-small-lesson','A small lesson','A teacher allows a learner to ask more questions', '''
A|hë mi shëno-m sharoa-ho he?|May I ask a question?
B|më ti shëno-m sharoa-ho.|You may ask.
A|hë ti mi-m yarëmi-ki he?|Can you teach me?
B|sen mi ti-m yarëmi-ki.|I can teach you.
A|sen mi rëmi-yu.|I will learn.
B|rëm mi ti-m daru-yu.|I will support your learning.
'''),
('the-late-apology','The late apology','A reply comes after the hurt has already happened', '''
A|zher mi shiwaro-m nu tika-te.|I did not see the message.
B|rak ti mi-m nu shiroawe.|You did not listen to me!
A|lën mi përë.|I am sorry.
B|sur mi nu haro.|I am not well.
A|më mi ti-m shiroawe-yu.|I will listen to you.
B|nëm mi nëru-yu.|I need to rest now.
'''),
('two-kinds-of-we','Two kinds of we','A speaker clarifies whether the listener is included', '''
A|zha naru goro-yu.|We, including you, will fly!
B|hë mi goro-yu he?|Will I fly?
A|sen naru goro-yu.|Yes, we will fly together.
B|zher muru goro-yu.|We will fly without including you, although I sound uncertain.
A|më mi ti-wa goro-yu.|I will fly with you.
B|hol mi ti-m holë.|Thank you.
'''),
('a-thirsty-flyer','A thirsty flyer','A flier asks for water before discussing anything else', '''
A|sen mi-na gëro dërawa.|My throat is dry.
B|hë ti kima-m këmë-yu he?|Will you drink some water?
A|sen mi kima-m këmë-yu.|I will drink water.
B|më mi ti-tu kima-m pëli-yu.|I will give you water.
A|hol mi ti-m holë.|Thank you for the kindness.
B|hë ti haro he?|Are you feeling better?
'''),
('choosing-a-boundary','Choosing a boundary','A visitor accepts someone else’s limits', '''
A|hë mi naro-gu nëra-ho he?|May I stay here?
B|sen ti naro-gu nëra-ho.|You may stay here.
A|hë mi ti-m sharoa-ho he?|May I ask you a question?
B|sen mi nu shiri-yu.|I will not talk right now.
A|nëm mi nëru-yu.|I will rest instead.
B|më mi ti-m nashi.|Thank you for respecting my boundary.
'''),
('the-star-and-the-sky','The star and the sky','A learner mistakes two different words while reading', '''
A|sen mi sëra-m shiroli-te.|I wrote the word star.
B|hë ti wena-m shiroli-te he?|Did you write sky?
A|sen mi wena-m nu shiroli-te.|I did not write sky.
B|zher mi shëno-m hari.|I have a question.
A|sen mi sëra-m tika-te.|I saw a star.
B|sen mi wena-m tika-te.|I saw the sky.
'''),
('a-warm-message','A warm message','Someone writes affection without making a demand', '''
A|më mi ti-m nashi.|I cherish you.
B|lën mi shëna-m hari.|I trust you.
A|më mi ti-tu shiwaro-m shiwari-yu.|I will send you a message.
B|hë ti mi-m shëliro-yu he?|Will you read with me?
A|zha naru shima-m shëliro-yu.|We will read a book together!
B|nëm naru nëru-yu.|Then we will rest.
'''),
('the-unfinished-answer','The unfinished answer','A speaker corrects a too-confident prediction', '''
A|hë sa goro-yu he?|Will they fly?
B|sen sa goro-yu hu.|I heard that they will fly.
A|zher sa goro-yu ye.|I infer that they will fly, without first-hand evidence.
B|sen mi sa-m nu tika-te.|I did not see them.
A|hë ti sa-m sharoa-yu he?|Will you ask them?
B|dal mi sa-m sharoa-yu.|I will ask them.
'''),
('an-empty-roost','An empty roost','A traveler learns that a building can be different from belonging', '''
A|sen mi naro-m tika-te.|I saw a home.
B|hë ti naro-m hari he?|Do you have a home?
A|sur mi naro-m nu hari.|I do not have a home.
B|më mi runa-m hari.|I have a chosen family.
A|hë ti mi-m dëmi-ki he?|Can you help me?
B|dal mi ti-m dëmi-yu.|I will help you.
'''),
('memory-on-paper','Memory on paper','A story is recorded so a friend can read it later', '''
A|sen mi moru-m hari.|I have a memory.
B|hë ti moru-m shiroli-ki he?|Can you write it down?
A|sen mi moru-m shiroli-yu.|I will write the memory.
B|sen mi shima-m shëliro-yu.|I will read the book.
A|më mi ti-m nashi.|I cherish you.
B|hol mi ti-m holë.|Thank you for trusting me.
'''),
('the-wrong-inference','The wrong inference','A listener confuses a report with an observation', '''
A|sen sa goro-te hu.|I was told they flew.
B|hë ti sa-m tika-te si he?|Did you see them personally?
A|sen mi sa-m nu tika-te.|I did not see them.
B|zher mi shëna-m nu hari.|I am not confident.
A|sen mi sa-m sharoa-yu.|I will ask them.
B|nëm mi shiwaro-m shëliro-yu.|I will read the answer.
'''),
('a-friendly-question','A friendly question','An invitation becomes an opportunity to choose freely', '''
A|hë ti mi-wa nëru-yu he?|Will you rest with me?
B|sen mi ti-wa nëru-ki.|I can rest with you.
A|hë ti mi-wa nëru-ho he?|Are you allowed to rest with me?
B|sen mi ti-wa nëru-ho.|I have permission to rest with you.
A|më mi ti-m nashi.|I care about you.
B|zha naru nëru-yu.|Then we will rest together!
'''),
('a-quiet-night','A quiet night','The night becomes a place to talk rather than a danger', '''
A|sur mi yami-lo nëra.|I remain here at night, feeling sad.
B|hë ti mi-m shiroawe-ki he?|Can you hear me?
A|sen mi ti-m shiroawe-ki.|I can hear you.
B|më mi ti-tu shiwaro-m shiwari-yu.|I will send you a message.
A|nëm mi shiwaro-m shëliro-yu.|I will read it calmly.
B|hol mi ti-m holë.|I appreciate you.
'''),
('sharing-a-book','Sharing a book','Two learners make space for one another while studying', '''
A|hë ti shima-m hari he?|Do you have the book?
B|sen mi shima-m hari.|I have a book.
A|hë ti mi-tu shima-m pëli-ki he?|Can you give me the book?
B|më mi ti-tu shima-m pëli-yu.|I will give it to you.
A|sen mi shima-m shëliro-yu.|I will read the book.
B|zha naru rëmi-yu.|We will learn together!
'''),
('care-without-a-promise','Care without a promise','A commitment is limited to what a speaker can actually do', '''
A|hë ti mi-wa sëna nëra-ki he?|Could you stay with me forever?
B|zher mi sëna nëra-ki ye.|I infer that I might be able to stay forever, but I am unsure.
A|sur mi kharo-m hari.|I am afraid.
B|qor mi ti-wa nëra-yu.|I will stay with you.
A|hë ti mi-m shiroawe-yu he?|Will you listen to me?
B|më mi ti-m shiroawe-yu.|I will listen.
'''),
('the-lesson-of-no','The lesson of no','Someone respects a refusal instead of trying to negotiate it', '''
A|hë ti mi-wa goro-yu he?|Would you fly with me?
B|sen mi nu goro-yu.|No, I will not fly.
A|hë ti mi-wa nëru-yu he?|Would you rather rest with me?
B|sen mi naro-lo nëru-yu.|I will rest at home.
A|më mi ti-m nashi.|I care about you.
B|nëm mi naro-lo nëra-yu.|I will stay home.
'''),
('the-first-word','The first word','A beginner learns why resonance belongs in writing', '''
A|hë ti qaroshi-m shiri he?|Do you speak Qaroshi?
B|sen mi qaroshi-m shiri.|I speak Qaroshi.
A|hë ti mi-m yarëmi-ki he?|Can you teach me?
B|sen mi ti-m yarëmi-ki.|I can teach you.
A|zha mi rëmi-yu.|I will learn!
B|hol mi ti-m holë.|I appreciate your effort.
'''),
('an-injured-wing','An injured wing','A traveler needs protection, not another challenge', '''
A|sur mi-na banu nu haro.|My wing is not well.
B|hë ti goro-ki he?|Can you fly?
A|sen mi nu goro-ki.|I cannot fly.
B|më mi ti-m daru-yu.|I will protect you.
A|nëm mi naro-lo nëru-yu.|I will rest at home.
B|sen mi ti-wa nëra-yu.|I will stay with you.
'''),
('checking-the-source','Checking the source','Two witnesses disagree and decide what evidence they actually have', '''
A|sen mi qaro-m tika-te si.|I directly saw a Nardoragon.
B|zher mi qaro-m nu tika-te.|I did not see the Nardoragon.
A|hë ti sa-m sharoa-te he?|Did you ask them?
B|sen mi sa-m sharoa-te si.|I asked them myself.
A|hë ti mi-tu shiwaro-m shiwari-yu he?|Will you send me a message?
B|sen mi ti-tu shiwaro-m shiwari-yu.|I will send you the report.
'''),
('patience-in-learning','Patience in learning','A teacher rejects the idea that one error ends progress', '''
A|zher mi nu rëmi.|I am not learning.
B|sen ti rëmi-se.|You are learning now.
A|hë ti mi-m yarëmi-yu he?|Will you teach me?
B|dal mi ti-m yarëmi-yu.|I will teach you.
A|sen mi shëno-m sharoa-yu.|I will ask a question.
B|më mi ti-m përoa-yu.|I will answer you.
'''),
('alone-but-not-lost','Alone but not lost','A traveler distinguishes being alone from needing help', '''
A|sen mi naro-de gura-te.|I left home.
B|hë ti naro-gu gura-yu he?|Will you return home?
A|zher mi naro-m nu tika.|I cannot see home.
B|hë mi ti-m dëmi-ho he?|Am I permitted to help you?
A|më ti mi-m dëmi-ho.|You may help me.
B|dal mi ti-m dëmi-yu.|I will help you.
'''),
('the-unread-story','The unread story','An author shares a story before anyone has read it', '''
A|sen mi moru-m shiroli-te.|I wrote a memory.
B|hë ti shima-m hari he?|Do you have a book?
A|sen mi shima-m hari.|I have a book.
B|hë mi shima-m shëliro-ho he?|May I read the book?
A|më ti shima-m shëliro-ho.|You may read it.
B|zha mi shima-m shëliro-yu.|I will read the book!
'''),
('a-new-friend','A new friend','Two people decide whether to trust one another slowly', '''
A|hë ti mara-m hari he?|Do you have a friend?
B|zher mi mara-m nu hari.|I do not have a friend.
A|më mi ti-m nashi.|I care about you.
B|hë ti mi-m shiroawe-ki he?|Can you listen to me?
A|sen mi ti-m shiroawe-ki.|I can listen.
B|hol mi ti-m holë.|Thank you for caring.
'''),
('an-uncertain-answer','An uncertain answer','A hesitant speaker refuses to invent certainty', '''
A|hë sa goro-yu he?|Will they fly?
B|zher sa goro-yu ye.|I infer that they will fly, but I am uncertain.
A|hë ti sa-m tika-te he?|Did you see them?
B|sen mi sa-m nu tika-te.|I did not see them.
A|sen mi sa-m sharoa-yu.|I will ask them.
B|nëm mi përoa-yu.|I will reply calmly.
'''),
('two-books','Two books','A learner distinguishes possession from lending', '''
A|hë ti shima-ri-m hari he?|Do you have books?
B|sen mi shima-ri-m hari.|I have books.
A|hë ti mi-tu shima-m pëli-ho he?|May you give me a book?
B|më mi ti-tu shima-m pëli-yu.|I will give you a book.
A|sen mi shima-m shëliro-yu.|I will read it.
B|rëm mi ti-m nashi.|I am proud of you.
'''),
('near-the-storm','Near the storm','A flyer changes a plan before a storm arrives', '''
A|hë ti lugoqa-m tika he?|Do you see the weather?
B|sen mi lushënga-m tika-te si.|I saw the storm myself.
A|zher mi goro-yu.|I had planned to fly.
B|khar ti nu goro ya.|Please do not fly!
A|sen mi naro-gu gura-yu.|I will go home.
B|nëm mi ti-wa nëra-yu.|I will stay with you.
'''),
('an-apology-accepted','An apology accepted','A hesitant apology is followed by a concrete change', '''
A|lën mi përë.|I am sorry.
B|sur mi nu haro.|I still feel bad.
A|hë ti mi-m shiroawe-ki he?|Can you listen to me?
B|sen mi ti-m shiroawe-ki.|I can listen.
A|qor mi shiwaro-m shëliro-yu.|I will read your message.
B|nëm mi nëru-yu.|I will rest now.
'''),
('teaching-permission','Teaching permission','A lesson makes the three modal endings explicit', '''
A|hë mi goro-ki he?|Can I fly?
B|sen ti goro-ki.|You are able to fly.
A|hë mi goro-ho he?|May I fly?
B|sen ti goro-ho.|You are allowed to fly.
A|hë mi goro-du he?|Must I fly?
B|sen ti nu goro-du.|You are not obligated to fly.
'''),
('the-silent-roost','The silent roost','A visitor learns when someone needs quiet', '''
A|hë ti haro he?|Are you okay?
B|sur mi nu haro.|I do not feel okay.
A|hë mi ti-m dëmi-ki he?|Can I help you?
B|nëm mi naro-lo nëru-yu.|I will rest at home.
A|më mi ti-wa nëra-yu.|I will stay near you.
B|hol mi ti-m holë.|Thank you for caring.
'''),
('a-returned-memory','A returned memory','A long conversation ends with one remembered promise', '''
A|sen mi moru-m shiroli-te.|I wrote down a memory.
B|hë ti moru-m shëliro-yu he?|Will you read it?
A|sen mi moru-m shëliro-yu.|I will read the memory.
B|hë ti mi-m nashi he?|Do you cherish me?
A|më mi ti-m nashi.|I cherish you.
B|nëm naru nëru-yu.|We will rest together.
'''),
('a-question-of-home','A question of home','A traveler asks whether shelter means belonging', '''
A|hë ti naro-m hari he?|Do you own a home?
B|sen mi naro-m hari.|I have a home.
A|hë ti runa-m hari he?|Do you have chosen family?
B|më mi runa-m hari.|I have a chosen family.
A|zher mi runa-m nu hari.|I do not have chosen family.
B|më mi ti-m nashi.|I care about you.
'''),
('a-letter-for-tomorrow','A letter for tomorrow','A message is planned for a later day', '''
A|sen mi shiwaro-m shiroli-yu.|I will write a message.
B|hë ti mi-tu shiwaro-m shiwari-yu he?|Will you send it to me?
A|sen mi ti-tu shiwaro-m shiwari-yu.|I will send it to you.
B|hë ti shiwaro-m shëliro-te he?|Did you read the earlier message?
A|sen mi shiwaro-m shëliro-te.|I read it.
B|hol mi ti-m holë.|Thank you.
'''),
('warmth-and-distance','Warmth and distance','Two friends agree that care does not require being in the same place', '''
A|wen mi ti-m nashi.|I miss you, and I cherish you.
B|më mi ti-m nashi.|I cherish you too.
A|hë ti mi-wa nëra-yu he?|Will you stay with me?
B|sen mi naro-lo nëra-yu.|I will stay at home.
A|sen mi ti-tu shiwaro-m shiwari-yu.|I will send you a message.
B|hol mi ti-m holë.|Thank you for keeping in touch.
'''),
('finding-the-question','Finding the question','A teacher asks a learner to clarify what is actually unknown', '''
A|zher mi shëno-m hari.|I have a question.
B|hë ti shëno-m sharoa-yu he?|Will you ask it?
A|sen mi goro-ho he?|Am I permitted to fly?
B|sen ti goro-ho.|You are allowed to fly.
A|hë mi goro-ki he?|But can I physically fly?
B|sen ti goro-ki.|You can fly.
'''),
('stars-over-the-roost','Stars over the roost','A story ends with observation rather than prediction', '''
A|nëm mi naro-lo nëra.|I am staying home calmly.
B|hë ti sëra-m tika he?|Do you see a star?
A|sen mi sëra-m tika si.|I see a star myself.
B|zher mi sëra-m nu tika.|I cannot see the star.
A|më mi ti-m daru-yu.|I will protect you.
B|nëm naru sëra-m tika-yu.|We will look together.
'''),
('the-double-negative','The double negative','A learner clarifies a sentence that could mislead', '''
A|sen mi goro-ki.|I can fly.
B|hë ti nu goro-ki he?|Can you not fly?
A|sen mi nu goro-ki.|I cannot fly.
B|zher mi shëno-m hari.|I have a question about that.
A|sen mi goro-ho.|I am permitted to fly.
B|sen mi goro-ki.|I am physically able to fly.
'''),
('trust-after-an-error','Trust after an error','A mistake becomes an invitation to repair the facts', '''
A|rak mi shiwaro-m nu shëliro-te.|I did not read the message!
B|lën mi përë.|I am sorry.
A|zher mi shëna-m nu hari.|I do not feel confident.
B|sen mi shiwaro-m shëliro-yu.|I will read the message.
A|nëm mi ti-m shiroawe-yu.|I will listen to you.
B|më mi ti-m nashi.|I care about you.
'''),
('one-more-story','One more story','Someone values listening more than another long explanation', '''
A|sen mi shima-m shëliro-te.|I read a book.
B|hë ti mi-tu moru-m shiri-yu he?|Will you tell me the memory?
A|sen mi moru-m shiroli-yu.|I will write it down.
B|hë ti mi-m shiroawe-ki he?|Can you listen to me instead?
A|më mi ti-m shiroawe-yu.|I will listen.
B|hol mi ti-m holë.|Thank you.
'''),
('the-cautious-reader','The cautious reader','An uncertain sentence prompts a question about source evidence', '''
A|sen sa goro-te hu.|I was told they flew.
B|hë ti sa-m tika-te si he?|Did you witness that yourself?
A|sen mi sa-m nu tika-te.|No, I did not.
B|zher mi moru-m nu hari.|I have no recollection.
A|sen mi shiwaro-m shëliro-yu.|I will read the message.
B|nëm mi ti-wa nëra-yu.|I will stay here with you.
'''),
('the-final-page','The final page','Two students finish a lesson without calling themselves fluent', '''
A|sen mi shima-m shëliro-te.|I finished reading a book.
B|hë ti qaroshi-m shiri-ki he?|Can you speak Qaroshi?
A|zher mi qaroshi-m shiri-ki ye.|I think I can speak some Qaroshi.
B|sen mi shëno-m hari.|I have a question.
A|hë ti mi-m sharoa-yu he?|Will you ask it?
B|dal naru rëmi-yu.|We will keep learning.
'''),
]

out=[];errors=[];ids=set();corpus=[]
for slug,title,premise,block in SCENES:
    assert slug not in ids,slug;ids.add(slug)
    turns=[]
    for k,line in enumerate([x.strip() for x in block.strip().splitlines() if x.strip()],1):
        parts=line.split('|',2)
        if len(parts)!=3:raise ValueError((slug,line))
        speaker,q,en=[x.strip() for x in parts]
        if q.split()[0] not in RESONANCES:errors.append((slug,k,'resonance missing',q))
        for token in words(q):
            if token in ('nu','si','hu','ye','he','ya','pëla','ko','ro','wë','ara','nao','oru','lan') or token in RESONANCES:continue
            result=word_analysis(token)
            if result['errors']:errors.append((slug,k,result['errors'],q))
        if not q.endswith(('.','?','!')):errors.append((slug,k,'punctuation',q))
        literal=parse_qaroshi(q)
        if not literal['translation']:errors.append((slug,k,'cannot parse literal reading',q))
        turn={'speaker':speaker,'qaroshi':q,'english':en,'literal_translation':literal['translation'],
              'ipa':ipa_text(q),'sound_out':sound_out_text(q),'status':'editorial original, not speaker-attested'}
        turns.append(turn)
        corpus.append({'scene_id':slug,'turn':k,**turn})
    if len(turns)<5:errors.append((slug,'too short'))
    out.append({'id':slug,'title':title,'premise':premise,'turns':turns,'provenance':'separately authored editorial, not spontaneous speaker conversation'})
if errors:
    for x in errors[:50]:print('ERROR',x)
    raise SystemExit(f'{len(errors)} failures')
DEST=ROOT/'corpus/original11';DEST.mkdir(exist_ok=True)
(DEST/'dialogues.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
with (DEST/'dialogue_turns.csv').open('w',encoding='utf8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(corpus[0]));writer.writeheader();writer.writerows(corpus)
# Native text count explicitly counts only Qaroshi surface tokens.
manifest={'authored_scenes':len(out),'turns':len(corpus),'qaroshi_tokens':sum(len(words(x['qaroshi'])) for x in corpus),
 'unique_qaroshi_utterances':len(set(x['qaroshi'] for x in corpus)),
 'unique_situation_ids':len(ids),'attested_spontaneous_conversations':0,
 'english_field':'contextual editorial paraphrase; literal_translation is derived separately by the rule/reference engine',
 'status':'editorial source texts, independently scripted scene outlines (not one rotated dialogue template); require human linguistic review'}
(DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
with (DEST/'Parallel_Dialogues.md').open('w',encoding='utf8') as f:
    f.write('# Independent Qaroshi editorial dialogue scenes\n\nThese are distinct authored scenarios. They have not been spontaneously produced by a real speaker or ratified by a Qaroshi community. Translations preserve the intended context but may include explanatory implications.\n\n')
    for d in out:
        f.write('## '+d['title']+'\n\n'+d['premise']+'\n\n')
        for t in d['turns']:
            f.write('**'+t['speaker']+':** '+t['qaroshi']+'\n\n'+t['english']+'  \nLiteral/reference parse: '+str(t['literal_translation'])+'  \nIPA: `'+t['ipa']+'`\n\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
