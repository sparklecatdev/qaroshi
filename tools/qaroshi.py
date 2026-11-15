#!/usr/bin/env python3
"""Qaroshi lexicon lookup, morphological formatter, glyph renderer, and checks.

This is a conservative reference utility, not a full natural-language translator.
"""
from __future__ import annotations
import argparse, csv, json, re, unicodedata
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT=Path(__file__).resolve().parents[1]
GLYPHS=ROOT/'assets/glyphs'
LETTERS=('sh','zh','kh','ng','k','a','w','t','r','q','o','d','z','u','ë','i','g','e','h','b','p','m','s','n','y','l')
RESONANCES='më zha qor sen hë lën sur rak khar yë nëm wen dal rëm hol zher'.split()
CASES=('m','na','lo','gu','de','wa','tu','shi','nga')
VOICE=('ru','li','wo','ne')
TENSE=('te','yu')
ASPECT=('se','mo','në')
MODAL=('ki','ho','du')
NOUN_DERIV=('wë','këlë','rëma','sharo','mi','ra','ma','rë','no')


def nfc(t): return unicodedata.normalize('NFC',t)


def entries():
    with (ROOT/'data/lexicon.csv').open('r',encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def glyphs_of(s: str, strict=True):
    """Return letter names and whitespace/punctuation for a Romanized string."""
    s=nfc(s).lower()
    out=[];i=0
    while i<len(s):
        if s[i] in ' \t\n-.,;:!?«»\"\'()0123456789':
            out.append(s[i]);i+=1;continue
        match=next((g for g in LETTERS if s.startswith(g,i)),None)
        if match:
            out.append(match);i+=len(match)
        elif strict:
            raise ValueError(f'Unknown Qaroshi grapheme at position {i}: {s[i:i+12]!r}')
        else:
            out.append('�');i+=1
    return out


def format_morphology(root,pos,plural=False,case=None,topic=False,endear=False,
                      voice=None,tense=None,aspect=None,modal=None,tender=False):
    if pos=='noun':
        if any((voice,tense,aspect,modal,tender)):raise ValueError('verb endings applied to noun')
        if case and case not in CASES:raise ValueError('invalid noun case')
        pieces=[root]+(['lë'] if endear else [])+(['ri'] if plural else [])+([case] if case else [])+(['së'] if topic else [])
    elif pos=='verb':
        if any((plural,case,topic,endear)):raise ValueError('noun endings applied to verb')
        for value,group,label in ((voice,VOICE,'voice'),(tense,TENSE,'tense'),
                                  (aspect,ASPECT,'aspect'),(modal,MODAL,'modal')):
            if value and value not in group:raise ValueError('invalid '+label)
        pieces=[root]+([voice] if voice else [])+([tense] if tense else [])+([aspect] if aspect else [])+([modal] if modal else [])+(['la'] if tender else [])
    else:raise ValueError('pos must be noun or verb')
    return '-'.join(pieces)


def analyze_word(spelling,lexicon):
    """Reference analysis: exact lexicon first, then teaching hyphens.

    Without hyphens, exhaustive morphological analysis is NOT claimed.
    """
    if spelling in lexicon:return {'lexeme':spelling,'segments':[],'exact':True}
    parts=spelling.split('-')
    if len(parts)==1:return None
    root=parts[0]
    if root not in lexicon:return None
    item=lexicon[root]
    pos=item['pos']
    if pos in ('n','pron','det'):
        order={'lë':0,'ri':1,**{v:2 for v in CASES},'së':3}
    elif pos=='v':
        order={**{v:0 for v in VOICE},**{v:1 for v in TENSE},
               **{v:2 for v in ASPECT},**{v:3 for v in MODAL},'la':4}
    else:return None
    slots=[]
    for end in parts[1:]:
        if end not in order:return None
        slots.append(order[end])
    if slots!=sorted(set(slots)):return None
    return {'lexeme':root,'segments':parts[1:],'exact':False}


def check_sentence(text,lexicon):
    s=nfc(text).strip()
    found=[]
    s=s.strip('«»\" ')
    chunks=re.split(r'\s+',s)
    first=chunks[0].strip('.,!?;:\"«»').lower() if chunks else ''
    if first not in RESONANCES:
        found.append('A complete sentence must start with exactly one resonance marker.')
    if len(chunks)>1 and chunks[1].lower() in RESONANCES:
        found.append('Two consecutive sentence-initial resonance markers are not permitted.')
    for raw in chunks:
        clean=raw.strip('.,!?;:\"«»()').lower()
        if not clean:continue
        try:glyphs_of(clean)
        except ValueError as e: found.append(str(e));continue
        if not analyze_word(clean,lexicon):
            # A full analyzer would need lexicalized compounding and unhyphenated inflections.
            found.append(f'Unresolved token (not necessarily ungrammatical): {clean}')
    if ' he?' in s and ' ya' in s:
        found.append('A single clause cannot be both a direct question and an imperative.')
    return found


def render_glyphs(text,path,width=1450,height_per_line=125,font_height=80):
    """Rendered transparent-background PNG in native handwritten glyph images."""
    letter_images={}
    for g in LETTERS:
        file=GLYPHS/(g+'.png')
        if not file.exists():raise FileNotFoundError(file)
        img=Image.open(file).convert('RGBA')
        # Crop transparent edges, then use equal glyph-height scaling.
        alpha=img.getchannel('A'); box=alpha.getbbox()
        if box: img=img.crop(box)
        img.thumbnail((int(font_height*1.5),font_height),Image.Resampling.LANCZOS)
        letter_images[g]=img
    components=glyphs_of(text)
    spans=[]; x=30; y=20
    for token in components:
        if token=='\n':x=30;y+=height_per_line;continue
        if token in (' ','\t'):
            x+=38 if token==' ' else 100;continue
        if token=='-':continue
        if token in ',.;:!?«»\"\'()0123456789':
            # Punctuation and numeral glyphs are modern technical marks.
            token_width=18
            if x+token_width>width-50:x=30;y+=height_per_line
            spans.append((token,x,y,None));x+=token_width+5;continue
        img=letter_images[token];w=img.width+6
        if x+w>width-45:x=30;y+=height_per_line
        spans.append((token,x,y,img));x+=w
    img_out=Image.new('RGBA',(width,y+height_per_line),(0,0,0,0))
    draw=ImageDraw.Draw(img_out)
    for token,xx,yy,im in spans:
        if im is None:
            draw.text((xx,yy+font_height//2),token,fill=(245,245,245,255))
        else:
            # Respect grayscale/alpha data in the original character image.
            img_out.alpha_composite(im,(xx,yy+(font_height-im.height)//2))
    img_out.save(path)
    return (img_out.width,img_out.height)


def validate_data():
    data=entries()
    problems=[]
    lookup={r['qaroshi']:r for r in data}
    if len(lookup)!=len(data):problems.append('duplicate headwords')
    with (ROOT/'source/Qaroshi_Dictionary_853.csv').open(encoding='utf-8-sig') as f:
        core=list(csv.DictReader(f))
    for row in core:
        w=row['qaroshi'];got=lookup.get(w)
        if not got or got['pos']!=row['pos'] or got['english']!=row['english']:
            problems.append('original entry changed: '+w)
    for r in data:
        try:glyphs_of(r['qaroshi'])
        except ValueError as e:problems.append(r['qaroshi']+': '+str(e))
        if r['type']=='compound':
            parts=r['components'].split(' + ')
            if len(parts)!=2 or ''.join(parts)!=r['qaroshi'] or any(p not in lookup for p in parts):
                problems.append('bad compound '+r['qaroshi'])
    with (ROOT/'corpus/parallel_sentences.csv').open(encoding='utf-8-sig') as f:
        corpus=list(csv.DictReader(f))
    for i,r in enumerate(corpus,1):
        first=r['qaroshi'].strip().lower().split(' ')[0]
        if first not in RESONANCES:problems.append('missing sentence register at corpus line '+str(i))
    for word in RESONANCES:
        if word not in lookup:problems.append('missing resonance in lexicon: '+word)
    for w in ('wënu','qinë','yëmë','rëshi','qona','nura'):
        if w not in lookup:problems.append('missing grammar marker: '+w)
    return problems,{'lexicon_entries':len(data),'core_preserved':len(core),
                     'sample_sentences':len(corpus),'resonance_types':len(RESONANCES)}


def main():
    ap=argparse.ArgumentParser(description='Qaroshi language tools')
    sp=ap.add_subparsers(dest='command',required=True)
    look=sp.add_parser('lookup',help='Search definitions (either language)')
    look.add_argument('query');look.add_argument('--limit',type=int,default=25)
    morph=sp.add_parser('morph',help='Apply a sequence of noun or verb endings')
    morph.add_argument('root');morph.add_argument('--pos',choices=['noun','verb'],required=True)
    morph.add_argument('--plural',action='store_true');morph.add_argument('--case',choices=CASES)
    morph.add_argument('--topic',action='store_true');morph.add_argument('--endear',action='store_true')
    morph.add_argument('--voice',choices=VOICE);morph.add_argument('--tense',choices=TENSE)
    morph.add_argument('--aspect',choices=ASPECT);morph.add_argument('--modal',choices=MODAL)
    morph.add_argument('--tender',action='store_true')
    png=sp.add_parser('render',help='Render Romanized Qaroshi using the 26 supplied glyphs')
    png.add_argument('text');png.add_argument('--output',required=True)
    check=sp.add_parser('check',help='Conservative sentence check (not a full grammar parser)')
    check.add_argument('sentence')
    sp.add_parser('validate',help='Validate lexicon, glyph and corpus invariants')
    args=ap.parse_args()
    if args.command=='lookup':
        q=nfc(args.query).lower()
        rows=[r for r in entries() if q in r['qaroshi'].lower() or q in r['english'].lower()]
        for r in rows[:args.limit]:print(f"{r['qaroshi']:25} {r['pos']:8} {r['english']:65} [{r['review']}]")
        print(f'{len(rows)} matching entries')
    elif args.command=='morph':
        print(format_morphology(args.root,args.pos,args.plural,args.case,args.topic,args.endear,args.voice,args.tense,args.aspect,args.modal,args.tender))
    elif args.command=='render':
        dim=render_glyphs(args.text,args.output);print(f'Saved native-glyph PNG {args.output}: {dim[0]}x{dim[1]}')
    elif args.command=='check':
        notes=check_sentence(args.sentence,{r['qaroshi']:r for r in entries()})
        print('\n'.join(notes) if notes else 'No basic structural issues found. Semantics not verified.')
    elif args.command=='validate':
        problems,stats=validate_data()
        print(json.dumps({'counts':stats,'problems':problems[:50],'problem_count':len(problems)},ensure_ascii=False,indent=2))
        raise SystemExit(1 if problems else 0)
if __name__=='__main__':main()
