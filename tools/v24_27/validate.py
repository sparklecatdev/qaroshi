#!/usr/bin/env python3
"""Conservative validation of Qaroshi amendment 24–27 on top of frozen v14.

This does NOT make arbitrary multi-clause judgments, nor rewrite prior QA records.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v14'))
sys.path.insert(0,str(ROOT/'tools/fluency11'))
from semantic_validator import validate_sentence as baseline
from engine import words,word_analysis

CODES={
 'R24-001':('Explicit passive agent needs a passive finite predicate','error'),
 'R24-002':('Historical -shi passive actor is ambiguous with an instrument','review'),
 'R24-003':('Multi-clause passive-agent attachment requires human review','review'),
 'R24-004':('Competing overt passive agents require context','review'),
 'R24-005':('Competing nominal cases on one noun phrase','error'),
}
CONNECTORS={'wë','do','yaro','uro','ko','ro','nao','ara','oru','ana','ëna'}
def validate_sentence(s:str,english:str|None=None)->dict:
 result=baseline(s,english)
 tokens=words(s)
 active=tokens[1:] if tokens and tokens[0] in {'më','zha','qor','sen','hë','lën','sur','rak','khar','yë','nëm','wen','dal','rëm','hol','zher'} else tokens
 agents=[t for t in active if t.endswith('-za') and not word_analysis(t).get('errors')]
 passives=[t for t in active if word_analysis(t).get('features',{}).get('voice')=='passive']
 for token in active:
  cases=[x for x in token.split('-')[1:] if x in {'m','na','lo','gu','de','wa','tu','shi','za'}]
  if len(cases)>1 and 'za' in cases:
   add(result,'R24-005',f'{token} carries competing noun-case endings: '+', '.join(cases))
 if agents:
  if CONNECTORS.intersection(active):
   add(result,'R24-003','A parser must associate each agent -za with a passive -li in its own finite clause; a flat scan cannot certify it.')
  elif not passives:
   add(result,'R24-001','-za must be an overt agent of a finite -li passive, not an active subject or means.')
  if len(agents)>1:
   add(result,'R24-004','Multiple overt -za phrases need coordination or separate clause analysis.')
 if passives and any(t.endswith('-shi') for t in active):
  add(result,'R24-002','In revised prose -shi is means/instrument; legacy passive-agent examples can still have the old reading.')
 result['valid_surface']=not any(f['severity']=='error' for f in result['findings'])
 result['amendment']='24–27 normative supplement; simple clause checks only'
 return result

def add(r,id,detail):
 title,severity=CODES[id]
 r['findings'].append({'rule_id':id,'title':title,'severity':severity,'detail':detail,'kind':'reform-24-27'})
if __name__=='__main__':
 cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('qaroshi');cli.add_argument('--english');args=cli.parse_args()
 print(json.dumps(validate_sentence(args.qaroshi,args.english),ensure_ascii=False,indent=2))
