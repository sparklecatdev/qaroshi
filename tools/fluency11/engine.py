#!/usr/bin/env python3
"""Qaroshi 11 editorial grammar engine.

Conservative rule-based parser/transducer, not a universal translator or
linguistic authority. It returns explicit interpretations and confidence
boundaries, never silently chooses an unlicensed sense or clause structure.
"""
from __future__ import annotations
import csv, json, re, unicodedata, argparse, difflib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f:
    LEX = {r['qaroshi']: r for r in csv.DictReader(f)}

RESONANCES = {'më':'tender', 'zha':'playful', 'qor':'solemn', 'sen':'neutral',
              'hë':'inquisitive', 'lën':'shy', 'sur':'grieving', 'rak':'defiant',
              'khar':'alarmed', 'yë':'surprised','nëm':'calm','wen':'longing',
              'dal':'determined','rëm':'proud','hol':'grateful','zher':'uncertain'}
VOICES={'ru':'causative','li':'passive','wo':'reciprocal','ne':'reflexive'}
TENSES={'te':'past','yu':'future'}
ASPECTS={'se':'progressive','mo':'completive','në':'habitual'}
MODALS={'ki':'ability','ho':'permission','du':'obligation'}
CASES={'m':'object','na':'genitive','lo':'location','gu':'goal','de':'source','wa':'companion','tu':'recipient','shi':'instrument'}
NSLOTS={'lë':1,'ri':2,**{x:3 for x in CASES},'së':4}
VSLOTS={**{x:1 for x in VOICES},**{x:2 for x in TENSES},**{x:3 for x in ASPECTS},**{x:4 for x in MODALS},'la':5}
PRON={'mi':('I','me','my',1),'ti':('you','you','your',2),'sa':('they','them','their',3),'sari':('they','them','their',3),'naru':('we','us','our',1),'muru':('we','us','our',1)}
FUNCTIONS={'nu','he','ya','si','hu','ye','pëla','lan'}
CONNECTORS={'wë': 'if','ro':'because','ko':'so that','uro':'although','yaro':'while','ana':'after','ëna':'before','do':'that','ara':'and','nao':'but','oru':'or'}
TOK=re.compile(r"[a-zë]+(?:-[a-zë]+)*",re.IGNORECASE)
LEX_VERBS={
 'goro':('fly',False),'këmë':('drink',True),'daru':('protect',True),
 'tika':('see',True),'shiri':('speak',True),'nashi':('cherish',True),
 'nëru':('rest',False),'nëra':('stay',False),'hari':('have',True),
 'dëmi':('help',True),'pëli':('give',True),'shiwari':('send',True),
 'shiroli':('write',True),'shëliro':('read',True),'sharoa':('ask',True),
 'rëmi':('learn',False),'yarëmi':('teach',True),'rëgë':('repair',True),
 'përoa':('reply',True),'shiroawe':('listen',True),
 'përë':('apologize',False),'gura':('travel',False),'holë':('thank',True),
}
LEX_NOUNS={
 'kima':('water','mass'),'naro':('home','count'),'mara':('friend','count'),
 'qaro':('Nardoragon','count'),'shima':('book','count'),
 'shiwaro':('message','count'),'moru':('memory','count'),
 'sëra':('star','count'),'wena':('sky','unique'),'yami':('night','count'),
 'gëro':('throat','count'),'banu':('wing','count'),
 'shëno':('question','count'),'namu':('promise','count'),
 'shëna':('trust','mass'),'lushënga':('storm','count'),
 'runa':('chosen family','mass'),'qaroshi':('Qaroshi','proper'),
 'shenaro':('device','count'),
}
LEX_ADJ={'haro':'well','lësha':'cute','dërawa':'dry','shërohi':'tired'}
EN_PRON={'i':'mi','you':'ti','they':'sa','we':'naru'}
IRREG_PAST={'see':'saw','fly':'flew','drink':'drank','give':'gave','have':'had',
 'write':'wrote','send':'sent','read':'read','speak':'spoke','teach':'taught'}
IRREG_PART={'see':'seen','fly':'flown','drink':'drunk','give':'given','have':'had',
 'write':'written','send':'sent','read':'read','speak':'spoken','teach':'taught'}

