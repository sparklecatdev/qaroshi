#!/usr/bin/env python3
"""Extend the 2.0 bilingual corpus with controlled 3.0 examples.

Original 880 corpus rows are preserved exactly. Sentences are demonstrative
usage specimens, not evidence of an independent speaker corpus.
"""
from __future__ import annotations
import csv,json,re,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
from sentences_v3 import PREDICATE_PAIRS
ROWS=list(csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf-8-sig')))
OLD=list(csv.DictReader((ROOT/'source/corpus_v2_snapshot.csv').open(encoding='utf-8-sig')))
assert len(OLD)==880
LEX={r['qaroshi']:r for r in ROWS}
BY_ENG={(r['english'].lower(),r['pos']):r['qaroshi'] for r in ROWS if ';' not in r['english']}
for r in ROWS:
    for gloss in r['english'].lower().split(';'):
        BY_ENG.setdefault((gloss.strip(),r['pos']),r['qaroshi'])

def W(s,pos):
    value=BY_ENG.get((s.lower(),pos)) or BY_ENG.get((s.lower().split(';')[0].strip(),pos))
    if not value:raise ValueError(f'Unresolved curated expression {s!r}/{pos}')
    return value

def render(s):
    return re.sub(r'\{(n|v|adj|adv|part|conj):([^{}]+)\}',
                  lambda m:W(m.group(2),m.group(1)),s)

COLS=['id','domain','qaroshi','english','note','edition','pattern']
new=[];all_text={r['qaroshi'] for r in OLD}

def add(domain,qaroshi,english,note,pattern):
    q=render(qaroshi)
    if q in all_text:return
    assert q.startswith(tuple(['më ','zha ','qor ','sen ','hë ','lën ','sur ','rak ','khar ','yë ','nëm ','wen ','dal ','rëm ','hol ','zher '])),q
    all_text.add(q)
    new.append({'id':f'S3{len(new)+1:05d}','domain':domain,'qaroshi':q,
                'english':english,'note':note,'edition':'3.0','pattern':pattern})

# 3.x editorial method: verb gloss names its canonical patient and the patient
# is found in the dictionary as an independent nominal lexeme. No cross-product.
verb_pairs=[]
for r in ROWS:
    if r['pos']!='v' or r['edition']!='3.0' or r['type']!='headword':continue
    text=r['english'].lower()
    split=text.split(' ',1)
    if len(split)!=2:continue
    rest=split[1]
    for prefix in ('a ','an ','the '):
        if rest.startswith(prefix):rest=rest[len(prefix):]
    if (rest,'n') not in BY_ENG:continue
    patient=W(rest,'n');verb=r['qaroshi']
    phrase=r['english']
    domain=r['domain']
    verb_pairs.append((patient,verb,phrase,domain))
    add(domain, f'sen mi {patient}-m {verb}.',f'I {phrase}.',
        'Unmarked finite present; overt object case -m','3.0 precise semantic patient')
    add(domain, f'dal mi {patient}-m {verb}-yu.',f'I will {phrase}.',
        'Firm Pulse with future -yu','3.0 precise semantic patient')
    add(domain, f'hë ti {patient}-m {verb}-yu he?',f'Will you {phrase}?',
        'Question he after the final verb; no double resonance','3.0 precise semantic patient')

# Only manually curated noun/adjective predicates: avoid ungrounded word pairing.
for noun,adj,english_n,english_a in PREDICATE_PAIRS:
    n=W(noun,'n');a=W(adj,'adj')
    add('Predicates',f'sen dëna {n} {a}.',f'This {english_n} is {english_a}.',
        'Demonstrative + noun + adjective predicate (no copula)','3.0 curated adjective predicate')
    add('Predicates',f'hë dëna {n} {a} he?',f'Is this {english_n} {english_a}?',
        'Question marker is final, after adjective predicate','3.0 curated adjective predicate')

# A full grammar/usage showcase with literal, reversible dictionary substitutions.
GRAMMAR_EXAMPLES=[
('Temporary aspect','sen mi {n:threat model}-m {part:about to; imminently} {v:review a threat model}.',
 'I am about to review a threat model.', 'Imminence marker directly before verb'),
('Temporary aspect','sen mi {n:threat model}-m {part:just finished} {v:review a threat model}-te.',
 'I have just finished reviewing a threat model.','Recent-completion particle before past predicate'),
('Temporary aspect','sen mi {n:threat model}-m {part:still continuing} {v:review a threat model}-se.',
 'I am still reviewing a threat model.','Continuative particle before progressive predicate'),
('Temporary aspect','sen mi {n:threat model}-m {part:not yet} nu {v:review a threat model}.',
 'I have not reviewed the threat model yet.','Not-yet particle immediately before nu + verb'),
('Temporary aspect','sen mi {n:threat model}-m {part:no longer} nu {v:review a threat model}.',
 'I no longer review the threat model.','Cessation particle immediately before nu + verb'),
('Focus','sen dëna qaro {part:only; exclusively} haro.',
 'Only this Nardoragon is well.','Only scopes over the noun phrase directly preceding it'),
('Focus','sen dëna qaro {part:also; in addition} haro.',
 'This Nardoragon is also well.','Additive focus does not imply exclusivity'),
('Focus','sen dëna qaro {part:even (unexpected member)} haro.',
 'Even this Nardoragon is well.','Scalar unexpected-member focus'),
('Quantification','sen qaro-ri {part:at least (minimum)} po goro.',
 'At least two Nardoragons fly.','Lower bound with the native base-six numeral po'),
('Quantification','sen qaro-ri {part:at most (maximum)} po goro.',
 'At most two Nardoragons fly.','Upper bound with numeral'),
('Quantification','sen qaro-ri {part:exactly (quantity)} po goro.',
 'Exactly two Nardoragons fly.','Lower and upper bounds simultaneously'),
('Evidence','sen sa goro-te {part:recalled from direct memory}.',
 'I remember witnessing that they flew.','Memory as source: not the same as current observation si'),
('Evidence','sen sa goro-te {part:computed or instrument-measured evidence}.',
 'Measurements indicate that they flew.','Measurement-derived evidence, not an assertion of direct seeing'),
('Evidence','sen sa goro-te {part:read in a document or archival source}.',
 'A written document reports that they flew.','Written report subtype of reported evidence'),
('Evidence','yë sa goro-te {part:unexpected discovery; mirative} si.',
 'Surprisingly, they flew, and I witnessed it.','Mirative before evidential, not a replacement for it'),
('Evidence','zher sa goro-te ye {part:tentatively asserted; low confidence}.',
 'It seems they flew, though I am not very confident.','Inferred source + low confidence'),
('Evidence','sen sa goro-te si {part:high confidence (not certainty)}.',
 'I witnessed them fly and am highly confident.','Evidence vs epistemic confidence'),
('Dialogue','hë {part:requesting clarification rather than agreement} ti haro he?',
 'Are you well? I am asking for clarification, not confirmation.','Seeking Call + clarification stance'),
('Dialogue','më {part:explicitly no obligation} mi ti-m nashi.',
 'I cherish you, and you are not obliged to reciprocate.','Pressure-free interpersonal expression'),
('Dialogue','lën {part:requesting permission to discuss sensitive matter} mi ti-tu shiri-ki he?',
 'May I talk to you about something sensitive?','Consent-check stance with polar question'),
('Dialogue','nëm {part:soft refusal without shame} mi nu shiri.',
 'I prefer not to speak right now.','Soft refusal still uses normal predicate negation'),
('Dialogue','sen {part:topic shift; new subject} mi qaroshi-m shiri.',
 'Changing topics, I speak Qaroshi.','Discourse shift after the mandatory resonance'),
('Dialogue','sen {part:my words are a paraphrase} mi qaroshi-m shiri.',
 'I am paraphrasing this in Qaroshi.','Statement marked as paraphrase'),
('Dialogue','sen {part:I am translating this approximately} mi qaroshi-m shiri.',
 'I am giving an approximate Qaroshi translation.','Translation fidelity disclaimer'),
('Dialogue','sen {part:speaker does not claim expertise} mi qaroshi-m shiri.',
 'I speak Qaroshi, but do not claim expertise.','Epistemic humility markers do not change literal predicate'),
('Dialogue','sen {part:this remains open for discussion} mi qaroshi-m shiri.',
 'I speak Qaroshi, and remain open to discussing this.','Nonfinal stance marker'),
('Dialogue','qor {part:speaking for a group by agreement} naru qaro-ri-m daru-yu.',
 'With the group’s agreement, we will protect the Nardoragons.','Stance does not imply automatic legal authority'),
('Dialogue','sen {part:correction of misheard words} mi ti-m nashi.',
 'To correct what was misheard: I care deeply about you.','Repair a misunderstanding without new resonance mid-sentence'),
('Dialogue','më {part:gentle request for emotional check-in} ti haro he?',
 'Are you doing okay? This is a gentle check-in.','Emotional check-in never overrides possibility of refusal'),
('Dialogue','sen {part:conditional acceptance} mi ti-wa goro-yu, wë ti haro.',
 'I will fly with you if you are well.','Conditioned acceptance is not a blank agreement'),
('Conditionals','sen {conj:while two actions overlap} mi nëru, ti shiri.',
 'While I rest, you speak.','Two finite clauses share one sentence-initial resonance'),
('Conditionals','sen {conj:as soon as} mi nëru-mo, mi shiri-yu.',
 'As soon as I finish resting, I will speak.','Temporal immediate succession'),
('Conditionals','sen {conj:as long as; provided that} mi haro, mi goro-yu.',
 'As long as I am well, I will fly.','Ongoing condition'),
('Conditionals','sen {conj:in case; as a precaution for} sa goro-yu, mi naro-lo nëra-yu.',
 'In case they fly, I will remain at home.','Precautionary event is not asserted as certain'),
('Conditionals','sen {conj:so that not; to prevent} ti nu zëru, mi ti-m daru-yu.',
 'So that you do not die, I will protect you.','Negative purpose clause with one explicit nu'),
('Conditionals','sen {conj:whether or not (alternative exhaustive)} ti goro-yu, mi naro-lo nëra-yu.',
 'Whether or not you fly, I will stay at home.','Exhaustive concession: no separate yes/no claim'),
('Old canon','më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.',
 'Please never die so you can stay with me forever.','Exact canonical original phrase preserved'),
]
for domain,q,en,note in GRAMMAR_EXAMPLES:
    add(domain,q,en,note,'3.0 grammar and pragmatics')

all_rows=OLD+new
assert len({r['qaroshi'] for r in new})==len(new)
assert not ({r['qaroshi'] for r in new}&{r['qaroshi'] for r in OLD})
with (ROOT/'corpus/parallel_sentences.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,COLS);w.writeheader();w.writerows(all_rows)
(ROOT/'corpus/parallel_sentences.json').write_text(json.dumps(all_rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
stat={'original_from_v2':len(OLD),'v3_sentence_entries':len(new),'total_sentences':len(all_rows),
      'semantically_exact_verb_patient_pairs':len(verb_pairs),
      'curated_noun_adjective_pairs':len(PREDICATE_PAIRS),
      'grammar_and_pragmatics_demonstrations':len(GRAMMAR_EXAMPLES),
      'v3_patterns':dict(Counter(r['pattern'] for r in new))}
(ROOT/'corpus/coverage.json').write_text(json.dumps(stat,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('3.0 corpus',json.dumps(stat,ensure_ascii=False))
