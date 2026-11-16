#!/usr/bin/env python3
"""100 manually designed situations x 5 controlled transformations = 500 distinct tests.

English stimuli are newly written for adversarial compositional testing; they
are NOT claims of known-good Qaroshi translations, nor independent utterances.
"""
from __future__ import annotations
import csv, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/stress81/challenges_500.csv'

DAILY=[
 ('the cook','washed the bowl','wash the bowl','washed the bowl','the guest would have used it'),
 ('the neighbor','closed the gate','close the gate','closed the gate','the dog would have stayed inside'),
 ('the student','found the missing key','find the missing key','found the missing key','the teacher would have opened the room'),
 ('the gardener','watered the seedlings','water the seedlings','watered the seedlings','the leaves would have stayed green'),
 ('the musician','packed the instrument','pack the instrument','packed the instrument','the trip would have started sooner'),
 ('the baker','burned the bread','burn the bread','burned the bread','the customers would have complained'),
 ('the driver','forgot the directions','forget the directions','forgotten the directions','the trip would have taken longer'),
 ('the child','hid the notebook','hide the notebook','hidden the notebook','the others would have searched for it'),
 ('the shopkeeper','counted the coins','count the coins','counted the coins','the register would have balanced'),
 ('the traveler','lost the ticket','lose the ticket','lost the ticket','the inspector would have asked for identification'),
]
MOTION=[
 ('the courier','crossed the river','cross the river','the bridge was inspected','the storm ended'),
 ('the passengers','boarded the ferry','board the ferry','the captain sounded the bell','the fog cleared'),
 ('the climber','reached the summit','reach the summit','the guide checked the route','the wind grew stronger'),
 ('the ambulance','left the station','leave the station','the dispatcher confirmed the address','the alarm stopped'),
 ('the bicycles','passed the market','pass the market','the road narrowed','the streetlights came on'),
 ('the pilot','landed the aircraft','land the aircraft','the runway lights appeared','the rain became heavier'),
 ('the tourists','entered the museum','enter the museum','the doors opened','the exhibition began'),
 ('the hikers','returned to camp','return to camp','the sun set','the fire was lit'),
 ('the train','stopped at the platform','stop at the platform','the signal changed','the crossing reopened'),
 ('the rescue team','approached the cliff','approach the cliff','the radio transmitted a warning','the tide rose'),
]
SOCIAL=[
 ('the host','the visitor','borrow the bicycle'),
 ('the friend','the neighbor','share the photograph'),
 ('the teacher','the student','read the private letter'),
 ('the dancer','the partner','change the choreography'),
 ('the organizer','the volunteer','record the conversation'),
 ('the artist','the customer','display the portrait'),
 ('the medic','the patient','enter the room'),
 ('the moderator','the member','publish the message'),
 ('the traveler','the companion','use the spare bed'),
 ('the researcher','the participant','keep the audio recording'),
]
LOGIC=[
 ('Nardoragon','Nardoragons','well'),
 ('friend','friends','cute'),
 ('home','homes','locked'),
 ('river','rivers','cold'),
 ('wing','wings','red'),
 ('message','messages','encrypted'),
 ('book','books','complete'),
 ('test result','test results','reliable'),
 ('medical device','medical devices','sterile'),
 ('answer','answers','correct'),
]
EVIDENCE=[
 ('the server restarted','the backup failed'),
 ('the witness changed their story','the meeting was canceled'),
 ('the window was already open','someone entered the room'),
 ('the comet disappeared behind a cloud','the telescope moved'),
 ('the child recognized the voice','the child recognized the face'),
 ('the scientist repeated the measurement','the scientist changed the hypothesis'),
 ('the parcel arrived yesterday','the parcel was returned'),
 ('the bridge cracked overnight','the bridge was repaired'),
 ('the dancer missed the cue','the conductor stopped playing'),
 ('the animal crossed the boundary','the sensor detected movement'),
]
EMBED=[
 ('person who called yesterday','left before sunrise','the meeting would start late','the office had closed'),
 ('book that the student borrowed','was missing its last page','the librarian would check the shelves','someone had torn it out'),
 ('letter that arrived without a name','contained a warning','we would contact the sender','the envelope was damaged'),
 ('machine that the engineer repaired','stopped working again','the team would inspect the wiring','the replacement part was faulty'),
 ('dog that followed the cyclist','waited near the bridge','its owner would come looking','the road was busy'),
 ('song that the choir rehearsed','was shorter than expected','the concert would finish early','one verse was omitted'),
 ('photograph that the traveler saved','showed the wrong mountain','the map would need correction','the camera clock was wrong'),
 ('message that the moderator deleted','had already been forwarded','the group would need an explanation','the message disclosed private data'),
 ('medicine that the patient requested','was not available','the doctor would suggest an alternative','the shipment was delayed'),
 ('story that the children invented','confused the adults','the teacher would ask for details','two characters had identical names'),
]
COUNTER=[
 ('the courier','deliver the letter','delivered the letter','the address was unreadable','the recipient would have replied'),
 ('the traveler','take the early train','taken the early train','the tickets were sold out','the traveler would have arrived by noon'),
 ('the gardener','save the tree','saved the tree','the roots were badly damaged','the courtyard would have more shade'),
 ('the student','solve the equation','solved the equation','the variables were missing','the class would have understood the proof'),
 ('the pilot','avoid the storm','avoided the storm','the radar was unavailable','the passengers would have landed sooner'),
 ('the librarian','replace the damaged book','replaced the damaged book','the replacement had not arrived','the readers would have found the chapter'),
 ('the musician','finish the concert','finished the concert','the power had failed','the audience would have heard the last song'),
 ('the mechanic','repair the engine','repaired the engine','the correct part was missing','the vehicle would have started'),
 ('the volunteer','open the shelter','opened the shelter','the keys had been misplaced','the guests would have entered safely'),
 ('the captain','reach the island','reached the island','the current was too strong','the crew would have rested earlier'),
]
VALENCY=[
 ('mechanic','engine','repaired','repair','repaired','a wrench'),
 ('baker','oven','cleaned','clean','cleaned','a brush'),
 ('gardener','fence','painted','paint','painted','a roller'),
 ('technician','sensor','calibrated','calibrate','calibrated','a reference device'),
 ('artist','wall','decorated','decorate','decorated','colored tiles'),
 ('archivist','document','copied','copy','copied','a scanner'),
 ('tailor','coat','altered','alter','altered','a needle'),
 ('carpenter','table','assembled','assemble','assembled','wooden pegs'),
 ('driver','vehicle','washed','wash','washed','a hose'),
 ('worker','door','secured','secure','secured','a steel lock'),
]
NARRATIVE=[
 ('the sky swallowed the last light','sunset arriving','astronomical destruction'),
 ('the forest kept its secrets','the narrator withholding information','trees possessing thoughts'),
 ('the clock argued with the silence','a tense atmosphere','a machine literally speaking'),
 ('the river carried a thousand memories','recollections tied to a place','water possessing human memories'),
 ('the town held its breath','collective anticipation','residents not breathing'),
 ('the mountain refused to move','the mountain appearing stubborn','rock deciding to resist'),
 ('the old house remembered every winter','an atmosphere shaped by history','a building having a brain'),
 ('the storm knocked on the door','wind and rain striking the entrance','weather making a polite request'),
 ('the road forgot its travelers','abandoned paths and lost history','pavement having amnesia'),
 ('the fire painted the room gold','warm colored light','flames using a paintbrush'),
]
TECH=[
 ('the battery overheated','the safety circuit should stop charging','the charger was defective'),
 ('the audit log was incomplete','the investigator should request another record','the operator deleted evidence'),
 ('the network connection dropped','the client should retry later','the server was attacked'),
 ('the laboratory sample was contaminated','the experiment should be repeated','the hypothesis was false'),
 ('the encrypted file was copied','the access keys should be rotated','the contents were decrypted'),
 ('the temperature sensor drifted','the measurement should be recalibrated','the equipment was permanently damaged'),
 ('the patient record contained an error','the clinician should verify the source','the patient was dishonest'),
 ('the bridge inspection revealed corrosion','the engineers should assess the structure','the bridge would collapse'),
 ('the telescope recorded a faint signal','the observers should rule out noise','the signal came from an alien civilization'),
 ('the contract lacked a signature','the parties should request clarification','the contract was automatically void'),
]
assert all(len(x)==10 for x in (DAILY,MOTION,SOCIAL,LOGIC,EVIDENCE,EMBED,COUNTER,VALENCY,NARRATIVE,TECH))

