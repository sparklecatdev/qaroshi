#!/usr/bin/env python3
"""Qaroshi 14.0: explainable morphosyntax and contextual translation-risk audits.

Transparent heuristics, not an authoritative native-speaker semantic oracle.
No canonical reference content is mutated by this module.
"""
from __future__ import annotations
import argparse, collections, json, re, sys, unicodedata
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools/fluency11'))
from engine import (word_analysis, words, RESONANCES, FUNCTIONS, CONNECTORS,
                    LEX, LEX_VERBS, parse_qaroshi)

CODE = {
    'R14-001': ('Missing sentence-opening resonance', 'error'),
    'R14-002': ('Unexpected internal sentence-opening resonance', 'review'),
    'R14-003': ('Unrecognized word or invalid suffix ordering', 'error'),
    'R14-004': ('Competing nominal case endings', 'error'),
    'R14-005': ('Competing tense, aspect, modal or voice endings', 'error'),
    'R14-006': ('Negator does not immediately precede an overt predicate', 'review'),
    'R14-007': ('Question marker and punctuation disagreement', 'error'),
    'R14-008': ('Evidential placement or stacking requires review', 'review'),
    'R14-009': ('Two direct objects or unlicensed object valency', 'review'),
    'R14-010': ('Unresolved clause, quotation or scope structure', 'review'),
    'R14-011': ('Contextual English omits or weakens grammatical negation', 'review'),
    'R14-012': ('Contextual English may omit or change ability', 'review'),
    'R14-013': ('Contextual English may omit or change permission', 'review'),
    'R14-014': ('Contextual English may omit or change obligation', 'review'),
    'R14-015': ('Source-of-evidence not explicit in English paraphrase', 'review'),
    'R14-016': ('Question versus declarative mismatch in English', 'review'),
    'R14-017': ('Contextual reading adds claims not overt in source', 'review'),
    'R14-018': ('Participant/reference disagreement in translation', 'review'),
    'R14-019': ('Potential cross-turn polarity repair or contradiction', 'review'),
    'R14-020': ('Exact source translation is not a semantic validation shortcut', 'info'),
}
NEG=re.compile(r"\b(?:not|never|no|without|cannot|can't|won't|wouldn't|isn't|aren't|didn't|don't|wasn't|weren't|failed|refused|disagree|unable|hadn't|haven't|doesn't|couldn't|shouldn't|neither|nor)\b",re.I)
ABILITY=re.compile(r"\b(?:can|can't|cannot|could|couldn't|able|unable|capable|manage|managed)\b",re.I)
PERMISSION=re.compile(r"\b(?:may|might|permission|permit|permitted|allowed|allow|welcome|invited)\b",re.I)
OBLIGATION=re.compile(r"\b(?:must|required|requirement|obliged|obligation|duty|need to|have to|has to|had to)\b",re.I)
EVIDENCE={
 'si':re.compile(r"\b(?:saw|seen|see|witnessed|witness|personally|directly|observed|observing|actually|myself|confirmed)\b",re.I),
 'hu':re.compile(r"\b(?:report|reported|heard|told|said|according|rumor|rumour|someone|they say|apparently)\b",re.I),
 'ye':re.compile(r"\b(?:infer|inferred|inference|seem|seemed|appears|apparently|perhaps|might|may|likely|probably|think|guess|suspect)\b",re.I),
}
PUNCT = re.compile(r'[.!?]$')

def _finding(code: str, detail: str, **additional: Any) -> dict:
    title, severity=CODE[code]
    return {'rule_id': code, 'title': title, 'severity': severity, 'detail': detail, 'kind': additional.pop('kind', 'structural'), **additional}


