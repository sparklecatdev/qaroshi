#!/usr/bin/env python3
"""Generate a deliberately labelled finite morphology/speech-act regression benchmark.

The expected result is *surface-form rule compliance*, not naturalness.
"""
import json,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v14'))
from semantic_validator import validate_sentence, CODE, LEX

NOUNS=['mara','kima','qaro','shiwaro','shima','moru','sëra','naro','gëro','banu']
VERBS=['goro','shiri','daru','tika','këmë','shiwari','nëru','nëra','shëliro','pëli']
for n in NOUNS:
 assert LEX[n]['pos']=='n',(n,LEX[n]['pos'])
for n in VERBS:
 assert LEX[n]['pos']=='v',(n,LEX[n]['pos'])
valid_nom=['-m','-na','-lo','-gu','-wa','-tu','-shi','-ri-m','-ri-gu','-lë-ri-m','-m-së']
invalid_nom=['-m-ri','-m-na','-ri-ri','-na-lo','-së-ri','-lë-lë','-ri-m-tu','-lo-de','-foo','-ri-ri-m']
valid_verbs=['-te','-yu','-te-se','-yu-mo','-në','-ki','-ho','-du','-li-te','-ru-yu','-te-mo-ho']
invalid_verbs=['-te-yu','-se-te','-ki-ho','-te-te','-mo-se','-ru-li','-du-ki','-la-yu','-foo','-yu-te']
rows=[]
def add(q,expect,rule):
 a=validate_sentence(q)
 res=a['valid_surface']
 if expect!=res:raise ValueError((q,expect,res,a['findings']))
 rows.append({'id':f'M14-{len(rows)+1:04}','kind':'morphology/sentence','qaroshi':q,
              'expected_surface_valid':expect,'expected_rule_category':rule,
              'evidence':'source-grammar structural rule; not a speaker acceptability judgement'})
for noun in NOUNS:
 for suf in valid_nom:add(f'sen mi {noun+suf} tika.',True,'nominal slot sequence')
 for suf in invalid_nom:add(f'sen mi {noun+suf} tika.',False,'nominal slot/order violation')
for verb in VERBS:
 for suf in valid_verbs:add(f'sen mi {verb+suf}.',True,'verbal slot sequence')
 for suf in invalid_verbs:add(f'sen mi {verb+suf}.',False,'verbal slot/order violation')
for q,exp,rule in [
 ('sen mi kima-m këmë.',True,'SOV statement'),
 ('hë ti haro he?',True,'complete question'),
 ('qor mi ti-m daru-yu.',True,'solemn future statement'),
 ('sen mi ti-tu kima-m pëli-yu.',True,'recipient + patient'),
 ('sen sa goro-te si.',True,'direct observation evidential'),
 ('sen sa goro-te hu.',True,'reported evidential'),
 ('sen sa goro-te ye.',True,'inferred evidential'),
 ('sen mi nu shiri.',True,'negation'),
 ('sen mi nu goro-ki.',True,'negated ability'),
 ('sen mi goro-ki.',True,'ability'),
 ('sen mi goro-ho.',True,'permission'),
 ('sen mi goro-du.',True,'obligation'),
 ('hë ti mi-m daru-ki he?',True,'ability question'),
 ('sen mi-n a goro.',False,'invalid token'),
 ('mi kima-m këmë.',False,'missing resonance'),
 ('sen mi kima-m-ri këmë.',False,'nominal order violation'),
 ('sen mi goro-te-yu.',False,'competing tense'),
 ('sen mi goro-ki-ho.',False,'competing modality'),
 ('sen mi goro-se-mo.',False,'competing aspect'),
 ('hë ti haro?',False,'question punctuation without he'),
 ('hë ti haro he ya?',False,'stacked question/command'),
 ('sen mi goro foo.',False,'unknown root'),
 ]:
  add(q,exp,rule)
folder=ROOT/'data/v14'
(folder/'grammar_regression_442.jsonl').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n',encoding='utf8')
assert len(rows)==442,len(rows)
print('Generated and independently re-checked',len(rows),'surface regression fixtures')
