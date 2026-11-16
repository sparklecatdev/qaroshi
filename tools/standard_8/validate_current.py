#!/usr/bin/env python3
"""Current Standard 8.0 conservative validator, without replacing legacy QA.

A limited structural validator can certify supported *forms*, not arbitrary
semantic truth. It emits explicit review results for underdetermined syntax.
"""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/standard_8'))
sys.path.insert(0,str(ROOT/'tools/v28_34'))
from scope import analyze as scope_analysis
from reform_core import validate_sentence as legacy_and_28

def check(s:str)->dict:
 parsed=scope_analysis(s)
 if parsed['supported']:
  verb=parsed['predicate']
  manual={r['lemma']:r for r in csv.DictReader((ROOT/'data/standard_8/verb_audit_400.csv').open(encoding='utf8'))}
  frame=manual.get(verb)
  statuses=[]
  # Structural syntax is licensed, but lexical valency must be assessed
  # separately, especially for quantified objects unlike exact corpus exemplars.
  if frame is None: statuses.append('Verb is outside the 400-frame learning inventory; review lexical valency.')
  elif frame['general_frame_review'].startswith('no'):statuses.append('Quantified object class is not independently licensed by a source exemplar; review verb selectional restrictions.')
  elif 'object:-m' in frame['required_roles'] or 'object:-m' in frame['licensed_optional_roles']:
   statuses.append('Verb has an inherited reviewed direct object frame; confirm object semantic class.')
  else:statuses.append('This reviewed verb frame may be intransitive; the quantified object might be unlicensed.')
  return {'standard':'Qaroshi 8.0','structural_status':'valid_current_two_quantifier_pattern',
          'lexical_status':'requires case-role review' if 'unlicensed' in statuses[-1] or 'not independently' in statuses[-1] else 'check selectional restrictions',
          'scope':parsed,'notes':statuses,'speaker_attested':False}
 # Single quantifier and other older input still goes through historical
 # analyzers which have rule-set limits; we do not promise full syntax coverage.
 old=legacy_and_28(s)
 return {'standard':'Qaroshi 8.0','structural_status':'legacy_or_current_simple_clause' if old['valid_surface'] else 'rejected_or_review_required',
         'scope':old.get('scope_analysis'), 'findings':old.get('findings',[]),
         'limitations':parsed['reason'],'speaker_attested':False}
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('sentence');args=ap.parse_args()
 print(json.dumps(check(args.sentence),ensure_ascii=False,indent=2))