# Existing Standard 7.0 controlled parallel examples supplement the grammar engine.
# They are examples from the reference, NOT observed natural speaker corpora.
def _norm_sentence(s:str) -> str:
    return re.sub(r'[\s,;.!?]+',' ',unicodedata.normalize('NFC',s).casefold()).strip()

CORPUS_Q={}
CORPUS_EN={}
with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:
    for row in csv.DictReader(f):
        q=_norm_sentence(row['qaroshi']);en=_norm_sentence(row['english'])
        CORPUS_Q.setdefault(q,[]).append(row)
        CORPUS_EN.setdefault(en,[]).append(row)


def words(text: str)->list[str]:
    return TOK.findall(unicodedata.normalize('NFC',text).lower())

def word_analysis(word:str)->dict:
    s=word.lower().strip(); root,*suffix=s.split('-')
    record=LEX.get(root)
    if not record:
        return {'surface':word,'root':root,'known':False,'errors':[f'Unknown lemma {root}'],
                'suggestions':difflib.get_close_matches(root,LEX.keys(),n=3,cutoff=.82)}
    pos=record['pos']; slots=VSLOTS if pos=='v' else NSLOTS if pos in ('n','pron','det') else {}
    errors=[];last=0;features={}
    for x in suffix:
        slot=slots.get(x)
        if slot is None:errors.append(f'{pos} cannot carry -{x}')
        elif slot<=last:errors.append(f'-{x} violates suffix order or duplicates slot {slot}')
        else:last=slot
        if x in CASES:features['case']=CASES[x]
        elif x=='ri':features['number']='plural'
        elif x in VOICES:features['voice']=VOICES[x]
        elif x in TENSES:features['tense']=TENSES[x]
        elif x in ASPECTS:features['aspect']=ASPECTS[x]
        elif x in MODALS:features['modal']=MODALS[x]
        elif x=='së':features['topic']=True
        elif x=='la':features['manner']='tender'
        elif x=='lë':features['diminutive']=True
    return {'surface':word,'root':root,'known':True,'pos':pos,
            'gloss':record['english'],'ipa':record['ipa'],'suffixes':suffix,
            'features':features,'errors':errors}


def _noun(n:dict,with_article:bool=True,case_role:str='object') -> str:
    root=n.get('root','');f=n.get('features',{})
    if root in PRON:
        if f.get('case')=='genitive':return PRON[root][2]
        if case_role=='subject':return PRON[root][0]
        return PRON[root][1]
    val,kind=LEX_NOUNS.get(root,(n.get('gloss','').split(';')[0], 'count'))
    if f.get('number')=='plural':
        if kind=='count':
            if val.endswith('y'):val=val[:-1]+'ies'
            elif val.endswith('s'):val+='es'
            else:val+='s'
        return val
    if kind=='unique':return 'the '+val
    if kind=='proper':return val
    if kind=='mass':return val
    if with_article:
        return ('an ' if val[0].lower() in 'aeiou' else 'a ')+val
    return val


def _np(seq:list[dict],i:int=0,role:str='subject'):
    """Consume a NP: [genitive-name] + noun or a pronoun/one noun. Returns (phrase, next_idx, features)."""
    if i>=len(seq):return None,i,{}
    w=seq[i]
    if not w.get('known'):return None,i,{}
    if w['pos'] not in ('pron','n','det'):return None,i,{}
    if w.get('features',{}).get('case')=='genitive':
        if i+1>=len(seq) or seq[i+1].get('pos')!='n':return None,i,{}
        own=_noun(w,False);child=seq[i+1];s=_noun(child,False)
        if own in ['my','your','their','our']:
            return own+' '+s,i+2,child['features']
        return own+"'s "+s,i+2,child['features']
    return _noun(w,case_role=role),i+1,w.get('features',{})


def _split_clause(ts:list[str]) -> tuple[list[str],str|None,list[str]]:
    # Subordinate split is only enabled with clear comma or conjunction role.
    for c in ['ko','ro','uro','nao','ara','oru','yaro','do']:
        if c in ts[1:-1]:
            i=ts.index(c)
            return ts[:i],c,ts[i+1:]
    return ts,None,[]


