#!/usr/bin/env python3
"""Individually written candidate explanatory distinctions grounded in source glosses.

Definitions are editorial interpretations, not speech-community-ratified meanings.
Sample uses come from unchanged prior corpus, not fabricated new attestations.
"""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v16';OUT.mkdir(exist_ok=True,parents=True)
# [lemma, interpretation, selection restriction, contrast / semantic uncertainty]
IDEAS=[
('tika','Perceive something visually or notice its presence.','The overt object should be something plausibly seen, or an explicit context should license a mental noticing reading.','ronaro means auditory perception; sëmi implies knowledge rather than one act of seeing.'),
('nëra','Remain or stay at a location.','A place case or context can make the location clear. Do not treat physical staying as resting.','nëru is rest, not necessarily staying still; gura is movement away.'),
('nëru','Pause activity and rest.','The predicate profiles rest rather than a guarantee of safety or sleep.','nëra is remaining in place; shërohi denotes being tired.'),
('holë','Verb expressing thanks or gratitude.','Use an appropriate recipient or object frame; gratitude cannot be inferred from a bare positive resonance.','hol is a resonance register of gratitude, not the same grammatical form as the verb holë.'),
('rëgë','Restore an object to functioning condition.','The affected entity must be something repairable in context. Metaphorical repair needs marking as figurative.','shëmoa is broken; daru means protect rather than repair.'),
('dëmi','Provide help or assistance.','The argument is a beneficiary or assisted activity; not identical to repairing an object.','rëgë focuses restoration, while daru focuses protection.'),
('këmiro','Recall a person, event or information.','Do not infer that a recollection is accurate merely because it is remembered.','moru is the remembered content; sëmi means possess knowledge.'),
('qaroshi','The Nardoragon language itself.','Names the language, not automatically an individual member of the species.','qaro names a Nardoragon being or individual.'),
('yami','Night, the dark part of the day.','A time expression; avoid conflating with all darkness or sadness.','nënayaro and yurayaro are calendar-day references.'),
('shenaro','Powered machine or device.','Not all tools or possessions are necessarily powered machines.','rëgë can repair a machine; shëmoa characterizes a broken one.'),
('tarowa','Bridge allowing passage across a gap.','Literal referents involve a crossing; a metaphorical social bridge needs explicit contextual licensing.','shënu is a road or trail, not necessarily an elevated crossing.'),
('raro','Door or entry barrier.','A door is an architectural entrance feature, not a room or whole house.','naro means home or shelter.'),
('kimazu','Rain or falling precipitation.','A weather event, not necessarily a storm.','lushënga is a storm; lugoqa denotes weather generally.'),
('shirali','Sing or perform a song.','The action presupposes vocal musical performance rather than all music making.','shira is a song; rënawa is music in general.'),
('tikaro','A visually perceived or represented picture, not tied to one artistic medium.','Does not require a painted medium; distinguish from works requiring the paint verb.','mërawë is painting or artistic image; dewësha is drawing.'),
('kharo','An experienced emotion of fear or an alarming state of concern.','An affective state; an alarmed reaction does not always show direct external danger.','khar is a written resonance register, not this nominal lexeme.'),
('pësheha','Doctor, medical professional.','Denotes a professional role, not a medicine or a symptom.','guwiko denotes medicine, a drug.'),
('zhëmiro','Find or discover an object, place or fact.','Do not translate as know unless acquisition of reliable knowledge is conveyed.','sëmi describes knowledge; shënami indicates losing something.'),
('debokhu','Apply pigment or color as a process of painting a surface or image.','Select a canvas/object or medium licensed by context.','mërawë denotes a painting, while dewësha denotes a drawing.'),
('shënami','Lose or misplace something.','Misplacing an object is not the same as forgetting a remembered detail.','këmiro is to recall; zhëmiro is to find.'),
('guwiko','A substance used as medicine, without guaranteeing an outcome.','The lexeme names a substance, not a doctor or a guaranteed cure.','pësheha denotes a doctor; dëmi denotes assistance.'),
('shëroa','A physical blanket or covering associated with warmth or protection.','A physical covering; use metaphorically only with contextual explanation.','naro is shelter, which is not always a blanket.'),
('wëli','Walk or move on foot.','Method of movement is on foot; flying and generic travel are separate verbs.','goro is fly; gura is travel in a broader sense.'),
('lugoqa','Weather or atmospheric conditions.','Describes the broader situation; not restricted to rain or storms.','kimazu is rain; lushënga is a storm.'),
('shënu','Road, route or traveled trail.','A constructed or traversed route, not automatically a bridge or map.','tarowa is a bridge; tëkaro is a map.'),
('yalë','Flower, the blossom of a plant.','A biological object; not necessarily a whole plant or garden.','tëzhida is a garden; lëruwa is a tree.'),
('tëzhida','Garden, cultivated area of plants.','Names a place; not a single flower or tree.','yalë means flower; lëruwa means tree.'),
('nësega','Edible matter considered as food, rather than a specific meal.','Do not infer a particular meal, bread, or eating action.','nëpoqo denotes bread; shëma means eat.'),
('rënali','Dance or move to rhythm.','Movement is rhythmic; not equivalent to any walking or to the music itself.','rëmawe is a dance; rënawa is music; wëli is walking.'),
('kimari','Fish, aquatic animal.','Literal referent is an animal; not a river or general water substance.','kimaro means river, kima means water.'),
('dewësha','Drawing, a visual work made by drawing.','An image form; can differ in medium and activity from painting.','debokhu is painting as a verb; mërawë is painting as an artwork.'),
('luguzha','Shore or edge of water.','A place at the boundary; not the sea or the river itself.','wëma is sea; kimaro is river.'),
('zekunga','A member of the animal category identified as a feline or cat.','An animal designation; should not be automatically applied to the Nardoragon species.','qaro denotes a Nardoragon individual.'),
('rënawa','Music or organized sound.','The category can include but is not limited to sung songs.','shira is a song; shëru is a rhythmic beat.'),
('karoa','An object or token providing access to a place or restricted system.','A means of access; does not necessarily refer to a physical metal key.','raro is the door whose access might be governed by a key.'),
('shëru','Rhythm or regular beat.','Temporal pattern of beats; not equivalent to a whole song or a dance.','rënawa is music; rëmawe is a dance.'),
('gëro','The anatomical throat as part of the body, not the voice itself.','A bodily location; do not conflate with voice as audible behavior.','shiri is speak; shi is voice or speech.'),
('dërawa','Dry or lacking moisture.','Property whose correct referent depends on context; not every abstract entity can be dry.','kima denotes water; dryness is not the same as thirst without contextual support.'),
('këmuro','Agree or arrive at consensus.','Reaching agreement is a negotiated event, not merely listening or acknowledging.','shiroawe means listen; sharoa means ask.'),
('rawëli','Want, wish or desire something.','Desire by itself is not a promise, ability, permission or obligation.','namu denotes promise; -ki, -ho and -du are distinct modalities.'),
('rëmawe','Dance, a coordinated movement sequence.','A dance as a structured event or piece, not automatically the act of dancing.','rënali is the act of dancing; shëru is the beat.'),
('tëkaro','Map or spatial representation.','Represents space, but is not itself a travel act or compass.','rehëngo means compass; shënu means road.'),
('wëma','A large sea or oceanic body of water, distinct from a river.','A major body of salt water; not an individual river, rain or drinking water.','kimaro is river; kima is water.'),
('maru','Leaf, part of a plant.','A single plant structure, not necessarily a tree, flower or garden.','lëruwa is tree; yalë is flower.'),
('lukhela','Sunrise, the sun appearing at daybreak.','A time-of-day event; do not read as a generic day or a metaphor for hope without context.','yami is night; nënayaro is today.'),
('rërawëmi','Finish or bring an activity to completion.','The action is completion of a task or process; not necessarily success or agreement.','këmuro is reach agreement; wëmi is work.'),
('khura','Wind, moving air, breath of the world.','Nature imagery in the gloss permits literal airflow; metaphorical breathing requires context.','lushënga means storm, a larger weather event.'),
('sëru','A reproductive seed of a plant, often a stage before germination.','Refers to a biological unit; a metaphorical beginning is only a proposed extension.','yalë is flower; maru is leaf.'),
('yela','The moon as a celestial body, distinct from an individual star.','Celestial body; do not confuse with the sun or a star.','sëra means star; lukhela sunrise.'),
('nëpoqo','Bread as a specific prepared food rather than nourishment in general.','A food item, not the entire category of nourishment.','nësega denotes food in general; shëma means eat.'),
('shëma','Consume food through eating, an action distinct from drinking.','The action requires a relevant edible object or a contextually omitted object.','këmë is drink; nësega is food.'),
('shërahi','Bird or winged wildlife.','Animal that is winged; does not automatically imply it is a Nardoragon.','qaro denotes Nardoragon; banu means wing.'),
('shilë','Letter or written sign.','An orthographic unit, not a complete written message.','shiwaro is message; shiroli is write.'),
('yarao','A person who teaches or mentors, not the teaching event itself.','Names a person in an instructional role, not the act of teaching.','yarëmi is teach; rëmi is learn.'),
('qëmogë','Market or commercial trading place.','Place/institution where buying occurs; not the act of purchase.','pëmi is buy; nësega is food, which might be traded.'),
('lëruwa','A woody plant with a trunk or branches, considered as a whole.','Whole plant rather than a single leaf or flower.','maru means leaf; yalë means flower.'),
('khimë','A visible mass of condensed moisture in the atmosphere.','Atmospheric object; its presence does not by itself establish rain or storm.','kimazu denotes rain; lushënga denotes storm.'),
]