def create():
    records=[]
    def add(domain,feature,family,variants):
        assert len(variants)==5 and all(isinstance(v,str) and v.rstrip('\"').endswith(('.', '?', '!')) for v in variants), (domain,family,variants)
        for variant,s in enumerate(variants,1):
            records.append({'id':f'QS81-{len(records)+1:04d}', 'domain':domain,
                            'scenario_family':f'{domain.upper()}-{family:02d}',
                            'variant':variant,'feature':feature[variant-1],
                            'english':s,'provenance':'editor-authored controlled challenge; not attested speech'})
    for i,(who,past,bare,part,consequence) in enumerate(DAILY,1):
        add('daily',('declarative','predicate negation','direct question','reported information','past counterfactual'),i,[
            f'{who.capitalize()} {past}.', f'{who.capitalize()} did not {bare}.',
            f'Did {who} {bare}?',f'I was told that {who} {past}.',
            f'If {who} had {part}, {consequence}.'])
    for i,(who,past,bare,after,before) in enumerate(MOTION,1):
        add('time_motion',('after clause','before clause','while contrast','until negation','temporal question'),i,[
            f'After {who} {past}, {after}.', f'Before {before}, {who} {past}.',
            f'{who.capitalize()} {past} while {after}.',
            f'{who.capitalize()} did not {bare} until {before}.',
            f'Did {who} {bare} before {after}?'])
    for i,(asker,other,action) in enumerate(SOCIAL,1):
        add('social_consent',('permission question','explicit refusal','offer rejection','silence inference','consent revocation'),i,[
            f'{asker.capitalize()} asked {other} whether it was okay to {action}.',
            f'{other.capitalize()} said no when {asker} asked to {action}.',
            f'{asker.capitalize()} offered to {action}, but {other} declined.',
            f'{asker.capitalize()} did not treat {other} leaving silently as permission to {action}.',
            f'{other.capitalize()} withdrew permission before {asker} could {action}.'])
    for i,(sing,plural,adj) in enumerate(LOGIC,1):
        add('quantifier_logic',('universal','not all','none','existential','exclusive focus'),i,[
            f'Every {sing} is {adj}.',f'Not every {sing} is {adj}.',
            f'No {sing} is {adj}.',f'Some {plural} are {adj}.',
            (f'Only this Nardoragon is well right now.' if i==1 else f'Only this {sing} is {adj}.')])
    for i,(claim,alternative) in enumerate(EVIDENCE,1):
        add('evidentiality',('direct observation','reported evidence','inference','embedded yes/no question','epistemic refusal'),i,[
            f'I witnessed that {claim}.',f'Someone told me that {claim}.',
            f'I inferred that {claim} from the evidence.',
            f'I do not know whether {claim}.',
            f'I am not claiming that {alternative}.'])
    for i,(head,predicate,consequence,reason) in enumerate(EMBED,1):
        add('embedding_reference',('relative clause','nested content','embedded yes/no question','conditional with relative','causal relative'),i,[
            f'The {head} {predicate}.',
            f'I think the {head} {predicate}.',
            f'I do not know whether the {head} {predicate}.',
            f'If the {head} {predicate}, {consequence}.',
            f'The {head} {predicate} because {reason}.'])
    for i,(who,base,part,barrier,consequence) in enumerate(COUNTER,1):
        add('counterfactual_modal',('past counterfactual','ability vs barrier','permission not ability','necessity despite barrier','open hypothetical'),i,[
            f'If {who} had {part}, {consequence}.',
            f'{who.capitalize()} could {base}, but {barrier}.',
            f'{who.capitalize()} was allowed to {base}, although {barrier}.',
            f'{who.capitalize()} had to {base} even though {barrier}.',
            f'{who.capitalize()} would {base} if {barrier} changed.'])
    for i,(actor,patient,past,bare,part,tool) in enumerate(VALENCY,1):
        add('voice_valency',('active object','explicit passive agent','instrument distinction','negative active','passive question'),i,[
            f'A {actor} {past} the {patient}.',
            f'The {patient} was {part} by a {actor}.',
            f'A {actor} {past} the {patient} using {tool}.',
            f'A {actor} did not {bare} the {patient}.',
            f'Was the {patient} {part} by a {actor}?'])
    for i,(metaphor,interpretation,literal) in enumerate(NARRATIVE,1):
        add('narrative_figures',('figurative narration','quoted metaphor','reported reading','literal vs figurative','misinterpretation repair'),i,[
            f'In the story, {metaphor}.',
            f'The narrator wrote, "{metaphor}."',
            f'The poet used "{metaphor}" to suggest {interpretation}.',
            f'The sentence "{metaphor}" does not assert {literal}.',
            f'The reader first took "{metaphor}" literally, then corrected that reading.'])
    for i,(claim,consequence,unsupported) in enumerate(TECH,1):
        add('technical_precision',('technical assertion','technical report','provisional uncertainty','conditional consequence','inference blocked'),i,[
            f'The report states that {claim}.',
            f'A second observer recorded that {claim}.',
            f'It is possible that {claim}, but that has not been independently verified.',
            f'If {claim}, {consequence}.',
            f'The fact that {claim} does not prove that {unsupported}.'])
    assert len(records)==500 and len({r['english'].casefold() for r in records})==500
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
    return records
if __name__=='__main__':
    from collections import Counter
    rows=create();print('Generated',len(rows),'novel controlled English challenge sentences:',dict(Counter(r['domain'] for r in rows)))
