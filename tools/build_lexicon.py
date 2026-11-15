#!/usr/bin/env python3
"""Reproducible Qaroshi 2.0 lexicon edition builder.

Baseline spellings are immutable. Expansion concepts are editorially curated,
but their generated Roman spellings are candidate vocabulary pending review.
"""
from __future__ import annotations
import csv, hashlib, json, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source'))
from curated_terms import AREAS
from functional_v2 import FUNCTIONS

ONSET = ['k','w','t','r','q','d','sh','z','g','kh','zh','ng','h','b','p','m','s','n','y','l']
VOWELS = ['a','e','i','o','u','ë']
FINAL_VOWELS = {'n':['a','o'],'v':['i','u'],'adj':['e','ë'],'adv':['e','ë']}
CORE_CSV = ROOT/'source/Qaroshi_Dictionary_853.csv'
OUT_CSV = ROOT/'data/lexicon.csv'
OUT_JSON = ROOT/'data/lexicon.json'


def norm(s: str) -> str:
    return unicodedata.normalize('NFC',s.strip())


def english_aliases(s):
    return [norm(x).lower() for x in re.split(r';',s) if x.strip()]


def stable_hash(key):
    return hashlib.sha256(key.encode('utf-8')).digest()


def new_stem(domain, pos, concept, prefix, used):
    endings = FINAL_VOWELS[pos]
    for attempt in range(100_000):
        h = stable_hash(f'Qaroshi-v2|{domain}|{pos}|{concept}|{attempt}')
        c1 = ONSET[int.from_bytes(h[0:2],'big')%len(ONSET)]
        v1 = VOWELS[int.from_bytes(h[2:4],'big')%len(VOWELS)]
        c2 = ONSET[int.from_bytes(h[4:6],'big')%len(ONSET)]
        v2 = endings[int.from_bytes(h[6:8],'big')%len(endings)]
        proposed = prefix + c1 + v1 + c2 + v2
        # Avoid ugly repeated syllables in a lexical root.
        if (prefix==c1+v1 or c1+v1==c2+v2 or proposed in used or proposed.startswith('nunu')):
            continue
        return proposed
    raise RuntimeError(f'No candidate for {concept}')


