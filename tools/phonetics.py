#!/usr/bin/env python3
"""Deterministic broad phonetic transcription for Qaroshi Standard 4.2.

All 26 sounds retain their established reference values. The /.../ forms
are phonemic IPA readings; stress and syllabification are convention-based.
They are not recordings or narrow acoustic transcriptions.
"""
from __future__ import annotations
import re
import unicodedata

# The 26 native letters in the alphabet chart's original order.
IPA = {
    'k':'k','a':'a','w':'w','t':'t','r':'ɾ','q':'q','o':'o','d':'d',
    'sh':'ʃ','z':'z','u':'u','ë':'ə','i':'i','g':'ɡ','kh':'x','zh':'ʒ',
    'e':'e','ng':'ŋ','h':'h','b':'b','p':'p','m':'m','s':'s','n':'n',
    'y':'j','l':'l'
}
LETTERS = tuple(IPA)
VOWELS = frozenset(('a','e','i','o','u','ë'))
GLIDES = frozenset(('r','l','w','y'))
DIGRAPHS = ('sh','zh','kh','ng')
# English-oriented *approximation* for users reading the Latin transcription.
# English cues are not IPA: /e o a q x ɾ/ have no exact General American equivalents.
SOUND_OUT = {
    'a':'ah','e':'eh','i':'ee','o':'oh','u':'oo','ë':'uh',
    'b':'b','d':'d','g':'g','h':'h','k':'k','kh':'kh',
    'l':'l','m':'m','n':'n','ng':'ng','p':'p','q':'q',
    'r':'r','s':'s','sh':'sh','t':'t','w':'w','y':'y',
    'z':'z','zh':'zh'
}

LEXEME = re.compile(r'[A-Za-zëË]+(?:-[A-Za-zëË]+)*')


def graphemes(word: str) -> list[str]:
    """Segment romanized Qaroshi greedily, treating four digraphs as units."""
    word = unicodedata.normalize('NFC', word).lower().replace('-', '')
    out = []
    i = 0
    while i < len(word):
        pair = word[i:i+2]
        c = pair if pair in DIGRAPHS else word[i]
        if c not in IPA:
            raise ValueError(f'Unknown Qaroshi letter {c!r} in {word!r}')
        out.append(c)
        i += len(c)
    return out


def syllabify(word: str) -> list[list[str]]:
    """Maximize legal medial onsets; split otherwise before last consonant."""
    letters = graphemes(word)
    vs = [i for i, g in enumerate(letters) if g in VOWELS]
    if len(vs) < 2:
        return [letters] if letters else []
    syllables = []
    start = 0
    for prev, next_vowel in zip(vs, vs[1:]):
        between = letters[prev+1:next_vowel]
        if not between:
            onset = 0  # Hiatus: adjacent vowels belong to different syllables.
        elif len(between) >= 2 and between[-1] in GLIDES and between[-2] not in GLIDES:
            onset = 2  # Permitted (C)(r/l/w/y) clusters.
        else:
            onset = 1  # Otherwise a single onset, with preceding codas.
        split = next_vowel - onset
        syllables.append(letters[start:split])
        start = split
    syllables.append(letters[start:])
    return syllables


def bare_ipa(word: str) -> str:
    groups = syllabify(word)
    stressed = max(0, len(groups)-2)
    out = []
    for i, syll in enumerate(groups):
        sound = ''.join(IPA[c] for c in syll)
        if len(groups) > 1 and i == stressed:
            sound = 'ˈ' + sound
        out.append(sound)
    return '.'.join(out)


def ipa_word(word: str) -> str:
    return '/' + bare_ipa(word) + '/'


def guide_word(word: str) -> str:
    groups = syllabify(word)
    stressed = max(0, len(groups)-2)
    return '-'.join((''.join(syll).upper() if len(groups)>1 and i==stressed else ''.join(syll))
                    for i, syll in enumerate(groups))


def sound_out_word(word: str) -> str:
    """Approximate English-friendly cues; preserves native marked consonants.

    A word with one syllable is unmarked; multisyllabic words show main
    penultimate stress by uppercasing the corresponding syllable.
    """
    groups=syllabify(word)
    stress=max(0,len(groups)-2)
    return '-'.join(''.join(SOUND_OUT[g] for g in syll).upper()
                    if len(groups)>1 and i==stress
                    else ''.join(SOUND_OUT[g] for g in syll)
                    for i,syll in enumerate(groups))


def _text(text: str, renderer) -> str:
    text = unicodedata.normalize('NFC', text)
    s = LEXEME.sub(lambda m:renderer(m.group()),text)
    return re.sub(r'\s+', ' ', s).strip()


def ipa_text(text: str) -> str:
    # Remove sentence-final punctuation *before* generating phonetic syllable dots.
    s = _text(re.sub(r'[.!?…]', '', text), bare_ipa)
    return '/' + s.strip() + '/'


def guide_text(text: str) -> str:
    return _text(text, guide_word)


def sound_out_text(text: str) -> str:
    return _text(text, sound_out_word)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Transcribe romanized Qaroshi into IPA and stress guide')
    ap.add_argument('text', nargs='+')
    args = ap.parse_args()
    text = ' '.join(args.text)
    print('IPA:', ipa_text(text))
    print('Reading guide:', guide_text(text))
    print('English-style sound-out:', sound_out_text(text))
