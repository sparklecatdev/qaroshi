"""Standard 8.0: explicitly limited two-quantifier scope grammar.

This is an adopted *constructed-language* convention for simple SOV clauses.
Position assigns scope; case assigns grammatical role. Distinguish those!
Any clause with embedded, quoted, focused, or elliptical scope is abstained.
"""
from __future__ import annotations
import csv, itertools, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LEX={r['qaroshi']:r for r in csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf-8'))}
RESONANCES={r['marker'] for r in json.loads((ROOT/'data/resonances.json').read_text(encoding='utf-8'))}
QUANT={'ngënao':'forall','shërano':'exists','nëgëra':'not_forall'}
BLOCK={'wë','wënu','shoru','qëhano','wëlëmi','dasha','ara','ro','ko','nao','yaro','ana','ëna','tëshi','nashu'}
TOKENS=re.compile(r'[a-zë]+(?:-[a-zë]+)*',re.I)

def analyze(sentence:str)->dict:
    tok=TOKENS.findall(sentence.lower())
    fail=lambda reason:{'supported':False,'reason':reason,'status':'requires manual structural analysis'}
    if len(tok)<6 or tok[0] not in RESONANCES:return fail('Expected a resonance and two quantified NPs.')
    if any(t in BLOCK for t in tok):return fail('Contains embedding, discourse framing or clause-coordination outside this simple-scope grammar.')
    if tok[-1] in ('he','ya','qinë'):return fail('Question, imperative and counterfactual require their own scope rules.')
    if any(x in ('nu','nura') for x in tok[1:-2]):return fail('Negation outside the immediately preverbal slot or negative pronoun is not licensed.')
    if len(tok) not in (6,7):return fail('Only two quantified nominal phrases and one final predicate are licensed.')
    q1,n1,q2,n2=tok[1:5]
    if q1 not in QUANT or q2 not in QUANT:return fail('Each noun phrase must have an explicitly documented quantifier.')
    if q1=='nëgëra' and q2=='nëgëra':return fail('Nested not-all quantifiers require an explicitly reviewed interpretation.')
    roles=[]
    for n in (n1,n2):
        case='object' if n.endswith('-m') else 'subject'
        root=n[:-2] if case=='object' else n
        if root not in LEX or LEX[root]['pos']!='n':return fail('Each quantified nominal must be a canonical noun or its -m object form.')
        roles.append((root,case))
    if sorted([r[1] for r in roles])!=['object','subject']:
        return fail('Exactly one subject and one -m object are required.')
    neg=tok[-2]=='nu'
    if len(tok)!=(7 if neg else 6):return fail('Predicate negation must be immediately before the final predicate.')
    if any(q=='nëgëra' for q in (q1,q2)) and neg:return fail('not-all with independent predicate negation needs explicit contextual disambiguation.')
    pred=tok[-1];root=pred.split('-')[0]
    if root not in LEX or LEX[root]['pos']!='v':return fail('Final predicate must be a documented lexical verb.')
    if '-' in pred:
        return fail('Inflected, voiced or modal predicate needs additional scope analysis.')
    subject_label='x' if roles[0][1]=='subject' else 'y';object_label='y' if roles[0][1]=='subject' else 'x'
    # Bind x to surface-first nominal, y to surface-second nominal; subject/object
    # selection is independent of binding order.
    def quant(q,v,body):
        return {'ngënao':f'∀{v}∈D: {body}','shërano':f'∃{v}∈D: {body}', 'nëgëra':f'¬∀{v}∈D: {body}'}[q]
    base=f'{root}({subject_label},{object_label})'
    if neg:base='¬'+base
    formula=quant(q1,'x',quant(q2,'y',base))
    return {'supported':True,'quantifiers':[q1,q2],'roles':[roles[0][1],roles[1][1]],'nouns':[roles[0][0],roles[1][0]],
            'predicate':root,'negated_predicate':neg,'logical_form':formula,
            'interpretation':'Surface-first quantified NP has widest scope; noun case (-m) independently determines thematic role.',
            'status':'Standard 8 adopted restricted two-quantifier rule; editorial constructed example, not observed speech.'}

def evaluate(form:str,relation:list[list[bool]],first_domain:list[int]|None=None,second_domain:list[int]|None=None)->bool:
    """Evaluate simple quantifier structure over a finite directed binary relation.

    relation[x][y] is P(x,y). The predicate's semantic subject/object order
    is adjusted by `first_is_subject` in the caller's form tag.
    """
    if not relation or not relation[0] or any(len(r)!=len(relation[0]) for r in relation):raise ValueError('Nonempty rectangular relation required')
    q1,q2,first_subject,negative=form.split('|')
    first_n=len(relation) if first_subject=='yes' else len(relation[0])
    second_n=len(relation[0]) if first_subject=='yes' else len(relation)
    a=first_domain if first_domain is not None else list(range(first_n))
    b=second_domain if second_domain is not None else list(range(second_n))
    if not a or not b:raise ValueError('Nonempty quantified domains required')
    if any(x<0 or x>=first_n for x in a) or any(y<0 or y>=second_n for y in b):raise ValueError('Domain index out of range')
    def calc(q,vals):
        return {'ngënao':all,'shërano':any,'nëgëra':lambda x:not all(x)}[q](vals)
    def p(x,y):
        v=relation[x][y] if first_subject=='yes' else relation[y][x]
        return (not v) if negative=='yes' else v
    return calc(q1,(calc(q2,(p(i,j) for j in b)) for i in a))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('sentence');args=p.parse_args();print(json.dumps(analyze(args.sentence),ensure_ascii=False,indent=2))
