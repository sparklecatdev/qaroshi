#!/usr/bin/env python3
"""Check a fixed six-item editorial subset, not open-domain translation."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / 'data/standard_8/challenge_reviews_8_6.json'
FRAMES = ROOT / 'data/standard_8/valency_overlay_8_6.json'


def evaluate(case, lexicon, frames):
    """Check only the exact simple, past, active challenge pattern."""
    if case['mode'] not in {'affirmative', 'negative', 'question'}:
        return False
    words = case['qaroshi'].strip().rstrip('.?').split()
    question = case['mode'] == 'question'
    if question:
        if not words or words[-1] != 'he':
            return False
        words = words[:-1]
    if len(words) not in (4, 5) or words[0] != ('hë' if question else 'sen'):
        return False
    if words[1] != case['subject'] or words[2] != case['object'] + '-m':
        return False
    if any(lexicon.get(case[key], {}).get('id') != case[key + '_id'] for key in ('subject', 'object')):
        return False
    negative = case['mode'] == 'negative'
    if words[3:-1] != (['nu'] if negative else []):
        return False
    frame = frames.get(case['verb'])
    return bool(frame and frame['frame'] == 'V1' and words[-1] == case['verb'] + '-te')


def main():
    cases = json.loads(CASES.read_text(encoding='utf8'))
    frames = {r['lemma']: r for r in json.loads(FRAMES.read_text(encoding='utf8'))}
    with (ROOT / 'data/lexicon.csv').open(encoding='utf8', newline='') as f:
        lex = {r['qaroshi']: r for r in csv.DictReader(f)}
    passed = sum(evaluate(case, lex, frames) for case in cases)
    print(f'8.6 fixed editorial subset: {passed}/{len(cases)} match the restricted structural checks')
    print('No semantic accuracy, independent comprehension, or full 500-item coverage is measured.')
    if passed != len(cases):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
