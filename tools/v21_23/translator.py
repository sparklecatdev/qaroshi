#!/usr/bin/env python3
"""Conservative, source-evidenced Qaroshi translation and annotation.

Absolute boundaries:
- An exact documented example is not evidence of natural usage or of a
  context-free translation. Report all variants and the source provenance.
- Grammar engine output is explicitly provisional, never canonical adjudication.
- Retrieval neighbors are NOT translations, and guesswork never fills gaps.
"""
from __future__ import annotations
import argparse, csv, difflib, json, re, sys, unicodedata
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/fluency11'))
import engine


def norm(x:str)->str:
    s=unicodedata.normalize('NFC',str(x)).casefold().strip()
    return re.sub(r'[\s,;.!?]+',' ',s).strip()


def records():
    output=[]
    with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf8',newline='') as f:
        for r in csv.DictReader(f):
            output.append({'id':r['id'],'qaroshi':r['qaroshi'],'english':r['english'],
                'kind':'canonical controlled bilingual example','source':'corpus/parallel_sentences.csv',
                'ipa':r['ipa'],'sound_out':r['sound_out'],'status':'controlled teaching reference, not speaker attested'})
    for piece in json.loads((ROOT/'corpus/v15/pieces.json').read_text(encoding='utf8')):
        for line in piece['lines']:
            output.append({'id':line['id'],'qaroshi':line['qaroshi'],'english':line['english_contextual'],
                'kind':'editorial context-dependent writing','source':f"corpus/v15/pieces.json / {piece['id']}",
                'ipa':line['ipa'],'sound_out':line['sound_out'],'status':line['review_state']})
    for i,piece in enumerate(json.loads((ROOT/'corpus/v12_13/anthology_12.json').read_text(encoding='utf8')),1):
        for j,line in enumerate(piece['sentences'],1):
            output.append({'id':f'earlier-12-{i:02}-{j:02}', 'qaroshi':line['qaroshi'],
                'english':line['english_editorial'],'kind':'earlier editorial narrative',
                'source':f'corpus/v12_13/anthology_12.json / earlier-12-{i:02}',
                'ipa':line['ipa'],'sound_out':line['sound_out'],
                'status':'editorial narrative; English may expand overt source'})
    for piece in json.loads((ROOT/'corpus/curated/short_readings.json').read_text(encoding='utf8')):
        for line in piece['sentences']:
            output.append({'id':f"{piece['id']}-{line['number']}", 'qaroshi':line['qaroshi'],
                'english':line['english'],'kind':'earlier curated short reading',
                'source':f"corpus/curated/short_readings.json / {piece['id']}",
                'ipa':line['ipa'],'sound_out':line['sound_out'],
                'status':'structurally checked editorial, not speaker attested'})
    return output


@lru_cache(maxsize=1)
def indices():
    allrows=records(); qr=defaultdict(list);en=defaultdict(list);inverted=defaultdict(set)
    for i,r in enumerate(allrows):
        qr[norm(r['qaroshi'])].append(i);en[norm(r['english'])].append(i)
        for word in set(norm(r['english']+' '+r['qaroshi']).split()):
            if len(word)>2:inverted[word].add(i)
    qa=defaultdict(list)
    with (ROOT/'data/v14/translation_review_103.csv').open(encoding='utf8',newline='') as f:
        for r in csv.DictReader(f):qa[norm(r['qaroshi'])].append({
            'audit_id':r['audit_id'],'category':r['interpretation_category'],
            'reason':r['editorial_reason'],'human_approved':r['human_semantic_approved']})
    return allrows,qr,en,inverted,qa


def neighbors(query:str,limit:int=8):
    allrows,_,_,inv,_=indices();tokens={t for t in norm(query).split() if len(t)>2}
    counts=defaultdict(int)
    for t in tokens:
        for i in inv.get(t,set()):counts[i]+=1
    result=[]
    for i,score in sorted(counts.items(),key=lambda x:(-x[1],x[0]))[:80]:
        r=allrows[i];den=max(len(tokens),1)
        if score/den <.15:continue
        result.append({'id':r['id'],'qaroshi':r['qaroshi'],'english':r['english'],
            'overlapping_tokens':score,'source':r['kind'],'warning':'RELATED EXAMPLE ONLY; NOT A TRANSLATION of the query'})
        if len(result)>=limit:break
    return result


def interpret(text:str,direction:str='auto',resonance:str='sen'):
    src=unicodedata.normalize('NFC',text).strip()
    if direction not in ('auto','to-en','to-qr'):raise ValueError('direction')
    if direction=='auto':
        ts=engine.words(src)
        direction='to-en' if ts and ts[0] in engine.RESONANCES else 'to-qr'
    allrows,qr,en,_,qa=indices()
    matches=qr.get(norm(src),[]) if direction=='to-en' else en.get(norm(src),[])
    variants=[allrows[i] for i in matches]
    flagged=qa.get(norm(src),[]) if direction=='to-en' else []
    out={'query':src,'direction':direction,'status':'unresolved','translation':None,
         'variants':variants,'review_flags':flagged,'related_examples':[],
         'warnings':[],'word_analysis':[],'grammar_analysis':None,
         'policy':'No unsourced claim of fluent translation or speaker attestation'}
    if not src:
        out['warnings'].append('Input is empty.');return out
    if matches:
        preferred=variants
        if direction=='to-qr':
            preferred=[r for r in variants if r['qaroshi'].split(' ')[0]==resonance] or variants
        out['translation']=preferred[0]['english' if direction=='to-en' else 'qaroshi']
        out['status']='exact documented source match, context-sensitive'
        if len({r['english' if direction=='to-en' else 'qaroshi'] for r in variants})>1:
            out['warnings'].append('Multiple distinct documented equivalents; inspect alternatives and resonance.')
        out['warnings'].append('Original examples are controlled/editorial, not independent speaker evidence.')
        if flagged:out['warnings'].append('Existing editorial QA notes identify possible translation-context discrepancies.')
    elif direction=='to-en':
        obj=engine.parse_qaroshi(src);out['grammar_analysis']={k:v for k,v in obj.items() if k not in ('source','direction')}
        if obj.get('translation') and not obj.get('errors'):
            out['translation']=obj['translation'];out['status']='provisional grammar engine interpretation'
        else:out['warnings'].append('No licensed complete interpretation; no translation was invented.')
        out['warnings']+=obj.get('warnings',[])+obj.get('errors',[])
    else:
        obj=engine.generate_qaroshi(src,resonance=resonance)
        out['grammar_analysis']={k:v for k,v in obj.items() if k not in ('source','direction')}
        if obj.get('translation') and not obj.get('errors'):
            out['translation']=obj['translation'];out['status']='provisional constrained generation'
        else:out['warnings'].append('Outside the supported English grammar; no Qaroshi was invented.')
        out['warnings']+=obj.get('warnings',[])+obj.get('errors',[])
    if direction=='to-en':
        out['word_analysis']=[engine.word_analysis(w) if w not in engine.RESONANCES and w not in engine.FUNCTIONS and w not in engine.CONNECTORS else {'surface':w,'functional':True} for w in engine.words(src)]
    if not matches:out['related_examples']=neighbors(src)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('text');p.add_argument('--direction',choices=['auto','to-en','to-qr'],default='auto');p.add_argument('--resonance',default='sen');a=p.parse_args();print(json.dumps(interpret(a.text,a.direction,a.resonance),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