def build():
    with CORE_CSV.open(encoding='utf-8-sig', newline='') as f:
        original = list(csv.DictReader(f))
    assert len(original) == 853, len(original)
    result=[]
    used=set()
    keys=set()
    reverse=defaultdict(list)
    for r in original:
        w=norm(r['qaroshi'])
        if w in used:
            raise ValueError(f'duplicate original headword: {w}')
        used.add(w)
        item = {'qaroshi':w,'pos':r['pos'],'english':norm(r['english']),
                'domain':norm(r['domain']),'note':norm(r['note']),
                'type':'headword','edition':'1.0','review':'established',
                'components':''}
        result.append(item)
        for k in english_aliases(item['english']):
            reverse[(k,item['pos'])].append(w)
            keys.add((k,item['pos']))
    # Standardized grammatical vocabulary is a fixed small class, not generated roots.
    for word,pos,gloss,note in FUNCTIONS:
        word=norm(word)
        if word in used: raise ValueError('new grammatical form collides with source: '+word)
        used.add(word)
        item={'qaroshi':word,'pos':pos,'english':gloss,'domain':'Grammar extension 2.0',
              'note':note,'type':'function word','edition':'2.0','review':'standardized',
              'components':''}
        result.append(item)
        for key in english_aliases(gloss):
            reverse[(key,pos)].append(word)
            keys.add((key,pos))
    domains=sorted(set(domain for domain,_,_ in AREAS))
    prefix_options = [c+v for c in ONSET for v in VOWELS if c+v not in used]
    prefix_file=ROOT/'data/domain_prefixes.json'
    prefixes=json.loads(prefix_file.read_text(encoding='utf-8')) if prefix_file.exists() else {}
    for domain in domains:
        if domain not in prefixes:
            available=[x for x in prefix_options if x not in prefixes.values()]
            if not available:raise ValueError('exhausted lexical family prefixes')
            prefixes[domain]=available[0]
    if len(set(prefixes.values())) < len(prefixes):
        raise ValueError('prefix collision')
    prefix_file.write_text(json.dumps(prefixes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lock_file=ROOT/'data/lexicon_lock.json'
    old_lock=json.loads(lock_file.read_text(encoding='utf-8')) if lock_file.exists() else {}
    skipped=Counter()
    for domain,pos,concepts in AREAS:
        for text in concepts:
            concept = norm(text)
            alias=(concept.lower(),pos)
            if alias in keys:
                skipped['already covered or duplicate sense']+=1
                continue
            lock_key=f'{domain}\t{pos}\t{concept}'
            prior=old_lock.get(lock_key)
            spelling=prior['qaroshi'] if prior else new_stem(domain,pos,concept,prefixes[domain],used)
            if spelling in used:raise ValueError('locked form collision: '+spelling)
            used.add(spelling); keys.add(alias)
            item={'qaroshi':spelling,'pos':pos,'english':concept,
                  'domain':domain,'note':'Modern Qaroshi terminology; scope is the English gloss shown.',
                  'type':prior.get('type','headword') if prior else 'headword',
                  'edition':'2.0','review':'candidate',
                  'components':prior.get('components','') if prior else ''}
            if item['type']=='compound':item['note']='Transparent modifier–head compound: '+item['components']
            result.append(item)
            reverse[alias].append(spelling)
    # Build readable compounds only when BOTH parts have independent lexical senses.
    # A two-part noun compound has a noun head. The left part may be a noun or adjective.
    compounds=0
    words={r['qaroshi']:r for r in result}
    for item in result:
        if item['edition']!='2.0' or item['pos']!='n' or item['type']=='compound':
            continue
        concept = item['english'].lower()
        if '(' in concept or ')' in concept or '/' in concept or '-' in concept:
            continue
        parts=concept.split(' ')
        if len(parts)!=2:
            continue
        modifier,head=parts
        # Prefer an exact base of the correct word class, not a similar English string.
        head_entries = reverse.get((head,'n'),[])
        mod_entries = reverse.get((modifier,'n'),[]) + reverse.get((modifier,'adj'),[])
        if not head_entries or not mod_entries:
            continue
        left=min(mod_entries,key=len)
        right=min(head_entries,key=len)
        if left==item['qaroshi'] or right==item['qaroshi']:
            continue
        composed=left+right
        if len(composed)>21 or composed in used:
            continue
        used.remove(item['qaroshi']); used.add(composed)
        words.pop(item['qaroshi'],None)
        # Fix reverse lookup for this exact sense.
        reverse[(concept,'n')]=[composed]
        item['qaroshi']=composed
        item['type']='compound'
        item['components']=left+' + '+right
        item['note']='Transparent modifier–head compound: '+left+' + '+right
        words[composed]=item
        compounds+=1
    # Exact invariants and canonical phrase spelling.
    assert len(set(r['qaroshi'] for r in result))==len(result)
    for canonical in ('qaroshi','më','zha','qor','pëla','ti','sëna','nu','zëru','ya','ko','mi','nëra'):
        assert canonical in {r['qaroshi'] for r in result},canonical
    # Persist headword spellings so new terminology cannot silently rename an
    # already documented word on a later rebuild.
    lock={f"{r['domain']}\t{r['pos']}\t{r['english']}":
          {'qaroshi':r['qaroshi'],'type':r['type'],'components':r['components']}
          for r in result if r['review']=='candidate'}
    lock_file.write_text(json.dumps(lock,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    result.sort(key=lambda x:x['qaroshi'])
    for i,item in enumerate(result,1): item['id']=f'Q{i:06d}'
    cols=['id','qaroshi','pos','english','domain','type','edition','review','components','note']
    OUT_CSV.parent.mkdir(parents=True,exist_ok=True)
    with OUT_CSV.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader();writer.writerows(result)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    stats={'original_entries':len(original),'expanded_entries':len(result)-len(original),
           'total_entries':len(result),'new_compounds':sum(r['type']=='compound' for r in result),
           'candidate_headwords':sum(r['review']=='candidate' and r['type']=='headword' for r in result),
           'fixed_new_function_words':len(FUNCTIONS),
           'domains':dict(sorted(Counter(r['domain'] for r in result).items())),
           'parts_of_speech':dict(sorted(Counter(r['pos'] for r in result).items())),
           'skipped_curated_duplicates':dict(skipped),
           'status_explanation':{
             'established':'Preserved verbatim from Standard Reference 1.0',
             'candidate':'Edition 2.0 lexical expansion pending community review; not a corpus-attested word',
             'standardized':'Explicitly documented grammatical marker in edition 2.0',
           }}
    (ROOT/'data/statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'total':len(result),'new':len(result)-len(original),'compounds':sum(r['type']=='compound' for r in result),'skipped':skipped},ensure_ascii=False))
    return result

if __name__=='__main__': build()