def _verb_forms(base:str,subject:str,features:dict,neg:bool,question:bool)->tuple[str,str]:
    tense=features.get('tense','present');asp=features.get('aspect');mod=features.get('modal')
    if features.get('voice') or features.get('manner'):
        raise ValueError('Voice or tender manner requires human validation in English rendering')
    if asp=='completive':
        # Distinguish past and future reference, avoid overconfident overlap with English perfects
        if tense=='past':aux='had';v=IRREG_PART.get(base,base+'ed')
        elif tense=='future':aux='will have';v=IRREG_PART.get(base,base+'ed')
        else:aux='have';v=IRREG_PART.get(base,base+'ed')
    elif asp=='progressive':
        aux={'past':'was' if subject=='I' else 'were','future':'will be',
             'present':'am' if subject=='I' else 'are'}[tense]
        v=base[:-1]+'ing' if base.endswith('e') and base not in ('see',) else base+'ing'
        if base=='fly':v='flying'
        if base=='see':v='seeing'
    elif asp=='habitual':aux='usually' if tense=='present' else ('used to' if tense=='past' else 'will usually');v=base
    elif mod:
        aux={'ability':'can','permission':'may','obligation':'must'}[mod];v=base
    elif tense=='future':aux='will';v=base
    elif tense=='past':aux='did' if question or neg else '';v=base if (question or neg) else IRREG_PAST.get(base,base+'ed')
    elif question or neg:aux='do' if subject in ('I','you','they','we') else 'does';v=base
    else:
        aux='';v=base if subject in ('I','you','they','we') else (base+'s' if not base.endswith(('s','sh','ch')) else base+'es')
    if neg:
        if not aux:aux='do' if subject in ('I','you','they','we') else 'does';v=base
        if aux=='can':aux='cannot'
        elif aux in ('may','must','did','do','does','will','have','had','was','were','are','am'):aux+=' not'
        elif aux in ('will be','will have'):aux+=' not'
        elif aux=='usually':aux='do not usually'
        elif aux=='used to':aux='did not use to'
    return aux,v


def _render_clause(raw:list[str], mood:str|None=None,evidential:str|None=None):
    ts=raw[:];errors=[];warnings=[]
    neg=False
    if len(ts)>1 and ts[-2]=='nu':
        neg=True;ts.pop(-2)
    if not ts:return None,['Empty clause'],[]
    part=[word_analysis(t) for t in ts]
    for w in part:errors.extend(w.get('errors',[]))
    if errors:return None,errors,warnings
    final=part[-1]
    if final.get('pos') not in ('v','adj'):
        return None,[f'No licensed finite predicate at end of clause ({ts[-1]})'],warnings
    predicate=part.pop()
    if not part:return None,['Missing subject/argument phrase'],warnings
    subject,j,subfeat=_np(part,0,'subject')
    if not subject:return None,['Could not identify initial subject NP'],warnings
    remainder=part[j:];obj=[];obliques=[];adv=[];unhandled=[]
    k=0
    while k<len(remainder):
        cur=remainder[k];root=cur.get('root');features=cur.get('features',{})
        if cur.get('pos')=='adv':
            ad=cur['gloss'].split(';')[0]
            if ad in ('always','never','often','sometimes','again','later','soon','today','tomorrow','yesterday'):adv.append(ad)
            else:unhandled.append(cur['surface'])
            k+=1;continue
        if cur.get('pos') not in ('n','pron'):unhandled.append(cur['surface']);k+=1;continue
        np,nk,nf=_np(remainder,k,'object')
        if not np:unhandled.append(cur['surface']);k+=1;continue
        role=features.get('case') or nf.get('case')
        if role=='object':obj.append(np)
        elif role in ('location','goal','source','companion','recipient','instrument'):
            obliques.append({'location':'at','goal':'toward','source':'from','companion':'with','recipient':'to','instrument':'using'}[role]+' '+np)
        else:unhandled.append(cur['surface'])
        k=nk
    if unhandled:return None,[f'Unsupported clause constituent(s): {", ".join(unhandled)}'],warnings
    if len(obj)>1:return None,['Multiple direct objects need an explicit licensed valency structure; use -tu for recipients'],warnings
    if final['pos']=='adj':
        if obj:return None,['Adjective predicate with direct object requires independent analysis'],warnings
        val=LEX_ADJ.get(final['root'],final['gloss'].split(';')[0])
        be='am' if subject=='I' else 'are' if subject in ['you','they','we'] else 'is'
        if mood=='question':line=f'{be.capitalize()} {subject.lower()} {"not " if neg else ""}{val}?'
        else:line=f'{subject} {be} {"not " if neg else ""}{val}'+(' '+ ' '.join(obliques) if obliques else '')+'.'
    else:
        root=final['root']
        if root not in LEX_VERBS:return None,[f'Verb {root} not yet assigned a validated English valency frame'],warnings
        base,transitive=LEX_VERBS[root]
        if not transitive and obj:return None,[f'{root} is not licensed with an object by the curated mapping'],warnings
        # This verifies morphosyntax, not all contexts.
        try:aux,verb=_verb_forms(base,subject,final['features'],neg,mood=='question')
        except ValueError as e:return None,[str(e)],warnings
        if root in ('shiroawe','përoa') and obj:
            complements=' to '+' and '.join(obj)
        elif root=='shiri' and obj:
            complements=' '+' and '.join(obj)
        else:complements=(' '+' and '.join(obj)) if obj else ''
        if obliques:complements+=' '+' '.join(obliques)
        if adv:complements+=' '+ ' '.join(adv)
        if mood=='question':
            if not aux:aux='do'
            line=f'{aux.capitalize()} {subject.lower()} {verb}{complements}?'
        elif mood=='command':
            if subject not in ('you','I'):return None,['Commands with non-addressee subjects need review'],warnings
            line=('Do not ' if neg else '')+(base if neg else base.capitalize())+complements+'!'
        elif aux:line=f'{subject} {aux} {verb}{complements}.'
        else:line=f'{subject} {verb}{complements}.'
    if evidential: warnings.append('Source-of-evidence particle '+evidential+' is not translated as factual certainty.')
    if subject=='they' and subfeat.get('number') is None:warnings.append('Singular sa uses they in English; antecedent may be context dependent.')
    return line,errors,warnings


