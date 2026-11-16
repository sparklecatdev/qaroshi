"""Recognize the same-actor pronoun subset of the 8.6 action-desire frame."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'stress85'))
from validate_attempt import analyze_attempt


def analyze_want(sentence):
    result = {'status': 'outside_restricted_checker', 'semantic_validation': 'not performed'}
    parts = sentence.strip().rstrip('.!?').split()
    if not parts or parts[-1].split('-')[0] != 'rawëli':
        return result
    parts[-1] = 'kërawë' + parts[-1][len('rawëli'):]
    return analyze_attempt(' '.join(parts))
