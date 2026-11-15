#!/usr/bin/env python3
"""Build Standard Reference 3.0 without reassigning any 2.0 headword or ID.

New concepts are curated English senses; generated Qaroshi spellings are
**candidate forms**, not attested linguistic usage. Lock file fixes output.
"""
from __future__ import annotations
import csv, hashlib, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
from curated_terms_v3 import iter_concepts
from functional_v3 import FUNCTIONS_V3
BASE=ROOT/'source/lexicon_v2_snapshot.csv'
OUT=ROOT/'data/lexicon.csv'
ONSETS=['k','w','t','r','q','d','sh','z','g','kh','zh','ng','h','b','p','m','s','n','y','l']
VOWELS=['a','e','i','o','u','ë']
FINAL={'n':['a','o'],'v':['i','u'],'adj':['e','ë'],'adv':['e','ë']}
COLS=['id','qaroshi','pos','english','domain','type','edition','review','components','note']

def nfc(s):return unicodedata.normalize('NFC',s.strip())
def key(gloss,pos):return (nfc(gloss).lower(),pos)

def make_stem(domain,pos,gloss,prefix,used):
    for attempt in range(100000):
        b=hashlib.sha256(f'QAROSHI|3.0|{domain}|{pos}|{gloss}|{attempt}'.encode()).digest()
        a=ONSETS[int.from_bytes(b[0:2],'big')%len(ONSETS)]
        v=VOWELS[int.from_bytes(b[2:4],'big')%len(VOWELS)]
        c=ONSETS[int.from_bytes(b[4:6],'big')%len(ONSETS)]
        last=FINAL[pos][int.from_bytes(b[6:8],'big')%len(FINAL[pos])]
        w=prefix+a+v+c+last
        if w not in used and prefix!=a+v and a+v!=c+last:
            return w
    raise ValueError('lexeme space exhausted')

def run():
    with BASE.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==6819, f'Expected authoritative 2.0 snapshot; got {len(rows)}'
    assert all(tuple(r)==tuple(COLS) for r in rows)
    base={r['qaroshi']:r.copy() for r in rows}
    assert len(base)==len(rows)
    used=set(base)
    english_keys={key(k,r['pos']) for r in rows for k in r['english'].split(';') if k.strip()}
    sk=Counter(); skipped_rows=[]
    lockfile=ROOT/'data/lexicon_lock_v3.json'
    lock=json.loads(lockfile.read_text(encoding='utf-8')) if lockfile.exists() else {}
    # Explicitly specified grammar forms: reviewed independently of generated roots.
    new_fixed=[]
    for i,(form,pos,gloss,rule) in enumerate(FUNCTIONS_V3,1):
        assert form not in used, f'Grammar form collision: {form}'
        used.add(form)
        new_fixed.append({'id':f'Q3F{i:04d}','qaroshi':form,'pos':pos,'english':gloss,
             'domain':'Grammar extension 3.0','type':'function word','edition':'3.0','review':'proposed',
             'components':'','note':rule})
        for alias in gloss.split(';'): english_keys.add(key(alias,pos))
    rows+=new_fixed
    # Each V3 semantic category gets a stable, non-overlapping first syllable.
    old_prefixes=json.loads((ROOT/'data/domain_prefixes.json').read_text(encoding='utf-8'))
    all_prefixes=[a+v for a in ONSETS for v in VOWELS]
    available=[p for p in all_prefixes if p not in old_prefixes.values()]
    domain_names=sorted({d for d,p,g in iter_concepts()})
    prefixes={d:available[i] for i,d in enumerate(domain_names)}
    (ROOT/'data/domain_prefixes_v3.json').write_text(json.dumps(prefixes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    new=[];new_lock={}
    seen_keys=set()
    for domain,pos,gloss in iter_concepts():
        concept=nfc(gloss)
        alias=key(concept,pos)
        if alias in english_keys:
            sk['existing English sense or repeated 3.0 sense']+=1
            skipped_rows.append({'domain':domain,'pos':pos,'english':concept,'reason':'existing/repeated sense'})
            continue
        if alias in seen_keys:
            sk['duplicate in 3.0 inventory']+=1
            skipped_rows.append({'domain':domain,'pos':pos,'english':concept,'reason':'duplicate inventory'})
            continue
        seen_keys.add(alias)
        lk=f'{domain}\t{pos}\t{concept}'
        word=lock.get(lk,{}).get('qaroshi') or make_stem(domain,pos,concept,prefixes[domain],used)
        if word in used:raise ValueError('Lexical collision, including with frozen form: '+word)
        used.add(word);english_keys.add(alias)
        item={'id':'Q3L'+hashlib.sha256(lk.encode('utf-8')).hexdigest()[:12].upper(),'qaroshi':word,'pos':pos,'english':concept,
              'domain':domain,'type':'headword','edition':'3.0','review':'candidate',
              'components':'','note':'Specialized semantic entry; editorially specified sense, candidate form pending review.'}
        new.append(item);new_lock[lk]={'qaroshi':word}
    assert not (set(base)&{r['qaroshi'] for r in new})
    rows.extend(new)
    rows.sort(key=lambda r:(r['qaroshi'],r['id']))
    assert len(rows)==len({r['qaroshi'] for r in rows})
    for word,orig in base.items():
        curr=next(r for r in rows if r['qaroshi']==word)
        assert curr==orig, f'Mutated canonical entry {word}'
    lockfile.write_text(json.dumps(new_lock,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    with OUT.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,COLS);writer.writeheader();writer.writerows(rows)
    (ROOT/'data/lexicon.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (ROOT/'data/v3_lexical_review_queue.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=COLS);writer.writeheader();writer.writerows(new)
    with (ROOT/'data/v3_skipped_senses.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['domain','pos','english','reason']);writer.writeheader();writer.writerows(skipped_rows)
    stats={'prior_reference_entries':len(base),'prior_core_entries':853,'prior_v2_entries':len(base)-853,
           'v3_new_grammar_forms':len(new_fixed),'v3_new_lexical_candidates':len(new),
           'v3_specifications_considered':sum(1 for _ in iter_concepts()),
           'v3_skipped_overlap':len(skipped_rows),'total_entries':len(rows),
           'review_counts':dict(Counter(r['review'] for r in rows)),
           'edition_counts':dict(Counter(r['edition'] for r in rows)),
           'domains':dict(sorted(Counter(r['domain'] for r in rows).items())),
           'v3_domain_counts':dict(sorted(Counter(r['domain'] for r in new).items())),
           'parts_of_speech':dict(sorted(Counter(r['pos'] for r in rows).items())),
           'note':'3.0 lexical spellings are candidates; count is entries, not evidence of natural-language parity.'}
    (ROOT/'data/statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('3.0: ',json.dumps({'base':len(base),'new_grammar':len(new_fixed),'new_candidate_lexemes':len(new),'duplicates_skipped':len(skipped_rows),'total':len(rows)},ensure_ascii=False))
    return rows

if __name__=='__main__':run()