def parse_qaroshi(text:str) -> dict:
    s=unicodedata.normalize('NFC',text).strip();ts=words(s);errors=[];warnings=[]
    result={'source':s,'direction':'qaroshi_to_english','translation':None,'confidence':'unresolved',
            'errors':errors,'warnings':warnings,'coverage':'finite SOV clause subset with selected subordination and morphology','analysis':[]}
    if not ts:errors.append('Empty input');return result
    if ts[0] not in RESONANCES:errors.append('Complete independent sentence must begin with one written resonance.');return result
    source_examples=CORPUS_Q.get(_norm_sentence(s),[])
    if source_examples:
        exemplar=source_examples[0]
        result['translation']=exemplar['english']
        result['confidence']='exact source-reference example (controlled, not speaker-attested)'
        result['source_example_ids']=[r['id'] for r in source_examples]
        result['evidential']=ts[-1] if ts[-1] in ('si','hu','ye') else (ts[-2] if len(ts)>1 and ts[-2] in ('si','hu','ye') else None)
        result['mood']='question' if ts[-1]=='he' else 'command' if ts[-1]=='ya' else 'statement'
        result['alternatives']=[r['english'] for r in source_examples if r['english']!=exemplar['english']]
        result['resonance']={'form':ts[0],'stance':RESONANCES[ts[0]]}
        result['analysis']=[word_analysis(w) if w not in FUNCTIONS and w not in CONNECTORS and w not in RESONANCES else {'surface':w,'functional':True} for w in ts]
        result['warnings'].append('Exact reference example; translation may depend on that example context. Not speaker attestation.')
        return result
    result['resonance']={'form':ts[0],'stance':RESONANCES[ts[0]]}
    core=ts[1:]
    if not core:errors.append('Resonance without proposition');return result
    mood=None
    if core[-1]=='he':mood='question';core.pop()
    elif core[-1]=='ya':mood='command';core.pop()
    elif s.endswith('?'):errors.append('Polar question requires terminal he');return result
    if core and core[-1] in ('si','hu','ye'):
        evidential=core.pop()
    else:evidential=None
    if core and core[-1] in ('si','hu','ye'):
        errors.append('Multiple evidential particles or invalid evidential scope');return result
    if not core:errors.append('Missing predicate');return result
    result['mood']=mood or 'statement';result['evidential']=evidential
    # If/when clauses may precede the main assertion. Avoid asserting the condition itself.
    if core[0]=='wë' and ',' in s:
        sub=core[1:];i=next((k for k in range(1,len(sub)) if k and sub[k] in ('mi','ti','sa','naru','muru') and sub[k-1] not in ('nu',)),None)
        if i is None:errors.append('Conditional main clause boundary ambiguous');return result
        left,right=sub[:i],sub[i:]
        ls,le,lw=_render_clause(left);rs,re,rw=_render_clause(right,mood,evidential)
        if le or re:errors.extend(le+re);return result
        condition=ls.rstrip('.').lower().replace(' will ', ' are going to ')
        result['translation']=f'If {condition}, {rs[0].lower()+rs[1:]}'
        result['confidence']='editorial parse, conditional-boundary heuristic';warnings.extend(lw+rw)
    else:
        left,c,right=_split_clause(core)
        if c:
            ls,le,lw=_render_clause(left)
            rs,re,rw=_render_clause(right,mood,evidential)
            if le or re:errors.extend(le+re);return result
            result['translation']=ls.rstrip('.')+' '+CONNECTORS[c]+' '+rs[0].lower()+rs[1:]
            result['confidence']='limited clause-linking interpretation';warnings.extend(lw+rw)
        else:
            line,le,lw=_render_clause(core,mood,evidential)
            if le:errors.extend(le);return result
            result['translation']=line;result['confidence']='rule-based controlled interpretation';warnings.extend(lw)
    if result['translation']:
        result['translation']=result['translation'][0].upper()+result['translation'][1:]
    result['analysis']=[word_analysis(w) if w not in FUNCTIONS and w not in CONNECTORS and w not in RESONANCES else {'surface':w,'functional':True} for w in ts]
    warnings.append('Resonance is interpersonal stance, not part of the core proposition.')
    if evidential: warnings.append('Evidential '+evidential+' indicates source of knowledge, not truth.')
    return result


