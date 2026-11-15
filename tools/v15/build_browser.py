#!/usr/bin/env python3
"""Build one self-contained offline corpus browser. No external assets, network calls, or font binaries."""
import json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def rows(path):
 with (ROOT/path).open(encoding='utf8') as f:return list(csv.DictReader(f))
pieces=[]
for x in load('corpus/original11/dialogues.json'):
    pieces.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':'earlier editorial dialogue','kind':'dialogue','release':'11.0','provenance':'11.0 editorial, not attested','lines':[{'speaker':r['speaker'],'qaroshi':r['qaroshi'],'english_contextual':r['english'],'ipa':r.get('ipa','')} for r in x['turns']]})
for x in load('corpus/v12_13/dialogues_12.json'):
    pieces.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':'earlier editorial dialogue','kind':'dialogue','release':'12–13','provenance':'12.0 editorial, not attested','lines':[{'speaker':r['speaker'],'qaroshi':r['qaroshi'],'english_contextual':r['english_editorial'],'ipa':r.get('ipa','')} for r in x['turns']]})
for x in load('corpus/v12_13/anthology_12.json'):
    pieces.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':x['genre'],'kind':'literature','release':'12–13','provenance':'12.0 editorial, not attested','lines':[{'speaker':'N','qaroshi':r['qaroshi'],'english_contextual':r['english_editorial'],'ipa':r.get('ipa','')} for r in x['sentences']]})
for x in load('corpus/curated/short_readings.json'):
    pieces.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':'earlier editorial reading','kind':'literature','release':'13.0','provenance':'editorial, not attested','lines':[{'speaker':'N','qaroshi':r['qaroshi'],'english_contextual':r['english'],'ipa':r.get('ipa','')} for r in x['sentences']]})
for x in load('corpus/v15/pieces.json'):
    pieces.append({'id':x['id'],'title':x['title'],'premise':x['premise'],'genre':x['genre'],'kind':x['kind'],'release':'15.0','provenance':x['provenance'],'lines':[{'speaker':r['speaker'],'qaroshi':r['qaroshi'],'english_contextual':r['english_contextual'],'ipa':r.get('ipa','')} for r in x['lines']]})
assert len({x['id'] for x in pieces})==len(pieces),'Duplicate piece IDs'
# Export the same corpus as portable aligned UTF-8 for downstream research.
catalog=[];aligned=[];source_only=[]
for piece in pieces:
    tokens=sum(len(line['qaroshi'].split()) for line in piece['lines'])
    catalog.append({'piece_id':piece['id'],'title':piece['title'],'release':piece['release'],'kind':piece['kind'],
                    'genre':piece['genre'],'premise':piece['premise'],'lines':len(piece['lines']),
                    'qaroshi_source_whitespace_tokens':tokens,'speaker_attested':'no'})
    source_only.append(f"# {piece['title']} [{piece['id']}] ({piece['release']})")
    for number,line in enumerate(piece['lines'],1):
        aligned.append({'piece_id':piece['id'],'release':piece['release'],'genre':piece['genre'],'line':number,
                        'speaker':line.get('speaker','N'),'qaroshi':line['qaroshi'],'english_contextual':line['english_contextual'],
                        'ipa':line.get('ipa',''),'source_status':'editorial writing, not speaker-attested'})
        source_only.append(line['qaroshi'])
    source_only.append('')
for file,records in [('editorial_piece_catalog.csv',catalog),('full_editorial_parallel.csv',aligned)]:
    with (ROOT/'corpus/v15'/file).open('w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
(ROOT/'corpus/v15/all_editorial_qaroshi_only.txt').write_text('\n'.join(source_only),encoding='utf8')
token_stats={}
for c in catalog:
    rel=c['release'];token_stats.setdefault(rel,0);token_stats[rel]+=c['qaroshi_source_whitespace_tokens']
(ROOT/'corpus/v15/cumulative_manifest.json').write_text(json.dumps({'total_piece_count':len(pieces),'editorial_dialogues':sum(x['kind']=='dialogue' for x in pieces),
 'editorial_literature':sum(x['kind']=='literature' for x in pieces), 'total_source_language_whitespace_tokens':sum(token_stats.values()),
 'tokens_by_release':token_stats,'aligned_lines':len(aligned),'speaker_attested_lines':0,
 'excluded_from_independent_counts':'Earlier 1,000 controlled template variants / 123,000 tokens are retained elsewhere but excluded',
 'caveat':'Editorial source-language tokens count, NOT empirically naturalistic/independently speaker-attested words'},ensure_ascii=False,indent=2),encoding='utf8')
lex=[[x['qaroshi'],x['english'],x['pos'],x['ipa']] for x in rows('data/lexicon.csv')]
manifest=load('corpus/v15/manifest.json')
stats={'dialogues':sum(x['kind']=='dialogue' for x in pieces),'literature':sum(x['kind']=='literature' for x in pieces),
       'newTokens':manifest['new_source_language_tokens_whitespace'],'newLines':manifest['new_dialogue_turns']+manifest['new_literature_sentences'],
       'newSurfaceValid':manifest['surface_valid'],'newReviewFlags':manifest['review_flagged_rows'],
       'uniqueNew':manifest['new_unique_sentence_forms']}
obj={'pieces':pieces,'lexicon':lex,'genres':sorted({x['genre'] for x in pieces}),'releases':sorted({x['release'] for x in pieces}), 'stats':stats}
template=(ROOT/'web/v15/reader_template.html').read_text(encoding='utf8')
blob=json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=template.replace('__DATA__',blob)
out=ROOT/'Qaroshi_15_Corpus_Library.html';out.write_text(html,encoding='utf8')
(ROOT/'data/v15/browser_manifest.json').write_text(json.dumps({'included_editorial_pieces':len(pieces),'dialogues':stats['dialogues'],'literature':stats['literature'],'lexicon_entries':len(lex),'size_bytes':out.stat().st_size,'no_network':True,'no_fonts_embedded':True},indent=2),encoding='utf8')
print('Browser: pieces',len(pieces),'dialogues',stats['dialogues'],'literature',stats['literature'],'size',out.stat().st_size)