def validate_sentence(text: str, english: str | None = None, *, context_id: str = '') -> dict:
    text=unicodedata.normalize('NFC',text).strip()
    ts=words(text)
    findings=[]
    if not ts or ts[0] not in RESONANCES:
        findings.append(_finding('R14-001','A complete independent clause starts with exactly one of the 16 documented written resonances.'))
    if any(t in RESONANCES for t in ts[1:]):
        findings.append(_finding('R14-002','An internal resonance can be legitimate only when a new independent or quoted sentence begins.'))
    forms=[];corpus_lexemes=[]
    for i,t in enumerate(ts):
        if (i==0 and t in RESONANCES) or t in FUNCTIONS or t in CONNECTORS or (i!=0 and t in RESONANCES):continue
        analyzed=word_analysis(t)
        forms.append(analyzed)
        if analyzed.get('known'):corpus_lexemes.append(analyzed['root'])
        for err in analyzed.get('errors',[]):
            suffixes=t.split('-')[1:]
            cases=[x for x in suffixes if x in ('m','na','lo','gu','de','wa','tu','shi')]
            classes={'te':'tense','yu':'tense','se':'aspect','mo':'aspect','në':'aspect','ki':'modal','ho':'modal','du':'modal','ru':'voice','li':'voice','wo':'voice','ne':'voice'}
            active=[classes[x] for x in suffixes if x in classes]
            rule=('R14-004' if len(cases)>1 else 'R14-005' if len(active)>len(set(active)) else 'R14-003')
            findings.append(_finding(rule,f'{t}: {err}',token=t))
    # Morphologically valid words need not form a licensed clause; review the main finite frame.
    core=ts[1:] if ts and ts[0] in RESONANCES else ts[:]
    mood=core[-1] if core and core[-1] in ('he','ya') else None
    if mood:core.pop()
    ev=core[-1] if core and core[-1] in ('si','hu','ye') else None
    if ev:core.pop()
    last=core[-1] if core else None
    if text.endswith('?') and mood!='he':
        findings.append(_finding('R14-007','A complete polar question ending in ? requires a final he.'))
    if mood=='he' and text.endswith('!'):
        findings.append(_finding('R14-007','Question marker he conflicts with exclamation mood; clarify intended speech act.'))
    if mood=='ya' and text.endswith('?'):
        findings.append(_finding('R14-007','A command ending in ya should not be presented as a polar question.'))
    if len(ts)>=2 and ts[-2:] in (['he','ya'],['ya','he']):
        findings.append(_finding('R14-007','Question and command ending markers cannot stack in one finite clause.'))
    nested=[(i,x) for i,x in enumerate(core) if x in ('si','hu','ye')]
    if nested or (ev is not None and len([x for x in ts if x in ('si','hu','ye')])>1):
        findings.append(_finding('R14-008','Evidentials normally follow the predicate and precede he/ya; stacked or embedded sources need explicit clause analysis.'))
    if 'nu' in core:
        for i,x in enumerate(core):
            if x!='nu':continue
            following=core[i+1] if i+1<len(core) else ''
            a=word_analysis(following) if following else {}
            if not a.get('known') or a.get('pos') not in ('v','adj'):
                findings.append(_finding('R14-006',f'nu is followed by {following!r}, not a recognized verb/adjective. This may be a complex construction.'))
    noun_objects=[]
    for form in forms:
        if form.get('features',{}).get('case')=='object':noun_objects.append(form['surface'])
    if len(noun_objects)>1 and not any(x in core for x in ('ara','nao','do','wë','yaro','ko','ro')):
        findings.append(_finding('R14-009',f'{len(noun_objects)} phrases bear -m: {", ".join(noun_objects)}. Check whether one is a recipient (-tu) or in a separate clause.'))
    # Intransitive lexical frames are known only for a small curated subset.
    if last:
        predicate=word_analysis(last)
        if predicate.get('pos')=='v' and predicate.get('root') in LEX_VERBS:
            _,trans=LEX_VERBS[predicate['root']]
            if not trans and noun_objects:
                findings.append(_finding('R14-009',f'Curated {last} frame is intransitive but has an overt -m direct object.'))
    if any(x in core for x in ('wë','do','yaro','uro','ko','ro','nao','ara','oru','ana','ëna')):
        findings.append(_finding('R14-010','Clause boundaries, argument attachment and truth-conditional scope must be reviewed in context; a flat token scan cannot settle them.'))
    # An exact controlled bilingual reference example can itself contain editorial
    # ambiguity. Never allow it to skip the independently executed checks above.
    en=(english or '').strip()
    if en:
        if 'nu' in ts and not NEG.search(en):
            findings.append(_finding('R14-011','The source has explicit nu, while the English does not explicitly negate. Some English euphemisms may express negation pragmatically.',kind='translation-risk'))
        if any(t.endswith('-ki') for t in ts) and not ABILITY.search(en):
            findings.append(_finding('R14-012','-ki encodes ability, but the English does not overtly express ability; contextual ellipsis may be intended.',kind='translation-risk'))
        if any(t.endswith('-ho') for t in ts) and not PERMISSION.search(en):
            findings.append(_finding('R14-013','-ho encodes permission, distinct from -ki ability. The English may not preserve this.',kind='translation-risk'))
        if any(t.endswith('-du') for t in ts) and not OBLIGATION.search(en):
            findings.append(_finding('R14-014','-du encodes obligation, distinct from ability and permission.',kind='translation-risk'))
        for e in ('si','hu','ye'):
            if e in ts and not EVIDENCE[e].search(en):
                findings.append(_finding('R14-015',f'Evidential {e} indicates a knowledge source but is not overtly preserved in the English.',kind='translation-risk',evidential=e))
        if mood=='he' and '?' not in en and not re.search(r'\b(?:whether|if)\b',en,re.I):
            findings.append(_finding('R14-016','The Qaroshi clause is a polar question but the English is not marked as interrogative.',kind='translation-risk'))
        if mood!='he' and '?' in en:
            findings.append(_finding('R14-016','The English is a question, but the Qaroshi independent clause has no final he.',kind='translation-risk'))
        # A handful of reference-contrast anchors are unambiguous enough to
        # check. General pronoun resolution is deliberately NOT inferred.
        if 'ti-wa' in ts and re.search(r'\bstay with them\b',en,re.I):
            findings.append(_finding('R14-018','ti-wa is with *you*; the English says *with them*. An explicit translation/referent review is required.',kind='translation-risk'))
        # Contextual enrichments are legitimate story choices, but should not be
        # silently promoted to literal translations.
        if re.search(r'\b(?:because|in order to|so that|before|after|unless)\b',en,re.I) and not any(x in ts for x in ('ko','ro','wë','ana','ëna','yaro')):
            findings.append(_finding('R14-017','English includes a logical/temporal relation not overtly encoded by the cited Qaroshi clause; check context.',kind='translation-risk'))
    return {'source':text,'english':en or None,'context_id':context_id,
            'valid_surface':not any(x['severity']=='error' for x in findings),
            'findings':findings,'known_lexemes':len(corpus_lexemes),
            'scope':'documented finite clause patterns only; no speaker naturalness or truth guarantee'}