EN_VERBS={english:(q,trans) for q,(english,trans) in LEX_VERBS.items()}
EN_NOUNS={english:(q,kind) for q,(english,kind) in LEX_NOUNS.items()}
EN_ADJS={english:q for q,english in LEX_ADJ.items()}

def _english_nom(text:str,case:str|None=None):
    t=text.strip().lower();t=re.sub(r'^(a|an|the)\s+','',t)
    if t in EN_PRON:return EN_PRON[t]+(('-'+case) if case else '')
    if t in ('me','us','them'):
        return {'me':'mi','us':'naru','them':'sa'}[t]+(('-'+case) if case else '')
    plural=False
    if t.endswith('s') and t[:-1] in EN_NOUNS:t=t[:-1];plural=True
    if t not in EN_NOUNS:return None
    q=EN_NOUNS[t][0]+('-ri' if plural else '')
    return q+('-'+case if case else '')


def generate_qaroshi(text:str, resonance:str='sen')->dict:
    """English-to-Qaroshi explicitly licensed templates with ability/permission distinct."""
    original=text.strip();s=re.sub(r'[.!?]+$','',original.lower().strip());s=re.sub(r'\s+',' ',s)
    if resonance not in RESONANCES:return {'source':original,'translation':None,'errors':['Unknown resonance marker'],'confidence':'unresolved'}
    # Productive simple patterns, not unrestricted translation.
    references=CORPUS_EN.get(_norm_sentence(original),[])
    # Prefer the requested resonance when an exact source example has it.
    reference=next((x for x in references if x['qaroshi'].split()[0]==resonance),None)
    if reference:
        return {'source':original,'translation':reference['qaroshi'],
                'resonance':resonance,'confidence':'exact controlled reference example',
                'source_example_id':reference['id'],'errors':[],
                'warnings':['Exact parallel example, not an independently attested fluent translation.']}
    r={'source':original,'translation':None,'direction':'english_to_qaroshi',
       'resonance':resonance,'confidence':'unresolved','errors':[],'warnings':['Default neutral sen may not match the intended interpersonal stance.']}
    adj=re.fullmatch(r'(i|you|we|they) (am|are) (not )?(well|cute|dry|tired)',s)
    if adj:
        subj,_,negative,val=adj.groups();q=EN_PRON[subj];root=EN_ADJS[val];r['translation']=f'{resonance} {q} '+('nu ' if negative else '')+root+('.' if not original.endswith('?') else '?')
        r['confidence']='controlled adjective template';return r
    poss=re.fullmatch(r'my (throat|home|friend) is (dry|cute|well|tired)',s)
    if poss:
        noun,adj=poss.groups();r['translation']=f'{resonance} mi-na {EN_NOUNS[noun][0]} {EN_ADJS[adj]}.';r['confidence']='controlled possessive template';return r
    question=original.endswith('?')
    # Subject+verb parse: keep ability vs permission vs obligation explicit.
    m=re.fullmatch(r'(i|you|we|they) (will |can |may |must |did |do not |did not |will not |cannot |may not |must not )?(fly|drink|protect|see|speak|cherish|rest|stay|have|help|give|send|write|read|ask|learn|teach|repair)(?: (.+))?',s)
    if m:
        subj,aux,verb,obj=m.groups();aux=(aux or '').strip();qverb,trans=EN_VERBS[verb]
        if not trans and obj:r['errors'].append(f'Verb {verb} does not take a direct object in the curated pattern');return r
        if (subj=='i' and obj=='me') or (subj=='you' and obj=='you') or (subj=='we' and obj=='us') or (subj=='they' and obj=='them'):
            r['errors'].append('Coreferential object needs a separate reflexive construction, not the plain object pronoun');return r
        if trans and not obj:r['errors'].append('A direct-object verb requires an object in this template');return r
        surface=''
        if obj:
            qobj=_english_nom(obj,'m')
            if not qobj:r['errors'].append('Unresolved object phrase '+obj);return r
            surface=qobj+' '
        mods={'will':'-yu','can':'-ki','may':'-ho','must':'-du','did':'-te','will not':'-yu','did not':'-te','cannot':'-ki','may not':'-ho','must not':'-du','do not':''}
        if aux not in mods and aux:r['errors'].append('Unsupported auxiliary '+aux);return r
        suff=mods.get(aux,'');neg='nu ' if aux.endswith('not') or aux=='cannot' else ''
        if question:r['warnings'].append('For polar questions, use an explicit interrogative template beginning with Can/May/Did/Will.')
        r['translation']=f'{resonance} {EN_PRON[subj]} {surface}{neg}{qverb}{suff}.'
        if aux=='did':r['warnings'].append('English emphatic did is rendered only as past tense; emphasis is not encoded in this template.')
        r['confidence']='controlled SOV transitive/intransitive template';return r
    q=re.fullmatch(r'(can|may|must|will|did|do) (i|you|we|they) (fly|drink|protect|see|speak|cherish|rest|stay|help|give|send|write|read|ask|learn|teach|repair)(?: (.+))?',s)
    if q and question:
        aux,subj,verb,obj=q.groups();qverb,trans=EN_VERBS[verb]
        if trans and not obj:r['errors'].append('Object is required for this verb');return r
        if not trans and obj:r['errors'].append('Object is not supported for this verb');return r
        object_=_english_nom(obj,'m')+' ' if obj and _english_nom(obj,'m') else ''
        if obj and not object_:r['errors'].append('Unknown object '+obj);return r
        suff={'can':'-ki','may':'-ho','must':'-du','will':'-yu','did':'-te','do':''}[aux]
        r['translation']='hë '+EN_PRON[subj]+' '+object_+qverb+suff+' he?'
        r['confidence']='controlled interrogative template';r['resonance']='hë';return r
    r['errors'].append('Construction outside validated English grammar subset; no Qaroshi sentence invented.')
    return r


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('text');p.add_argument('--direction',choices=['to-en','to-qr'],default='to-en');p.add_argument('--resonance',default='sen');p.add_argument('--json',action='store_true')
    a=p.parse_args();r=parse_qaroshi(a.text) if a.direction=='to-en' else generate_qaroshi(a.text,a.resonance)
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
