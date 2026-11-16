#!/usr/bin/env python3
"""Qaroshi 28–34 conservative grammar extension and scope interpreter.

Normative only for the narrowly specified negative universal determiner nëgëra;
all other 7.0 / 24–27 rules remain in force. Never claims open-domain parsing.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/v24_27'))
sys.path.insert(0,str(ROOT/'tools/fluency11'))
from validate import validate_sentence as previous_validator
from engine import words,LEX,RESONANCES
NEW='nëgëra'
# Dedicated, non-overlapping spelling: this is a post-7.0 lexical overlay.
QUANTIFIERS={'ngënao':'forall','nëgëra':'not_forall','shërano':'exists'}
SCOPE_FORMS={('ngënao',False):'∀x∈D P(x)',('ngënao',True):'∀x∈D ¬P(x)',
 ('nëgëra',False):'∃x∈D ¬P(x)',('shërano',False):'∃x∈D P(x)',('shërano',True):'∃x∈D ¬P(x)'}

def analyze_quantifier(s:str)->dict:
 """Interpret only a simple resonance + quantifier + noun + (nu) + finite predicate.

 The result explicitly abstains rather than guessing on complex clauses,
 nested topics, unknown lexemes, tense-negation interaction or question scope.
 """
 t=words(s)
 r={'interpretable':False,'scope':None,'logical_form':None,'note':'Not a simple one-quantifier affirmative statement; inspect by hand.'}
 if len(t)<4 or t[0] not in RESONANCES or t[1] not in QUANTIFIERS:return r
 q,n=t[1:3]
 if n not in LEX or LEX[n]['pos']!='n':return {**r,'note':'Quantifier requires an existing noun in subject position.'}
 if q=='nëgëra' and len(t)>=4 and t[3]=='nu':return {**r,'note':'nëgëra already negates universal force; use shërano NP nu V for the equivalent existential negative.'}
 neg=len(t)==5 and t[3]=='nu';target=t[4] if neg else t[3]
 if len(t) != (5 if neg else 4):return {**r,'note':'Requires exactly one quantified subject and one predicate; additional roles need clause analysis.'}
 root=target.split('-')[0]
 if root not in LEX or LEX[root]['pos'] not in ('v','adj'):return {**r,'note':'Predicate needs a documented verb or adjective for this restricted rule.'}
 if any(x in t for x in ('wë','nao','ro','ara','do','ko','shoru')):return r
 formula=SCOPE_FORMS.get((q,neg))
 if formula is None:return r
 return {'interpretable':True,'scope':QUANTIFIERS[q],'quantifier':q,'noun':n,'predicate':target,
    'negated_predicate':neg,'logical_form':formula,'domain_nonempty_required':q=='nëgëra',
    'note':{'nëgëra':'At least one relevant member does not satisfy P. Does not assert any do satisfy P.',
    'ngënao':'Universal distribution; following predicate nu has narrow scope.',
    'shërano':'Existential distribution, not necessarily exclusion of other members.'}[q]}

def evaluate_on_finite_domain(form:str,values:list[bool])->bool:
 """Small-model semantics for scope regression, not a truth evaluator for prose."""
 if form=='every':return all(values)
 if form=='none':return not any(values)
 if form=='not_every':return bool(values) and not all(values)
 if form=='some':return any(values)
 if form=='some_not':return any(not x for x in values)
 if form=='only_one':return sum(values)==1
 if form=='at_least_two':return sum(values)>=2
 if form=='at_most_two':return sum(values)<=2
 if form=='exactly_two':return sum(values)==2
 raise ValueError('Unknown logical form: '+form)

def validate_sentence(s:str, english:str|None=None)->dict:
 r=previous_validator(s,english)
 t=words(s)
 newcount=t.count(NEW)
 if newcount:
  # The frozen v14 lexical engine does not know the *newly adopted* determiner.
  # Suppress ONLY the exact unknown-lemma diagnostic for this single spelling.
  r['findings']=[f for f in r['findings'] if not (f.get('rule_id')=='R14-003' and f.get('detail','').strip()==f'{NEW}: Unknown lemma {NEW}')]
  if newcount!=1:r['findings'].append(_issue('R30-01','error','Only one nëgëra can occur in an independent simple clause.'))
  if len(t)<4 or t[0] not in RESONANCES or t[1]!=NEW:
   r['findings'].append(_issue('R30-02','error','nëgëra must immediately precede the quantified subject after the opening resonance in the simple-clause construction.'))
  if not analyze_quantifier(s)['interpretable']:
   r['findings'].append(_issue('R30-03','review','A general or embedded nëgëra clause requires a phrase-structure analysis. This simple checker cannot license it.'))
  if len(t)>3 and t[3]=='nu' and t[1]==NEW:
   r['findings'].append(_issue('R30-04','error','Do not combine nëgëra with predicate negation to mean not everyone.'))
  if len(t)>3 and t[2] not in LEX:
   r['findings'].append(_issue('R30-05','error','The quantified noun must be a documented lexical noun.'))
 r['scope_analysis']=analyze_quantifier(s)
 r['valid_surface']=not any(f.get('severity')=='error' for f in r['findings'])
 r['amendment']='Qaroshi 28–34 supplement; quantified simple clauses only; 7.0 and 24–27 legacy preserved'
 return r

def _issue(rule_id,severity,detail):return {'rule_id':rule_id,'severity':severity,'detail':detail,'title':'Quantifier standard 30','kind':'reform-28-34'}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('qaroshi');p.add_argument('--english');args=p.parse_args()
 print(json.dumps(validate_sentence(args.qaroshi,args.english),ensure_ascii=False,indent=2))
