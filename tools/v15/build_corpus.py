#!/usr/bin/env python3
"""Build Qaroshi 15 independently drafted editorial corpus with transparent provenance.
No template recombination is counted as a new independent dialogue.
"""
from pathlib import Path
import sys,json,csv,re,hashlib,collections
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'tools/v14')]
from phonetics import ipa_text,sound_out_text
from semantic_validator import validate_sentence
DEST=ROOT/'corpus/v15'

def parse_file(name,kind):
    lines=(DEST/name).read_text(encoding='utf8').splitlines()
    out=[];cur=None
    for lineno,line in enumerate(lines,1):
        line=line.strip()
        if not line or line.startswith('#'):continue
        if line.startswith('@ '):
            parts=[x.strip() for x in line[2:].split('|')]
            assert len(parts)==3, (name,lineno,line)
            title,genre,premise=parts
            cur={'id':f'q15-{len(out)+1:03d}', 'title':title,'genre':genre,'premise':premise,'kind':kind,'provenance':'independently drafted editorial Qaroshi; NOT speaker attested','lines':[]}
            out.append(cur)
        else:
            assert cur is not None,(name,lineno)
            p=line.split('|')
            if kind=='dialogue':
                assert len(p)==3,(name,lineno,line)
                speaker,q,en=[s.strip() for s in p]
                assert speaker in {'A','B','C'}, (name,lineno)
            else:
                assert len(p)==2,(name,lineno,line)
                speaker='NARRATOR';q,en=[s.strip() for s in p]
            result=validate_sentence(q,en)
            findings=result['findings']
            cur['lines'].append({'id':cur['id']+f'.{len(cur["lines"])+1:02d}', 'speaker':speaker,'qaroshi':q,'english_contextual':en,
                                 'ipa':ipa_text(q),'sound_out':sound_out_text(q),
                                 'surface_pass':result['valid_surface'],
                                 'findings':[f['rule_id'] for f in findings],
                                 'review_state':'editorial draft; not human adjudicated'})
    return out

DS=parse_file('new_scenes.txt','dialogue')+parse_file('additional_scenes.txt','dialogue');TEXT=parse_file('new_texts.txt','literature')
for i,p in enumerate(DS,1):
    p['id']=f'q15-{i:03d}'
    for j,l in enumerate(p['lines'],1):l['id']=p['id']+f'.{j:02d}'
assert len(DS)>=45 and len(TEXT)>=10
for p in DS:assert len(p['lines'])>=5,(p['title'],len(p['lines']))
for p in TEXT:assert len(p['lines'])>=8,(p['title'],len(p['lines']))
assert len({p['title'].casefold() for p in DS+TEXT})==len(DS+TEXT)
# Collision-free identifiers between separate authoring sets.
for i,p in enumerate(TEXT,1):
    old=p['id'];p['id']=f'q15t-{i:03d}'
    for j,l in enumerate(p['lines'],1):l['id']=p['id']+f'.{j:02d}'
rows=[]
for piece in DS+TEXT:
    for i,l in enumerate(piece['lines'],1):
        rows.append({'source_id':l['id'],'piece_id':piece['id'],'title':piece['title'],'genre':piece['genre'],'kind':piece['kind'],'premise':piece['premise'],
                     'turn':i,'speaker':l['speaker'],'qaroshi':l['qaroshi'],'english_contextual':l['english_contextual'],
                     'ipa':l['ipa'],'sound_out':l['sound_out'],'surface_pass':str(l['surface_pass']).lower(),
                     'rule_ids':';'.join(l['findings']),'review_state':l['review_state'],'source_type':'15.0 separate editorial writing'})
with (DEST/'corpus_rows.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(DEST/'pieces.json').write_text(json.dumps(DS+TEXT,ensure_ascii=False,indent=2),encoding='utf8')
report=[]
for r in rows:
    if r['rule_ids'] or r['surface_pass']!='true':
        report.append({k:r[k] for k in ['source_id','qaroshi','english_contextual','kind','rule_ids','surface_pass']})
with (DEST/'editorial_review_queue.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=list(report[0]) if report else list(rows[0]));w.writeheader();w.writerows(report)
# Word count on Qaroshi ONLY. Defining whitespace tokens as reproducible tokenization.
q_tokens=[tok for x in rows for tok in x['qaroshi'].strip().split()]
wordlike=[re.sub(r'^[^A-Za-zëË]+|[^A-Za-zëË?.!]+$','',t) for t in q_tokens]
tokens=sum(bool(t) for t in wordlike)
counts=collections.Counter(f for r in rows for f in r['rule_ids'].split(';') if f)
manifest={'edition':'15.0 Natural Conversation & Literature','new_independently_scripted_editorial_dialogues':len(DS),
          'new_independently_scripted_editorial_texts':len(TEXT),'new_dialogue_turns':sum(len(p['lines']) for p in DS),
          'new_literature_sentences':sum(len(p['lines']) for p in TEXT),'new_source_language_tokens_whitespace':tokens,
          'new_unique_sentence_forms':len({r['qaroshi'] for r in rows}),'new_distinct_genre_labels':len({p['genre'] for p in DS+TEXT}),
          'surface_valid':sum(x['surface_pass']=='true' for x in rows),'surface_errors':sum(x['surface_pass']!='true' for x in rows),
          'review_flagged_rows':len(report),'rule_counts':dict(counts),'speaker_attestations':0,'human_semantic_approvals':0,
          'claim_limits':'Editorial independently drafted pieces; formulaic sentences repeat; structural pass ≠ native fluency, idiomaticity or verified translations. Not a 100k-word natural corpus or 1,000 fully distinct speaker-reviewed dialogues.',
          'baseline_lexicon_sha256':hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest(),
          'genre_counts':dict(collections.Counter(p['genre'] for p in DS+TEXT))}
(DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
md=['# Qaroshi 15.0: independent editorial conversations and literature','','These pieces were separately scripted as new teaching/editorial writing. They are not transcribed speech, not verified native idioms, and not a naturalistic 100,000-word corpus.','']
for p in DS+TEXT:
    md += ['## '+p['title'],f'*{p["genre"]} · {p["kind"]}*',p['premise'],'']
    for l in p['lines']:
        md += [f'**{l["speaker"]}: {l["qaroshi"]}**',f'*{l["english_contextual"]}*',f'IPA `{l["ipa"]}`','']
(DEST/'Qaroshi_15_Reader.md').write_text('\n'.join(md),encoding='utf8')
print(json.dumps({k:manifest[k] for k in ['new_independently_scripted_editorial_dialogues','new_independently_scripted_editorial_texts','new_dialogue_turns','new_literature_sentences','new_source_language_tokens_whitespace','surface_valid','surface_errors','review_flagged_rows','rule_counts']},ensure_ascii=False,indent=2))