def main():
 with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f: lex={x['qaroshi']:x for x in csv.DictReader(f)}
 with (ROOT/'data/v16/lexical_evidence_index_30000.csv').open(encoding='utf8',newline='') as f:evidence={x['qaroshi']:x for x in csv.DictReader(f)}
 output=[]
 for i,(word,definition,restriction,contrast) in enumerate(IDEAS,1):
  if word not in lex:raise RuntimeError('Unknown source word: '+word)
  x=lex[word];e=evidence[word]
  output.append({'id':f'LXP16-{i:03d}','qaroshi':word,'source_headword_id':x['id'],
  'canonical_gloss_unmodified':x['english'],'editorial_definition_proposal':definition,
  'restriction_and_usage_boundary':restriction,'contrast_or_false_friend':contrast,
  'example_qaroshi':e['editorial_example_qaroshi'],'example_english':e['editorial_example_english'],
  'example_source_id':e['editorial_example_source'],
  'example_status':'previous separately drafted editorial or controlled bilingual example; not speaker-attested' if e['editorial_example_qaroshi'] else 'none present',
  'pos':x['pos'],'ipa':x['ipa'],'status':'new individually written lexical explanation, pending independent review',
  'reviewer':'','human_approval':'no','revised_definition':'','editorial_notes':''})
 out=ROOT/'data/v16/new_core_lexical_profiles.csv'
 with out.open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
 print('written_profiles',len(output),'with_previous_examples',sum(bool(r['example_qaroshi']) for r in output))
if __name__=='__main__':main()
