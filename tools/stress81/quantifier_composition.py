#!/usr/bin/env python3
"""Narrow, independently reproducible 8.0 quantifier composition probes.

These are editorial rule-based composition drafts with dictionary-root and
standard-grammar witnesses, NOT community-attested free translation.
"""
from __future__ import annotations
import csv,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LEX={r['qaroshi']:r for r in csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf8'))}
# Authored semantic selections; English glosses and word classes are rechecked
# against the frozen 7.0 source. We do not choose an arbitrary English synonym.
PAIRS=[
 ('Nardoragon','Nardoragons','well','qaro','haro'),
 ('friend','friends','cute','mara','lësha'),
 ('home','homes','locked','naro','yushale'),
 ('river','rivers','cold','kimaro','ngëruwa'),
 ('wing','wings','red','banu','zhëwa'),
 ('message','messages','encrypted','shiwaro','qebiya'),
 ('book','books','complete','shima','rënaroa'),
 ('test result','test results','reliable','nishakho','yugude'),
 ('medical device','medical devices','sterile','mëgudapasëku','yukhëgë'),
 ('answer','answers','correct','rënoa','shënoawe'),
]
for singular,_,adj,noun,prop in PAIRS:
    assert LEX[noun]['pos']=='n' and singular.casefold() in LEX[noun]['english'].casefold(),(singular,noun)
    assert LEX[prop]['pos']=='adj' and adj.casefold() in LEX[prop]['english'].casefold(),(adj,prop)

def compose(challenge:dict):
    if challenge['domain']!='quantifier_logic':return None
    family=int(challenge['scenario_family'].split('-')[-1]); variant=int(challenge['variant'])
    singular,plural,adj,noun,prop=PAIRS[family-1]
    # One context-dependent English time adjunct is deliberately outside our
    # licensed syntax, so this set supports 49, not a fake '50/50' success.
    if family==1 and variant==5:return None
    candidates={
        1:f'sen ngënao {noun} {prop}.',
        2:f'sen nëgëra {noun} {prop}.',
        3:f'sen ngënao {noun} nu {prop}.',
        4:f'sen shërano {noun} {prop}.',
        5:f'sen dëna {noun} ngëshi {prop}.',
    }
    return {'candidate':candidates[variant], 'reference':'Standard 8.0 grammar chapter 78, inherited chapter 2/4/9, 28–34 quantifier amendment',
      'source_lemmas':noun+' | '+prop,
      'status':'constructed compositional proposal from adopted grammar and source lexemes; no independent semantic ratification',
      'verified_bounds':'one quantified noun with documented adjective; distributive reading only'}
