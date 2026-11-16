#!/usr/bin/env python3
"""Qaroshi 8.1 narrow structural recognizer for an embedded polar question.

Does not translate unrestricted prose or infer participant omission or verb
selection from gloss. This is a verified parser for a deliberately narrow
subgrammar of current 90-chapter norms.
"""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MARKERS={r['marker'] for r in json.loads((ROOT/'data/resonances.json').read_text(encoding='utf8'))}
PRON={'mi':'I','ti':'you','sa':'they','naru':'we (inclusive)','muru':'we (exclusive)','tiri':'you (plural)','sari':'they (plural)'}
PRED={'haro': 'be well', 'goro':'fly'}
TOK=re.compile(r'[a-zë]+(?:-[a-zë]+)*',re.I)

def analyze(sentence:str)->dict:
    tokens=TOK.findall(sentence.lower())
    def fail(reason):return {'supported':False,'reason':reason,'status':'outside the documented 8.1 one-complement fragment'}
    if not tokens or tokens[0] not in MARKERS:return fail('A full written sentence requires one opening resonance.')
    if len(tokens)<6:return fail('Not enough terms for an embedded clause and matrix clause.')
    if tokens.count('do')!=1:return fail('Exactly one content-clause boundary do is licensed in this narrow recognizer.')
    i=tokens.index('do')
    inner=tokens[1:i];outer=tokens[i+1:]
    if any(t in MARKERS for t in inner+outer):return fail('A subordinate clause cannot open with its own resonance.')
    inner_question=bool(inner and inner[-1]=='he')
    if inner_question:inner=inner[:-1]
    matrix_question=bool(outer and outer[-1]=='he')
    if matrix_question:outer=outer[:-1]
    if 'he' in inner or 'he' in outer:return fail('he is only licensed immediately before do or as the matrix final.')
    if len(inner) not in (2,3) or inner[0] not in PRON or inner[-1] not in PRED:return fail('Requires a simple pronoun + documented predicate in the embedded proposition.')
    inner_neg=len(inner)==3 and inner[1]=='nu'
    if len(inner)==3 and not inner_neg:return fail('Embedded nu must be directly before its predicate.')
    if len(outer) not in (2,3) or outer[0] not in PRON or outer[-1]!='sëmi':return fail('Matrix clause must be a pronoun + (nu) + sëmi (know) in this recognizer.')
    matrix_neg=len(outer)==3 and outer[1]=='nu'
    if len(outer)==3 and not matrix_neg:return fail('Matrix nu must directly precede sëmi.')
    person=PRON[inner[0]]
    if inner[-1]=='haro':
        predicate=('am' if inner[0]=='mi' else 'are')+(' not' if inner_neg else '')+' well'
    else:
        predicate=('do not ' if inner_neg else '')+'fly'
    statement=f'{person} {predicate}'
    complement=f'whether {statement}' if inner_question else f'that {statement}'
    speaker=PRON[outer[0]]
    interp=(f'Do {speaker} '+('not ' if matrix_neg else '')+f'know {complement}?' if matrix_question
            else f'{speaker} '+('do not know' if matrix_neg else 'know')+f' {complement}.')
    interp=interp[0].upper()+interp[1:]
    return {'supported':True,'status':'one-embedded-content-clause normative structure',
      'embedded_polar':inner_question,'embedded_negative':inner_neg,'matrix_negative':matrix_neg,
      'matrix_polar':matrix_question,'complement_type':'whether' if inner_question else 'that',
      'meaning_gloss':interp,
      'truth_policy':'know-whether does not assert the embedded proposition true; nu scopes only to its local predicate',
      'structural_warning':'Example interpretation only; semantic valency and full paragraph inference not certified'}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('sentence');a=p.parse_args()
 print(json.dumps(analyze(a.sentence),ensure_ascii=False,indent=2))