def possible_repair_pairs(turns: list[dict]) -> list[dict]:
    """Find potentially inconsistent successive *claims by the same speaker*.
    Only a review queue: shifts in time, corrections and quotation are allowed.
    """
    memory={};out=[]
    for i,t in enumerate(turns):
        ts=words(t.get('qaroshi',''))
        core=ts[1:]
        # restrict to a simple two-token subject/predicate frame
        if len(core)<2:continue
        pred=core[-1];pred_a=word_analysis(pred)
        if not pred_a.get('known') or pred_a.get('pos')!='v':continue
        subject=core[0]
        if subject not in ('mi','ti','sa','naru','muru'):continue
        key=(t.get('speaker',''),subject,pred_a['root'],tuple(sorted(pred_a.get('features',{}).items())))
        neg=('nu' in core)
        if key in memory and memory[key][0] != neg:
            out.append({'first_turn':memory[key][1],'second_turn':t.get('turn',i+1),
                        'speaker':key[0],'predicate':key[2],
                        'category':'possible statement repair, polarity contrast or conflict; requires contextual review'})
        memory[key]=(neg,t.get('turn',i+1))
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('qaroshi');p.add_argument('--english');p.add_argument('--pretty',action='store_true')
    a=p.parse_args()
    print(json.dumps(validate_sentence(a.qaroshi,a.english),indent=2 if a.pretty else None,ensure_ascii=False))
if __name__=='__main__':main()
